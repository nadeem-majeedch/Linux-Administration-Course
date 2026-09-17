# Unit 5 Speaker Notes — Software, Storage & Time (M16–M19)

> Companion to [../lecture-slides/unit-05-software-storage-time-slides.md](../lecture-slides/unit-05-software-storage-time-slides.md).

## Sessions 15–18 overview

**Teaching purpose.** Resource stewardship: software in/out with trust,
disk space with diagnosis, compute with manners, repetition with
evidence. Feeds LA-2, A2, and the final exam's systems sections.

**Opening question (S15).** "Where does software *come from* on Linux?"
Expect "app stores / apt." Sharpen: apt is a *catalogue with signatures*
— the trust model is the lesson, not the convenience.

## Per-slide guidance

- *S2 (apt):* catalogue metaphor: `update` = refresh the menu, `upgrade`
  = order the dishes. Never let them blur again — quiz polls confirm.
  Read dependency resolution aloud as negotiation ("this needs that
  library at least version X").
- *S3 (PPA risk):* supply-chain framing: adding a PPA = adding a stranger
  to your kitchen. One real incident story (any historical apt/mirror
  compromise) told in 45 seconds makes the abstract concrete.
- *S4 (df/du):* the deleted-but-open mystery: plant it, give 90 seconds,
  then resolve with the fd idea. `lsof +L1` mention now; M17's lab
  stages the full reproduction on loopback.
- *S5 (fstab):* field-by-field with volunteers re-explaining. The
  `nofail` option is a boot-safety story: "a missing backup disk should
  cost you a backup, not a boot." Loopback safety architecture: say
  explicitly that the destructive commands are real, the *disk* is not.
- *S7 (load average):* make them compute: "your VM: 2 cores, load 1.5 —
  roomy or busy?" (roomy-ish; queueing perspective). The D-state aside
  ("can't even be killed") explains phantom hangs they'll meet in M32.
- *S8 (signals):* the trap-demo is the moral center: TERM runs cleanup,
  KILL skips it. `pkill` proximity-fusing story (two python3s) previews
  an M18 quiz item.
- *S9 (cron):* the unescaped-`%` demo is 30 seconds of horror; the
  environment trap sets up S18's failed-cron diagnosis. Timers get fair
  billing: journald logging is the decider for scheduled-work evidence.

## Misconceptions (unit-wide)

1. "`apt update` installs things" — catalogue refresh only.
2. "Formatting is always catastrophic" — *on loopback it's rehearsal*;
   the safety is in the object, not the command.
3. "`kill -9` is the professional way" — it's the last resort; skipped
   cleanup is the cost.
4. "Cron failures email me" — only if mail is configured; this course's
   rule is explicit logging.
5. "Load average = CPU%" — load counts runnable+uninterruptible; decode
   against core count.

## Demo choreography & error table

| Session | Demo | Failure beat | Recovery shown |
|---|---|---|---|
| S15 | apt install htop | — (success read aloud) | — |
| S15 | df full/du small setup | mystery stated | fd explanation, lsof +L1 |
| S16 | loopback lifecycle | umount busy (cd inside!) | exit dir, retry |
| S17 | trap script | TERM cleans, KILL doesn't | restart, re-TERM |
| S18 | cron env trap | job works in shell, fails in cron | absolute paths + log file |

The `umount: target is busy` beat in S16 is accidental genius — a
student's shell is usually the cause; diagnose it live every time it
happens.

## Classroom activities

- S16: fstab field quiz (6 fields, 30 seconds each).
- S17: signal-choice scenarios (4 cards: graceful stop, config reload,
  interrupt, last resort).
- S18: cron-expression reading relay — 5 expressions, teams translate to
  English, then write one for "02:30 on the 1st and 15th."

## Timing & cuts

S15 packs two modules: cut the source-install concept slide if behind
(reading assignment instead). S18's systemd-timer section can compress
to "cron for course, timers for production, same rules" if the lab
start slips.

## Transition

"Your machine now runs work unattended. Unit 6: what happens when those
workloads *are* the machine — services, networks, strangers on the
wire." (M20–M25.)
