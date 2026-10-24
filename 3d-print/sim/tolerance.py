"""tolerance.py — how large a calibration error the glass cycle survives: every holder is shifted by the
same error (robot frame), 8 directions, 1..7 mm, one glass; first failure per direction.
Writes <lab>/docs/sim_tolerance.txt. Run: .venv/Scripts/python tolerance.py [--lab ../lab2]"""
import argparse
import math

import dry_run


def fails(rep):
    return [l.strip() for l in rep if "COLLISION" in l or "WRONG PLACE" in l or "not fully on the glass" in l or "!!" in l]


def main():
    ap = argparse.ArgumentParser()
    dry_run.twin.add_lab_arg(ap)
    dry_run.twin.use_lab(ap.parse_args().lab)
    dry_run.load_cycle()
    lines = []
    for k in range(8):
        a = math.radians(45 * k)
        first = None
        for e in range(1, 8):
            r = dry_run.Run([1])
            for role in ("input", "workstation", "output"):
                dry_run.cycle.holder(r.lay, role)["teach"].update(dx=round(e * math.cos(a), 2), dy=round(e * math.sin(a), 2))
            f = fails(r.run())
            if f:
                first = (e, f[0])
                break
        lines.append(f"direction {45 * k:3d} deg: " + (f"fails at {first[0]} mm: {first[1]}" if first else "ok up to 7 mm"))
        print(lines[-1])
    (dry_run.twin.LAB / "docs" / "sim_tolerance.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
