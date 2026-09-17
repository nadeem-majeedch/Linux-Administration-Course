# Module 27 Troubleshooting — Python, Jupyter & Data on Linux

> Ten patterns, ordered by how often they hit real students.
> Each: **symptom → likely cause → diagnosis → fix → prevention**.
> Every fix stays inside project-local venvs and loopback
> listeners; the escalation table sits at the bottom.

## 1. `ModuleNotFoundError: No module named 'pandas'`

**Cause:** the interpreter running your code is not the
environment you installed into — wrong venv, notebook kernel
bound elsewhere, or the install went to `~/.local` under a
different Python.

**Diagnosis:** in the *same context as the failure*, run
`python -c "import sys; print(sys.executable, sys.prefix)"`
and `which pip`. Mismatch between the two = you're installing
into A and importing from B. Inside a notebook:
`import sys; sys.executable` — is it your `.venv/bin/python`?

**Fix:** activate the right venv, or align the kernel
(`.venv/bin/python -m ipykernel install --user --name proj`),
then `python3 -m pip install pandas` *in that environment*.

**Prevention:** one venv per project, registered as the
notebook's kernel at project setup; never bare `pip`.

## 2. `pip` installs succeed but nothing imports — silently

**Cause:** classic split-brain: `pip` on PATH belongs to the
system (or another venv) while `python` belongs to the venv.
The install vanishes into the wrong site-packages.

**Diagnosis:** `which -a python pip` — list them all; then
`python -m pip --version` vs `pip --version`. Different
interpreters in the two outputs = confirmed.

**Fix:** always `python3 -m pip install …` (Q1's rule), or
`.venv/bin/pip` explicitly.

**Prevention:** shell alias discipline — after `source
.venv/bin/activate`, the *first* command you run in a new
terminal is `which python`, every time, until it's muscle
memory.

## 3. Jupyter starts, but the notebook has none of my packages

**Cause:** kernel/venv mismatch (Lesson 2 §3) — the server runs
fine; the *kernel* is a different interpreter.

**Diagnosis:** in the notebook: `import sys;
print(sys.executable)`. Not your venv? That's it. Cross-check
`jupyter kernelspec list`.

**Fix:** register the venv as a kernel and select it —
`~/proj/.venv/bin/python -m ipykernel install --user --name proj`.
(You may need `python3 -m pip install ipykernel` *inside the
venv* first.)

**Prevention:** register the kernel as step zero of every
project, before the first notebook exists (C3 rehearses it).

## 4. `curl http://<vm-ip>:8888` refuses — "is Jupyter really running?"

**Cause:** it's running and refusing *by design*: loopback-only
binding (Lab 2 §D) means the VM's LAN address has no listener.

**Diagnosis:** on the VM, `ss -tlnp | grep 8888` —
`127.0.0.1:8888` proves the posture is correct. From outside,
the connection refuse is the *expected* result.

**Fix:** none needed on the server — connect the intended way:
`ssh -L 9999:127.0.0.1:8888 ds@vm -N`, then browse
`127.0.0.1:9999` locally.

**Prevention:** treat "reachable from the LAN" as a bug, not a
goal. The tunnel *is* the access path (M22 + M25 echo).

## 5. Background Jupyter/training job dies when the SSH window closes

**Cause:** SIGHUP on session teardown — the process was tied to
the controlling terminal.

**Diagnosis:** the log ends exactly when the disconnect
happened; `ps aux | grep <name>` afterward finds nothing.

**Fix:** relaunch under a survivor: `nohup … > out.log 2>&1 &`
(short jobs), `tmux new -s train` (interactive/long jobs —
detach with Ctrl-b d, reattach from anywhere), or a proper
systemd unit for always-on services (M20 §3).

**Prevention:** *decide the survival strategy at launch*, not
after the first heartbreak. Rule of thumb: >5 minutes ⇒ tmux;
must-run-daily ⇒ timer (M19).

## 6. `Permission denied` writing into `data/raw/`

**Cause:** the read-only dataset guard working as intended —
mode bits (Lab 1 Part E / C5) reject the open-for-write.

**Diagnosis:** `ls -ld data/raw` (check w bit for *your*
identity) and `id` (are you in the owning group?); `namei -l
data/raw` finds which directory level actually denied — often
it's a parent, not the leaf.

**Fix:** if legitimate, write to `data/processed/` (that's what
it's for); if the guard is wrong, the *owner* adjusts it
deliberately (`chmod u+w` or group change), never via sudo
habit.

**Prevention:** directory contracts — `raw/` read-only,
`processed/` group-writable, `outputs/` published — enforced by
chmod, not convention (Q18).

## 7. Scheduled Python job silently never runs

**Cause:** one of the cron classics — sparse PATH (bare
`python`), relative paths, no `>> log 2>&1` so errors vanish, or
the script lost its executable bit.

**Diagnosis:** `grep CRON /var/log/syslog` (or
`journalctl -u cron`) for the invocation + exit; then the
`env -i HOME=$HOME PATH=/usr/bin:/bin /abs/path/script.sh`
rehearsal (Lab 3 §C). If it survives `env -i`, cron isn't the
problem.

**Fix:** absolute interpreter path
(`/home/ds/proj/.venv/bin/python`), absolute data paths, redirect
every scheduled line, `chmod +x`.

**Prevention:** the nightly-script checklist — hard paths, venv
interpreter by full path, log redirect, idempotent write —
applied *before* the crontab line is written (M19 §1).

## 8. Notebook output files vanish / notebook "loses" its changes

**Cause:** two usually-innocent mechanisms: (a) you saved in the
browser but a *second* Jupyter instance (old PID, still bound to
8888) served the session — your save landed in the other
process's root_dir; (b) autosave-vs-checkpoint confusion —
`.ipynb_checkpoints/` holds the last checkpoint, not your latest
save.

**Diagnosis:** `ps aux | grep -i jupyter` — more than one
process? `ls -la notebooks/.ipynb_checkpoints/` and compare
mtimes; `ss -tlnp | grep 8888` shows which PID owns the port.

**Fix:** kill the stale instance politely
(`kill $(cat jupyter.pid)` if recorded; SIGTERM the correct PID
otherwise), restart one server, reopen. Recover unsaved work
from the checkpoint copy if needed.

**Prevention:** one server per machine (kill before relaunch),
`root_dir` pinned in config (Lab 2 §A), and treat
`.ipynb_checkpoints/` as a safety net — commit real versions to
Git (M26), not checkpoint archaeology.

## 9. `env: ‘python’: No such file or directory` from a script

**Cause:** the script's shebang (`#!/usr/bin/env python`) or its
body calls bare `python` — which doesn't exist on Ubuntu's
system PATH (`python3` does), and cron's PATH is even sparser.

**Diagnosis:** `command -v python` in *your* shell vs in the
`env -i` rehearsal. Present interactively, absent under
`env -i` = environment dependence.

**Fix:** shebang points at the venv interpreter directly
(`#!/home/ds/proj/.venv/bin/python`) or the script is invoked as
`/path/.venv/bin/python script.py`; inside the script, no bare
`python` ever.

**Prevention:** venv-path shebangs for scheduled scripts,
`python3` for interactive one-liners — and `env -i` before every
crontab edit (Q16).

## 10. Disk fills up: `.venv`-sprawl and output creep

**Cause:** dozens of venvs × ~200 MB each, plus `outputs/`
accumulating nightly artifacts and Jupyter checkpoints — `df
-h` creeps toward 100% over a semester.

**Diagnosis:** `df -h` for the volume, then `du -xh --max-depth=1
~ | sort -h | tail` to find the biggest tree; inside a project,
`du -sh .venv outputs notebooks` splits environment vs
artifacts.

**Fix:** delete venvs of dead projects (`rm -rf` — the whole
point of `.venv` is disposability; `requirements.txt` rebuilds
it), archive or compress old outputs (`gzip` the stale
summaries), clear orphaned checkpoints.

**Prevention:** one project = one `.venv`, deleted with the
project; retention rule for `outputs/` (keep 30 nightly files,
M24 lesson 5); a weekly `du` glance is 10 seconds of hygiene.

## Escalation table

| Layer | Evidence command | Hands off / call for help when |
|---|---|---|
| Shell/env | `which -a python pip`, `echo $PATH` | Fixes need another *user's* files |
| venv | `python -m pip --version`, `pip check` | Resolver conflicts you can't reconcile → curate pins, ask |
| Kernel | `sys.executable`, `jupyter kernelspec list` | Kernel JSON corruption → re-register, don't hand-edit |
| Server | `ss -tlnp`, `ps aux`, `jupyter lab list` | Multiple users on one box → coordinate, don't kill blind |
| Cron | `journalctl -u cron`, `env -i` rehearsal | System crontabs (`/etc/cron.*`) → instructor |
| Storage | `df -h`, `du -xh --max-depth=1` | Shared volume >90% → tell the admin *before* deleting anything |

Related modules: [M18](../../M18-processes-jobs-signals/content/troubleshooting.md)
(signals), [M19](../../M19-scheduling-cron-timers/content/troubleshooting.md)
(scheduling), [M22](../../M22-ssh-remote-admin/content/troubleshooting.md)
(connectivity).
