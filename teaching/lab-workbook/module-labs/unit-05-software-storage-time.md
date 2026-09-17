# Unit 5 Labs — Software, Storage & Time (M16–M19)

> Sessions S15–S18 · packages, loopback disks, processes, scheduling.
> **Snapshot before package and disk labs** — announced as ritual.

| Lab | Module | Duration | Difficulty | Deliverable | Link |
|---|---|---|---|---|---|
| apt lifecycle drills | M16 | 20' | ★ | search/show/install/remove with dependency notes | [M16 labs](../../../modules/M16-package-management/content/labs/README.md) |
| df/du/lsblk triage | M17 | 20' | ★★ | contradiction resolved with evidence | [M17 labs](../../../modules/M17-storage-and-filesystems/content/labs/README.md) |
| Loopback disk lifecycle | M17 | 40' | ★★★ | format→mount→write→fstab→remount transcript | [M17 labs](../../../modules/M17-storage-and-filesystems/content/labs/README.md) |
| Process triage | M18 | 25' | ★★ | htop/ps evidence + signal-choice log | [M18 labs](../../../modules/M18-processes-jobs-signals/content/labs/README.md) |
| Signal ladder | M18 | 20' | ★★ | trap-script TERM-vs-KILL evidence | [M18 labs](../../../modules/M18-processes-jobs-signals/content/labs/README.md) |
| Cron + environment trap | M19 | 30' | ★★★ | scheduled job that *logs*, trap diagnosed | [M19 labs](../../../modules/M19-scheduling-cron-timers/content/labs/README.md) |
| Timer comparison | M19 | 15' | ★★ | same job as systemd timer, journald evidence | [M19 labs](../../../modules/M19-scheduling-cron-timers/content/labs/README.md) |

## Session mapping

- **S15**: apt drills (+ M17 triage starts)
- **S16**: loopback lifecycle — the session's centerpiece
- **S17**: process triage + signal ladder
- **S18**: cron trap lab + timer comparison; backup script scheduling HW

## The unit's safety architecture

- **Loopback disks only** — every formatting command names a file that
  behaves like a disk; the four-line rule (purpose/risk/safe/recovery)
  is recited at the lab brief
- **Snapshot before apt labs** — announced; a broken half-removal is a
  restore, not a crisis
- **Signal ladder discipline** — TERM → wait → KILL, demonstrated on a
  trap script before anyone kills anything real

## Checkpoints that matter most

- Loopback lab: every fstab *field* explained in one line each
- Cron trap: the diagnosis trio (PATH, tilde, logging) named and fixed
- Signal ladder: "why TERM first" answered with the trap-demo evidence

## Extension routing (★★★)

- M17: RAID-0-on-loopback concept; LVM reading
- M19: systemd `OnCalendar` expressions; timer with failure handling

## Instructor staging

- 100 MB loopback images ready (or the lab's `dd` fallback)
- Snapshot the room before S15 and before S16
- [Infrastructure checklist](../../setup-and-delivery/lab-infrastructure.md)
  items 5–6

## After this unit

**LA-2 — Pipeline Fluency** (graded, week 8 window) tests M09+M10
evidence skills; **A2 (Assignment 2)** released S17 covers M09–M19 —
this unit is its heart.
