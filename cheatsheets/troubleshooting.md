# 19 — Troubleshooting

> Learn it: [The Troubleshooting Clinic](../modules/M32-linux-performance-troubleshooting/content/README.md) ·
> Lookup, not understanding — the method *is* the assessed skill.

## The eight steps (in order, every time)

| # | Step | Discipline |
|---|---|---|
| 1 | Define the problem | one sentence: what's broken, since when, who notices |
| 2 | Gather evidence | read-only commands first, timestamps noted |
| 3 | Identify the component | which layer owns the symptom (table below) |
| 4 | Form hypotheses | from evidence, not vibes; rank them |
| 5 | Test safely | reversible probes; staged faults in scratch space |
| 6 | Fix | the narrowest change that addresses the cause |
| 7 | Verify | **the original symptom must be gone** — not just "it looks better" |
| 8 | Document | symptom → decisive evidence → cause → fix → prevention |

Anti-patterns the clinic grades against: random restarts as
diagnosis; theories before facts ("it's always DNS" as a *first*
move); fixing symptoms while the cause lives on; no documentation.

## Which layer owns the symptom?

| Family | First evidence commands |
|---|---|
| Process | `pgrep -af NAME` · `ps aux` · `top` (state `D`/`Z`?) |
| Memory | `free -h` (available!) · `vmstat 1` (si/so) · `journalctl -k -g oom` |
| CPU | `top` (us/sy/wa) · `uptime` vs cores · `ps aux --sort=-%cpu` |
| Disk space | `df -h` · `du -xsh /*` · `lsof +L1` (deleted-open) |
| Disk I/O | `iostat -x 1` (await, %util) · `vmstat 1` (wa) |
| Network | `ip a` → `ip r` → `ping GW` → `ping IP` → `dig NAME` → `ss -tlnp` (in that order) |
| Service | `systemctl status U` · `journalctl -u U -n 50` · `systemctl cat U` |
| Identity | `id` · `ls -l` · `namei -l PATH` (which triad fails?) |
| Python env | `which python3` · `pip -V` · `import sys; sys.executable` |

## The classic signatures (recognize on sight)

| You see | It means |
|---|---|
| `df` full, `du` small | deleted-but-open file (`lsof +L1`) or unreadable-to-you files |
| load high + `wa` high | disk-bound, not CPU — find the writer |
| load high + 90% idle | D-state (uninterruptible I/O) tasks inflating load |
| works locally, refused remotely | loopback bind (`ss -tlnp`) or firewall — in that order |
| `Connection refused` | nothing listening (service dead) — not a network fault |
| name fails, IP works | DNS: `resolvectl status`, `/etc/hosts` |
| unit `activating (auto-restart)` | crash-loop — journal has the reason |
| works in shell, fails in cron | environment: PATH/cwd/rc-files (see [cron.md](cron.md)) |
| `ModuleNotFoundError` | interpreter ≠ environment (see [python-environments.md](python-environments.md)) |
| key auth fails after "I added it" | server-side permissions (`~/.ssh` 700, `authorized_keys` 600) |

## Evidence-first toolkit (read-only by default)

```console
$ date; uptime                       # when am I, how long has it been like this
$ dmesg \| tail -20                  # kernel's last words (OOM, device errors)
$ journalctl -p err --since -24h     # recent errors, all units
$ systemctl --failed                 # what's broken at a glance
$ last \| head                       # who logged in when
$ history                            # what did *we* just do
```

## Staging faults to *practice* safely (own VM only)

| Skill | Staged with |
|---|---|
| service crash-loop | user unit pointing at a missing interpreter |
| full disk that isn't | big file + background process holding it open (`lsof +L1`) |
| poisoned DNS | `/etc/hosts` entry (with a pre-staged undo) |
| phantom hang | `sleep`-loop process, nice-19, with a red-herring sibling |
| permission incident | second user account + `chown root:root` on a scratch file |

Every staged fault: pre-stage the **undo** before applying the
fault. The undo is part of the exercise.

## The incident note (your exit ticket)

```text
Symptom:    what was observed, when, who reported
Evidence:   the decisive command outputs, quoted
Hypotheses: what we considered, and what killed each wrong one
Fix:        the change, in one command block
Verify:     proof the original symptom is gone
Prevention: what detects this earlier next time
```
Fixes without evidence lines can't be reviewed; documentation is
step 8, not an afterthought.
