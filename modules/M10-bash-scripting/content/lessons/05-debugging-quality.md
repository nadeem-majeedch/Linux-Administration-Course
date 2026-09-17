# Lesson 5 — Debugging and Quality: bash -x, bash -n, shellcheck

> Module 10 · Unit 3 · Difficulty: Intermediate
> Reading time: ~20 min · Lab: [Lab 1 — fix the bugs](../labs/lab-01-fix-the-bugs.md)
> Up next: [Mini-Project A — Dataset QC toolkit](../mini-project-a-dataset-qc-toolkit.md)

---

## 1. The debugging ladder — four rungs, cheapest first

When a script misbehaves, climb in order:

1. **Read the error verbatim.** Bash names line numbers
   (`script.sh: line 12: ...`) — most errors die at rung 1.
2. **`bash -n script.sh`** — *syntax check only*: parse, execute
   nothing. Catches unbalanced `if/fi`, `do/done`, quotes.
3. **`bash -x script.sh args`** — *trace mode*: prints every command
   after expansion, prefixed `+`, so you see what the script *actually
   ran*, not what you meant.
4. **`shellcheck script.sh`** — static analysis: finds whole *classes*
   of bugs without running (§3).

### Tracing in action

Given the bug:

```bash
filename="my data.csv"
rm -v $filename              # unquoted: TWO words
```

```console
$ bash -x cleanup.sh
+ filename='my data.csv'
+ rm -v my data.csv          # the trace SHOWS the split
rm: cannot remove 'my': No such file or directory
```

The trace output *is* the diagnosis: `rm` received two arguments
because the expansion split. **Trace-reading is the single most
valuable debugging habit**: the `+` lines show reality; compare them
to intention and the gap is the bug.

Selective tracing — heavy scripts don't need whole-run traces:

```bash
exec 2>/dev/null             # hmm, don't do this at home yet — instead:
set -x                       # start tracing HERE
./the-suspicious-part
set +x                       # stop tracing
```

And for "what is this variable *right now*":

```bash
printf 'DEBUG file=%s rows=%s\n' "$file" "$rows" >&2   # stderr: out of the data path
```

## 2. bash -n — the zero-risk syntax gate

```console
$ bash -n dq.sh
dq.sh: line 23: unexpected EOF while looking for matching `"'
```

Parses the whole script, runs nothing — safe on any file, any size.
The course habit: `bash -n` before every commit-to-canvas moment
(before `chmod +x`, before scheduling, before sharing). Cheap, silent
when clean, precise when not.

## 3. shellcheck — the quality gate

**shellcheck** is a static analyzer that knows the shell's traps by
name — including most of this module's "Common mistakes" sections.
Install (the M16 five-beat workflow):

```console
$ sudo apt install shellcheck
$ shellcheck dq.sh
```

What it catches, with the codes you'll learn to recognize:

| Code | Class | Example |
|---|---|---|
| SC2086 | unquoted expansion (word splitting) | `rm $file` |
| SC2046 | unquoted command substitution | `rows=$(wc -l < $f)` then `wc $rows` |
| SC2115 | `rm` with unquoted variable — *"Use `"${var:?}"` to ensure this never expands to empty"* — the guard that stops `rm -rf ""` | `rm -rf "$TMPDIR"` where TMPDIR unset |
| SC2155 | assignment swallowing a command's status (`local x=$(cmd)` hides failure) | `local rows=$(wc -l < f)` |
| SC2181 | checking `$?` instead of `if cmd` | `cmd; if [ $? -eq 0 ]` |
| SC2162 | `read` without `-r` | `read line` |
| SC2034 | variable set, never used (typos live here) | `filee="$file"` |

### The workflow — findings are not insults

```console
$ shellcheck dq.sh

In dq.sh line 18:
    for f in $files; do
             ^-- SC2068: Double quote array expansions to avoid
                re-splitting elements.
```

The course contract (from the roadmap, now in force): **every
submitted script passes shellcheck with zero findings.** The loop:

1. `shellcheck script.sh`
2. Read the code + the wiki link it names (each code has a page
   explaining the *why*).
3. Fix the *cause*, not the symptom — suppress only with
   justification: `# shellcheck disable=SC2086` directly above the
   line, when you can argue why splitting is wanted (rare).
4. Re-run. Repeat until silence.

The skill compounds: after a month of shellcheck, you write its
findings *before* it does — the analyzer becomes internalized style.

## 4. Script style — readable is debuggable

The conventions this course grades:

```bash
#!/usr/bin/env bash
# clean.sh — one-line purpose                        # what + why
# usage: clean.sh DIR [--ext csv]

set -euo pipefail                                    # strict, always

readonly SCRIPT_NAME="$(basename "$0")"              # constants: readonly + UPPER
readonly TARGET_EXT="${2:-csv}"

log()   { printf '%s INFO  %s\n' "$(date -Iseconds) [$SCRIPT_NAME]" "$*" >&2; }
usage() { printf 'usage: %s DIR [--ext csv]\n' "$SCRIPT_NAME" >&2; }

main() {                                            # one entry point
    local dir="${1:?usage error}"                    # :? = fail loudly if empty
    ...
}

main "$@"                                           # only call at the bottom
```

- **Header comment**: purpose + usage. Future-you is the audience.
- **`main "$@"`**: all logic in `main`, called last — definitions
  before actions, no code at top level except setup.
- **`readonly`** for constants; `UPPER_CASE` for them, `lower_case`
  for locals.
- **`${var:?message}`** — the strict-mode guard for "must be set":
  empty/unset aborts *with your message*.
- Blank lines between logical blocks; comments say *why*, not *what*.

## 5. Reusable scripts — from one-off to tool

The graduation path of a good script:

1. **One-off** — inline commands.
2. **Named script** — shebang, strict mode, `"$1"`.
3. **Parameterized** — usage function, guards, log/fail (Lesson 3).
4. **Functioned** — main entry point, helpers, arrays as config
   (Lesson 4).
5. **Reusable tool** — steps 1–4 plus: predictable exit codes, pure
   stdout data (logs to stderr), `--help`, shellcheck-clean,
   *documented in a README* (Mini-Project A's bar).

Placement makes reuse real: keep working scripts in `~/bin/` (add it
to `PATH` per [M15](../../../M15-environment-variables/README.md)) or
`~/.local/bin` (often already on it — `echo $PATH | tr ':' '\n'`).
A script in your PATH *is* a command: `dq.sh sales.csv` becomes
`dq sales.csv` — and your tooling grows by accumulation, not
rewriting.

## 6. Try it now (10 minutes)

1. Take `first.sh` from Lesson 1: run `bash -n`, then
   `shellcheck`. Fix everything it names. (If it's silent — remove
   the quotes from `"$dataset"` and let it catch you.)
2. Trace comprehension: `bash -x triage.sh 2>&1 | head -20` — follow
   three `+` lines and match each to a source line.
3. Deliberate crime: write `set -x; rm $unquoted_var; set +x` in a
   scratch script with `unquoted_var="two words.txt"`. Watch the
   trace. Feel the lesson of SC2086.
4. Promote `triage.sh` to rung 5: header, main, usage, log, PATH
   placement, shellcheck silence.

## 7. Common mistakes

- Debugging by *re-running blindly* with edits — change one thing,
  re-trace, compare. The ladder beats guess-resave-rerun loops.
- Reading shellcheck's *fix suggestions* without its *explanations*
  — the wiki page is the lesson; the fix is just this instance.
- Tracing to stdout — `bash -x` traces to stderr, and
  `bash -x script > file` mixes trace into data. Redirect trace
  separately: `bash -x script 2> trace.log`.
- `local x=$(cmd)` (SC2155) — hides a failure; split:
  `local x; x=$(cmd)`.
- A script that "works here" but not in cron/CI: almost always PATH
  (M15) or relative paths. Fix: `readonly` absolute paths, full
  command paths where it matters — M19 returns to this.

> **Next:** [Mini-Project A — Dataset QC toolkit](../mini-project-a-dataset-qc-toolkit.md)
> — the lessons become a documented, shellcheck-clean toolkit; then
> [M11](../../../M11-advanced-shell-automation/content/README.md) hardens
> it for the real world (traps, dry-runs, idempotency).
