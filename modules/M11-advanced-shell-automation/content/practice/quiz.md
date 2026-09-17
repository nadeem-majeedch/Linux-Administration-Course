# Module 11 Quiz — Advanced Shell & Automation

> 20 questions. Answer first, then check [quiz-answers.md](quiz-answers.md).
> Scope: lessons 1–3. Property questions (dry-run/idempotency/trap)
> are graded on reasoning.

## Section A — lines & streams (Q1–7)

**Q1.** What does IFS contain by default, and what does the *scoped*
form `IFS=, read -r a b c` change — and for how long?

**Q2.** In `IFS=, read -r name age rest <<< "ana,42,DS,extra,info"`:
what lands in each variable, exactly?

**Q3.** Why does `cat file | while read -r l; do n=$((n+1)); done;
echo $n` print 0 — and the two fixes?

**Q4.** What is process substitution `<(cmd)`, and name one two-file
tool it unlocks for pipelines?

**Q5.** Write the comm-based line: IDs in today.csv but not
yesterday.csv (first column, headers skipped, both unsorted).

**Q6.** What do `IFS=` and `-r` each prevent in `while IFS= read -r`?

**Q7.** When is a while-read loop the *wrong* choice vs a pure M08
pipeline?

## Section B — signals, temp, cleanup (Q8–13)

**Q8.** Which trap fires on *every* exit path — success, error,
interrupt — and why is that the right one for cleanup?

**Q9.** Why must `tmpdir=$(mktemp -d)` come *before* `trap cleanup
EXIT`, and what does `set -u` do to a trap that references a
not-yet-set variable?

**Q10.** Name three guarantees `mktemp` gives that `out.$RANDOM.tmp`
does not.

**Q11.** What filesystem property makes write-temp-then-`mv` atomic,
and what breaks it (the cross-filesystem case)?

**Q12.** In the cleanup handler, why capture `rc=$?` *first*, and
what must the handler do with it?

**Q13.** A script interrupted with Ctrl+C exits with which code —
and why does logging it matter for M19's cron use?

## Section C — dry-run, idempotency, options (Q14–20)

**Q14.** State the "one doorway" rule and the failure mode when it's
broken.

**Q15.** In dry-run, which commands still execute and which don't —
and why is running the *validations* essential to an honest preview?

**Q16.** Define idempotency in one sentence, then convert three of:
`mkdir d` / `cp a b` / `ln -s t l` / append-to-log into idempotent
forms.

**Q17.** In `while getopts ":no:h" opt`, what does the leading colon
change, what does `o:` mean, and what are the `\?` and `:` case arms
for?

**Q18.** What does `shift $((OPTIND - 1))` accomplish, and what is
`$1` afterward?

**Q19.** Interpret `OUTDIR="${ORGANIZE_OUTDIR:-./sorted}"` — including
what happens when the env var is unset vs set-but-empty.

**Q20.** Why is `source some.conf` treated as *executing* code, and
what guardrails does the course put on config sourcing?

## Bonus (Q21) — the interrupted organizer

You Ctrl+C an organizer mid-move. List, in order, the four pieces of
state you must verify afterward — and which single mechanism
(trap/mktemp/atomic-mv/dry-run) accounts for each.
