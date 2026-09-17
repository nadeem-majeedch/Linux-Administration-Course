# LA-4 — Service & Log Forensics (30 min)

> Assesses: M20 + M24 labs · 10 points · evidence transcript
> required. Setup: instructor-staged VM snapshot with one user-level
> unit `healthbot.service` that crash-loops and one bloated journal.

## Given

- `systemctl --user status healthbot` → `activating (auto-restart)`.
- The unit references `~/venvs/hb/bin/python`, but `~/venvs/hb` was
  rebuilt last night and `pyyaml` is no longer installed in it.
- `/var/log/journal` has grown to ~900 MiB from repeated
  crash-loop restarts over two weeks.

## Tasks

**T1 (4).** Identify *from the journal* why the unit crash-loops.
Quote the decisive line in your transcript. Do not open the unit
file until you have quoted it — journal-first is the graded habit.

**T2 (4).** Repair the unit to a steady `active (running)` state.
The correct venv exists at `~/venvs/hb2` (has pyyaml). Use the
right reload step so systemd picks up your edit, then show the
running proof.

**T3 (2).** Report the journal's disk usage before and after a
safe, tool-native reduction that keeps the last 7 days. State the
config file where a permanent cap would live.

## Rubric

| Points | Requirement |
|---|---|
| 1 | T1 uses `journalctl --user -u healthbot` (scope correct) |
| 1 | T1 decisive line quoted (`ModuleNotFoundError: pyyaml` or `203/EXEC`) |
| 1 | T2 edits unit + `systemctl --user daemon-reload` visible |
| 1 | T2 `is-active` proof (`active (running)`) |
| 1 | T2 least privilege: user-level fix, no sudo, no system-scope move |
| 1 | T3 `journalctl --disk-usage` shown before *and* after |
| 1 | T3 uses `--vacuum-time=7d` (or `--vacuum-size`) — not `rm` on journal dirs |
| 1 | T3 names `/etc/systemd/journald.conf` (or a drop-in) for the permanent cap |
| 1 | Transcript starts before first diagnostic command |
| 1 | No destructive shortcuts: nothing `rm`'d, no `history` edits |

## Common failures

- Jumping to the unit file first (T1 caps at 1/4 — the habit is the
  objective).
- `systemctl edit` at system scope for a user unit.
- "Vacuum" attempted with `find /var/log/journal -delete` — zero for
  T3, this exact anti-pattern is taught against in M24.
