# Module 23 Challenges — C1–C8

> Same contract as the Drill Book: your own VM, you break what you
> own, evidence in `lab-log.md`, the eight-step block for anything
> that looks like an incident.

## C1 — The two-minute sweep

Script `sweep.sh`: run the Performance Clinic's four-instrument sweep
(uptime+load ratio, vmstat snapshot, free available, iostat top line)
and print a *machine-readable verdict line* — e.g.
`VERDICT: cpu=ok mem=ok disk=SUSPECT net=ok` with the number that
flagged each. Test it during `./io_churn.sh 60`. Deliverable: the
script + one paragraph on what it still misses (saturation *trends*,
for one).

## C2 — Exit-code decoder

Write `decode-exit.sh <unit>`: given a user-unit name, print the last
exit code (`systemctl --user show -p ExecMainStatus`), its decoded
meaning (1 app-error / 137 SIGKILL-class / 203 exec-problem /
start-limit), and the last journal line. Test against a deliberately
broken unit for each class. Deliverable: script + the three staged
codes with their journal quotes.

## C3 — The namei forensic

Create a nested path `~/c3/a/b/c/file.txt` and break access at level
`b` (chmod on the *directory*), then from a *second user* attempt
read. Evidence: the failing command, `namei -l`, the discriminating
line. Fix minimally (`chmod o+x` on `b` only — traversal, not read),
verify as the second user, undo. Deliverable: the block + one
sentence on why `o+x` and not `o+r`.

## C4 — Chronology as evidence

Run `journalctl --since -5m -o short-precise` after staging a
mini-incident of your choosing (a service restart loop, an OOM-ish
malloc burst, a cron fire). Deliverable: a five-line timeline in your
journal where each line is *timestamp → event → inference*, with
inferences marked `// inference:` — the step-2 discipline, made
visible.

## C5 — The hypothesis ledger

Take any Drill Book incident you already solved and reconstruct its
*hypothesis ledger* formally: H1/H2/H3, each with the test command
that would confirm/kill it, ranked by probability × cheapness. Mark
which hypothesis you *actually* tested first and whether the ranking
would have saved a step. Deliverable: the ledger + one paragraph.

## C6 — Blind diagnosis swap

Pair up (or enlist an instructor/TA): they stage any setup script
from the Drill Book *or* a card-family variant on your VM while you're
away; you get only the symptom. Solve to a verified fix within 30
minutes using the method. Deliverable: the eight-step block, plus one
sentence on where the method saved you from guessing.

## C7 — The composite incident

Design (and stage) an incident that spans **three** cards — e.g., a
disk that filled (2) → OOM during the cache rebuild (3) → Jupyter
kernel dead (12). Solve it fresh the next day. Deliverable: the setup
script (kept with the answer key), the eight-step block, and one
paragraph on how composite incidents change the *order* of the ladder
(they don't — but they punish skipping verify between layers).

## C8 — Design: the on-call runbook

One page, no execution: the runbook for the course's fictional shared
analysis server (6 users, Jupyter + Postgres + nightly batch). For
each of four incident classes (card 1, 2, 6, 12): the alert that
pages, the first three commands, the escalation line, and the
canary. Every command must be one the course has taught; every
threshold must cite its lesson. Deliverable: the runbook + the three
gaps you'd flag to the professor.

**Stretch** — the method card: one page, wallet-sized. The eight
steps with their one-line rules; the four-instrument sweep; the six
network rungs; the exit-code decoder; the `namei`/`getent`/`ss`
discriminators. If it doesn't fit one page, you don't know it yet.

---
*All challenges: own VM, staged-by-you breakage, evidence in
`lab-log.md`.*
