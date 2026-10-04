# PrusaSlicer pipeline (`prusa.py`)

Author: Dennel04 (with the tutor), 2026-10-04. Shared for the team on 2026-10-04.

Lets you (or the tutor) slice, check, see and ship a print the way the team
does in the lab: Prusa CORE One, HF0.4 nozzle, `0.20mm SPEED`, Prusament PLA.
Needs PrusaSlicer 2.9 in `C:\Program Files\Prusa3D\PrusaSlicer` (or set
`PRUSA_SLICER_DIR`) and Python with Pillow. Run from the `fusion-tutor`
folder.

| Command | What it does |
|---|---|
| `python shared/tools/prusa/prusa.py slice people/<me>/models/<part>-vN.stl --supports buildplate --style organic --rotate-x 180` | `.bgcode` named like the team's files (`<part>_0.4n_0.2mm_PLA_COREONE_45m.bgcode`), `<part>-sliced.3mf` **with the print settings inside**, a report (time, grams, support layers, first layer) and a preview PNG. Options: `--set perimeters=3`, `--set ironing=on`, `--out DIR`, `--usb` |
| `... check <file.gcode>` | Report from a text G-code |
| `... render <file.gcode>` | PNG: iso, front, side, first layer; supports in green |
| `... screen [--title "G-code Viewer"]` | Screenshot of the PrusaSlicer / G-code Viewer window (the tutor sees what you see) |
| `... open <file>` | Opens in PrusaSlicer (G-code Viewer for .gcode/.bgcode) |
| `... usb <file>` | Copies to the PRUSA USB stick, checks sha256 |
| `... profile <old.bgcode/.gcode/.3mf/.ini> [--name X]` | Saves the full config of a past print as `profiles/X.ini`; `slice --profile X` uses it |

`profiles/team-coreone-hf04.ini` is the full config of the team's print
`Lab2_Glass2_Input_Holder_0.4n_0.2mm_PLA_COREONE_47m.bgcode` (2026-10-04).
Support settings are set per slice with `--supports/--style`.

Text twins of the G-code, previews and screenshots go to
`%LOCALAPPDATA%\fusion-tutor\prusa\`, not into git.

Before printing, look at the preview (or the G-code Viewer): supports where
the part overhangs, nothing stuck inside small holes you'll have to clean.

Pitfalls found while building it: `../../knowledge/prusaslicer-pipeline.md`.
