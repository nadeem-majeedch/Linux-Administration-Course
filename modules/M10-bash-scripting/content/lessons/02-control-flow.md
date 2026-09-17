# Lesson 2 — Control Flow: if, case, and the Loops

> Module 10 · Unit 3 · Difficulty: Intermediate
> Reading time: ~25 min · Up next: [Lesson 3 — arguments & exit codes](03-arguments-exit-codes.md)

---

## 1. Exit status — the ground truth every `if` stands on

Every command ends with a number, `$?`: **0 = success, non-zero =
failure** (0 is "zero problems"). This convention — so the shell can
tell `if` "it worked" — is the foundation of all branching:

```console
$ grep -q ERROR server.log
$ echo $?
1                              # not found → failure status
$ grep -q ERROR error.log
$ echo $?
0                              # found → success
```

You rarely print `$?` by hand — you hand commands to `if`, which
reads the status for you. But knowing it demystifies everything below:
**`if` is not magic; it's an exit-status reader.**

## 2. if / elif / else — decisions

```bash
#!/usr/bin/env bash
# check_log.sh — does a log contain ERROR lines?

logfile="$1"

if grep -q "ERROR" "$logfile"; then
    echo "ERROR lines found in $logfile"
elif grep -q "WARN" "$logfile"; then
    echo "no errors, but warnings present"
else
    echo "clean: no errors or warnings"
fi
```

Structure: `if <command>; then ... elif <command>; then ... else ...
fi` — note the semicolon before `then`, and `fi` closing. The
`<command>` slot holds *any command*; `if` reacts to its exit status.
`grep -q` (quiet) is the workhorse here: search silently, report by
status.

## 3. test, [ ], [[ ]] — the comparison toolbox

Inside `if` you usually want comparisons, not raw commands. `test`
(and its alias `[`) evaluates an expression and succeeds/fails; `[[`
is bash's upgraded version. **In bash scripts, use `[[`** — it
handles unquoted-empty gracefully, supports `&&`/`||` inside, and
doesn't word-split. (`[` remains for POSIX-`sh` scripts — a fine
thing to recognize, not to write.)

**File tests — the ones you'll use weekly:**

| Test | True when |
|---|---|
| `-e "$f"` | exists (file or dir) |
| `-f "$f"` | exists and is a regular file |
| `-d "$f"` | exists and is a directory |
| `-r / -w / -x` | readable / writable / executable by *this user* |
| `-s "$f"` | exists and is non-empty |
| `"$f1" -nt "$f2"` | f1 newer than f2 (used in backup scripts) |

**String tests:**

| Test | True when |
|---|---|
| `"$a" == "$b"` | strings equal (`=` also works) |
| `"$a" != "$b"` | strings differ |
| `-z "$a"` | string is **z**ero-length (empty) |
| `-n "$a"` | string is **n**on-empty |
| `"$hay" == *"$needle"*` | glob-style pattern match (inside `[[ ]]`) |

**The cardinal rule — quote inside tests too:**

```bash
if [[ -f "$logfile" ]]; then ...     # quotes: survives spaces in paths
```

Putting it together, the most common guard in all of scripting:

```bash
if [[ ! -f "$logfile" ]]; then
    echo "error: no such file: $logfile" >&2     # errors to stderr (M09!)
    exit 1                                        # non-zero: "I failed" (Lesson 3)
fi
```

Read it aloud: *"if not-a-file, complain on stderr and stop."* This
is the shape — check, complain, exit — that turns scripts from
`mysterious error cascade` into `clear refusal`.

## 4. Numeric comparisons — inside (( )) or [[ ]]

```bash
if (( rows > 1000 )); then echo "big file"; fi
if [[ "$count" -eq 0 ]]; then echo "empty"; fi
```

Operators: `-eq -ne -lt -le -gt -ge` (equal, not-equal, less-than,
less-or-equal, greater-than, greater-or-equal). Inside `(( ))` you
may use the mathematical dialect instead: `>  <  >=  <=  ==  !=`.

## 5. case — matching many values

```bash
#!/usr/bin/env bash
# classify a file by extension

case "$filename" in
    *.csv)  echo "tabular data" ;;
    *.json) echo "structured data" ;;
    *.log|*.txt) echo "text: log or notes" ;;
    *)      echo "unknown type: $filename" ;;
esac
```

`case` matches against glob **patterns** (same wildcards as M07's
globbing: `*`, `?`, `[abc]`), tries each `pattern)` in order, runs
the first match, `;;` ends it, `*)` is the catch-all. Anywhere you'd
write an `if/elif/elif/elif` chain over *one* value, `case` is
cleaner — it's the natural shape for CLI option dispatch (M11's
`getopts` uses exactly this).

## 6. for — iterate over a known list

```bash
# over a glob (the DS workhorse: batch every CSV)
for file in *.csv; do
    printf 'checking %s\n' "$file"
    [[ -s "$file" ]] || echo "  EMPTY: $file"
done

# over explicit words
for epoch in 1 2 3 4 5; do
    echo "training epoch $epoch"
done

# over ranges
for i in {1..5}; do echo "run $i"; done
```

The glob form deserves a starring role: `for file in *.csv` is how
"do this thing to all my files" is written. Two footnotes: quote
*uses* of `"$file"` inside the loop (the glob itself must stay
unquoted to expand); and if the glob matches nothing, bash keeps the
literal `*.csv` unless you set `shopt -s nullglob` — Lesson 5's
shellcheck section returns to this.

## 7. while + read — line-by-line, the data way

```bash
#!/usr/bin/env bash
# every CSV row, one line at a time

while IFS= read -r line; do
    printf 'row: %s\n' "$line"
done < data.csv
```

Anatomy, because every token matters:
- `< data.csv` — feeds the loop from the file (no `cat |` needed).
- `IFS=` — don't trim leading/trailing whitespace from each line.
- `-r` — don't mangle backslashes.
- `read` returns failure at end-of-input — which is *exactly* what
  stops the `while`. (The while-read idiom, IFS traps, and stream
  safety are expanded in [M11](../../../M11-advanced-shell-automation/content/README.md).)

Filter as you read — the pipeline-in-a-loop shape:

```bash
while IFS= read -r line; do
    case "$line" in *ERROR*) echo "$line" ;; esac
done < server.log
```

(For *pure filtering* on big files, M08's `grep` alone is faster —
the loop earns its keep when each line needs *decisions*.)

## 8. until — while, inverted

```bash
until ping -c1 -W1 127.0.0.1 >/dev/null 2>&1; do
    echo "waiting for local stack..."; sleep 2
done
echo "up."
```

`until` runs *until* the command succeeds — `while !` spelled
politely. Rarer than `while`, ideal for wait-for-condition.

## 9. Putting it together — a deciding script

`~/lab10/triage.sh` — if/case/for in one small tool:

```bash
#!/usr/bin/env bash
# triage.sh — classify every CSV in the current directory

for file in *.csv; do
    if [[ ! -f "$file" ]]; then
        echo "no CSVs here"; exit 1
    fi
    rows=$(wc -l < "$file")
    case "$rows" in
        0)      status="EMPTY" ;;
        [1-9])  status="TINY" ;;
        *)      status="OK ($rows rows)" ;;
    esac
    printf '%-30s %s\n' "$file" "$status"
done
```

New trick: `%-30s` left-aligns the filename in 30 columns —
`printf`'s field widths turn ad-hoc output into a report.

## 10. Try it now (15 minutes)

1. Build `triage.sh`; run it in `~/lab10` with 3 CSVs of different
   sizes. Add one `*.tsv` case.
2. Write `waitfor.sh`: `until` loop that waits until a given file
   exists (`./waitfor.sh done.marker`), checking every 2 seconds,
   with a message per wait. (This is a real ops pattern — waiting
   for a job's completion marker.)
3. The empty-dir edge: run `triage.sh` in an empty directory. Which
   line catches it, and why does `[[ ! -f "$file" ]]` fire when the
   glob matched nothing? (Answer: `$file` is the literal `*.csv`.)
4. Rewrite one `case` arm from `triage.sh` as `if/elif` — feel why
   the course prefers `case` for value dispatch.

## 11. Common mistakes

- `if [ "$a" = "$b" ] && [ -f "$x" ]` in bash: works, but `[[ ]]`
  does both tests in one, cleanly: `[[ "$a" == "$b" && -f "$x" ]]`.
- Forgetting `;;` in `case` — falls through into the next pattern.
- Unquoted variables in tests: `[[ -f $file ]]` breaks on spaces.
  Quotes: always.
- `while read` without `IFS=`/`-r`: silent data mangling.
- Using `for line in $(cat file)`: word-splits *and* globs the file
  — `while IFS= read -r` is the correct idiom (a Lab 1 patient).

> **Up next:** [Lesson 3 — arguments & exit codes](03-arguments-exit-codes.md):
> scripts that take input properly and fail loudly — strict mode.
