# Module 11 Quiz — Answer Key

> Reasoning graded; command answers on "would it work if typed".

## Section A — lines & streams

**A1.** Space, tab, newline. The scoped form changes splitting to
comma **for that one `read` command only** — the shell's global IFS
is untouched afterward. (Contrast: a bare `IFS=','` assignment
poisons everything downstream.)

**A2.** `name=ana`, `age=42`, `rest=DS,extra,info` — the last
variable absorbs the remainder *with separators intact* (fields
containing commas survive in `rest`).

**A3.** The pipe runs the loop in a **subshell** — `n` is incremented
in a copy that vanishes at `done`. Fixes: feed via redirection
(`done < file`), or use process substitution (`while ...; done <
<(cat file)`) which keeps the loop in the current shell.

**A4.** Runs a command and exposes its output as a **file path**
(`/dev/fd/...`) without a temp file. Unlocks two-file tools over
live pipelines: `comm`, `diff`, `join` — e.g.
`comm -23 <(sort a) <(sort b)`.

**A5.**
```bash
comm -23 <(cut -d, -f1 today.csv | tail -n +2 | sort) \
         <(cut -d, -f1 yesterday.csv | tail -n +2 | sort)
```

**A6.** `IFS=`: don't strip leading/trailing whitespace (split on
nothing). `-r`: raw — don't interpret backslashes. Together: the
line arrives verbatim.

**A7.** When the per-line action is *pure filtering/counting* — grep/
awk/sort do it faster and shorter. The loop wins when each line needs
bash state, decisions, or function calls (or the file is being
streamed alongside bash variables, as in reconcile logic).

## Section B — signals, temp, cleanup

**B8.** `trap ... EXIT`. It fires on success, error (`set -e`),
interrupt (INT), and TERM alike — one handler, no path forgotten.
(INT/TERM traps add message-specific behavior, but EXIT is the
guarantee.)

**B9.** The handler references `tmpdir`; defining it first means the
trap never sees an unset variable. Under `set -u`, an unset reference
*inside the cleanup* crashes the cleanup itself — debris plus a
confusing new error at the worst moment.

**B10.** (1) The file is **created atomically** at that exact name —
no create-race; (2) the name is **unpredictable** — no
symlink-attack prediction on shared machines; (3) **no collision**
with any concurrent run. `$RANDOM` gives none of these.

**B11.** `mv` within one filesystem is a **rename(2)** — an instant
metadata operation that atomically replaces the destination. Across
filesystems, `mv` degrades to copy+delete — a window where the
destination is partial. Hence `mktemp --tmpdir="$(dirname "$target")"`.

**B12.** `$?` is overwritten by the *first command in the handler* —
the original exit status must be stashed before anything else runs,
and **re-emitted** (`exit "$rc"`) so the caller still sees the true
code.

**B13.** 130 (128 + SIGINT's 2). Logged, it tells a cron/syslog
reader *how* the run ended — distinguishing "crashed with an error"
(rc=66) from "a human stopped it" (130) — which M24's incident
method treats as different diagnoses.

## Section C — dry-run, idempotency, options

**C14.** Every modifying command passes through one function
(`run()`). If any `mv`/`rm`/`cp` bypasses it, the dry-run *lies* —
it reports a plan while real changes happen (or reports nothing
while nothing would have happened). The pattern's value is exactly
its non-lyingness.

**C15.** Reads, validations, guards: **run**. Modifying commands:
**narrate** (`[dry-run]` to stderr). Validations must run because a
dry-run that doesn't validate previews *nothing* — "it would have
worked" must be earned by actually checking inputs.

**C16.** Running it again (once or many times) produces no further
change and exits successfully. Conversions: `mkdir -p d`; `cp -n a b`
(or `[[ -e b ]] || cp a b`); `ln -sfn t l`; write-fresh-temp +
atomic `mv` instead of `>>` appends.

**C17.** The leading `:` enables **silent error mode** — bash doesn't
print its own error messages, your `case` arms handle them. `o:`:
option `-o` **takes an argument** (arrives as `$OPTARG`). `\?`:
unknown option; `:` (case arm): option missing its argument — both
exit 64 with usage.

**C18.** Removes the parsed options from the argument list. `$1`
becomes the **first non-option operand** (e.g. the directory).

**C19.** If `ORGANIZE_OUTDIR` is set-and-non-empty, use it;
otherwise default `./sorted`. Set-but-**empty** also falls to the
default (`:-` treats empty as unset; the `:-`→`-` variant would
accept empty). Env-overridable, default-backed configuration.

**C20.** `source` runs the file **in the current shell** — every
line executes with your script's full powers (assignments, commands,
rm). Guardrails: source only files you authored/audited; document
which variables it may set; prefer env-var config for simple cases.

## Bonus (Q21) — model answer

1. **No half-written outputs** — atomic `mv` (temp-beside-target)
   means the destination is old or new, never partial.
2. **No temp debris** — `trap cleanup EXIT` fired even on INT,
   removing the mktemp scratch.
3. **True exit code recorded** — the handler's `rc=$?` stash →
   logged as 130, not lost.
4. **A trustworthy re-run plan** — dry-run now shows exactly what
   remains (idempotency means the re-run completes only the
   unfinished parts).

## Score guide

| Score | Meaning |
|---|---|
| 18–21 | Tool-builder — the final challenge is yours |
| 14–17 | Re-read the flagged sections; redo the interrupt drill |
| < 14 | Repeat lessons 2–3; graceful death is the module's core skill |
