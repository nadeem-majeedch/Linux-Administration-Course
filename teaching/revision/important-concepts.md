# Important Concepts — The Exam-Grade List

> ~40 concepts the course's assessments actually probe, grouped by
> unit. Each entry: the **claim**, and a **self-check** you must be
> able to answer aloud. If a self-check takes > 30 seconds, that unit
> goes back on your practice list.

## Unit 1 — Foundations (M01–M04)

1. **Kernel vs user space** — the kernel owns hardware and runs in
   privileged mode; everything else (shell, python, systemd) is user
   space asking via syscalls.
   *Self-check:* when Python "writes a CSV to disk", who actually
   touches the platter?
2. **Everything is a file** — devices, sockets, process info exposed
   through the filesystem (`/dev`, `/proc`, `/sys`).
   *Self-check:* why does `cat /proc/cpuinfo` work like reading a file?
3. **Distro = kernel + userland + package philosophy** — Ubuntu
   (apt/.deb) vs Fedora (dnf/rpm); commands differ where userland
   differs.
   *Self-check:* which of `apt`, `dnf`, `pacman` would exist on a
   server you just SSH'd into, and how would you find out?
4. **The shell is a program, the terminal is a window** — bash parses
   your line; the emulator draws the pixels.
   *Self-check:* what's the difference between Ctrl-Alt-F3 (TTY) and a
   terminal-app tab?
5. **Boot is a relay race** — firmware → bootloader → kernel →
   systemd. *Self-check:* at which leg does networking come up?
6. **VM/WSL2 sandboxes** — a VM is a full machine behind a hypervisor;
   WSL2 is a real Linux kernel in a lightweight VM integrated with
   Windows. *Self-check:* why does the course forbid practicing
   `useradd`/partitioning on the host OS?

## Unit 2 — Command line (M05–M07)

7. **Path resolution** — absolute starts at `/`; relative starts at
   your cwd; `..` is a real entry; `~` expands to `$HOME`.
   *Self-check:* `cd ~/../..` — where do you land, and why?
8. **Globs are expanded by the shell, not the command** — `ls *.csv`
   becomes `ls a.csv b.csv` before `ls` runs.
   *Self-check:* what does `rm *` in the wrong directory do, and which
   two habits guard against it? (safety card!)
9. **Streams** — stdin (0), stdout (1), stderr (2) are separate
   channels; `>` redirects 1, `2>` redirects 2, `2>&1` merges.
   *Self-check:* why did `command > out.log` still show errors on
   screen?
10. **Pipes connect stdout→stdin only** — stderr bypasses the pipe
    unless redirected. *Self-check:* `grep x file.log | wc -l` —
    which messages never reach `wc`?
11. **Hard link = another name for an inode; symlink = pointer to a
    path.** *Self-check:* which survives if you `mv` the target across
    the filesystem, and why?
12. **Quoting rules** — single quotes = literal; double quotes allow
    `$` expansion; no quotes = glob + word-split.
    *Self-check:* `echo "$HOME"`, `echo '$HOME'`, `echo $HOME*` —
    three different outputs; predict them.

## Unit 3 — Scripting & automation (M08–M09)

13. **Exit status is the contract** — 0 success, non-zero failure;
    `$?`, `set -e`, and every `if`/`&&`/`||` read it.
    *Self-check:* why does `grep nope file; echo $?` print 1?
14. **`set -euo pipefail` is the safety net** — exit on error, error
    on unset vars, catch failures inside pipes.
    *Self-check:* what bug does `-u` catch that silent defaults hide?
15. **Quoting in scripts: always `"$var"`** — unquoted variables
    word-split and glob. *Self-check:* what happens with
    `rm "$DIR"/*` vs `rm $DIR/*` when DIR contains a space?
16. **Functions take `$1…` locally** — they make scripts testable and
    reusable. *Self-check:* inside a function, what does `$1` refer to?
17. **Traps run code on exit/signal** — cleanup, lock removal, log
    close. *Self-check:* write the trap that deletes a temp dir no
    matter how the script ends.

## Unit 4 — Identity & permissions (M10–M13)

18. **Permissions bind to inode, ownership to uid/gid** — chmod
    changes the mode bits; chown changes who they apply to.
    *Self-check:* which command moves a file from "ana:research" to
    "ana:staff" without touching mode bits?
19. **rwx on a directory ≠ rwx on its contents** — x on a dir is
    *traverse*; without it, even read can't reach paths through it.
    *Self-check:* `chmod 644 dir` breaks what, exactly?
20. **Numeric vs symbolic modes** — 640 = rw- r-- ---;
    `u+x`,`g-w` are relative. *Self-check:* convert `rw-r-----` both
    ways.
21. **umask subtracts from default modes** — 022 → files 644, dirs
    755. *Self-check:* which umask makes new files group-writable?
22. **SGID on a shared directory makes new files inherit the
    directory's group** — the shared-server pattern.
    *Self-check:* without SGID, whose *primary* group owns files Ben
    creates in the team dir?
23. **sudo grants audited, logged, per-command privilege** — vs `su`
    which swaps identity wholesale. *Self-check:* where is a failed
    sudo attempt recorded on Ubuntu?
24. **Least privilege** — give each actor the minimum rights needed;
    the anti-pattern is group-of-everyone-writable.
    *Self-check:* Elena needs read-only on results, write on her own
    folder — sketch the group+permission layout.

## Unit 5 — Software, storage, time (M15–M19)

25. **apt = dpkg + dependency + repo resolution**; `apt update`
    refreshes the *index*, `upgrade` installs.
    *Self-check:* why "update then upgrade", and what does the index
    contain?
26. **PATH is searched left to right** — first hit wins.
    *Self-check:* how do you find out *which* python3 runs, and which
    one would run if you prepended a venv bin?
27. **Block devices, partitions, filesystems, mounts** — lsblk shows
    the tree; a filesystem is unusable until mounted somewhere in the
    tree. *Self-check:* why can't you `ls /mnt/data` right after
    attaching a disk?
28. **df vs du** — free space on mounted filesystems vs space
    *walked* in directories. *Self-check:* name two reasons they
    disagree (deleted-but-open files, other filesystems, sparse files).
29. **cron inherits a minimal environment** — no `$USER` assumptions,
    no venv, often no `$HOME`-relative tools.
    *Self-check:* why does a script that works interactively fail in
    cron, and what's the two-line fix (absolute paths + PATH line)?
30. **Backups follow 3-2-1 and must be restore-tested** — an
    unverified archive is a hope, not a backup.
    *Self-check:* what does `tar -tzf` prove, and what does it
    *not* prove?

## Unit 6 — Services, network, security (M20–M25, M32)

31. **systemd units: want vs active** — `enable` wires boot,
    `start` runs now; both are needed for "runs now and at boot".
    *Self-check:* a service is active but won't survive reboot —
    which command did you forget?
32. **`status` is the front door; journal is the evidence** —
    `journalctl -u NAME -n 50 --no-pager`.
    *Self-check:* the unit fails in 3 seconds — name the exact
    command pair that shows why.
33. **Ports listen per-address** — `127.0.0.1:8888` is invisible to
    the network; `0.0.0.0:8888` is world-visible (then firewall!).
    *Self-check:* your Jupyter won't load from the laptop — which
    single ss line answers "is it even listening externally"?
34. **The six-rung ladder** — link → resolution → route → port →
    service → application, in that order.
    *Self-check:* `curl: (6) Could not resolve host` — which rung,
    which command next?
35. **UFW default-deny inbound + explicit allow** — the server's
    minimal exposure model.
    *Self-check:* after `ufw enable`, SSH drops. Why, and what
    should you have run first?
36. **SSH keys beat passwords; agent holds unlocks; config names
    hosts** — key auth, `ssh-agent`, `~/.ssh/config`.
    *Self-check:* what does `ssh -v` show first when a key is
    rejected — and which file on the *server* decides acceptance?
37. **rsync copies deltas; scp copies whole files** — and rsync's
    `--delete` mirrors deletions.
    *Self-check:* why is `rsync -avn` the mandatory first pass before
    any `--delete`?

## Unit 7 — Data science stack (M26–M29, M31)

38. **venv = isolation via PATH prefix** — `source bin/activate`
    prepends; the interpreter resolves through it.
    *Self-check:* `pip installed pandas but import fails` — the
    single command that reveals which python is running.
39. **Jupyter is a server; kernels are processes** — which explains
    stuck RAM after "closing" a notebook.
    *Self-check:* how do you find and kill a zombie kernel from the
    shell?
40. **Docker image = layers; container = process on those layers** —
    `-v` bind mounts put *your* data in; containers are disposable.
    *Self-check:* what disappears when a container is removed, and
    where must results live instead?
41. **Reproducibility = pinned deps + immutable data + recorded
    provenance** — requirements.txt, checksums, git history.
    *Self-check:* a teammate reruns your analysis and gets different
    numbers — list the three places the divergence hides.
