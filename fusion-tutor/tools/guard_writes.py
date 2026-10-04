"""PreToolUse-хук: курс учитель читает, а пишет только в свою папку
участника fusion-tutor/people/<я>/ и в общую fusion-tutor/shared/.

Курсовой репозиторий командный и с оцениванием. Read/Glob/Grep внутри
курса разрешаются без вопросов (только если папка выше — действительно клон
курса, и не внутри .git); Edit/Write — только в people/<я>/ и shared/.
Всё остальное запрещено: курс, чужие папки people/<другой>/ и сам учитель
(.claude/ — в т.ч. settings.local.json, иначе учитель мог бы выдать себе
права, — .mcp.json, CLAUDE.md, tools/, templates/). Курс нарочно НЕ добавлен в
additionalDirectories: тогда acceptEdits без вопросов пропускал бы
sed/cp туда через shell. Работает на любом пути клона, в отличие от
path-правил в settings.json.
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
    except ValueError:  # другой диск
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
        return  # обычные правила Claude Code
    target = norm(os.path.join(call.get("cwd") or ROOT, path))
    if tool in READ_TOOLS:
        if (is_course(COURSE) and inside(target, COURSE)
                and not inside(target, os.path.join(COURSE, ".git"))):
            decide("allow", "Чтение курса разрешено учителю.")
        return
    if inside(target, SHARED):
        return
    if inside(target, PEOPLE):
        me, _ = whoami.resolve()
        if not me:
            deny("Не знаю, кто занимается: сначала python tools/whoami.py "
                 "(или --set <логин>).")
        elif not inside(target, os.path.join(PEOPLE, me)):
            deny(f"Это чужая папка: ты пишешь только в people/{me}/ и shared/.")
        return
    deny("Учитель пишет только в people/<свой логин>/ и shared/. Курсовые "
         "файлы студент меняет сам, по правилам лабы; сам учитель (.claude/, "
         "tools/, CLAUDE.md, templates/) не правится из занятия.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # fail closed
        deny(f"guard_writes hook error: {e!r}")
