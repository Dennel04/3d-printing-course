# Dennel04's tools

## `prusa.py`: PrusaSlicer pipeline (2026-10-04)

Lets the tutor slice, check, see and ship prints the way the student does.
Stdlib + Pillow. Run from `people/Dennel04/`.

| Command | What it does |
|---|---|
| `python tools/prusa.py profile <old.bgcode/.gcode/.3mf/.ini>` | Saves the full config of a past print as `tools/profiles/team-coreone-hf04.ini` (baseline: CORE One HF0.4, 0.20mm SPEED, Prusament PLA) |
| `python tools/prusa.py slice models/<part>-vN.stl --supports buildplate --style organic --rotate-x 180` | `.bgcode` named like the team's files, `<part>-sliced.3mf` **with settings inside**, a report (time, grams, support layers, first layer) and a preview PNG. `--set perimeters=3`, `--set ironing=on`, `--usb` |
| `python tools/prusa.py check <file.gcode>` | Report from a text G-code |
| `python tools/prusa.py render <file.gcode>` | PNG: iso, front, side, first layer; supports in green |
| `python tools/prusa.py screen [--title "G-code Viewer"]` | Screenshot of the PrusaSlicer / G-code Viewer window: the tutor sees what the student sees |
| `python tools/prusa.py open <file>` | Opens in PrusaSlicer (or G-code Viewer for .gcode/.bgcode) |
| `python tools/prusa.py usb <file>` | Copies to the PRUSA USB stick, checks sha256 |

Text twins of G-code, previews and screenshots go to
`%LOCALAPPDATA%\fusion-tutor\prusa\`, not into git.

Lessons that led to it:
- `prusa-slicer-console --export-3mf` writes a model-only 3MF: the GUI then
  slices it with its own presets (we saw "no supports"). The tool embeds
  `Metadata/Slic3r_PE.config`.
- `--printer-profile/--print-profile` need a configured `--datadir`; this PC
  has none, so the tool loads the full config from a past team print instead.
- `.bgcode` is compressed: checks run on a text G-code sliced with the same
  options (same grams and time = same slice).
- Bool options in the CLI are flags: `--support-material` /
  `--no-support-material`, not `=1/0`.
