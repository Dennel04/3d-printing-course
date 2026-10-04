"""PreToolUse-хук: курс учитель читает, а пишет только в fusion-tutor/.

Курсовой репозиторий командный и с оцениванием. Read/Glob/Grep внутри
курса разрешаются без вопросов; Edit/Write вне fusion-tutor/ (и в сам
хук/настройки учителя) запрещены. Курс нарочно НЕ добавлен в
additionalDirectories: тогда acceptEdits без вопросов пропускал бы
sed/cp туда через shell. Работает на любом пути клона, в отличие от
path-правил в settings.json.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSE = os.path.dirname(ROOT)
READ_TOOLS = ("Read", "Glob", "Grep")
PROTECTED = [os.path.join(ROOT, ".claude", "settings.json"),
             os.path.join(ROOT, "tools")]


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
    return os.path.commonpath([target, folder]) == folder


def main():
    call = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    args = call.get("tool_input") or {}
    tool = call.get("tool_name", "")
    path = args.get("file_path") or args.get("notebook_path") or args.get("path")
    if not path:
        return  # обычные правила Claude Code
    target = norm(os.path.join(call.get("cwd") or ROOT, path))
    if tool in READ_TOOLS:
        if inside(target, COURSE):
            decide("allow", "Чтение курса разрешено учителю.")
        return
    if not inside(target, ROOT):
        deny("Учитель пишет только в папку fusion-tutor/. Курсовые файлы "
             "студент меняет сам, по правилам лабы.")
    elif any(target == norm(p) or target.startswith(norm(p) + os.sep) for p in PROTECTED):
        deny("Хуки и настройки учителя не правятся из занятия.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # fail closed
        deny(f"guard_writes hook error: {e!r}")
