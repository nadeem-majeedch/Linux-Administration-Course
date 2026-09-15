# Lesson 2 — Job Control & Signals: kill, jobs, bg, fg, nohup

> Module 18 · Unit 5 · Difficulty: Intermediate
> Reading time: ~35 min · Lab: [Lab 2 — the signal handshake](../labs/lab-02-signal-handshake.md)
> Prerequisites: [Lesson 1](01-processes-inspection.md)

> ⚠️ **Safety first:** this lesson teaches killing processes — a normal,
> necessary skill with real blast radius. Two rules until the safeguards
> are habits:
> 1. **Never `kill -9` as your first move.** TERM first (§4); escalate only
>    on evidence.
> 2. **Check what you're about to signal:** `pgrep -a` before `pkill`;
>    verify the PID twice with `kill`. `pkill python3` in a shared Jupyter
>    server kills *everyone's* kernels — pattern-matched kills are
>    indiscriminate by design.

---

## 1. Job control: the shell's traffic lights

Your shell can run several **jobs** at once — processes it started and
tracks. Three keystrokes and four commands are the whole system:

| Action | What it does |
|---|---|
| `command &` | start a job *in the background* immediately |
| `Ctrl-Z` | suspend the *foreground* job (state `T`) |
| `jobs` | list the shell's jobs with numbers `[1] [2] ...` |
| `bg %1` | resume suspended job 1 *in the background* |
| `fg %2` | bring job 2 to the foreground |
| `disown %1` | detach job 1 from the shell (survives shell exit) |

Live demo, every step observable:

```console
$ sleep 300 &           # job 1: sleeps in background
[1] 5412
$ jobs
[1]+  Running    sleep 300 &
$ fg %1                 # bring it forward
sleep 300
^Z                      # Ctrl-Z: suspend it
[1]+  Stopped    sleep 300
$ jobs
[1]+  Stopped    sleep 300
$ bg %1                 # send it back, running
[1]+  sleep 300 &
```

`[1]+` — the `+` marks the most-recent job; `[1]` alone refers to it, so
`fg %1` and plain `fg` agree here.

**The two states a background job can surprise you with:**

- **Stopped jobs block shell exit.** `exit` with a stopped job → bash warns
  "There are stopped jobs." Resume or kill them first.
- **Background jobs die with the terminal by default.** Closing the
  terminal sends SIGHUP (§4) to its jobs. Two escapes: `nohup` (next) or
  `disown %1` *before* exiting. This is why overnight SSH jobs vanish —
  the fix below, the durable fix in M22 (tmux/screen).

### DS framing

`python3 train.py &` then closing the laptop = lost hours. The two-command
ritual `nohup python3 train.py > train.log 2>&1 &` is the *minimum*
survivable pattern — and the bridge to M19 (cron/systemd timers) where
jobs stop depending on your shell entirely.

---

## 2. nohup: surviving the hangup

`nohup COMMAND` runs COMMAND immune to SIGHUP; output that would go to the
terminal is redirected to `nohup.out` (append) unless you redirect it:

```console
$ nohup python3 train.py > train.log 2>&1 &
[1] 5480
$ nohup: ignoring input and appending output to...   # (only if unredirected)
$ jobs ; tail -f train.log      # watch progress; Ctrl-C stops *tail*, not the job
```

Anatomy: `nohup` (survive hangup) + `> train.log` (keep the evidence) +
`2>&1` (stderr too — [M09](../../../M09-pipes-and-redirection/content/lessons/01-stdin-stdout-stderr-redirection.md))
+ `&` (background). Each piece does one job; together they're the difference
between "it finished overnight" and "it died when I closed my SSH window."

`disown` after the fact: started a job *without* nohup? `Ctrl-Z`, `bg %1`,
`disown %1` — retroactive insurance. (`disown -h %1` marks it HUP-immune
without full detach.)

**Honest caveat:** `nohup` solves only the hangup signal. A reboot, an OOM
kill, or a logout that tears down the session differently still kills the
job. The sysadmin-grade answer is `tmux`/`screen` (M22) or a systemd
*user service* (M20) — nohup is the pocket tool, not the surgery.

---

## 3. Signals: how the kernel talks to processes

A **signal** is a tiny asynchronous message: a number with a name and a
conventional meaning. The kernel (or any process with permission — same
user or root) delivers them; the target either handles it, ignores it (if
allowed), or dies by default. Roughly: **kill -L** prints the table; these
five are the working vocabulary:

| Signal | Number | Default action | Meaning |
|---|---|---|---|
| SIGINT | 2 | terminate | *interrupt* — what Ctrl-C sends to the foreground job |
| SIGTERM | 15 | terminate | *please terminate* — the polite, catchable request; `kill`'s default |
| SIGKILL | 9 | kill | *die now* — cannot be caught, blocked, or ignored |
| SIGHUP | 1 | terminate | hangup — terminal closed; daemons often re-read config on it |
| SIGSTOP/SIGCONT | 17/19 | stop/continue | suspend/resume — the machinery behind Ctrl-Z / `bg` |

**Why TERM-before-KILL is not just politeness:** a process that receives
SIGTERM may flush buffered output, close database connections, save
checkpoints, release locks, delete its PID file, or tell its supervisor
"clean exit." SIGKILL permits none of that — buffers are lost, locks are
left held, a training run's last hours vanish. KILL is the fire axe:
reserved for a process *proven* to ignore TERM.

---

## 4. kill, killall, pkill: three delivery mechanisms

Despite the name, `kill` sends *any* signal, not just death:

```console
$ kill 5412              # SIGTERM to PID 5412 (polite)
$ kill -9 5412           # SIGKILL — last resort, evidence required
$ kill -INT %1           # SIGINT to job 1 (job syntax works!)
$ kill -l | head -3
 1) SIGHUP	 2) SIGINT	 3) SIGQUIT	 4) SIGILL	 5) SIGTRAP
```

**PID-based (`kill`) vs pattern-based (`pkill`, `killall`)** — the safety
hierarchy:

```console
$ pgrep -a -u $USER python3     # STEP 1: look before you leap
$ pkill -u $USER -f train.py    # STEP 2: pattern + user scoping
$ killall sleep                  # matches exact NAME; Ubuntu ships it
```

- `pkill -f` matches the *full command line* — powerful and dangerous:
  `pkill -f train.py` also matches `tail -f train.log`. Always `pgrep -af`
  first to see exactly who matches.
- Scope every pattern kill: `-u $USER` (yours only), `-P PPID` (children of
  a launcher). On a shared server, unscoped `pkill python3` is an incident.
- `killall` matches exact process *names* — safer than `-f` but still
  pattern-based; prefer PID kills when you have the number.

**The escalation ladder, stated as policy:**

```console
$ pgrep -a -u $USER train          # 1. identify
$ kill 5412                        # 2. TERM, wait 10–20 s
$ kill -KILL 5412                  # 3. only if still alive: KILL
$ pgrep -a -u $USER train || echo gone   # 4. verify
```

Zombies can't be killed (they're already dead); fix the parent or wait for
it to reap. `D`-state processes ignore everything — the problem is the
I/O, not the signal (Lesson 1 §3).

---

## 5. What Ctrl-C actually does (and when it doesn't)

Ctrl-C has no magic: the terminal driver sends **SIGINT** to the foreground
process *group*. Consequences worth knowing:

- A background job (`&`) does *not* receive it — Ctrl-C in the shell
  doesn't touch it. (Verify in Lab 2.)
- Programs can trap SIGINT: `jupyter` double-presses confirm; a python
  script with `except KeyboardInterrupt` chooses its own exit; `vim` just
  prints "Type :qa!".
- A `D`-state process ignores it; so does a process with SIGINT ignored.

So when Ctrl-C "doesn't work," the diagnosis is a question: is the
process trapping it, stopped, in `D`, or are you pointed at the wrong
terminal? (Full drill: Lab 2 §C.)

---

## Exercises (lab-log.md)

1. Reproduce the §1 demo verbatim, then: `sleep 60 &` twice, `jobs`, kill
   *only* job 2 by job spec (`kill %2`), and prove job 1 survived.
2. Explain in one sentence each: why `nohup ... &` without redirection can
   still annoy you (what file appears?), and why `2>&1` belongs in the
   ritual.
3. TERM a `sleep 300` of yours; then TERM a `sleep 300` *from a second
   terminal*. Note both succeed — same user. Now reason (no root): what
   stops you from TERM-ing another *user's* process? (Kernel permission
   rule from §3.)
4. `pkill -f` hazard hunt: start `tail -f train.log` and a script literally
   named `train.py`; show one command that matches both (`pgrep -af train`)
   and write the scoped kill that hits only the python one.
5. Why can't you `kill -9` a zombie? What *can* you do? (Two sentences.)
6. Design check: you're about to `pkill -f jupyter` on the university
   server to "restart my kernel." Write the safer three-command sequence.

## Check yourself before Lesson 3

- [ ] I can suspend, background, disown and re-foreground jobs by number.
- [ ] I can state TERM vs KILL vs INT and why the ladder exists.
- [ ] Every pattern kill I write is scoped by user and previewed by pgrep.
- [ ] I know why background jobs die with the terminal and three fixes.

## Further reading (official sources)

- `man bash` → section *JOB CONTROL*; `man 7 signal` (the full table)
- `man nohup`, `man pkill`, `man killall`
- GNU coreutils nohup manual: https://www.gnu.org/software/coreutils/manual/
