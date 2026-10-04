# fusion-tutor: a Fusion tutor for the team

A mentor for modelling in Autodesk Fusion, running on Claude Code: it looks at
your model through Fusion MCP, gives hints step by step (question -> tool ->
steps) and remembers past lessons: **every team member has their own memory**.
It teaches rather than models for you; on request it can do it itself, with an
automatic checkpoint before every change. It starts in English and switches
to your language if you ask (saved in your profile).

## What you need

- [Claude Code](https://claude.com/claude-code), Python 3 and git on PATH.
  Preferably [GitHub CLI](https://cli.github.com/) (`gh auth login`): it is
  the surest way for the tutor to recognise you.
- Fusion: Preferences > General > API > enable **Fusion MCP Server**
  (port 27182, path `/mcp`).

## How to use it

1. `cd 3d-printing-course/fusion-tutor && claude`: start it **from this
   folder**, otherwise the role, commands and hooks aren't loaded. The first
   time: accept the trust dialog and approve the `fusion` MCP server.
2. `/lesson today I want to ...`: the tutor pulls the repo, recognises you,
   runs the pre-flight check and opens your memory. The first time it
   creates `people/<your-login>/`.
3. You model yourself, ask the tutor, it looks at the model.
4. "This is for everyone" / "ready for the lab": the tutor copies the material
   to `shared/`.
5. `/lab-publish <part> <version>`: put a finished part into `3d-print/labN/`
   the way the lab asks (source/STL/3MF `-vN`, README file list and devlog in
   Estonian), check it with `tools/lab.py check`, commit only that lab. You
   approve every copy, README edit and the commit in a prompt.
6. `/rewind [N|last]`: roll the document back to version N (history is kept)
   or undo the last step.
7. `/lesson-end`: lesson log, progress update, commit + push of your folder.

Any time: `python tools/preflight.py` (all systems check) and
`python tools/fusion_status.py` (Fusion state + the tutor's last actions).
The Fusion document must have been saved to a project at least once, or the
hook won't let the tutor change it (there would be nothing to roll back to).

## How the tutor knows who you are

`tools/whoami.py` matches what this computer says against
`people/*/profile.md`:
- **sure**: your GitHub account (`gh`), git email, university e-mail, Windows
  user name: it just greets you;
- **guess**: a similar name (Windows full name, git `user.name`) or the lab
  computer you used before (lab PCs are shared): it asks "Are you X?";
- **conflict or nothing**: it asks for your GitHub login.
A confirmed answer is cached for this computer + Windows user in `.whoami`
(not in git). Shared accounts like `student` are never trusted. Your language
lives in `profile.md` (`- language: en`) with a dated history of changes.

## Layout

```
people/<login>/     - each person's own (in git): profile, progress, my-rules,
                      log/, research/, models/, docs/      -> people/README.md
shared/             - for everyone, only on the author's word -> shared/README.md
  knowledge/          techniques, Fusion pitfalls, part data
  lab-ready/labN/     ready for a teammate's lab; /lab-publish moves it into 3d-print/
templates/          - starting files for a new person's folder
CLAUDE.md, AGENTS.md, .claude/, tools/ - the tutor itself
```

## Good to know

- **Full access to Fusion without prompts.** The tutor's scripts are arbitrary
  Python inside Fusion. Protection: the hook `tools/fusion_checkpoint.py`
  pings Fusion before every call (a silent Fusion almost always means a dialog
  is open), closes orbit/pan itself but never your real command, refuses to
  open documents while others are unsaved, saves a version ("claude
  checkpoint ...") before every change, and logs everything to
  `people/<login>/log/fusion-actions.jsonl`. `ui.messageBox` is blocked (it
  freezes Fusion).
- **Where the tutor writes.** `tools/guard_writes.py` allows writes only to
  your folder (once you are confirmed) and to `shared/`, never instruction
  files or dot-files there; the course, other people's folders and the tutor
  itself are read-only. Shell commands that change the course (`sed`, `cp` ...)
  are asked of you by Claude Code: don't approve them. This guards against
  mistakes, it is not a sandbox: a Python script in Fusion can technically
  write anything to disk.
- **Git only via `tools/sync.py`.** It commits just `people/<you>/` and
  `shared/`, leaves your labs and staged files alone and never pushes your own
  unpushed commits.
- **The tutor's own updates from GitHub are never applied silently.** `sync.py
  pull` takes only data without asking: files in `people/`, `shared/` and lab
  work. If anything that runs or is read as instructions changed (`tools/`,
  `.claude/`, any `CLAUDE.md`/`AGENTS.md`, root files, symlinks ...), it stops
  and shows the files and a SHA. Read the diff and, if it's fine, run
  `python tools/sync.py pull --accept <SHA>` yourself: exactly what you
  reviewed is applied (the tutor may not do this without your approval).
- **`whoami.py --set`** also needs your approval, and refuses if GitHub on the
  computer names a different login. This prevents mix-ups, it is not
  authentication: the real control is push access to the repo.
- **Another AI agent** (Codex, Cursor ...) reads `AGENTS.md` -> `CLAUDE.md`, but
  the hooks don't run there; it has to follow the rules itself.
