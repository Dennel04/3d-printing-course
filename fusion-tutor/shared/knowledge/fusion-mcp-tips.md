# Fusion MCP and API: pitfalls and workarounds

Author: Dennel04 (with the tutor), 2026-10-04. Collected from problems hit
while the tutor worked through Fusion MCP, plus searching (Autodesk forums,
Autodesk MCP help).

## What got in the way, and why

| Symptom | Cause | Fix |
|---|---|---|
| Hook: "Cannot perform 'script' while a command dialog is open" | A command is active in Fusion: `ConstrainedOrbitCommand` (orbit), `FusionDeleteCommand` (an accidental Delete) | The student presses Esc. Check beforehand: `fusion_mcp_read` -> `activeCommand`. Idle = `SelectCommand`. Hook v2 closes navigation commands itself |
| The model keeps orbiting with the mouse and won't stop | Known Fusion bug (FUS-82525): releasing the orbit button over the browser tree leaves orbit active | Drag the ViewCube by a corner towards the screen centre (accepted answer on the Autodesk forum). Orbit with Shift+wheel, not the Orbit button on the bottom bar |
| Fusion doesn't answer even read-only calls, hook "timed out" | A modal dialog is open in Fusion; every API call waits until it is closed. On 2026-10-04 it was "save / don't save `_tutor-sandbox`", popping up when the tutor created a new document. The sandbox with unsaved changes sat in the background although `activeDocument` was empty | The student closes the dialog. At the start of a lesson look at **all** open documents (`fusion_mcp_read` -> `document`/`open`), not just the active one; save or close unsaved ones before creating new ones. Hook v2 pings first (8 s) instead of waiting 90 s, and refuses new documents while others are unsaved |
| Saving / the checkpoint hangs for a long time | The version is uploading to the cloud; per Autodesk help: antivirus/firewall/slow internet/large files | Don't make needless versions; insert large assemblies (the robot) by reference (XREF), not as a copy |

## API: verified workarounds

- **f3z** won't import via `importManager.createFusionArchiveImportOptions`
  (f3d only) -> `DataFolder.uploadFile(path)` into the project, then open it.
- **Cut "through all" both ways**: `setAllExtent(SymmetricExtentDirection)` /
  `setOneSideExtent(ThroughAll, Symmetric)` cuts **one way only** (confirmed
  by us and on the forum "API Extrude 2 sides Through All"). Works:
  `setTwoSidesExtent(ThroughAll, ThroughAll)`; when editing an existing
  feature the angles are needed too: `setTwoSidesExtent(a, b, V('0 deg'), V('0 deg'))`.
- **Editing an existing feature** -> first `feature.timelineObject.rollTo(True)`,
  then `design.timeline.moveToEnd()`, otherwise "Didn't roll editing feature back".
- `unitsManager.evaluateExpression(expr, 'mm')` returns **cm** (internal
  units), not mm.
- **Sketch on an offset construction plane**: dimensions from `originPoint`
  didn't make it "fully constrained". Workaround: sketch on the base plane +
  an `OffsetStartDefinition` on the extrude with the same expression.
- Sketch on the XZ plane: sketch x = world X, sketch y = **-**world Z -> place
  points via `sketch.modelToSketchSpace(Point3D)`.
- **A failed script rolls back entirely** (one transaction): no partial
  features are left, fix it and run again.
- `app.data.activeProject` fails (InternalValidationError) when no document
  is open -> find the project in `app.data.dataProjects` by name.
- A bought part (STEP): into a new component with a matrix
  (`addNewComponent(matrix)` + `importToTarget2(..., comp)`), then no position
  snapshot is needed.
- Someone else's large assembly: `occurrences.addByInsert(dataFile, matrix, True)`
  (XREF): light, updates, fine for Interference.
- A read-only script can: move the view camera, read `ui.activeCommand`,
  call `ui.terminateActiveCommand()` (verified while `SelectCommand` was active).
- `ui.activeSelections` is `None` while no document is open (hook v2 handles it).

## Hook v2 (2026-10-04, `tools/fusion_checkpoint.py`)

Verified on live Fusion on 04.10:
- `OrbitCommand` (Orbit button on the bottom bar) -> the hook closed it itself
  (`terminateActiveCommand` from a read-only script), checkpoint, allowed; 0.44 s.
- Extrude open (`Extrude`) -> the change was denied naming the command; the
  read was allowed; Extrude stayed open.
- Wrong port (simulating "Fusion is silent") -> denied at once; `messageBox` -> denied.
- Not verified live yet: the denial for an unsaved document in the background.

Command ids seen: `SelectCommand` (idle), `OrbitCommand`,
`ConstrainedOrbitCommand`, `FusionDeleteCommand`, `Extrude`.
State in one command: `python tools/fusion_status.py`.

## Rule for the tutor

After every build check the **geometry** (how many holes and where,
dimensions), not only Interference. The holes-on-one-wall mistake was caught
by the student, not by a check.
