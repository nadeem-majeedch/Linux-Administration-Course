# Midterm Examination — Units 1–3 (M01–M13)

> **Format:** 2 hours · closed book · 100 points.
> A computer is provided with a *fresh* Ubuntu VM snapshot; Section C
> is performed live on it and graded on the terminal transcript you
> export (`script midterm.log` — start it first).
> **Coverage:** M01–M13 (fundamentals → permissions). Everything
> tested was taught in a lab, a quiz, or a challenge — but no question
> is a copy of one. Key: [midterm-key.md](midterm-key.md).

## Section A — Reasoning (30 pts, 10 × 3)

Answer in complete sentences; "because it's Linux" is worth zero.

**A1.** A classmate says: "I'll do the whole course on my *host*
Windows machine with Git Bash." Name the two course requirements this
environment cannot deliver at all, and the one it can only partially
deliver.

**A2.** `mkdir -p a/b/c` vs three nested `mkdir` calls vs `mkdir
a a/b a/b/c`: state the one behavioral difference that matters in a
script, and why `-p` is the *idempotent* form.

**A3.** Why does `rm -rf $DIR` with an unset `$DIR` not fail — and
what does it do? Write the two-character addition that makes this
class of bug fail loudly.

**A4.** `ls -l` shows a file of size 1 byte; `du` reports 4 KiB for
it. Both are "true". Explain what each measures.

**A5.** You `mv ~/data/big.csv /mnt/usb/`. The terminal hangs longer
than for any previous `mv` in the course. Explain what `mv` is
actually doing this time and why the earlier ones were instant.

**A6.** Wildcards: explain precisely why `rm *.csv` is dangerous in a
directory that also contains `important_notes.csv`, and write the
safer form taught in the labs that *forces you to look before
deleting*.

**A7.** After `umask 077`, a newly created shared script is unusable
by teammates. Decode 077 into resulting modes for files and
directories, and state the trade-off this umask expresses.

**A8.** Why is `chmod 777` *never* the fix for "teammate can't
execute my script"? Give the correct minimal mode and the ownership
precondition it depends on.

**A9.** A hard link and a copy of the same file are both "the file,
twice". Give one terminal observation that distinguishes them, and
one operation after which their contents *differ*.

**A10.** Root can read any file regardless of mode bits, yet the
course still insists on correct permissions for root-owned files.
Give the strongest operational reason (think: non-root *services*,
not people).

## Section B — Trace the output (30 pts, 6 × 5)

For each snippet, write the exact output (or the error) and one
sentence explaining the decisive mechanism. Assume a fresh shell,
umask 0022, in an empty scratch directory unless stated.

**B1.**
```console
$ mkdir proj && cd proj
$ touch a.txt b.csv a2.csv
$ ls *.csv
```

**B2.**
```console
$ printf 'x\n' > f1
$ ln f1 f2
$ ln -s f1 f3
$ ls -li
```
(reproduce every column for each of the three lines)

**B3.**
```console
$ echo one > out 2> err
$ cat out err
$ cat missing 2> err2
$ echo $? ; cat err2
```

**B4.**
```console
$ name=data
$ echo 'value is $name'
$ echo "value is $name"
$ echo "value is $(echo $name | tr a-z A-Z)"
```

**B5.**
```console
$ cd /nonexistent_dir 2> /dev/null
$ echo $?
$ pwd
```

**B6.**
```console
$ mkdir -p lvl1/lvl2
$ touch lvl1/f lvl1/lvl2/f
$ find lvl1 -type f | sort
$ find lvl1 -maxdepth 1 -type f | wc -l
```

## Section C — Live terminal (40 pts)

Perform on the provided VM, inside `~/midterm/`. Grade: correctness
of end state **and** evidence in the transcript (commands visible, no
`history`-free guessing).

**C1 (10).** Build `~/midterm/{raw,scripts,reports}`. In `raw/`
create five files `sensor_01.csv` … `sensor_05.csv` each containing
one line `sensor,ok`. Copy exactly the odd-numbered ones into
`reports/` using a single glob (no listing files individually), then
show a listing proving it.

**C2 (10).** Create `scripts/clean.sh` that: prints the number of
`.csv` files in a directory passed as `$1`, errors with usage text
and exit status 2 when `$1` is missing, and returns 0 otherwise. Make
it executable, run it correctly, run it incorrectly, and show both
exit statuses.

**C3 (10).** Create group `midteam`; add your user to it (you have
passwordless sudo on the exam VM). Make `~/midterm/reports`
group-owned by `midteam` with SGID and mode 2775. Create a file in it
and prove, with one `ls -l` line, that the inheritance worked.

**C4 (10).** Something is wrong with `~/midterm/hidden/.keep_me`:
it cannot be deleted even by you. Diagnose using non-destructive
commands, state the cause, then delete it and show the evidence
chain (before-diagnosis → fix → after-proof).

---

## Grading notes (instructor)

- A-section: 3 pts per item — 1 for the mechanism word, 1 for the
  correct consequence, 1 for precision. Half-marks for mechanisms
  named correctly with wrong consequences.
- B-section: all-or-nothing per line of output (5 = exact lines +
  correct explanation; 3 = exact output, explanation missing/wrong;
  1 = right mechanism, wrong output).
- C-section: end state alone caps at 6/10; the remaining 4 require
  visible evidence commands in the transcript.
