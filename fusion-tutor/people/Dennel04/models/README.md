# Models: XIAO camera mount on the MG400 J4 square

Fusion project `3d-printing`. Robot as XREF, J4 axis = Z, bottom of the
square = z 0, robot = +X. Write-up of v1: `shared/knowledge/mg400-end-square.md`.

| Version | Fusion | Files here | Status |
|---|---|---|---|
| v1 | `xiao-square-mount-v1` | (none) | Made by the tutor 2026-10-04. Not printed |
| v2 | `xiao-square-mount-v2` | `xiao-square-mount-v2.f3d/.stl/.3mf`, `-sliced.3mf`, `_0.4n_0.2mm_PLA_COREONE.bgcode` | **On the printer 2026-10-04 (fit test)**. CORE One HF0.4, 0.20mm SPEED, Prusament PLA, organic supports on build plate, printed upside down (clamp rim on the bed), 45 min, 15.6 g |
| v3 | `xiao-square-mount-v3` | `xiao-square-mount-v3.f3d/.stl/.3mf` (not sliced) | **Next, after the v2 test.** Not printed |

## Into the lab: one source, STL and 3MF per print

Lab 2 asks for "lähtefailid, STL ja `.3mf` iga prindi kohta" and the README
checklist "Iga prindi lähtefail, STL ja 3MF on versioonitud". The student
copies them into `3d-print/lab2/camera-mounts/` (the tutor doesn't write there):

| Lab path | v2 (printed) | v3 (after slicing) |
|---|---|---|
| `src/xiao-square-mount-vN.f3d` | `xiao-square-mount-v2.f3d` | `xiao-square-mount-v3.f3d` |
| `stl/xiao-square-mount-vN.stl` | `xiao-square-mount-v2.stl` | `xiao-square-mount-v3.stl` |
| `3mf/xiao-square-mount-vN.3mf` | `xiao-square-mount-v2-sliced.3mf` (**rename**) | `xiao-square-mount-v3-sliced.3mf` (after `prusa.py slice`) |

`xiao-square-mount-vN.3mf` in this folder (without `-sliced`) is a mesh
export from Fusion, **not** the lab 3MF: the lab 3MF is the PrusaSlicer
project. The `.f3d` files (~3 MB) carry the robot (XREF) inside. The
`.bgcode` is for the printer only. v1 was never printed, so it needs no files
in the lab.

## v2: what changed from v1 (2026-10-04)

- Removed the zip-tie bridge (`ziptie_bridge`, `ziptie_slot`, params `br_*`,
  `zt_*`). Why: a tie needs a consumable and has to be cut to remove the cable.
- Added `cable_clip2` on the +Y clamp wall, axis along X (cable runs along
  the wall towards the robot), snaps in from outside. Same `cable_d`,
  `clip_t`, `clip_len`, `open_k` as clip 1; new `clip2_z` 10, `clip2_emb` 0.6.

## v2 test: what to check on the print

1. Square 44 mm: slides on with slight play, no force (`clr` 0.3 per side).
2. Cover screws: the stock 6.3 mm screw reaches the thread through the
   counterbore floor (`cb_floor` 1 mm); otherwise a screw 1 mm longer.
3. XIAO board: slides into the rails, doesn't rattle (`b_clr`, `pcb_clr`, `blip`).
4. Cable Ø: snaps into both clips and holds (`cable_d` 4, `open_k` 0.75).
5. Supports in the Ø2.9 screw holes: clean them (drill 2.9-3 mm by hand).
6. Write the results in the next lesson log; put the corrected numbers into
   Change Parameters of **v3**, not v2.

## v3: what changed from v2 (2026-10-04)

Problem (found by Dennel04): the camera module hangs on its flex under the
board, nothing holds it: it shakes and doesn't come back to the same spot
(Lab 2 part 4: "Kaamera on iga kord samas kohas ... kuju, mis lubab ainult
ühte asendit, mitte hõõrdumine").

- `camera_nest`: U pocket hanging from both rails, floor under the camera,
  side walls fix X; walls stay below `ledge_z` 7.8 so the Sense board, its
  B2B connector and the flex slide over them. Open towards +Y: the camera
  slides in together with the board.
- `camera_stop`: stop wall on the -Y side, `stopw_h` 3 (under the flex).
- `lens_window`: Ø `lens_d` 6.5 in the floor.
- Checked: sketches fully constrained; Interference 0 with XIAO and robot;
  board+camera pulled out along the rails 0-24 mm in 2 mm steps: no collision.
- New params (all from the STEP, **MEASURE**): `cam_w` 8, `cam_h` 5.8,
  `cam_z0` 14, `cam_y0` 2.9, `cam_dx` 0.6, `lens_d` 6.5; fit `cam_clr` 0.2,
  `floor_t` 1.2, `nest_t` 1.6.
- Open: nothing holds the camera from lifting (gravity holds it, lens down);
  no board latch yet; lowest point now z -15.4 (was -5.6): check against the
  suction cup tip; heat: if PLA softens near the module, print in PETG
  (Printables case authors report it).

Slicing: `python shared/tools/prusa/prusa.py slice people/Dennel04/models/xiao-square-mount-v3.stl --supports buildplate --style organic --rotate-x 180`.
