# Unit 2 Lecture Slides — Command Line Fluency (M05–M09)

> **Delivery:** Sessions 5–8 · Speaker notes:
> [../speaker-notes/unit-02-command-line-notes.md](../speaker-notes/unit-02-command-line-notes.md)

---

# Slide 1 — Title

## Slide Content
**Unit 2 — Command Line Fluency**
Shell · Filesystem · Files · Text processing · Pipes (M05–M09)
*The four weeks that change how you work with data*

## Instructor Delivery Notes
Set the stake: "Everything else in this course — permissions, servers,
containers — is administered *through these words*."

## Visual or Demonstration Suggestion
One terminal, blank prompt, cursor blinking. Say nothing for 3 seconds.

## Student Question
"What can a terminal do that your file manager can't?"

---

# Slide 2 — Shell vs terminal vs console

## Slide Content
- **Terminal**: the window (the emulator)
- **Shell**: the program inside it that reads commands (bash)
- **Console**: the raw text machine itself (pre-GUI meaning)
- Prompt anatomy: `dsstudent@lab:~$` = user@host:path + privilege hint

## Instructor Delivery Notes
Draw the three-boxes diagram (you → terminal → shell → kernel). The `$`
vs `#` prompt distinction previews Unit 4's sudo work.

## Visual or Demonstration Suggestion
`echo $0` shows the shell; `tty` shows the terminal device.

## Student Question
"When you 'type a command', which of the three actually executes it?"

---

# Slide 3 — Command anatomy & getting help

## Slide Content
```
command  -o  --long-option  argument  argument
```
- `man command` — the manual (space to page, `q` to quit, `/word` to search)
- `command --help` — the quick version
- Teach the reflex: **unknown flag → `man` first**

## Instructor Delivery Notes
Live `man ls`: demonstrate the SYNOPSIS line reading skill — brackets
mean optional, `...` means repeatable. Reading synopses is a superpower.

## Visual or Demonstration Suggestion
Project `man rsync`'s synopsis and decode it together.

## Student Question
"In `cp [-R] source... dest`, how many sources may you give?"

---

# Slide 4 — The filesystem hierarchy (FHS)

## Slide Content
```
/            root of everything
├── home     user files (you live here)
├── etc      configuration
├── var      variable data (logs, spool)
├── tmp      ephemeral — wiped on reboot
├── usr      installed software
├── proc     kernel's diary (virtual!)
└── dev      devices as files
```
- "Everything is a file" — even hardware and kernel state

## Instructor Delivery Notes
Walk it live in a terminal, not on the slide. The FHS is a *vocabulary*
for the whole course: "check /var/log" means something from now on.

## Visual or Demonstration Suggestion
`ls /proc` then `cat /proc/uptime` — kernel state as readable files.

## Student Question
"Where would a program's settings live? Its logs? Your downloads?"

---

# Slide 5 — Paths: absolute, relative, ~, -

## Slide Content
- Absolute: `/home/dsstudent/data/file.csv` (from `/`)
- Relative: `data/file.csv` (from where you are) · `.` here · `..` up
- `~` = home · `cd -` = jump to previous directory
- `pwd` when lost — non-negotiable reflex

## Instructor Delivery Notes
The relative-path wall is real: have them `cd` three levels and predict
`pwd` before checking. `cd -` buys delight; spend it early.

## Visual or Demonstration Suggestion
Two terminals side by side, same commands from different starting dirs —
different results, same meaning.

## Student Question
"You're in `/var/log`. What's the relative path to `/var/log/apt`? To `/etc`?"

---

# Slide 6 — Knowledge check

## Slide Content
1. `/tmp` vs `/home` — which survives reboot? Why does the design make sense?
2. What does `~../bin` (from your home) resolve to?
3. In one command each: go to `/usr/share/doc` and back to where you were.

## Instructor Delivery Notes
Q2 is the discriminator — expect `~/bin` vs `/home/bin` confusion; draw
the tree and resolve it stepwise.

## Visual or Demonstration Suggestion
Resolution animation: each `..` deletes one path component.

## Student Question
(Q3 doubles as the check — watch for `cd /usr/share/doc` then `cd -`)

---

# Slide 7 — Files & directories: the workhorse verbs

## Slide Content
- `mkdir -p a/b/c` — deep creation, no complaints
- `cp -r` for trees · `mv` = move **and rename** (no copy-then-delete)
- `ls -lh` — long, human sizes · `tree` — the map
- Naming discipline: **no spaces in dataset filenames** (your future scripts thank you)

## Instructor Delivery Notes
`mv`-as-rename surprises everyone — demo it twice. The spaces warning
previews quoting hell in Unit 3; one story now saves an hour later.

## Visual or Demonstration Suggestion
`ls -li` on two hard links — same inode, two names. Inode talk: 3 minutes max.

## Student Question
"mv moves. What does it *do* when the destination exists?"

---

# Slide 8 — rm with respect (safety slide)

## Slide Content
- `rm file` — gone. No trash can. No undo.
- Course reflexes: **`ls` the glob before `rm` the glob** · prefer `rm -i` in training · never `rm -rf` on anything you didn't `ls` first
- `-r` = recursion (directories) · `-f` = force (silence — danger)
- `rmdir` only removes *empty* dirs — the safe training wheels

## Instructor Delivery Notes
Purpose/Risk/Recovery framing out loud: purpose — deletion is real work;
risk — globs expand before rm sees them; recovery — snapshots (this is
*why* week 2 made you snapshot).

## Visual or Demonstration Suggestion
In the VM: `ls *.csv` then `rm *.csv` — with the `ls`-first reflex narrated.

## Student Question
"Why does the shell expand `*.csv` *before* `rm` runs — and why does that matter?"

---

# Slide 9 — Text processing: profile before you compute

## Slide Content
- `cat / less / head / tail / wc` — look, page, sample, count
- `sort -k2 -n` · `uniq -c` (needs sorted input!) · `cut -d, -f3` · `tr`
- One-liner profiling beats opening a 5 GB file in any editor
- `tail -f app.log` — watch data as it arrives

## Instructor Delivery Notes
Dataset profiling challenge: "this 50 MB CSV — how many rows, which
columns, top values of column 2 — **without opening it**." Let them
build it; wrong answers are productive here.

## Visual or Demonstration Suggestion
`head -3 sales.csv` → `wc -l` → `cut -d, -f2 | sort | uniq -c | sort -rn | head -5` built one pipe at a time.

## Student Question
"Why must input to `uniq -c` already be sorted?"

---

# Slide 10 — grep, sed, awk: the heavy trio

## Slide Content
- `grep -E 'regex' file` — filter lines (the finder)
- `sed 's/old/new/g'` — stream edit (the replacer)
- `awk -F, '{print $2, $4}'` — column-aware processing (the selector)
- Rule of thumb: **grep finds, sed changes, awk reports**

## Instructor Delivery Notes
Scope discipline: sed s/// and awk print/tally only — no scripting in
these tools; that's Unit 3's bash. The trio's one-liners get DS-flavored:
log levels, sensor IDs, cost columns.

## Visual or Demonstration Suggestion
One log line; extract timestamp/level/message three ways (cut, sed, awk) — same answer, different tools.

## Student Question
"When is awk strictly *necessary* over cut?"

---

# Slide 11 — Pipes and redirection: where do the bytes go?

## Slide Content
```
cmd1 | cmd2          stdout → next stdin
cmd > file           overwrite        (danger: truncates)
cmd >> file          append
cmd 2> err.log       stderr only
cmd > out 2>&1       both (or: &> out)
cmd < input.txt      feed a file as stdin
```
- `2>&1` order matters; `> file` *truncates before the command runs*

## Instructor Delivery Notes
The x-y table (from M09) is the single highest-value exam artifact —
build it on the board interactively. The truncate-before-running surprise
is worth a live demo on a throwaway file.

## Visual or Demonstration Suggestion
`ls > f` where `f` is full of text — show it emptied. Fear is instructive.

## Student Question
"Why does `sort < f > f` sometimes corrupt — and what's the fix?"

---

# Slide 12 — Knowledge check + activity

## Slide Content
1. Build: top-3 most common log levels in `app.log`, highest first.
2. What's the difference in output: `wc -l < f` vs `wc -l f`?
3. Relay race: 4 students each add one stage to a pipeline.

## Instructor Delivery Notes
Q2 is stdin-vs-filename-argument understanding — the quiet idea under
all of pipes. The relay is loud but effective; keep stages honest
(each stage must *transform*).

## Visual or Demonstration Suggestion
Pipeline on the board growing left to right; data sample flowing under it.

## Student Question
(relay question: "which stage could be reordered without changing the result?")

---

# Slide 13 — Common mistakes (Unit 2)

## Slide Content
- `uniq` without `sort` — silently wrong counts
- `grep` on a *directory* without `-r` — confusing error
- Relative-path drift after `cd` — script runs elsewhere, "works on my machine"
- `rm` on an untested glob — the one mistake with no undo
- Forgetting `2>` — errors vanish into the terminal void

## Instructor Delivery Notes
Each maps to a lab exercise in the modules; preview that the fix-the-bug
labs will weaponize these.

## Visual or Demonstration Suggestion
The `sort|uniq` wrong-vs-right side-by-side.

## Student Question
"Which of these five have you already done this week?" (laughter normalizes recovery)

---

# Slide 14 — Data Science connection

## Slide Content
- **Before pandas:** is this 40 GB CSV even worth loading? One pipeline answers.
- Data hygiene: dedupe (`sort -u`), profile (`uniq -c`), extract (`awk -F,`)
- Log analysis for your future services — same tools
- The M08 mini-project: shell tools as the *first pass*, Python as the second

## Instructor Delivery Notes
Show a real profiling result and the decision it enabled ("column 3 is
90% NULL — don't bother loading it"). Tools serve judgment.

## Visual or Demonstration Suggestion
Pipeline result beside a pandas `describe()` of the same column — agreement is the point.

## Student Question
"What dataset question can you now answer in one line that used to need a script?"

---

# Slide 15 — Unit summary

## Slide Content
- Shell executes; FHS names; paths address
- Files: verbs (cp/mv/rm) + inodes + globs — with `rm` reflexes
- Text tools: profile, find, transform, report
- Pipes compose them; redirection aims them
- **You are now dangerous. Unit 3 makes you *responsible*.**

## Instructor Delivery Notes
The "dangerous → responsible" line lands — it's the segue to scripting
with `set -euo pipefail`.

## Visual or Demonstration Suggestion
Rebuild the Unit-2 concept map from memory, class-wide.

## Student Question
"Which command family will you use tomorrow on real data?"

---

# Slide 16 — Exit ticket & homework

## Slide Content
**Exit ticket:** write a one-line pipeline that counts lines in `data.csv`
containing `ERROR`, then HW:
- M07–M09 quizzes · M08 mini-project started
- LA-1 next week — practice the [navigation circuits](../../labs/README.md)

## Instructor Delivery Notes
Collect pipelines; the best two open Session 9 (scripting) as
"yesterday's one-liners become today's scripts."

## Visual or Demonstration Suggestion
— (formative collection)

## Student Question
(exit ticket is the question)

---

## Deck references
- Modules: [M05](../../modules/M05-terminal-and-shell/README.md) · [M06](../../modules/M06-filesystem-hierarchy/README.md) · [M07](../../modules/M07-files-and-directories/README.md) · [M08](../../modules/M08-text-processing/README.md) · [M09](../../modules/M09-pipes-and-redirection/README.md)
- Next deck: [Unit 3 — Scripting & Automation](unit-03-scripting-automation-slides.md)
