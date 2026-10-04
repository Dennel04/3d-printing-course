"""Tutor <-> GitHub sync: the tutor's only way into git.

Commits ONLY fusion-tutor/people/<me>/ and fusion-tutor/shared/. Other
people's folders, the labs and whatever the student keeps staged are left
alone.

  python tools/sync.py pull                -> get the team's work (rebase, autostash)
  python tools/sync.py pull --accept SHA   -> apply exactly the SHA a human reviewed
  python tools/sync.py push "message"      -> commit my paths + push

Hooks, settings and instructions (tools/, .claude/, CLAUDE.md, ...) run or
are read by the agent on every machine. So pull applies only "data" without
asking: plain files in the tutor's people/ and shared/, and lab work.
Everything else (an allowlist, not a denylist; matched the way Windows/NTFS
reads names) needs review: sync shows the files and the SHA, a human reads
the diff and runs `pull --accept SHA` themselves (the tutor may not without
approval). Exactly the reviewed SHA is applied, not whatever is on GitHub a
second later.
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
SPECIAL_MODES = {"120000", "160000"}  # symlink, submodule
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def git(*args, check=True):
    r = subprocess.run(["git", *args], cwd=COURSE, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}:\n{r.stdout}{r.stderr}".strip())
    return r


def odd_segment(s):
    """A name Windows/NTFS may read differently from git."""
    return (s != s.rstrip(". ")                       # NTFS drops trailing dots/spaces
            or any(ord(c) < 32 or c in ':\\*?"<>|' for c in s)  # ADS streams, \, control chars
            or re.search(r"~\d", s) is not None         # 8.3 short names (FUSION~1)
            or unicodedata.normalize("NFC", s) != s)


def needs_review(path, modes):
    """True if the change can run, or become an instruction for the agent."""
    raw = path.split("/")
    if modes & SPECIAL_MODES or any(odd_segment(s) for s in raw):
        return True
    parts = [unicodedata.normalize("NFKC", s).casefold() for s in raw]
    if (len(parts) == 1                                 # files at the course root
            or any(s.startswith(".") for s in parts)    # .claude, .mcp.json, .whoami, .git*
            or parts[-1] in INSTRUCTION_FILES):         # CLAUDE.md / AGENTS.md anywhere
        return True
    if parts[:2] == ["fusion-tutor", "people"] and parts[-1] == "profile.md":
        return True                                     # identity evidence, see whoami.py
    if parts[0] == "fusion-tutor" or not raw[0].isascii():
        return not (len(parts) >= 3 and raw[0].isascii() and raw[1].isascii()
                    and parts[1] in ("people", "shared"))
    return False


def incoming(target):
    """Paths target changes relative to its merge base with HEAD, with file modes."""
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
            raise RuntimeError("--accept needs the full SHA printed by sync.py pull.")
        if git("merge-base", "--is-ancestor", accept, upstream, check=False).returncode != 0:
            raise RuntimeError(f"{accept[:7]} is not in the GitHub history: check the SHA.")
        target = accept
    gated = sorted(p for p, m in incoming(target).items() if needs_review(p, m))
    if gated and accept is None:
        raise RuntimeError(
            "Hooks/settings/instructions changed on GitHub; not applying them without review:\n  "
            # names from other people's commits: escaped only, never inside a command
            + "\n  ".join(json.dumps(p, ensure_ascii=False) for p in gated)
            + f"\n\nReview: git diff HEAD...{target}"
            + f"\nIf it all looks fine: python tools/sync.py pull --accept {target}")
    r = git("rebase", "--autostash", target, check=False)  # exactly the reviewed commit
    if r.returncode != 0:
        git("rebase", "--abort", check=False)
        raise RuntimeError("pull failed (conflict?), nothing changed:\n" + r.stdout + r.stderr)


def push(message):
    login, _ = whoami.resolve()
    if not login:
        sys.exit("Don't know who is studying: run python tools/whoami.py first")
    paths = [f"fusion-tutor/people/{login}", "fusion-tutor/shared"]
    paths = [p for p in paths if os.path.exists(os.path.join(COURSE, p))]
    git("add", "--", *paths)
    if git("diff", "--cached", "--quiet", "--", *paths, check=False).returncode != 0:
        git("commit", "-m", f"tutor({login}): {message}", "--", *paths)
    # Unpushed commits (incl. from an earlier failed push) go out only if they
    # are all the tutor's: the student pushes their own commits themselves.
    ahead = git("rev-list", "@{upstream}..HEAD").stdout.split()
    if not ahead:
        print("Nothing to push.")
        return
    foreign = [c for c in ahead if any(
        not any(f == p or f.startswith(p + "/") for p in paths)
        for f in git("diff-tree", "-z", "--no-commit-id", "--name-only", "-r", c).stdout.split("\0") if f)]
    if foreign:
        raise RuntimeError("There are unpushed commits that are not the tutor's "
                           f"({', '.join(c[:7] for c in foreign)}): the student pushes those "
                           "(git push). The tutor's commit is kept locally.")
    for attempt in (1, 2):
        if git("push", check=False).returncode == 0:
            print(f"Pushed: {git('log', '--oneline', '-1').stdout.strip()}")
            return
        pull()
    raise RuntimeError("push failed: the commit stays local, try again later.")


def main(argv):
    if argv[:1] == ["pull"]:
        if argv[1:2] == ["--accept"] and len(argv) == 3:
            pull(accept=argv[2])
        elif len(argv) == 1:
            pull()
        else:
            sys.exit(__doc__)
        print("Up to date.")
    elif argv[:1] == ["push"] and len(argv) >= 2:
        push(" ".join(argv[1:]))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # the Windows console can be cp1252
    sys.stderr.reconfigure(encoding="utf-8")
    try:
        main(sys.argv[1:])
    except RuntimeError as e:
        sys.exit(str(e))
