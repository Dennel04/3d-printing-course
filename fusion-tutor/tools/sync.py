"""Синхронизация учителя с GitHub — единственный путь учителя в git.

Коммитит ТОЛЬКО fusion-tutor/people/<я>/ и fusion-tutor/shared/ — чужие
папки, лабы и то, что студент сам держит в индексе, не трогает.

  python tools/sync.py pull                -> подтянуть команду (rebase, autostash)
  python tools/sync.py pull --accept       -> то же, когда изменился сам учитель
  python tools/sync.py push "сообщение"    -> commit своих путей + push

Код учителя (.claude/, tools/, CLAUDE.md, AGENTS.md, .mcp.json, templates/)
выполняется как хуки и инструкции на каждой машине. Если pull его меняет,
sync ничего не применяет и показывает изменения: человек смотрит их и сам
запускает `pull --accept` (учителю это без одобрения не разрешено).
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import whoami  # noqa: E402

COURSE = os.path.dirname(whoami.ROOT)
TUTOR_CODE = [f"fusion-tutor/{p}" for p in
              (".claude", "tools", "CLAUDE.md", "AGENTS.md", ".mcp.json", "templates")]


def git(*args, check=True):
    r = subprocess.run(["git", *args], cwd=COURSE, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}:\n{r.stdout}{r.stderr}".strip())
    return r


def pull(accept=False):
    git("fetch", "--quiet")
    upstream = git("rev-parse", "--abbrev-ref", "@{upstream}").stdout.strip()
    changed = git("diff", "--stat", f"HEAD...{upstream}", "--", *TUTOR_CODE).stdout.strip()
    if changed and not accept:
        raise RuntimeError(
            "В GitHub изменился сам учитель (хуки/инструкции) — без просмотра не "
            "применяю:\n" + changed + f"\n\nПосмотреть: git diff HEAD...{upstream} -- fusion-tutor\n"
            "Если всё в порядке: python tools/sync.py pull --accept")
    r = git("pull", "--rebase", "--autostash", check=False)
    if r.returncode != 0:
        git("rebase", "--abort", check=False)
        raise RuntimeError("pull не удался (конфликт?), ничего не изменено:\n" + r.stdout + r.stderr)


def push(message):
    login, _ = whoami.resolve()
    if not login:
        sys.exit("Не знаю, кто занимается: сначала python tools/whoami.py")
    paths = [f"fusion-tutor/people/{login}", "fusion-tutor/shared"]
    paths = [p for p in paths if os.path.exists(os.path.join(COURSE, p))]
    git("add", "--", *paths)
    if git("diff", "--cached", "--quiet", "--", *paths, check=False).returncode != 0:
        git("commit", "-m", f"tutor({login}): {message}", "--", *paths)
    # Неотправленные коммиты (в т.ч. от прошлого неудачного push) отправляем,
    # только если все они — учителя: свои коммиты студента пушит он сам.
    ahead = git("rev-list", "@{upstream}..HEAD").stdout.split()
    if not ahead:
        print("Нечего отправлять.")
        return
    foreign = [c for c in ahead if any(
        not any(f == p or f.startswith(p + "/") for p in paths)
        for f in git("diff-tree", "-z", "--no-commit-id", "--name-only", "-r", c).stdout.split("\0") if f)]
    if foreign:
        raise RuntimeError("Есть неотправленные коммиты не только учителя "
                           f"({', '.join(c[:7] for c in foreign)}) — их отправляет студент сам "
                           "(git push). Коммит учителя сохранён локально.")
    for attempt in (1, 2):
        if git("push", check=False).returncode == 0:
            print(f"Отправлено: {git('log', '--oneline', '-1').stdout.strip()}")
            return
        pull()
    raise RuntimeError("push не удался — коммит остался локально, попробуй позже.")


def main(argv):
    if argv[:1] == ["pull"]:
        pull(accept=argv[1:] == ["--accept"])
        print("Подтянуто.")
    elif argv[:1] == ["push"] and len(argv) >= 2:
        push(" ".join(argv[1:]))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # консоль Windows бывает cp1252
    sys.stderr.reconfigure(encoding="utf-8")
    try:
        main(sys.argv[1:])
    except RuntimeError as e:
        sys.exit(str(e))
