"""slot_picker.py — MG400 + Gridfinity grid in a web page (http://127.0.0.1:8010).

Drive: click a cell, the suction cup goes up to travel_z, across, and down to the hover height
(never into a pocket). Edit layout: add, name, type, move and delete holders (saved to layout.json).
Test: choose the input / workstation / output holders, teach their pick and place points, run the
glass cycle (cycle.py) one glass or four at a time and save each round into docs/refit_test.csv.

Talks to the mg400-base server (http://127.0.0.1:8000), which must already be connected and enabled.
Cell X/Y come from the 24.10.26 three-cell fit in ../calibration/cells.py.

Usage: python slot_picker.py [--port 8010] [--check]
"""
import argparse
import csv
import json
import math
import sys
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
LETTERS = "ABCDEFG"
NUMBERS = [5, 4, 3, 2, 1, -1, -2, -3, -4, -5]  # operator view, left to right
REFIT_CSV = HERE.parent / "docs" / "refit_test.csv"

FRAMES = HERE / "frames"  # tool camera JPEGs: the View button, the cycle and Claude's captures; newest one is shown
PROBES = HERE / "probes"  # one folder per probe run: probe.csv + a frame per step, data for touch detection
PROBE_AXES = {"z-": (0, 0, -1), "x+": (1, 0, 0), "x-": (-1, 0, 0), "y+": (0, 1, 0), "y-": (0, -1, 0)}
PROBE_HEADER = ["time", "step", "target_x", "target_y", "target_z", "x", "y", "z", "r",
                "adc", "vacuum_adc", "pump", "frame"]
sys.path.insert(0, str(HERE.parent / "calibration"))
sys.path.insert(0, str(HERE.parent / "tool-camera"))
import cells as calibration  # noqa: E402  single source of the grid fit (G-1, E+3, D-2)
from capture import open_port, read_frame  # noqa: E402
import cycle  # noqa: E402
from pressure import PressureMonitor  # noqa: E402

_, cell_robot = calibration.fit()

CELL_NAMES = [f"{letter}{n:+d}" for letter in LETTERS for n in NUMBERS]
HOLDER_KEYS = ("name", "type", "cells", "status", "no_go", "teach")


class ToolCamera:
    """The only owner of the XIAO COM port. While someone wants frames (the live view, View,
    a cycle snapshot) it keeps the port open and asks for a frame every 1/fps s; after idle_s
    without anyone wanting them it closes the port, so capture.py can use it again."""

    def __init__(self, port, fps=4.0, idle_s=10.0):
        self.port, self.period, self.idle_s = port, 1 / fps, idle_s
        self.cond = threading.Condition()
        self.jpeg, self.seq, self.wanted = None, 0, 0.0
        self.state = {"open": False, "fps": 0.0, "error": None}
        threading.Thread(target=self._loop, daemon=True).start()

    def wait_frame(self, after, timeout=8.0):
        """(jpeg, seq) of the first frame with seq > after, or (None, seq) on timeout."""
        deadline = time.time() + timeout
        with self.cond:
            while self.seq <= after:
                self.wanted = time.time()
                self.cond.notify_all()
                left = deadline - time.time()
                if left <= 0:
                    return None, self.seq
                self.cond.wait(min(left, 1.0))
            self.wanted = time.time()
            return self.jpeg, self.seq

    def fresh(self, timeout=8.0):
        """A frame asked for after this call, not one already on its way (e.g. from before the arm stopped)."""
        jpeg, _ = self.wait_frame(self.seq + 1, timeout)
        if jpeg is None:
            raise RuntimeError(f"camera: {self.state['error'] or 'no frame'}")
        return jpeg

    def _loop(self):
        ser, times = None, []
        while True:
            with self.cond:
                if time.time() - self.wanted > self.idle_s:
                    if ser is not None:
                        ser.close()
                        ser, times = None, []
                        self.state.update(open=False, fps=0.0)
                    self.cond.wait(1.0)
                    continue
            t0 = time.time()
            try:
                if ser is None:
                    ser = open_port(self.port)
                    self.state["open"] = True
                jpeg = read_frame(ser)
            except Exception as exc:
                if ser is not None:
                    ser.close()
                ser, times = None, []
                self.state.update(open=False, fps=0.0, error=f"{self.port}: {exc}"[:200])
                time.sleep(2.0)
                continue
            with self.cond:
                self.jpeg, self.seq = jpeg, self.seq + 1
                self.cond.notify_all()
            times = [t for t in times if t > t0 - 3] + [t0]
            self.state.update(error=None, fps=round((len(times) - 1) / (t0 - times[0]), 1) if len(times) > 1 else 0.0)
            time.sleep(max(0.0, self.period - (time.time() - t0)))


def load_layout():
    return json.loads((HERE / "layout.json").read_text(encoding="utf-8"))


def save_layout(layout):
    (HERE / "layout.json").write_text(json.dumps(layout, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def snapshot(camera, prefix):
    jpeg = camera.fresh()
    FRAMES.mkdir(exist_ok=True)
    out = FRAMES / time.strftime(f"{prefix}-%Y%m%d-%H%M%S.jpg")
    out.write_bytes(jpeg)
    return out.name


def is_no_go(holder, types):
    return bool(holder.get("no_go", types.get(holder.get("type"), {}).get("no_go")))


def check_holders(holders, types):
    """Validate holders sent by the layout editor; raises ValueError with the first problem."""
    names, used = set(), {}
    for h in holders:
        name = str(h.get("name", "")).strip()
        if not name:
            raise ValueError("every holder needs a name")
        if name in names:
            raise ValueError(f"two holders are called {name!r}")
        names.add(name)
        if h.get("type") not in types:
            raise ValueError(f"{name}: unknown type {h.get('type')!r}")
        if not h.get("cells"):
            raise ValueError(f"{name}: no cells")
        for c in h["cells"]:
            if c not in CELL_NAMES:
                raise ValueError(f"{name}: no cell {c!r} on the grid")
            if c in used:
                raise ValueError(f"{c} is in both {used[c]} and {name}")
            used[c] = name


def build_cells(layout):
    motion, types = layout["motion"], layout["types"]
    holder_of = {c: h for h in layout["holders"] for c in h["cells"]}
    cells = []
    for letter in LETTERS:
        for n in NUMBERS:
            name = f"{letter}{n:+d}"
            x, y = cell_robot(name)
            radius = math.hypot(x, y)
            holder = holder_of.get(name)
            reason = None
            if not motion["radius_min"] <= radius <= motion["radius_max"]:
                reason = f"r {radius:.0f} mm outside {motion['radius_min']:.0f}-{motion['radius_max']:.0f}"
            elif holder and is_no_go(holder, types):
                reason = f"{holder['name']}: no-go"
            cells.append({"name": name, "x": round(x, 2), "y": round(y, 2), "radius": round(radius, 1),
                          "holder": holder["name"] if holder else None,
                          "type": holder.get("type") if holder else None, "blocked": reason})
    return cells


class Mg400:
    def __init__(self, base):
        self.base = base

    def call(self, path, body=None):
        req = urllib.request.Request(self.base + path,
                                     data=None if body is None else json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        return json.load(urllib.request.urlopen(req, timeout=5))


class Sequencer:
    """Runs one action list at a time (a goto or the glass cycle); Stop cancels it and holds the arm.
    The pump is left as it is on Stop or error: switching it off would drop a carried glass."""

    def __init__(self, robot, layout, camera, pressure):
        self.robot, self.layout, self.camera, self.pressure = robot, layout, camera, pressure
        self.lock = threading.Lock()
        self.cancel = threading.Event()
        self.state = {"busy": False, "cell": None, "step": "idle", "error": None, "cycle": None}

    def ready_status(self):
        motion = self.layout["motion"]
        status = self.robot.call("/status")
        self._check(status)
        if status.get("speed_ratio", 100) > motion["max_speed_ratio"]:
            raise ValueError(f"speed {status['speed_ratio']}% > {motion['max_speed_ratio']}%: lower it in mg400-base first")
        return status

    def goto(self, cell, hover_z):
        motion = self.layout["motion"]
        if cell["blocked"]:
            raise ValueError(f"{cell['name']} blocked: {cell['blocked']}")
        if not motion["min_hover_z"] <= hover_z <= motion["travel_z"]:
            raise ValueError(f"hover Z must be {motion['min_hover_z']} … {motion['travel_z']}")
        status = self.ready_status()
        cx, cy = status["pose"][0], status["pose"][1]
        self._start([("move", "up", cx, cy, motion["travel_z"]),
                     ("move", "across", cell["x"], cell["y"], motion["travel_z"]),
                     ("move", "down", cell["x"], cell["y"], hover_z)], cell=cell["name"])

    def go_above(self, x, y, label):
        """To x/y at the cycle travel height (lower than the Drive travel_z), for teaching."""
        status = self.ready_status()
        tz = self.layout["cycle"]["travel_z"]
        cx, cy, cz = status["pose"][:3]
        self._start([("move", "up", cx, cy, max(cz, tz)), ("move", label, x, y, tz)])

    def run_cycle(self, glasses, rnd, by_name):
        if not self.layout["cycle"].get("workstation_step") and len(glasses) != 1:
            raise ValueError("transfer test: one glass at a time (tick Workstation step for the full round)")
        cycle.check_ready(self.layout, by_name, glasses)
        status = self.ready_status()
        tz = self.layout["cycle"]["travel_z"]
        cx, cy, cz = status["pose"][:3]
        actions = [("move", "up to travel height", cx, cy, max(cz, tz))]
        for g in glasses:
            actions += cycle.plan_glass(self.layout, g, by_name)
        actions.append(("pump", "off"))
        results = {str(g): {f: False for f in cycle.fields(self.layout)} for g in glasses}
        self._start(actions, cycle_state={"id": time.time(), "round": rnd, "glasses": glasses,
                                          "results": results, "frames": [], "grips": []})

    def probe(self, axis, step, distance, suction, label):
        """Step from the current pose along axis, one step at a time; at each step (and at the start)
        record pose, Atom ADC/vacuum and a fresh tool camera frame into probes/<run>/. No touch is
        detected yet: this only collects the data to tune it. Ends back at the start pose."""
        pr = self.layout["probe"]
        if axis not in PROBE_AXES:
            raise ValueError(f"probe axis: {', '.join(PROBE_AXES)}")
        if not 0.1 <= step <= 2:
            raise ValueError("probe step 0.1-2 mm")
        if not step <= distance <= pr["max_distance_mm"]:
            raise ValueError(f"probe distance {step}-{pr['max_distance_mm']} mm")
        x0, y0, z0 = self.ready_status()["pose"][:3]
        safe = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in label.strip())[:40] or "probe"
        run = PROBES / time.strftime(f"%Y%m%d-%H%M%S-{safe}-{axis}")
        run.mkdir(parents=True)
        info = {"dir": run.name, "rows": 0, "last": None}
        dx, dy, dz = PROBE_AXES[axis]
        n = int(round(distance / step))
        actions = [("baseline",)]  # pump off: vacuum is measured against this
        if suction:
            actions += [("pump", "suck"), ("wait", pr["suck_wait_s"])]
        actions.append(("probe_sample", run, info, 0, x0, y0, z0))
        for i in range(1, n + 1):
            x, y, z = (round(v + d * step * i, 3) for v, d in ((x0, dx), (y0, dy), (z0, dz)))
            actions += [("move", f"probe {axis} {i}/{n}", x, y, z, min(0.5, step / 2)),
                        ("probe_sample", run, info, i, x, y, z)]
        if suction:
            actions.append(("pump", "off"))  # release at the bottom, not on the way up
        actions.append(("move", "probe: back to start", x0, y0, z0))
        self._start(actions, probe_state=info)

    def stop(self):
        self.cancel.set()
        self.robot.call("/stop", {})

    def _start(self, actions, cell=None, cycle_state=None, probe_state=None):
        with self.lock:
            if self.state["busy"]:
                raise ValueError("already moving")
            self.cancel.clear()
            self.state = {"busy": True, "cell": cell, "step": "start", "error": None,
                          "cycle": cycle_state if cycle_state is not None else self.state.get("cycle"),
                          "probe": probe_state if probe_state is not None else self.state.get("probe")}
        threading.Thread(target=self._run, args=(actions, cycle_state), daemon=True).start()

    def _run(self, actions, cyc):
        r = self.layout["calibration"]["tool_r"]
        try:
            for act in actions:
                if self.cancel.is_set():
                    raise RuntimeError("stopped by user")
                kind = act[0]
                if kind == "move":
                    label, x, y, z = act[1:5]
                    self.state["step"] = label
                    self._move(x, y, z, r, *act[5:])
                elif kind == "pump":
                    self.state["step"] = f"pump {act[1]}"
                    reply = self.robot.call("/pump", {"mode": act[1]})
                    if not reply.get("ok"):
                        raise RuntimeError(f"pump refused: {reply}")
                elif kind == "wait":
                    if self.cancel.wait(act[1]):
                        raise RuntimeError("stopped by user")
                elif kind == "mark":
                    cyc["results"][str(act[1])][act[2]] = True
                elif kind == "snap":
                    try:
                        cyc["frames"].append(snapshot(self.camera, act[1]))
                    except Exception as exc:  # a missing camera must not stop the robot mid-cycle
                        cyc["frames"].append(f"no frame: {exc}")
                elif kind == "baseline":
                    self.pressure.mark_baseline()
                elif kind == "grip":  # record only: lost pressure data must not stop the cycle
                    cyc["grips"].append(self._grip(act[1], act[2]))
                elif kind == "probe_sample":
                    self._probe_sample(*act[1:])
            self.state["step"] = "done" if cyc else "arrived"
        except Exception as exc:
            self.state["error"] = str(exc)[:200]
            self.state["step"] = "stopped"
        finally:
            self.state["busy"] = False

    def _move(self, x, y, z, r, tolerance=None):
        motion = self.layout["motion"]
        tolerance = tolerance or motion["arrive_tolerance_mm"]
        start = self.robot.call("/status")["pose"]
        reply = self.robot.call("/move", {"x": x, "y": y, "z": z, "r": r})
        if not reply.get("ok"):
            raise RuntimeError(f"move refused: {reply}")
        c = reply.get("clamped", {})
        if any(abs(c.get(k, v) - v) > 0.5 for k, v in (("x", x), ("y", y), ("z", z))):
            self.robot.call("/stop", {})
            raise RuntimeError(f"mg400-base clamped the target to {c}; stopped")
        # long moves at low speed take a while: allow 2 mm/s on top of the fixed timeout
        timeout = motion["step_timeout_s"] + math.dist(start[:3], (x, y, z)) / 2
        t0 = time.time()
        while True:
            if self.cancel.is_set():
                raise RuntimeError("stopped by user")
            s = self.robot.call("/status")
            self._check(s)
            p = s["pose"]
            if max(abs(p[0] - x), abs(p[1] - y), abs(p[2] - z)) < tolerance and abs(p[3] - r) < 0.5:
                return
            if time.time() - t0 > timeout:
                self.robot.call("/stop", {})
                raise RuntimeError(f"not arriving, pose {p}")
            time.sleep(0.1)

    def _probe_sample(self, run, info, i, x, y, z):
        """One probe.csv row; written at once, so a run stopped halfway keeps its rows."""
        self.state["step"] = f"probe sample {i}"
        if self.cancel.wait(self.layout["probe"]["settle_s"]):
            raise RuntimeError("stopped by user")
        s = self.robot.call("/status")
        try:
            frame = f"step-{i:02d}.jpg"
            (run / frame).write_bytes(self.camera.fresh())
        except Exception as exc:  # a missing camera still leaves the pose and pressure rows
            frame = f"no frame: {exc}"
        adc, vac = self.pressure.mean(), self.pressure.vacuum()
        row = [time.strftime("%H:%M:%S"), i, x, y, z, *(round(v, 3) for v in s["pose"]),
               "" if adc is None else round(adc, 1), "" if vac is None else round(vac, 1),
               s.get("pump_mode") or "", frame]
        path = run / "probe.csv"
        new = not path.exists()
        with path.open("a", newline="", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            if new:
                w.writerow(PROBE_HEADER)
            w.writerow(row)
        info["rows"] += 1
        info["last"] = dict(zip(PROBE_HEADER, row))

    def _grip(self, glass, what):
        vac, need = self.pressure.vacuum(), self.layout["cycle"]["grip_min_vacuum_adc"]
        if vac is None:
            return f"g{glass} {what}: no pressure data ({self.pressure.state()['error']})"
        return f"g{glass} {what}: vacuum {vac:.0f} ADC " + ("ok" if vac >= need else f"LOW (< {need})")

    @staticmethod
    def _check(s):
        if s.get("error") or s.get("alarm_ids") or not s.get("enabled"):
            raise RuntimeError(f"robot not ready: {s.get('mode_name')} {s.get('alarm_ids')} {s.get('fault_label') or ''}")


def latest_frame():
    frames = sorted(FRAMES.glob("*.jpg"), key=lambda p: p.stat().st_mtime)
    return frames[-1] if frames else None


def make_handler(layout, seq, port):
    table = {}  # cells and by_name, rebuilt when the layout editor saves

    def rebuild():
        table["cells"] = build_cells(layout)
        table["by_name"] = {c["name"]: c for c in table["cells"]}

    rebuild()
    # Only this page may drive the robot: other sites open in the same browser could otherwise
    # POST here (CSRF), and a foreign Host header means DNS rebinding.
    hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
    origins = {f"http://{h}" for h in hosts}

    def idle():
        if seq.state["busy"]:
            raise ValueError("the robot is moving; wait or press STOP")

    def teach_point(role, what):
        """Store the arm's current pose as a taught value of the role's holder."""
        idle()
        if role not in cycle.ROLES:
            raise ValueError(f"unknown role {role!r}")
        h = cycle.holder(layout, role)
        s = seq.robot.call("/status")
        seq._check(s)
        x, y, z, r = s["pose"]
        if abs(r - layout["calibration"]["tool_r"]) > 0.5:
            raise ValueError(f"R is {r:.1f}, teach at R {layout['calibration']['tool_r']}")
        t = cycle.teach(h)
        if what in ("pick_z", "place_z"):
            if what not in cycle.NEEDS[role]:
                raise ValueError(f"{role} has no {what}")
            t[what] = round(z, 2)
        elif what == "xy":
            c = table["by_name"][cycle.slot_cell(layout, role, 1)]
            dx, dy = x - c["x"], y - c["y"]
            if math.hypot(dx, dy) > 15:
                raise ValueError(f"{dx:+.1f} / {dy:+.1f} mm from {c['name']}: too far, is the arm above the right cell?")
            t["dx"], t["dy"] = round(dx, 2), round(dy, 2)
        else:
            raise ValueError(f"unknown teach value {what!r}")
        h["teach"] = t
        save_layout(layout)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def _json(self, code, data):
            body = json.dumps(data).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _foreign(self, post):
            if self.headers.get("Host") not in hosts:
                return "bad Host"
            origin = self.headers.get("Origin")
            if origin is not None and origin not in origins:
                return "cross-origin request"
            if post and self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
                return "Content-Type must be application/json"
            return None

        def do_GET(self):
            if (why := self._foreign(post=False)):
                return self._json(403, {"error": why})
            if self.path == "/":
                body = (HERE / "index.html").read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(body)
            elif self.path == "/api/layout":
                self._json(200, {"cells": table["cells"], "holders": layout["holders"], "types": layout["types"],
                                 "motion": layout["motion"], "cycle": layout["cycle"], "fields": cycle.fields(layout),
                                 "letters": LETTERS, "numbers": NUMBERS})
            elif self.path == "/api/state":
                try:
                    s = seq.robot.call("/status")
                    robot = {k: s.get(k) for k in ("mode_name", "enabled", "error", "alarm_ids", "pose",
                                                   "speed_ratio", "pump_mode")}
                except Exception as exc:
                    robot = {"mode_name": f"mg400-base unreachable ({type(exc).__name__})"}
                self._json(200, {"robot": robot, "seq": seq.state, "camera": seq.camera.state,
                                 "pressure": seq.pressure.state()})
            elif self.path == "/stream.mjpg":
                # multipart MJPEG: an <img> shows it as video; the camera stays open while it runs
                self.send_response(200)
                self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=frame")
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                last, missed = 0, 0
                try:
                    while missed < 6:  # ~1 min without frames: give the port back
                        jpeg, last = seq.camera.wait_frame(last, timeout=10)
                        if jpeg is None:
                            missed += 1
                            continue
                        missed = 0
                        self.wfile.write(b"--frame\r\nContent-Type: image/jpeg\r\nContent-Length: %d\r\n\r\n"
                                         % len(jpeg) + jpeg + b"\r\n")
                except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                    pass  # the page closed the stream
            elif self.path == "/api/photo":
                f = latest_frame()
                self._json(200, {"name": f.name, "time": time.strftime("%H:%M:%S", time.localtime(f.stat().st_mtime))}
                           if f else {"name": None})
            elif self.path.startswith("/frames/"):
                f = {p.name: p for p in FRAMES.glob("*.jpg")}.get(self.path[len("/frames/"):])
                if f is None:
                    return self._json(404, {"error": "no such frame"})
                body = f.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "image/jpeg")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            else:
                self._json(404, {"error": "not found"})

        def do_POST(self):
            if (why := self._foreign(post=True)):
                return self._json(403, {"ok": False, "error": why})
            length = int(self.headers.get("Content-Length") or 0)
            data = json.loads(self.rfile.read(length) or b"{}")
            try:
                if self.path == "/api/goto":
                    cell = table["by_name"].get(data.get("cell"))
                    if cell is None:
                        raise ValueError("unknown cell")
                    seq.goto(cell, float(data.get("hover_z", layout["motion"]["default_hover_z"])))
                elif self.path == "/api/stop":
                    seq.stop()
                elif self.path == "/api/holders":
                    holders = [{k: v for k, v in h.items() if k in HOLDER_KEYS} for h in data.get("holders", [])]
                    for h in holders:
                        h["name"] = str(h["name"]).strip()
                    check_holders(holders, layout["types"])
                    layout["holders"] = holders
                    save_layout(layout)
                    rebuild()
                elif self.path == "/api/view":
                    snapshot(seq.camera, "view")
                elif self.path == "/api/cycle/roles":
                    idle()
                    roles = {r: data.get(r) or None for r in cycle.ROLES}
                    names = {h["name"] for h in layout["holders"]}
                    for r, name in roles.items():
                        if name is not None and name not in names:
                            raise ValueError(f"{r}: no holder {name!r}")
                    ws_cell = data.get("workstation_cell") or None
                    ws = next((h for h in layout["holders"] if h["name"] == roles["workstation"]), None)
                    if ws_cell and (ws is None or ws_cell not in ws["cells"]):
                        raise ValueError(f"workstation cell {ws_cell} is not in {roles['workstation']}")
                    layout["cycle"]["roles"] = roles
                    layout["cycle"]["workstation_cell"] = ws_cell
                    layout["cycle"]["workstation_step"] = bool(data.get("workstation_step"))
                    save_layout(layout)
                elif self.path == "/api/cycle/above":
                    idle()
                    role, glass = data.get("role"), int(data.get("glass", 1))
                    x, y = cycle.slot_xy(layout, role, glass, table["by_name"])
                    seq.go_above(x, y, f"above {role} glass {glass}")
                elif self.path == "/api/cycle/teach":
                    teach_point(data.get("role"), data.get("what"))
                elif self.path == "/api/jog":
                    idle()
                    axis, delta = data.get("axis"), float(data.get("delta", 0))
                    if axis not in ("x", "y", "z") or not 0 < abs(delta) <= 5:
                        raise ValueError("jog: axis x/y/z, step up to 5 mm")
                    seq.ready_status()
                    reply = seq.robot.call("/jog", {"axis": axis, "delta": delta})
                    if not reply.get("ok"):
                        raise RuntimeError(f"jog refused: {reply}")
                elif self.path == "/api/pump":
                    if data.get("mode") not in ("off", "suck", "blow"):
                        raise ValueError("pump mode: off, suck or blow")
                    if data["mode"] != "off":
                        idle()
                    reply = seq.robot.call("/pump", {"mode": data["mode"]})
                    if not reply.get("ok"):
                        raise RuntimeError(f"pump refused: {reply}")
                elif self.path == "/api/cycle/run":
                    idle()
                    glasses = sorted({int(g) for g in data.get("glasses", [])})
                    if not glasses or not set(glasses) <= {1, 2, 3, 4}:
                        raise ValueError("glasses: some of 1-4")
                    rnd = int(data.get("round", 0))
                    if not 1 <= rnd <= 99:
                        raise ValueError("round must be 1-99")
                    seq.run_cycle(glasses, rnd, table["by_name"])
                elif self.path == "/api/probe":
                    idle()
                    seq.probe(data.get("axis"), float(data.get("step", 0)), float(data.get("distance", 0)),
                              bool(data.get("suction")), str(data.get("label", "")))
                elif self.path == "/api/refit":
                    idle()
                    rnd = int(data.get("round", 0))
                    rows = data.get("rows", [])
                    if not 1 <= rnd <= 99 or not rows or any(int(r.get("glass", 0)) not in (1, 2, 3, 4) for r in rows):
                        raise ValueError("refit: round 1-99 and rows for glasses 1-4")
                    cycle.save_refit(REFIT_CSV, rnd, rows)
                else:
                    return self._json(404, {"error": "not found"})
                self._json(200, {"ok": True})
            except Exception as exc:
                self._json(400, {"ok": False, "error": str(exc)})

    return Handler


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=8010)
    ap.add_argument("--check", action="store_true", help="print the 24.10 check cells and exit")
    args = ap.parse_args()
    layout = load_layout()
    check_holders(layout["holders"], layout["types"])
    cells = build_cells(layout)
    if args.check:
        # B+5 / F-4 were driven to 215.52 / -186.15 and 378.39 / 152.37 on 24.10 and judged centred.
        for name in ("G-1", "E+3", "D-2", "B+5", "F-4"):
            c = next(c for c in cells if c["name"] == name)
            print(f"{name}: {c['x']:.2f} / {c['y']:.2f}  r {c['radius']}")
        return
    seq = Sequencer(Mg400(layout["mg400_api"]), layout, ToolCamera(layout["camera_port"]),
                    PressureMonitor(layout.get("pressure_port")))
    server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(layout, seq, args.port))
    print(f"slot picker on http://127.0.0.1:{args.port}  (mg400-base: {layout['mg400_api']})")
    server.serve_forever()


if __name__ == "__main__":
    main()
