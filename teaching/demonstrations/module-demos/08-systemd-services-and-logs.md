# Demo 8 — systemd Services & Logs: Break, Read, Fix

> **Sessions:** S19 (break/fix) and S23 (the same failure read through
> journald) · **Duration:** ~12 min · **Risk:** low — a *user* unit in
> your demo VM; nothing system-wide · **Objective:** the full service
> failure loop — break a unit, read the state, query the journal,
> one-line fix — as a *repeatable method*, not a magic trick.

## Prerequisites

- Demo VM with systemd user session (any Ubuntu 24.04 VM)
- A tiny worker script for the service to run

## Setup (before class)

```console
$ mkdir -p ~/demolab ~/.config/systemd/user
$ cat > ~/demolab/ticker.sh <<'EOF'
#!/usr/bin/env bash
while true; do echo "tick $(date -Is)"; sleep 5; done
EOF
$ chmod +x ~/demolab/ticker.sh
$ cat > ~/.config/systemd/user/ticker.service <<'EOF'
[Unit]
Description=Ticker demo service

[Service]
ExecStart=%h/demolab/ticker.sh
Restart=on-failure

[Install]
WantedBy=default.target
EOF
$ systemctl --user daemon-reload
$ systemctl --user start ticker && systemctl --user status ticker --no-pager | head -6
```

Expected: `active (running)`, a PID, recent "tick" log lines.

## Procedure — S19 half: the break and the state

**Step 1 — break it (move the script).**

```console
$ mv ~/demolab/ticker.sh ~/demolab/ticker.sh.bak
$ systemctl --user restart ticker; sleep 3
$ systemctl --user status ticker --no-pager | head -6
● ticker.service - Ticker demo service
     Active: activating (auto-restart) (Result: exit-code)
```

*Narration:* "Read the state like a chart: `activating (auto-restart)`
— it *died*, and Restart=on-failure is *trying again*. The state tells
us the shape of the failure before we ask why."

**Step 2 — enable-vs-start, made visible.**

```console
$ systemctl --user is-enabled ticker
disabled
$ systemctl --user enable ticker      # creates the symlink in default.target.wants
Created symlink /home/dsstudent/.config/systemd/user/default.target.wants/ticker.service → ...
```

*Narration:* "`enable` wired the *boot graph* — nothing is running
because of it. `start` runs it *now*. Two graphs, two verbs." (If the
unit is currently crash-looping, stop it first: `systemctl --user stop
ticker`.)

## Procedure — S23 half: the journal reads the cause

**Step 3 — the journal names the exec failure.**

```console
$ journalctl --user -u ticker -n 8 --no-pager
... Failed at step EXEC spawning /home/dsstudent/demolab/ticker.sh: No such file or directory
```

*Narration:* "Quoted evidence, timestamped, from the unit itself. This
one line is the incident report's centerpiece — step 2 of the method
you'll drill in M32."

**Step 4 — the one-line fix and verification.**

```console
$ mv ~/demolab/ticker.sh.bak ~/demolab/ticker.sh
$ systemctl --user restart ticker && sleep 2
$ systemctl --user is-active ticker
active
$ journalctl --user -u ticker -n 2 --no-pager
... tick 2026-09-17T10:41:07+01:00
```

*Narration:* "Fix → **verify the original symptom is gone** — step 7 of
the method. 'It should work now' is not a state; `is-active` is."

## Expected output

Unit names/PIDs/timestamps vary; the state transitions and the EXEC
error shape are stable — read the shapes.

## Questions to ask

1. After step 1: "is the service running? Is it enabled? Are those the
   same question?"
2. After step 3: "which *step* of the incident method did we just
   complete?" (evidence gathering)
3. "What does `Restart=on-failure` cost us during the broken window?"
   (a crash-loop — the journal fills; mention M24's vacuum)

## Common errors & recovery

- `daemon-reload` forgotten after editing the unit → the old config
  ghosts around; the demo's edit is a file *move*, so reload is needed
  if you edit ExecStart live — say the rule when it applies
- `journalctl --user` empty on some lab images → lingering/session
  scope; `loginctl enable-linger $USER` or run from a real login shell
  (module lab covers both)
- `status` showing green while the script is broken → you broke the
  file but the *old* ExecStart path still resolves — restart before
  reading, or the demo's causality collapses

## Recovery

Full teardown is the recovery: stop, disable, remove unit + script,
`daemon-reload`. A snapshot is the faster path.

## Cleanup (census)

```console
$ systemctl --user disable --now ticker
$ rm ~/.config/systemd/user/ticker.service ~/demolab/ticker.sh
$ systemctl --user daemon-reload && systemctl --user reset-failed 2>/dev/null
$ ls ~/demolab   # confirm empty, then remove if only demo artifacts
```

## Optional extension

Add `RestartSec=10` and a rate-limit discussion (`StartLimitBurst`) —
why the *default* burst stops crash-loops after 5 tries; the LA-4
staged unit uses exactly this behavior.
