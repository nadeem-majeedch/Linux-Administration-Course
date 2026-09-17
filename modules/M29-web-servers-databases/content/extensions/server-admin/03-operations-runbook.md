# Lesson 3 — Operations: Runbooks, Reviews, and the Living Server

> Extension A · Server Administration · Difficulty: Advanced
> Reading time: ~25 min · Up next: [Configuration management concepts](04-config-management-concepts.md)
> Prerequisites: M24's monitoring kit, M25's hardening checklist, M29 core's runbook

---

## 1. Provisioning ends; operating begins

The lifecycle from lesson 1 spends most of its time in **operate** —
and operating is a *practice*, not a state. The practices, consolidated
from everything the course has built: **observe** (logs, monitoring),
**protect** (backups, security reviews), and — the one that binds them
— **document** (the runbook). A server whose operation isn't documented
is a server only its author can run, and authors leave.

## 2. The runbook: the server's operator's manual

M29 core wrote a runbook for one service. The fleet-grade version
covers the *machine*, and its template is worth memorizing:

```markdown
# Runbook — ds-analysis-01 (role: teaching analysis node)

## Identity & access
- Host: ds-analysis-01 · 10.0.2.15 · admin: ds (key-only)
- Fleet file: repos/fleet/README.md · provisioned by: v2.3 manifest
- Break-glass: console access via hypervisor host (M04's VirtualBox console)

## Services (what should be running, and how to tell)
| Unit | Port | Health check | Logs |
|------|------|--------------|------|
| jupyter.service (user: ds) | 127.0.0.1:8888 (tunnel) | `curl 127.0.0.1:8888` → 302 | journalctl --user -u jupyter |
| postgresql | 127.0.0.1:5432 | `pg_isready` | journalctl -u postgresql |

## Routine operations (exact commands, expected outputs)
- Start/stop Jupyter: `systemctl --user <cmd> jupyter` (as ds)
- Weekly check: `~/bin/health.sh` → outputs to logs/health/ (M24 kit)
- Backup: runs 02:15 (M19 timer); verify with `ls -lt backups/` (M24 §5)
- **Test-restore: quarterly, timed, logged** (the untested-backup rule)

## Failure playbooks (the drill cards, pre-answered for THIS box)
- Service down → drill card 6; this box: check journal tail, exit code,
  then venv (card 10 crossover)
- Disk filling → card 2; this box: outputs/ and journal are the growers
- Slow → card 1; four-instrument sweep, then fork

## Change log (append-only, by hand or by CI)
- 2026-09-20 v2.3 — added nightly pg_dump timer (M19/M29)
```

Three properties separate a runbook from a document: **commands are
exact and expected outputs are stated** (M24's evidence discipline);
**failure playbooks link the drill cards with box-specific facts**
(the method from M32-clinic, pre-localized); and **the change log is
append-only** — history is data, not narrative.

## 3. The operational calendar

Operating is scheduled, and the cadence matters more than the tooling:

| Cadence | Practice | Source |
|---|---|---|
| Continuous | logs consulted *on demand* (journalctl skills), health kit running | M24 |
| Daily | backup runs; its log line is checked in the morning glance | M24 §5 |
| Weekly | `df`/`docker system df`/`apt` security-review glance; convergence re-run of the manifest | M17/M28/this ext |
| Monthly | restore drill (timed!); package updates reviewed & applied | M24 §5/M16 |
| Quarterly | hardening checklist re-walk (M25); runbook accuracy check (every command still true?); fleet inventory verified | M25/this ext |

The monthly restore drill deserves its emphasis: it is the single
practice that separates professional operations from backup theater —
and it's *already scripted* from M24's exercises. The quarterly runbook
check is the same honesty applied to documentation: docs rot at the
speed of change; the calendar is the preservative.

## 4. Security reviews and the monitoring posture

The **security review** is M25's hardening checklist, re-walked
periodically and *against evidence*: `sudo -l` outputs per role, `ss
-tlnp` snapshot (nothing new listening), `ufw status` (policy as
declared), last-logins and sudo usage (`journalctl _COMM=sudo`,
M24's auth lesson), package counts (`apt list --upgradable`). Each
check produces a line in the review log — a pass, a finding, or a
ticket.

**Monitoring** at fleet level is the M24 kit plus reachability: the
health script runs *from* a different box (or the fleet file drives a
loop), because self-reported health is the liar's health. Even in this
course's single-VM world, the habit is established by running
`health.sh` from a cron *and* from a second context — the monitoring
lesson of clouds (Extension B) without any cloud.

---

## Key takeaways

- Operating = observe + protect + document, on a **calendar**, not on
  inspiration.
- The runbook is exact commands + expected outputs + localized failure
  playbooks + an append-only change log.
- The **monthly restore drill** and **quarterly runbook check** are the
  two calendar items that keep the other ten months honest.
- Security review = the M25 checklist re-walked *with evidence*;
  monitoring = the M24 kit run from *outside* the thing monitored.

## Check yourself

1. What three properties make a runbook operational rather than merely
   written?
2. Why should health checks run from a second context rather than the
   monitored box itself?
3. Your backup has run nightly for a year. What's the one calendar
   item that makes that claim meaningful, and what does it produce?
4. In the security review, why walk `ss -tlnp` and `sudo -l` with
   *saved outputs* rather than from memory?

*Answers:* (1) Exact commands with expected outputs; failure playbooks
localized to the box; append-only change log. (2) Self-reported health
shares the failure domain it reports on — a dead box reports nothing
(also: it can't see network-level failures); outside checks catch what
inside checks can't say. (3) The monthly timed test-restore; it
produces a logged RTO and a verification checksum — converting "we
have backups" into "restores work, in N minutes." (4) Because the
review is *evidence* (M24/M32-clinic discipline): saved outputs make
the review comparable over time and the findings arguable — memory
makes both impossible.

Up next: [Configuration management concepts](04-config-management-concepts.md) —
the tools that make policy executable.
