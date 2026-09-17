# Final Revision Checklist — The Last Week

> A **do** list, not a read list. Every item is something you *re-run
> cold* in your VM; ticking the box means you did it, not that you
> remember it. Budget: ~2 h/day for 6 days.

## Day 1 — Command-line core (Midterm B/C)

- [ ] Build the M07 lab tree from memory: globs, streams, pipes — no
      notes for the first pass
- [ ] Redo one redirection puzzle: separate stdout/stderr into two
      files, then merge, then count each
- [ ] Hard link vs symlink: create, move target, predict, verify with
      `ls -li`
- [ ] One quoting triad: `"$VAR"` / `'$VAR'` / `$VAR*` — predict all
      three outputs *before* running

## Day 2 — Scripting (Final C, Assignment 4)

- [ ] Rewrite `clean.sh` (midterm C) from a blank file with
      `set -euo pipefail`
- [ ] Add a trap that cleans a temp dir on any exit path
- [ ] Run shellcheck on it; fix every finding
- [ ] Explain aloud: why `-u`, why `pipefail`, why quoted vars

## Day 3 — Identity & permissions (Practical II, LA-2/3)

- [ ] Rebuild the M13 shared-dir design from scratch: group, SGID,
      umask, test as two users
- [ ] One numeric/symbolic conversion drill set (5 files)
- [ ] Diagnose one planted permission error (have a classmate plant
      one, or use M13's clinic)

## Day 4 — Services, logs, network (Final D, Practical I/IV)

- [ ] Full ladder cold: link → dig → route → ss → service → app,
      narrated in under 3 minutes
- [ ] Break one user unit deliberately (bad ExecStart), fix it from
      the journal only — no config peeking until `journalctl` has
      named the cause
- [ ] Quote one real journal line and explain every field you can

## Day 5 — Storage, time, transfer (Practical III)

- [ ] tar a directory, list the archive, extract to a scratch dir,
      checksum-verify — full loop
- [ ] rsync dry-run, then real sync, then *verify*; note what the
      summary told you
- [ ] Read cron's environment for your user; make one job observable
      (redirect + PATH) and run it once

## Day 6 — DS stack (Final C, A6, capstone)

- [ ] venv from zero: create, activate, verify which python, pin a
      requirements.txt, prove isolation
- [ ] Git loop under time: status → branch → commit → merge, with
      one conflict resolved honestly
- [ ] Docker: run a container with a bind mount, write to the mount
      from inside, destroy the container, show the file survived
- [ ] One full DS transfer story: pull raw → clean → push results →
      checksums (M23)

## Day 7 — Simulation

- [ ] Sit one past-format paper closed-book
      ([midterm](../../assessments/exams/midterm.md) or
      [final](../../assessments/exams/final.md)) in time-boxed
      conditions — *before* opening any key
- [ ] Grade yourself with the public grading notes; list every missed
      *mechanism* (not missed fact)
- [ ] Re-read only those mechanisms: [important-concepts.md](important-concepts.md)
- [ ] [Safety card](../../resources/cheatsheets/safety-card.md) one
      final read — the destructive-command guards are exam content
- [ ] Sleep

## Non-negotiables whatever the week looks like

1. **No new topics after Day 6** — consolidation beats cramming.
2. **Everything above is safe-lab content** — all in your own VM.
3. **Explain aloud** — the viva samples your spoken reasoning; rehearse
   it in spoken form.
