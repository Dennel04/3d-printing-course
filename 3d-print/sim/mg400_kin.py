"""MG400 joint-space model, copied from our mg400-base fork (github.com/Dennel04/mg400-base, branch
lab-jog, commit 982ebf8, mg400/kinematics.py) so the twin uses exactly the numbers the robot server
uses to refuse targets. Links fitted to 6 real poses (GetAngle vs GetPose, rms 0.01 mm).

    radius = R0 + L1*sin(J2) + L2*cos(J3)      J2 from vertical, J3 below horizontal
    z      = Z0 + L1*cos(J2) - L2*sin(J3)      (robot Z of the flange point)
"""
import math

L1, L2, R0, Z0 = 174.2, 175.07, 109.49, -52.97
LIMITS = {"J1": (-160.0, 160.0), "J2": (-25.0, 85.0), "J3": (-25.0, 105.0),
          "parallelogram J3-J2": (-60.0, 60.0)}
MARGIN = 2.0   # mg400-base stops this far short of every limit


def forward(j1, j2, j3):
    a1, a2, a3 = (math.radians(v) for v in (j1, j2, j3))
    radius = R0 + L1 * math.sin(a2) + L2 * math.cos(a3)
    return radius * math.cos(a1), radius * math.sin(a1), Z0 + L1 * math.cos(a2) - L2 * math.sin(a3)


def inverse(x, y, z):
    """Flange (robot X, Y, Z) -> (J1, J2, J3) deg, elbow-up, or None if out of reach."""
    j1 = math.degrees(math.atan2(y, x))
    u, w = math.hypot(x, y) - R0, z - Z0
    d2 = u * u + w * w
    d = math.sqrt(d2)
    if d < 1e-6 or d > L1 + L2 or d < abs(L1 - L2):
        return None
    beta = math.acos(max(-1.0, min(1.0, (L1 * L1 + d2 - L2 * L2) / (2 * L1 * d))))
    a2 = math.atan2(u, w) - beta
    ex, ez = L1 * math.sin(a2), L1 * math.cos(a2)
    a3 = math.atan2(-(w - ez), u - ex)
    return j1, math.degrees(a2), math.degrees(a3)


def check(x, y, z, margin=MARGIN):
    """(ok, reason, joints): reason names the limit that would be hit."""
    j = inverse(x, y, z)
    if j is None:
        return False, "out of reach", None
    j1, j2, j3 = j
    for name, v in (("J1", j1), ("J2", j2), ("J3", j3), ("parallelogram J3-J2", j3 - j2)):
        lo, hi = LIMITS[name]
        if v < lo + margin:
            return False, f"{name} {v:.1f} deg at its low limit ({lo:g})", j
        if v > hi - margin:
            return False, f"{name} {v:.1f} deg at its high limit ({hi:g})", j
    return True, None, j
