# Lab 3 — First Commands

> Lesson 7 · Time: ~40 min · Risk level: zero (read-only commands; you will create
> nothing and delete nothing)
> Environment: any Ubuntu system

## Goal

Speak the command grammar fluently: options, arguments, quoting, and exit codes.
By the end you will have built your first *deliverable* — a "system card" text
report assembled from command outputs — which is, in miniature, exactly what
administrators and data engineers do when they write status scripts.

## Before you start

- [ ] Terminal open; Lessons 5–7 fresh (prompt, grammar, `$?`)
- [ ] `lab-log.md` ready

## Part 1 — Prediction-verify table (15 min)

For each line: **write your prediction in the log, run it, compare.** If reality
disagreed, write *why* in five words or fewer. The disagreements are the lesson.

| # | Command | Predict (before!) |
|---|---|---|
| 1 | `date +%A` | |
| 2 | `date +%Y-%m-%d` | |
| 3 | `echo one    two` | |
| 4 | `echo "one    two"` | |
| 5 | `echo $(whoami)` | |
| 6 | `id -un` | |
| 7 | `uname -r` | |
| 8 | `ls -d /etc` | (check `man ls` for `-d` first) |
| 9 | `hostname; whoami` | (two commands, one line) |
| 10 | `date +%F; echo done` | |

Scoring yourself: 8–10 correct → fluency arriving; 5–7 → re-read Lesson 7 §3–4;
<5 → re-run Lab 3 after one more Lesson-7 pass. Nobody is judged here; everybody
keeps the reflex.

## Part 2 — Options in the wild (10 min)

1. Run all three: `ls -l -a -h`, `ls -la -h`, `ls -lah` (in your home directory).
   Are the outputs identical? Which form will you use in scripts, and why?
2. `free -m` vs `free -h`: what does `-m` change? Which do you prefer for eyes
   and which for (future) scripts, and why might a *script* prefer fixed units?
3. `man free` — find the option to make `free` repeat its output continuously
   (search `/repeat`). Try it briefly, then stop it with **Ctrl+C**.
4. `head -n 3 /etc/os-release` vs `head -3 /etc/os-release`: both work — verify.
   What does this tell you about how strict GNU tools are with attached values?

## Part 3 — Exit codes: the command's report card (10 min)

```console
$ date
$ echo $?
```

Record the number. Now the failing path:

```console
$ date --definitely-not-an-option
date: unrecognized option '--definitely-not-an-option'
$ echo $?
```

Record this number too. Then the diagnostic pattern professionals actually use:

```console
$ free --bogus 2> /dev/null ; echo "exit code: $?"
```

(What you just saw: the error message *silenced* — `2>` redirects error output,
Module 9's topic, met as a magic trick today — while the exit code still told the
truth.) In your log, one sentence: why is the exit code more reliable to *programs*
than the error message is?

## Part 4 — Deliverable: your system card (10 min)

Assemble a text report from commands you already know. Type these lines one at a
time, observe, then write the outputs into `lab-log.md` under `Lab 3 — system card`:

```console
$ hostname
$ whoami
$ date +%F
$ uname -srm
$ cat /etc/os-release | head -2
$ free -h | head -2
$ lscpu | grep -i "model name" | head -1
```

The last two lines sneak-preview pipes (`|` sends one command's output into the
next — Module 9's beating heart; today it is enough to *see* that it composes).

Add a header line in your card: `# System card — <date>` (yes, `#` starts a comment
in shell too). Congratulations: you have written your first *report* on Linux.

## Wrap-up checklist

- [ ] 10/10 prediction rows have both prediction and outcome recorded
- [ ] Part 2's four option questions answered with man-page receipts
- [ ] Both exit codes recorded and explained in one sentence
- [ ] System card complete and dated in `lab-log.md`
- [ ] Zero destructive commands were needed — and you know what `$` means

## What you can now do

You can read a command line and predict what it does *before* running it, prove a
command's success or failure from its exit code, and assemble command outputs into
a report. From here, Module 2 (and every later module) assumes exactly this fluency.
