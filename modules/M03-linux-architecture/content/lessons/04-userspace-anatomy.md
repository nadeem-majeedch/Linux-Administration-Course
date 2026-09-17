# Lesson 4 — User-Space Anatomy: what runs when you type

> Module 03 · Unit 1 · Difficulty: Intermediate
> Reading time: ~20 min · Lab: [Lab 1](../labs/lab-01-anatomy-tour.md)
> Up next: [Mini-review + practice](../practice/quiz.md)

---

## 1. The cast behind every keystroke

Type `ls -l /tmp` and, in microseconds:

1. **bash** parses the line; `-l` and `/tmp` become argv
2. bash finds the executable via `$PATH` → `/usr/bin/ls` (M15)
3. bash asks the kernel to fork + exec it (Lesson 2's boundary)
4. the kernel loads `/usr/bin/ls`, finds `PT_INTERP` → the **dynamic
   loader** (`ld-linux.so`) runs first
5. the loader maps **shared libraries** (`libc.so.6` at minimum; see
   `ldd`), resolves symbols, jumps to `main`
6. `ls` calls libc → syscalls → kernel → your listing

Four user-space actors: **shell** (parser/dispatcher), **executable**
(the program), **dynamic loader** (stagehand), **shared libraries**
(the toolkit). The kernel just gave the process a sandbox and waited.

## 2. Inspecting the cast, safely

```console
$ type -a ls                          # shell layer: alias/function/file?
$ echo $PATH | tr ':' '\n' | head     # search order (M15)
$ file /usr/bin/ls                    # "dynamically linked" = needs loader+libs
$ ldd /usr/bin/ls                     # the library list (never ldd untrusted binaries)
$ ls -l /usr/bin/python3              # a symlink chain: python3 → python3.12
$ readlink -f /usr/bin/python3        # resolve it to the real file
```

- `file` says `dynamically linked` for most things; a `statically
  linked` binary carries its toolkit inside (busybox-style) — smaller
  surface, no loader.
- **Why `ldd` on untrusted binaries is dangerous:** it works by
  running the binary's loader in a probe mode; a malicious ELF can
  abuse that. On your own VM with distro binaries: fine.

## 3. Shared libraries: one copy, many tenants

`.so` files are mapped read-only into each process that needs them —
ten notebooks can share one `libpython` mapping. Two consequences:

- **Updates are atomic per file** but running processes keep the old
  mapping until restart — why "you updated it, why is the old version
  running?" ends with "restart the daemon" (M20).
- **Breaking a library breaks every tenant at once** — the fear
  behind M16's advice: system packages update *as one consistent
  set*; don't hand-patch `/usr/lib`.

Peek at the load map of a *running* process (read-only):

```console
$ less /proc/self/maps     # q to quit; every .so your shell mapped
```

## 4. Services: user space that outlives your login

So far, actors die when your shell closes. **Daemons** (sshd, journald,
your future Jupyter server) are user-space processes supervised by
systemd — they use the same loader, the same libc, the same syscall
wall; they're only distinguished by *who starts and reaps them*
(PID 1, M20) and by having no controlling terminal.

Evidence trail on your VM:

```console
$ systemctl --no-pager --type=service --state=running | head
$ ps -o pid,ppid,user,cmd -C systemd-journald   # who owns the daemon?
$ cat /proc/1/comm                              # Act 4's star, alive
```

## 5. The failure modes each actor owns

| Symptom | Likely actor | Evidence |
|---|---|---|
| `bash: xyz: command not found` | shell + `$PATH` | `type -a`, `echo $PATH` (M15/M27) |
| `error while loading shared libraries: libX.so: cannot open` | loader/libs | `ldd`, `ldconfig -p \| grep X` |
| `Permission denied` on exec | kernel mode bits | `ls -l`, mount `noexec` (M13/M17) |
| wrong Python runs | shell/PATH/symlink chain | `type -a python3`, `readlink -f` (M27) |
| service won't start | init supervision | `systemctl status`, `journalctl -u` (M20/M24) |

That table is the module in one breath: every "weird Linux behavior"
is one of these actors misbehaving — and each names its own evidence
command.

## 6. DS connection

A "broken environment" (M27's classic) is user-space anatomy: the
*shell* resolved a different `python3` than the notebook's kernel;
the *loader* then mapped that interpreter's libraries. Every fix
(`which python3`, venv activation, `readlink -f`) is an actor-check
from this lesson. When you later *package* an environment (Docker,
M28), you are shipping exactly this cast — interpreter, loader,
libraries — as an image.

---

**Key takeaways**

- Typing a command exercises: shell → PATH → fork/exec → dynamic
  loader → shared libs → syscalls.
- `type -a`, `file`, `ldd`, `readlink -f`, `/proc/*/maps` inspect
  each actor without changing anything.
- Daemons are ordinary user-space processes with PID 1 as a parent —
  same wall, same tools.

**Check yourself:** `python3` runs, but `import numpy` says "No module
named numpy." Which *actors* could be responsible, and what one
command distinguishes them?

**Next:** [practice/quiz.md](../practice/quiz.md) — then
[labs/README.md](../labs/README.md).
