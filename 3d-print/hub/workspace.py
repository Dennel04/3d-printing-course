"""Work zone calibration: the operator jogs the pen over the four corners of the sheet and presses
Point 1-4 (in the air is fine), lowers the pen onto the paper and presses Pen height, then Done.
The zone is kept in workspace.json and written into the Lab 1 drawing calibration (paper corner/edge,
size, pen down/up Z, R), which smart-solutions lab1/src/paper.py reads.

Point 1 -> Point 2 is the direction of a line of text (the reader's left -> right); Point 3 and 4 are
the other two corners in any order. Corners taught by eye are never an exact rectangle, so a rectangle
is fitted: the four points are ordered round their centre, the common angle of the four edges sets the
sides, the shorter of each pair of opposite sides keeps letters on the paper, and it is centred on the
points. The Lab 1 sheet frame has Y (letter up) 90 degrees counter-clockwise from X; the sheet origin
is the corner from which the sheet lies on that side, so letters are never mirrored.
"""
import json
import math
import time
from pathlib import Path

MIN_SIDE_MM = 50.0          # Lab 1 refuses a baseline shorter than this
MAX_CORNER_ERR_MM = 15.0    # a taught point further than this from the fitted rectangle is a mis-click
PEN_PRESS_MM = 0.5          # pen down = the taught touch height minus this
PEN_LIFT_MM = 10.0          # pen up = pen down plus this
MARGIN_MM = 10.0


def _ccw_order(points):
    """Indices of the four points counter-clockwise round their centre, starting at point 0."""
    cx = sum(p[0] for p in points) / 4
    cy = sum(p[1] for p in points) / 4
    order = sorted(range(4), key=lambda i: math.atan2(points[i][1] - cy, points[i][0] - cx))
    k = order.index(0)
    return order[k:] + order[:k], (cx, cy)


def fit(points):
    """Best rectangle through four corner points -> (order, fitted corners in that order, worst error).
    order: point indices counter-clockwise starting at point 1; fitted[i] belongs to points[order[i]]."""
    order, (cx, cy) = _ccw_order(points)
    q = [points[i] for i in order]
    edges = [(q[(i + 1) % 4][0] - q[i][0], q[(i + 1) % 4][1] - q[i][1]) for i in range(4)]
    # common edge direction modulo 90 degrees: average the edge angles times four (length weighted)
    s4 = sum(math.sin(4 * math.atan2(ey, ex)) * math.hypot(ex, ey) for ex, ey in edges)
    c4 = sum(math.cos(4 * math.atan2(ey, ex)) * math.hypot(ex, ey) for ex, ey in edges)
    base = math.atan2(s4, c4) / 4
    a0 = math.atan2(edges[0][1], edges[0][0])
    ang = min((base + k * math.pi / 2 for k in range(4)),
              key=lambda a: abs(math.atan2(math.sin(a - a0), math.cos(a - a0))))
    u, v = (math.cos(ang), math.sin(ang)), (-math.sin(ang), math.cos(ang))
    dot = lambda e, w: abs(e[0] * w[0] + e[1] * w[1])
    w = min(dot(edges[0], u), dot(edges[2], u))
    h = min(dot(edges[1], v), dot(edges[3], v))
    c0 = (cx - w / 2 * u[0] - h / 2 * v[0], cy - w / 2 * u[1] - h / 2 * v[1])
    fitted = [c0, (c0[0] + w * u[0], c0[1] + w * u[1]),
              (c0[0] + w * u[0] + h * v[0], c0[1] + w * u[1] + h * v[1]), (c0[0] + h * v[0], c0[1] + h * v[1])]
    err = max(math.hypot(a[0] - b[0], a[1] - b[1]) for a, b in zip(q, fitted))
    return order, fitted, err


def derive(points, pen):
    """points: Point 1..4 as [x, y, z, r]; pen: [x, y, z, r] with the pen on the paper."""
    if len(points) != 4 or any(p is None for p in points):
        raise ValueError("teach all four corner points first")
    if pen is None:
        raise ValueError("lower the pen onto the paper and press Pen height")
    order, f, err = fit(points)
    if err > MAX_CORNER_ERR_MM:
        raise ValueError(f"a point is {err:.0f} mm off the fitted sheet rectangle (max {MAX_CORNER_ERR_MM:.0f}); "
                         "re-teach the corner that is off")
    # text direction: Point 1 -> Point 2; if Point 2 is the diagonal corner, Point 1 -> the corner taught next
    target = next(i for i in (1, 2, 3) if order.index(i) in (1, 3))
    if order.index(target) == 1:        # the sheet lies counter-clockwise of the line: origin is Point 1
        origin, edge, far = f[0], f[1], f[3]
    else:                               # clockwise: origin is the corner next to Point 1 on the other side
        origin, edge, far = f[1], f[2], f[0]
    width = math.dist(origin, edge)
    height = math.dist(origin, far)
    if min(width, height) < MIN_SIDE_MM:
        raise ValueError(f"sheet {width:.0f} x {height:.0f} mm: each side must be at least {MIN_SIDE_MM:.0f} mm")
    pen_down = round(pen[2] - PEN_PRESS_MM, 2)
    return {
        "paper": {
            "corner_x": round(origin[0], 2), "corner_y": round(origin[1], 2),
            "edge_x": round(edge[0], 2), "edge_y": round(edge[1], 2),
            "width_mm": round(width, 1), "height_mm": round(height, 1),
            "size": "A4", "orientation": "landscape" if width >= height else "portrait",
            "margin_mm": MARGIN_MM,
        },
        "pose": {"r": round(pen[3], 2), "pen_down_z": pen_down, "pen_up_z": round(pen_down + PEN_LIFT_MM, 2)},
        "corner_err_mm": round(err, 1),
    }


class Workspace:
    """Points in memory while teaching; Done derives, saves workspace.json and the Lab 1 calibration."""

    def __init__(self, store: Path, lab1_calibration: Path | None, lab1_template: Path | None = None):
        self.store, self.lab1, self.template = store, lab1_calibration, lab1_template
        saved = json.loads(store.read_text(encoding="utf-8")) if store.is_file() else {}
        self.saved = saved or None
        # points taught but not yet Done survive a hub restart
        self.draft = store.with_name(store.stem + "_draft.json")
        draft = json.loads(self.draft.read_text(encoding="utf-8")) if self.draft.is_file() else {}
        self.points = draft.get("points") or [None] * 4
        self.pen = draft.get("pen")

    def _keep(self):
        self.draft.write_text(json.dumps({"points": self.points, "pen": self.pen}) + "\n", encoding="utf-8")

    def state(self):
        return {"points": self.points, "pen": self.pen, "saved": self.saved,
                "lab1_file": str(self.lab1) if self.lab1 else None}

    def set_point(self, n, pose, mode):
        if mode != "real":
            raise ValueError("switch to Real: work zone points are taken from the real arm")
        if n not in (1, 2, 3, 4):
            raise ValueError("point: 1, 2, 3 or 4")
        if not pose or len(pose) < 4:
            raise ValueError("no robot pose yet")
        self.points[n - 1] = [round(float(v), 2) for v in pose[:4]]
        self._keep()

    def set_pen(self, pose, mode):
        if mode != "real":
            raise ValueError("switch to Real: the pen height is taken from the real arm")
        if not pose or len(pose) < 4:
            raise ValueError("no robot pose yet")
        self.pen = [round(float(v), 2) for v in pose[:4]]
        self._keep()

    def clear(self):
        self.points = [None] * 4
        self.pen = None
        self._keep()

    def save(self):
        derived = derive(self.points, self.pen)
        record = {"points": self.points, "pen": self.pen, "saved_at": time.strftime("%Y-%m-%dT%H:%M:%S"), **derived}
        self.store.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        self.saved = record
        if self.lab1:
            self._write_lab1(derived)
        return record

    def _write_lab1(self, derived):
        src = self.lab1 if self.lab1.is_file() else self.template
        doc = json.loads(src.read_text(encoding="utf-8")) if src and src.is_file() else {
            "version": 1, "workspace": {"origin_x": None, "origin_y": None, "width": None, "height": None},
            "motion": {"speed_percent": 10}}
        doc["pose"] = dict(derived["pose"])
        doc["paper"] = dict(derived["paper"])
        doc["paper_comment"] = (f"Taught in the MG400 Station Hub (Jog tab, Work zone) "
                                f"{time.strftime('%d.%m.%y %H:%M')}: four sheet corners, rectangle fitted; pen height taught on the paper.")
        for key in [k for k in doc if k.startswith("paper_previous") or k == "air_test_comment"]:
            del doc[key]
        self.lab1.parent.mkdir(parents=True, exist_ok=True)
        self.lab1.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
