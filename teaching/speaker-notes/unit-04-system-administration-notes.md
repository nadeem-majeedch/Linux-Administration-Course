# Unit 4 Speaker Notes — System Administration (M12–M15)

> Companion to [../lecture-slides/unit-04-system-administration-slides.md](../lecture-slides/unit-04-system-administration-slides.md).

## Sessions 11–12 overview

**Teaching purpose.** Shift the frame from *can I* to *may I*: identity,
permission design, sudo policy. This unit feeds LA-3 (permissions
repair) and the midterm's heaviest sections, and the capstone's
permission-matrix rubric area.

**Opening question (S11).** "On a shared lab server, what stops you from
deleting your teammate's dataset?" Collect: permissions, groups,
etiquette — then show that the first two *are* the third, enforced.

## Per-slide guidance

- *S2 (identity):* `id` decode is done by volunteers, one field each.
  The uid<1000 system-users fact gets its 30 seconds and pays off in
  M20 when services appear as "users".
- *S3 (triplet):* run the decode as a *ritual* — owner/group/other in
  chorus. The directory-x discussion is the session's conceptual peak;
  use `chmod 000` on a directory live: listing fails differently than
  opening, and the error messages name the missing bit.
- *S4 (modes):* 640/755/600 drills in chorus. umask: teach *why* files
  start 666 and dirs 777 (execute is a security decision, never granted
  by default) — this defuses the "different bases" confusion permanently.
- *S6 (SGID/sticky):* the scenario vote (2770 vs 1770 for Elena's
  read-only team) is the unit's best activity. Expect initial votes for
  2770 "because sharing"; the delete-the-teammate's-file demo flips the
  room. Don't skip the demo because the vote concluded — seeing it is
  believing it.
- *S7 (sudo):* read one M14 incident aloud as a *story* (who, what typo,
  what blast radius). The redirection trap (`sudo cmd > file`) goes on
  the board with the shell-vs-sudo open-by-who diagram.
- *S8 (PATH):* the shadowing demo (fake python3 prepended) is the hook
  for M27. Leave the mystery unresolved for 60 seconds — discomfort is
  the memory glue.

## Misconceptions (unit-wide)

1. "`chmod 777` fixes sharing" — it removes accountability; the M13 line
   ("a confession") is quotable and exam-relevant.
2. "Groups are for organization only" — they're the *primary* sharing
   mechanism; SGID makes inheritance automatic.
3. "sudo is a bigger password" — it's a *policy engine* with logging.
4. "Environment is global" — it's inherited per-process; every demo in
   this unit quietly proves otherwise.

## Expected responses & probes

- S6 vote flip: after the sticky demo, ask *why* /tmp has been 1777
  forever — connects their design decision to the system's.
- S7 "what would you grant?" — insist on the *command list* shape of the
  answer (`/usr/bin/apt install` scoped), not vibes. Vague grants get
  LA-3-style deductions later; say that.

## Demo choreography & error table

| Demo | Setup | Failure shown | Recovery |
|---|---|---|---|
| dir-x | `chmod 664 dir` | ls names but no entry | restore x |
| sticky | 2770 dir, teammate file | owner deletes other's file | `chmod 1770`, retry blocked |
| sudo redirect | `sudo cmd > /etc/…` | permission denied | `sudo sh -c 'cmd > file'` (and explain) |
| PATH shadow | fake python3 first in PATH | type -a shows both | remove from PATH |

## Classroom activity

Permission-decoding sprints: project 8 `ls -l` lines, 20 seconds each,
pairs write (a) who can read, (b) who can delete. Scoring is instant and
loud. Lines include one sticky-bit dir and one ACL line as stretch.

## Timing & cuts

S11 is content-dense: if behind, ACL slide shrinks to "getfacl shows the
extended view; M13 has the clinic" — the labs carry depth. S12 never
cuts the PATH mystery or the sudoers drop-in demo.

## Transition

"You decide who may do what. Next unit: the machine's *resources* —
software, space, and time." (M16–M19.)
