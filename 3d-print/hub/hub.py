"""hub.py — MG400 Station Hub: one page for the robot, the slot picker, the digital twin and its checks.

    cd 3d-print/hub
    ../sim/.venv/Scripts/python hub.py            # http://127.0.0.1:8020, starts in Simulation
    ../sim/.venv/Scripts/python hub.py --lab ../lab2 --port 8020

Simulation: an in-process MG400 (sim_robot.py) that answers like mg400-base. Real: the mg400-base
server from layout.json (`mg400_api`, normally http://127.0.0.1:8000/api), already connected and
enabled. Switching is allowed only while nothing moves. Everything the slot picker does (drive to a
cell, layout editor, teach points, glass cycle, refit CSV, tool camera) runs unchanged on top of the
selected robot; the hub adds the DobotStudio-style jog (Cartesian and joint), the live 3D view and
the twin checks (sim/*.py) behind buttons.
"""
import argparse
import json
import math
import subprocess
import sys
import threading
import time
from http.server import ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIM = HERE.parent / "sim"
STATIC = HERE / "static"
VIEWER_DATA = SIM / "viewer" / "data"

sys.path.insert(0, str(SIM))
import mg400_kin as kin  # noqa: E402
from sim_robot import SimRobot  # noqa: E402

CART_AXES = ("x", "y", "z", "r")
JOINT_AXES = ("j1", "j2", "j3", "j4")
MAX_STEP = {"cart": 10.0, "joint": 10.0}

# twin checks behind the Tests tab: (title, script, args, what it answers)
TESTS = {
    "dry_run": ("Dry run: layout as the robot runs it", "dry_run.py", [],
                "Every move of the current layout.json cycle against the arm, holders and glasses"),
    "dry_run_full": ("Dry run: planned full cycle", "dry_run.py", ["--full"],
                     "Input → workstation → output with derived heights"),
    "refit": ("Refit rounds 2-5", "refit_sim.py", [],
              "Holders put back anywhere inside their foot play (±1 mm), 4 glasses per round"),
    "tolerance": ("Calibration error tolerance", "tolerance.py", [],
                  "How far all holders may be off before a glass fails, 8 directions"),
    "audit": ("Scene audit", "audit_scene.py", [],
              "Holders dropped onto the rig, glass gaps, taught Z vs first touch"),
    "export": ("Rebuild 3D scene", "export_viewer.py", [],
               "Scene and cycle animation for the 3D view from the current layout"),
    "hub": ("Hub self-test", None, [], "Simulation robot, joint jog and the hub API"),
}


def verdict(name, out, code):
    """pass / warn / fail and a one-line summary from a check's output."""
    if code != 0:
        last = [l for l in out.strip().splitlines() if l.strip()][-1:] or ["no output"]
        return "fail", f"exit {code}: {last[0][:160]}"
    lines = out.splitlines()
    hits = [l for l in lines if "COLLISION" in l and "COLLISION-free" not in l]
    if name in ("dry_run", "dry_run_full"):
        warn = [l for l in lines if "not fully on the glass" in l or "WRONG PLACE" in l]
        if hits:
            return "fail", f"{len(hits)} colliding moves"
        if warn:
            return "warn", f"no collisions; {len(warn)} warnings (cup off the glass centre / landing)"
        return "pass", f"no collisions in {sum(1 for l in lines if ' ok ' in l or ' close ' in l)} moves"
    if name == "refit":
        tot = [l for l in lines if l.startswith("total")]
        if tot:
            a, b = (int(v) for v in tot[-1].split()[1].split("/"))
            return ("pass" if a == b else "fail"), f"{a}/{b} glasses through rounds 2-5"
    if name == "tolerance":
        fails = [l for l in lines if l.startswith("direction")]
        mins = [int(l.split("fails at ")[1].split()[0]) for l in fails if "fails at" in l]
        if mins:
            m = min(mins)
            return ("warn" if m <= 2 else "pass"), f"weakest direction fails at {m} mm calibration error"
    if name == "audit":
        bad = [l for l in lines if "CHECK" in l or "FLOATING" in l or "SUNK" in l]
        return ("warn" if bad else "pass"), (f"{len(bad)} objects to check" if bad else "all holders and glasses seated")
    if name == "hub":
        ran = next((l.strip() for l in lines if l.startswith("Ran ")), "")
        ok = any(l.strip().startswith("OK") for l in lines)
        bad = next((l.strip() for l in lines if l.startswith("FAILED")), "")
        return ("pass" if ok and not bad else "fail"), f"{ran}: {'OK' if ok and not bad else bad or 'see output'}"
    return "pass", (lines[-1].strip()[:160] if lines else "done")


class Robots:
    """The robot the slot picker talks to: Simulation (in-process) or Real (mg400-base)."""

    def __init__(self, real, sim):
        self.real, self.sim, self.mode = real, sim, "sim"

    @property
    def current(self):
        return self.sim if self.mode == "sim" else self.real

    def call(self, path, body=None):
        return self.current.call(path, body)


class Tests:
    def __init__(self, lab):
        self.lab = lab
        self.lock = threading.Lock()
        self.state = {k: {"title": v[0], "about": v[3], "status": "idle", "summary": "", "output": "",
                          "seconds": None, "finished": None} for k, v in TESTS.items()}

    def start(self, name):
        if name not in TESTS:
            raise ValueError(f"unknown test {name!r}")
        with self.lock:
            if self.state[name]["status"] == "running":
                raise ValueError(f"{name} is already running")
            self.state[name].update(status="running", summary="running…", output="")
        threading.Thread(target=self._run, args=(name,), daemon=True).start()

    def _run(self, name):
        _, script, args, _ = TESTS[name]
        t0 = time.time()
        if script is None:
            cmd, cwd = [sys.executable, "-m", "unittest", "-v", "test_hub"], HERE / "tests"
        else:
            cmd, cwd = [sys.executable, script, *args, "--lab", str(self.lab)], SIM
        try:
            p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=1800,
                               encoding="utf-8", errors="replace")
            out, code = p.stdout + ("\n" + p.stderr if p.stderr.strip() else ""), p.returncode
            if name == "hub":   # unittest reports on stderr
                out = p.stderr + p.stdout
        except subprocess.TimeoutExpired:
            out, code = "timed out after 30 min", -1
        status, summary = verdict(name, out, code)
        with self.lock:
            self.state[name].update(status=status, summary=summary, output=out[-20000:],
                                    seconds=round(time.time() - t0, 1), finished=time.strftime("%H:%M:%S"))


class LivePose:
    """Poses of every moving part of the twin for the 3D view (same frames as export_viewer.py)."""

    def __init__(self):
        self.twin = None
        self.error = None
        threading.Thread(target=self._load, daemon=True).start()

    def _load(self):
        try:
            import numpy as np
            import twin
            import export_viewer as ev
            self._np, self._ev, self._twin_mod = np, ev, twin
            self.twin = twin.Twin(with_post=False, layout={"holders": []})
        except Exception as exc:  # the hub still runs without the 3D view
            self.error = f"{type(exc).__name__}: {exc}"

    def poses(self, x, y, z, r, press=0.0):
        if self.twin is None:
            return None
        np, ev, tw = self._np, self._ev, self._twin_mod
        parts = self.twin.pose_meshes(x, y, z, r)
        if parts is None:
            return None
        shift = np.eye(4)
        shift[:2, 3] = tw.cup_offset(tw.TOOL_R)
        out = {n: ev.qpos(shift @ tf if (n.startswith("arm ") or n == "xiao mount") else tf)
               for n, (_, tf) in parts.items()}
        for n in ("cup metal", "cup fitting", "cup flange", "cup collet", "cup oring", "cup rubber"):
            out[n] = out["cup"]
        return out


def joint_target(status, axis, delta):
    """Cartesian goal for a joint jog: current joints + delta through the fitted forward model.
    MG400 R = J1 + J4, so turning J1 alone keeps the tool's angle to the arm (R moves with it)."""
    x, y, z, r = status["pose"]
    j = kin.inverse(x, y, z)
    if j is None:
        raise ValueError("current pose is outside the model")
    j1, j2, j3 = j
    j4 = r - j1
    i = JOINT_AXES.index(axis)
    vals = [j1, j2, j3, j4]
    vals[i] += delta
    nx, ny, nz = kin.forward(*vals[:3])
    ok, reason, _ = kin.check(nx, ny, nz)
    if not ok:
        raise ValueError(f"{axis.upper()} {delta:+g}°: {reason}")
    return {"x": round(nx, 3), "y": round(ny, 3), "z": round(nz, 3), "r": round(vals[0] + vals[3], 3)}


def build(lab, port):
    sys.path.insert(0, str(lab / "slot-picker"))
    import slot_picker as sp

    layout = sp.load_layout()
    sp.check_holders(layout["holders"], layout["types"])
    robots = Robots(sp.Mg400(layout["mg400_api"]), SimRobot(speed_ratio=min(10, layout["motion"]["max_speed_ratio"])))
    seq = sp.Sequencer(robots, layout, sp.ToolCamera(layout["camera_port"]), sp.PressureMonitor(layout.get("pressure_port")))
    tests = Tests(lab)
    live = LivePose()
    Picker = sp.make_handler(layout, seq, port)
    if not (VIEWER_DATA / "scene.glb").exists():
        tests.start("export")

    def robot_status():
        try:
            s = robots.call("/status")
            s["reachable"] = True
        except Exception as exc:
            s = {"reachable": False, "mode_name": f"mg400-base unreachable ({type(exc).__name__})"}
        return s

    class Hub(Picker):
        def _file(self, path, ctype):
            body = path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if (why := self._foreign(post=False)):
                return self._json(403, {"error": why})
            path = self.path.split("?")[0]
            types = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
                     ".css": "text/css; charset=utf-8", ".glb": "model/gltf-binary", ".json": "application/json"}
            if path == "/":
                return self._file(STATIC / "index.html", types[".html"])
            if path == "/picker":
                return self._file(lab / "slot-picker" / "index.html", types[".html"])
            if path.startswith("/static/") or path.startswith("/viewer/"):
                root, rel = (STATIC, path[8:]) if path.startswith("/static/") else (VIEWER_DATA, path[8:])
                f = (root / rel).resolve()
                if root.resolve() not in f.parents or not f.is_file():
                    return self._json(404, {"error": "not found"})
                return self._file(f, types.get(f.suffix, "application/octet-stream"))
            if path == "/hub/state":
                s = robot_status()
                pose = s.get("pose")
                three = live.poses(*pose) if pose and s.get("reachable") else None
                return self._json(200, {"mode": robots.mode, "robot": s, "seq": seq.state,
                                        "limits": {"max_speed_ratio": layout["motion"]["max_speed_ratio"],
                                                   "tool_r": layout["calibration"]["tool_r"]},
                                        "pose3d": three, "pose3d_error": live.error,
                                        "camera": seq.camera.state})
            if path == "/hub/tests":
                return self._json(200, {"tests": tests.state})
            return super().do_GET()

        def do_POST(self):
            if not self.path.startswith("/hub/"):
                return super().do_POST()
            if (why := self._foreign(post=True)):
                return self._json(403, {"error": why})
            try:
                data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
                reply = self._hub(self.path.split("?")[0], data)
                self._json(200, {"ok": True, **(reply or {})})
            except (ValueError, KeyError, TypeError) as exc:
                self._json(400, {"ok": False, "error": str(exc)})
            except Exception as exc:
                self._json(500, {"ok": False, "error": f"{type(exc).__name__}: {exc}"})

        def _hub(self, path, data):
            if path == "/hub/mode":
                mode = data.get("mode")
                if mode not in ("sim", "real"):
                    raise ValueError("mode: sim or real")
                if seq.state["busy"]:
                    raise ValueError("the robot is moving; stop it before switching")
                robots.mode = mode
                return {"mode": mode}
            if path == "/hub/jog":
                space, axis = data.get("space", "cart"), data.get("axis")
                delta = float(data.get("delta", 0))
                if seq.state["busy"]:
                    raise ValueError("the robot is running a sequence; press STOP first")
                if not 0 < abs(delta) <= MAX_STEP.get(space, 0):
                    raise ValueError(f"step must be 0 < |step| <= {MAX_STEP.get(space)}")
                s = seq.ready_status()
                if space == "cart":
                    if axis not in CART_AXES:
                        raise ValueError("axis: x, y, z or r")
                    reply = robots.call("/jog", {"axis": axis, "delta": delta})
                elif space == "joint":
                    if axis not in JOINT_AXES:
                        raise ValueError("axis: j1, j2, j3 or j4")
                    reply = robots.call("/move", joint_target(s, axis, delta))
                else:
                    raise ValueError("space: cart or joint")
                if not reply.get("ok"):
                    raise ValueError(reply.get("error") or f"refused: {reply}")
                return {"target": reply.get("clamped")}
            if path in ("/hub/enable", "/hub/disable", "/hub/clear_error", "/hub/stop"):
                if path == "/hub/stop":
                    seq.stop()
                    return {}
                return robots.call(path[4:], {})
            if path == "/hub/connect":
                return robots.call("/connect", {"ip": data.get("ip")} if data.get("ip") else {})
            if path == "/hub/tests/run":
                tests.start(data.get("name"))
                return {}
            raise KeyError(f"no route {path}")

    return Hub, robots


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--port", type=int, default=8020)
    ap.add_argument("--lab", default=str(HERE.parent / "lab2"))
    a = ap.parse_args()
    lab = Path(a.lab).resolve()
    handler, _ = build(lab, a.port)
    server = ThreadingHTTPServer(("127.0.0.1", a.port), handler)
    print(f"MG400 Station Hub on http://127.0.0.1:{a.port}  (lab {lab.name}, starts in Simulation)")
    server.serve_forever()


if __name__ == "__main__":
    main()
