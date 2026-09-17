# Practical Examination — The Staged Server

> **Format:** 90 minutes · open-notes on *your own* module notes only
> (no internet) · 100 points · pass ≥ 70 with **no zero-score items**.
> **Environment:** an instructor-staged Ubuntu VM snapshot. Start
> `script practical.log` **before anything else** — the transcript is
> your submission alongside end states. Key:
> [practical-key.md](practical-key.md).
>
> **The rule of the room:** every task is solvable with evidence —
> read the system before acting. Guess-and-check chains are visible
> in the transcript and graded accordingly.
>
> **Staged state (unknown to you until found):** the snapshot
> contains 6 faults planted across services, permissions, disk,
> network and a repo. You are told only what "the user complains
> about" — never where the fault is.

---

## Part I — Service rescue (25 pts)

A data-upload service the team depends on is down. The user report:
*"the upload page says connection refused since this morning."*

**T1 (10).** Bring the `upload-api` service back to a healthy,
boot-persistent state. The unit file, its venv and the journal are
all suspects — at least one of them is lying. Evidence required:
journal line that identified the fault, the change you made, and
`systemctl status` + `is-enabled` output as proof.

**T2 (8).** After your fix, uploads still fail *from other machines*
but work from the server itself. Diagnose using read-only commands,
fix it, and show the proof from a client perspective
(`curl` from the VM to itself *is not* proof — state what would be,
and simulate it if no second machine exists).

**T3 (7).** The service wrote 1.2 GiB of logs this week. Reduce the
footprint *without deleting anything older than 7 days* and make the
cap permanent. Evidence: before/after `du` or `journalctl --disk-usage`
and the config line that enforces the cap.

## Part II — Identity & permissions (25 pts)

**T4 (9).** A teammate account `sam` exists but reports "my own
script won't run and I can't read my own data". Both symptoms are
real. Diagnose both (one is ownership, one is mode), fix with the
*least* privilege that works, and show before/after evidence.

**T5 (8).** Create the shared workspace `/srv/lab` for group
`labteam`: sam and you can create files; files created by either are
immediately group-writable; neither can delete the other's files
there. Two of those three requirements are property checks — prove
each one with a command sequence, not a claim.

**T6 (8).** Someone ran a script that created 500 zero-byte files
named `dump_*.bin` in `/srv/lab/incoming`. Remove exactly those —
nothing else in the directory — using a pipeline you first *dry-run*
against `ls`. Show the dry-run and the final count proof.

## Part III — Disk & data (25 pts)

**T7 (10).** "Disk full" alert, but the largest visible directory is
small. Find the real consumer, free at least 500 MiB *without
deleting any user data*, and show the before/after `df` plus the
one-line explanation of what was actually consuming space.

**T8 (8).** Create a 100 MiB loopback filesystem mounted at
`/mnt/examfs` with a filesystem of your choice from the course,
add it to `/etc/fstab` using its UUID, then unmount and
remount **by fstab alone**. Evidence: `findmnt /mnt/examfs` after the
remount. (One `fstab` typo tolerated; two means you didn't
`mount -a`-test before rebooting — grading reflects that discipline.)

**T9 (7).** In `~/examdata/` there is a mixed tree. Produce
`report.txt` (in the tree root) containing: total size of `.csv`
files, the count of files larger than 1 MiB, and the ten largest
files by size. Any correct pipeline allowed — the report is graded,
not the tooling.

## Part IV — Network & workflow (25 pts)

**T10 (8).** A cron job was supposed to back up `~/examdata` to
`~/backups` nightly. It has *never run successfully*. Find out why
(evidence, not vibes), fix it, and prove it fires by shortening the
schedule for a demonstration run.

**T11 (9).** Using the staged local repo `~/examrepo`: commit the two
safe modified files with a meaningful message, leave the one
credential-bearing file uncommitted, and add the `.gitignore` rule
that keeps it excluded durably. Then show `git log --oneline -3` and
`git status --short` as the final state.

**T12 (8).** Spin up the provided `python:3.12-slim` image as a
container that: runs a bind-mounted copy of `~/examdata` read-only,
prints the total line count of all `.csv` files inside, and exits.
Evidence: the `docker run` line and its output. No image builds
required.

---

## Submission

1. `exit` the `script` session → `practical.log` in your home dir.
2. Rename to `practical-<yourname>.log` and submit with a
   `findings.txt`: **6 numbered faults**, one line each — the fault,
   the evidence that identified it, the fix.

## Integrity rules

- Transcript must start before the first diagnostic command.
- Any `rm -rf` outside `/srv/lab/incoming`, `~/examdata` scratch or
  your own `/tmp` = zero for Part III.
- History editing (`history -c`, `.bash_history` removal) = zero
  overall.
