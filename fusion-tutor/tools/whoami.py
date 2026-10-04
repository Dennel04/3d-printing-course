"""Who is studying with the tutor right now: the team member's GitHub login.

Two kinds of evidence, matched against people/*/profile.md:
  SURE  - the GitHub account on this machine (`gh api user`), git email,
          university e-mail (Windows UPN) or Windows user name;
  GUESS - the person's name (Windows full name, git user.name) resembling a
          profile name/login, or the computer name (lab PCs are shared).
A guess or conflicting evidence means the tutor MUST ask the student; with
no evidence at all it asks too. `.whoami` caches a SURE answer for this
computer + Windows user (not in git).

  python tools/whoami.py                 -> one line, see main() for the forms
  python tools/whoami.py --set LOGIN     -> the student confirmed: bind people/LOGIN/
  python tools/whoami.py --language CODE -> set my language (en, ru, et, ...), logged in the profile

This is not authentication, just protection against mix-ups among teammates:
the tutor may not run `--set` without the human's approval, and it refuses
if GitHub on this computer names a different login. Real control is push
access to the repo.
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
LANG_RE = re.compile(r"^[a-z]{2,3}(?:-[A-Za-z]{2,4})?$")
DEFAULT_LANGUAGE = "en"
SUBDIRS = ("log", "research", "models", "docs")
FIELDS = ("git_email", "email", "os_user", "name", "computer", "language")
SURE_SOURCES = ("cache", "set", "github", "git_email", "email", "os_user")
# Shared lab/guest accounts identify nobody: no os_user evidence, no cache.
GENERIC_USERS = {"student", "students", "user", "users", "guest", "admin", "administrator",
                 "lab", "labor", "pc", "kasutaja", "opilane", "tudeng"}


def sh(cmd, timeout=15):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=ROOT,
                           encoding="utf-8", errors="replace")
        return r.stdout.strip() if r.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def cache_key():
    computer = os.environ.get("COMPUTERNAME") or socket.gethostname()
    return f"{computer}|{getpass.getuser()}".lower()


def machine(slow=False):
    """What this computer says about its user. slow=True also asks Windows for
    the full name and UPN (about a second; not done inside hooks)."""
    m = {"computer": os.environ.get("COMPUTERNAME") or socket.gethostname(),
         "os_user": getpass.getuser(),
         "git_email": sh(["git", "config", "user.email"]).lower(),
         "git_name": sh(["git", "config", "user.name"]),
         "name": "", "email": ""}
    if slow and os.name == "nt":
        m["email"] = sh(["whoami", "/upn"], 10).lower()
        m["name"] = sh(["powershell", "-NoProfile", "-Command",
                        '([adsi]"WinNT://$env:USERDOMAIN/$env:USERNAME,user").FullName'], 10)
    return m


def profile_path(login):
    return os.path.join(PEOPLE, login, "profile.md")


def profile_fields(login):
    keys = {k: [] for k in FIELDS}
    p = profile_path(login)
    if os.path.isfile(p):
        for line in open(p, encoding="utf-8"):
            m = re.match(r"^- (" + "|".join(FIELDS) + r"):\s*(.+?)\s*$", line)
            if m:
                keys[m.group(1)].append(m.group(2).lower())
    return keys


def profiles():
    if not os.path.isdir(PEOPLE):
        return {}
    return {login: profile_fields(login) for login in os.listdir(PEOPLE)
            if os.path.isfile(profile_path(login))}


def language(login):
    """The student's preferred language; English until they choose another."""
    langs = profile_fields(login)["language"] if login else []
    return langs[-1] if langs and LANG_RE.match(langs[-1]) else DEFAULT_LANGUAGE


def canonical(login):
    """GitHub logins are case-insensitive: one folder per person."""
    if os.path.isdir(PEOPLE):
        for name in os.listdir(PEOPLE):
            if name.lower() == login.lower():
                return name
    return login


def tokens(text):
    return {t for t in re.split(r"[^\w]+", text.casefold()) if len(t) >= 3}


def identify(use_cache=True, network=True, slow=False):
    """{"login", "source", "sure", "evidence"}; login None if unknown or conflicting."""
    if use_cache and not generic_account():
        try:
            c = json.load(open(CACHE, encoding="utf-8"))
            if c.get("key") == cache_key() and LOGIN_RE.match(c.get("login", "")):
                return {"login": c["login"], "source": "cache", "sure": True, "evidence": {}}
        except (OSError, ValueError):
            pass
    m = machine(slow)
    profs = profiles()
    sure = {}  # source -> login
    if network:
        gh = sh(["gh", "api", "user", "--jq", ".login"])
        if LOGIN_RE.match(gh):
            sure["github"] = canonical(gh)
    for field, value in (("git_email", m["git_email"]), ("email", m["email"]),
                         ("os_user", "" if generic_account() else m["os_user"].lower())):
        if not value:
            continue
        hits = [l for l, k in profs.items()
                if value in k[field] or (field.endswith("email") and value in k["git_email"] + k["email"])]
        if len(hits) == 1:
            sure[field] = hits[0]
    logins = set(sure.values())
    if len(logins) > 1:
        return {"login": None, "source": "conflict", "sure": False, "evidence": sure}
    if logins:
        source = next(iter(sure))
        return {"login": logins.pop(), "source": source, "sure": True, "evidence": sure}

    guess = {}
    name_tokens = tokens(m["name"]) | tokens(m["git_name"]) | (set() if generic_account() else tokens(m["os_user"]))
    if name_tokens:
        hits = [l for l, k in profs.items()
                if name_tokens & (tokens(" ".join(k["name"])) | tokens(l))]
        if len(hits) == 1:
            guess["name"] = hits[0]
    hits = [l for l, k in profs.items() if m["computer"].lower() in k["computer"]]
    if len(hits) == 1:
        guess["computer"] = hits[0]
    logins = set(guess.values())
    if len(logins) == 1:
        return {"login": logins.pop(), "source": "+".join(guess), "sure": False, "evidence": guess}
    if len(logins) > 1:
        return {"login": None, "source": "conflict", "sure": False, "evidence": guess}
    return {"login": None, "source": None, "sure": False, "evidence": {}}


def resolve(network=True):
    """(login, source) for hooks; check is_sure(source) before trusting it."""
    r = identify(network=network)
    return r["login"], r["source"]


def is_sure(source):
    return source in SURE_SOURCES


def generic_account():
    return getpass.getuser().lower() in GENERIC_USERS


def remember(login):
    if generic_account():
        return
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump({"login": login, "key": cache_key()}, f)


def ensure(login, m=None, record=True):
    """Create people/<login>/ from templates. With record=True also add this
    machine's evidence to the profile: only when the identity comes from the
    GitHub account or the student confirmed it (--set). Recording on weaker
    evidence would let one person's signals leak into another's profile,
    e.g. a teammate on a PC whose git config carries someone else's email."""
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
    prof = profile_path(login)
    if not os.path.exists(prof):
        with open(prof, "w", encoding="utf-8", newline="\n") as f:
            f.write(f"# {login}\n\n"
                    f"Created {datetime.date.today().isoformat()}. The tutor recognises the student by\n"
                    "these lines (see tools/whoami.py) and speaks `language`. Lines\n"
                    "`- key: value` can be added.\n\n"
                    f"- github: {login}\n"
                    f"- language: {DEFAULT_LANGUAGE}\n")
    if not record:
        return home
    m = m or machine(slow=True)
    have = profile_fields(login)
    add = []
    for field, value in (("name", m["name"]), ("email", m["email"]), ("git_email", m["git_email"]),
                         ("os_user", "" if generic_account() else m["os_user"]), ("computer", m["computer"])):
        if value and value.lower() not in have[field]:
            add.append(f"- {field}: {value}\n")
    if add:
        lines = open(prof, encoding="utf-8").read().splitlines(keepends=True)
        at = max((i for i, l in enumerate(lines) if re.match(r"^- (github|" + "|".join(FIELDS) + "):", l)),
                 default=len(lines) - 1) + 1
        lines[at:at] = add
        with open(prof, "w", encoding="utf-8", newline="\n") as f:
            f.writelines(lines)
    return home


def set_language(login, code):
    """Replace the `- language:` line and append the change to the profile history."""
    old = language(login)
    prof = profile_path(login)
    lines = open(prof, encoding="utf-8").read().splitlines()
    lines = [l for l in lines if not re.match(r"^- language:", l)]
    at = max((i for i, l in enumerate(lines) if re.match(r"^- (github|" + "|".join(FIELDS) + "):", l)),
             default=len(lines) - 1) + 1
    lines.insert(at, f"- language: {code}")
    if "## Language history" not in lines:
        lines += ["", "## Language history", ""]
    lines.append(f"- {datetime.date.today().isoformat()}: {old} -> {code}")
    with open(prof, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    return old


def main(argv):
    if len(argv) >= 2 and argv[0] == "--set":
        login = argv[1]
        if not LOGIN_RE.match(login):
            sys.exit(f"Doesn't look like a GitHub login: {login!r}")
        gh = sh(["gh", "api", "user", "--jq", ".login"])
        if LOGIN_RE.match(gh) and gh.lower() != login.lower():
            sys.exit(f"GitHub on this computer is {gh}, not {login}. "
                     f"A different person should sign in with their own account: gh auth login")
        login = canonical(gh if LOGIN_RE.match(gh) else login)
        ensure(login)
        remember(login)
        print(f"login {login} source set sure language {language(login)}")
        return
    if len(argv) >= 2 and argv[0] == "--language":
        login, source = resolve()
        if not login or not is_sure(source):
            sys.exit("Confirm who is studying first (python tools/whoami.py), then set the language.")
        code = argv[1].lower()
        if not LANG_RE.match(code):
            sys.exit(f"Not a language code (en, ru, et, ...): {argv[1]!r}")
        old = set_language(login, code)
        print(f"login {login} language {old} -> {code}")
        return

    # Start of a lesson: fresh detection (the cache is for hooks), with the slow signals.
    m = machine(slow=True)
    r = identify(use_cache=False, slow=True)
    ev = ", ".join(f"{k}={v}" for k, v in r["evidence"].items())
    if r["sure"]:
        ensure(r["login"], m, record=r["source"] == "github")
        remember(r["login"])
        print(f"login {r['login']} source {r['source']} sure language {language(r['login'])}")
    elif r["login"]:
        print(f"GUESS {r['login']} ({ev}): ask the student \"Are you {r['login']}?\"; "
              f"if yes, run: python tools/whoami.py --set {r['login']}")
    elif r["source"] == "conflict":
        print(f"CONFLICT ({ev}): ask the student who they are (GitHub login), "
              "then run: python tools/whoami.py --set <login>")
    else:
        print("UNKNOWN: ask the student for their GitHub login, "
              "then run: python tools/whoami.py --set <login>")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # the Windows console can be cp1252
    sys.stderr.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
