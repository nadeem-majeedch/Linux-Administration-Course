# Lesson 1 — Processes & Inspection: ps, top, htop, pstree

> Module 18 · Unit 5 · Difficulty: Intermediate
> Reading time: ~35 min · Lab: [Lab 1 — the process zoo](../labs/lab-01-process-zoo.md)
> Up next: [Lesson 2 — jobs & signals](02-jobs-and-signals.md)

> 🔒 Safety: every command here *observes*; nothing you run in this lesson
> changes your system. Killing things starts in Lesson 2 — with safeguards.

---

## 1. What a process is

A **program** is a file on disk (binary or script). A **process** is that
program *running*: the kernel has loaded its code into memory, given it an
address space, and created the data structures that track it. One program
(like `bash`) can be many processes (one per terminal).

Every process carries:

- **PID** — process ID, the kernel's unique handle (recycled upward, wraps)
- **PPID** — parent PID: who started it. Orphaned processes are re-parented
  to PID 1 (or systemd's user manager in some setups)
- **UID/GID** — whose identity it runs as (links back to [M12](../../../M12-users-groups-permissions/content/lessons/01-identity-users-groups.md))
- **state** — running, sleeping, stopped, zombie (§3)
- **priority/nice** — scheduling weight (Lesson 3)
- **open files, memory maps, environment** — everything `lsof` and `/proc`
  can show you

Processes form a **tree**: the kernel starts PID 1 (systemd on Ubuntu),
which starts everything else. Your shell started your editor; your editor
started a linter. `pstree` (§6) draws this.

### DS framing

When you "run a training script," you spawn a process tree: bash → python →
worker threads (same PID) or dataloader subprocesses (child PIDs). Every
debugging question — *is it running? is it stuck? how much memory does it
hold? did it die quietly?* — is a process question.

---

## 2. ps: the snapshot tool

`ps` without options shows only *your* processes in *your* terminal —
historically useless for real work. Two option families exist (BSD and
System V); Ubuntu's `ps` accepts both. Learn two invocations and you're set
for life:

```console
$ ps aux | head -5
USER   PID %CPU %MEM    VSZ   RSS TTY  STAT START  TIME COMMAND
root     1  0.0  0.1 167392 11520 ?    Ss   09:00  0:02 /sbin/init splash
root     2  0.0  0.0      0     0 ?    S    09:00  0:00 [kthreadd]
dsstud 1843  0.4  0.9 412336 36864 pts/0 Ss 09:05  0:01 -bash
dsstud 2201  0.0  0.0  46340  3328 pts/0 R+  09:41  0:00 ps aux
```

- `a` — all users' processes; `u` — user-oriented columns; `x` — include
  daemons without a terminal (`?` in TTY)
- **RSS** = resident set size: actual RAM in KB. **VSZ** = virtual (mostly
  inflation). **STAT** = state, §3. **TIME** = total CPU time consumed —
  a python job at 400% CPU is *using four cores*, and TIME proves it.

The second incantation — a *tree for one command's family*:

```console
$ ps -ef | grep -v grep | grep jupyter
dsstud  5001  1843  2 09:30 pts/1  00:00:12 /usr/bin/python3 -m jupyter-lab
```

`-e` everything, `-f` full format (PPID column visible). The
`grep -v grep` dance avoids matching the grep itself.

**Targeted queries — the ones you'll actually use weekly:**

```console
$ pgrep -a python3              # find PIDs by name, show the command line
5001 /usr/bin/python3 -m jupyter-lab
$ ps -fp 5001                   # full detail for one PID
$ ps -u $USER -o pid,pcpu,pmem,etime,cmd --sort=-pcpu | head   # my busiest
$ ps -o pid,ppid,stat,cmd -p 5001 --forest    # one subtree, drawn
```

Note `--sort=-pcpu`: descending CPU. `-o` picks columns — this is the
bridge to Lesson 3's troubleshooting playbook.

---

## 3. Process states — reading STAT

The kernel moves processes between a handful of states; `ps` shows them
(plus modifiers) in the STAT column:

| Code | State | Meaning in practice |
|---|---|---|
| `R` | Running/runnable | on a CPU or queued for one |
| `S` | Interruptible sleep | waiting for an event (input, network, timer) — *most* processes, most of the time |
| `D` | Uninterruptible sleep | waiting on I/O that can't be interrupted — usually disk/NFS. A `D` process ignores signals; killing it is impossible until I/O returns |
| `T` | Stopped | suspended by job control (Ctrl-Z) or a signal |
| `Z` | Zombie | dead but not reaped by its parent — a booking that hasn't been cancelled |

Modifiers: `s` session leader, `l` multithreaded, `+` foreground, `<`
high priority, `N` low priority.

**The three states worth internalizing for DS work:**

1. Wall of `S` — normal. Servers *sleep* between requests; python sleeps
   waiting on data.
2. Wall of `D` — the machine has an I/O problem (dying disk, saturated
   NFS mount, thrashing swap). `top` will show I/O wait (§4).
3. `Z` accumulating — a parent is leaking children (bad dataloader code,
   a crashed jupyter kernel). Zombies hold PIDs, not memory; a *flood* of
   them is still a problem.

```console
$ ps axo pid,stat,cmd | awk '$2 ~ /^D/ {print}'    # who is stuck on I/O?
$ ps axo stat,cmd | grep -c ^Z                     # zombie census
```

---

## 4. top: the live dashboard

```console
$ top
```

Read it in three zones:

**Header line 1** — `load average: 0.52, 0.48, 0.44`: jobs waiting for CPU,
averaged over 1/5/15 min. Rule of thumb: compare to core count. 4 cores →
load 4.0 = saturated; load 8.0 = twice oversubscribed (Lesson 3 unpacks
load vs CPU%).

**Header line 3** — `%Cpu(s): 12.5 us, 2.1 sy, 0.0 ni, 84.9 id, 0.4 wa`

- `us` user CPU (your training loop lives here)
- `sy` kernel CPU (high = syscall-heavy workload)
- `id` idle; **`wa` I/O wait — CPU idle *because* disk is slow.** High `wa`
  + STAT `D` = an I/O story, not a compute story.

**Header line 4–5** — memory and swap. Memorize this interpretation:
*free RAM being low is normal and good* (Linux caches disk in "buff/cache");
what hurts is **swap in use and growing** while `available` shrinks.

**The task list** — columns as in `ps aux`, sorted by %CPU by default.
Keystrokes that matter (all in the man page, but these are daily):

| Key | Action |
|---|---|
| `M` | sort by memory (find the leak) |
| `P` | sort by CPU (default) |
| `1` | expand per-core CPU bars |
| `u` | filter to one user |
| `k` | send a signal to a PID (Lesson 2) |
| `r` | renice a PID (Lesson 3) |
| `z`,`c` | color; full command path |

`htop` is `top` with arrows, colors, tree view (`F5`), search (`F3`), and
mouse support:

```console
$ sudo apt install htop     # if missing (M16 covers apt in depth)
$ htop
```

Use `top` everywhere (always installed), `htop` for thinking.

---

## 5. CPU & memory usage — the numbers that matter

**CPU% per process can exceed 100** — it's normalized to *one* core. A
dataloader at 400% occupies four cores. `ps aux` `%CPU` is a *lifetime
average* since start; `top`'s is current. A stalled job that burned CPU
early shows high in `ps`, low in `top` — check both before declaring a
process dead.

**Memory:** RSS is the working set. For python, watch RSS growth over time
in `top` (`M` sort): a slow climb from 2 GB → 14 GB during training is a
leak or an ever-growing cache list. The other number: `top` header's
`avail Mem` — the honest "can I start another job?" figure.

**Quick one-shots without top:**

```console
$ uptime                     # load averages
$ free -h                    # RAM/swap, human units
$ ps -o pid,rss,cmd -p 5001  # one process's RSS in KB
```

`free -h`'s `available` column (≈ what's usable without swapping) is the
number to quote in incident reports — not `free`.

---

## 6. pstree: seeing the shape

```console
$ pstree -p | head -12
systemd(1)─┬─ModemManager(742)─┬─{ModemManager}(758)
           │                   └─{ModemManager}(763)
           ├─sshd(918)───sshd(1843)───bash(1844)───python3(5001)─┬─...
           └─ ...
$ pstree -p 5001              # just the jupyter subtree
```

- PIDs in parentheses (`-p`).
- Brace notation `{name}(tid)` = threads of the same process.
- **Debugging gold:** "why are there 40 python processes?" — `pstree -p`
  shows whether it's 40 independent jobs or one launcher with 39 dataloader
  children. Killing the parent (Lesson 2) vs each child is a different
  operation with different consequences.

---

## 7. /proc: where ps gets its facts (a two-minute peek)

Everything above reads the **/proc** virtual filesystem. Each PID gets a
directory of live kernel state:

```console
$ ls /proc/5001/ | head
$ cat /proc/5001/status | grep -E "State|VmRSS|Threads"
State:	S (sleeping)
VmRSS:	   2874452 kB
Threads:	14
$ cat /proc/5001/cmdline | tr '\0' ' ' ; echo
```

`cmdline` is NUL-separated — hence the `tr`. You will rarely need /proc
directly, but knowing `ps` and `top` are *frontends* to it demystifies
both — and it's the fallback when a process is too broken for tools to
summarize.

---

## Exercises (lab-log.md)

1. Run `ps aux | head -1` to see the header, then find: (a) the process
   with the highest TIME, (b) any process in state `D` or `Z`. Explain each
   finding in one sentence.
2. Start `python3 -m http.server 8765` in a second terminal. In the first:
   find its PID with `pgrep`, show its subtree with `pstree -p`, and report
   its RSS from `ps -o rss`. Stop the server with Ctrl-C *in its own
   terminal* (mechanism explained in Lesson 2).
3. In `top`: press `1`, then `M`. Which process holds the most RSS? Is it
   yours or a system cache consumer?
4. Explain the difference between `ps aux`'s %CPU and `top`'s — and give
   one scenario where each gives a misleading picture alone.
5. A colleague says "the server has no free memory!" — `free -h` shows
   `free: 212 Mi, available: 11 Gi`. Write the two-sentence correction.
6. (Stretch) In `/proc/1/status`, find the state and the `Name`. Why is
   PID 1 special? (One sentence now; systemd formalizes it in M20.)

## Check yourself before Lesson 2

- [ ] I can find any process by name and get its PID + full command.
- [ ] I can explain R/S/D/T/Z and name the two that indicate trouble.
- [ ] I know what `wa` in top means and what it implies.
- [ ] I know RSS vs free vs available, and which to quote when.

## Further reading (official sources)

- `man ps`, `man top`, `man htop` (project page: https://htop.dev/)
- `man 5 proc` — the /proc filesystem
- procps-ng upstream: https://gitlab.com/procps-ng/procps
