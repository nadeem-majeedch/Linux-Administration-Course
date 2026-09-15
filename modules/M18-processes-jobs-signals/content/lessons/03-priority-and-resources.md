# Lesson 3 — Priority & Resources: nice, renice, and the Troubleshooting Playbook

> Module 18 · Unit 5 · Difficulty: Intermediate
> Reading time: ~30 min · Lab: [Lab 3 — the priority clinic](../labs/lab-03-priority-clinic.md)
> Prerequisites: [Lesson 1](01-processes-inspection.md), [Lesson 2](02-jobs-and-signals.md)

> 🔒 Safety: nice/renice are among the *safest* administrative tools — you
> can only *lower* your own processes' priority, never raise it. Nothing in
> this lesson requires sudo except one marked, optional check.

---

## 1. Scheduling in one paragraph

Linux preempts: the kernel interrupts programs thousands of times per
second and hands each CPU to whichever runnable process deserves it most.
"Deserves" weighs many factors, but for humans there's one knob: the
**nice value**, from −20 (most favored) to +19 (most deferred). Default 0.
Higher nice = *nicer to everyone else* = less CPU when machines get busy.
When the machine is idle, nice barely matters — scheduling only bites
under contention, which is exactly when servers misbehave.

Two facts make this safe to practice:

1. **Unprivileged users can only increase niceness** (be kinder) on their
   own processes. Lowering nice (demanding more) requires root — a small,
   elegant least-privilege rule.
2. Nice shifts *share*, not correctness. A nicely-behaved job still runs;
   it just yields during contention.

---

## 2. nice: launch politely

```console
$ nice -n 10 python3 preprocess.py &     # start pre-nicened
$ nice -n 10 bash -c 'while :; do :; done' &   # our CPU burner for labs
[1] 6001
$ ps -o pid,ni,cmd -p 6001
   PID  NI CMD
  6001  10 bash -c while :; do :; done
```

`NI` column = nice value. (Old scripts may show `nice --10` — double dash
for *negative*; requires root for negatives.)

### DS framing

Batch preprocessing, dataset conversion, thumbnail generation — anything
that can take its time — should start life at `nice -n 10`. It costs
nothing when the box is idle and saves everyone's interactive experience
when it isn't. On shared GPU/login nodes this is etiquette *and* often
policy; some clusters enforce it.

---

## 3. renice: change the deal mid-flight

```console
$ renice -n 15 -p 6001        # kinder: any user, own processes
6001 (process ID) old priority 10, new priority 15
$ renice -n 5 -p 6001         # greedier: NOT permitted
renice: failed to set priority for 6001: Permission denied
$ sudo renice -n 5 -p 6001    # root may (in your VM; think twice on shared boxes)
```

Also useful on a whole tree — the launcher and its dataloader children:

```console
$ pgrep -P 6001 | xargs -r sudo renice -n 10 -p     # children too
```

(`xargs -r` from [M09](../../../M09-pipes-and-redirection/content/lessons/02-pipes-chaining-substitution.md);
M19 automates this idea via cgroups/systemd, which supersede hand-renicing
for services.)

**Policy of thumb:** interactive things (desktop, editor, sshd) want nice
0 or better; batch wants +10; a runaway *diagnostic* job you can't kill
yet gets +19 while you investigate — renice is the brake pedal you press
before reaching for kill.

---

## 4. CPU & memory under the microscope (the diagnosis toolkit)

Lesson 1 taught the tools; here is what each is *for* when something's
wrong:

**top/htop:** is anything eating CPU right now? `P` sorts; `1` shows
per-core saturation; a single process pinned at ~100×N% is a serial job
using all cores it was given — or all cores it *found*, if you forgot to
limit it.

**load average vs %CPU:** load counts *runnable + uninterruptible* tasks.
On a 4-core box: load 4 with `wa`=0 → perfectly busy. Load 20 → queue
20 deep: everyone's latency suffers even if %CPU shows cores "busy."
High load + low CPU% + rising `wa` → the queue is `D`-state I/O waiters
(Lesson 1 §3) — a storage story.

**free -h / top M-sort:** RSS growth over time = leak or unbounded cache;
`available` shrinking toward swap = the cliff where OOM lives.

**iostat/vmstat (one-liners, no install on Ubuntu server):**

```console
$ vmstat 2 5          # si/so (swap in/out) nonzero = real memory pressure
$ iostat -x 2 3       # %util near 100 = the disk is the bottleneck
```

---

## 5. The OOM killer: memory pressure's exit door

When RAM *and* swap are exhausted, the kernel invokes the **out-of-memory
killer**: it scores processes (heavily weighting memory footprint and
recentness) and SIGKILLs the worst offender to save the system.

What you must know operationally:

- Victims die with no terminal message — the first symptom is usually
  *"my process vanished."* **Check the evidence:**
  ```console
  $ journalctl -k --no-pager | grep -iE "out of memory|oom" | tail
  $ dmesg -T | grep -i oom | tail
  ```
  A line like `Out of memory: Killed process 7312 (python3)` ends the
  mystery.
- The *victim* isn't always the *culprit* — the largest process at the
  moment of crisis dies, which may be your 40-GB notebook while the leak
  grew elsewhere.
- Prevention is capacity planning: `ulimit -v`/systemd limits (M20) cap a
  job before it caps the server; for Jupyter kernels, chunk the data
  before the kernel chunks you.

### DS framing

OOM stories are *the* classic shared-GPU-server support ticket: notebook
A loads a 60-GB dataframe, the kernel balloons, the OOM killer takes out
notebook B (unrelated, but big), and two people lose a day. The defenses —
chunking, limits, monitoring RSS growth — are processes management's
contribution to data ethics: don't destabilize shared infrastructure.

---

## 6. The troubleshooting playbook

When "the server is slow / my job died," walk this ladder — each step
takes seconds and eliminates a family of causes:

1. **Load & saturation:** `uptime`; compare load to cores. High load →
   step 2; low load + still slow → step 5 (waiting on *someone else*, e.g.
   NFS or a remote API).
2. **Who's burning CPU:** `top` (`P`). Mine at 100%: my problem. Theirs:
   renice/politics. Nothing pegged: skip to 4.
3. **Memory:** `free -h`, top `M`. RSS climbing → leak; swap growing →
   pressure; OOM lines in journal → §5.
4. **I/O:** `wa` in top; `iostat -x`; `D`-state census
   (`ps axo stat,cmd | grep ^D`). Disk saturated → the job is I/O-bound;
   no amount of CPU niceness fixes a slow disk.
5. **Not my machine:** network mounts, remote databases, throttled APIs.
   Load idle + job slow = look at what it *waits* on (`strace` is the
   scalpel — optional, `man strace`).
6. **The specific process:** `ps -fp PID`, `/proc/PID/status`, then the
   Lesson-2 ladder (TERM, wait, KILL) if it must die.

**The one-paragraph incident report these steps produce:** "Load 22/4
cores, python3 (PID 7312) at 380% CPU with RSS 38 GB, swap 4 GB and
growing; kernel OOM-killed PID 6888 at 14:02; mitigations: reniced 7312 to
+10, will chunk the dataframe and add a memory limit; monitoring via top
every 10 min."

## Exercises (lab-log.md)

1. Start two CPU burners: one plain, one `nice -n 19`. On a ≥4-core VM
   watch `top` (1). Now start a third *nice 0* — which two share the
   machine first, and why? Record the NI of each.
2. `renice` your own burner +5, then attempt −5 without sudo (capture the
   denial), then (optional, your VM) `sudo renice -n -5 -p PID`. Restore
   +19 before killing everything.
3. Explain why renice-before-kill is the better first move on someone
   else's borderline run (two sentences: what you preserve, what you
   risk).
4. Produce a load-vs-CPU mismatch: `iostat -x 2 3` during a `D`-heavy
   moment (copy a huge file while `top` runs). Report `wa` and `%util`
   together.
5. Simulate (safely!) a runaway: `nice -n 19 bash -c 'x=1; while :; do
   x=$((x+1)); done' &`. Playbook steps 1–2 against it. Then decide:
   renice or kill — and justify *from the numbers*.
6. Write your own 5-line "slow server" runbook card for your desk — the
   playbook distilled to what *you'll* remember.

## Check yourself before the labs

- [ ] I can launch a pre-nicened job and change its mind mid-flight.
- [ ] I can explain load vs CPU% and name the state that bridges them.
- [ ] I know where OOM evidence lives and what report to write after.
- [ ] I have a personal playbook order: load → CPU → memory → I/O.

## Further reading (official sources)

- `man nice`, `man renice`, `man 2 setpriority`
- `man vmstat`, `man iostat` (sysstat docs: https://github.com/sysstat/sysstat)
- kernel docs — OOM: https://docs.kernel.org/admin-guide/mm/ (and `man 7 proc` overview)
