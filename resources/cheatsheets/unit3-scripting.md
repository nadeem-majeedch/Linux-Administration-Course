# Cheatsheet — Unit 3: Scripting & Automation

## Script skeleton (M10)

```bash
#!/usr/bin/env bash
set -euo pipefail                 # fail on error, undefined vars, pipe breaks
FILE="${1:-}"; [ -n "$FILE" ] || { echo "usage: $0 FILE" >&2; exit 64; }
echo "$(date -Is) starting with $FILE"
```

```bash
bash -n script.sh     # syntax check without running
bash -x script.sh     # trace execution
shellcheck script.sh  # linter — fix everything it says
chmod +x script.sh    # make executable
```

## Control flow

```bash
if [[ -f "$FILE" ]]; then echo exists; fi         # -f file -d dir -z empty -n nonempty
if [[ "$A" == "$B" ]]; then ...; elif ...; fi     # numbers: (( N > 5 ))
for f in *.csv; do echo "$f"; done
while IFS= read -r line; do echo "$line"; done < input.txt
case "$opt" in start) ...;; stop) ...;; *) usage;; esac
```

**Quote every variable.** `"$VAR"` survives spaces; `$VAR` word-splits.

## Functions, arguments, exit codes

```bash
log() { echo "$(date -Is) $*" >> "$LOGFILE"; }
usage() { echo "usage: $0 [-i INT] [-n NAME] FILE"; exit 64; }
# $1..$9 args · $# count · "$@" all args, quoted · $? last exit code
getopts "i:n:h" opt && case "$opt" in
  i) INTERVAL="$OPTARG" ;;  n) NAME="$OPTARG" ;;  h) usage ;;
esac
```

Exit codes: `0` success · `1` general failure · `2/64` usage · `130` Ctrl+C.

## Automation patterns (M11)

```bash
trap 'rm -rf "$TMPDIR"' EXIT                 # cleanup on any exit
TMPDIR="$(mktemp -d)"                        # private temp dir
[ "$1" = "--dry-run" ] && { echo "DRY: would do X"; exit 0; }
cp file "file.bak-$(date +%F)"               # backup before modify
nohup ./longjob > job.log 2>&1 &             # survive terminal close
```

Idempotent = re-running is safe: check-then-create, write-temp-then-`mv`,
report instead of duplicate.
