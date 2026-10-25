# Gridfinity socket of the MG 400 rakis grid, and the foot that fits it

Author: Dennel04 (with Claude), 2026-10-24. Measured on the instructor's
`MG 400 rakis` model (cloud, Fusion), body `rakis_E_long / grid_pos_0`, cell
A+1, by reading the exact B-Rep faces (not by sampling points). The same
numbers come out in every cell (they are pattern copies).

## Why this note exists

Our first holders had a **plain square foot** (35.98 mm, then 35.78 mm with
R1.5). It only matched the narrowest point of the socket. Above it the
socket is 37.68 mm and then opens to 42 mm, so the holder had **0.95 mm
play per side** and nothing centred it: Denys saw the 2 x 2 output box
`valjundhoidik-v1` move back and forth and not seat fully.
Lesson: a fit is a **profile**, not one width. Measure the whole profile.

## The socket (Z from the grid top, which is z = 7.279 mm in the rig model)

| Step | Z (rig model) | Depth | Half-width from cell centre | Corner radius | Face types |
|---|---|---|---|---|---|
| Top chamfer 45 deg | 7.279 -> 5.129 | 2.15 | 20.99 -> 18.84 | 3.99 -> 1.84 | 4 planes + 4 cones |
| Vertical | 5.129 -> 3.329 | 1.80 | 18.84 (37.68 wide) | 1.84 | 4 planes + 4 cylinders |
| Lower chamfer 45 deg | 3.329 -> 2.629 | 0.70 | 18.84 -> 18.14 | 1.84 -> 1.14 | 4 planes + 4 cones |
| Throat of the rig (open below) | 2.629 -> -16.72 | | 18.14 (36.28 wide) | 1.14 | planes + cylinders |

- All corner arcs (cones and cylinders) share **one centre: 17.000 mm from
  the cell centre** in X and Y. That is why the radius grows exactly with
  the half-width: radius = half-width - 17.
- 0.7 + 1.8 + 2.15 = 4.65 mm: the standard Gridfinity **baseplate** profile.
  (A standard **bin** foot is 0.8 + 1.8 + 2.15 = 4.75 mm, 41.5 mm at the top.)
- Neighbouring sockets meet in a sharp ridge at the grid top (42 mm pitch,
  20.99 + 21.01). A multi-cell holder rests on these ridges; a 1 x 1 does not
  touch them (see below).

## The foot that fits: the STANDARD one

The assignment says: standard Gridfinity foot, 4.75 mm, "take it from a
generator or library, don't draw it by eye". The generator
gridfinity-rebuilt-openscad (kennetek, `src/core/standard.scad`,
`BASE_PROFILE`, based on gridfinity.xyz/specification):

| Step (from the bottom) | Height | Width | Corner radius |
|---|---|---|---|
| 45 deg | 0.8 | 35.6 -> 37.2 | 0.8 -> 1.6 |
| vertical | 1.8 | 37.2 | 1.6 |
| 45 deg | 2.15 | 37.2 -> 41.5 | 1.6 -> 3.75 |

Bin top 41.5 x 41.5 (42 n - 0.5), outer radius 3.75, base height 7 mm
(`BASE_HEIGHT`), height unit 7 mm, magnets 6 x 2 mm optional.

**How it sits in our socket** (checked in Fusion against the real grid,
24.10): bin and socket profiles are parallel with a 0.24 mm horizontal gap.
- **1 x 1**: the bin sinks until its chamfers touch the socket chamfers
  (foot bottom 0.34 below the 0.7 chamfer start, top of the bin body 0.24 mm
  below the grid top; the 41.5 body fits inside the 42 cell opening).
  Lateral play is zero: moving it 0.05 mm sideways already interferes.
  Nominal: the top of a 21 mm bin is 16.0 mm above the grid surface. A
  printed bin that stands higher means the foot prints wider.
- **2 x 2 and bigger**: the flat bottom between the feet lands on the bin's
  own inner ridges first (z 7.28), the chamfers keep 0.24 mm play. That is
  the standard behaviour ("foot top ~0.1 mm above the grid" in the
  assignment).

Our first attempt "socket offset by 0.25" (0.7 bottom chamfer, 4.65 high)
was **not** the standard: a 1 x 1 would rest on the ridges with 0.25 play.
Don't use it.

In Fusion: three extrudes downward from the bin bottom plane + 4.75, the
45 deg steps with **taper -45 deg** (negative = shrinks along the extrude),
sketch = rounded rectangle with corner radius `half - 17`. Script:
`../tools/fusion-geometry/gf_std_foot.py` (`add_std_feet(component,
centres_mm, foot_top_z_mm)`, parameter `gf_fit_adjust` = extra inward offset
per side, 0 = standard). Calibration bin: `../tools/fusion-geometry/gf_calibration_bin.py`
(3d-print/lab2/gridfinity-calibration).

Checks after building:
- Interference with the grid = none; `measureMinimumDistance` = contact;
- move it 0.05 mm sideways / down: interference appears (1 x 1 is wedged);
- probe half-widths with `pointContainment` at several Z.

## Open (physical)

- Calibration bin printed 24.10: seats in the grid, no rock, used for the C-2 calibration.
- Why `valjundhoidik-v1` does not go in to the end is not proven yet: check
  support remnants under the base, elephant foot on the first layer (caliper:
  the foot bottom should be ~35.8 mm), where it stops.

## Converting an existing holder to the standard foot (done 25.10 on glass-input-holder-v3)

Author: Dennel04 (with Claude), 2026-10-25.
1. Suppress the old foot features (sketches, extrudes, fillets, chamfers): don't delete, keep the history.
2. Outer size: `42 * n - 0.5` only. The team's first holders also subtracted `grid_clearance` (83.2 instead of 83.5).
3. **Check that the outer sketch is tied to the origin.** v2's rectangle had only two dimensions,
   so a larger size grew to one side (-41.9 .. +41.6). Fix: construction diagonal, midpoint
   constraint to the sketch origin. Measure extents with `pointContainment`, not
   `boundingBox` (it is loose).
4. `add_std_feet(root, [(+-21, +-21)], foot_top_z)` with `foot_top_z` = the body bottom; check
   half-widths 17.85 / 18.60 / 20.70 near the bottom / middle / top.
5. 2 x 2 sliced feet down without supports: the 45 deg chamfers print by themselves.
