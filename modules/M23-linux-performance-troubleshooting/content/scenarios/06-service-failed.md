# Drill Card 6 — "Service Failed"

> Scenario family: Services · Difficulty: ●●○
> Source modules: [M20](../../../M20-systemd-services/README.md), [M24 lesson 1](../../../M24-logs-journald-monitoring/content/lessons/01-journald-journalctl.md)

## Symptom

`systemctl --user status X` says *failed*, or the service is "active"
but not serving (which is card 12's composite), or it died overnight
and nobody knows when.

## Decision tree

```text
systemctl --user status X
├─ failed (exit code?) → journalctl -u X: WHY did it exit?
├─ activating (loop?)  → start-limit hit; journal shows crash-restart cycle
├─ active but dead port → card 12 (serving vs running)
└─ inactive (dead)     → enabled? Wanted-by whom? Who stopped it?
```

## Evidence

```console
$ systemctl --user status myapi.service          # state, exit code, recent lines
$ journalctl --user -u myapi.service -n 50 --no-pager   # the exit's own words
$ journalctl --user -u myapi.service --since -24h   # timeline: when did it die?
$ systemctl --user cat myapi.service             # the unit as-is (ExecStart, deps)
$ systemctl --user list-dependencies myapi.service  # did a dependency die?
```

Read the exit code as a clue family (M28's decoder, service edition):
**1** = the app said no (config/code — the journal tail says exactly
what), **137** = SIGKILL (OOM? cgroup? — card 3's verdict), **203** =
ExecStart path/exec-bit wrong, **start-limit** = crash loop, the
*policy* kicked in.

## Fix pattern

- **Config/code exit (1)**: the journal's last lines are the error;
  fix the config, pin the dependency (M27), `daemon-reload` if the
  unit changed, restart, *watch the first ten log lines*.
- **203**: `ExecStart=` must be absolute and executable — the venv
  python by full path is the course pattern (M19 §1's lesson in a
  service costume).
- **137**: memory — fix the workload or add the cap (card 3).
- **Crash loop**: `systemctl --user reset-failed X` after the real fix
  — clearing the limit *is* part of the restart.
- **Died silently overnight**: check `journalctl --since` timeline for
  the trigger (a 02:15 backup? an OOM? a dependency's restart?).

## Verify

Three layers, in order: unit *active*; port *listening* (`ss -tlnp`);
**and the actual work works** (`curl` the endpoint / run the job).
Then the overnight question: what would catch this at 02:30 instead
of 09:00? (A timer'd health check — M19's timer pattern + M24's
health.sh.)

## Document

Quote the exit code and the journal's final error line. Root-cause
vocabulary: *"venv recreated without pandas (no pin)"*, *"relative
ExecStart"*, *"dependency restart race"* — each maps to a prevention
(pin, absolute paths, healthcheck).

**Done when:** you've driven one of *your own* M20 user units to
failure and back, with the exit code decoded and the journal quoted.
