---
description: End the lesson: write the log and update progress.md
---

The lesson is ending. Talk to the student in their language; write files in
English.

1. If Fusion MCP is available, look at the final model once more (read only)
   and note what is good in it and what to fix.
2. Create or append `people/<login>/log/YYYY-MM-DD.md` (today's date) using:

   ```
   ## Lesson HH:MM - <topic>
   - Fusion file: <document name / version>
   - Did on their own:
   - Got stuck on, and how we solved it:
   - Mistakes (mark recurring ones "repeat"):
   - Understood (in the student's own words, if they said it):
   - Homework:
   ```
3. Update `people/<login>/progress.md`: skill statuses with dates, "Recurring
   mistakes", "Fixed", "Current goals". Delete nothing: change the status.
4. If the student phrased a useful rule or technique, add it to
   `people/<login>/my-rules.md`. Research from the lesson goes to their
   `research/`. If something is useful for the whole team (part data, Fusion
   pitfalls), ask whether to put it into `shared/`; without their "yes", don't.
5. `python tools/sync.py push "lesson: <date> <topic>"` sends only their
   folder and `shared/`. If the push fails, say the commit stayed local.
6. Show the student a 3-5 line summary and the homework.
