# Demo 1 — Filesystem Navigation: Paths That Lie

> **Session:** S5 · **Duration:** ~8 min · **Risk:** none (read-only)
> **Objective:** install the model that *the same string resolves
> differently from different working directories* — the root of every
> path bug this course will ever see.

## Prerequisites

- Projector showing a VM terminal at readable font size
- Student VMs at the S5 checkpoint (any directory)

## Setup (before class, or live in 20 seconds)

```console
$ mkdir -p /tmp/demolab/{docs,docs/2026,archive}
$ touch /tmp/demolab/docs/report.txt /tmp/demolab/archive/report.txt
```

Both `report.txt` files get **different contents**:

```console
$ echo "fresh version" > /tmp/demolab/docs/report.txt
$ echo "old version"  > /tmp/demolab/archive/report.txt
```

## Procedure (with narration)

**Step 1 — same command, different worlds.**

```console
$ cd /tmp/demolab/docs && cat report.txt
fresh version
$ cd ../archive && cat report.txt
old version
```

*Narration:* "I never lied — `report.txt` was always the address. What
changed was *where the address starts*."

**Step 2 — the prediction.** Ask the class to write what this outputs
**before** running:

```console
$ cd /tmp/demolab/archive && cat ../docs/../archive/report.txt
```

(Answer: `old version` — `..` cancels `docs`, then re-enters archive.
Expect half the room to miss the cancel-out.)

**Step 3 — `~` and `-`.**

```console
$ cd ~ && pwd
/home/dsstudent
$ cd /tmp/demolab/archive && cd - && pwd
/home/dsstudent
$ cd - && pwd
/tmp/demolab/archive
```

*Narration:* "`-` is the shell remembering where you just were — it's a
toggle, not magic."

**Step 4 — absolute anchoring.** Show the same file reached with the
absolute path from *any* directory:

```console
$ cd / && cat /tmp/demolab/docs/report.txt
fresh version
```

*Narration:* "Absolute paths work from anywhere — that's why scripts
use them; humans use relative because we know where we are. Until we
don't."

## Expected output

Exactly as shown above (paths and usernames vary — say so; *evidence
over memorization*).

## Questions to ask

1. After step 2's surprise: "Walk me through the resolution, one
   component at a time."
2. "Why do scripts prefer absolute paths?" (expected: they can't know
   the caller's cwd)
3. "What does `pwd` cost you, and why run it anyway?" (nothing; it's
   the cheapest insurance in Linux)

## Common errors during the demo

- Typo'd path → `No such file or directory` — read it *with* the class;
  the message names the truth
- Running `cd` with no argument mid-demo → lands home; turn it into the
  `cd` = home reminder

## Recovery

None needed — read-only demo. If you mistype, diagnose aloud and
continue; that's the course's own method modeled.

## Cleanup (census first)

```console
$ ls /tmp/demolab          # confirm: only demo artifacts
$ rm -r /tmp/demolab && ls /tmp/demolab 2>&1   # gone; message proves it
```

`/tmp` self-cleans on reboot anyway — say so; it's the FHS lesson
recurring.

## Optional extension

`readlink -f ../docs/../archive/report.txt` — canonicalization shows
the *resolved* path; the tool makes the shell's mental model visible.
