"""PreToolUse-хук: учитель пишет только в свою папку fusion-tutor/.

Курсовой репозиторий командный и с оцениванием — Edit/Write в него (и в
сам хук/настройки учителя) запрещены. Работает на любом пути клона, в
отличие от path-правил в settings.json.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROTECTED = [os.path.join(ROOT, ".claude", "settings.json"),
             os.path.join(ROOT, "tools")]


def norm(p):
    return os.path.normcase(os.path.realpath(p))


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "permissionDecision": "deny",
        "permissionDecisionReason": reason}}))


def main():
    call = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    args = call.get("tool_input") or {}
    path = args.get("file_path") or args.get("notebook_path")
    if not path:
        return
    target = norm(os.path.join(call.get("cwd") or ROOT, path))
    root = norm(ROOT)
    if os.path.commonpath([target, root]) != root:
        deny("Учитель пишет только в папку fusion-tutor/. Курсовые файлы "
             "студент меняет сам, по правилам лабы.")
    elif any(target == norm(p) or target.startswith(norm(p) + os.sep) for p in PROTECTED):
        deny("Хуки и настройки учителя не правятся из занятия.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # fail closed
        deny(f"guard_writes hook error: {e!r}")
