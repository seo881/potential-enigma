#!/usr/bin/env bash
# ops/sync.sh commits only the paths it is given (Divit 2026-10-15, after d5109889 swept another agent's tests/golden/run.py).
# Runs the real ops/sync.sh against throwaway repos with a local bare "origin"; never touches this repo's origin.
#   bash tests/test_sync.sh        exit 0 when every case passes
set -uo pipefail
SYNC="${SYNC:-$(cd "$(dirname "$0")/.." && pwd)/ops/sync.sh}"   # SYNC=<file> runs the cases against another version
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
fails=0; n=0
ok()  { n=$((n+1)); echo "ok   $1"; }
bad() { n=$((n+1)); fails=$((fails+1)); echo "FAIL $1"; }
check() { if eval "$2"; then ok "$1"; else bad "$1"; fi; }

export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t GIT_CONFIG_GLOBAL=/dev/null
git init -q --bare -b main "$T/origin.git"
git clone -q "$T/origin.git" "$T/a" 2>/dev/null
cd "$T/a"
mkdir -p ops tests/golden status images/form/x
cp "$SYNC" ops/sync.sh
for f in mine.txt shared.txt tests/golden/run.py status/form.json images/form/x/a.svg; do echo base > "$f"; done
git add -A && git commit -q -m base && git push -q origin HEAD:main
git clone -q "$T/origin.git" "$T/b" 2>/dev/null

# 1. other agents' work in the same clone: a modified tracked file, a staged file, an untracked file
echo "half done" >> tests/golden/run.py
echo "staged by another agent" >> shared.txt; git add shared.txt
echo new > untracked.txt
echo "my change" >> mine.txt
out="$(bash ops/sync.sh "mine" mine.txt 2>&1)"; rc=$?
check "sync exits 0" '[ $rc = 0 ]'
files="$(git show --name-only --format= HEAD)"
check "commit holds only mine.txt" '[ "$files" = mine.txt ]'
check "origin got the commit" '[ "$(git --git-dir="$T/origin.git" rev-parse main)" = "$(git rev-parse HEAD)" ]'
check "unrelated modified file still dirty, uncommitted" 'git diff --quiet -- tests/golden/run.py; [ $? = 1 ]'
check "staged file of another agent still staged, uncommitted" 'git diff --cached --name-only | grep -qx shared.txt'
check "untracked file left alone" '[ -n "$(git status --porcelain -- untracked.txt)" ]'
check "diffstat printed" 'echo "$out" | grep -q "mine.txt"'

# 2. refusals: no paths, '.', a directory, a glob, an absolute path, private/
for args in "" "." "tests" "tests/golden" "*.txt" "$T/a/mine.txt" "private/x" "nope.txt"; do
  head="$(git rev-parse HEAD)"
  if [ -z "$args" ]; then bash ops/sync.sh "x" >/dev/null 2>&1; else bash ops/sync.sh "x" "$args" >/dev/null 2>&1; fi; rc=$?
  check "refuses '${args:-<no paths>}'" '[ $rc != 0 ] && [ "$(git rev-parse HEAD)" = "$head" ]'
done

# 3. an allowlisted page folder is accepted, and only it is committed
echo v2 > images/form/x/a.svg
bash ops/sync.sh "images" images/form/x >/dev/null 2>&1; rc=$?
check "page image folder accepted" '[ $rc = 0 ] && [ "$(git show --name-only --format= HEAD)" = images/form/x/a.svg ]'

# 4. origin moved and the autostash pop collides with a dirty unrelated file: the pushed commit still holds only my path
( cd "$T/b" && git pull -q origin main && echo upstream > tests/golden/run.py && echo up >> status/form.json \
  && git commit -qam upstream && git push -q origin HEAD:main )
echo "my change 2" >> mine.txt
out="$(bash ops/sync.sh "mine 2" mine.txt 2>&1)"; rc=$?
check "sync after upstream move exits 0" '[ $rc = 0 ]'
check "rebased commit holds only mine.txt" '[ "$(git show --name-only --format= HEAD)" = mine.txt ]'
check "pushed on top of upstream" '[ "$(git --git-dir="$T/origin.git" rev-parse main)" = "$(git rev-parse HEAD)" ] && git merge-base --is-ancestor HEAD~1 HEAD && [ "$(git log -1 --format=%s HEAD~1)" = upstream ]'
check "pop conflict reported, not committed" 'echo "$out" | grep -q "tests/golden/run.py" && ! git show HEAD --format= --name-only | grep -q run.py'
# leave the tree as the other agent would after resolving: take upstream, drop the stash
git checkout -q HEAD -- tests/golden/run.py 2>/dev/null; git stash drop -q 2>/dev/null; git restore --staged -- shared.txt 2>/dev/null

# 5. conflict markers in my own file are refused
printf '<<<<<<< ours\na\n=======\nb\n>>>>>>> theirs\n' > mine.txt
head="$(git rev-parse HEAD)"
bash ops/sync.sh "markers" mine.txt >/dev/null 2>&1; rc=$?
check "conflict markers refused and unstaged" '[ $rc != 0 ] && [ "$(git rev-parse HEAD)" = "$head" ] && ! git diff --cached --name-only | grep -qx mine.txt'

echo "$((n-fails))/$n passed"; [ $fails = 0 ]
