"""Pre-flight check before a lesson: python tools/preflight.py

Like an aircraft checklist: every system is OK, WARN (can fly, but worth
fixing) or FAIL (not working). Every problem comes with how to fix it.
Changes nothing. Exit code 1 if anything FAILs.
"""
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fusion_checkpoint as hook  # noqa: E402
import whoami  # noqa: E402

ROOT = whoami.ROOT
COURSE = os.path.dirname(ROOT)
results = []


def check(level, name, detail="", fix=""):
    results.append((level, name, detail, fix))


def git(*args):
    r = subprocess.run(["git", *args], cwd=COURSE, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    return r.stdout.strip()


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # the Windows console defaults to cp1252

    # 1. Python
    v = sys.version_info
    check("ok" if v >= (3, 9) else "fail", "Python", f"{v.major}.{v.minor}",
          "" if v >= (3, 9) else "Python 3.9+ is needed (hooks and checks run on it)")

    # 2. Who is studying
    me, source = whoami.resolve()
    if not me:
        check("fail", "Student", "unknown",
              "Ask for the GitHub login, then: python tools/whoami.py --set <login>")
    elif source.startswith("computer"):
        check("warn", "Student", f"{me} (by computer name only)",
              "Lab computers are shared: confirm who this is before using their memory")
    else:
        check("ok", "Student", f"{me} (by {source}), language: {whoami.language(me)}")

    # 3. Git
    head = git("status", "-sb").splitlines()
    first = head[0] if head else "?"
    if "ahead" in first:
        check("warn", "Git", first, "Unpushed commits: `python tools/sync.py push \"...\"` "
              "for tutor ones; your own lab commits you push yourself")
    elif "behind" in first:
        check("warn", "Git", first, "Behind GitHub: python tools/sync.py pull")
    else:
        check("ok", "Git", first)

    # 4. Claude Code settings and hooks
    try:
        st = json.load(open(os.path.join(ROOT, ".claude", "settings.json"), encoding="utf-8"))
    except Exception as e:
        check("fail", "settings.json", f"unreadable: {e}", "Restore it from git")
        st = {}
    pre = (st.get("hooks") or {}).get("PreToolUse") or []

    def hooked(script):
        return [h for h in pre if any(script in x.get("command", "") for x in h.get("hooks", []))]

    cp = hooked("fusion_checkpoint.py")
    if not cp:
        check("fail", "Checkpoint hook", "not wired in settings.json", "Restore .claude/settings.json from git")
    elif "read" not in cp[0].get("matcher", ""):
        check("warn", "Checkpoint hook", f"matcher {cp[0].get('matcher')}: reads go unchecked",
              "Restore .claude/settings.json from git")
    else:
        check("ok", "Checkpoint hook", cp[0]["matcher"])
    if not hooked("guard_writes.py"):
        check("fail", "Write guard", "not wired: the tutor could write anywhere",
              "Restore .claude/settings.json from git")
    else:
        check("ok", "Write guard", "writes only to people/<me>/ and shared/")

    # 5. MCP config
    try:
        mcp = json.load(open(os.path.join(ROOT, ".mcp.json"), encoding="utf-8"))
        url = mcp["mcpServers"]["fusion"]["url"]
        enabled = "fusion" in (st.get("enabledMcpjsonServers") or [])
        check("ok" if enabled else "fail", "MCP config", url + ("" if enabled else ": server not enabled"),
              "" if enabled else 'In settings.json: "enabledMcpjsonServers": ["fusion"]')
    except Exception as e:
        check("fail", "MCP config", f".mcp.json: {e}", "Restore .mcp.json from git")

    # 6. Course
    if os.path.isfile(os.path.join(COURSE, "AGENTS.md")):
        check("ok", "Course", COURSE)
    else:
        check("fail", "Course", f"{COURSE} is not the course repo",
              "Run the tutor from 3d-printing-course/fusion-tutor")

    # 7. Lesson memory
    if me:
        home = os.path.join(ROOT, "people", me)
        has_progress = os.path.exists(os.path.join(home, "progress.md"))
        logdir = os.path.join(home, "log")
        logs = [f for f in os.listdir(logdir) if f[:4].isdigit()] if os.path.isdir(logdir) else []
        check("ok" if has_progress else "warn", "Memory",
              f"progress.md {'present' if has_progress else 'MISSING'}, lesson logs: {len(logs)}"
              + (f", latest {max(logs)}" if logs else ""),
              "" if has_progress else "python tools/whoami.py creates it from templates/")

    # 8. Fusion live
    try:
        t0 = time.time()
        s = hook.Fusion().state()
        ms = int((time.time() - t0) * 1000)
    except Exception as e:
        check("fail", "Fusion", f"not answering ({e})",
              "Start Fusion; Preferences > General > API > Fusion MCP Server; "
              "if Fusion is open, close the dialog in it (save?/message)")
    else:
        idle = s["cmd"] in hook.IDLE
        check("ok" if idle else "warn", "Fusion",
              f"answers in {ms} ms, command: {s['cmdName'] or s['cmd'] or '-'}",
              "" if idle else "A command is open in Fusion: finish it (OK) or press Esc")
        for d in s["docs"]:
            if d["modified"] and not d["active"]:
                check("warn", "Document", f"{d['name']}: unsaved changes in the background",
                      "Save or close it, otherwise a new document makes Fusion ask \"save?\" and freeze")
            elif d["active"] and not d["saved"]:
                check("warn", "Document", f"{d['name']}: never saved",
                      "Save it to a project (Ctrl+S), otherwise no checkpoints and no rollback")
        if not s["docs"]:
            check("ok", "Documents", "nothing open")

    icon = {"ok": "OK  ", "warn": "WARN", "fail": "FAIL"}
    for level, name, detail, fix in results:
        print(f"{icon[level]} {name}: {detail}")
        if fix and level != "ok":
            print(f"     -> {fix}")
    fails = sum(1 for r in results if r[0] == "fail")
    warns = sum(1 for r in results if r[0] == "warn")
    print()
    print("Ready for take-off." if not fails and not warns else f"Total: FAIL {fails}, WARN {warns}.")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
