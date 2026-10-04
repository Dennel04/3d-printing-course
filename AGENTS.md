# AGENTS.md — 3D Printing & CAD course repo

This repo belongs to a 3-student team working through the "Smart Solutions" /
3D Printing & CAD labs. One repo covers the whole course; each lab gets its
own folder under the matching subject prefix (e.g. `3d-print/lab1/`,
`3d-print/lab2/`, ...).

## What this course is building toward

By the end of the year, an MG400 robot arm assembles a sign: an AtomS3
(ESP32) with a polycarbonate screen glued on. Every part that mounts on the
robot or holds electronics is 3D printed by the team. Three subjects share
one team and one demo: **press a key on the AtomS3, the robot draws that
letter** — this course provides the printed mechanical parts (holder,
mounts), a separate programming course drives the robot, a separate
electronics course drives the display.

## Repo layout

```
3d-print/
  lab1/
    README.md          <- the lab assignment, copied here on day 1, filled in as work happens
    cube/               <- tolerance test print (5x5x5 cm cube, r2cm inner cylinder)
      src/              <- Fusion 360 (or other) source/design files
      stl/              <- exported STL per version
      3mf/              <- sliced PrusaSlicer project per version
    flex-piece/         <- flex/snap test print (bend/break point)
      src/  stl/  3mf/
    pen-holder/         <- the actual tool: spring-loaded pen holder for MG400
      src/  stl/  3mf/
  lab2/
    README.md           <- Lab 2 checklist, measured decisions, and devlog
    docs/               <- layout.md, refit_test.csv, bom.md, and photos
    src/                <- reusable parametric CAD prototypes, not yet print-verified
    input-holders/      <- final holders for AtomS3, glass, and battery
      src/  stl/  3mf/
    workstation-holder/ <- holder for the assembly step
      src/  stl/  3mf/
    output-holders/     <- good-part and reject locations
      src/  stl/  3mf/
    camera-mounts/      <- tool camera mount and overhead camera post
      src/  stl/  3mf/
    gripper-attachment/ <- MG400 gripper: flange boss, AtomS3R/battery fork, suction cup and syringe mounts
      src/  stl/  3mf/
  lab3/
    README.md           <- Lab 3 checklist, known inputs, file index, and devlog
    assignment-EST.md   <- original assignment text, unmodified
    docs/               <- tool_layout.md, tool_offsets.md, leak_test.csv,
                           cycle_test.csv, bom.md, photos/
    nut-pocket-test/    <- small block for nut pocket + print pause test
      src/  stl/  3mf/
    valve-mount/        <- 3/2 solenoid valve mount
      src/  stl/  3mf/
    tool/               <- combined tool: suction cup, syringe, UV lamp, camera
      src/  stl/  3mf/
    purge-cup-holder/   <- Gridfinity holder for the purge cup
      src/  stl/  3mf/
    nozzle-park/        <- dark, covered parking spot for the syringe nozzle
      src/  stl/  3mf/
fusion-tutor/            <- Claude Code tutor for learning Fusion (run `claude` inside it);
                           see fusion-tutor/README.md. Per-student memory in
                           fusion-tutor/people/<github-login>/, team material in shared/.
```

Each lab folder from Lab 2 on also keeps `assignment-EST.md`: the original
assignment text exactly as issued (never edited). The lab `README.md` holds
the team's working version.

Each later lab under `3d-print/labN/` should follow the same pattern:
`README.md` (assignment + filled-in answers/devlog) + one subfolder per
physical part, each with `src/` `stl/` `3mf/`.

## Conventions

- **Language:** assignments are issued in Estonian. `README.md` in each lab
  folder stays in Estonian (it's the official template with `KAARDISTA ISE`
  fill-in-the-blank sections) — the student adds Estonian or English notes
  inline. Team chat / dev notes can be in Russian or English; ask Claude to
  translate any Estonian instructions.
- **Versioning parts:** every reprint is a new version — new file, not an
  overwrite. Name iterations like `pen-holder-v1.f3d`, `pen-holder-v2.f3d`,
  and matching `pen-holder-v1.stl`, `pen-holder-v1.3mf`. Note in the README
  what changed and why for each version.
- **Lab 2 fit:** Lab 1 only bounded printer clearance to 0.2–0.4 mm. Treat
  that as a starting range, record whether a CAD value is per-side or total,
  and verify Gridfinity feet and part pockets with physical test prints.
- **Lab 2 CAD:** shared parametric OpenSCAD prototypes may live in `lab2/src/`.
  Once a design is assigned to a physical part and tested, keep its versioned
  source, STL, and 3MF together under that part's folder.
- **Nothing gets deleted.** A wrong measurement stays in the doc with its
  date; the correction goes underneath it, not over it.
- **Devlog entries** live inside each lab's `README.md` under
  "Arenduspäevik" — one entry per work session, appended (not edited later).
- Git tag per lab on submission, e.g. `3d-print-lab1`.

## Tools in play

- Fusion 360 (educational license) for the cube and tolerance parts.
- Any tool that exports STL for the pen holder (Fusion, Blender, ...).
- OpenSCAD for the Lab 2 parametric holder prototypes (install locally to render/export).
- PrusaSlicer for slicing, lab printers, PLA (later maybe PETG).
- MG400 robot arm + Python base package (from the instructor) for the demo.

## Safety notes (for anyone, human or agent, drafting instructions)

- Nozzle runs 200–230 °C — parts come off the bed with a spatula once it's
  cooled, never bare hands on the nozzle/bed.
- Hands stay off the table while the MG400 is powered on; first run of any
  new program goes slow with the e-stop in reach.
- Side cutters cut away from the face.

## For an AI agent picking up work here

- Check the current lab's `README.md` first — it has the live goals,
  checklist, and devlog; don't duplicate what's already answered there.
- For Lab 2, also read `3d-print/lab2/docs/MG 400 rakis.md`,
  `3d-print/lab2/docs/measurements.md`, and
  `3d-print/lab2/docs/test-procedure.md` before changing CAD, measurements,
  or test records.
- Prefer adding new versioned files over overwriting existing STL/3mf/source
  files.
- If asked to translate assignment text, translate faithfully; don't
  editorialize instructor requirements.
