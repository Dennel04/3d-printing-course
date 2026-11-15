"""Work zone calibration: rectangle fit from four corners, text direction, the Lab 1 calibration it writes.
Run: ../../sim/.venv/Scripts/python -m unittest -v test_workspace"""
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

HUB = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HUB))
from workspace import Workspace, derive  # noqa: E402

LAB1_SRC = HUB.parents[2] / "smart-solutions-course" / "smart-solutions" / "lab1" / "src"

# an A4 landscape sheet (297 x 210) turned 10 degrees; sheet frame: x along the text line, y = letter up
A = math.radians(10)
UX, UY = (math.cos(A), math.sin(A)), (-math.sin(A), math.cos(A))


def at(x, y, z=-60.0, r=-160.0):
    return [220 + x * UX[0] + y * UY[0], -150 + x * UX[1] + y * UY[1], z, r]


BL, BR, TR, TL = at(0, 0), at(297, 0), at(297, 210), at(0, 210)   # reader's bottom-left ... top-left
PEN = at(150, 100, -111.35)


def sheet(d):
    return d["paper"]


class DeriveTest(unittest.TestCase):
    def assertSheet(self, d, origin, edge, w=297, h=210):
        p = sheet(d)
        self.assertAlmostEqual(p["corner_x"], origin[0], delta=0.1)
        self.assertAlmostEqual(p["corner_y"], origin[1], delta=0.1)
        self.assertAlmostEqual(p["edge_x"], edge[0], delta=0.1)
        self.assertAlmostEqual(p["edge_y"], edge[1], delta=0.1)
        self.assertAlmostEqual(p["width_mm"], w, delta=0.1)
        self.assertAlmostEqual(p["height_mm"], h, delta=0.1)

    def test_bottom_line_taught_first(self):
        self.assertSheet(derive([BL, BR, TR, TL], PEN), BL, BR)

    def test_top_line_taught_first_puts_origin_at_bottom_left(self):
        # Point 1 -> 2 along the top edge: same text direction, the sheet lies below the line
        self.assertSheet(derive([TL, TR, BR, BL], PEN), BL, BR)

    def test_points_3_and_4_in_any_order_and_diagonal_point_2(self):
        self.assertSheet(derive([BL, BR, TL, TR], PEN), BL, BR)
        self.assertSheet(derive([BL, TR, BR, TL], PEN), BL, BR)   # diagonal 2nd: the 3rd point gives the line

    def test_corners_taught_by_eye_fit_inside(self):
        rough = [at(-6, 4), at(300, -5), at(293, 214), at(3, 207)]
        d = derive(rough, PEN)
        self.assertLess(sheet(d)["width_mm"], 297)
        self.assertLess(d["corner_err_mm"], 15)

    def test_pen_height_and_r(self):
        d = derive([BL, BR, TR, TL], PEN)
        self.assertEqual(d["pose"], {"r": -160.0, "pen_down_z": -111.85, "pen_up_z": -101.85})

    def test_refuses(self):
        with self.assertRaisesRegex(ValueError, "off the fitted"):
            derive([BL, BR, at(360, 260), TL], PEN)
        with self.assertRaisesRegex(ValueError, "four"):
            derive([BL, None, TR, TL], PEN)
        with self.assertRaisesRegex(ValueError, "Pen height"):
            derive([BL, BR, TR, TL], None)


class WorkspaceTest(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.lab1 = self.dir / "robot_calibration_pen.json"
        self.ws = Workspace(self.dir / "workspace.json", self.lab1)

    def teach(self, points=(BL, BR, TR, TL)):
        for n, p in enumerate(points, 1):
            self.ws.set_point(n, p, "real")
        self.ws.set_pen(PEN, "real")
        self.ws.save()

    def test_only_from_the_real_arm(self):
        with self.assertRaisesRegex(ValueError, "Real"):
            self.ws.set_point(1, BL, "sim")
        with self.assertRaisesRegex(ValueError, "Real"):
            self.ws.set_pen(PEN, "sim")

    def test_save_persists_and_writes_lab1(self):
        self.teach()
        again = Workspace(self.dir / "workspace.json", self.lab1)
        self.assertAlmostEqual(again.saved["paper"]["width_mm"], 297.0, delta=0.1)
        doc = json.loads(self.lab1.read_text(encoding="utf-8"))
        self.assertEqual(doc["pose"]["pen_down_z"], -111.85)
        self.assertEqual(doc["paper"]["margin_mm"], 10.0)

    @unittest.skipUnless(LAB1_SRC.is_dir(), "smart-solutions-course not cloned next to this repo")
    def test_lab1_maps_sheet_corners_back_and_letters_point_up(self):
        self.teach((TL, TR, BR, BL))
        sys.path[:0] = [str(LAB1_SRC.parent), str(LAB1_SRC)]
        from src.robot_calibration import load_robot_calibration
        from src.paper import PaperFrame
        pc = load_robot_calibration(self.lab1).paper
        frame = PaperFrame(pc.corner_x, pc.corner_y, pc.edge_x, pc.edge_y, pc.width_mm, pc.height_mm)
        for (sx, sy), p in zip([(0, 0), (297, 0), (297, 210), (0, 210)], (BL, BR, TR, TL)):
            x, y = frame.to_robot(sx, sy)
            self.assertAlmostEqual(x, p[0], delta=0.3)
            self.assertAlmostEqual(y, p[1], delta=0.3)


if __name__ == "__main__":
    unittest.main()
