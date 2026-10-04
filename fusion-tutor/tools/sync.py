"""Синхронизация учителя с GitHub — единственный путь учителя в git.

Коммитит ТОЛЬКО fusion-tutor/people/<я>/ и fusion-tutor/shared/ — чужие
папки, лабы и то, что студент сам держит в индексе, не трогает.

  python tools/sync.py pull                -> подтянуть команду (rebase, autostash)
  python tools/sync.py push "сообщение"    -> commit своих путей + push
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import whoami  # noqa: E402

COURSE = os.path.dirname(whoami.ROOT)


def git(*args, check=True):
    r = subprocess.run(["git", *args], cwd=COURSE, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}:\n{r.stdout}{r.stderr}".strip())
    return r


def pull():
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
    if git("diff", "--cached", "--quiet", "--", *paths, check=False).returncode == 0:
        print("Нечего коммитить.")
        return
    git("commit", "-m", f"tutor({login}): {message}", "--", *paths)
    for attempt in (1, 2):
        if git("push", check=False).returncode == 0:
            print(f"Отправлено: {git('log', '--oneline', '-1').stdout.strip()}")
            return
        pull()
    raise RuntimeError("push не удался — коммит остался локально, попробуй позже.")


def main(argv):
    if argv[:1] == ["pull"]:
        pull()
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
