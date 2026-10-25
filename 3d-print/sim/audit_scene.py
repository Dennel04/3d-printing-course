"""audit_scene.py — are the objects of the twin where they physically are? One table of numbers:
  holders   placed by the rule (base on the grid top / old feet on the beams) vs dropped like gravity onto
            the rig (twin._settle): the change must be ~0, and what each one rests on
  glasses   bottom of every glass vs the pocket floor under it (gap > 0.2 mm = floating, < 0 = sunk)
  cup       every taught "down to" point: first touch vs the taught Z = how far the robot goes below the
            twin's first touch (pad lip ~1-2 mm, the rest = twin height error) (from viewer/data/anim.json, made by export_viewer.py)
Run: .venv/Scripts/python audit_scene.py [--lab ../lab2]
"""
import argparse
import json

import numpy as np

import dry_run
import twin


def below(T, x, y, z, skip):
    best = (-1e9, "nothing")
    for n, m in T.scene.items():
        if n in skip:
            continue
        loc, _, _ = m.ray.intersects_location([[x, y, z]], [[0, 0, -1.0]])
        if len(loc) and loc[:, 2].max() > best[0]:
            best = (float(loc[:, 2].max()), n)
    return best


def main():
    ap = argparse.ArgumentParser()
    twin.add_lab_arg(ap)
    twin.use_lab(ap.parse_args().lab)
    dry_run.load_cycle()
    run = dry_run.Run([1, 2, 3, 4])
    T = run.T
    print("HOLDERS (rule height vs dropped onto the rig)")
    for name, (z0, dz) in T.seat.items():
        m = T.scene.get("holder:" + name) or T.scene.get("calibration")
        lo = m.bounds[0]
        c = m.bounds.mean(axis=0)
        z, on = below(T, c[0], c[1], lo[2] + 0.05, {"holder:" + name})
        verdict = "ok" if abs(dz) < 0.3 else ("was FLOATING" if dz < 0 else "was SUNK into the rig")
        print(f"  {name:24s} bottom z {lo[2]:7.2f}  change {dz:+.2f} mm  {verdict}")
    print("GLASSES (bottom vs the surface under the centre)")
    for n, m in T.scene.items():
        if not n.startswith("glass"):
            continue
        c = m.bounds.mean(axis=0)
        z, on = below(T, c[0], c[1], m.bounds[0][2] + 0.01, {n})
        gap = m.bounds[0][2] - z
        print(f"  {n:10s} on {on:28s} gap {gap:+.2f} mm  {'ok' if abs(gap) < 0.2 else 'CHECK'}")
    if "AtomS3" in T.scene:
        b, a = T.scene["battery"], T.scene["AtomS3"]
        z, on = below(T, *b.bounds.mean(axis=0)[:2], b.bounds[0][2] + 0.01, {"battery", "AtomS3"})
        print(f"  battery    on {on:28s} gap {b.bounds[0][2] - z:+.2f} mm; AtomS3 top z {a.bounds[1][2]:.2f}")
    data = twin.HERE / "viewer" / "data" / "anim.json"
    print("CUP (taught Z below the twin's first touch)")
    if data.exists():
        for line in json.loads(data.read_text(encoding="utf-8")).get("press", []):
            if line.startswith("glass 1:"):
                print("  " + line[9:])
    else:
        print("  run export_viewer.py first")


if __name__ == "__main__":
    main()
