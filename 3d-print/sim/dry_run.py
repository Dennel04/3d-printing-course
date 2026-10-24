"""dry_run.py — run the real slot-picker glass cycle (slot-picker/cycle.py) in the twin before the robot.

Uses the action list cycle.plan_glass() builds for the robot and slot-picker/layout.json as it is
(mode, roles, taught dx/dy/Z), i.e. what the robot would run now. A Z not taught yet is derived from
the twin geometry (pick: cup on the glass top pressed 1 mm, place on the workstation: glass on the Atom
screen, output: glass 1 mm above the floor); taught and derived values are both reported.
--full checks the planned full cycle instead: roles below, workstation step on, all Z derived. Every move is checked as a straight line every 2 mm (assumption: mg400-base streams a
straight Cartesian path): joint limits, and collisions of the arm, the XIAO mount, the cup and the
carried glass with the rig, holders, the webcam post, glasses in pockets and the battery+Atom stack.
The cup and the carried glass may touch only their own target pocket during approach/down/lift.

Writes <lab>/docs/sim_dry_run.txt (--full: sim_dry_run_full.txt).
Run: .venv/Scripts/python dry_run.py [--lab ../lab2] [--glasses 1,2,3,4] [--full]
"""
import argparse
import copy
import math
import sys

import fcl
import numpy as np
import trimesh

import mg400_kin as kin
import twin

cycle = None


def load_cycle():
    """The lab's own slot-picker/cycle.py (the code the robot runs)."""
    global cycle
    path = str(twin.LAB / "slot-picker")
    if path not in sys.path:
        sys.path.insert(0, path)
    import importlib
    cycle = importlib.import_module("cycle")
    return cycle


load_cycle()

GLASS = (30.0, 30.0, 2.0)
ATOM_H, BATTERY_H = 12.9, 21.97          # measurements.md (Atom nominal, battery measured)
STEP = 2.0
WARN_CLEARANCE = 3.0
PICK_OFFSET_MAX = (GLASS[0] - twin.CUP_D) / 2   # cup fully on the glass up to this offset (5 mm)
PRESS_ALLOWED = 1.5     # the cup may press this far into its target (picks are taught 1 mm into the glass)
ROLES = {"input": "Glass input", "workstation": "Workstation (orange)", "output": "Good output"}


def box(extents, centre):
    m = trimesh.creation.box(extents=extents)
    m.apply_translation(centre)
    return m


class Run:
    def __init__(self, glasses, full=False):
        lay = copy.deepcopy(twin.json.loads((twin.LAB / "slot-picker" / "layout.json").read_text(encoding="utf-8")))
        self.full = full
        if full:
            lay["cycle"]["roles"] = dict(ROLES)
            lay["cycle"]["workstation_step"] = True
            lay["cycle"]["workstation_cell"] = None
            for h in lay["holders"]:
                h.pop("teach", None)
        for role, name in ROLES.items():
            lay["cycle"]["roles"][role] = lay["cycle"]["roles"].get(role) or name
        ws_h = cycle.holder(lay, "workstation")
        lay["cycle"]["workstation_cell"] = lay["cycle"].get("workstation_cell") or ws_h["cells"][0]
        self.lay = lay
        self.T = twin.Twin(layout=lay)
        self.by_name = {}
        for r in "ABCDEFG":
            for n in (5, 4, 3, 2, 1, -1, -2, -3, -4, -5):
                c = f"{r}{n:+d}"
                x, y = twin.flange_for_cup(c)
                self.by_name[c] = {"name": c, "x": x, "y": y, "blocked": None}
        self.glasses = glasses
        self.log = []
        self._teach()
        self._place_parts()

    # floor of the pocket under a cell centre (top surface of the holder there), world z
    def _surface(self, holder_name, cell):
        mesh = self.T.scene["holder:" + holder_name]
        p = twin.rig_to_world((*twin.cell_model(cell), 0))
        loc, _, _ = mesh.ray.intersects_location([[p[0], p[1], 300.0]], [[0, 0, -1.0]])
        return float(loc[:, 2].max())

    def _teach(self):
        T, lay = self.T, self.lay
        inp, ws, out = (cycle.holder(lay, r) for r in ("input", "workstation", "output"))
        self.floor = {"input": self._surface(inp["name"], inp["cells"][0]),
                      "workstation": self._surface(ws["name"], lay["cycle"]["workstation_cell"]),
                      "output": self._surface(out["name"], out["cells"][0])}
        self.atom_top = self.floor["workstation"] + BATTERY_H + ATOM_H
        g = GLASS[2]
        derived = {"input": {"pick_z": T.robot_z_for_tip(self.floor["input"] + g - 1)},
                   "workstation": {"place_z": T.robot_z_for_tip(self.atom_top + g),
                                   "pick_z": T.robot_z_for_tip(self.atom_top + g - 1)},
                   "output": {"place_z": T.robot_z_for_tip(self.floor["output"] + g + 1)}}
        used = cycle.roles(lay)
        self.log.append("mode: " + ("planned full cycle" if self.full else "layout.json as is, "
                        + ("full cycle" if lay["cycle"].get("workstation_step") else "transfer test (no workstation)"))
                        + "; " + ", ".join(f"{r} = {cycle.holder(lay, r)['name']}" for r in used))
        # roles may share one holder (transfer test): fill in only what a used role misses, never overwrite
        for role, h in (("input", inp), ("workstation", ws), ("output", out)):
            if role not in used:
                continue
            t = h.setdefault("teach", {})
            t.setdefault("dx", 0)
            t.setdefault("dy", 0)
            for k, v in derived[role].items():
                v = round(v, 1)
                if t.get(k) is None:
                    t[k] = v
                    self.log.append(f"{role} {k}: not taught, derived {v}")
                else:
                    self.log.append(f"{role} {k}: taught {t[k]}, twin derives {v} ({t[k] - v:+.1f} mm)"
                                    + (f"; taught dx {t['dx']} dy {t['dy']}" if t["dx"] or t["dy"] else ""))
        self.log.append(f"pocket floors z {self.floor['input']:.2f} / {self.floor['workstation']:.2f} / "
                        f"{self.floor['output']:.2f}, Atom top z {self.atom_top:.2f}")

    def _world(self, cell):
        return twin.rig_to_world((*twin.cell_model(cell), 0))[:2]

    def _place_parts(self):
        lay = self.lay
        inp = cycle.holder(lay, "input")
        for g in self.glasses:
            x, y = self._world(inp["cells"][g - 1])
            self.T.scene[f"glass {g}"] = box(GLASS, (x, y, self.floor["input"] + GLASS[2] / 2))
        if not lay["cycle"].get("workstation_step"):     # transfer test: no battery + Atom on the table
            self._refresh()
            return
        x, y = self._world(lay["cycle"]["workstation_cell"])
        f = self.floor["workstation"]
        self.T.scene["battery"] = box((24.04, 24.01, BATTERY_H), (x, y, f + BATTERY_H / 2))
        self.T.scene["AtomS3"] = box((24, 24, ATOM_H), (x, y, f + BATTERY_H + ATOM_H / 2))
        self._refresh()

    def _refresh(self):
        self.T._build_fcl()
        self.T._scene_box = {n: (m.bounds[0], m.bounds[1]) for n, m in self.T.scene.items()}

    # ---- checking one straight move ----
    def check_move(self, a, b, label, carried, allowed):
        n = max(1, int(math.dist(a, b) / STEP))
        worst = (math.inf, "", "")
        problems = []
        for i in range(n + 1):
            p = [a[k] + (b[k] - a[k]) * i / n for k in range(3)]
            ok, why, _ = kin.check(*p)
            if not ok:
                problems.append(f"joint limit at {tuple(round(v, 1) for v in p)}: {why}")
                break
            hits = [h for h in self.T.collisions(*p) if not (h[0] == "cup" and h[1] in allowed)]
            if carried is not None:
                hits += [("carried glass", s) for s in self._glass_hits(p, allowed)]
            if hits:
                problems.append(f"{hits[0][0]} touches {hits[0][1]} at {tuple(round(v, 1) for v in p)}")
                break
            if i % 5 == 0 or i == n:
                for d, part, s in self._near(p, allowed, carried):
                    if d < worst[0]:
                        worst = (d, part, s)
        return problems, worst

    def _glass_obj(self, p):
        ox, oy = twin.cup_offset(twin.TOOL_R)
        tip = self.T.cup_tip_z(p[2])
        g = fcl.Box(*GLASS)
        return fcl.CollisionObject(g, fcl.Transform(np.eye(3), [p[0] + ox, p[1] + oy, tip - GLASS[2] / 2]))

    def _glass_hits(self, p, allowed):
        obj = self._glass_obj(p)
        return [s for s, o in self.T._scene_obj.items() if s not in allowed and
                fcl.collide(obj, o, fcl.CollisionRequest(), fcl.CollisionResult())]

    def _near(self, p, allowed, carried):
        """Smallest distances of every moving part at p (only scene parts within 30 mm of its box)."""
        out = []
        parts = self.T.pose_meshes(*p)
        movers = []
        for name, (mesh, tf) in parts.items():
            g = fcl.Cylinder(mesh.extents[0] / 2, mesh.extents[2]) if name == "cup" else self.T._arm_bvh[name]
            movers.append((name, fcl.CollisionObject(g, fcl.Transform(tf[:3, :3], tf[:3, 3])),
                           *self.T._aabb(mesh, tf)))
        if carried is not None:
            o = self._glass_obj(p)
            c = np.array(o.getTranslation())
            movers.append(("carried glass", o, c - 16, c + 16))
        for name, obj, lo, hi in movers:
            for s, (slo, shi) in self.T._scene_box.items():
                if name in ("cup", "carried glass") and s in allowed:
                    continue
                if (lo - 30 > shi).any() or (hi + 30 < slo).any():
                    continue
                d = fcl.distance(obj, self.T._scene_obj[s], fcl.DistanceRequest(), fcl.DistanceResult())
                out.append((d, name, s))
        return out

    def run(self):
        lay, T = self.lay, self.T
        inp, out = cycle.holder(lay, "input"), cycle.holder(lay, "output")
        pos = None
        carried = None
        last_allowed = set()
        report = list(self.log)
        for g in self.glasses:
            target_of = {"input": [f"glass {g}", "holder:" + inp["name"]],
                         "workstation": ["AtomS3", "holder:" + cycle.holder(lay, "workstation")["name"]],
                         "output": ["holder:" + out["name"]] + [f"placed glass {k}" for k in self.glasses]}
            for act in cycle.plan_glass(lay, g, self.by_name):
                if act[0] == "pump":
                    if act[1] == "suck":
                        carried = g
                        name = f"glass {g}" if f"glass {g}" in T.scene else None
                        if pos and self._near_ws(pos):
                            name = f"workstation glass {g}"
                        if name and name in T.scene:
                            ox, oy = twin.cup_offset(twin.TOOL_R)
                            c = T.scene[name].bounds.mean(axis=0)
                            off = math.hypot(pos[0] + ox - c[0], pos[1] + oy - c[1])
                            report.append(f"glass {g}: pick {name}: cup {off:.1f} mm from the glass centre "
                                          + ("ok" if off <= PICK_OFFSET_MAX else
                                             f"COLLISION-free but the cup is not fully on the glass (> {PICK_OFFSET_MAX:.0f} mm): suction may fail"))
                            del T.scene[name]
                            self._refresh()
                    elif act[1] == "blow" and carried is not None:
                        ox, oy = twin.cup_offset(twin.TOOL_R)
                        tip = T.cup_tip_z(pos[2])
                        key = f"workstation glass {g}" if self._near_ws(pos) else f"placed glass {g}"
                        report.append(f"glass {g}: release -> " + self._landing(pos, tip, {"AtomS3"} if self._near_ws(pos) else last_allowed))
                        T.scene[key] = box(GLASS, (pos[0] + ox, pos[1] + oy, tip - GLASS[2] / 2))
                        self._refresh()
                        carried = None
                    continue
                if act[0] != "move":
                    continue
                _, label, x, y, z = act
                b = (x, y, z)
                if pos is None:
                    pos = (x, y, z)
                    continue
                where = "input" if "input" in label else "workstation" if "workstation" in label else "output"
                allowed = set(target_of[where]) | ({f"workstation glass {g}"} if where == "workstation" else set())
                if "above" in label:          # travelling: only the pocket we leave may still be touched at the start
                    allowed = set()
                last_allowed = allowed
                probs, worst = self.check_move(pos, b, label, carried, allowed)
                if allowed and not probs and b[2] < pos[2]:
                    zc, what = self.first_contact(b, carried, allowed, max(pos[2], self.lay["cycle"]["travel_z"]))
                    if zc is not None and b[2] < zc - PRESS_ALLOWED:
                        probs.append(f"pushes {zc - b[2]:.1f} mm into {what} (first touch at Z {zc:.1f}, "
                                     f"allowed {PRESS_ALLOWED} mm)")
                status = "COLLISION" if probs else ("close" if worst[0] < WARN_CLEARANCE else "ok")
                report.append(f"glass {g}: {label:38} {status:9} min clearance {worst[0]:6.1f} mm ({worst[1]} - {worst[2]})"
                              + (f"\n      !! {probs[0]}" if probs else ""))
                pos = b
        return report

    def _landing(self, p, tip, allowed):
        """What is under the released glass: rays down from its 4 corners and centre."""
        ox, oy = twin.cup_offset(twin.TOOL_R)
        cx, cy = p[0] + ox, p[1] + oy
        under = []
        for dx, dy in ((0, 0), (14, 14), (14, -14), (-14, 14), (-14, -14)):
            best = (-math.inf, "nothing")
            for n, m in self.T.scene.items():
                loc, _, _ = m.ray.intersects_location([[cx + dx, cy + dy, tip - GLASS[2] + 0.5]], [[0, 0, -1.0]])
                if len(loc) and loc[:, 2].max() > best[0]:
                    best = (loc[:, 2].max(), n)
            under.append(best)
        top_z, support = max(under)
        centre_z, centre_on = under[0]
        drop = tip - GLASS[2] - top_z
        overhang = sorted({n for z, n in under if z < top_z - 0.5})
        if support in allowed and centre_on == support:
            return (f"rests on {support}, falls {drop:.1f} mm, ok"
                    + (f" (edges overhang {', '.join(overhang)})" if overhang else ""))
        return (f"WRONG PLACE: glass rests on {support}" + (f", centre over {centre_on}" if centre_on != support else "")
                + f" (falls {drop:.1f} mm)")

    def first_contact(self, p, carried, allowed, z_from):
        """Highest Z (going down from z_from at p's X/Y) where the cup or the carried glass touches a target."""
        def touching(z):
            q = (p[0], p[1], z)
            hit = [h[1] for h in self.T.collisions(*q) if h[0] == "cup" and h[1] in allowed]
            if carried is not None:
                obj = self._glass_obj(q)
                hit += [s for s in allowed if s in self.T._scene_obj and
                        fcl.collide(obj, self.T._scene_obj[s], fcl.CollisionRequest(), fcl.CollisionResult())]
            return hit
        if not touching(p[2]):
            return None, None
        hi, lo = z_from, p[2]
        if touching(hi):
            return hi, touching(hi)[0]
        while hi - lo > 0.05:          # hi: not touching, lo: touching
            mid = (hi + lo) / 2
            if touching(mid):
                lo = mid
            else:
                hi = mid
        return hi, touching(lo)[0]

    def _near_ws(self, p):
        if not self.lay["cycle"].get("workstation_step"):
            return False
        wx, wy = cycle.slot_xy(self.lay, "workstation", 1, self.by_name)
        return math.hypot(p[0] - wx, p[1] - wy) < 1.0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glasses", default="1,2,3,4")
    ap.add_argument("--full", action="store_true", help="the planned full cycle instead of layout.json as is")
    twin.add_lab_arg(ap)
    a = ap.parse_args()
    twin.use_lab(a.lab)
    load_cycle()
    run = Run([int(v) for v in a.glasses.split(",")], full=a.full)
    rep = run.run()
    text = "\n".join(rep)
    print(text)
    (twin.LAB / "docs" / ("sim_dry_run_full.txt" if a.full else "sim_dry_run.txt")).write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
