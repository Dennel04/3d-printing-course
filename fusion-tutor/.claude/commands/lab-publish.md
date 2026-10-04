---
description: Put a finished part into the lab (3d-print/labN/), check it against the lab rules, commit it
argument-hint: [part / version, e.g. xiao-square-mount v2 -> lab2 camera-mounts]
---

The student wants a finished part in the lab: $ARGUMENTS
The lab is shared and graded, so do it the way the instructor asked, not
roughly. Talk in the student's language. Lab text (README entries) is
**Estonian**, like the rest of the lab README (`../AGENTS.md` "Conventions").

**Go only if all three hold**, otherwise say what is missing and stop:
1. The student asked for it in this conversation ("put it into the lab").
2. You know the part from this lesson or the student's memory
   (`people/<me>/models/`, `log/`, `progress.md`): which Fusion document and
   version, what changed and why, how it was printed, what is measured and
   what isn't.
3. The files are complete: a source, an STL and the PrusaSlicer 3MF (not
   Fusion's mesh 3MF) per printed version. Not printed yet: say so in the
   README; don't invent results.

Steps:
1. `python tools/sync.py pull`. Read in full: `../AGENTS.md`,
   `../3d-print/labN/assignment-EST.md` (the instructor's original;
   Lab 1: its `README.md`), `../3d-print/labN/README.md` (checklist,
   "CAD-failid"/file list, "Arenduspäevik"), and for Lab 2 also the docs
   `../AGENTS.md` names. Find the assignment's requirements and grading
   criteria ("Hindamiskriteeriumid") this part touches; quote them, don't
   paraphrase.
2. `python tools/lab.py check labN`: the state before. Problems that were
   there before you are reported to the student, not fixed silently.
3. Show the student the plan in one block: which files go where (with the
   new names), the README file-list line and the devlog entry, word for word.
   Wait for "yes".
4. Copy each file: `python tools/lab.py copy people/<me>/models/<file>
   labN/<part>/<src|stl|3mf>/<name>-vN.<ext>`. Names: `<name>-vN`, the same
   stem in all three folders; never over an existing file (a reprint is a new
   version).
5. Edit `README.md` with Edit (append; never rewrite others' text):
   - file list ("CAD-failid"): one line per version: paths, Fusion document,
     what it is, state of the physical fit (`TODO — waiting for physical test`
     until measured);
   - checklist: tick only what is really verified, with the date;
   - "Arenduspäevik" at the end, one entry for this session, in the format
     the existing entries use: `**DD.MM.YY — <login> (<name>) koos
     Claude'iga**`, then `Tegime`, `Mõõtmised ja tulemused koos ühikutega`
     (say which numbers are CAD/datasheet and which are caliper), `Otsused ja
     põhjendused` (instructor decisions with date), `Failid ja versioonid`,
     `Järgmiseks`. Never edit an older entry: a correction goes underneath.
6. `python tools/lab.py check labN` again: zero new problems. Then show the
   student `git -C .. diff --stat` and the README diff
   (`git -C .. diff -- 3d-print/labN/README.md`).
7. On their "yes": `python tools/lab.py commit labN "<what, in English>"`.
   It commits only `3d-print/labN/` and pushes. Report the commit hash.
8. Write in `people/<me>/models/README.md` (and the lesson log) that the
   version is in the lab, with the commit hash.

Each `lab.py copy|commit` and each README edit asks the student through a
permission prompt: that click is their approval, so never try another path
(shell cp, git) around it.
