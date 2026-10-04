"""PreToolUse hook: the tutor reads the course but writes only to the
student's own folder fusion-tutor/people/<me>/ and to fusion-tutor/shared/.

The course repo is shared by the team and graded. Read/Glob/Grep inside the
course are allowed without asking (only if the parent really is the course
clone, and never inside .git). Edit/Write only in people/<me>/ and shared/,
and even there never an instruction file (CLAUDE.md, AGENTS.md) or a
dot-name, which would plant instructions/settings for later sessions.
Lab publishing: Edit/Write inside 3d-print/labN/ and the commands
`tools/lab.py copy|commit` are never allowed silently: the hook answers "ask",
so the student sees and approves every change (denied in bypass mode, where
nobody would). Never there: assignment-EST.md, instruction files, dot-names,
or Write over an existing file (nothing is overwritten; Edit appends).
Everything else is denied: the rest of the course, other people's people/<other>/ and
the tutor itself (.claude/ incl. settings.local.json, or the tutor could
grant itself permissions; .mcp.json, CLAUDE.md, tools/, templates/). Writes
to people/ also need a confirmed identity: a guess by name or computer is
not enough. The course is deliberately NOT in additionalDirectories:
acceptEdits would then let sed/cp into it through the shell. Works for any
clone path, unlike path rules in settings.json.
"""
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sync  # noqa: E402  (odd_segment: one rule for both gates)
import whoami  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSE = os.path.dirname(ROOT)
READ_TOOLS = ("Read", "Glob", "Grep")
PEOPLE = os.path.join(ROOT, "people")
SHARED = os.path.join(ROOT, "shared")
INSTRUCTION_FILES = {"claude.md", "claude.local.md", "agents.md"}


def norm(p):
    return os.path.normcase(os.path.realpath(p))


def decide(decision, reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "permissionDecision": decision,
        "permissionDecisionReason": reason}}))


def deny(reason):
    decide("deny", reason)


def inside(target, folder):
    folder = norm(folder)
    try:
        return os.path.commonpath([target, folder]) == folder
    except ValueError:  # another drive
        return False


def is_course(folder):
    return (os.path.isdir(os.path.join(folder, ".git"))
            and os.path.isfile(os.path.join(folder, "AGENTS.md")))


def student_approves(call, what):
    """Lab changes: the student sees each one; nobody can in bypass mode."""
    if call.get("permission_mode") == "bypassPermissions":
        deny(f"{what} needs the student's approval, and bypass mode shows no prompt. "
             "Restart the tutor without --dangerously-skip-permissions.")
        return
    me, source = whoami.resolve()
    if not me or not whoami.is_sure(source):
        deny("Don't know for sure who is studying: run python tools/whoami.py first.")
        return
    decide("ask", f"{what}: the student ({me}) approves it. Lab rules: "
           "fusion-tutor/.claude/commands/lab-publish.md.")


def lab_of(target):
    labs = norm(os.path.join(COURSE, "3d-print"))
    if not inside(target, labs):
        return None
    lab = os.path.relpath(target, labs).split(os.sep)[0]
    return lab if re.fullmatch(r"lab\d+", lab) else None


def main():
    call = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    args = call.get("tool_input") or {}
    tool = call.get("tool_name", "")
    if tool in ("Bash", "PowerShell"):
        if re.search(r"\blab\.py\b[\s\S]*\b(copy|commit)\b", args.get("command") or ""):
            student_approves(call, "Publishing into the lab")
        return  # other commands: normal Claude Code rules
    path = args.get("file_path") or args.get("notebook_path") or args.get("path")
    if not path:
        return  # normal Claude Code rules
    target = norm(os.path.join(call.get("cwd") or ROOT, path))
    if tool in READ_TOOLS:
        if (is_course(COURSE) and inside(target, COURSE)
                and not inside(target, os.path.join(COURSE, ".git"))):
            decide("allow", "The tutor may read the course.")
        return
    # Check the path as given: Windows path normalisation (realpath/abspath) itself
    # drops trailing dots/spaces, so "CLAUDE.md." would already look like a new
    # name here while NTFS writes CLAUDE.md. Ambiguous names are denied outright,
    # with the same rule as sync.py's review gate.
    segs = [s for s in re.split(r"[\\/]+", path) if s not in ("", ".", "..")]
    if segs and re.fullmatch(r"[A-Za-z]:", segs[0]):
        segs = segs[1:]
    if any(sync.odd_segment(s) for s in segs):
        deny("Ambiguous file name (trailing dot/space, ':' stream, 8.3 short name, "
             "control or non-normalised characters): use a plain name.")
        return
    lab = lab_of(target) if is_course(COURSE) else None
    if lab:
        name = unicodedata.normalize("NFKC", os.path.basename(target)).casefold()
        rel = os.path.relpath(target, norm(COURSE)).split(os.sep)
        if any(s.startswith(".") for s in rel) or name in INSTRUCTION_FILES:
            deny("No instruction files or dot-files in the lab.")
        elif name == "assignment-est.md":
            deny("assignment-EST.md is the instructor's original: never edited.")
        elif tool == "Write" and os.path.exists(target):
            deny("Nothing in the lab is overwritten: Edit to append (devlog, file list), "
                 "or a new -vN file via tools/lab.py copy.")
        else:
            student_approves(call, f"Changing 3d-print/{lab}/")
        return
    if inside(target, SHARED) or inside(target, PEOPLE):
        rel = [unicodedata.normalize("NFKC", s).casefold()
               for s in os.path.relpath(target, norm(ROOT)).split(os.sep)]
        if any(s.startswith(".") for s in rel) or rel[-1] in INSTRUCTION_FILES:
            deny("No instruction files (CLAUDE.md, AGENTS.md) or dot-files in people/ or "
                 "shared/: they would act as instructions/settings for later sessions.")
            return
        if len(rel) == 3 and rel[0] == "people" and rel[2] == "profile.md":
            deny("profile.md is written only by tools/whoami.py (identity evidence). "
                 "To change the language: python tools/whoami.py --language <code>.")
            return
    if inside(target, SHARED):
        return
    if inside(target, PEOPLE):
        me, source = whoami.resolve()
        if not me:
            deny("Don't know who is studying: run python tools/whoami.py first.")
        elif not whoami.is_sure(source):
            deny(f"Only a guess that this is {me} ({source}). Ask the student, then "
                 f"python tools/whoami.py --set <login> (they approve it).")
        elif not inside(target, os.path.join(PEOPLE, me)):
            deny(f"That is someone else's folder: you write only to people/{me}/ and shared/.")
        return
    deny("The tutor writes only to people/<own login>/, shared/ and, with the student's "
         "approval, 3d-print/labN/ (see /lab-publish); the tutor itself (.claude/, "
         "tools/, CLAUDE.md, templates/) is not edited during a lesson.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # fail closed
        deny(f"guard_writes hook error: {e!r}")
