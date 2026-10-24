"""reach_map.py — for every grid cell: how low the suction cup can go over the cell centre (R 33),
and what stops it first: a joint limit (as mg400-base enforces it) or a collision of the cup, the
XIAO mount or the arm with the rig, a holder, the webcam post or the table.

Writes <lab>/docs/sim_reach.csv and <lab>/docs/photos/sim-reach-map.png.
Run: .venv/Scripts/python reach_map.py [--lab ../lab2]
"""
import argparse
import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import mg400_kin as kin  # noqa: E402
import twin  # noqa: E402

ROWS, COLS = "ABCDEFG", [5, 4, 3, 2, 1, -1, -2, -3, -4, -5]   # slot picker operator view
Z_TOP, Z_BOTTOM = 0.0, -230.0


def name(r, c):
    return f"{r}{c:+d}"


def lowest(pred, hi=Z_TOP, lo=Z_BOTTOM, tol=0.1):
    """Lowest Z in [lo, hi] where pred(Z) still holds, pred true at hi and false below some point."""
    if not pred(hi):
        return None
    if pred(lo):
        return lo
    while hi - lo > tol:
        mid = (hi + lo) / 2
        hi, lo = (mid, lo) if pred(mid) else (hi, mid)
    return hi


def main():
    ap = argparse.ArgumentParser()
    twin.add_lab_arg(ap)
    twin.use_lab(ap.parse_args().lab)
    T = twin.Twin()
    holder_at = {c: h["name"] for h in T.layout["holders"] for c in h["cells"]}
    rows = []
    for r in ROWS:
        for c in COLS:
            cell = name(r, c)
            x, y = twin.flange_for_cup(cell)
            zj = lowest(lambda Z: kin.check(x, y, Z)[0])
            why_j = kin.check(x, y, (zj if zj is not None else Z_TOP) - 0.2)[1]
            zc = lowest(lambda Z: kin.inverse(x, y, Z) is not None and not T.collisions(x, y, Z, first=True))
            hit = T.collisions(x, y, (zc if zc is not None else Z_TOP) - 0.3) if zc is not None else [("-", "already at Z 0")]
            hit = hit[0] if hit else ("?", "?")
            if zj is None:
                zmin, stop = None, f"unreachable: {why_j}"
            elif zc is None or zj > zc:
                zmin, stop = zj, f"joint: {why_j}"
            else:
                zmin, stop = zc, f"touch: {hit[0]} -> {hit[1]}"
            tip = T.cup_tip_z(zmin) - twin.GRID_TOP if zmin is not None else None
            rows.append(dict(cell=cell, holder=holder_at.get(cell, ""), flange_x=round(x, 2), flange_y=round(y, 2),
                             z_min=None if zmin is None else round(zmin, 1),
                             tip_above_grid=None if tip is None else round(tip, 1),
                             z_joint=None if zj is None else round(zj, 1),
                             z_touch=None if zc is None else round(zc, 1), stops=stop))
            print(f"{cell:4} {holder_at.get(cell, ''):22} Zmin {rows[-1]['z_min']!s:>7}  tip {rows[-1]['tip_above_grid']!s:>6} mm above grid  {stop}")
    out = twin.LAB / "docs" / "sim_reach.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    plot(rows, T)
    print("written", out)


def plot(rows, T):
    by = {r["cell"]: r for r in rows}
    fig, ax = plt.subplots(figsize=(13, 9.5))
    cmap = plt.get_cmap("RdYlGn_r")
    for i, r in enumerate(ROWS):
        for j, c in enumerate(COLS):
            d = by[name(r, c)]
            tip = d["tip_above_grid"]
            joint = d["stops"].startswith(("joint", "unreachable"))
            col = (0.75, 0.75, 0.75) if tip is None else cmap(min(1.0, max(0.0, (tip + 5) / 40)))
            ax.add_patch(plt.Rectangle((j, -i), 1, 1, facecolor=col, edgecolor="white", lw=2))
            hold = d["holder"].split(" (")[0]
            txt = f"{name(r, c)}\n" + ("—" if tip is None else f"{tip:+.1f} mm\nZ {d['z_min']}") + \
                  ("\nJOINT" if joint else "") + (f"\n{hold}" if hold else "")
            ax.text(j + 0.5, -i + 0.5, txt, ha="center", va="center", fontsize=7.5,
                    fontweight="bold" if joint else "normal")
    ax.set_xlim(0, 10)
    ax.set_ylim(-6, 1.35)
    ax.add_patch(plt.Rectangle((3.5, 1.05), 3, 0.3, facecolor="#333"))
    ax.text(5, 1.2, "MG400", color="white", ha="center", va="center", fontsize=9)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Lowest suction-cup tip over each cell centre, mm above the grid top (R 33)\n"
                 "JOINT = stopped by a joint limit (mg400-base margin 2 deg), otherwise the first touch; "
                 f"cup length {T.cup_len} mm, layout.json holders", fontsize=10)
    fig.tight_layout()
    fig.savefig(twin.LAB / "docs" / "photos" / "sim-reach-map.png", dpi=110)


if __name__ == "__main__":
    main()
