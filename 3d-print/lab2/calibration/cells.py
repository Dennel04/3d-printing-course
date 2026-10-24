"""cells.py CELL [CELL ...] — Gridfinity cell centre in MG400 robot X/Y (mm).

Model formula from assignment-EST.md ("Ruutude nimed"), model rotated 180° about Z,
then the rigid fit (rotation + shift) to the measured cell centres below.
Valid only at R = 33° (the suction cup is off the J4 axis). Example: python cells.py D-2 E+3
"""
import math
import re
import sys

R_DEG = 33.0
# 24.10.26, R 33: measured centre (robot X, Y) per cell; see docs/measurements.md
# C-2 added 24.10.26 evening: calibration bin v3, four inner corners in touch (docs/calibration_c-2_v3.csv)
MEASURED = {
    "G-1": (420.50, 27.55),
    "E+3": (340.498, -101.1465),
    "D-2": (297.201, 67.479),
    "C-2": (253.805, 68.46),
}


def model(cell):
    m = re.fullmatch(r"([A-G])([+-][1-5])", cell.upper())
    if not m:
        raise ValueError(f"bad cell name {cell!r}, expected e.g. B-2 or E+3")
    letter, n = "ABCDEFG".index(m[1]), int(m[2])
    x = -139.5 - 42 * letter
    y = 42 * n - 21 if n > 0 else 42 * n + 21
    return -x, -y


def fit(measured=MEASURED):
    pairs = [(xy, model(c)) for c, xy in measured.items()]
    k = len(pairs)
    mr = [sum(r[i] for r, _ in pairs) / k for i in (0, 1)]
    mm = [sum(m[i] for _, m in pairs) / k for i in (0, 1)]
    sxx = sum((m[0] - mm[0]) * (r[0] - mr[0]) + (m[1] - mm[1]) * (r[1] - mr[1]) for r, m in pairs)
    sxy = sum((m[0] - mm[0]) * (r[1] - mr[1]) - (m[1] - mm[1]) * (r[0] - mr[0]) for r, m in pairs)
    th = math.atan2(sxy, sxx)
    c, s = math.cos(th), math.sin(th)

    def robot(cell):
        x, y = model(cell)
        dx, dy = x - mm[0], y - mm[1]
        return mr[0] + c * dx - s * dy, mr[1] + s * dx + c * dy

    return math.degrees(th), robot


if __name__ == "__main__":
    rot, robot = fit()
    print(f"rotation {rot:+.2f} deg, R {R_DEG}")
    for cell in sys.argv[1:] or MEASURED:
        x, y = robot(cell)
        print(f"{cell.upper():4} X {x:7.2f}  Y {y:8.2f}")
