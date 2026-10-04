# Progress

Updated at the end of every lesson. Statuses: `—` not started, `🟡` tried /
with hints, `🟢` do it confidently on my own. Next to it: date last checked.

## Already done in the course (before the tutor)

- Lab 1: tolerance test cube (`cube-tolerance-v1.f3d`), pen holder for the
  MG400 v1 -> v2 (`Pastaka_kinnitus_robotile.f3d`, `Pastaka_sisu_rakis.f3d`).
  Who modelled what themselves: to clarify at the first lesson.
- Lab 1 tolerance result: 0.4 mm fits freely, 0.2 mm jams.

## Skill map

### Sketch
| Skill | Status | Date |
|---|---|---|
| Line / Rectangle / Circle / Arc | — | |
| Sketch Dimension | — | |
| Constraints (coincident, horizontal, tangent, symmetry, equal) | — | |
| Fully constrained sketch (all black) | — | |
| Construction lines, Project / Include | — | |
| Offset, Trim, Mirror, Pattern in a sketch | — | |

### Parameters and design intent
| Skill | Status | Date |
|---|---|---|
| User Parameters (Change Parameters) | — | |
| Dimensions through parameter names and formulas | — | |
| The model rebuilds without errors when a parameter changes | — | |

### Bodies and features
| Skill | Status | Date |
|---|---|---|
| Extrude (New Body / Join / Cut, To Object) | — | |
| Revolve | — | |
| Hole / Thread | — | |
| Fillet / Chamfer | — | |
| Shell | — | |
| Pattern / Mirror (3D) | — | |
| Combine | — | |
| Sweep / Loft | — | |

### Assembly
| Skill | Status | Date |
|---|---|---|
| Components instead of bodies | — | |
| Joints / As-built Joints | — | |
| Interference / Section Analysis | — | |

### For printing
| Skill | Status | Date |
|---|---|---|
| Fit tolerances in the model (per-side vs total clearance) | — | |
| Export STL / 3MF | — | |
| Designing without supports (angles, bridges) | — | |
## Recurring mistakes

_(none has recurred yet; candidates to check in the next lessons)_

- 2026-10-04: confusion about "what rotates": thought the clamp on the square
  "would spin", missing that a non-round fit itself stops rotation. Check on
  a fit/locking task.

## Strengths (observations)

- 2026-10-04: checks the model against reality: found on his own that the
  screw holes were only on one wall; measured the screw himself and asked
  about the thread length.

## Fixed

_(mistakes that no longer recur move here)_

## Current goals

0. **(2026-10-04, the main thing now)** Lab 2 cameras. The XIAO holder on the
   MG400 square v1 was made by the tutor (`xiao-square-mount-v1`, write-up in
   `shared/knowledge/mg400-end-square.md`). Next, the student himself:
   measurements -> Change Parameters -> v2 improvements (board latch, clip
   arm ribs, lip chamfers) **with his own hands**, the tutor gives hints.
   Webcam: decision in `shared/knowledge/lab2-webcam-mount.md`, measurements
   needed. Skills in the map above did not change on 04.10: the student did
   not do the modelling.
1. First lesson: diagnosis: look at my Lab 1 models together with the tutor
   and honestly mark the statuses above. _(not done: on 04.10 we worked on the
   Lab 2 cameras; do it when there is a first model of my own)_
2. Lab 2: model a parametric 1x1 Gridfinity holder in Fusion myself (compare
   with the OpenSCAD version `lab2/src/gridfinity-calibration-v2.scad`).
3. Lab 3 (issued 27.10): practise in advance what it will need: components vs
   bodies, Interference, a light "cone" body, a nut pocket, a syringe size
   parameter, a spring clamp using the Lab 1 numbers.
