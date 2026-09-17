# Lesson 1 — First Scripts: Variables, Quoting, Substitution

> Module 10 · Unit 3 · Difficulty: Intermediate (but Lesson 1 assumes
> you've never scripted)
> Reading time: ~25 min · Lab: [Lab 2](../labs/lab-02-build-dq-toolkit.md)
> Up next: [Lesson 2 — control flow](02-control-flow.md)

---

## 1. What a script is

A Bash script is a **text file of commands, run top to bottom**, by
bash — the same shell you've been typing into since
[M05](../../../M05-terminal-and-shell/README.md). Everything you can type
interactively, a script can do; the differences are that a script

- is *repeatable* (same input → same actions, no typos),
- is *nameable* (a pipeline with 14 stages becomes `dq.sh`),
- and can *make decisions* (lessons 2–4).

That trio — repeatable, nameable, decision-capable — is exactly what
turns weekly data chores into automations.

## 2. The shebang — first line, not optional

```bash
#!/usr/bin/env bash
```

When a file is executed, the kernel asks the first line, starting
`#!` (**shebang**), *which interpreter should run this file*. `env`
finds `bash` on your `PATH` — the portable form; hardcoding
`#!/bin/bash` works on Ubuntu but breaks on systems where bash lives
elsewhere (BSDs, some containers). A script without a shebang run as
`./script.sh` may be executed by `sh` — a *different, older shell* —
and fail in maddeningly subtle ways. **Every script you write in this
course starts with this exact line.**

Two ways to run:

```console
$ bash script.sh        # explicit: bash reads it (shebang ignored)
$ ./script.sh           # needs chmod +x, then the shebang rules
$ chmod +x script.sh    # one-time: the executable bit (M12 formalizes this)
```

## 3. Variables — assignment and use

```bash
#!/usr/bin/env bash
dataset="sales_2026.csv"        # assign: name=value, NO spaces around =
row_count=42
echo "processing $dataset"      # use: $name or better, "${name}"
```

Three rules that prevent 80% of beginner bugs:

1. **No spaces around `=`.** `dataset = "x"` runs the command
   `dataset` with arguments — not an assignment.
2. **Quote every use: `"$var"`** — reasons in §4.
3. **Names** are letters, digits, underscores, not starting with a
   digit. Values may be anything.

Variable values are **strings** — even `row_count=42` is the string
"42" (arithmetic is Lesson 4's `(( ))`). And casing convention:
`lowercase` for script-local names; `UPPERCASE` only for exported
environment variables (`PATH`, `HOME`) — mirroring the env-var rules
from [M15](../../../M15-environment-variables/README.md).

## 4. Quoting — the load-bearing rule of shell

The shell, before running any command, performs **word splitting**:
unquoted text is chopped on whitespace. Quoting is how you opt out:

```bash
name="report final.csv"

cp $name backup/          # DANGER: runs cp report final.csv backup/
                          #   → two arguments: "report" and "final.csv"
cp "$name" backup/        # correct: ONE argument: "report final.csv"
```

The two quote characters behave differently:

| | Single `'...'` | Double `"..."` |
|---|---|---|
| Variables expanded? | no — literal `$name` | **yes** |
| Backticks/`$(...)` run? | no | yes |
| Use when | text is literal, has `$` or `!` | text contains a variable |

```bash
echo 'cost: $100'          # cost: $100        (literal)
echo "file: $name"         # file: report final.csv
echo "sum: $(wc -l < "$name")"   # command substitution, §5
```

**Course rule:** double-quote *every* variable expansion, everywhere,
always — `"$var"`, `"${var}"`. Shellcheck flags every bare `$var` for
exactly this reason. The braces `${}` form is required when the
variable name bumps into other text: `"${name}.bak"`, not `"$name.bak"`
(which looks for a variable called `name.bak`).

## 5. Command substitution — capture output

```bash
today=$(date +%F)              # 2026-09-15
rows=$(wc -l < sales.csv)      # note: < redirects, so no filename in the count
echo "file has $rows rows"
```

`$(...)` **runs a command and yields its output as a string** — the
single most important bridge from [M09's
pipelines](../../../M09-pipes-and-redirection/README.md) into
scripts: any pipeline you've built can now be *captured* and *labeled*:

```bash
error_count=$(grep -c ERROR server.log)
echo "errors found: ${error_count}"     # the pipeline gets a name
```

The old backtick form `` `command` `` does the same, badly (no
nesting, mangling of backslashes). Use `$(...)`.

## 6. echo vs printf — and why printf wins for scripts

```bash
echo "total: $total"            # fine for quick lines...
printf 'total: %s\n' "$total"   # ...printf for anything real
```

- `printf` takes a **format string** and arguments — `%s` string,
  `%d` integer — and **no trailing newline unless you write `\n`**.
- `echo`'s behavior with `-e`, `-n`, backslashes varies across
  shells/`/bin/sh` — a portability trap.

The script habit: `printf` when output format matters (reports, logs,
CSV lines), `echo` for interactive chit-chat:

```bash
printf 'name,size\n'                       # CSV header
printf '%s,%d\n' "$filename" "$rows"       # CSV row — format is explicit
```

## 7. A first real script — assemble the pieces

`~/lab10/first.sh` — every concept of this lesson in nine lines:

```bash
#!/usr/bin/env bash
# first.sh — greet a dataset and count its rows

dataset="${1:-sales_2026.csv}"        # first argument, or the default
line_count=$(wc -l < "$dataset")      # capture a pipeline's output

printf 'dataset : %s\n' "$dataset"
printf 'rows    : %d\n' "$line_count"
printf 'checked : %s\n' "$(date -Iseconds)"
```

Run it:

```console
$ mkdir -p ~/lab10 && cd ~/lab10
$ cp ~/datasets/sales_2026.csv .   # or any CSV you have from M08
$ chmod +x first.sh
$ ./first.sh
dataset : sales_2026.csv
rows    : 1201
checked : 2026-09-15T21:04:11+00:00
```

Line by line: the shebang (§2); a comment (scripts are read by humans
first); `${1:-default}` — "first argument, or default if absent"
(Lesson 3 expands this); quoted command substitution; `printf` with
explicit formats. The `~` and `PATH` environment variables you met in
[M15](../../../M15-environment-variables/README.md) are readable here
too: `echo "$HOME"`, `echo "$PATH"` — scripts live in the same
environment as your shell.

## 8. Try it now (10 minutes)

1. Write `first.sh` above and run it on two different CSVs — no
   edits, just arguments. That's *reusability*, the point of §1.
2. Break it on purpose: remove the quotes from `"$dataset"` in the
   `wc` line, create `my data.csv` (with a space), and run again.
   Read the error. This bug is Lab 1's first patient.
3. `echo "$SHELL $HOME"` vs `echo '$SHELL $HOME'` — predict before
   running.
4. Capture in one variable: `csv_count=$(ls *.csv | wc -l)` — the
   M09 pipeline, named.

## 9. Common mistakes

- Spaces around `=` in assignments.
- Unquoted variables — breaks on spaces, glob characters (`*`),
  empty values (word disappears entirely).
- Forgetting the shebang, then wondering why `[[` fails (sh ran it).
- `$(date +%F)` inside single quotes — quotes are not decoration;
  single quotes *prevent* substitution.
- Reading `$1` with no default and no check — Lesson 3's strict mode
  makes that a crash instead of a mystery.

> **Up next:** [Lesson 2 — control flow](02-control-flow.md): scripts
> that decide — `if`, tests, `case`, and the three loops.
