# Tool camera auto-calibration and look-before-descent — design

Date: 2026-10-25 · Owner: Dennel04 (Denys) with Claude · Lab: 3D printing Lab 2 (MG400 glass cell)

## Problem

The pocket centre drifts. One holder is hit well, the next one is off, and after a few cycles the same
holder is off again. The digital twin cannot give real robot accuracy, and a wrong descent can push a
holder or trigger the MG400 collision stop (~12 N).

Facts behind this (repo docs): the MG400 repeats to ±0.05 mm, the table to ±0.3–0.5 mm, Gridfinity
returns a holder "within a few tenths of a mm". The current grid map is a rigid 2D fit with residuals up
to 1.9 mm (goal < 0.5 mm, `lab2/docs/measurements.md`). Known drift suspects: cup X/Y depends on R (all
points are taught at R 33; DobotStudio changes R), holder play in the grid, the glass sliding on the cup,
touch judged by eye. The assignment asks for "two cameras, two jobs: one sees everything, one sees
precisely" (`lab2/assignment-EST.md:259`).

## Decisions (Denys, 25.10.2026)

- Correct with the camera **before every descent** of the cycle (pick and place), not only on a button.
- Find the pocket by **comparing with a reference frame** taught once per holder (no markers, no
  trained model). AI is for analysing the logs later, not for measuring.
- The table webcam (global "holders in place, path free") is a later, separate stage.

## Success criteria

1. The cycle never descends when the measured offset is larger than `max_correction_mm` (3 mm) or the
   match is poor or there is no frame: it stops with a message and the saved frame.
2. On the real robot, the pocket offset seen after correction is ≤ 0.5 mm in every step of 5 refit
   rounds × 4 glasses (`docs/refit_test.csv`).
3. A drift test answers where the drift comes from (R, holder, cycle count) with numbers in a CSV.
4. Unit tests: a known synthetic shift/rotation is recovered within 0.1 px; Jacobian and the decision
   thresholds are covered; the hub tests keep passing.

## Architecture

```
hub (UI: Picker → Test → Vision panel)
  └─ slot_picker.py  Sequencer: new actions look / vision_cal / drift; routes /api/vision/*
        ├─ cycle.py   inserts ("look", role, glass, action) before each descent
        ├─ vision.py  pure functions, no robot, no serial: register, Jacobian, decide
        └─ ToolCamera (existing, COM5) — fresh() frames
```

### vision.py (new, `lab2/slot-picker/vision.py`)

- `register(ref, img) -> Match(dx_px, dy_px, angle_deg, score)`: grayscale, CLAHE, Hanning window,
  `cv2.phaseCorrelate` for the coarse shift, then `cv2.findTransformECC` (MOTION_EUCLIDEAN) seeded with
  it for sub-pixel shift and the small angle. `score` = ECC correlation (0..1).
- `solve_jacobian(samples) -> J` (2×2, mm per px): least squares over (robot dX, dY) vs (image dx, dy)
  pairs; returns the residual in mm.
- `to_mm(J, dx_px, dy_px) -> (dx_mm, dy_mm)` in robot X/Y.
- `decide(dx_mm, dy_mm, score, cfg) -> ("ok" | "correct" | "stop", reason)`.
- Reads/writes `vision/calibration.json` and reference images; no hardware.

### Configuration (`layout.json`, new block `vision`)

```json
"vision": { "enabled": true, "look_z": -110.0, "settle_s": 0.4,
            "min_score": 0.6, "deadband_mm": 0.15, "confirm_mm": 0.5, "max_correction_mm": 3.0,
            "cal_step_mm": 2.0 }
```

`look_z` must be reachable over every holder and above every holder top (holder tops ≈ Z −140;
travel Z −90). Default −110 = the picker's hover height.

### Camera calibration (button "Calibrate camera")

Over the calibration box (F+2), at `look_z`, R 33: frames at (0,0), (±cal_step, 0), (0, ±cal_step).
Each frame is registered to the centre frame → five (robot shift, image shift) pairs → J. Accept only if
the residual < 0.1 mm and every score ≥ `min_score`; save `vision/calibration.json` (J, look_z, R,
date, residual). Without a calibration the look step stops the cycle ("calibrate the camera first").

### References (taught once)

After `teach_point` saves a holder's pick_z / place_z, the robot goes up to `look_z` over the same X/Y and
stores `vision/refs/<holder>-<pick|place>.jpg` + `.json` (pose, R, look_z, date). One reference per
holder and action serves all cells of that holder. A "Retake reference" button redoes it at the taught
point. Input references show a glass in the pocket; place references show an empty pocket.

### Look step in the cycle

For every pick and place: travel → over the slot at `look_z` → wait `settle_s` → `camera.fresh()` (up to
3 tries; COM5 short reads happen) → register against the holder's reference → mm offset (`J`) →
`decide`:

- `|d| ≤ deadband`: descend as planned.
- `deadband < |d| ≤ max_correction` and `score ≥ min_score`: shift the slot X/Y by −d for this descent
  and the climb; if `|d| > confirm_mm`, look once more at the corrected point and require
  `|d2| ≤ confirm_mm`.
- otherwise: stop the sequence (no descent), state error "vision: <reason>", frame saved to `frames/`.

Every look is a row in `lab2/docs/vision_log.csv`: time, run, glass, role, holder, cell, R, x, y,
dx_mm, dy_mm, angle, score, decision. In Simulation (no camera) the step is skipped and logged
"vision: sim". With `vision.enabled` false the cycle runs as today.

### Drift test (button)

N visits (default 10) to one chosen slot, each from travel height, look only, no correction and no
descent; optional R jitter (33 ± 2°) to test the R hypothesis. Rows to `lab2/docs/vision_drift.csv`.
The panel shows mean/max offset and the offset against R and visit number.

### UI (hub Picker → Test → Vision)

Calibration state (date, residual) + Calibrate camera; per role: reference thumbnail, date, Retake;
"Correct with the camera" switch (= `vision.enabled`); last look: frame with the reference crosshair,
dx/dy mm, score, decision; Drift test with slot selector and N. Motion buttons obey the hub motion
switch (routes added to `MOTION_PATHS`).

## Error handling

- No frame after retries, low score, offset over the limit, missing calibration or reference: stop
  before the descent, never guess.
- Camera errors outside the look step keep today's behaviour (a missing snapshot does not stop the cycle).
- Calibration is tied to `look_z` and R; changing either asks for a new calibration.

## Testing

- `slot-picker/tests/test_vision.py`: synthetic images (rendered pocket edges + noise) shifted by known
  sub-pixel amounts and rotated ≤ 2°: register error < 0.1 px; Jacobian from known pairs; decide
  thresholds; poor-match image (blank) gives low score → stop.
- Sequencer test with a fake camera returning shifted images: the descent target is corrected; over the
  limit the sequence stops before any downward move.
- Hub tests keep passing (27 now).
- Real robot, at 5–10 %: calibrate, take references, drift test, then refit rounds 2–5 with the look step.

## Out of scope (later)

Table webcam global check; ArUco markers; AI analysis of the logs; Z/touch detection by camera.

## Dependency

`opencv-python-headless` added to `3d-print/sim/requirements.txt` (the hub's venv) and installed there.
