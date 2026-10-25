"""real_robot.py — the real MG400, driven from the hub process itself (no mg400-base server).

Same calls and replies as sim_robot.py and the old mg400-base HTTP API (`call("/status")`, `/move`, `/jog`,
`/jog_hold`, `/speed`, `/pump`, `/stop`, `/check`, `/connect`, `/enable`, ...), so the slot picker and the hub
drive it without knowing. The TCP/IP driver is mg400/driver.py: a ServoP follower thread with speed and
acceleration caps (smooth start and stop), a joint-limit guard (mg400/kinematics.py) and the Z floor clamp
(mg400/limits.py).
"""
import threading

from mg400 import kinematics
from mg400.driver import DobotError, DobotMG400
from mg400.limits import clamp_pose

DEFAULT_IP = "192.168.1.6"
Z_FLOOR = -160.0         # lab floor for the slot picker rig (what mg400-base ran with: --z-floor -160)
MAX_LIN_VEL = 200.0      # mm/s at 100 %
MAX_ANG_VEL = 90.0       # deg/s at 100 %
RAMP_SECS = 0.5          # rest -> speed cap, and the same to brake
SUCK_DO, BLOW_DO = 2, 1  # pump box: DO2 suck, DO1 blow (verified in the lab)


class RealRobot:
    def __init__(self, ip=DEFAULT_IP, z_floor=Z_FLOOR, speed_ratio=10, **driver_kw):
        self.ip, self.z_floor, self.speed_ratio = ip, z_floor, speed_ratio
        self.driver_kw = driver_kw        # tests point the driver at a fake robot (ports=...)
        self.robot = None
        self.lock = threading.Lock()      # connect / disconnect only; the driver is thread-safe

    # ---- the API ----
    def call(self, path, body=None):
        body = body or {}
        path = path.split("?")[0].rstrip("/")
        handler = {
            "/status": self._status, "/connect": self._connect, "/disconnect": self._disconnect,
            "/enable": self._enable, "/disable": self._disable, "/clear_error": self._clear,
            "/speed": self._speed, "/stop": self._stop, "/pump": self._pump, "/move": self._move,
            "/jog": self._jog, "/jog_hold": self._jog_hold, "/check": self._check, "/z_floor": self._z_floor,
            "/recover": self._recover,
        }.get(path)
        if handler is None:
            return {"ok": False, "error": f"real robot has no {path}"}
        if path not in ("/status", "/connect", "/check", "/z_floor"):
            r = self.robot
            if r is None or not r.is_connected():
                err = r.get_state().get("link_error") if r is not None else None
                return {"ok": False, "error": f"Connection lost ({err}). Press Connect." if err else "Not connected"}
        try:
            return handler(body)
        except DobotError as e:
            return {"ok": False, "error": str(e), "errid": e.errid}

    def clamp(self, x, y, z, r):
        return clamp_pose(x, y, z, r, self.z_floor)

    def _reply(self, errid_resp):
        errid, resp = errid_resp
        return {"ok": errid == 0, "errid": errid, "resp": resp, **({} if errid == 0 else {"error": f"ErrorID {errid}: {resp}"})}

    def _apply_motion(self):
        frac = self.speed_ratio / 100.0
        self.robot.set_max_velocity(frac * MAX_LIN_VEL, frac * MAX_ANG_VEL)
        self.robot.set_max_accel(frac * MAX_LIN_VEL / RAMP_SECS, frac * MAX_ANG_VEL / RAMP_SECS)

    def _pump_mode(self, bits):
        suck, blow = bool(bits & (1 << (SUCK_DO - 1))), bool(bits & (1 << (BLOW_DO - 1)))
        return "conflict" if suck and blow else "suck" if suck else "blow" if blow else "off"

    def _status(self, _):
        r = self.robot
        st = DobotMG400._blank_state() if r is None else r.get_state()
        st["pump_mode"] = self._pump_mode(st.get("digital_out", 0))
        st["target"] = None if r is None else r.get_target()
        st["ramp_secs"] = RAMP_SECS
        st["z_floor"] = self.z_floor
        st["speed_ratio"] = self.speed_ratio
        st["ip"] = self.ip
        return st

    def _connect(self, b):
        ip = b.get("ip") or self.ip
        with self.lock:
            if self.robot is not None:
                self.robot.close()
                self.robot = None
            robot = DobotMG400(ip, **self.driver_kw)
            try:
                robot.connect()
            except DobotError as e:
                return {"ok": False, "error": f"Could not connect to {ip}: {e}"}
            self.robot, self.ip = robot, ip
        return {"ok": True, "ip": ip}

    def _disconnect(self, _):
        with self.lock:
            if self.robot is not None:
                self.robot.close()
                self.robot = None
        return {"ok": True}

    def _enable(self, _):
        r = self.robot
        try:
            r.clear_error()
        except DobotError:
            pass
        reply = self._reply(r.enable())
        if reply["ok"]:
            r.start_servo()
            self._apply_motion()
            r.speed_factor(self.speed_ratio)
        return reply

    def _disable(self, _):
        self.robot.stop_servo()
        return self._reply(self.robot.disable())

    def _clear(self, _):
        return self._reply(self.robot.clear_error())

    def _speed(self, b):
        try:
            ratio = int(b["ratio"])
        except (KeyError, TypeError, ValueError):
            return {"ok": False, "error": "ratio must be 1-100"}
        if not 1 <= ratio <= 100:
            return {"ok": False, "error": "ratio must be 1-100"}
        self.speed_ratio = ratio
        self._apply_motion()
        return {**self._reply(self.robot.speed_factor(ratio)), "ratio": ratio}

    def _stop(self, _):
        self.robot.hold()          # smooth stop: brake along the current direction
        return {"ok": True}

    def _pump(self, b):
        if b.get("mode") not in ("suck", "blow", "off"):
            return {"ok": False, "error": "mode: off, suck or blow"}
        return {**self._reply(self.robot.set_pump(b["mode"], SUCK_DO, BLOW_DO)), "mode": b["mode"]}

    def _goal(self, x, y, z, r):
        if not self.robot.get_state()["servo_active"]:
            return {"ok": False, "error": "the follower is not running — press Enable"}
        x, y, z, r = self.clamp(x, y, z, r)
        self.robot.set_target_pose(x, y, z, r)
        return {"ok": True, "clamped": {"x": round(x, 2), "y": round(y, 2), "z": round(z, 2), "r": round(r, 2)}}

    def _move(self, b):
        try:
            x, y, z = (float(b[k]) for k in ("x", "y", "z"))
            r = float(b.get("r", self.robot.get_state()["pose"][3]))
        except (KeyError, TypeError, ValueError):
            return {"ok": False, "error": "x, y, z (and r) must be numbers"}
        return self._goal(x, y, z, r)

    def _jog(self, b):
        axis = b.get("axis")
        if axis not in ("x", "y", "z", "r"):
            return {"ok": False, "error": "axis must be x, y, z or r"}
        try:
            delta = float(b["delta"])
        except (KeyError, TypeError, ValueError):
            return {"ok": False, "error": "delta must be a number"}
        base = self.robot.get_target() or list(self.robot.get_state()["pose"])
        base["xyzr".index(axis)] += delta
        reply = self._goal(*base)
        if reply.get("ok"):
            reply["target"] = reply["clamped"]
        return reply

    def _jog_hold(self, b):
        axis = b.get("axis", "x")
        if axis not in ("x", "y", "z", "r"):
            return {"ok": False, "error": "axis must be x, y, z or r"}
        try:
            sign = int(b.get("dir", 0))
        except (TypeError, ValueError):
            return {"ok": False, "error": "dir must be -1, 0 or 1"}
        if sign not in (-1, 0, 1):
            return {"ok": False, "error": "dir must be -1, 0 or 1"}
        if sign and not self.robot.get_state()["servo_active"]:
            return {"ok": False, "error": "the follower is not running — press Enable"}
        self.robot.jog_hold(axis, sign, clamp=self.clamp)
        return {"ok": True}

    def _check(self, b):
        try:
            x, y, z = (float(b[k]) for k in ("x", "y", "z"))
        except (KeyError, TypeError, ValueError):
            return {"ok": False, "error": "x, y, z must be numbers"}
        ok, reason, joints = kinematics.check(x, y, z)
        return {"ok": True, "reachable": ok, "reason": reason,
                "joints": None if joints is None else [round(v, 2) for v in joints]}

    def _z_floor(self, b):
        if "z" in b:
            try:
                self.z_floor = float(b["z"])
            except (TypeError, ValueError):
                return {"ok": False, "error": "z must be a number"}
        return {"ok": True, "z_floor": self.z_floor}

    def _recover(self, _):
        ok, msg = self.robot.recover_from_limit()
        if ok:
            self.robot.start_servo()
            self._apply_motion()
            self.robot.speed_factor(self.speed_ratio)
        return {"ok": ok, "message": msg, "error": None if ok else msg}
