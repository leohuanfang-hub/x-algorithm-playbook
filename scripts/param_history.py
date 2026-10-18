#!/usr/bin/env python3
"""List every change to the ranking parameters in X's open-source For You algorithm.

Reads home-mixer/params/param.rs across the git history of github.com/xai-org/x-algorithm
and prints one row per changed parameter: date, commit, parameter, old value, new value.

Usage:
  python3 scripts/param_history.py                 # clones into ./.x-algorithm (or updates it)
  python3 scripts/param_history.py --repo PATH     # use an existing clone
  python3 scripts/param_history.py --since 2026-09-01 --grep Weight
  python3 scripts/param_history.py --markdown > changes.md
"""
import argparse, os, re, subprocess, sys

PARAM_FILE = "home-mixer/params/param.rs"
PARAM_RE = re.compile(r'param!\(\s*(\w+),\s*[\w<>]+,\s*"[^"]+",\s*([^)]+?)\s*\)', re.S)

def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True).stdout

def ensure_repo(path):
    if os.path.isdir(os.path.join(path, ".git")):
        subprocess.run(["git", "-C", path, "pull", "-q", "--ff-only"], check=False)
        if os.path.exists(os.path.join(path, ".git", "shallow")):
            subprocess.run(["git", "-C", path, "fetch", "-q", "--unshallow"], check=False)
    else:
        subprocess.run(["git", "clone", "-q", "https://github.com/xai-org/x-algorithm", path], check=True)
    return path

def params_at(repo, commit):
    try:
        src = git(repo, "show", f"{commit}:{PARAM_FILE}")
    except subprocess.CalledProcessError:
        return {}
    return {m.group(1): " ".join(m.group(2).split()) for m in PARAM_RE.finditer(src)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".x-algorithm")
    ap.add_argument("--since", help="only commits on or after this date, YYYY-MM-DD")
    ap.add_argument("--grep", help="only parameters whose name contains this text")
    ap.add_argument("--markdown", action="store_true")
    a = ap.parse_args()
    repo = ensure_repo(a.repo)
    log = git(repo, "log", "--reverse", "--format=%H %cs", "--", PARAM_FILE).split("\n")
    commits = [l.split() for l in log if l.strip()]
    prev, rows = {}, []
    for sha, day in commits:
        cur = params_at(repo, sha)
        if prev and (not a.since or day >= a.since):
            for name in sorted(set(prev) | set(cur)):
                old, new = prev.get(name, "(new)"), cur.get(name, "(removed)")
                if old != new and (not a.grep or a.grep.lower() in name.lower()):
                    rows.append((day, sha[:7], name, old, new))
        prev = cur
    if a.markdown:
        print("| Date | Commit | Parameter | Old | New |\n|---|---|---|---|---|")
        for r in rows:
            print("| " + " | ".join(r) + " |")
    else:
        for r in rows:
            print(f"{r[0]}  {r[1]}  {r[2]}: {r[3]} -> {r[4]}")
    if not rows:
        print("No parameter changes found for this filter.", file=sys.stderr)

if __name__ == "__main__":
    main()
