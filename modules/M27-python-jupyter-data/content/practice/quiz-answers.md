# Module 27 Quiz — Answer Key

> Grading guide: Sections A–C are factual; D accepts any wording
> that demonstrates the *reasoning*. Command answers graded on
> "would it work if typed", not exact form.

## Section A — Python environments

**Q1.** `python3 -m pip` guarantees the pip that runs belongs to the
same interpreter that will import the package. Bare `pip` can
resolve to (1) a *different* interpreter's pip (another venv on
PATH first) — you install into the wrong environment — or (2) a
stale/user-scoped pip that installs into `~/.local` while your
script runs a venv. The `-m` form pins both ends to one binary.

**Q2.** Diagnosis order: (1) *wrong environment* — they installed into
a different venv/system than the notebook's kernel uses (`which
python` in each context); (2) *kernel/venv mismatch* — the notebook
is bound to a kernel whose Python isn't the venv's (Lesson 2 §3);
(3) *never actually installed* — the pip run failed silently or
went to `~/.local` under a different user. Check with
`python -c "import pandas; print(pandas.__file__)"`.

**Q3.** Freeze captures **every installed package with exact
versions**, including transitive dependencies you never named —
the full closure that makes `pip install -r` reproduce the
environment. Cost: brittleness with size — dozens of pinned lines,
some of which (build-time pins) may conflict on a future
reinstall; it's a snapshot, not a curated manifest. For
distribution, curate top-level pins and freeze only for true
reproducibility.

**Q4.** The venv's own interpreter lands at
`.venv/bin/python` (plus `.venv/bin/pip`). Resolution works by
(1) **PATH priority** — activation puts `.venv/bin` first, so
`python` and `pip` resolve there; and (2) **site-packages
isolation** — the venv's `sys.path` is constructed from its own
`pyvenv.cfg` and `lib/pythonX.Y/site-packages`, so imports never
reach the system site-packages.

**Q5.** It works because the venv is *self-contained*: invoking its
interpreter by full path uses that interpreter's `pyvenv.cfg`,
which points imports at the venv's site-packages — no activation
required. It's more reliable because scheduled jobs get a sparse
environment (no interactive PATH, no `source` shell, no
`deactivate` cleanup); a hard-coded interpreter path removes all
three failure points. This is the standard cron pattern
(M19 + Lab 3).

**Q6.** Reproducibility side: each project pins its own dependency
versions — project A can have pandas 2.2, project B 2.1, with no
crosstalk; a teammate recreating from `requirements.txt` gets
byte-identical versions. System-integrity side: the OS ships and
manages system Python via apt (`python3-apt`, update-manager
hooks); `sudo pip install` can shadow apt-installed modules and
break system tooling (PEP 668's externally-managed-environment
guard on modern Ubuntu exists precisely for this). Project-local
venvs keep both worlds clean.

## Section B — Jupyter on Linux

**Q7.** Because the lab's threat model is a shared/multi-user machine:
`0.0.0.0:8888` advertises an unauthenticated-by-default service on
every interface — anyone on the network can attempt the token
(brute-force, or token leakage in shared terminals). Loopback +
SSH tunnel means the *only* path in is an authenticated SSH
session ([M22](../../../M22-ssh-remote-admin/README.md)), and the
firewall never opens 8888 at all
([M25](../../../M25-security-firewall/README.md)).

**Q8.** The browser URL is *local to the physical machine*: your
browser talks to `127.0.0.1:9999`, which is the **SSH client's**
listening socket. `-L 9999:127.0.0.1:8888` splits into: *listen on
local port 9999* (client side) and *forward to 127.0.0.1:8888 as
seen from the SSH server* (the VM's loopback — which is exactly
where Jupyter is bound). The traffic rides encrypted inside the
SSH connection; Jupyter never sees a non-local client.

**Q9.** Kernels are bound to specific interpreters. A kernel
registered against venv A (pandas installed) and another against
system Python (pandas absent) will disagree — the notebook
*file* is portable but the runtime is not. Fix: register the
correct venv as a kernel
(`.venv/bin/python -m ipykernel install --user --name sales-analysis`)
and select it in Jupyter.

**Q10.** `nbconvert --to script` converts the notebook into a
runnable `.py`, which fits pipelines: versionable diffs, runnable
under cron/nohup, no browser dependency. It loses interactivity —
cell-by-cell state, inline plots, the exploratory loop — and any
magics or rich output that don't translate. The pattern: explore
in the notebook, productionize via nbconvert.

**Q11.** `ps aux | grep jupyter` finds the process but killing by
what grep matches is fragile (matches the grep itself, multiple
workers, wrong PID). Polite: record the PID at launch
(`echo $! > jupyter.pid`) and `kill $(cat jupyter.pid)` — SIGTERM
lets Jupyter flush checkpoints, close the SQLite journal, and
exit cleanly. Verify with `ss -tlnp | grep 8888` going quiet.

**Q12.** Notebooks are created relative to the **working directory of
the `jupyter lab` process** — run it from `~` and the browser
starts at `~`. `c.ServerApp.root_dir` pins that root to the
project directory regardless of where you launched from, which is
how the server-side config keeps notebooks, data, and outputs in
one coherent tree.

## Section C — processes, scheduling, permissions

**Q13.** Background jobs receive SIGHUP when their controlling
terminal's session ends (logout/SSH disconnect). `nohup` makes the
process immune to SIGHUP and redirects stdout to `nohup.out` (or
wherever you redirect), so it keeps running and keeps its output.
It changes *signal disposition*, not priority or scheduling —
that's why it's the lightest-weight survival tool before tmux
(M22 §4) or systemd units (M20).

**Q14.** `renice -n 10 -p <PID>` (or launch with `nice -n 10 python
big_job.py`). Nice *lowers scheduling priority*: the kernel favors
other runnable processes when CPU is contended, so interactive
users and other jobs stay responsive; it does **not** cap CPU —
on an idle box the job still gets 100%. `renice` on a running PID
is the move when a job is already underway and the box got busy
*after* launch. Note: unprivileged users can only *increase*
niceness (be nicer), not decrease — another least-privilege
echo.

**Q15.** In order: (1) `crontab -l` — is the line actually installed,
right user?; (2) `grep CRON /var/log/syslog` (or
`journalctl -u cron`) — did cron *invoke* it, and with what exit?;
(3) run the exact command via `env -i` with cron's sparse PATH —
does it fail outside the interactive shell?; (4) check the
redirect target exists and is writable (`>> outputs/cron.log`)
and that the script itself is executable and spelled absolutely.

**Q16.** `env -i` starts the process with *almost no environment* —
no interactive PATH, no aliases, no activated venv, no session
variables — which is precisely cron's world. It strips: (1) the
user's full PATH (scripts that call bare `python` fail);
(2) shell/session exports (venv state, API keys); (3) login-shell
profile sourcing. If the script passes `env -i`, it passes cron.
The three assumptions it kills: *PATH inheritance*, *environment
inheritance*, *interactive shell presence*.

**Q17.** `chmod 2750 data/` (or `chmod g+s data/` on an existing
`rwxrwx---` group dir) plus `chgrp research data/`: `rwxrws---`
— group read-write-execute, others nothing, **SGID** so new files
inherit the `research` group rather than the creating user's
primary group. (M13's shared-directory pattern applied to
datasets.)

**Q18.** Permission bits are enforced by the kernel at every open-for-
write — convention is enforced by memory. A write *attempt* fails
with EACCES regardless of which tool tries it, which is the only
guard that survives a tired 2 a.m. `pandas.to_csv("data/raw/x.csv")`.
It does not protect against the owner with sudo
(`sudo rm`/`sudo chmod` bypasses), or root — permissions are
policy, not jail. (This is why the lab pairs the chmod with a
backup: M24's rule.)

**Q19.** "pip installed it" is only true *for the environment pip
belonged to*. Jupyter sees packages through its **kernel's
interpreter** — if the kernel runs a different venv (or system
Python), the import fails no matter what pip did. Install into
the same venv the kernel was registered from, or re-register
`.venv/bin/python -m ipykernel install --user`.

**Q20.** The bundle: (1) the **log line** (`[timestamp] wrote …` in
`nightly.log`); (2) the **output artifact** (`summary-2026-…txt`
exists, right mtime); (3) the **exit evidence** (cron's log or
`systemctl status`/`journalctl` showing exit 0). It cannot prove
*correctness* — that the numbers are right, only that the job ran
and wrote. Correctness needs content checks (row counts, hashes),
which is why the challenge set adds them.

**Q21.** Truncate-then-rename writes the full summary to a `.tmp`
sibling and `mv`s it into place only on success. Guarantee: the
destination is *either* the previous complete file or the new
complete file — never a partial. `mv` within a filesystem is
atomic; a crash mid-write leaves the `.tmp` orphaned but the
published output untouched. For per-epoch checkpoints the same
idea becomes write-then-rename per checkpoint (checkpoint-6 is
never corrupted by a checkpoint-7 crash).

**Q22.** Three benefits, three concepts: (1) **isolation/repro** —
`.venv/` + `requirements.txt` make the environment a file
(Q1–Q5); (2) **permissions** — `data/raw` read-only, `outputs`
group-writable map the SGID/umask story (Q17) onto real research
hygiene; (3) **automation** — a fixed tree is scriptable:
`scripts/nightly_summary.sh` can find inputs and publish outputs
by convention, and `.gitignore` can exclude exactly the derived
artifacts (M26). One big folder gives none of these seams.

Check understanding in practice: [challenges.md](challenges.md) ·
Symptoms: [../troubleshooting.md](../troubleshooting.md)
