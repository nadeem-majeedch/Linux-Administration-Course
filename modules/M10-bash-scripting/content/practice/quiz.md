# Module 10 Quiz — Bash Scripting

> 22 questions. Answer first, then check [quiz-answers.md](quiz-answers.md).
> Scope: lessons 1–5. Several questions show code — predict before
> reading the answers.

## Section A — foundations (Q1–6)

**Q1.** What does the shebang line do, and why is
`#!/usr/bin/env bash` preferred over `#!/bin/bash` in course scripts?

**Q2.** `count = 5` in a script produces `count: command not found`.
Why — and what is bash actually trying to do?

**Q3.** For `name="my report.csv"`, what does `cp $name backup/` do
*exactly* (argument by argument), and what one change fixes it?

**Q4.** Single vs double quotes: give one line where the choice
changes the output, and state which form expands `$(date +%F)`.

**Q5.** What does `rows=$(wc -l < file.csv)` store, and why the `<`
instead of `wc -l file.csv`?

**Q6.** When is `printf` preferable to `echo` in scripts? Give two
concrete reasons.

## Section B — control flow (Q7–12)

**Q7.** What is `$?` after a successful command, and what does `if`
actually read from the command it guards?

**Q8.** Name three file tests (with letters) and their meanings; then
the string test for "variable is empty".

**Q9.** Why does the course use `[[ ]]` in bash scripts instead of
`[ ]`? Two reasons.

**Q10.** Convert this `if/elif` chain to a `case`:
`if [[ "$ext" == csv ]]; then ... elif [[ "$ext" == tsv ]]; then ...
else ... fi`

**Q11.** In `for f in *.csv; do ...; done`, what does `f` contain if
the directory has no CSVs — and which two mechanisms handle that
gracefully?

**Q12.** In `while IFS= read -r line; do ... done < data.csv`, what do
`IFS=` and `-r` each prevent, and what ends the loop?

## Section C — arguments, exit codes, strict mode (Q13–18)

**Q13.** Script runs as `./dq.sh a.csv b.csv`: state `$0`, `$1`, `$#`,
and the correct way to pass all arguments onward to another command.

**Q14.** Write the guard line: exactly one argument or die with usage
and exit 64.

**Q15.** Why must error messages go to stderr (`>&2`) in a tool whose
stdout is data?

**Q16.** Explain each of `set -e`, `set -u`, `set -o pipefail` in one
sentence, and name the failure each one turns from "silent" to "loud".

**Q17.** Under `set -e`, which of these still runs to completion, and
why? (a) `[[ -f "$x" ]] || exit 66` (b) `grep -q pat missing.log` (c)
`false | wc -l` with pipefail off

**Q18.** What exit code should `./tool.sh` return when the input file
is unreadable — and what does 0 mean to a caller?

## Section D — functions, arrays, quality (Q19–22)

**Q19.** What does `local` do in a function, and what bug class
appears without it?

**Q20.** For `arr=(a "b c" d)`: how do you print the element count,
the second element, and iterate all elements *safely*?

**Q21.** `(( count-- ))` under `set -e` kills the script when count
goes from 1 to 0. Why — and the two standard fixes?

**Q22.** What do `bash -n` and `bash -x` each do, and which shellcheck
code class guards the "unquoted rm variable" bug the course treats as
the lab's most important?

## Bonus (Q23) — read the trace

```console
$ bash -x buggy.sh
+ filename='my data.csv'
+ rm -v my data.csv
rm: cannot remove 'my': No such file or directory
```

In two sentences: what is the bug, and which character in the trace
*proves* it?
