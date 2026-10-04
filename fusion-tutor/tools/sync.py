"""Синхронизация учителя с GitHub — единственный путь учителя в git.

Коммитит ТОЛЬКО fusion-tutor/people/<я>/ и fusion-tutor/shared/ — чужие
папки, лабы и то, что студент сам держит в индексе, не трогает.

  python tools/sync.py pull                -> подтянуть команду (rebase, autostash)
  python tools/sync.py pull --accept SHA   -> применить ровно SHA, просмотренный человеком
  python tools/sync.py push "сообщение"    -> commit своих путей + push

Хуки, настройки и инструкции (tools/, .claude/, CLAUDE.md, …) выполняются
или читаются агентом на каждой машине. Поэтому без вопросов pull применяет
только «данные»: обычные файлы в people/ и shared/ учителя и работу в лабах.
Всё остальное (белый список, а не чёрный; регистр букв не важен — Windows
его не различает) — только после просмотра: sync показывает файлы и SHA,
человек смотрит diff и сам запускает `pull --accept SHA` (учителю это без
одобрения не разрешено). Применяется ровно проверенный SHA, а не то, что
окажется на GitHub через секунду.
"""
import json
import os
import re
import subprocess
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import whoami  # noqa: E402

COURSE = os.path.dirname(whoami.ROOT)
DATA_DIRS = ("fusion-tutor/people/", "fusion-tutor/shared/")
INSTRUCTION_FILES = {"claude.md", "claude.local.md", "agents.md"}
SPECIAL_MODES = {"120000", "160000"}  # симлинк, submodule
SHA_RE = re.compile(r"^[0-9a-f]{40}$")

def git(*args, check=True):
    r = subprocess.run(["git", *args], cwd=COURSE, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}:\n{r.stdout}{r.stderr}".strip())
    return r


def odd_segment(s):
    """Имя, которое Windows/NTFS может прочитать не так, как git."""
    return (s != s.rstrip(". ")                       # NTFS обрезает точки/пробелы в конце
            or any(ord(c) < 32 or c in ':\\*?"<>|' for c in s)  # потоки ADS, \, управляющие
            or re.search(r"~\d", s) is not None         # короткие имена 8.3 (FUSION~1)
            or unicodedata.normalize("NFC", s) != s)


def needs_review(path, modes):
    """True, если изменение может исполниться или стать инструкцией агента."""
    raw = path.split("/")
    if modes & SPECIAL_MODES or any(odd_segment(s) for s in raw):
        return True
    parts = [unicodedata.normalize("NFKC", s).casefold() for s in raw]
    if (len(parts) == 1                                 # файлы в корне курса
            or any(s.startswith(".") for s in parts)    # .claude, .mcp.json, .whoami, .git*
            or parts[-1] in INSTRUCTION_FILES):         # CLAUDE.md / AGENTS.md где угодно
        return True
    if parts[0] == "fusion-tutor" or not raw[0].isascii():
        return not (len(parts) >= 3 and raw[0].isascii() and raw[1].isascii()
                    and parts[1] in ("people", "shared"))
    return False


def incoming(target):
    """Пути, которые меняет target относительно общей с HEAD базы, с режимами."""
    raw = git("diff", "--raw", "-z", "--no-renames", f"HEAD...{target}").stdout.split("\0")
    out = {}
    for meta, path in zip(raw[0::2], raw[1::2]):
        if meta.startswith(":"):
            old_mode, new_mode = meta[1:].split()[:2]
            out[path] = {old_mode, new_mode}
    return out


def pull(accept=None):
    git("fetch", "--quiet")
    upstream = git("rev-parse", "@{upstream}").stdout.strip()
    if accept is None:
        target = upstream
    else:
        if not SHA_RE.match(accept):
            raise RuntimeError("--accept ждёт полный SHA из сообщения sync.py pull.")
        if git("merge-base", "--is-ancestor", accept, upstream, check=False).returncode != 0:
            raise RuntimeError(f"{accept[:7]} нет в истории GitHub — проверь SHA.")
        target = accept
    gated = sorted(p for p, m in incoming(target).items() if needs_review(p, m))
    if gated and accept is None:
        raise RuntimeError(
            "В GitHub изменились хуки/настройки/инструкции — без просмотра не применяю:\n  "
            # имена из чужих коммитов — только экранированными и не в команде
            + "\n  ".join(json.dumps(p, ensure_ascii=False) for p in gated)
            + f"\n\nПосмотреть: git diff HEAD...{target}"
            + f"\nЕсли всё в порядке: python tools/sync.py pull --accept {target}")
    r = git("rebase", "--autostash", target, check=False)  # ровно проверенный коммит
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
        if argv[1:2] == ["--accept"] and len(argv) == 3:
            pull(accept=argv[2])
        elif len(argv) == 1:
            pull()
        else:
            sys.exit(__doc__)
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
