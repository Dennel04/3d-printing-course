"""cycle.py — the Lab 2 glass cycle: input -> workstation -> output, as a list of robot actions.

Each role (input, workstation, output) is a holder from layout.json. A holder keeps its taught
points in "teach": dx/dy (offset of the pocket from the cell centre, mm) and pick_z / place_z.
The offset belongs to the holder, not to the cell, so a holder moved to another cell reuses it:
that is the 42 mm question of the refit test.

Glass n (1-based) is taken from the n-th input cell and put into the n-th output cell; the
workstation always uses layout["cycle"]["workstation_cell"].
"""
import csv
from pathlib import Path

ROLES = ("input", "workstation", "output")
# Which taught Z values each role needs.
NEEDS = {"input": ("pick_z",), "workstation": ("place_z", "pick_z"), "output": ("place_z",)}
FIELDS = ("picked_from_input", "placed_at_workstation", "picked_from_workstation", "placed_at_output")
REFIT_HEADER = ["round", "glass_id", *FIELDS, "notes"]


def holder(layout, role):
    name = layout["cycle"]["roles"].get(role)
    for h in layout["holders"]:
        if h["name"] == name:
            return h
    raise ValueError(f"{role}: no holder {name!r} in the layout (choose one in Test)")


def teach(h):
    return {"dx": 0.0, "dy": 0.0, "pick_z": None, "place_z": None, **h.get("teach", {})}


def slot_cell(layout, role, glass):
    h = holder(layout, role)
    if role == "workstation":
        cell = layout["cycle"].get("workstation_cell") or h["cells"][0]
        if cell not in h["cells"]:
            raise ValueError(f"workstation cell {cell} is not in {h['name']}")
        return cell
    if glass > len(h["cells"]):
        raise ValueError(f"{h['name']} has {len(h['cells'])} cells, no place for glass {glass}")
    return h["cells"][glass - 1]


def slot_xy(layout, role, glass, by_name):
    """Robot X/Y of the pocket: cell centre from the calibration + the holder's taught offset."""
    t = teach(holder(layout, role))
    c = by_name[slot_cell(layout, role, glass)]
    if c["blocked"]:
        raise ValueError(f"{c['name']}: {c['blocked']}")
    return c["x"] + t["dx"], c["y"] + t["dy"]


def check_ready(layout, by_name):
    """Raise ValueError naming the first thing missing before a run."""
    for role in ROLES:
        h = holder(layout, role)
        t = teach(h)
        for z in NEEDS[role]:
            if t[z] is None:
                raise ValueError(f"{role} ({h['name']}): {z} not taught")
    for g in range(1, 5):
        for role in ROLES:
            slot_xy(layout, role, g, by_name)


def plan_glass(layout, glass, by_name):
    """Actions for one glass. ("move", label, x, y, z) | ("pump", mode) | ("wait", s) |
    ("mark", glass, field) | ("snap", label)."""
    cyc = layout["cycle"]
    travel, approach = cyc["travel_z"], cyc["approach_mm"]

    def pick(x, y, z, what):
        return [("move", f"glass {glass}: above {what}", x, y, travel),
                ("move", f"glass {glass}: approach {what}", x, y, z + approach),
                ("move", f"glass {glass}: down to {what}", x, y, z),
                ("pump", "suck"), ("wait", cyc["suck_dwell_s"]),
                ("move", f"glass {glass}: lift from {what}", x, y, travel)]

    def place(x, y, z, what):
        return [("move", f"glass {glass}: above {what}", x, y, travel),
                ("move", f"glass {glass}: approach {what}", x, y, z + approach),
                ("move", f"glass {glass}: down to {what}", x, y, z),
                ("pump", "blow"), ("wait", cyc["blow_s"]), ("pump", "off"),
                ("move", f"glass {glass}: lift from {what}", x, y, travel)]

    ti, tw, to = (teach(holder(layout, r)) for r in ROLES)
    xi, yi = slot_xy(layout, "input", glass, by_name)
    xw, yw = slot_xy(layout, "workstation", glass, by_name)
    xo, yo = slot_xy(layout, "output", glass, by_name)
    return [*pick(xi, yi, ti["pick_z"], "input"), ("mark", glass, FIELDS[0]),
            *place(xw, yw, tw["place_z"], "workstation"), ("mark", glass, FIELDS[1]),
            ("snap", f"r-g{glass}-workstation"),
            *pick(xw, yw, tw["pick_z"], "workstation"), ("mark", glass, FIELDS[2]),
            *place(xo, yo, to["place_z"], "output"), ("mark", glass, FIELDS[3]),
            ("snap", f"r-g{glass}-output")]


def save_refit(path: Path, rnd: int, rows):
    """Write one round into refit_test.csv. An empty template row (round, glass) is filled in;
    a row that already has results is kept and the new result is appended below it."""
    with path.open(newline="", encoding="utf-8") as f:
        table = list(csv.DictReader(f))
    for row in rows:
        new = {"round": str(rnd), "glass_id": str(row["glass"]),
               **{k: "yes" if row.get(k) else "no" for k in FIELDS}, "notes": row.get("notes", "").strip()}
        empty = next((r for r in table if r["round"] == new["round"] and r["glass_id"] == new["glass_id"]
                      and not any(r[k] for k in FIELDS)), None)
        if empty is not None:
            empty.update(new)
        else:
            last = max((i for i, r in enumerate(table) if r["round"] == new["round"]), default=len(table) - 1)
            table.insert(last + 1, new)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=REFIT_HEADER, lineterminator="\n")
        w.writeheader()
        w.writerows(table)
