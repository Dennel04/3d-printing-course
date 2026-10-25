"""refit_sim.py — refit test rounds in the twin: before each round every holder lands somewhere inside its foot
play (random, independent per holder), then the planned full cycle runs 4 glasses with the same taught points.
Writes <lab>/docs/sim_refit.txt. Run: .venv/Scripts/python refit_sim.py [--play 1.0] [--rounds 2,3,4,5]"""
import argparse
import random

import dry_run
from tolerance import fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--play", type=float, default=1.0, help="max holder shift per axis, mm (old feet ~1, standard 0.24)")
    ap.add_argument("--rounds", default="2,3,4,5")
    ap.add_argument("--seed", type=int, default=29)
    dry_run.twin.add_lab_arg(ap)
    a = ap.parse_args()
    dry_run.twin.use_lab(a.lab)
    dry_run.load_cycle()
    rnd = random.Random(a.seed)
    lines = [f"holder play +-{a.play} mm per axis, seed {a.seed}"]
    ok_total = n_total = 0
    for rnd_no in (int(x) for x in a.rounds.split(",")):
        r = dry_run.Run([1, 2, 3, 4], full=True)
        shifts = {}
        for role in ("input", "workstation", "output"):
            # holder moved by s = the taught point is off by -s relative to the holder
            s = (round(rnd.uniform(-a.play, a.play), 2), round(rnd.uniform(-a.play, a.play), 2))
            shifts[role] = s
            dry_run.cycle.holder(r.lay, role).setdefault("teach", {}).update(dx=-s[0], dy=-s[1])
        rep = r.run()
        bad = {g: [l for l in fails(rep) if l.startswith(f"glass {g}:")] for g in (1, 2, 3, 4)}
        ok = sum(1 for g in bad if not bad[g])
        ok_total += ok
        n_total += 4
        lines.append(f"round {rnd_no}: shifts " + ", ".join(f"{k} {v[0]:+.2f}/{v[1]:+.2f}" for k, v in shifts.items())
                     + f" -> {ok}/4 ok")
        for g, f in bad.items():
            if f:
                lines.append(f"   glass {g}: {f[0]}")
        print(lines[-1] if not any(bad.values()) else "\n".join(lines[-1 - sum(1 for f in bad.values() if f):]))
    lines.append(f"total {ok_total}/{n_total}")
    print(lines[-1])
    (dry_run.twin.LAB / "docs" / "sim_refit.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
