# 9 — systemd

> Learn it: [M20 — systemd & Services](../modules/M20-systemd-services/content/README.md) ·
> Lookup, not understanding.

## The core verbs

| Command | Purpose |
|---|---|
| `systemctl start UNIT` | run it **now** |
| `systemctl stop UNIT` | stop it now |
| `systemctl restart UNIT` | stop+start (drops connections) |
| `systemctl reload UNIT` | re-read config without dropping (if the unit supports it) |
| `systemctl status UNIT` | state, PID, last log lines |
| `systemctl enable UNIT` | start **at boot** (creates wants/ symlink) |
| `systemctl disable UNIT` | remove from boot |
| `systemctl enable --now UNIT` | enable **and** start in one go |
| `systemctl is-active UNIT` / `is-enabled` | scriptable yes/no |
| `systemctl daemon-reload` | **after editing any unit file** |
| `systemctl list-units --type=service` | what's running |
| `systemctl list-units --failed` | what failed |
| `systemctl cat UNIT` | show the unit file on disk |
| `systemctl edit UNIT` | drop-in override editor (safe change path) |

`enable` ≠ `start`: enable writes the boot-graph symlink in
`/etc/systemd/system/multi-user.target.wants/`; start only acts on
the present. A service that "works but dies on reboot" is enabled-
but-not-started in reverse — usually never enabled.

## Reading a unit file

```ini
[Unit]
Description=Model API                     # human label
After=network.target                      # ordering hint

[Service]
User=svc-upload                           # who runs it (least privilege)
WorkingDirectory=/srv/app
ExecStart=/srv/app/venv/bin/python app.py # absolute path always
Restart=on-failure                        # crash → auto-recover
Environment=API_KEY_FILE=/etc/app/key     # secrets via file, not argv

[Install]
WantedBy=multi-user.target                # which boot target pulls it in
```

Restart values: `no` (default) · `on-failure` (non-zero exit/signal)
· `always` (even clean exits) · `on-watchdog`. `Restart=` hides
crashes from *you* while recovering — pair it with journal checks.

## User units — services without root

```console
$ systemctl --user start ds-agent         # note the --user scope
$ journalctl --user -u ds-agent
$ systemctl --user edit ds-agent
$ loginctl enable-linger                  # keep units after logout
```
Unit files live in `~/.config/systemd/user/`. ⚠️ Mixing scopes is
the classic error: a user unit is invisible to `sudo systemctl`.
`linger` is the difference between "works in my session" and
"works overnight" (Level-5 lesson).

## Targets (the modern runlevels)

| Target | Meaning |
|---|---|
| `multi-user.target` | normal full system, no GUI — default for services |
| `graphical.target` | multi-user + display manager |
| `rescue.target` | single-user repair |
| `getty.target` | logins |

| Command | Purpose |
|---|---|
| `systemctl get-default` | boot target |
| `systemctl isolate rescue.target` | ⚠️ switch now (drops everything else) |
| `systemctl list-dependencies UNIT` | the dependency graph |

## Anatomy of a boot (four acts)

Firmware (UEFI) → bootloader (GRUB2) → kernel + initramfs →
**systemd** as PID 1, starting units in dependency order. Services
start **in parallel** where dependencies allow — that's why
ordering hints (`After=`) exist and why "the network wasn't ready"
is a unit-dependency bug, not an excuse.

## Failure triage order

```console
$ systemctl status UNIT        # state + Result (exit-code/signal/timeout)
$ systemctl cat UNIT           # what is it actually running?
$ journalctl -u UNIT -n 50     # what did it say? (journal-first habit)
$ systemctl list-jobs          # boot/start hanging on what?
```
`status` decodes: `active (running)` · `failed (Result: exit-code)`
· `activating (auto-restart)` = **crash-loop**, go read the journal.
