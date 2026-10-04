"""Publish a finished part into the lab, check the lab against its rules, commit it.

The tutor's only way to write files into 3d-print/labN/ (besides Edit on the
lab README, which the hook also sends to the student for approval). Every
call of `copy` and `commit` is shown to the student first: guard_writes.py
answers "ask" for them, and denies them in bypass mode, where nobody would see.

  python tools/lab.py check labN                 -> list what breaks the lab rules
  python tools/lab.py copy SRC labN/<part>/<src|stl|3mf>/<name>-vN.<ext>
  python tools/lab.py commit labN "message"      -> commit only 3d-print/labN/ + push

Rules (../AGENTS.md "Conventions", lab assignment "iga prindi kohta"):
- a source, an STL and a 3MF per printed version, in <part>/src|stl|3mf/,
  named <name>-vN.<ext>;
- nothing is overwritten or deleted: a reprint is a new version;
- assignment-EST.md is never edited;
- every lab file is mentioned in README.md, and the devlog ("Arenduspäevik")
  gets an entry for the session.
SRC must be in the student's own people/<me>/ or in shared/lab-ready/.
"""
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sync  # noqa: E402
import whoami  # noqa: E402

ROOT = whoami.ROOT
COURSE = os.path.dirname(ROOT)
LABS = os.path.join(COURSE, "3d-print")
LAB_RE = re.compile(r"^lab\d+$")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*-v\d+\.([a-z0-9]+)$")
KIND_EXT = {"src": {"f3d", "f3z", "step", "stp", "scad", "fcstd", "blend"},
            "stl": {"stl"}, "3mf": {"3mf"}}
NO_PART = {"docs", "src", "reference"}  # lab folders that are not a part


def norm(p):
    return os.path.normcase(os.path.realpath(p))


def inside(target, folder):
    folder = norm(folder)
    try:
        return os.path.commonpath([norm(target), folder]) == folder
    except ValueError:
        return False


def lab_dir(lab):
    if not LAB_RE.match(lab):
        raise RuntimeError(f"Lab must look like lab2, not {lab!r}.")
    d = os.path.join(LABS, lab)
    if not os.path.isfile(os.path.join(d, "README.md")):
        raise RuntimeError(f"3d-print/{lab}/README.md not found.")
    return d


def me():
    login, source = whoami.resolve()
    if not login or not whoami.is_sure(source):
        raise RuntimeError("The student is not confirmed: run python tools/whoami.py first.")
    return login


def copy(src, dest):
    login = me()
    src = os.path.abspath(src)
    if not os.path.isfile(src):
        raise RuntimeError(f"No such file: {src}")
    if not (inside(src, os.path.join(ROOT, "people", login))
            or inside(src, os.path.join(ROOT, "shared", "lab-ready"))):
        raise RuntimeError(f"SRC must be in people/{login}/ or shared/lab-ready/.")
    parts = dest.replace("\\", "/").split("/")
    if len(parts) != 4 or any(sync.odd_segment(s) for s in parts):
        raise RuntimeError("DEST must be labN/<part>/<src|stl|3mf>/<name>-vN.<ext>.")
    lab, part, kind, name = parts
    lab_dir(lab)
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", part) or part in NO_PART:
        raise RuntimeError(f"Part folder {part!r}: lowercase-with-dashes, one per physical part.")
    m = NAME_RE.match(name)
    if kind not in KIND_EXT or not m or m.group(1) not in KIND_EXT[kind]:
        raise RuntimeError(f"{kind}/{name}: name must be <name>-vN with "
                           f"{'/'.join(sorted(KIND_EXT.get(kind, ['src', 'stl', '3mf'])))}.")
    target = os.path.join(LABS, lab, part, kind, name)
    if os.path.exists(target):
        raise RuntimeError(f"3d-print/{dest} already exists: a reprint is a new version (-vN+1), "
                           "nothing is overwritten.")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copy2(src, target)
    print(f"Copied -> 3d-print/{dest} ({os.path.getsize(target)} bytes)")


def check(lab):
    d = lab_dir(lab)
    readme = open(os.path.join(d, "README.md"), encoding="utf-8").read()
    problems, versions = [], {}
    tracked = set(sync.git("ls-files", "--", f"3d-print/{lab}").stdout.split("\n"))
    changed = sync.git("status", "--porcelain", "--", f"3d-print/{lab}").stdout
    if any(line[3:].endswith("assignment-EST.md") for line in changed.splitlines()):
        problems.append("assignment-EST.md is changed: it is never edited.")
    for line in changed.splitlines():
        if line[:2].strip() == "D":
            problems.append(f"Deleted: {line[3:]} (nothing gets deleted).")
    for part in sorted(os.listdir(d)):
        pdir = os.path.join(d, part)
        if not os.path.isdir(pdir) or part in NO_PART or part.startswith("."):
            continue
        for kind in KIND_EXT:
            kdir = os.path.join(pdir, kind)
            for name in sorted(os.listdir(kdir)) if os.path.isdir(kdir) else []:
                if name.startswith("."):  # .gitkeep
                    continue
                rel = f"{part}/{kind}/{name}"
                m = NAME_RE.match(name)
                if not m or m.group(1) not in KIND_EXT[kind]:
                    problems.append(f"{rel}: not <name>-vN.<{'|'.join(sorted(KIND_EXT[kind]))}>.")
                    continue
                versions.setdefault((part, name.rsplit(".", 1)[0]), set()).add(kind)
                if rel not in readme and name not in readme:
                    problems.append(f"{rel}: not mentioned in README.md.")
        for f in sorted(os.listdir(pdir)):
            if os.path.isfile(os.path.join(pdir, f)):
                problems.append(f"{part}/{f}: loose file, belongs in src/ stl/ or 3mf/.")
    for (part, stem), kinds in sorted(versions.items()):
        missing = [k for k in KIND_EXT if k not in kinds]
        if missing:
            problems.append(f"{part}/{stem}: no {', '.join(missing)} "
                            "(source, STL and 3MF per print; say in README if not printed yet).")
    if "Arenduspäevik" not in readme:
        problems.append("README.md has no 'Arenduspäevik' (devlog) section.")
    new = [l[3:] for l in changed.splitlines() if l[3:] not in tracked]
    print(f"3d-print/{lab}: {len(versions)} part versions, "
          f"{len(changed.splitlines())} uncommitted changes ({len(new)} new).")
    print("\n".join("PROBLEM " + p for p in problems) or "OK: no rule broken that a script can see.")
    print("By hand: devlog entry for today (who, what, measurements with units, "
          "decisions and why, files, next), checklist ticks only for verified items, "
          "untested values stay `TODO — waiting for physical test`.")
    return not problems


def commit(lab, message):
    login = me()
    lab_dir(lab)
    path = f"3d-print/{lab}"
    sync.git("add", "--", path)
    if sync.git("diff", "--cached", "--quiet", "--", path, check=False).returncode == 0:
        print("Nothing to commit in " + path)
    else:
        sync.git("commit", "-m", f"{lab}: {message}\n\nPublished by fusion-tutor for {login}, "
                 "approved by the student.", "--", path)
    ahead = sync.git("rev-list", "@{upstream}..HEAD").stdout.split()
    allowed = [path, f"fusion-tutor/people/{login}", "fusion-tutor/shared"]
    foreign = [c for c in ahead if any(
        not any(f == p or f.startswith(p + "/") for p in allowed)
        for f in sync.git("diff-tree", "-z", "--no-commit-id", "--name-only", "-r", c)
        .stdout.split("\0") if f)]
    if foreign:
        raise RuntimeError("Unpushed commits outside this lab and your tutor folder "
                           f"({', '.join(c[:7] for c in foreign)}): push them yourself (git push).")
    if ahead and sync.git("push", check=False).returncode != 0:
        sync.pull()
        if sync.git("push", check=False).returncode != 0:
            raise RuntimeError("push failed: the commit stays local, try again later.")
    print(sync.git("log", "--oneline", "-1").stdout.strip() + (" (pushed)" if ahead else ""))


def main(argv):
    if argv[:1] == ["check"] and len(argv) == 2:
        sys.exit(0 if check(argv[1]) else 1)
    elif argv[:1] == ["copy"] and len(argv) == 3:
        copy(argv[1], argv[2])
    elif argv[:1] == ["commit"] and len(argv) >= 3:
        commit(argv[1], " ".join(argv[2:]))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    try:
        main(sys.argv[1:])
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        sys.exit(str(e))
