# Lesson 3 — Arguments, Exit Codes and Strict Mode

> Module 10 · Unit 3 · Difficulty: Intermediate
> Reading time: ~25 min · Lab: [Lab 2 — build dq.sh](../labs/lab-02-build-dq-toolkit.md)
> Up next: [Lesson 4 — functions & arrays](04-functions-arrays-tests.md)

---

## 1. Positional parameters — the script's inputs

When you run `./dq.sh sales.csv`, the words after the script name
arrive as **positional parameters**:

| Variable | Meaning |
|---|---|
| `$0` | the script's own name/path |
| `$1` … `$9` | first … ninth argument |
| `${10}` | tenth (braces required from 10 up) |
| `$#` | number of arguments |
| `$@` | all arguments — as separate words when quoted `"$@"` |
| `$*` | all arguments joined (avoid; `"$@"` is the correct one) |

`shift` drops `$1` and renumbers (`$2` becomes `$1`) — the classic
way to walk through arguments one at a time. Always quoted: `"$@"`
preserves argument boundaries; `$@` unquoted re-splits on spaces.

```console
$ ./demo.sh "a b" c
$1 → a b        $# → 2        "$@" → "a b" c     (two arguments, boundary intact)
```

The `${1:-default}` from Lesson 1 is the light version of argument
handling — "use default if absent". The professional version adds an
*explicit contract* (§3).

## 2. read — asking the running script questions

`read` takes a line from stdin into a variable:

```bash
read -r -p "dataset name: " name
echo "processing $name"
```

- `-r` — no backslash mangling (same as while-read; use it always).
- `-p` — prompt text.
- `-s` — silent (passwords — though course scripts never need them).

When scripts are chained in pipelines or run unattended (M19),
prompts *hang forever* — so the course pattern is: **arguments for
anything automated; `read` only for genuinely interactive tools.**

## 3. The usage contract — validate before working

A script with unvalidated arguments fails *midway through real work*,
having made a mess. The contract: **validate first, act second.**

```bash
#!/usr/bin/env bash
# dq.sh — data-quality report for a CSV file
set -euo pipefail

usage() {
    printf 'usage: %s FILE\n' "$(basename "$0")"
    printf '       prints row count, empty-row count, duplicate check\n'
}

[[ $# -eq 1 ]] || { usage >&2; exit 64; }        # EX_USAGE
file="$1"
[[ -f "$file" ]] || { echo "error: no such file: $file" >&2; exit 66; }  # EX_NOINPUT
```

Read the guard line carefully — it's two idioms fused:
`[[ ... ]] || { ...; exit N; }` = "when the test fails, do the brace
block". Errors go to **stderr** (`>&2`) so pipelines and logs can
separate failure talk from data talk (M09). Exit codes:

| Code | Convention |
|---|---|
| 0 | success |
| 1 | general failure |
| 2 | misuse of shell builtins (bash's own) |
| 64 | usage error (BSD convention, widely adopted) |
| 66 | input missing/can't be read |
| 126/127 | not executable / command not found |

Any *distinct* non-zero code works; what matters is that the *caller*
(someone's cron job, someone's pipeline) can tell "bad usage" from
"file vanished" from "worked".

## 4. Exit codes and the caller's view

Your script's exit code is how the *world* reacts to it:

```console
$ ./dq.sh missing.csv
error: no such file: missing.csv
$ echo $?
66
```

`&&` and `||` chain on it (`./dq.sh f && ./report.sh`); cron notes it
(M19); systemd records it in the journal (M20); a *test* is nothing
but a caller asserting a code. This is why "fail loudly" is a feature:
a script that exits 0 after failing lies to every machine downstream.

## 5. Strict mode — set -euo pipefail

Two lines, placed after the shebang, that change the failure physics:

```bash
set -euo pipefail
```

- **`-e`** — *errexit*: any command failing (non-zero) aborts the
  script immediately. No more "the copy failed but the script kept
  going and deleted things based on a file that isn't there."
- **`-u`** — *nounset*: using an undefined variable is an error.
  Typos become crashes at the typo, not silent empty-string chaos
  three steps later.
- **`-o pipefail`** — a pipeline's status is the *rightmost non-zero*
  status, not just the last command's. Without it, `false | wc -l`
  succeeds — the classic way broken pipelines report success.

What `-e` does **not** catch (know the edges): commands in `if`/
`while` conditions (a failed test is *supposed* to be allowed);
commands followed by `&&`/`||` (you're explicitly handling it);
commands in pipelines *without* pipefail. So the pattern
`[[ -f "$x" ]] || exit 66` remains the way to express deliberate
failure — strict mode catches *accidents*, guards express *policy*.

```bash
set -euo pipefail                      # after the shebang, every script
readonly SCRIPT_NAME=$(basename "$0")  # -u makes typos like $SCIRPT_NAME fatal
```

**Course rule from here on: every script starts with the shebang and
`set -euo pipefail`.** Shellcheck will remind you (Lesson 5).

## 6. Logging — the script that explains itself

A script run unattended must *narrate*. The minimal contract (M24's
greppable-log standard, previewed):

```bash
readonly LOG_PREFIX="$(date -Iseconds) [dq]"

log()  { printf '%s INFO  %s\n' "$LOG_PREFIX" "$*" >&2; }
fail() { printf '%s ERROR %s\n' "$LOG_PREFIX" "$*" >&2; exit 1; }

log "checking $file"
[[ -f "$file" ]] || fail "missing input: $file"
```

- Timestamped, level-tagged, one event per line.
- To **stderr** (`>&2`) — so stdout stays pure data, pipeline-able.
- `$*` joins the function's arguments into one message.

`fail` shows the *decision function* pattern — a named, reusable
failure (Lesson 4 generalizes this into real functions).

## 7. The full skeleton — memorize this shape

```bash
#!/usr/bin/env bash
# dq.sh — one-line purpose                              # what
set -euo pipefail                                       # strict
readonly SCRIPT_NAME="$(basename "$0")"

usage()    { printf 'usage: %s FILE\n' "$SCRIPT_NAME"; }
log()      { printf '%s INFO  %s\n' "$(date -Iseconds) [$SCRIPT_NAME]" "$*" >&2; }
fail()     { printf '%s ERROR %s\n' "$(date -Iseconds) [$SCRIPT_NAME]" "$*" >&2; exit 1; }

[[ $# -eq 1 ]] || { usage >&2; exit 64; }               # contract
[[ -f "$1"   ]] || fail "input not found: $1"

log "starting"
# ... the actual work ...
log "done: $line_count rows checked"
```

Five structural elements — header comment, strict mode, usage, log/
fail pair, guards — and the work sits in the middle, confident that
inputs exist and failures speak. Every script in the labs and
Mini-Project A is this skeleton with different middles.

## 8. Try it now (15 minutes)

1. Write the skeleton as `~/lab10/skel.sh` with a trivial middle
   (`wc -l "$1"`). Test all four paths: no args (64), missing file
   (66 + your message), good file (0), and `echo $?` after each.
2. Strict-mode safari: without `set -u`, misspell a variable
   (`$filee`) and watch the silent empty string. Add `set -u`, rerun:
   the typo now names itself. That's the difference.
3. Give `skel.sh` a space-named file (`my data.csv`) — if the guards
   and tests are quoted, it just works. Un-quote one test and watch
   it burn. Restore the quote.
4. Chain it: `./skel.sh a.csv && echo GOOD || echo BAD` — your exit
   code steering someone else's logic.

## 9. Common mistakes

- `exit 0` at the end of a script that just failed — the caller is
  now confidently wrong. Let the last command's status stand, or exit
  explicitly.
- Errors printed to stdout — they vanish into pipelines; `>&2`.
- Validating *after* starting work (mkdir, downloading, writing) —
  validate first; the contract is cheap, the mess isn't.
- `set -e` as a superstition without guards — `-e` skips what you
  check, so checked guards + `-e` is the combination, not either.
- `$*` where `"$@"` is meant — argument boundaries are data.

> **Up next:** [Lesson 4 — functions & arrays](04-functions-arrays-tests.md):
> organizing growing scripts — `local`, named actions, and lists of
> things.
