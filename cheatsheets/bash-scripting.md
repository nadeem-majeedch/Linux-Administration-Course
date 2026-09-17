# 12 — Bash Scripting

> Learn it: [M10 — Bash Scripting](../modules/M10-bash-scripting/content/README.md) ·
> [M11 — Advanced Shell Automation](../modules/M11-advanced-shell-automation/content/README.md) ·
> Lookup, not understanding.

## Skeleton (copy this)

```bash
#!/usr/bin/env bash
# purpose: <one line>          ← why, not what
set -euo pipefail              # fail on error, unset var, pipe failure

usage() { echo "usage: $0 <dir>" >&2; exit 2; }
[ $# -eq 1 ] || usage          # fail loudly, distinct status (2 = usage)

DIR=$1
log() { printf '%s %s\n' "$(date -Is)" "$*" >&2; }   # timestamped to stderr
log "processing $DIR"
```

| Guard | Catches |
|---|---|
| `set -e` | stop on first failing command |
| `set -u` | unset variable = error (kills `rm -rf $DIR` typos) |
| `set -o pipefail` | pipeline fails if **any** stage fails, not just the last |
| `set -x` | trace mode (debugging; turn off for prod output) |

## Variables & quoting

```bash
NAME="value"            # no spaces around =
"$NAME"                 # ALWAYS double-quote expansions
"${NAME}"               # braces when concatenating
: "${DIR:?must be set}" # assert: fail loudly if unset
```

| Form | Meaning |
|---|---|
| `"…"` | expands variables, keeps spaces |
| `'…'` | **literal** — nothing expands |
| `` `…` `` | old substitution form — prefer `$( )` |
| `$(CMD)` | command substitution, nestable |
| `${VAR:-default}` | default if unset |
| `${VAR%.csv}` / `${VAR#pre-}` | strip suffix / prefix |

⚠️ Unquoted `"$VAR"` breaks on spaces: `mv "$f" done/`, never
`mv $f done/`.

## Tests & branching

| Test | True when |
|---|---|
| `[ -f F ]` / `[ -d D ]` | file / directory exists |
| `[ -r R ]` / `[ -x X ]` | readable / executable |
| `[ -z S ]` / `[ -n S ]` | empty / non-empty string |
| `[ "$a" = "$b" ]` | string equal (quote both sides) |
| `[ "$n" -eq 5 ]` | numeric (eq,ne,lt,le,gt,ge) |
| `[[ -f $f && $f == *.csv ]]` | bash-native: `&&`, `\|\|`, globs, regex `=~` |

```bash
if [ $# -eq 0 ]; then
    echo "need an argument" >&2    # errors to stderr
    exit 2
elif [ -d "$1" ]; then
    …
else
    …
fi

case "$ext" in
    csv) echo comma ;;
    tsv) echo tab ;;
    *)   echo "unknown: $ext" >&2; exit 1 ;;
esac
```

## Loops

```bash
for f in data/*.csv; do            # glob, NOT ls
    [ -e "$f" ] || continue        # guard: no-match leaves literal pattern
    process "$f"
done

for i in 1 2 3; do echo "$i"; done
for i in {1..10}; do echo "$i"; done

while read -r line; do             # -r preserves backslashes
    echo "line: $line"
done < input.txt

while true; do … ; sleep 60; done  # polling loop
```

## Functions

```bash
cleanup() {
    rm -f "$TMPFILE"                       # use with trap
}
trap cleanup EXIT                          # runs on any exit path

train() {
    local epochs=$1                        # local, always
    python train.py --epochs "$epochs"
}
train 50
```

## Arguments & exit codes

| Variable | Meaning |
|---|---|
| `$1 $2 …` | positional args |
| `$#` | count |
| `"$@"` | **all args, individually quoted** (the loopable form) |
| `$0` | script name |
| `$?` | last exit status (0 = success) |
| `$USER`/`$HOME` | environment, don't shadow them |

| Status | Convention |
|---|---|
| 0 | success |
| 1 | general failure |
| 2 | usage error (course convention) |
| 130 | killed by SIGINT (Ctrl+C) — don't fake it |

## Signals & traps

```bash
trap 'echo interrupted; exit 130' INT
trap cleanup EXIT INT TERM        # one handler for all paths
```
Use: clean temp files, kill children, mark the checkpoint.

## Debugging & hygiene

| Tool | Use |
|---|---|
| `bash -n script.sh` | syntax check, no execution |
| `bash -x script.sh` | trace every expansion |
| `shellcheck script.sh` | **static analysis — run it, then fix what it says** |
| `set -x` / `set +x` | trace a section |

Habits that are graded habits: absolute paths for cron/systemd
contexts; re-run safety (marker dirs, idempotent steps); ⚠️ no
`rm -rf` on a variable that a `set -u` check hasn't blessed; no
`cd` without `pushd`/subshell or a restore plan.
