# Lesson 2 — Pipes, Chaining & Command Substitution

> Module 09 · Unit 2 · Difficulty: Intermediate
> Reading time: ~30 min · Lab: [Lab 2 — Pipeline workshop](../labs/lab-02-pipeline-workshop.md)
> Up next: [M10 — Bash scripting](../../../M10-bash-scripting/README.md)

---

## 1. The pipe: Unix's central nervous system

A **pipe** (`|`) connects one command's stdout directly to the next command's
stdin — no intermediate files, no saving, pure flow:

```
grep ERROR job.log │  wc -l          →  42
   (finds lines)     (counts lines)
```

```console
$ grep ERROR job.log | wc -l
42
```

Philosophy, stated by Unix's authors and proven daily since: **write programs
that do one thing well; write programs to work together.** Every tool here is
mediocre alone and brilliant piped. This lesson makes you fluent at composing
them — *the* skill that makes a 5 GB log file analyzable in seconds without a
notebook ever loading it into RAM.

## 2. The filter cast (a working set)

You've met these as individuals; piped, they become an analytics toolkit:

| Command | Job | Example |
|---|---|---|
| `grep` | keep matching lines | `grep ERROR app.log` |
| `grep -v` | drop matching lines | `grep -v DEBUG app.log` |
| `sort` | sort lines | `sort names.txt` |
| `uniq -c` | collapse/count adjacent duplicates | `sort x | uniq -c` |
| `wc -l` | count lines | `... | wc -l` |
| `head`/`tail -n` | first/last N lines | `... | head -10` |
| `cut -d, -f3` | extract a field | CSV columns |
| `tr a-z A-Z` | character translate | case normalization |

**The counting idiom** — learn this shape; you'll write it weekly:

```console
$ sort access.log | uniq -c | sort -rn | head -5
 512 /api/v1/data
 308 /health
 ...
```

(*sort → uniq -c → sort -rn → head*: "count each distinct line, biggest first,
top five." `uniq` only collapses *adjacent* duplicates — that's why `sort`
always comes first. This one pipeline is a top-N analysis in four words.)

## 3. DS walk-through: a CSV pipeline, start to finish

Given `sales.csv` (columns: `order_id,customer_email,amount`), answer real
questions with pipelines:

```console
# How many rows (minus header)?
$ tail -n +2 sales.csv | wc -l

# Top 5 customers by order count:
$ tail -n +2 sales.csv | cut -d, -f2 | sort | uniq -c | sort -rn | head -5

# All unique email domains (quick-and-dirty, before M08's regexes):
$ tail -n +2 sales.csv | cut -d, -f2 | tr 'A-Z' 'a-z' | sort -u

# Revenue lines only, biggest first (numeric sort!):
$ tail -n +2 sales.csv | cut -d, -f3 | sort -rn | head -5
```

Two correctness notes that matter more than speed:

- `sort -n` for numbers, `sort` (lexicographic) for text — `sort` puts `10`
  before `9` by default. Wait, *that's wrong-looking* — exactly: lexicographic
  order compares character-by-character. `sort -rn` is the numeric fix.
- Real CSVs bite: quoted fields containing commas break naive `cut -d,`. The
  honest pipeline answers *approximate* questions fast; pandas answers exact
  ones slowly. Knowing which question you're asking is the data engineer's
  judgment call — and the reason this course teaches both layers.

## 4. Chaining commands: `;`, `&&`, `||`

Sequences, with semantics that matter:

| Operator | Reads as | Runs next command… |
|---|---|---|
| `;` | "and then" | always |
| `&&` | "and *if that succeeded*" | only if previous exit code was 0 |
| `||` | "*or if that failed*" | only if previous exit code was ≠ 0 |

```console
$ mkdir -p backups && cp data.csv backups/      # copy only if mkdir worked
$ grep ERROR job.log || echo "no errors — clean run"
$ make clean; make all                          # textbook ; usage (you'll know make soon)
```

`&&` chains are how scripts *fail fast* (M10's `set -e`-thinking in miniature):
each step is a gate. `||` is the emergency-handler hook. The M01 exit-code
lesson pays off here — the shell routes on those numbers.

## 5. Command substitution: `$(...)`

A command's *output* can become part of another command line:

```console
$ echo "Backed up at $(date +%H:%M)"
Backed up at 22:58

$ cp sales.csv "sales-$(date +%F).csv"
$ ls sales-*
sales-2026-09-15.csv
```

`$(...)` runs first; its stdout is pasted into the line; then the outer command
runs. Daily uses: timestamped filenames (backups, M11/M24), "count into a
variable" (`N=$(grep -c ERROR job.log)` — M10's variables), and
self-documenting messages. Legacy backticks `` `...` `` do the same job; modern
style is `$(...)` — it nests.

## 6. History & aliases: making your fluency compound

Two shell conveniences that turn today's pipelines into tomorrow's one-word
commands.

### History, level 2 (M01 taught the keys)

```console
$ history | tail -5
$ !497          # rerun command #497 from history
$ !!            # rerun the previous command (classic: sudo !!)
$ !grep         # rerun the most recent command STARTING with 'grep'
```

`Ctrl+R` (interactive search) remains the daily driver; `history | grep tee`
finds "that pipeline from Tuesday". History is per-session-file (`~/.bashrc`
configures size — M15).

### Aliases: names for your reflexes

```console
$ alias ll='ls -lh'
$ alias taillog='tail -f logs/job.log'
$ ll
$ unalias taillog                 # remove one
$ alias                           # list all
```

An alias is a *name* the shell expands to a command — evaluated at typing time,
before history. Two cautions: aliases live in your shell (not scripts — scripts
get functions/variables, M10); and redefining something dangerous-sounding
(`alias rm='rm -i'`) trains reliance that vanishes on any other machine — the
safety must live in your *habits*, not your dotfile (M15's debate, referenced by
M07's exercises).

## 7. Preview: feeding commands to commands

One more join to glimpse — `xargs` turns *piped text* into *arguments*:

```console
$ grep -l ERROR logs/*.log | xargs rm -i      # delete exactly the logs that contain ERROR
```

Don't adopt it yet (M09's full module covers `-I`, `-0`, `-P` and its safety
rails); see the *shape*: pipelines can build command lines, not just text.

## Exercises (lab-log.md)

1. Rebuild the counting idiom on any text file: `sort f | uniq -c | sort -rn |
   head -3`. Then break it on purpose: remove the first `sort` — explain the
   difference (adjacency!).
2. Numeric-vs-lexicographic: `printf '9\n10\n2\n' | sort` vs `| sort -rn`.
   Record both; one sentence on when each ordering is *correct*.
3. On `~/projects/eds-01/logs/job.log` (build it if needed with 6 echo lines):
   count ERROR lines with one pipeline; then list today's non-INFO lines,
   biggest-first if numeric — echo-checked into a file with `tee`.
4. Chain: `mkdir -p ~/scratch/chained && cp /etc/os-release
   ~/scratch/chained/ && ls -l ~/scratch/chained` — explain why `;` would be
   *wrong* here in the failure case.
5. Timestamp three copies: `cp /etc/os-release "os-$(date +%s).txt"` — what
   does `%s` give, and why is it collision-proof? Then build the human version
   with `+%F-%H%M`.
6. Alias lab: create `ll`, `lht` (`ls -lht`), and `countcsv` (a pipeline
   counting CSV rows in a named file — hint: aliases can't take arguments!
   What limitation do you hit? M10's functions solve it — log the discovery).
7. History archaeology: use `Ctrl+R` to re-run your longest pipeline from
   this lesson; then `history | tail -10` and annotate each line's purpose.

## Check yourself before M10

- I can compose the counting idiom and a top-N pipeline from memory.
- `;` vs `&&` vs `||`: I can predict all three given any first-command outcome.
- I use `$(date +%F)`-style substitution without thinking.
- Aliases: I know what they're for, their script-limitation, and why safety
  doesn't live in them.

## Further reading (official sources)

- bash manual: Pipelines, Lists, Command Substitution, Aliases —
  <https://www.gnu.org/software/bash/manual/>
- `man sort`, `man uniq`, `man cut`, `man tr`, `man xargs` (preview)
- M08 (next content phase) deepens grep/sed/awk — the filter cast grows again

Next: [M10 — Bash Scripting](../../../M10-bash-scripting/README.md)
