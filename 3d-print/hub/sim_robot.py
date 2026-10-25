"""sim_robot.py — an MG400 that lives in this process and answers like the mg400-base server.

Same calls and replies as mg400-base (`call("/status")`, `/move`, `/jog`, `/speed`, `/pump`, `/stop`,
`/check`, `/enable`, ...), so the slot picker's sequencer drives it without knowing. Joint limits and
reach come from sim/mg400_kin.py (the copy of mg400-base kinematics.py), the Z floor is the one the lab
server runs with (-160). The arm moves like the mg400-base follower: a straight line at up to
`MAX_SPEED * ratio / 100` mm/s with a RAMP_SECS speed ramp (`slew` is a copy of mg400-base driver.slew),
and `/jog_hold` keeps it cruising while a jog button is held.
"""
import math
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sim"))
import mg400_kin as kin  # noqa: E402

MAX_SPEED = 300.0        # mm/s at 100 %; the slot picker caps the ratio at 30 %
R_SPEED = 90.0           # deg/s at 100 %
Z_FLOOR = -160.0
HOME = (300.0, 0.0, -50.0, 33.0)
PUMP_MODES = ("off", "suck", "blow")
RAMP_SECS = 0.5          # rest → speed cap (mg400-base RAMP_SECS)
JOG_TTL = 0.35           # s a /jog_hold call keeps the arm moving (mg400-base driver.JOG_TTL)
JOG_LEAD_SECS = 0.3      # the held-jog target rides braking distance + this much travel ahead
JOG_MIN_LEAD = 0.5       # mm


def slew(setpoint, vel, target, max_lin, lin_acc, max_ang, ang_acc, dt):
    """One follower tick (copy of mg400-base driver.slew): X/Y/Z as one vector, speed and acceleration
    capped, braked early enough to arrive at rest; R ramped the same way on its own."""
    sp, v = list(setpoint), list(vel)
    delta = [target[i] - sp[i] for i in range(3)]
    dist = math.sqrt(sum(d * d for d in delta))
    if dist > 1e-9:
        scale = min(max_lin, math.sqrt(2.0 * lin_acc * dist)) / dist
        desired = [d * scale for d in delta]
    else:
        desired = [0.0, 0.0, 0.0]
    dv = [desired[i] - v[i] for i in range(3)]
    dv_len = math.sqrt(sum(d * d for d in dv))
    if dv_len > lin_acc * dt:
        dv = [d * lin_acc * dt / dv_len for d in dv]
    v[:3] = [v[i] + dv[i] for i in range(3)]
    step = [v[i] * dt for i in range(3)]
    step_len = math.sqrt(sum(s * s for s in step))
    heading_in = sum(step[i] * delta[i] for i in range(3)) > 0
    if dist <= 1e-9 or (heading_in and step_len >= dist):
        sp[:3] = list(target[:3])
        v[:3] = [0.0, 0.0, 0.0]
    else:
        sp[:3] = [sp[i] + step[i] for i in range(3)]
    remaining = target[3] - sp[3]
    direction = 1.0 if remaining >= 0 else -1.0
    v_des = min(max_ang, math.sqrt(2.0 * ang_acc * abs(remaining))) * direction
    v[3] += max(-ang_acc * dt, min(ang_acc * dt, v_des - v[3]))
    r_step = v[3] * dt
    if abs(r_step) >= abs(remaining) and (r_step >= 0) == (remaining >= 0):
        sp[3] = target[3]
        v[3] = 0.0
    else:
        sp[3] += r_step
    return sp, v


class SimRobot:
    def __init__(self, pose=HOME, speed_ratio=10):
        self.lock = threading.Lock()
        self.pose = list(pose)
        self.target = None
        self.vel = [0.0, 0.0, 0.0, 0.0]
        self.jog = None          # held jog: {"axis": 0-3, "sign": ±1, "deadline"}
        self.speed_ratio = speed_ratio
        self.enabled = True
        self.pump = "off"
        self.alarm = None
        threading.Thread(target=self._follow, daemon=True).start()

    # ---- the mg400-base API ----
    def call(self, path, body=None):
        body = body or {}
        path = path.split("?")[0].rstrip("/")
        handler = {
            "/status": self._status, "/move": self._move, "/jog": self._jog, "/jog_hold": self._jog_hold,
            "/speed": self._speed,
            "/pump": self._pump, "/stop": self._stop, "/check": self._check, "/enable": self._enable,
            "/disable": self._disable, "/connect": lambda b: {"ok": True, "ip": "simulation"},
            "/clear_error": self._clear, "/z_floor": lambda b: {"ok": True, "z_floor": Z_FLOOR},
        }.get(path)
        if handler is None:
            return {"ok": False, "error": f"simulation has no {path}"}
        with self.lock:
            return handler(body)

    def _status(self, _):
        j = kin.inverse(*self.pose[:3])
        joints = [0.0, 0.0, 0.0, 0.0] if j is None else [j[0], j[1], j[2], self.pose[3] - j[0]]
        return {"connected": True, "mode_name": "ENABLED" if self.enabled else "DISABLED",
                "enabled": self.enabled, "error": bool(self.alarm), "alarm_ids": [self.alarm] if self.alarm else [],
                "fault_label": self.alarm, "pose": [round(v, 3) for v in self.pose],
                "joints": [round(v, 3) for v in joints], "target": self.target, "speed_ratio": self.speed_ratio,
                "pump_mode": self.pump, "servo_active": self.enabled, "z_floor": Z_FLOOR, "simulation": True}

    def _goal(self, x, y, z, r):
        if not self.enabled:
            return {"ok": False, "error": "robot is disabled"}
        clamped = {"x": x, "y": y, "z": max(z, Z_FLOOR), "r": r}
        ok, reason, _ = kin.check(clamped["x"], clamped["y"], clamped["z"])
        if not ok:
            return {"ok": False, "error": f"out of reach: {reason}"}
        self.target = [clamped["x"], clamped["y"], clamped["z"], clamped["r"]]
        return {"ok": True, "clamped": dict(clamped)}

    def _move(self, b):
        try:
            x, y, z = (float(b[k]) for k in ("x", "y", "z"))
            r = float(b.get("r", self.pose[3]))
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
        base = list(self.target or self.pose)
        base["xyzr".index(axis)] += delta
        return self._goal(*base)

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
        if not sign:
            if self.jog is not None:
                self.jog = None
                self._brake()
            return {"ok": True}
        if not self.enabled:
            return {"ok": False, "error": "robot is disabled"}
        i = "xyzr".index(axis)
        if self.jog is None or (self.jog["axis"], self.jog["sign"]) != (i, sign):
            self.jog = {"axis": i, "sign": sign}
        self.jog["deadline"] = time.monotonic() + JOG_TTL
        return {"ok": True}

    def _speed(self, b):
        try:
            ratio = int(b["ratio"])
        except (KeyError, TypeError, ValueError):
            return {"ok": False, "error": "ratio must be 1-100"}
        if not 1 <= ratio <= 100:
            return {"ok": False, "error": "ratio must be 1-100"}
        self.speed_ratio = ratio
        return {"ok": True, "ratio": ratio}

    def _pump(self, b):
        if b.get("mode") not in PUMP_MODES:
            return {"ok": False, "error": "mode: off, suck or blow"}
        self.pump = b["mode"]
        return {"ok": True, "mode": self.pump}

    def _stop(self, _):
        self.jog = None
        self._brake()
        return {"ok": True}

    def _check(self, b):
        try:
            x, y, z = (float(b[k]) for k in ("x", "y", "z"))
        except (KeyError, TypeError, ValueError):
            return {"ok": False, "error": "x, y, z must be numbers"}
        ok, reason, joints = kin.check(x, y, z)
        return {"ok": True, "reachable": ok, "reason": reason,
                "joints": None if joints is None else [round(v, 2) for v in joints]}

    def _enable(self, _):
        self.enabled = True
        return {"ok": True}

    def _disable(self, _):
        self.enabled, self.target, self.jog, self.vel = False, None, None, [0.0, 0.0, 0.0, 0.0]
        return {"ok": True}

    def _clear(self, _):
        self.alarm = None
        return {"ok": True}

    # ---- motion ----
    def _caps(self):
        lin, ang = MAX_SPEED * self.speed_ratio / 100, R_SPEED * self.speed_ratio / 100
        return lin, lin / RAMP_SECS, ang, ang / RAMP_SECS

    def _brake(self):
        """Smooth stop like mg400-base hold(): the target becomes the braking point."""
        if self.target is None:
            return
        lin, lin_acc, _, ang_acc = self._caps()
        v = self.vel
        tgt = list(self.pose)
        for i in range(3):
            tgt[i] += v[i] * math.hypot(*v[:3]) / (2 * lin_acc)
        tgt[3] += math.copysign(v[3] * v[3] / (2 * ang_acc), v[3])
        self.target = tgt

    def _jog_target(self):
        """Held jog: the target rides a braking distance + JOG_LEAD_SECS ahead, kept above the floor and in reach."""
        jog = self.jog
        if time.monotonic() > jog["deadline"]:        # no call for JOG_TTL: the page is gone
            self.jog = None
            self._brake()
            return
        lin, lin_acc, ang, ang_acc = self._caps()
        if jog["axis"] == 3:
            lead = ang * ang / (2 * ang_acc) + ang * JOG_LEAD_SECS
        else:
            lead = lin * lin / (2 * lin_acc) + lin * JOG_LEAD_SECS
        while lead >= JOG_MIN_LEAD:
            tgt = list(self.pose)
            tgt[jog["axis"]] += jog["sign"] * lead
            tgt[2] = max(tgt[2], Z_FLOOR)
            if kin.check(*tgt[:3])[0]:
                self.target = tgt
                return
            lead /= 2
        self.target = self.target or list(self.pose)
        self._brake()

    def _follow(self, dt=0.02):
        while True:
            time.sleep(dt)
            with self.lock:
                if self.jog is not None:
                    self._jog_target()
                if self.target is None:
                    continue
                lin, lin_acc, ang, ang_acc = self._caps()
                self.pose, self.vel = slew(self.pose, self.vel, self.target, lin, lin_acc, ang, ang_acc, dt)
                if self.pose == list(self.target) and not any(self.vel):
                    self.target = None
