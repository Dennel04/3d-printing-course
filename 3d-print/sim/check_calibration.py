"""check_calibration.py — in which cells does the four-corner method work with the calibration bin?

For each candidate cell the bin is put there, the cup goes to the four inner corners (centre +- 8 mm,
the cup then just reaches both walls of the 37 mm pocket) at 3 mm above the bin floor, R 33.
A cell passes when the joints allow that Z and nothing but the cup touches anything.
"""
import argparse

import mg400_kin as kin
import twin

CELLS = ["B-2", "B-3", "C-2", "C-1", "D-2", "E+3", "E-3", "F-2", "F-3", "G-1"]
FLOOR_ABOVE_FOOT = 7.0      # cal_floor
FOOT_Z = 2.289              # foot bottom when seated (1 x 1 wedges on the chamfers)
REACH = 8.0                 # cup centre offset towards each corner


def main():
    ap = argparse.ArgumentParser()
    twin.add_lab_arg(ap)
    twin.use_lab(ap.parse_args().lab)
    for cell in CELLS:
        T = twin.Twin(calibration_at=cell, layout={"holders": []})
        tip = FOOT_Z + FLOOR_ABOVE_FOOT + 3.0
        Z = T.robot_z_for_tip(tip)
        x0, y0 = twin.flange_for_cup(cell)
        worst = []
        for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            x, y = x0 + sx * REACH, y0 + sy * REACH
            ok, why, _ = kin.check(x, y, Z)
            if not ok:
                worst.append(f"corner {sx:+d}{sy:+d}: {why}")
                continue
            hits = [h for h in T.collisions(x, y, Z) if not (h[0] == "cup" and h[1] == "calibration")]
            if hits:
                worst.append(f"corner {sx:+d}{sy:+d}: {hits[0][0]} touches {hits[0][1]}")
        print(f"{cell:4} robot Z {Z:7.1f}  {'OK' if not worst else 'NO  ' + '; '.join(worst[:2])}")


if __name__ == "__main__":
    main()
