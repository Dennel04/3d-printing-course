# PrusaSlicer from the command line: pitfalls and workarounds

Author: Dennel04 (with the tutor), 2026-10-04. Verified on PrusaSlicer 2.9.6,
Prusa CORE One HF0.4. The tool: `../tools/prusa/prusa.py`.

| Symptom | Cause | Fix |
|---|---|---|
| A 3MF exported with `prusa-slicer-console --export-3mf` opens in the GUI **without supports** | The CLI writes a model-only 3MF (no `Metadata/Slic3r_PE.config`); the GUI slices it with whatever presets are selected | Add `Metadata/Slic3r_PE.config` (`; key = value` lines) to the zip; `prusa.py slice` does it. Check: the 3MF re-sliced by the CLI gives the same grams/time |
| `--printer-profile/--print-profile/--material-profile`: "Configuration wasn't found. Check your 'datadir' value." | These need a configured PrusaSlicer data dir; this PC had none (`%APPDATA%\PrusaSlicer` missing) | Take the full config from a past team print and `--load` it (`prusa.py profile <file>`) |
| You can't read settings or check supports in a `.bgcode` | Binary G-code is compressed (MeatPack/heatshrink) | The settings are in the "slicer metadata" block (deflate): `prusa.py profile` reads it. For checks, slice the same options to a text `.gcode`: same grams and time = the same slice |
| `--support-material-buildplate-only 1` fails or is ignored | Bool options are flags | `--support-material-buildplate-only` / `--no-support-material-buildplate-only` |
| The report/preview shows the part far bigger than it is | The start G-code purge line counts as extrusion (`;TYPE:Custom`) | Skip `Custom` when measuring |

Seen on the XIAO square mount v2 (organic, build plate only): trees also grow
into the Ø2.9 mm side screw holes. Small holes bridge fine; block them with a
Support blocker in the GUI, or drill them clean after printing.

There is no API to drive the PrusaSlicer GUI. The MCP servers found on
2026-10-04 (Noosbai/PrusaMCP, Casys-AI/mcp-prusaslicer, OpenGalatea,
gioelemo/prusa-mcp via Prusa Connect) all wrap the same CLI; none was
installed.
