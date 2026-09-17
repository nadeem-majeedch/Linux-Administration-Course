# Level 4 — Administrator: The Fleet Exercise

> Assumes M20–M25 · ~4 h · your own VM · `script level-4.log` first.
> Internet allowed *with citation*. You are the on-call administrator
> of a small production-ish node: two services, a database-ish
> backend, a firewall, and a set of users with opinions. Take it
> from "works on my desk" to "operable by someone else at 3 a.m."

## Part 0 — Stand up the estate (30 min)

1. Provision: one nginx (static page), one app service (any tiny
   Python HTTP API from a venv, **user-level systemd unit**), one
   PostgreSQL (course package), all on the same VM.
2. Identity: users `alice` (admin), `bob` (deploy, sudo-limited to
   the app unit + journal read — scoped drop-in, and say what the
   drop-in grants), `carol` (read-only service account that runs
   nothing).
3. Baseline evidence: `systemctl` states for all three, `ss -tlnp`,
   `ufw status verbose`, `df -h`, `free -h` — saved to
   `baseline.txt`. This file is your "before" for everything below.

## Part 1 — Harden the perimeter (45 min)

1. ufw to default-deny incoming; open exactly: 22 (from any),
   80/443 (any), app port (localhost-only — i.e. *don't* open it,
   and prove it's unreachable externally while `curl localhost`
   works).
2. SSH: key-only for `alice` and `bob` (drop-in), passwords still
   allowed for nobody else to break — document the rollback file.
3. **Break-and-verify deliberately:** from a *second* terminal
   (before locking), confirm each rule's effect; after locking,
   attempt the three things a stranger would try (ssh with
   password, app port direct, HTTP) and capture all three
   refusals. Refusals *are* the deliverable.

## Part 2 — Operability (60 min)

1. Logs: app logs to journal; nginx to its access/error logs.
   Produce `queries.sh` — four read-only one-liners: last hour's
   app errors, top-10 nginx paths by hits, all authentication
   failures today, journal errors since boot. Each must run
   *unmodified* by a teammate.
2. Monitoring: a 10-line `healthcheck.sh` — df threshold, free
   memory floor, unit states, app HTTP probe — exits non-zero on
   any failure, prints which. Wire it to a *systemd timer* (not
   cron — justify the choice in one sentence: calendar semantics or
   persistent catch-up).
3. **Fault injection round (the core of this level).** Stage and
   repair, *in this order*, keeping notes as you go:
   - fill `/tmp` to 85% with a scratch file → watch healthcheck
     fire → resolve;
   - kill the app process ungracefully → watch `Restart=` recover
     it → time the recovery;
   - `chmod 000` the app's static asset directory → observe → fix
     → explain in one sentence why the unit *itself* stayed
     "running" (the difference between a healthy process and a
     healthy service).

## Part 3 — The 3 a.m. test (60 min)

1. Write `RUNBOOK.md` for your node: what runs where (from your
   baseline), the four queries, the healthcheck, the three fault
   procedures from Part 2 as playbooks (symptom → evidence → fix →
   verify), and the two-line "restart everything in order" section.
2. **Peer test:** swap runbooks with a classmate (or instructor
   script). They perform your healthcheck + one playbook *using
   only your runbook*. Their stumbling points become your v1.1
   — attach the corrected diff.
3. Incident note: one page on the fault that surprised you most —
   symptom, wrong hypothesis you actually held, the evidence line
   that killed it, the fix, the prevention.

## Rubric (10 pts)

| Pts | Requirement |
|---|---|
| 1 | Baseline evidence file complete |
| 1 | Part 1: three refusals captured + rollback documented |
| 1 | Part 2: queries.sh runs unmodified by a stranger |
| 1 | Part 2: timer with justification; healthcheck exits non-zero correctly |
| 2 | Part 2: three faults staged, observed, repaired, explained |
| 2 | Part 3: runbook passes the peer test |
| 1 | Part 3: v1.1 diff attached |
| 1 | Incident note in the five-part shape |

## Watch-for

- Opening the app port "to test" and forgetting to close: the
  second terminal's evidence must show it refused *after* locking —
  a rule you added then removed without re-verifying is a finding,
  not a fix.
- `Restart=always` hiding failures: the recovery *timing* you
  record is what distinguishes an operator from a user — anyone can
  wait for the green light; you must know how long it took and why.
