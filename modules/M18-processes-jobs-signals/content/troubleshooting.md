# Troubleshooting — Module 18

Symptom → cause → check → fix → prevention. Own VM/WSL2; on shared
servers, escalate per policy after diagnosing.

## 1. "My training run vanished" — no error, just gone

- **Cause:** OOM killer (Lesson 3 §5) — the silent exit.
- **Check:** `journalctl -k --no-pager | grep -i oom | tail`;
  `dmesg -T | grep -i oom | tail`
- **Fix:** prevent recurrence — chunk data, cap memory (systemd limit in
  M20), monitor RSS growth.
- **Prevention:** quote `available`, not `free`; set limits before the
  cliff.

## 2. `There are stopped jobs.` on exit

- **Cause:** a Ctrl-Z'd job still attached to the shell.
- **Check:** `jobs`
- **Fix:** `fg %1` then let it finish or Ctrl-C; or `kill %1`.
- **Prevention:** don't leave `T`-state jobs; `disown` what should
  outlive the shell.

## 3. Background job died overnight after closing SSH

- **Cause:** SIGHUP on session teardown (Lesson 2 §1).
- **Check:** re-run and observe; `pgrep` right after `exit` of a test
  session.
- **Fix:** `nohup CMD > log 2>&1 &` or `disown %1`; durable: tmux (M22)
  or systemd user service (M20).
- **Prevention:** overnight ⇒ never a bare `&`.

## 4. Ctrl-C doesn't stop the program

- **Cause:** handler traps SIGINT (jupyter: double-press), or it's in
  `D`, or you're in the wrong terminal.
- **Check:** its STAT (`ps -o stat -p PID`); does a *second* Ctrl-C work?
- **Fix:** trap-aware: follow the program's own exit path; `D`: fix I/O;
  else ladder: TERM → wait → KILL (Lesson 2 §4).
- **Prevention:** know each tool's exit ritual before the long run.

## 5. Machine slow, but top shows CPU mostly idle

- **Cause:** I/O wait (storage), not compute.
- **Check:** `wa` in top; `iostat -x 2 3`; D-state census.
- **Fix:** find the heavy writer (`iotop` if installed), pace it
  (renice/ionice), or move data (M17 storage).
- **Prevention:** sort large datasets on local disk, not NFS.

## 6. `renice: Permission denied` (lowering nice)

- **Cause:** unprivileged users can't *raise* priority (nice ↓).
- **Check:** `id -u` ≠ 0.
- **Fix:** `sudo renice` (your VM only) or restart pre-nicened.
- **Prevention:** design batch to launch at `nice -n 10` from birth.

## 7. Zombie count climbing

- **Cause:** a parent isn't reaping dead children (dataloader bug).
- **Check:** `ps axo pid,ppid,stat,cmd | awk '$3 ~ /^Z/'` — group by PPID.
- **Fix:** TERM the *parent* (children re-parent to init and get reaped);
  fix the code later.
- **Prevention:** in python, `subprocess.run()` (waits) over misused
  `Popen`.

## 8. Killed the "wrong" python with pkill

- **Cause:** unscoped pattern matched more than intended (VS Code, other
  kernels).
- **Check:** `pgrep -af` — always — before `pkill`.
- **Fix:** restart what died; nothing else to do.
- **Prevention:** scope (`-u`, `-f` with distinctive paths), or kill by
  PID from `pgrep` output after eyeballing it.

## 9. `kill: (PID) - No such process` but pgrep found it

- **Cause:** race — it exited between pgrep and kill; or you killed the
  *pgrep's* own match (self-match trap in pipelines).
- **Check:** re-run `pgrep -af`; note `pgrep -f "pgrep"` matches itself.
- **Fix:** usually nothing — the process is gone, which was the goal.
- **Prevention:** kill by exact PID captured in one step:
  `kill $(pgrep -f 'exact pattern')`.

## 10. htop shows 100% on one core only for a "parallel" job

- **Cause:** GIL-bound python or single-threaded I/O — the *code* is
  serial.
- **Check:** `1` in top; threads in `/proc/PID/status`; profile the job.
- **Fix:** real parallelism: multiprocessing/joblib, or vectorize; or
  accept I/O-bound reality (Lesson 3 §4).
- **Prevention:** benchmark a small slice before a 12-hour run.
