# Lab 2, part 5: mounting the webcam above the table

Author: Dennel04 (with the tutor). Decision of 2026-10-04 (lesson with the
tutor). Numbers are from the datasheet, **not yet checked with calipers**.

## Camera

Verbatim AWC-03, code 49580 ([datasheet](https://cdn-reichelt.de/documents/datenblatt/E910/VERBATIM_49580_DB-EN.pdf)):

- envelope 106 x 55 x 42.5 mm (LxWxH; which number is which axis: to check), 129 g
- 120° field of view **diagonal**, frame 3840 x 2160 (16:9)
- autofocus from 15 cm
- monitor stand with a hinge: 360° rotation, 120° tilt
- 1/4" tripod thread (standard 1/4"-20 UNC)
- USB-A cable, 1.5 m

No ready CAD model from Verbatim or on GrabCAD/Printables/Thingiverse
(searched 2026-10-04) -> we model it ourselves: an envelope block + what we
attach to.

## Decision

1. **Keep the stand**, don't take the camera apart: it's lab property, the
   latches break, nothing to gain.
2. **A metal 1/4"-20 UNC tripod screw holds it**, from below through the top
   plate of the post into the stand's thread. Metal in the factory thread, not
   a printed thread in PLA. The lab has no such screw -> a line in `docs/bom.md`.
3. **Repeatability comes from the pocket, not the screw.** A pocket on the
   plate exactly the shape of the stand's foot; the screw only clamps. The
   assignment: *"kuju, mis lubab ainult ühte asendit, mitte hõõrdumine"*
   (a shape that allows only one position, not friction). Pocket clearance
   from the Lab 1 numbers (this is the "lõtk ja kust see tuli" item in grading).
4. **A stop locks the hinge.** Find the angle by holding the camera above the
   table by hand; then a printed wedge stop the camera head rests on.
5. **Post in a corner Gridfinity cell (G-5 / G+5)**, base over several cells,
   triangular post or with ribs: *"Jäikus tuleb kujust, mitte täitest"*
   (stiffness comes from shape, not infill). Taller than the printer bed ->
   print in parts; the joint must not become the weakest and loosest spot;
   layer direction by the Lab 1 break number.

## Measure before modelling

| What | Why |
|---|---|
| Stand foot: L x W x thickness, shape | The pocket |
| Thread position on the foot (from the edges) | The screw hole |
| Thread depth | Screw length, not bottoming out |
| Lens centre: height above the foot and forward offset at the chosen angle | Post height, frame calculation |
| Highest point of the MG400 arm (station, ruler) | Camera and post above it |

## Why not otherwise

- **Remove the stand**: risk of breaking it, we lose the hinge, need our own fit.
- **Screw only**: the camera turns around the screw, the angle drifts.
- **Table edge**: an option in the assignment, but Gridfinity already gives
  "the same place every time" without a new standard.

## Model in Fusion

`3d-printing / lab2-cameras-reference`: components `XIAO_ESP32S3_Sense`
(STEP from Seeed) and `Verbatim_AWC03_49580` (envelope block, parameters
`webcam_L/W/H`, `webcam_fov_diag`, `webcam_offset`).
