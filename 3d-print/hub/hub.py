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
import base64
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
# Hold-to-move in joint space: the goal rides this far ahead of the live joints and is renewed on every
# call (~10 per second), so the follower cruises instead of braking before each step. If the page dies the
# arm stops at most this far on (Cartesian holds have a timeout in mg400-base / the simulation instead).
JOINT_HOLD_LEAD = 6.0    # degrees

# twin checks behind the Tests tab: (title, script, args, what it answers)
TESTS = {
    "dry_run": ("Dry run: layout as the robot runs it", "dry_run.py", [],
                "Calculation, the arm does not move: every move of the current layout.json cycle against the arm, holders and glasses"),
    "dry_run_full": ("Dry run: planned full cycle", "dry_run.py", ["--full"],
                     "Calculation, the arm does not move: input → workstation → output with heights from the CAD"),
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


# every request that can move the arm; refused while motion is locked (one lock for the whole hub)
MOTION_PATHS = {"/api/goto", "/api/transfer", "/api/cycle/above", "/api/cycle/run", "/api/jog", "/api/probe",
                "/hub/jog"}   # /hub/jog_hold checks the lock itself: releasing a held key always passes


class Robots:
    """The robot the slot picker talks to: Simulation (in-process) or Real (mg400-base), and the motion lock."""

    def __init__(self, real, sim, mode_file=None):
        # the last selected robot survives a hub restart (mode_file); motion always starts off
        self.real, self.sim, self.mode_file = real, sim, mode_file
        saved = mode_file.read_text().strip() if mode_file and mode_file.is_file() else ""
        self._mode = saved if saved in ("sim", "real") else "sim"
        self.armed = False

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = mode
        if self.mode_file:
            self.mode_file.write_text(mode)
        if mode == "real":
            self.ensure_connected()

    def ensure_connected(self):
        """Real robot: open mg400-base's link to the arm if it is down (no motion; Enable stays a click)."""
        try:
            if not self.real.call("/status").get("connected"):
                self.real.call("/connect", {})
        except Exception:
            pass          # server down or robot off: the top bar shows it and offers Connect

    def arm(self, on):
        self.armed = bool(on)

    def motion_allowed(self):
        return self.armed

    def arm_state(self):
        return {"armed": self.armed}

    @property
    def current(self):
        return self.sim if self.mode == "sim" else self.real

    def call(self, path, body=None):
        return self.current.call(path, body)


class Tests:
    def __init__(self, lab, on_export=None):
        self.lab = lab
        self.on_export = on_export
        self.lock = threading.Lock()
        self.state = {k: {"title": v[0], "about": v[3], "status": "idle", "summary": "", "output": "",
                          "seconds": None, "finished": None} for k, v in TESTS.items()}

    def start(self, name):
        if name not in TESTS:
            raise ValueError(f"unknown test {name!r}")
        with self.lock:
            if self.state[name]["status"] == "running":
                raise ValueError(f"{name} is already running")
            self.state[name].update(status="running", summary="starting…", output="", started=time.time())
        threading.Thread(target=self._run, args=(name,), daemon=True).start()

    def _run(self, name):
        _, script, args, _ = TESTS[name]
        t0 = time.time()
        if script is None:
            cmd, cwd = [sys.executable, "-m", "unittest", "-v", "test_hub"], HERE / "tests"
        else:
            cmd, cwd = [sys.executable, script, *args, "--lab", str(self.lab)], SIM
        cmd.insert(1, "-u")          # unbuffered: the page shows each line as it comes
        lines = []
        try:
            p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                 encoding="utf-8", errors="replace")
            for line in p.stdout:
                lines.append(line.rstrip("\n"))
                with self.lock:
                    self.state[name].update(output="\n".join(lines[-400:]),
                                            summary=f"running {time.time() - t0:.0f} s · {lines[-1][:110]}")
                if time.time() - t0 > 1800:
                    p.kill()
                    lines.append("timed out after 30 min")
            code = p.wait()
            out = "\n".join(lines)
        except OSError as exc:
            out, code = f"could not start: {exc}", -1
        status, summary = verdict(name, out, code)
        with self.lock:
            self.state[name].update(status=status, summary=summary, output=out[-20000:],
                                    seconds=round(time.time() - t0, 1), finished=time.strftime("%H:%M:%S"))
        if name == "export" and self.on_export:
            self.on_export()


class LivePose:
    """Poses of every moving part of the twin for the 3D view (same frames as export_viewer.py)."""

    GRAB_XY = 12.0     # mm: cup centre within this of a glass centre
    GRAB_Z = (-3.0, 6.0)  # mm: glass top this far below / above the cup tip when the pump starts sucking

    def __init__(self):
        self.twin = None
        self.error = None
        self.glasses = {}         # name -> [x, y, z] glass centre, world frame
        self.home = {}            # where reset_glasses put them
        self.carried = None
        self.lock = threading.Lock()
        threading.Thread(target=self._load, daemon=True).start()

    def reset_glasses(self):
        """Glasses back where the cycle starts (anim.json frame 0, i.e. the current layout's input pockets)."""
        with self.lock:
            self.carried = None
            try:
                f0 = json.loads((VIEWER_DATA / "anim.json").read_text(encoding="utf-8"))["frames"][0]["s"]
                self.glasses = {n: list(v[:3]) for n, v in f0.items() if n.startswith("glass ")}
            except (OSError, ValueError, KeyError, IndexError):
                self.glasses = {}
            self.home = {n: list(v) for n, v in self.glasses.items()}

    @property
    def glasses_moved(self):
        """Some 3D glass is away from its input pocket (the stage then offers to put them back)."""
        with self.lock:
            return any(math.dist(v, self.home.get(n, v)) > 1.0 for n, v in self.glasses.items())

    def _load(self):
        try:
            import numpy as np
            import twin
            import export_viewer as ev
            self._np, self._ev, self._twin_mod = np, ev, twin
            self.twin = twin.Twin(with_post=False, layout={"holders": []})
            self.reset_glasses()
        except Exception as exc:  # the hub still runs without the 3D view
            self.error = f"{type(exc).__name__}: {exc}"

    def _glasses(self, x, y, z, pump):
        """Pick a glass up when the pump starts sucking on it, carry it, leave it where blow/off happens.
        The picture of the cycle only: the robot itself cannot see a glass."""
        ox, oy = self._twin_mod.cup_offset(self._twin_mod.TOOL_R)
        cx, cy, tip = x + ox, y + oy, self.twin.cup_tip_z(z)
        with self.lock:
            if pump == "suck" and self.carried is None:
                best = None
                for n, (gx, gy, gz) in self.glasses.items():
                    d = math.hypot(gx - cx, gy - cy)
                    if d <= self.GRAB_XY and self.GRAB_Z[0] <= gz + 1 - tip <= self.GRAB_Z[1] and (best is None or d < best[0]):
                        best = (d, n)
                if best:
                    self.carried = best[1]
            elif pump != "suck":
                self.carried = None
            if self.carried:
                self.glasses[self.carried] = [cx, cy, tip - 1.0]
            return {n: [round(v[0], 2), round(v[1], 2), round(v[2], 2), 0.0, 0.0, 0.0, 1.0] for n, v in self.glasses.items()}

    def poses(self, x, y, z, r, pump="off"):
        if self.twin is None:
            return None
        np, ev, tw = self._np, self._ev, self._twin_mod
        parts = self.twin.pose_meshes(x, y, z, r)
        if parts is None:
            return None
        shift = np.eye(4)
        shift[:2, 3] = tw.cup_offset(tw.TOOL_R)
        out = {n: ev.qpos(shift @ tf if ev.on_arm(n) else tf)
               for n, (_, tf) in parts.items()}
        for n in ("cup metal", "cup fitting", "cup flange", "cup collet", "cup oring", "cup rubber"):
            out[n] = out["cup"]
        out.update(self._glasses(x, y, z, pump))
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


def joint_hold_target(status, axis, sign):
    """Goal for a held joint jog: JOINT_HOLD_LEAD ahead of the live joints, shortened near a joint limit."""
    lead = JOINT_HOLD_LEAD
    while True:
        try:
            return joint_target(status, axis, sign * lead)
        except ValueError:
            lead /= 2
            if lead < 0.2:
                raise


def follow_workstation_cell(layout, before, save, letters, numbers):
    """After a layout save: if the workstation holder moved, its chosen cell moves with it (same offset);
    if that is impossible the cell falls back to the holder's first cell. The picker itself does not do this,
    and a cell left behind sends the real cycle to an empty spot."""
    cyc = layout["cycle"]
    name, cell = cyc["roles"].get("workstation"), cyc.get("workstation_cell")
    h = next((h for h in layout["holders"] if h["name"] == name), None)
    if not cell or h is None or cell in h["cells"]:
        return None
    new = None
    old = before.get(name)
    if old and len(old) == len(h["cells"]) and cell in old:
        L, N = list(letters), list(numbers)
        pos = lambda c: (L.index(c[0]), N.index(int(c[1:])))
        shifts = {(pos(b)[0] - pos(a)[0], pos(b)[1] - pos(a)[1]) for a, b in zip(sorted(old, key=pos), sorted(h["cells"], key=pos))}
        if len(shifts) == 1:
            (dl, dn), (l0, n0) = shifts.pop(), pos(cell)
            moved = f"{L[l0 + dl]}{N[n0 + dn]:+d}"
            new = moved if moved in h["cells"] else None
    cyc["workstation_cell"] = new
    save(layout)
    return new


def scene_stale(lab):
    """The 3D scene is missing or older than the picker's layout.json."""
    scene, layout = VIEWER_DATA / "scene.glb", lab / "slot-picker" / "layout.json"
    return not scene.exists() or (layout.exists() and layout.stat().st_mtime > scene.stat().st_mtime)


WEBCAM_MAX_BYTES = 20_000_000   # a 4K JPEG is ~1-3 MB


def build(lab, port, mode_file=None):
    sys.path.insert(0, str(lab / "slot-picker"))
    import slot_picker as sp

    layout = sp.load_layout()
    sp.check_holders(layout["holders"], layout["types"])
    robots = Robots(sp.Mg400(layout["mg400_api"]), SimRobot(speed_ratio=min(10, layout["motion"]["max_speed_ratio"])), mode_file)
    if robots.mode == "real":
        threading.Thread(target=robots.ensure_connected, daemon=True).start()
    seq = sp.Sequencer(robots, layout, sp.ToolCamera(layout["camera_port"]), sp.PressureMonitor(layout.get("pressure_port")))
    live = LivePose()
    tests = Tests(lab, on_export=lambda: live.reset_glasses() if live.twin else None)
    Picker = sp.make_handler(layout, seq, port)
    if scene_stale(lab):          # also after a hub restart that cut a rebuild short
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
                return self._file(STATIC / "picker.html", types[".html"])   # hub version of slot-picker/index.html
            if path.startswith("/static/") or path.startswith("/viewer/"):
                root, rel = (STATIC, path[8:]) if path.startswith("/static/") else (VIEWER_DATA, path[8:])
                f = (root / rel).resolve()
                if root.resolve() not in f.parents or not f.is_file():
                    return self._json(404, {"error": "not found"})
                return self._file(f, types.get(f.suffix, "application/octet-stream"))
            if path == "/hub/state":
                s = robot_status()
                pose = s.get("pose")
                three = live.poses(*pose, pump=s.get("pump_mode") or "off") if pose and s.get("reachable") else None
                return self._json(200, {"mode": robots.mode, "robot": s, "seq": seq.state, "motion": robots.arm_state(),
                                        "limits": {"max_speed_ratio": layout["motion"]["max_speed_ratio"],
                                                   "tool_r": layout["calibration"]["tool_r"]},
                                        "pose3d": three, "pose3d_error": live.error, "glasses_moved": live.glasses_moved,
                                        "camera": seq.camera.state})
            if path == "/hub/tests":
                return self._json(200, {"tests": tests.state})
            return super().do_GET()

        def do_POST(self):
            path = self.path.split("?")[0]
            if path == "/api/holders" and not self._foreign(post=True):
                before = {h["name"]: list(h["cells"]) for h in layout["holders"]}
                super().do_POST()
                follow_workstation_cell(layout, before, sp.save_layout, sp.LETTERS, sp.NUMBERS)
                return
            if path in MOTION_PATHS and not self._foreign(post=True) and not robots.motion_allowed():
                return self._json(409, {"ok": False, "error": "Motion is off: turn on the Motion switch in the Jog tab first."})
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
                robots.arm(False)          # a new robot starts locked
                return {"mode": mode}
            if path == "/hub/arm":
                robots.arm(bool(data.get("armed")))
                return robots.arm_state()
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
            if path == "/hub/jog_hold":
                space, axis, sign = data.get("space", "cart"), data.get("axis"), int(data.get("dir", 0))
                if sign not in (-1, 0, 1):
                    raise ValueError("dir: -1, 0 or 1")
                if not sign:                              # released: brake smoothly (not a running sequence)
                    return {} if seq.state["busy"] else robots.call("/stop", {})
                if not robots.motion_allowed():
                    raise ValueError("Motion is off: turn on the Motion switch in the Jog tab first.")
                if seq.state["busy"]:
                    raise ValueError("the robot is running a sequence; press STOP first")
                status = seq.ready_status()
                if space == "joint" and axis == "j4":     # J4 alone turns only R (R = J1 + J4)
                    space, axis = "cart", "r"
                if space == "cart":
                    if axis not in CART_AXES:
                        raise ValueError("axis: x, y, z or r")
                    reply = robots.call("/jog_hold", {"axis": axis, "dir": sign})
                elif space == "joint":
                    if axis not in JOINT_AXES:
                        raise ValueError("axis: j1, j2, j3 or j4")
                    reply = robots.call("/move", joint_hold_target(status, axis, sign))
                else:
                    raise ValueError("space: cart or joint")
                if not reply.get("ok"):
                    raise ValueError(reply.get("error") or f"refused: {reply}")
                return {}
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
            if path == "/hub/layout3d":
                # the picker's layout.json -> 3D scene (holders, glasses, cycle replay); glasses go home when done
                if tests.state["export"]["status"] != "running":
                    tests.start("export")
                return {}
            if path == "/hub/webcam/frame":
                # the page grabs the picture from the table webcam itself and posts one JPEG (base64) here
                jpeg = base64.b64decode(data.get("jpeg") or "", validate=True)
                if not jpeg.startswith(b"\xff\xd8") or len(jpeg) > WEBCAM_MAX_BYTES:
                    raise ValueError("expected one JPEG picture")
                folder = lab / "webcam-frames"
                folder.mkdir(exist_ok=True)
                name = time.strftime("webcam-%Y%m%d-%H%M%S.jpg")
                (folder / name).write_bytes(jpeg)
                return {"name": name}
            if path == "/hub/glasses/reset":
                live.reset_glasses()
                return {}
            raise KeyError(f"no route {path}")

    return Hub, robots


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--port", type=int, default=8020)
    ap.add_argument("--lab", default=str(HERE.parent / "lab2"))
    a = ap.parse_args()
    lab = Path(a.lab).resolve()
    handler, robots = build(lab, a.port, mode_file=HERE / ".mode")
    server = ThreadingHTTPServer(("127.0.0.1", a.port), handler)
    print(f"MG400 Station Hub on http://127.0.0.1:{a.port}  (lab {lab.name}, robot: {robots.mode}, motion off)")
    server.serve_forever()


if __name__ == "__main__":
    main()
