"""Real robot in the hub process (real_robot.py + mg400/driver.py) against a fake MG400 on localhost, no arm needed.
Run: ../../sim/.venv/Scripts/python -m unittest -v test_real_robot"""
import sys
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from fake_mg400 import FakeMG400, wait_for  # noqa: E402
from real_robot import RealRobot  # noqa: E402


class RealRobotTest(unittest.TestCase):
    def setUp(self):
        self.fake = FakeMG400()
        self.r = RealRobot(ip="127.0.0.1", z_floor=-20.0, speed_ratio=25,
                           command_timeout=0.5, ports=self.fake.ports, settings_port=self.fake.settings_port)

    def tearDown(self):
        self.r.call("/disconnect")
        self.fake.close()

    def ready(self):
        self.assertTrue(self.r.call("/connect")["ok"])
        self.assertTrue(wait_for(lambda: self.r.call("/status")["feedback_ok"]))
        self.assertTrue(self.r.call("/enable")["ok"])
        self.assertTrue(self.r.call("/status")["servo_active"])

    def hold(self, axis, sign, secs):
        end = time.monotonic() + secs
        while time.monotonic() < end:
            self.assertTrue(self.r.call("/jog_hold", {"axis": axis, "dir": sign})["ok"])
            time.sleep(0.1)

    def test_not_connected(self):
        self.assertFalse(self.r.call("/move", {"x": 300, "y": 0, "z": 0})["ok"])
        self.assertFalse(self.r.call("/status")["connected"])

    def test_move_is_clamped_to_the_floor(self):
        self.ready()
        reply = self.r.call("/move", {"x": 320, "y": 0, "z": -300})
        self.assertEqual(reply["clamped"]["z"], -20.0)
        self.assertTrue(wait_for(lambda: abs(self.fake.pose[2] + 20.0) < 0.01, timeout=5))

    def test_held_jog_cruises_and_brakes(self):
        self.ready()
        x0 = self.fake.pose[0]
        self.fake.servo_points.clear()
        self.hold("x", 1, 1.2)
        pts = self.fake.servo_points
        steps = [b[0] - a[0] for a, b in zip(pts, pts[1:])]
        self.assertGreater(min(steps[len(steps) // 2:]), 0)       # never stops while held
        self.assertTrue(self.r.call("/jog_hold", {"dir": 0})["ok"])
        self.assertTrue(wait_for(lambda: self.r.call("/status")["target"] == list(self.fake.pose), timeout=3))
        self.assertGreater(self.fake.pose[0], x0 + 20)

    def test_held_jog_stops_at_the_floor(self):
        self.ready()
        self.hold("z", -1, 1.0)
        self.r.call("/jog_hold", {"dir": 0})
        time.sleep(0.5)
        self.assertGreaterEqual(min(p[2] for p in self.fake.servo_points), -20.0 - 1e-6)

    def test_pump_and_speed(self):
        self.ready()
        self.assertTrue(self.r.call("/pump", {"mode": "suck"})["ok"])
        self.assertFalse(self.r.call("/pump", {"mode": "vent"})["ok"])
        self.assertTrue(self.r.call("/speed", {"ratio": 5})["ok"])
        self.assertEqual(self.r.call("/status")["speed_ratio"], 5)


if __name__ == "__main__":
    unittest.main()
