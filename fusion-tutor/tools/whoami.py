"""Кто сейчас занимается с учителем — GitHub-логин участника команды.

Порядок (от надёжного к слабому):
  1. кэш `.whoami` для этого компьютера и пользователя Windows (в git не идёт);
  2. `gh api user` — аккаунт GitHub, под которым здесь работает git;
  3. `git config user.email` из people/*/profile.md;
  4. имя компьютера из people/*/profile.md — СЛАБО: компьютеры в аудитории
     общие, учитель обязан переспросить.

  python tools/whoami.py              -> "login <логин> source <откуда>" или "UNKNOWN"
  python tools/whoami.py --set LOGIN  -> создать/привязать папку people/LOGIN/
"""
import datetime
import getpass
import json
import os
import re
import shutil
import socket
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PEOPLE = os.path.join(ROOT, "people")
TEMPLATES = os.path.join(ROOT, "templates")
CACHE = os.path.join(ROOT, ".whoami")
LOGIN_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")
SUBDIRS = ("log", "research", "models", "docs")


def sh(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=15, cwd=ROOT)
        return r.stdout.strip() if r.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def machine():
    return {"computer": os.environ.get("COMPUTERNAME") or socket.gethostname(),
            "os_user": getpass.getuser(),
            "git_email": sh(["git", "config", "user.email"]).lower()}


def profiles():
    """{login: {"git_email": [...], "computer": [...]}} из people/*/profile.md."""
    out = {}
    if not os.path.isdir(PEOPLE):
        return out
    for login in os.listdir(PEOPLE):
        p = os.path.join(PEOPLE, login, "profile.md")
        if not os.path.isfile(p):
            continue
        keys = {"git_email": [], "computer": []}
        for line in open(p, encoding="utf-8"):
            m = re.match(r"^- (git_email|computer):\s*(.+?)\s*$", line)
            if m:
                keys[m.group(1)].append(m.group(2).lower())
        out[login] = keys
    return out


def resolve(network=True):
    """(login, source) или (None, None)."""
    m = machine()
    key = f"{m['computer']}|{m['os_user']}".lower()
    try:
        c = json.load(open(CACHE, encoding="utf-8"))
        if c.get("key") == key and LOGIN_RE.match(c.get("login", "")):
            return c["login"], "cache"
    except (OSError, ValueError):
        pass
    if network:
        login = sh(["gh", "api", "user", "--jq", ".login"])
        if LOGIN_RE.match(login):
            return login, "github"
    profs = profiles()
    if m["git_email"]:
        hits = [l for l, k in profs.items() if m["git_email"] in k["git_email"]]
        if len(hits) == 1:
            return hits[0], "git_email"
    hits = [l for l, k in profs.items() if m["computer"].lower() in k["computer"]]
    if len(hits) == 1:
        return hits[0], "computer (общий компьютер? переспроси)"
    return None, None


def remember(login):
    m = machine()
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump({"login": login, "key": f"{m['computer']}|{m['os_user']}".lower()}, f)


def ensure(login):
    """Создать people/<login>/ из шаблонов и дописать этот компьютер в профиль."""
    home = os.path.join(PEOPLE, login)
    for d in SUBDIRS:
        os.makedirs(os.path.join(home, d), exist_ok=True)
        keep = os.path.join(home, d, ".gitkeep")
        if not os.listdir(os.path.join(home, d)):
            open(keep, "w").close()
    for name in ("progress.md", "my-rules.md"):
        dst = os.path.join(home, name)
        if not os.path.exists(dst):
            shutil.copy(os.path.join(TEMPLATES, name), dst)
    m = machine()
    prof = os.path.join(home, "profile.md")
    if not os.path.exists(prof):
        with open(prof, "w", encoding="utf-8", newline="\n") as f:
            f.write(f"# {login}\n\n"
                    f"Создан {datetime.date.today().isoformat()}. По этим строкам учитель\n"
                    "узнаёт участника, если GitHub не отвечает. Строки `- key: value`\n"
                    "можно дописывать.\n\n"
                    f"- github: {login}\n")
    text = open(prof, encoding="utf-8").read().lower()
    add = []
    if m["git_email"] and f"- git_email: {m['git_email']}" not in text:
        add.append(f"- git_email: {m['git_email']}\n")
    if f"- computer: {m['computer'].lower()}" not in text:
        add.append(f"- computer: {m['computer']}\n")
    if add:
        with open(prof, "a", encoding="utf-8", newline="\n") as f:
            f.writelines(add)
    return home


def main(argv):
    if len(argv) >= 2 and argv[0] == "--set":
        login = argv[1]
        if not LOGIN_RE.match(login):
            sys.exit(f"Не похоже на GitHub-логин: {login!r}")
        ensure(login)
        remember(login)
        print(f"login {login} source set")
        return
    login, source = resolve()
    if not login:
        print("UNKNOWN — спроси GitHub-логин и запусти: python tools/whoami.py --set <логин>")
        return
    ensure(login)
    if source in ("cache", "github", "git_email"):
        remember(login)
    print(f"login {login} source {source}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # консоль Windows бывает cp1252
    sys.stderr.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
