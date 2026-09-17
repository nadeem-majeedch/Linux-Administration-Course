# Unit 5 Lecture Slides — Software, Storage & Time (M16–M19)

> **Delivery:** Sessions 15–18 · Speaker notes:
> [../speaker-notes/unit-05-software-storage-time-notes.md](../speaker-notes/unit-05-software-storage-time-notes.md)

---

# Slide 1 — Title

## Slide Content
**Unit 5 — Software, Storage & Time**
Packages · Disks & filesystems · Processes & signals · Scheduling (M16–M19)

## Instructor Delivery Notes
Framing: "You can now run a machine *today*. This unit is about
*keeping* it running: software in and out, space to grow, work that
runs while you sleep."

## Visual or Demonstration Suggestion
`apt list --installed | wc -l` — "you manage all of these now."

## Student Question
"Who has installed software by downloading random .exe/.deb from the web? Why is that different from apt?"

---

# Slide 2 — apt: the package lifecycle

## Slide Content
- `apt update` — refresh the *catalogue* (installs nothing)
- `apt install / remove / upgrade` — act on it
- `apt search / show` — discover before installing
- `apt purge` removes config too · `apt autoremove` tidies orphans
- `--dry-run` — rehearse before consequential upgrades

## Instructor Delivery Notes
The update/upgrade distinction is a decade of confusion in one slide —
make the catalogue metaphor carry it. Never teach `dpkg -i` as the
primary path; it's the manual override, and it skips dependency
resolution.

## Visual or Demonstration Suggestion
`apt install htop` live: read the dependency resolution out loud as a negotiation.

## Student Question
"You ran upgrade without update. What did you actually get?"

---

# Slide 3 — Repositories & trust (and PPA risk)

## Slide Content
- Sources live in `/etc/apt/sources.list.d/` — the catalogue's addresses
- Ubuntu repos: curated, signed, security-patched
- **PPAs**: convenient third-party stores — you inherit the maintainer's trust
- RPM world: `dnf/yum` + `.rpm` (identify-don't-use for this course)
- Installing from source: the *concept* (configure → make → install) and why repos beat it

## Instructor Delivery Notes
Trust framing: "apt update is a *promise check*; the signature is the
promise." PPA story: the maintainer's laptop becomes part of your supply
chain. Exams ask identify-not-administer for RPM — say so.

## Visual or Demonstration Suggestion
`apt policy` on a package showing repo priority; a sources.list.d diff before/after adding a PPA.

## Student Question
"Why does 'it works on my machine' often mean 'I installed a PPA and forgot'?"

---

# Slide 4 — Disks and the block-device view

## Slide Content
- `lsblk` — the tree of disks, partitions, mountpoints
- `/dev/sdb1` style names — devices as files (M06 payoff)
- `df -h` — *space by filesystem* · `du -sh dir` — *space by directory*
- The classic contradiction: `df` full, `du` small → a **deleted-but-open** file
- Loopback disks: files that behave like disks — this course's safe playground

## Instructor Delivery Notes
df/du contradiction is a real interview question and a real 3 a.m.
incident; plant it, resolve it with `lsof +L1` mention, full depth in
M17's lab. Loopback framing: "we will format a disk today — a *fake*
one, and that changes everything about safety."

## Visual or Demonstration Suggestion
`lsblk` before/after attaching a 100 MB loopback disk.

## Student Question
"You deleted a huge log but `df` didn't shrink. What's holding it?"

---

# Slide 5 — Filesystems: mkfs, mount, fstab

## Slide Content
- `mkfs.ext4 /dev/loop0p1` — create a filesystem (format) — **destructive by definition**
- `mount /mnt/point` — attach it to the tree · `umount` — detach
- `/etc/fstab` — mount instructions at boot: *what where type options dump pass*
- `nofail` option — a removable disk must not block boot
- Safety rule: **mkfs on loopback only in this course** — same commands, zero real risk

## Instructor Delivery Notes
Read fstab field-by-field; make a student re-explain the pass field.
The loopback safety architecture deserves 60 seconds of respect: same
muscles, no blood.

## Visual or Demonstration Suggestion
Full lifecycle live: truncate loop file → partition → mkfs → mount → write → unmount → remount.

## Student Question
"Which fstab field would make a missing backup disk non-fatal at boot?"

---

# Slide 6 — Knowledge check

## Slide Content
1. `apt update` vs `apt upgrade` — one sentence each.
2. fstab: what does the `pass` field order, and why does `/` go first?
3. A 2 GB file was deleted; `df` still shows full. Two diagnostics?

## Instructor Delivery Notes
Q3 connects storage to processes (the fd) — the first true
cross-module exam item; let them struggle 90 seconds before hinting.

## Visual or Demonstration Suggestion
— 

## Student Question
(Q3 is the check)

---

# Slide 7 — Processes: what the kernel runs

## Slide Content
- Every process: PID (unique), PPID (parent), state (R/S/D/Z)
- `ps aux` snapshot · `top`/`htop` live · `pstree` family portrait
- Load average vs CPU%: load counts *runnable + uninterruptible* — decode with core count
- D-state: waiting on I/O so hard it can't even be killed

## Instructor Delivery Notes
Load-average decoding is the DS-server survival skill (M31 reuses it):
1.0 on 1 core = saturated; 8.0 on 32 cores = quiet. Have them compute
their VM's "roominess" live.

## Visual or Demonstration Suggestion
`htop` with F5 tree view: find systemd (pid 1) and trace your terminal's ancestry.

## Student Question
"Load 4.0: crisis or nap? What else must you know?"

---

# Slide 8 — Jobs & signals: the polite-to-forceful ladder

## Slide Content
- Shell jobs: `Ctrl-Z` pause · `bg`/`fg` · `&` start background · `jobs`
- Signals: **SIGINT (Ctrl-C, 2)** · **SIGTERM (15, default: please exit)** · **SIGKILL (9, cannot be caught)** · SIGHUP (1, often "config reload")
- Order of force: TERM first, wait, KILL last
- `kill PID` · `pkill -f pattern` (aim carefully — pattern-matching is proximity-fused)

## Instructor Delivery Notes
Demo with a `trap` script: TERM gets cleanup, KILL skips it — "SIGKILL
is the fire axe; glass everywhere." pkill by pattern gets the
two-python3s story (M18 quiz material).

## Visual or Demonstration Suggestion
trap-demo script: SIGTERM prints "cleaning up…", SIGKILL prints nothing. Run both.

## Student Question
"Why does `kill -9` not run your script's cleanup block?"

---

# Slide 9 — Scheduling: cron and systemd timers

## Slide Content
```
┌───────── minute (0–59)
│ ┌─────── hour (0–23)
│ │ ┌───── day of month (1–31)
│ │ │ ┌─── month (1–12)
│ │ │ │ ┌─ weekday (0–7, 0=Sun)
* * * * * command
```
- `crontab -e` per-user · `%` must be escaped in commands
- **Cron's environment trap**: minimal PATH, no shell profile, no terminal
- systemd timers: the modern alternative, journald-logged (M20 synergy)
- Rule: scheduled jobs log their output — *always*

## Instructor Delivery Notes
The 2-a.m.-failed-cron story opens the slide: it "works in my shell"
because the shell loads a world cron never sees. The M19 trap-lab
inflicts this deliberately — preview it.

## Visual or Demonstration Suggestion
A crontab line with an unescaped `%` — show it eat the rest of the line.

## Student Question
"Your backup script uses `~/bin/helper`. Why does cron not find it?"

---

# Slide 10 — Knowledge check

## Slide Content
1. `0 4 * * 1-5` — when does this run?
2. Your cron job can't find a command. Three fixes, best first?
3. When would you pick a systemd timer over cron?

## Instructor Delivery Notes
Q2's best answer: absolute paths (then PATH=, then wrapper) — ordering
is graded thinking. Q3 expects journald logging + calendar events +
missed-run handling.

## Visual or Demonstration Suggestion
crontab.guru-style parse read aloud from memory.

## Student Question
(Q2 is the check)

---

# Slide 11 — Common mistakes (Unit 5)

## Slide Content
- `apt upgrade` without `update` — stale catalogue
- mkfs on the wrong device — *the* reason loopback exists in this course
- `kill -9` as a first reflex — orphaned temp files, skipped cleanup
- `%` unescaped in crontab — silent command truncation
- Scheduled job with no logging — failure at 2 a.m. with zero evidence

## Instructor Delivery Notes
Each maps to a planted fault in LA-2/A2 grading — name the connection.

## Visual or Demonstration Suggestion
The unescaped `%` crontab screenshot.

## Student Question
"Which of these five would you notice *latest*?" (usually: the unlogged cron job)

---

# Slide 12 — Data Science connection

## Slide Content
- Datasets grow: the df/du triage decides *which dataset eats the server*
- Training runs = processes: monitor load, choose signals politely, leave clean temp state
- Nightly dataset sync/backup = cron or timers (M23's sync script returns)
- Pin & install Python tooling via apt *only* for system pieces — venvs (M27) own the rest

## Instructor Delivery Notes
Point forward: "the capstone's pipeline area requires ≥3 logged scheduled
runs" — this unit is where that becomes possible.

## Visual or Demonstration Suggestion
Capstone rubric rows 1–2 projected beside today's topics.

## Student Question
"Which scheduled job would *your* capstone need first?"

---

# Slide 13 — Summary & exit ticket

## Slide Content
**Summary:** apt lifecycle + trust · df/du/loopback/mkfs/mount/fstab ·
process anatomy + signals ladder + jobs · cron fields + environment trap +
timers
**Exit ticket:** decode `30 3 * * 6`; one-line: why TERM before KILL?
which fstab option protects boot?
**HW:** M16–M19 quizzes · schedule your W5 backup script · A2 progress

## Instructor Delivery Notes
Exit answers predict A2 quality — skim and re-teach the mode of the
worst question at S19's warm-up.

## Visual or Demonstration Suggestion
—

## Student Question
(exit ticket is the question)

---

## Deck references
- Modules: [M16](../../modules/M16-package-management/README.md) · [M17](../../modules/M17-storage-and-filesystems/README.md) · [M18](../../modules/M18-processes-jobs-signals/README.md) · [M19](../../modules/M19-scheduling-cron-timers/README.md)
- Next deck: [Unit 6 — Services, Network & Security](unit-06-services-network-security-slides.md)
