# MG400: the square at the end of the arm (for the XIAO camera mount)

Author: Dennel04 (with the tutor). Taken on 2026-10-04 from the robot's CAD
model, **not yet checked with calipers**.

## Where the model comes from

- The course's official table file: `3d-print/lab2/reference/MG 400 rakis.f3z`
  (from the course root). Inside, the robot assembly `mg400-solidworks_asm` is
  an XREF (imported from SolidWorks, apparently from the manufacturer).
- Uploaded to Fusion: project `3d-printing` -> folder `reference`
  (`MG 400 rakis` and `mg400-solidworks_asm`). The course file was not changed.
- `f3z` doesn't import through `importManager`, only `DataFolder.uploadFile`
  (as the API documentation says).

## Dimensions (part `2206058300-1`, the cover around the J4 motor)

| What | Value |
|---|---|
| Cross-section | 44 x 44 mm, J4 axis in the centre |
| Side face height | ~76 mm, chamfer on top to ~81 mm |
| Bottom of the square -> bottom of the J4 flange | ~13 mm (the flange is below the square) |
| Outer face (away from the robot) | flat, ~40 x 76 mm, no holes |
| Side faces (both) | 2 holes Ø2.7 mm, 24 mm apart, symmetric about J4, 2.5 mm above the bottom edge |
| Face towards the robot | Ø16 hole ~66 mm above the bottom (cable/connector?) |

The square **does not rotate with J4**: the motor housing is fixed, the shaft
and flange rotate. Checked on the real robot (Denys) and matches the CAD.

## Open questions

- Check everything with calipers on our robot.
- The Ø2.7 holes are most likely the cover's own screws. Can longer screws go
  through them to hold our part: ask the instructor.
- Distance from the bottom of the square to the suction cup tip (depends on
  the existing holder): measure.

## Mount v1 (2026-10-04): `3d-printing / xiao-square-mount-v1`

Robot inserted as XREF: J4 axis = Z axis, bottom of the square = z 0, robot = +X.
- U-clamp around 3 faces (outer + sides); on the robot side the lips `lip`
  reach behind the face strips (the arm there is ±17.5 mm, the square ±22).
  Snaps on from the side; doesn't rotate because the square isn't round.
- Height: holes for the cover's M2.5 screws (`scr_pitch` 24, `scr_z` 2.5);
  `skirt` 3 mm below the square so there is material under the hole.
- XIAO tray: the board slides along rails with `blip` 0.8 mm lips towards +Y
  to the stop, lens down, USB-C open towards +Y. Stiffening rib.
- Interference with the robot and the XIAO: 0. Volume 12.1 cm³ (~15 g solid PLA).
- All 8 sketches fully constrained, 24 User Parameters.

Added the same day:
- **A mistake found by Denys:** the hole cut first went through only one wall
  (the symmetric "through all" cut one side). Fixed with two "through all"
  extents -> 4 holes, 2 on each side. Lesson: after building, check the
  geometry (how many holes, where), not just Interference.
- **Cover screws (measured):** total length with head 6.3 mm, mushroom head
  Ø4.62 mm. Counterbore `cb_d` = 4.62 + 0.6 mm, `cb_floor` 1 mm under the
  head. Reasoning: thread in the plate ≈ 6.3 - head height - cover wall ~1.5.
  The clamp reduces it by `cb_floor`. For the final version, a screw **1 mm
  longer than stock** (M2.5 pan head) -> goes into the plate exactly as deep as
  the stock one, can't bottom out. Head height still to measure.
- **Cable:** an arm from the tray above the plug (`tab_z0` 2 mm, to clear the
  plug body), a cable clip behind the plug (snaps in from below, `open_k`
  0.75), a zip-tie bridge on the +Y side wall (slot 4 x 1.6 mm). This is
  "strain relief": hold the cable right behind the connector so a pull goes
  into the housing, not the USB-C. `plug_l` 18 and `cable_d` 4: **measure
  your cable**.
- 14 sketches, all fully constrained; Interference 0; volume 13.1 cm³.

Not done: keeping the board from sliding out towards +Y (the cable clip holds
it partly), lead-in chamfers on the lips, camera tilt, check with the suction
cup holder (not in the model).

## Related

- The instructor allowed putting the XIAO camera on this square, not only on
  the suction cup holder as the assignment text says.
- Plus: the cable doesn't twist when J4 turns. To think about: the glass in
  the frame rotates with J4; can the square see the point under the suction
  cup, and in Lab 3 the syringe tip.
- Webcam above the table: `lab2-webcam-mount.md`.
