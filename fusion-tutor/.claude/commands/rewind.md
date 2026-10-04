---
description: Roll the Fusion model back to an earlier version (like /rewind in Claude Code)
argument-hint: [version number, or "last" to undo the last step]
---

Roll back the active Fusion document. Argument: $ARGUMENTS

1. If the argument is `last`: one `fusion_mcp_update` `undo` call, show a
   screenshot and stop.
2. Otherwise show the list of versions (read-only script, `readOnly: true`):

   ```python
   import adsk.core, datetime
   def run(_context: str):
       doc = adsk.core.Application.get().activeDocument
       print(doc.name, "| unsaved changes:", doc.isModified)
       for v in doc.dataFile.versions:
           t = datetime.datetime.fromtimestamp(v.dateCreated).strftime("%d.%m %H:%M:%S")
           print(f"v{v.versionNumber}  {t}  {v.description}")
   ```
   Next to each version, add what the tutor changed after it, from
   `people/<login>/log/fusion-actions.jsonl` / the lesson log. If no number
   was given, ask which version to go back to.
3. Roll back to version N: one `fusion_mcp_execute` script call (without
   readOnly; the hook saves the current state first, so the rollback can be
   undone too):

   ```python
   import adsk.core, adsk.fusion
   def run(_context: str):
       app = adsk.core.Application.get()
       doc = app.activeDocument
       df = doc.dataFile
       target = [v for v in df.versions if v.versionNumber == N][0]
       if not target.promote():          # version N becomes the new latest
           raise RuntimeError("promote() failed")
       doc.close(False)                  # the current state is already checkpointed
       newdoc = app.documents.open(df.latestVersion)
       d = adsk.fusion.Design.cast(app.activeProduct)
       print("opened", newdoc.name, "v", newdoc.dataFile.versionNumber,
             [b.name for b in d.rootComponent.bRepBodies])
   ```
   (Verified 2026-10-03 on `_tutor-sandbox`: v1 -> v8 and back v7 -> v9.)
   The hook refuses this while other documents have unsaved changes (the
   reopen would pop up a "save?" dialog): ask the student to save or close them.
4. Check the result (`inspect_model.py` + screenshot) and tell the student
   what we went back to. Note the rollback in the lesson log.
