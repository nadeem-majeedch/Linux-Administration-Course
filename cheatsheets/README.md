# Cheatsheets — 20 Command References

> **What this is:** fast lookup *after* you've learned the material —
> the right syntax at the moment of typing, with the warnings that
> keep the command safe.
>
> **What this is not:** a course. Every sheet says so. If a command
> here surprises you, the lesson link at the top of its section is
> where understanding lives. The course's assessments are written
> specifically so this folder cannot pass them for you.
>
> **Conventions:** Ubuntu LTS is the primary target; commands that
> need privilege are marked `sudo` explicitly; a ⚠️ marks anything
> destructive, irreversible, or commonly miscast. Labs run in your
> own VM — these sheets assume nothing about other machines.

| # | Sheet | Covers | Module |
|---|---|---|---|
| 1 | [command-line.md](command-line.md) | terminal, navigation, history, help | M05 |
| 2 | [files-and-directories.md](files-and-directories.md) | file ops, paths, links, FHS | M06–M07 |
| 3 | [permissions.md](permissions.md) | chmod, umask, special bits, ACLs | M12–M13 |
| 4 | [users-and-groups.md](users-and-groups.md) | identity, sudo, user/group admin | M12, M14 |
| 5 | [processes.md](processes.md) | ps, top, jobs, signals, priority | M18 |
| 6 | [package-management.md](package-management.md) | apt, dpkg, repos, pip division | M16 |
| 7 | [text-processing.md](text-processing.md) | grep, sed, awk, sort, pipelines | M08–M09 |
| 8 | [networking.md](networking.md) | ip, ss, DNS, curl, diagnostics | M21 |
| 9 | [systemd.md](systemd.md) | units, lifecycle, user services, timers | M20 |
| 10 | [logs.md](logs.md) | journalctl, /var/log, rotation | M24 |
| 11 | [ssh.md](ssh.md) | keys, config, scp/sftp, tunnels | M22 |
| 12 | [bash-scripting.md](bash-scripting.md) | variables, tests, loops, functions | M10–M11 |
| 13 | [cron.md](cron.md) | crontab, timers, env traps | M19 |
| 14 | [storage.md](storage.md) | disks, filesystems, mounting, loopback | M17 |
| 15 | [git.md](git.md) | core loop, branches, remotes, hygiene | M26 |
| 16 | [python-environments.md](python-environments.md) | venv, pip, PATH, pinning | M15, M27 |
| 17 | [jupyter.md](jupyter.md) | servers, kernels, tunnels, hygiene | M27, M31 |
| 18 | [docker.md](docker.md) | images, containers, volumes, compose | M28 |
| 19 | [troubleshooting.md](troubleshooting.md) | the 8-step method, evidence ladder | M23-clinic |
| 20 | [data-science-linux.md](data-science-linux.md) | the DS working set on one page | M31 |

Per-unit quick references also live in
[`resources/cheatsheets/`](../resources/cheatsheets/) (broader,
unit-oriented); the safety card there
([`safety-card.md`](../resources/cheatsheets/safety-card.md)) pairs
well with sheet 19.
