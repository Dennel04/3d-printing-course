"""slot_picker.py — click a Gridfinity cell, the suction cup goes above it;
the Edit layout mode adds, names, types, moves and deletes holders (saved to layout.json).

Serves a small page (http://127.0.0.1:8010) next to the mg400-base server
(http://127.0.0.1:8000), which must already be connected and enabled.
Each click runs three moves through mg400-base /api/move, waiting for the arm
to arrive after each: up to travel_z where it is, across at travel_z, then down
to the hover height. It never descends into a pocket: grid-surface Z is not
measured yet. Cell X/Y come from the 24.10.26 three-cell fit in ../calibration/cells.py.

Usage: python slot_picker.py [--port 8010] [--check]
"""
import argparse
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


FRAMES = HERE / "frames"  # tool camera JPEGs: the View button and Claude's captures; newest one is shown
sys.path.insert(0, str(HERE.parent / "calibration"))
sys.path.insert(0, str(HERE.parent / "tool-camera"))
import cells as calibration  # noqa: E402  single source of the grid fit (G-1, E+3, D-2)
from capture import capture  # noqa: E402

_, cell_robot = calibration.fit()


CELL_NAMES = [f"{letter}{n:+d}" for letter in LETTERS for n in NUMBERS]


def load_layout():
    return json.loads((HERE / "layout.json").read_text(encoding="utf-8"))


def save_layout(layout):
    (HERE / "layout.json").write_text(json.dumps(layout, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


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
    """Runs one goto at a time; Stop cancels it and holds the arm."""

    def __init__(self, robot, layout):
        self.robot, self.layout = robot, layout
        self.lock = threading.Lock()
        self.cancel = threading.Event()
        self.state = {"busy": False, "cell": None, "step": "idle", "error": None}

    def goto(self, cell, hover_z):
        motion, cal = self.layout["motion"], self.layout["calibration"]
        if cell["blocked"]:
            raise ValueError(f"{cell['name']} blocked: {cell['blocked']}")
        if not motion["min_hover_z"] <= hover_z <= motion["travel_z"]:
            raise ValueError(f"hover Z must be {motion['min_hover_z']} … {motion['travel_z']}")
        status = self.robot.call("/status")
        self._check(status)
        if status.get("speed_ratio", 100) > motion["max_speed_ratio"]:
            raise ValueError(f"speed {status['speed_ratio']}% > {motion['max_speed_ratio']}%: lower it in mg400-base first")
        with self.lock:
            if self.state["busy"]:
                raise ValueError("already moving")
            self.cancel.clear()
            self.state = {"busy": True, "cell": cell["name"], "step": "start", "error": None}
        x, y, r = cell["x"], cell["y"], cal["tool_r"]
        cx, cy = status["pose"][0], status["pose"][1]
        steps = [("up", cx, cy, motion["travel_z"]),
                 ("across", x, y, motion["travel_z"]),
                 ("down", x, y, hover_z)]
        threading.Thread(target=self._run, args=(steps, r), daemon=True).start()

    def stop(self):
        self.cancel.set()
        self.robot.call("/stop", {})

    def _run(self, steps, r):
        motion = self.layout["motion"]
        try:
            for label, x, y, z in steps:
                self.state["step"] = label
                reply = self.robot.call("/move", {"x": x, "y": y, "z": z, "r": r})
                if not reply.get("ok"):
                    raise RuntimeError(f"move refused: {reply}")
                c = reply.get("clamped", {})
                if any(abs(c.get(k, v) - v) > 0.5 for k, v in (("x", x), ("y", y), ("z", z))):
                    self.robot.call("/stop", {})
                    raise RuntimeError(f"mg400-base clamped the target to {c}; stopped")
                self._wait(x, y, z, motion)
            self.state["step"] = "arrived"
        except Exception as exc:
            self.state["error"] = str(exc)[:200]
            self.state["step"] = "stopped"
        finally:
            self.state["busy"] = False

    def _wait(self, x, y, z, motion):
        t0 = time.time()
        while True:
            if self.cancel.is_set():
                raise RuntimeError("stopped by user")
            s = self.robot.call("/status")
            self._check(s)
            p = s["pose"]
            if max(abs(p[0] - x), abs(p[1] - y), abs(p[2] - z)) < motion["arrive_tolerance_mm"]:
                return
            if time.time() - t0 > motion["step_timeout_s"]:
                self.robot.call("/stop", {})
                raise RuntimeError(f"not arriving, pose {p}")
            time.sleep(0.1)

    @staticmethod
    def _check(s):
        if s.get("error") or s.get("alarm_ids") or not s.get("enabled"):
            raise RuntimeError(f"robot not ready: {s.get('mode_name')} {s.get('alarm_ids')} {s.get('fault_label') or ''}")


def latest_frame():
    frames = sorted(FRAMES.glob("*.jpg"), key=lambda p: p.stat().st_mtime)
    return frames[-1] if frames else None


def make_handler(layout, seq):
    table = {}  # cells and by_name, rebuilt when the layout editor saves

    def rebuild():
        table["cells"] = build_cells(layout)
        table["by_name"] = {c["name"]: c for c in table["cells"]}

    rebuild()
    camera_lock = threading.Lock()  # one owner of the camera COM port at a time

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

        def do_GET(self):
            if self.path == "/":
                body = (HERE / "index.html").read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(body)
            elif self.path == "/api/layout":
                self._json(200, {"cells": table["cells"], "holders": layout["holders"], "types": layout["types"],
                                 "motion": layout["motion"], "letters": LETTERS, "numbers": NUMBERS})
            elif self.path == "/api/state":
                try:
                    s = seq.robot.call("/status")
                    robot = {k: s.get(k) for k in ("mode_name", "enabled", "error", "alarm_ids", "pose", "speed_ratio")}
                except Exception as exc:
                    robot = {"mode_name": f"mg400-base unreachable ({type(exc).__name__})"}
                self._json(200, {"robot": robot, "seq": seq.state})
            elif self.path == "/api/photo":
                f = latest_frame()
                self._json(200, {"name": f.name, "time": time.strftime("%H:%M:%S", time.localtime(f.stat().st_mtime))}
                           if f else {"name": None})
            elif self.path.startswith("/frames/"):
                f = FRAMES / Path(self.path).name
                if not f.is_file():
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
                    holders = [{k: v for k, v in h.items() if k in ("name", "type", "cells", "status", "no_go")}
                               for h in data.get("holders", [])]
                    for h in holders:
                        h["name"] = str(h["name"]).strip()
                    check_holders(holders, layout["types"])
                    layout["holders"] = holders
                    save_layout(layout)
                    rebuild()
                elif self.path == "/api/view":
                    FRAMES.mkdir(exist_ok=True)
                    out = FRAMES / time.strftime("view-%Y%m%d-%H%M%S.jpg")
                    with camera_lock:
                        try:
                            capture(layout["camera_port"], str(out))
                        except SystemExit as exc:  # capture() reports camera errors this way
                            raise RuntimeError(f"camera: {exc}") from None
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
    seq = Sequencer(Mg400(layout["mg400_api"]), layout)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(layout, seq))
    print(f"slot picker on http://127.0.0.1:{args.port}  (mg400-base: {layout['mg400_api']})")
    server.serve_forever()


if __name__ == "__main__":
    main()
