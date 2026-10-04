# people: one folder per team member

`people/<github-login>/` is created by the tutor at the first lesson
(`python tools/whoami.py`). The tutor writes only to the folder of whoever is
studying right now; other people's folders are read-only.

```
<login>/
  profile.md     - how to recognise the student (github, emails, Windows user,
                   name, computers), their language and language history
  progress.md    - skill map, recurring mistakes, current goals
  my-rules.md    - own rules in own words
  log/           - YYYY-MM-DD.md per lesson + fusion-actions.jsonl (what the tutor did in Fusion)
  research/      - research, write-ups, comparing options
  models/        - model exports (.f3d / .step / .stl) and notes on them
  docs/          - measurements, photos, drafts
```

Files are in English; the tutor talks to each student in their `language`.
What is ready for everyone or for the lab goes to `../shared/`.
