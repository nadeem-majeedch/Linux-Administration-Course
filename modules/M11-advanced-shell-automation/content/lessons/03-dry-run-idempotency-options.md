# Lesson 3 — Dry-Run, Idempotency and Real Options

> Module 11 · Unit 3 · Difficulty: Intermediate
> Reading time: ~25 min · Lab: [Lab 2 — the final scripting challenge](../labs/lab-02-final-scripting-challenge.md)
> Up next: [Unit 4 — permissions](../../../M12-users-groups-permissions/README.md)
> (M10/M11 content thread closes with Mini-Project A hardening)

---

## 1. Three properties of scripts you can trust

M10 made scripts *work*. This lesson makes them **safe to re-run**
(idempotency), **safe to preview** (dry-run), and **safe to hand
over** (proper options and config). Those three — plus Lesson 2's
graceful death — are the difference between a script you run
yourself, carefully, and a script that lives in a team's toolbox or
on cron (M19) or in a container (M28).

## 2. The dry-run pattern — show, don't do

Every script that *modifies* anything gets `--dry-run` (or `-n`):
execute nothing, narrate everything. The implementation is one
decision function away:

```bash
#!/usr/bin/env bash
set -euo pipefail

DRY_RUN=false
run() {
    # single doorway through which every modifying command passes
    if [[ "$DRY_RUN" == true ]]; then
        printf '[dry-run] %s\n' "$*" >&2
    else
        "$@"
    fi
}

run mkdir -p "$HOME/lab11/demo"
run mv -- "$src" "$dst"
```

Design rules that make it honest:

- **One doorway.** All modifying commands go through `run()`. If a
  `mv` sneaks in raw, the dry-run lies — the pattern's whole value
  is that it *can't* lie when the doorway is single.
- **Everything else still runs.** Validation, guards, log lines —
  a dry-run that skips checking is a preview of nothing.
- **`[dry-run]` lines go to stderr** — narration, not data.
- The dry-run output should read like a plan:

```console
$ ./organize.sh --dry-run ~/incoming
[dry-run] mkdir -p /home/ds/lab11/processed
[dry-run] mv -- /home/ds/lab11/incoming/processed_sales.csv /home/ds/lab11/processed/sales.csv
2 actions planned; re-run without --dry-run to execute
```

Roadmap note: the same idea reappears in M16 as `apt install --dry-run`
and in M23 as `rsync -n` — the pattern is universal because the fear
is universal: *bulk modification without preview*.

## 3. Idempotency — safe to run twice (and by two people)

**Idempotent:** running it again changes nothing further. The
organizational payoff: cron can fire hourly, a teammate can re-run
after a failure, a half-finished run can just be re-run — no special
"undo first" dance.

The transformations, before/after:

| Naive | Idempotent |
|---|---|
| `mkdir $d` (fails on re-run) | `mkdir -p $d` (succeeds either way) |
| `cp a b` (overwrites) | `cp -n a b` or `[[ -e b ]] \|\| cp a b` (never clobbers) |
| `ln -s target link` (fails on re-run) | `ln -sfn target link` |
| append `>> log` per run (grows forever) | write fresh temp + atomic `mv` (Lesson 2) |
| `mv $f done/` | `mv -n` + guard, or skip-if-already-there |

The general shape — **check, then act, and make the check cheap**:

```bash
if [[ -e "$dst" ]]; then
    log "skip (exists): $dst"
else
    run mv -- "$src" "$dst"
fi
```

Idempotency is also *self-healing*: re-running after a partial
failure completes the remaining work instead of erroring from the
top. That's why the roadmap has M19 (scheduling) require it: a
script that's safe to re-run is a script cron can be trusted with.

## 4. getopts — real command-line options

`if [[ "$1" == --dry-run ]]` works for one flag and degrades
immediately for two. `getopts` is bash's built-in parser for the
real thing:

```bash
#!/usr/bin/env bash
set -euo pipefail

usage() {
    printf 'usage: %s [-n] [-o OUTDIR] DIR\n' "$(basename "$0")"
    printf '  -n        dry-run (show actions, do nothing)\n'
    printf '  -o OUTDIR organize into OUTDIR (default: ./sorted)\n'
    printf '  -h        this help\n'
}

dry=false; outdir="./sorted"
while getopts ":no:h" opt; do
    case "$opt" in
        n) dry=true ;;
        o) outdir="$OPTARG" ;;
        h) usage; exit 0 ;;
        \?) echo "unknown option: -$OPTARG" >&2; usage >&2; exit 64 ;;
        :) echo "option -$OPTARG needs an argument" >&2; exit 64 ;;
    esac
done
shift $((OPTIND - 1))          # drop parsed options; $1 is now the first operand

[[ $# -eq 1 ]] || { usage >&2; exit 64; }
echo "dir=$1 outdir=$outdir dry=$dry" >&2
```

Reading it: the `":no:h"` **optstring** — leading `:` = *silent
error mode* (you handle errors), `n`/`h` are flags, `o:` takes an
argument (delivered in `$OPTARG`). The `case` is M10's dispatch
pattern, repurposed. `shift $((OPTIND - 1))` is the standard line
that leaves operands in `$@`. The two error cases — unknown option
(`\?`) and missing argument (`:`) — both exit 64 with usage.

Convention note: long options (`--dry-run`) have no bash-native
parser; course tools accept a *manual* long-form alias (`--dry-run) |
dry=true ;;` in a case over `"$1"` — shown in Lab 1) or simply
document the short form. Handle `--` (end of options) explicitly
when operands might start with `-`.

## 5. Configuration — variables over hardcoding

The last hardcoding in a script is the bug you find at 2 AM. The
course pattern — *defaults, overridable by environment*:

```bash
readonly DEFAULT_OUTDIR="./sorted"
OUTDIR="${ORGANIZE_OUTDIR:-$DEFAULT_OUTDIR}"     # env wins, default catches
THRESHOLD="${ORGANIZE_WARN:-80}"
```

Read like [M15's](../../../M15-environment-variables/README.md) rules
with a purpose: `${VAR:-default}` (use if set-and-non-empty), no
bare expansions (strict mode), `UPPER_CASE` for exported config,
`readonly` for values the script won't change. A config *file* —
`source ./organize.conf` with assignments inside — is fine for
multi-tool setups, with two guardrails: source only files you wrote
(sourcing executes!), and document every variable the file may set.

## 6. The reusable-tool checklist

Lesson 5 of M10 listed the rung-5 path; here is the final checklist
— Lab 2's grading rubric in miniature:

- [ ] shebang + `set -euo pipefail` + header (purpose, usage)
- [ ] guards first: usage (64), inputs (66), overwrites (2)
- [ ] `log`/`fail` on stderr; data on stdout only
- [ ] `run()` doorway + `--dry-run` (if it modifies anything)
- [ ] idempotent by construction (mkdir -p, -n flags, exists-guards)
- [ ] mktemp + trap cleanup; atomic promotion for outputs
- [ ] getopts with usage and silent-error handling
- [ ] env-overridable config, no magic numbers
- [ ] `bash -n` + `shellcheck` silent
- [ ] self-test or demonstrated transcript, both failure and
      interrupt paths

Ten lines, every one traceable to a lesson. Scripts meeting it are
ready for M19's cron, M24's health checks, and the capstone's
deployment — because they're ready for *other people*.

## 7. Try it now (15 minutes)

1. Retro-fit: take M10's `organize_datasets.sh` and add the `run()`
   doorway + `--dry-run`. Preview, then execute, then **run the
   real pass twice** — second run should be all `skip (exists)`
   lines. That's idempotency, demonstrated.
2. getopts drill: add `-v` (verbose) and `-o OUT` to the same
   script; test unknown-option and missing-argument paths (both
   exit 64).
3. Config: replace a hardcoded path with `ORGANIZE_OUTDIR`-
   overridable; show both default and overridden runs.
4. Read a dry-run you didn't write: `apt install -s hello`
   (M16's preview flag) and compare its narration style to your
   `run()` lines — same pattern, professional grade.

## 8. Common mistakes

- A second raw `mv` outside the `run()` doorway — the dry-run now
  lies. Audit: `grep -n "mv\|rm\|cp" script.sh` — every hit through
  `run` or guarded.
- Idempotency by *crash*: `mkdir $d` without `-p` "prevents" reruns
  by failing — loud, not safe. Choose the `-p` path.
- getopts optstring without the leading `:` — bash prints its own
  errors, *then* your case runs: double messaging.
- `--dry-run` skipping validation — a preview that validates
  nothing previews nothing.
- Sourcing untrusted config files — `source` is execution; treat
  configs like scripts.

> **Next:** [Lab 2 — the final scripting
> challenge](../labs/lab-02-final-scripting-challenge.md) assembles
> all three properties into one tool; then [Mini-Project A
> hardening](../mini-project-a-hardening.md) closes the scripting
> thread and hands off to Unit 4's permissions.
