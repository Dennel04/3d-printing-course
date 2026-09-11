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
```

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
- **Nothing gets deleted.** A wrong measurement stays in the doc with its
  date; the correction goes underneath it, not over it.
- **Devlog entries** live inside each lab's `README.md` under
  "Arenduspäevik" — one entry per work session, appended (not edited later).
- Git tag per lab on submission, e.g. `3d-print-lab1`.

## Tools in play

- Fusion 360 (educational license) for the cube and tolerance parts.
- Any tool that exports STL for the pen holder (Fusion, Blender, ...).
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
- Prefer adding new versioned files over overwriting existing STL/3mf/source
  files.
- If asked to translate assignment text, translate faithfully; don't
  editorialize instructor requirements.
