"""PreToolUse hook: the tutor reads the course but writes only to the
student's own folder fusion-tutor/people/<me>/ and to fusion-tutor/shared/.

The course repo is shared by the team and graded. Read/Glob/Grep inside the
course are allowed without asking (only if the parent really is the course
clone, and never inside .git). Edit/Write only in people/<me>/ and shared/,
and even there never an instruction file (CLAUDE.md, AGENTS.md) or a
dot-name, which would plant instructions/settings for later sessions.
Everything else is denied: the course, other people's people/<other>/ and
the tutor itself (.claude/ incl. settings.local.json, or the tutor could
grant itself permissions; .mcp.json, CLAUDE.md, tools/, templates/). Writes
to people/ also need a confirmed identity: a guess by name or computer is
not enough. The course is deliberately NOT in additionalDirectories:
acceptEdits would then let sed/cp into it through the shell. Works for any
clone path, unlike path rules in settings.json.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
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


def main():
    call = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    args = call.get("tool_input") or {}
    tool = call.get("tool_name", "")
    path = args.get("file_path") or args.get("notebook_path") or args.get("path")
    if not path:
        return  # normal Claude Code rules
    target = norm(os.path.join(call.get("cwd") or ROOT, path))
    if tool in READ_TOOLS:
        if (is_course(COURSE) and inside(target, COURSE)
                and not inside(target, os.path.join(COURSE, ".git"))):
            decide("allow", "The tutor may read the course.")
        return
    if inside(target, SHARED) or inside(target, PEOPLE):
        rel = os.path.relpath(target, norm(ROOT)).split(os.sep)
        if any(s.startswith(".") for s in rel) or rel[-1].casefold() in INSTRUCTION_FILES:
            deny("No instruction files (CLAUDE.md, AGENTS.md) or dot-files in people/ or "
                 "shared/: they would act as instructions/settings for later sessions.")
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
    deny("The tutor writes only to people/<own login>/ and shared/. Course files are "
         "changed by the student, following the lab rules; the tutor itself (.claude/, "
         "tools/, CLAUDE.md, templates/) is not edited during a lesson.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # fail closed
        deny(f"guard_writes hook error: {e!r}")
