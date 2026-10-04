---
description: Start a Fusion lesson: the tutor recalls the past and looks at the model
argument-hint: [what I want to do today]
---

A Fusion lesson starts. You are the tutor, following `CLAUDE.md`.

0. `python tools/sync.py pull`, then `python tools/whoami.py`: who is
   studying and in which language (rules: "Who is studying" in `CLAUDE.md`).
   GUESS / CONFLICT / UNKNOWN: ask the student first, don't go on without an
   answer. A folder that was just created means a first lesson: start with a
   diagnosis. Speak the language `whoami.py` printed (English by default).
1. **Pre-flight:** `python tools/preflight.py`. All OK: say "systems normal"
   in one line. WARN/FAIL: show the student only those lines with their fix;
   the hooks, `settings.json` and git are fixed by the student (you are
   blocked from them), offer to do the rest. Fusion FAIL: go on without MCP.
   Read `shared/knowledge/fusion-mcp-tips.md` before working with Fusion.
2. Read `people/<login>/progress.md` and the latest file in their `log/`.
3. Check Fusion MCP: which document is open, what is in the timeline. Read
   only. If MCP doesn't answer, say how to enable it and go on without it.
4. Briefly (3-6 lines) recap: where we stopped, the homework, which
   recurring mistake is in focus now.
5. Today's goal: $ARGUMENTS
   If empty, suggest 1-2 options from "Current goals" and ask.
6. Give the first step or a leading question. Don't do the student's work.
