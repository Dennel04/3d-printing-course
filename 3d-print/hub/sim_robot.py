"""sim_robot.py — an MG400 that lives in this process and answers like the mg400-base server.

Same calls and replies as mg400-base (`call("/status")`, `/move`, `/jog`, `/speed`, `/pump`, `/stop`,
`/check`, `/enable`, ...), so the slot picker's sequencer drives it without knowing. Joint limits and
reach come from sim/mg400_kin.py (the copy of mg400-base kinematics.py), the Z floor is the one the lab
server runs with (-160). The arm moves in a straight line at `MAX_SPEED * ratio / 100` mm/s.
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


class SimRobot:
    def __init__(self, pose=HOME, speed_ratio=10):
        self.lock = threading.Lock()
        self.pose = list(pose)
        self.target = None
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
            "/status": self._status, "/move": self._move, "/jog": self._jog, "/speed": self._speed,
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
        self.target = None
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
        self.enabled, self.target = False, None
        return {"ok": True}

    def _clear(self, _):
        self.alarm = None
        return {"ok": True}

    # ---- motion ----
    def _follow(self, dt=0.02):
        while True:
            time.sleep(dt)
            with self.lock:
                if self.target is None:
                    continue
                v = MAX_SPEED * self.speed_ratio / 100 * dt
                w = R_SPEED * self.speed_ratio / 100 * dt
                d = math.dist(self.pose[:3], self.target[:3])
                k = 1.0 if d <= v else v / d
                for i in range(3):
                    self.pose[i] += (self.target[i] - self.pose[i]) * k
                dr = self.target[3] - self.pose[3]
                self.pose[3] += max(-w, min(w, dr))
                if d <= v and abs(dr) <= w:
                    self.pose = list(self.target)
                    self.target = None
