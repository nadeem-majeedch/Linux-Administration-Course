# Unit 5 Teaching Guide — Software, Storage & Time (M16–M19)

> Sessions S15–S18 · companions: [speaker notes](../../speaker-notes/unit-05-software-storage-time-notes.md) · [deck](../../lecture-slides/unit-05-software-storage-time-slides.md)

## M16 Package Management (S15)

**Objectives.** apt lifecycle with the catalogue metaphor; repository
trust; PPA risk; identify-level RPM awareness.

**Sequence.** Lifecycle verbs → dependency resolution read-aloud →
sources & trust → PPA story → RPM two-minutes → source-install concept.

**Difficult concepts.** *Update vs upgrade* — catalogue metaphor until
reflex. *Dependency negotiation* — read apt's resolution aloud as
dialogue.

**Common mistakes.** `dpkg -i` as a primary path (skips resolution);
random PPAs left installed; treating `autoremove` as optional cleanup
(it's orphan hygiene).

**Demo plan.** `apt install htop` with the dependency text read
rationally; `apt policy` for repo provenance.

**Activity.** "Which package command when?" scenario round.

**Assessment hook.** M16 quiz (apt failure triage); feeds A2's
environment section.

**Extension.** ★★★: apt pinning concept (reading-level) from M16
challenges.

**Troubleshooting (in class).** Snapshot *before* package labs — a
broken half-removal mid-lab is a restore, not a crisis. `apt lock`
contention (two apt processes) happens if students parallel-run labs —
diagnose the lockfile live once; it's a teachable

## M17 Storage & Filesystems (S15–S16, spans)

**Objectives.** df/du/lsblk fluency; the deleted-but-open mystery;
full loopback lifecycle; fstab field literacy.

**Sequence.** S15: lsblk/df/du + the mystery planted. S16: the
loopback lifecycle lab *with the safety architecture narrated*, then
fstab field-by-field.

**Difficult concepts.**
- *mkfs destructiveness vs loopback safety* — the whole lesson is
  "same commands, different object"; name the architecture explicitly.
- *fstab pass field* — boot-order semantics; volunteers re-explain
  until clean.

**Common mistakes.** `umount: target is busy` (their own shell's cwd —
diagnose live every time); writing fstab entries without `nofail` for
removable media; formatting *simulated* disks but still testing
`rm -rf`-adjacent commands carelessly.

**Demo plan.** Full lifecycle: truncate loop file → partition → mkfs →
mount → write → unmount → remount → fstab entry → `mount -a` (with
`nofail` discussed as the boot-safety option).

**Activity.** fstab field quiz; df/du contradiction resolution pairs.

**Assessment hook.** M17 quiz (df/du contradiction resolution — a
graded classic); feeds A2 and the capstone storage-design area.

**Extension.** ★★★: M17 challenges (loopback RAID-0 concept, LVM
reading-level).

**Troubleshooting.** Pre-stage 100 MB loopback images; if losetup
permissions bite (contested VM state), the lab's fallback path uses
`dd`-created images under `~/` — module lab covers both.

## M18 Processes, Jobs & Signals (S17)

**Objectives.** Process anatomy reading (ps/top/htop); signal-choice
discipline; job control; load-average decoding against core count.

**Difficult concepts.** Load ≠ CPU% (runnable + uninterruptible ÷
cores); D-state (uninterruptible sleep explains "unkillable" processes);
SIGKILL's skipped cleanup (trap demo).

**Common mistakes.** `kill -9` first reflex; `pkill` by loose pattern
(the two-python3s story); confusing shell jobs with daemons.

**Demo plan.** htop ancestry walk (systemd → terminal → processes);
trap script TERM-vs-KILL.

**Activity.** Which-signal cards (graceful/reload/interrupt/last-resort).

**Assessment hook.** M18 quiz (signal selection, state interpretation);
feeds the practical exam's process tasks.

**Extension.** ★★★: M18 challenges (nice/renice fairness experiment).

**Troubleshooting.** htop not installed on some VMs (it's in the lab's
apt step — verify staging).

## M19 Scheduling: cron & timers (S18)

**Objectives.** Crontab grammar; the environment trap *experienced*;
logging discipline; timers-vs-cron judgment.

**Difficult concepts.** Cron's minimal environment — the failed-in-cron
demo makes "works in my shell" a diagnosed phenomenon, not a mystery.
`%` escaping (30-second horror show).

**Common mistakes.** Relative paths and `~` in cron commands; no
logging; `6`/`7` weekday confusion (both Sunday); expecting an email
that isn't configured.

**Demo plan.** The inflected cron job: works interactively, fails in
cron — diagnose PATH + tilde + logging live.

**Activity.** Cron-expression reading relay; write "02:30 on the 1st
and 15th."

**Assessment hook.** M19 quiz (environment traps, timer design); A2's
scheduled-job section grades the logging discipline.

**Extension.** ★★★: M19 challenges (systemd timer with `OnCalendar`
expressions).

---

## Unit-level notes

- **A2 releases S17** — its scope (M09–M19) is now fully taught; read
  the integrity section aloud.
- **The loopback lifecycle (S16) is the course's most important safety
  demo** — rehearse it; keep the pre-recorded fallback.
- **Staging dependencies:** loopback images (S16), staged bloated
  journals are *next* unit but the M24 staging shares the snapshot
  discipline — check the [infrastructure checklist](../../setup-and-delivery/lab-infrastructure.md)
  before S15.
