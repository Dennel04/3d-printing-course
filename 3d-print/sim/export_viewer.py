"""export_viewer.py — the glass cycle of the twin for the 3D viewer (viewer/index.html).

Same layout.json, cycle.py, cells.py and arm model as dry_run.py. Writes
  viewer/data/scene.glb   every object as a named node: static ones in world coordinates (z up, mm),
                          moving ones (arm links, XIAO mount + camera, cup, glasses) in their own frame
  viewer/data/anim.json   frames every 2 mm of the path: pose of every moving node, the action label,
                          plus dry_run's verdict per move (ok / close / COLLISION)
Extra objects (anything exported from Fusion as STL) go in viewer/extras.json, see viewer/README.md.
Run: .venv/Scripts/python export_viewer.py [--full] [--glasses 1,2,3,4]   then  python -m http.server -d viewer 8020
"""
import argparse
import json
import math
import re

import numpy as np
import trimesh

import dry_run
import mg400_kin as kin
import twin

HERE = twin.HERE
OUT = HERE / "viewer" / "data"
STEP = 2.0

# print colours of the real parts where known, otherwise neutral
COLORS = {"Glass input": "#f2f2ee", "AtomS3 input": "#f2f2ee", "Workstation (orange)": "#f26b1d",
          "Good output": "#d9d9d4", "Calibration": "#222222"}


def color_for(name):
    if name.startswith("holder:"):
        return COLORS.get(name[7:], "#cfcfca")
    if "pipe" in name:
        return "#8f98a3"
    if name.startswith("rakis"):
        return "#9aa3ad"
    if name == "table":
        return "#3a3f47"
    if name.startswith("webcam post"):
        return "#e8e8e3"
    if name == "battery":
        return "#3b6fb6"
    if name == "AtomS3 screen":
        return "#10161c"
    if name == "AtomS3":
        return "#cfd2d4"
    if name.startswith("arm "):
        return "#e9ecef" if "link5" not in name else "#c9ced4"
    if name == "xiao mount":
        return "#f26b1d"
    if name == "xiao camera":
        return "#2e3a46"
    if name in ("cup rubber", "cup oring"):
        return "#161616"
    if name == "cup collet":
        return "#eeeeea"
    if name in ("cup metal", "cup fitting", "cup flange"):
        return "#c3c8ce"
    if name.startswith("glass"):
        return "#9fd3ff"
    return "#b0b0b0"


# Suction tool as on the robot (close-up photo 25.10), top to bottom:
#  * Dobot MG400 end flange, official CAD robot/meshes/mg400_end_flange.stl (MG400_End_Flange_3D.stp, Dobot via
#    Pololu; User Guide V1.7 fig. 5.3: boss D22 x 10 on the J4 shaft D8 x 12, disc D40 x 4)
#  * holder plate D40 x 4 under it, 4 socket head screws from below on PCD 30
#  * aluminium body D16 with a side 4 mm push-in fitting near its lower end, step, O-ring, shiny pad adapter
#  * black pad stamped "C20" = SMC ZP20C style, flat with ribs, D20 (catalog ZPT 13-11-6: outer D23, height
#    C 14; caliper 24.10: D22.25 x 13.8). No buffer spring: the press is the rubber lip only.
# Lengths of the plate/body/adapter from the photos (no public CAD of the holder); the body is stretched so
# the pad tip is at the twin's cup length (66.2 from the shaft end, from a touch). TODO caliper the free
# length. Picture only: collisions use the twin cylinder.
SHAFT = 12.0
FLANGE = 14.0
HOLDER_LEN = 63.0
HOLDER_PROFILE = {   # (radius, depth below the flange disc, mm); "body" parts stretch, the pad does not
    "cup metal": [(0, 0), (20, 0), (20, 4), (8, 4), (8, 42), (6, 42), (6, 44), (6.6, 44), (6.6, 49), (0, 49)],
    "cup rubber": [(0, 49), (5.6, 49), (5.6, 52), (5, 53), (6, 55.5), (6.6, 56.5), (11.12, 61.6), (11.12, 63),
                   (0, 63)],
}
STRETCH_FROM = 4.0     # depths between the plate and the pad adapter (the body) take the length difference
STRETCH_TO = 42.0


def suction_tool(length):
    """Meshes of the tool in the twin's cup frame (z up, top = J4 shaft end at +length/2, tip at -length/2)."""
    top = length / 2
    extra = (length - (FLANGE - SHAFT)) - HOLDER_LEN       # stretch of the body to reach the twin's tip

    def depth(d):
        return d + extra * min(1.0, max(0.0, (d - STRETCH_FROM) / (STRETCH_TO - STRETCH_FROM)))
    out = {}
    fl = trimesh.load(HERE / "robot" / "meshes" / "mg400_end_flange.stl")   # mm, axis y, disc y 0..-4, boss to -14
    fl.apply_transform(trimesh.transformations.rotation_matrix(-math.pi / 2, (1, 0, 0)))   # y -> -z
    fl.apply_translation((0, 0, top + SHAFT - fl.bounds[1][2]))   # boss top at the motor face
    zt = fl.bounds[0][2]                                          # underside of the flange disc
    out["cup flange"] = fl
    for name, prof in HOLDER_PROFILE.items():
        pts = [(r, zt - depth(d)) for r, d in prof]
        out[name] = trimesh.creation.revolve(np.array(pts[::-1]), sections=64)
    parts = []
    for i in range(4):               # socket head screws under the holder plate, PCD 30
        a = math.pi / 4 + i * math.pi / 2
        h = trimesh.creation.cylinder(radius=2.75, height=3, sections=20)
        h.apply_translation((15 * math.cos(a), 15 * math.sin(a), zt - 4 - 1.5))
        parts.append(h)
    zf = zt - depth(36)              # side push-in fitting: hex 9 + white collet D8 (4 mm hose), towards +x
    hexn = trimesh.creation.cylinder(radius=5.2, height=6, sections=6)
    hexn.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, (0, 1, 0)))
    hexn.apply_translation((7.5 + 3, 0, zf))
    out["cup fitting"] = trimesh.util.concatenate(parts + [hexn])
    collet = trimesh.creation.cylinder(radius=4.2, height=6, sections=32)
    collet.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, (0, 1, 0)))
    collet.apply_translation((7.5 + 6 + 3, 0, zf))
    out["cup collet"] = collet
    oring = trimesh.creation.annulus(r_min=5.6, r_max=6.9, height=1.4, sections=48)
    oring.apply_translation((0, 0, zt - depth(43)))
    out["cup oring"] = oring
    return out


def qpos(m):
    q = trimesh.transformations.quaternion_from_matrix(m)      # w x y z
    return [round(float(v), 2) for v in m[:3, 3]] + [round(float(v), 5) for v in (q[1], q[2], q[3], q[0])]


def verdicts(full, glasses):
    rep = dry_run.Run(glasses, full=full).run()
    out = []
    for line in rep:
        m = re.match(r"glass \d+: (glass \d+: .+?)\s{2,}(ok|close|COLLISION)\b", line)
        if m:
            out.append((m.group(1).strip(), m.group(2), line.strip()))
    return out, rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true", help="the planned full cycle instead of layout.json as is")
    ap.add_argument("--glasses", default="1,2,3,4")
    twin.add_lab_arg(ap)
    a = ap.parse_args()
    twin.use_lab(a.lab)
    dry_run.load_cycle()
    glasses = [int(v) for v in a.glasses.split(",")]
    cycle = dry_run.cycle

    moves_verdict, report = verdicts(a.full, glasses)
    run = dry_run.Run(glasses, full=a.full)
    T, lay = run.T, run.lay

    scene = trimesh.Scene()
    static = []

    def add(name, mesh, kind):
        m = trimesh.Trimesh(mesh.vertices, mesh.faces, process=False)     # colours are set in the page
        scene.add_geometry(m, node_name=name, geom_name=name)
        static.append({"name": name, "kind": kind})

    glass_names = [n for n in T.scene if n.startswith("glass ")]
    for n, mesh in T.scene.items():
        if n in glass_names:
            continue
        if n == "AtomS3":           # one mesh for collisions, two colours in the picture
            add(n, dry_run.ATOM_SHELL.copy().apply_translation(run.atom_at), "static")
            add("AtomS3 screen", dry_run.ATOM_SCREEN.copy().apply_translation(run.atom_at), "static")
            continue
        add(n, mesh, "static")
    base = T.arm.link_poses(0, 0, 0, 0)["base_link"]
    # The twin keeps the cells.py fit shift as a cup offset from the J4 axis (31 mm at R 33). On the robot the
    # cup is centred under the flange (photo), so the picture moves the arm by that shift instead: same cup
    # path, arm drawn where the fit says the robot really stands relative to the rig.
    shift = np.eye(4)
    shift[:2, 3] = twin.cup_offset(twin.TOOL_R)
    add("arm base_link", T.arm.meshes["base_link"].copy().apply_transform(shift @ base), "static")

    # moving nodes: geometry in its own frame, pose per frame
    first = T.pose_meshes(*cycle.slot_xy(lay, "input", glasses[0], run.by_name), lay["cycle"]["travel_z"])
    movers = list(first)
    for n, (mesh, _) in first.items():
        if n == "cup":
            continue
        add(n, mesh, "moving")
    tool = suction_tool(T.cup_len)
    for n, mesh in tool.items():
        add(n, mesh, "moving")
    movers = [m for m in movers if m != "cup"] + list(tool)
    glass_local = dry_run.box(dry_run.GLASS, (0, 0, 0))
    glass_pose = {}
    for n in glass_names:
        c = T.scene[n].bounds.mean(axis=0)
        add(n, glass_local, "moving")
        glass_pose[n] = np.eye(4)
        glass_pose[n][:3, 3] = c
    for e in json.loads((HERE / "viewer" / "extras.json").read_text(encoding="utf-8")) if (HERE / "viewer" / "extras.json").exists() else []:
        mesh = trimesh.load(twin.LAB / e["stl"] if not (HERE / e["stl"]).exists() else HERE / e["stl"])
        if e.get("frame", "rig") == "rig":
            mesh.apply_transform(twin.rig_matrix())
        name = "extra " + e["name"]
        COLORS[name] = e.get("color", "#b0b0b0")
        m = trimesh.Trimesh(mesh.vertices, mesh.faces, process=False)
        scene.add_geometry(m, node_name=name, geom_name=name)
        static.append({"name": name, "kind": "static"})

    # ---- walk the cycle like the robot ----
    frames, labels, segs = [], [], []
    pos, carried, t = None, None, 0.0
    ox, oy = twin.cup_offset(twin.TOOL_R)
    vi = 0

    contact = {"z": None}       # robot Z where the cup (or the carried glass) first touches the current target

    def press(p):
        return max(0.0, contact["z"] - p[2]) if contact["z"] is not None else 0.0

    def snap(p, label):
        parts = T.pose_meshes(*p)
        if parts is None:
            return
        c = press(p)
        f = {n: qpos(shift @ tf if (n.startswith("arm ") or n.startswith("xiao ")) else tf) for n, (_, tf) in parts.items()}
        for n in ("cup metal", "cup fitting", "cup flange", "cup collet", "cup oring"):
            f[n] = f["cup"]
        # the robot goes c mm lower than the twin's first touch: drawn as the pad giving way (see dry_run.PRESS_ALLOWED)
        rubber = parts["cup"][1].copy()
        rubber[2, 3] += c
        f["cup rubber"] = qpos(rubber)
        if carried:
            g = np.eye(4)
            g[:3, 3] = (p[0] + ox, p[1] + oy, T.cup_tip_z(p[2]) + c - dry_run.GLASS[2] / 2)
            glass_pose[carried] = g
        for n, m in glass_pose.items():
            f[n] = qpos(m)
        frames.append({"t": round(t, 3), "p": [round(v, 2) for v in p], "a": len(labels) - 1, "c": round(c, 2), "s": f})

    inp_h, out_h = cycle.holder(lay, "input"), cycle.holder(lay, "output")
    press_log = []

    def target_of(g):
        return {"input": [f"glass {g}", "holder:" + inp_h["name"]],
                "workstation": ["AtomS3", "holder:" + cycle.holder(lay, "workstation")["name"]],
                "output": ["holder:" + out_h["name"]] + [f"placed glass {k}" for k in glasses]}

    for g in glasses:
        for act in cycle.plan_glass(lay, g, run.by_name):
            if act[0] == "pump":
                if act[1] == "suck":
                    carried = f"glass {g}"
                    for name in (f"glass {g}", f"workstation glass {g}"):
                        if name in T.scene:
                            del T.scene[name]
                    run._refresh()
                    labels.append({"text": f"glass {g}: pump on, glass picked", "status": "event"})
                elif act[1] == "blow" and carried:
                    labels.append({"text": f"glass {g}: blow, glass released", "status": "event"})
                    key = f"workstation glass {g}" if run._near_ws(pos) else f"placed glass {g}"
                    gz = T.cup_tip_z(pos[2]) + press(pos) - dry_run.GLASS[2] / 2
                    T.scene[key] = dry_run.box(dry_run.GLASS, (pos[0] + ox, pos[1] + oy, gz))
                    run._refresh()
                    carried = None
                snap(pos, None)
                continue
            if act[0] == "wait":
                labels.append({"text": f"wait {act[1]} s", "status": "event"})
                t += float(act[1])
                snap(pos, None)
                continue
            if act[0] != "move":
                continue
            _, label, x, y, z = act
            b = (x, y, z)
            if "down to" in label:
                where = "input" if "input" in label else "workstation" if "workstation" in label else "output"
                allowed = set(target_of(g)[where]) | ({f"workstation glass {g}"} if where == "workstation" else set())
                zc, _ = run.first_contact(b, carried, allowed, lay["cycle"]["travel_z"])
                contact["z"] = zc
                if zc is not None:
                    press_log.append(f"glass {g}: {label}: first touch at Z {zc:.1f}, robot goes to {z:.1f} -> "
                                     f"taught Z {zc - z:.1f} mm below the first touch")
            elif "above" in label:
                contact["z"] = None
            st = "ok"
            line = ""
            if vi < len(moves_verdict) and moves_verdict[vi][0] == label:
                st, line = moves_verdict[vi][1], moves_verdict[vi][2]
            if pos is not None:
                vi += 1
            labels.append({"text": label, "status": st, "detail": line, "z": z})
            if pos is None:
                pos = b
                snap(pos, label)
                continue
            n = max(1, int(math.dist(pos, b) / STEP))
            for i in range(1, n + 1):
                p = tuple(pos[k] + (b[k] - pos[k]) * i / n for k in range(3))
                t += math.dist(pos, b) / n / 100.0          # 100 mm/s nominal; the page has a speed control
                snap(p, label)
            pos = b

    OUT.mkdir(parents=True, exist_ok=True)
    scene.export(OUT / "scene.glb")
    colors = {s["name"]: color_for(s["name"]) if not s["name"].startswith("extra ") else COLORS[s["name"]] for s in static}
    meta = {"mode": "planned full cycle" if a.full else "layout.json as the robot runs it",
            "lab": twin.LAB.name, "glasses": glasses, "nodes": static, "colors": colors, "movers": movers + glass_names,
            "actions": labels, "frames": frames, "report": report, "press": press_log,
            "holders": [{"name": h["name"], "cells": h["cells"]} for h in lay["holders"]]}
    (OUT / "anim.json").write_text(json.dumps(meta, separators=(",", ":")), encoding="utf-8")
    print(chr(10).join(press_log))
    print(f"{len(frames)} frames, {t:.0f} s at 100 mm/s, {len(static)} objects -> {OUT}")


if __name__ == "__main__":
    main()
