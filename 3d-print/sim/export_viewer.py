"""export_viewer.py — the glass cycle of the twin for the 3D viewer (viewer/index.html).

Same layout.json, cycle.py, cells.py and arm model as dry_run.py. Writes
  viewer/data/scene.glb   every object as a named node: static ones in world coordinates (z up, mm),
                          moving ones (arm links, XIAO mount, cup, glasses) in their own frame
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
    if name == "AtomS3":
        return "#7aa7d9"
    if name.startswith("arm "):
        return "#e9ecef" if "link5" not in name else "#c9ced4"
    if name == "xiao mount":
        return "#f26b1d"
    if name == "cup rubber":
        return "#161616"
    if name in ("cup metal", "cup fitting"):
        return "#c3c8ce"
    if name.startswith("glass"):
        return "#9fd3ff"
    return "#b0b0b0"


# Suction tool as on the robot (photo docs/photos/mg400-tool-mount-side-2026-10-24.jpg, scaled by the caliper
# cup OD 22.25 mm): Dobot kit flange hub -> clamp collar -> buffer body with a side 4 mm push-in fitting ->
# nut -> buffer rod -> black bellows cup. No public CAD exists (Dobot, SMC-type buffer pad); proportions from
# the photo, total stretched to the twin's cup length. Only for the picture: collisions use the twin cylinder.
PHOTO_LEN = 79.5
TOOL_PROFILE = {   # part: [(radius, z from the motor bottom down, photo mm), ...]
    "cup metal": [(0, 0), (15, 0), (15, 4), (22, 4), (22, 8), (11, 8), (11, 19), (9, 19), (9, 57), (7.5, 57),
                  (7.5, 65), (4, 65), (4, 67), (0, 67)],
    "cup rubber": [(0, 66), (6.5, 66), (8, 69), (7, 71.5), (11.125, 78.5), (11.125, 79.5), (0, 79.5)],
}


def suction_tool(length):
    """Meshes of the tool in the twin's cup frame (z up, top at +length/2, tip at -length/2)."""
    k = length / PHOTO_LEN
    out = {}
    for name, prof in TOOL_PROFILE.items():
        pts = [(r, length / 2 - z * k) for r, z in prof]
        m = trimesh.creation.revolve(np.array(pts[::-1]), sections=48)
        out[name] = m
    # side push-in fitting (hex + collet), towards +x, at photo z 49
    zf = length / 2 - 49 * k
    hexn = trimesh.creation.cylinder(radius=5, height=7, sections=6)
    hexn.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, (0, 1, 0)))
    hexn.apply_translation((9 + 3.5, 0, zf))
    collet = trimesh.creation.cylinder(radius=4.2, height=9, sections=24)
    collet.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, (0, 1, 0)))
    collet.apply_translation((9 + 7 + 4.5, 0, zf))
    out["cup fitting"] = trimesh.util.concatenate([hexn, collet])
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
        f = {n: qpos(shift @ tf if (n.startswith("arm ") or n == "xiao mount") else tf) for n, (_, tf) in parts.items()}
        for n in ("cup metal", "cup fitting"):
            f[n] = f["cup"]
        # the bellows cup + buffer rod give way: the robot goes c mm lower than the first touch
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
                                     f"cup + buffer compressed {zc - z:.1f} mm")
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
