# Unit 1 Teaching Guide — Foundations (M01–M04)

> Sessions S1–S4 · companions: [speaker notes](../../speaker-notes/unit-01-foundations-notes.md) · [deck](../../lecture-slides/unit-01-foundations-slides.md)

## M01 What Is Linux? (S1)

**Teaching objectives.** Establish course identity and the OS mental
model; plant the kernel/distro distinction that Unit 1 keeps returning to.

**Sequence.** Course contract (10 min, non-negotiable) → OS layer story
→ Linux's place → why DS cares → SETUP walkthrough as the bridge out.

**Difficult concepts.** "Everything is a file" previews here but *lands*
in M06/M17 — introduce the phrase, don't defend it yet.

**Common mistakes.** Students conflate *installing Ubuntu* with
*installing VirtualBox* — say both words slowly in the walkthrough.

**Demo plan.** Boot instructor VM before class (S1's only hard
dependency). `uname -a` read-aloud; no more.

**Practical activity.** SETUP.md guided start; finish at home (HW).

**Discussion questions.** "What does the OS do that your browser can't
do for itself?" · "Who is the *administrator* of your phone?"

**Assessment hook.** M01 quiz (this week) — low stakes, attempt-culture
setting.

**Extension.** Students with Linux experience: install in a *second*
distro and diff `/etc/os-release` outputs — report next session.

**Troubleshooting.** The projector won't show the VM: keep the boot
narration as a story (it's actually better pedagogy).

## M02 Distributions (S2, half session)

**Objectives.** Identify distros from evidence; justify the Ubuntu LTS
choice; know the Debian/Red Hat map.

**Sequence.** Family tree (10) → evidence reading (`/etc/os-release`,
`/etc/debian_version`) → LTS rationale (10) → M03.

**Difficult concepts.** "Release model" (rolling vs fixed) — one slide,
no rabbit holes.

**Common mistakes.** "Red Hat isn't Linux" (family-tree blindness) —
the dnf-vs-apt evidence demo settles it.

**Demo plan.** `cat /etc/os-release` on two distros side by side (instructor keeps a second VM or screenshots).

**Activity.** Distro-identification from three redacted terminal outputs.

**Assessment hook.** M02 quiz; the identification format *is* the quiz's
format.

**Extension.** Read the Ubuntu release page; report LTS vs interim
support windows in weeks.

**Troubleshooting.** None — pure lecture content.

## M03 Architecture (S2, second half)

**Objectives.** The seven-layer stack as a *map*; boot's four acts as
*vocabulary*; syscall boundary as *security*.

**Sequence.** Stack drawing (interactive) → four acts (12 min cap) →
kernel/user space with the Python-CSV chain → `/proc` window.

**Difficult concepts.** The syscall boundary is the unit's densest idea —
the chain restatement drill (three students) is the scaffold.

**Common mistakes.** Placing glibc *inside* the kernel (pair-task data);
"kernel panic = broken computer" fatalism.

**Demo plan.** `ls /proc` + `cat /proc/uptime`; boot video if the live
boot is too fast.

**Activity.** The stack-drawing pair task (deck S6).

**Assessment hook.** M03 quiz — layer-attribution questions.

**Extension.** `strace ls` (existence + one-line description only —
proper use is beyond scope but the *idea* of watching syscalls lands).

**Troubleshooting.** If the boot demo is too fast to narrate: the
four-act diagram on the board while a student re-narrates it.

## M04 Installing Ubuntu / VMs (S3–S4)

**Objectives.** Everyone leaves with a working, snapshotted, updated VM;
snapshot/restore becomes *reflex*, not concept.

**Sequence.** VM concepts (15) → guided install (60, hands-on) → S4:
snapshot drills → boot recap → typed-command anatomy → bridge to M05.

**Difficult concepts.** Virtual disk vs real disk (the "Erase disk"
talk); snapshot as *time machine* (what it does/doesn't capture — it is
not a backup, a distinction the capstone will grade).

**Common mistakes.** 1 GB RAM allocations; snapshots never taken;
password forgotten at first login (reinstall is fine in week 2 — low
stakes on purpose).

**Demo plan.** The break-and-restore choreography (hostname rename →
restore) — full choreography in the speaker notes; pre-recorded fallback
recommended.

**Activity.** Restore race (pairs).

**Assessment hook.** M04 quiz; snapshot verification screenshot as HW
completion evidence.

**Extension.** ★★★: install with LVM and explain the volume-group layer
(reading-level); or scripted unattended install pointer.

**Troubleshooting.** VT-x/BIOS, install hangs at copy phase, forgotten
password — fixes in [troubleshooting-teaching](../troubleshooting-teaching.md#1-mass-vm-breakage-lab-day-30-seats-nothing-boots)
and SETUP.md. Two spare ISOs on USB, always.

---

## Unit-level notes

- **Pacing:** S3 is the course's first hands-on hour; protect it. All
  lecture trimming happens in S2.
- **The snapshot flag:** every student must have `clean-baseline` before
  leaving S4 — check it off; week 3's labs depend on it.
- **Reading assignment rhythm starts now:** each session's prep line in
  the [plan](../../teaching-plan/16-week-course-plan.md) names the exact
  lesson; hold students to it gently (quiz attempts are the enforcement).
