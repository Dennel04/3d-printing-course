"""twin.py — digital twin of the MG400 workstation: MG400 + rig + holders + tool, exact mesh collisions.
Shared by all labs (3d-print/sim); the lab-specific inputs come from the lab folder chosen with use_lab()
(default 3d-print/lab2, or the SIM_LAB environment variable; the scripts take --lab).

World frame W = robot frame: origin on the J1 axis at the robot floor, X/Y as the robot reports them,
z = height above the robot floor in mm (the rig model's z). Robot Z (as GetPose reports it) is not
the same number: z_link5 = Z + HZ, computed from the URDF against the fitted joint model.

Sources (all in this repo or vendored):
- joints and limits: mg400_kin.py (= mg400-base, fitted to the real arm)
- arm geometry: robot/ (Dobot-Arm/MG400_ROS URDF + meshes, MIT, commit 2bcf6a9)
- rig: scene/rakis_*.stl (MG 400 rakis, exported from Fusion in the rig frame)
- grid -> robot: <lab>/calibration/cells.py (lab2: 24.10.26 fit, rotation +0.87 deg)
- holders: <lab>/slot-picker/layout.json + the holders' STL files in <lab>
"""
import importlib.util
import json
import math
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import fcl
import numpy as np
import trimesh

import mg400_kin as kin

HERE = Path(__file__).resolve().parent
LAB = None
cells = None
FIT_DEG, _robot_of, _C, _S = 0.0, None, 1.0, 0.0


def use_lab(path):
    """Point the twin at a lab folder: its calibration (cells.py), layout, cycle and part files."""
    global LAB, cells, FIT_DEG, _robot_of, _C, _S
    LAB = Path(path).resolve()
    spec = importlib.util.spec_from_file_location("cells", LAB / "calibration" / "cells.py")
    cells = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cells)
    FIT_DEG, _robot_of = cells.fit()
    _C, _S = math.cos(math.radians(FIT_DEG)), math.sin(math.radians(FIT_DEG))
    return LAB


def add_lab_arg(ap):
    ap.add_argument("--lab", default=os.environ.get("SIM_LAB", str(HERE.parent / "lab2")),
                    help="lab folder with calibration/, slot-picker/ and the part files (default: lab2)")

GRID_TOP = 7.28          # rig model: grid top above the robot floor
TOOL_R = 33.0            # every calibrated point is taken at R 33
# Cup length below the J4 motor, from the 24.10 D-2 touch (Z -150 on the glass holder v1 pocket floor,
# holder on its 3 mm foot extension, +2.85 mm). Cross-check: 23.10 G-1 corners then sit 1.6 mm above the
# first calibration bin floor (the other assumption puts the cup 1.2 mm under the floor). TODO measure.
CUP_LEN = 66.2

# ---- tool (TODO measure: cup diameter, cup offset from the J4 axis, cup length) ----
CUP_D = 22.25            # suction cup outer diameter, mm (caliper 24.10, measurements.md; effective ~23 from the C-2 corners)
# Calibration fit: flange - cup = (31.10, 0.08) mm at R 33 (robot frame). Assumes the robot sits in the
# rig exactly as in CAD, so the whole fit shift is the cup's offset from the J4 axis.
CUP_OFFSET_R33 = (-31.10, -0.08)
MOTOR_LEN = 85.0         # link5 (J4 motor) hangs this far below its frame origin (URDF mesh)

# ---- holder STL per layout type, and how the part sits (z of its local 0 above the grid top) ----
HOLDER_STL = {
    "glass": "glass-input-holder/stl/glass-input-holder.stl",
    "atom": "atoms3-input-holder/stl/atoms3-input-holder-v1.stl",
    "workstation": "ready-parts-input-holder/stl/ready-parts-input-holder-v1.stl",
    "output": "valjundhoidik/stl/valjundhoidik-v1.stl",
    "calibration": "gridfinity-calibration/stl/gridfinity-calibration.stl",
}
# local z = 0 is the base bottom (feet below it); the calibration bin is placed by its bounds instead.
CAL_FOOT_Z = 2.289          # calibration bin foot bottom when seated (1 x 1 wedges on the chamfers)
BEAM_TOP = 2.48          # rig model: top of the beams under the +-1 / +-3 columns
TABLE_Z = -16.72         # table = grid bottom (Denys, 24.10)
PIPE_D, PIPE_Y, PIPE_Z = 16.0, 110.5, -7.1      # rig pipes (MG 400 rakis.md)
PIPE_LEN, PIPE_X_FRONT = 670.0, -586.5          # front end 50 mm past the table edge (x -536.5)
POST_PIPE_X, POST_PIPE_Z0, POST_PIPE_LEN = -555.7, 7.5, 458.0
FOOT = 4.65              # socket depth; a deeper foot (old 3 mm extension) stands on the beams


def holder_lift(mesh):
    """How much higher than the grid top an old-foot holder stands: its foot reaches below the beam tops."""
    depth = -mesh.bounds[0][2]
    return max(0.0, depth - (GRID_TOP - BEAM_TOP))


def cell_model(cell):
    """Cell centre in the rig model frame (mm), assignment formula."""
    x, y = cells.model(cell)       # cells.model returns the 180-deg rotated (-x, -y)
    return -x, -y


def rig_to_world(p):
    """Rig model point (x, y, z) -> world: rotated 180 deg + the fitted rotation about the J1 axis."""
    x, y = -p[0], -p[1]
    return (_C * x - _S * y, _S * x + _C * y, p[2])


def rig_matrix():
    m = np.eye(4)
    m[:2, :2] = [[-_C, _S], [-_S, -_C]]
    return m


def cup_offset(r_deg):
    a = math.radians(r_deg - TOOL_R)
    c, s = math.cos(a), math.sin(a)
    x, y = CUP_OFFSET_R33
    return c * x - s * y, s * x + c * y


def flange_for_cup(cell, r_deg=TOOL_R):
    """Robot X/Y that puts the cup over the cell centre (same as cells.py at R 33)."""
    x, y = _robot_of(cell)
    if r_deg != TOOL_R:
        cx, cy = cup_offset(TOOL_R)
        ox, oy = cup_offset(r_deg)
        x, y = x + cx - ox, y + cy - oy
    return x, y


# ---------------- arm: URDF forward kinematics with the parallelogram mimics ----------------
class Arm:
    def __init__(self):
        root = ET.parse(HERE / "robot" / "mg400_description.urdf").getroot()
        self.joints = {}
        for j in root.findall("joint"):
            o = j.find("origin")
            xyz = [float(v) * 1000 for v in (o.get("xyz") if o is not None else "0 0 0").split()]
            ax = j.find("axis")
            axis = [float(v) for v in (ax.get("xyz") if ax is not None else "0 0 1").split()]
            m = j.find("mimic")
            self.joints[j.get("name")] = dict(parent=j.find("parent").get("link"), child=j.find("child").get("link"),
                                              xyz=xyz, axis=axis,
                                              mimic=(m.get("joint"), float(m.get("multiplier") or 1)) if m is not None else None)
        self.meshes = {}
        for lk in root.findall("link"):
            if lk.find("visual") is not None:
                mesh = trimesh.load(HERE / "robot" / "meshes" / f"{lk.get('name')}.STL")
                mesh.apply_scale(1000.0)
                self.meshes[lk.get("name")] = mesh
        self.J1_X = -self.joints["j1"]["xyz"][0]     # base_link origin is 5 mm behind the J1 axis

    def angles(self, j1, j2, j3, j4):
        """Dobot joint angles (deg) -> URDF joint values (rad), mimics resolved."""
        q = {"j1": j1, "j2": j2, "j3": j3, "j4": j4}
        q = {k: math.radians(v) for k, v in q.items()}
        done = False
        while not done:
            done = True
            for n, j in self.joints.items():
                if n not in q and j["mimic"] and j["mimic"][0] in q:
                    q[n] = q[j["mimic"][0]] * j["mimic"][1]
                    done = False
        return q

    def link_poses(self, j1, j2, j3, j4):
        q = self.angles(j1, j2, j3, j4)
        base = np.eye(4)
        base[0, 3] = self.J1_X
        poses = {"base_link": base}
        pending = dict(self.joints)
        while pending:
            for n, j in list(pending.items()):
                if j["parent"] in poses:
                    t = np.eye(4)
                    t[:3, 3] = j["xyz"]
                    t[:3, :3] = trimesh.transformations.rotation_matrix(q.get(n, 0.0), j["axis"])[:3, :3]
                    poses[j["child"]] = poses[j["parent"]] @ t
                    del pending[n]
        return poses


# ---------------- the twin ----------------
class Twin:
    def __init__(self, layout=None, with_post=True, calibration_at=None):
        self.arm = Arm()
        self.layout = layout or json.loads((LAB / "slot-picker" / "layout.json").read_text(encoding="utf-8"))
        self.HZ = self._fit_hz()
        self.cup_len = CUP_LEN
        self.scene = {}               # name -> trimesh in world frame
        self._load_rig()
        self._load_table()
        self._load_holders(with_post, calibration_at)
        self._tool_meshes()
        self._build_fcl()

    # robot Z -> world z of the link5 frame origin
    def _fit_hz(self):
        d = []
        for j2 in range(0, 81, 10):
            for j3 in range(-20, 101, 10):
                if abs(j3 - j2) > 58:
                    continue
                x, y, z = kin.forward(0, j2, j3)
                p = self.arm.link_poses(0, j2, j3, 0)["link5"][:3, 3]
                d.append((p[2] - z, math.hypot(p[0], p[1]) - math.hypot(x, y)))
        d = np.array(d)
        self.fk_spread = (d[:, 0].std(), np.abs(d[:, 1]).max())
        return float(d[:, 0].mean())

    def _add(self, name, mesh):
        self.scene[name] = mesh

    def _load_rig(self):
        m = rig_matrix()
        for f in sorted((HERE / "scene").glob("rakis_*.stl")):
            if f.stem.startswith("rakis_pipe_long"):
                continue                # drawn below at their real length and place
            mesh = trimesh.load(f)
            mesh.apply_transform(m)
            self._add(f.stem, mesh)
        # the two 16 mm pipes: 670 mm (table 700 - 30, rakis doc), front ends ~50 mm past the table edge since
        # Denys moved the L brackets (24.10, by eye); axes y +-110.5, z -7.1 in the rig model
        for side, y in (("neg", -PIPE_Y), ("pos", PIPE_Y)):
            pipe = trimesh.creation.cylinder(radius=PIPE_D / 2, height=PIPE_LEN, sections=32)
            pipe.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, (0, 1, 0)))
            pipe.apply_translation((PIPE_X_FRONT + PIPE_LEN / 2, y, PIPE_Z))
            pipe.apply_transform(m)
            self._add(f"rakis_pipe_long_{side}", pipe)

    def _load_table(self):
        box = trimesh.creation.box(extents=(700, 700, 20))
        box.apply_translation((-300, 0, TABLE_Z - 10))     # rig frame, under the grid and the post
        box.apply_transform(rig_matrix())
        self._add("table", box)

    def _settle(self, mesh):
        """Drop a holder (world frame, at its cell) onto the rig like gravity would: lowest height where it
        touches the grid, beams or pipes but does not cut into them. Moves the mesh; returns the change in mm."""
        lo, hi = mesh.bounds
        obj = fcl.CollisionObject(self._bvh(mesh))
        sup = []
        for n, m in self.scene.items():
            if not (n.startswith("rakis") or n == "table"):
                continue
            b = m.bounds
            if (b[0][:2] > hi[:2] + 1).any() or (b[1][:2] < lo[:2] - 1).any():
                continue
            if n not in self._sup_cache:
                self._sup_cache[n] = fcl.CollisionObject(self._bvh(m))
            sup.append(self._sup_cache[n])

        def hits(dz):
            obj.setTransform(fcl.Transform(np.eye(3), [0.0, 0.0, dz]))
            return any(fcl.collide(obj, s, fcl.CollisionRequest(), fcl.CollisionResult()) for s in sup)
        up = 0.0
        while hits(up):
            up += 5.0
            if up > 60:
                raise RuntimeError("holder cannot be placed: cuts into the rig even 60 mm higher")
        down = up - 1.0                       # small steps: fcl only sees surfaces crossing, a big step could
        while not hits(down):                 # jump through a thin wall
            down -= 1.0
            if down < -60:
                raise RuntimeError("holder falls through the rig")
        a, b = down, up                       # a: cutting in, b: free
        while b - a > 0.01:
            m_ = (a + b) / 2
            if hits(m_):
                a = m_
            else:
                b = m_
        mesh.apply_translation((0, 0, b))
        return b

    def _load_holders(self, with_post, calibration_at):
        self.seat = {}
        self._sup_cache = {}
        for h in self.layout["holders"]:
            path = HOLDER_STL.get(h["type"])
            if not path:
                continue
            mesh = trimesh.load(LAB / path)
            if h["type"] == "calibration":
                b = mesh.bounds
                x0, y0, z0 = (b[0][0] + b[1][0]) / 2, (b[0][1] + b[1][1]) / 2, CAL_FOOT_Z - b[0][2]
            else:
                x0, y0, z0 = 0.0, 0.0, GRID_TOP + holder_lift(mesh)
            cs = [cell_model(c) for c in h["cells"]]
            cx, cy = sum(c[0] for c in cs) / len(cs), sum(c[1] for c in cs) / len(cs)
            t = np.eye(4)
            t[:3, 3] = (cx - x0, cy - y0, z0)
            mesh.apply_transform(t)
            mesh.apply_transform(rig_matrix())
            self.seat[h["name"]] = (z0, self._settle(mesh))
            self._add("holder:" + h["name"], mesh)
        if with_post:
            for part in ("nurk", "ulemine"):
                mesh = trimesh.load(LAB / f"veebikaamera-post/stl/veebikaamera-post-v1-{part}.stl")
                mesh.apply_transform(rig_matrix())
                self._add("webcam post " + part, mesh)
            # vertical 16 mm pipe between the elbow and the top part (tools/fusion-mcp/s_post_v4.py: axis
            # x -555.7 / y -110.5 in the rig model, from the socket floor z 7.5, 458 mm)
            pipe = trimesh.creation.cylinder(radius=PIPE_D / 2, height=POST_PIPE_LEN, sections=32)
            pipe.apply_translation((POST_PIPE_X, -PIPE_Y, POST_PIPE_Z0 + POST_PIPE_LEN / 2))
            pipe.apply_transform(rig_matrix())
            self._add("webcam post pipe", pipe)
        if calibration_at:
            mesh = trimesh.load(LAB / "gridfinity-calibration/stl/gridfinity-calibration.stl")
            b = mesh.bounds
            cx, cy = cell_model(calibration_at)
            t = np.eye(4)
            t[:3, 3] = (cx - (b[0][0] + b[1][0]) / 2, cy - (b[0][1] + b[1][1]) / 2, CAL_FOOT_Z - b[0][2])
            mesh.apply_transform(t)
            mesh.apply_transform(rig_matrix())
            self.seat["calibration"] = (CAL_FOOT_Z, self._settle(mesh))
            self._add("calibration", mesh)

    def _tool_meshes(self):
        # XIAO mount v2: its file frame has the J4 axis at x = y = 0 and the motor bottom at z = -13,
        # the arm pointing -X; link5 frame: arm along +X, motor bottom at z = -85.
        mount = trimesh.load(LAB / "camera-mounts/stl/xiao-square-mount-v2.stl")
        t = trimesh.transformations.rotation_matrix(math.pi, (0, 0, 1))
        t[2, 3] = -MOTOR_LEN + 13.0
        mount.apply_transform(t)
        self.mount_local = mount

    # ---- tool length from a touch: cup pressed on a known surface at a known robot Z ----
    def set_cup_length_from_touch(self, robot_z, surface_z):
        self.cup_len = robot_z + self.HZ - MOTOR_LEN - surface_z
        return self.cup_len

    def cup_tip_z(self, robot_z):
        return robot_z + self.HZ - MOTOR_LEN - self.cup_len

    def robot_z_for_tip(self, tip_z):
        return tip_z - self.HZ + MOTOR_LEN + self.cup_len

    # ---- geometry at a pose ----
    def pose_meshes(self, x, y, z, r=TOOL_R, joints=None):
        j = joints or kin.inverse(x, y, z)
        if j is None:
            return None
        j1, j2, j3 = j[:3]
        poses = self.arm.link_poses(j1, j2, j3, r - j1)
        out = {}
        for name, mesh in self.arm.meshes.items():
            if name == "base_link":
                continue
            out["arm " + name] = (mesh, poses[name])
        # tool parts ride on the fitted flange position (the URDF arm drawing is up to ~4 mm off)
        t5 = poses["link5"].copy()
        t5[:3, 3] = (x, y, z + self.HZ)
        # the XIAO mount sits on the J4 motor square, which does not turn with J4: its yaw follows J1 only
        tm = self.arm.link_poses(j1, j2, j3, 0.0)["link5"].copy()
        tm[:3, 3] = t5[:3, 3]
        out["xiao mount"] = (self.mount_local, tm)
        ox, oy = cup_offset(r)
        tip = self.cup_tip_z(z)
        top = z + self.HZ - MOTOR_LEN
        cup = trimesh.creation.cylinder(radius=CUP_D / 2, height=top - tip, sections=32)
        t = np.eye(4)
        t[:3, :3] = t5[:3, :3]          # turns with J4 (the side vacuum fitting shows it in the viewer)
        t[:3, 3] = (x + ox, y + oy, (tip + top) / 2)
        out["cup"] = (cup, t)
        return out

    # ---- fcl ----
    @staticmethod
    def _bvh(mesh):
        m = fcl.BVHModel()
        m.beginModel(len(mesh.vertices), len(mesh.faces))
        m.addSubModel(np.asarray(mesh.vertices, dtype=float), np.asarray(mesh.faces, dtype=np.int32))
        m.endModel()
        return m

    def _build_fcl(self):
        self._scene_obj = {n: fcl.CollisionObject(self._bvh(m)) for n, m in self.scene.items()}
        self._arm_bvh = {"arm " + n: self._bvh(m) for n, m in self.arm.meshes.items() if n != "base_link"}
        self._arm_bvh["xiao mount"] = self._bvh(self.mount_local)

    def clearance(self, x, y, z, r=TOOL_R, ignore=(), cup_ignore=()):
        """Smallest distance (mm) from every moving part to every scene part at this pose, worst first.
        ignore: scene names skipped for all parts; cup_ignore: skipped for the cup only (its target)."""
        parts = self.pose_meshes(x, y, z, r)
        if parts is None:
            return None
        res = []
        for pname, (mesh, tf) in parts.items():
            if pname == "cup":
                g = fcl.Cylinder(mesh.extents[0] / 2, mesh.extents[2])
            else:
                g = self._arm_bvh[pname]
            obj = fcl.CollisionObject(g, fcl.Transform(tf[:3, :3], tf[:3, 3]))
            for sname, sobj in self._scene_obj.items():
                if sname in ignore or (pname == "cup" and sname in cup_ignore):
                    continue
                req, rr = fcl.DistanceRequest(enable_signed_distance=True), fcl.DistanceResult()
                d = fcl.distance(obj, sobj, req, rr)
                res.append((d, pname, sname))
        res.sort()
        return res


    def _aabb(self, mesh, tf):
        c = trimesh.transformations.transform_points(trimesh.bounds.corners(mesh.bounds), tf)
        return c.min(axis=0), c.max(axis=0)

    def collisions(self, x, y, z, r=TOOL_R, ignore=(), cup_ignore=(), first=False, pad=0.0):
        """[(moving part, scene part)] touching at this pose (pad: grow the cup by this much)."""
        parts = self.pose_meshes(x, y, z, r)
        if parts is None:
            return None
        if not hasattr(self, "_scene_box"):
            self._scene_box = {n: (m.bounds[0], m.bounds[1]) for n, m in self.scene.items()}
        hits = []
        for pname, (mesh, tf) in parts.items():
            lo, hi = self._aabb(mesh, tf)
            if pname == "cup":
                g = fcl.Cylinder(mesh.extents[0] / 2 + pad, mesh.extents[2])
                lo, hi = lo - pad, hi + pad
            else:
                g = self._arm_bvh[pname]
            obj = None
            for sname, (slo, shi) in self._scene_box.items():
                if sname in ignore or (pname == "cup" and sname in cup_ignore):
                    continue
                if (lo > shi).any() or (hi < slo).any():
                    continue
                obj = obj or fcl.CollisionObject(g, fcl.Transform(tf[:3, :3], tf[:3, 3]))
                if fcl.collide(obj, self._scene_obj[sname], fcl.CollisionRequest(), fcl.CollisionResult()):
                    hits.append((pname, sname))
                    if first:
                        return hits
        return hits


use_lab(os.environ.get("SIM_LAB", HERE.parent / "lab2"))
