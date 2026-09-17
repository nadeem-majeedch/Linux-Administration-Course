# Module 27 Challenges — Python, Jupyter & Data on Linux

> Eight challenges. Difficulty ramps from C1 (drills) to C8
> (design). Every challenge runs inside your own VM and every
> deliverable lands in `lab-log.md` (same evidence rule as
> M19/M22). Nothing touches system Python, `sudo pip`, or any
> port beyond loopback.

## C1 — Which Python? (drill)

Five terminals, five answers. From: (a) bare login shell, (b)
inside `.venv` activated, (c) `~/proj/.venv/bin/python` invoked
directly, (d) a `sudo -i` shell, (e) a cron-simulated
`env -i PATH=/usr/bin:/bin python3` — run
`which python; which pip; python -c "import sys; print(sys.executable, sys.prefix)"`.
Record all five; annotate *which* site-packages each `sys.prefix`
implies. **Stretch:** explain in one line each why (d) is the
dangerous one for pip.

## C2 — requirements.txt archaeology

A teammate hands you a `requirements.txt` with `pandas`,
`numpy`, `scikit-learn`, *no pins*. In a scratch venv, `pip
install -r` it today, freeze, and record the resolved versions.
Then "time travel": add `pandas==1.5.3` (an older line) and
`pip install -r` again into a *second* venv — observe the
resolver downgrade and what else moves with it. Deliverable: the
two freezes side by side + one paragraph on why "requirements"
without pins is a rumor, not a contract. (Safety: both venvs are
project-local; nothing system-wide is touched.)

## C3 — The kernel registry lab

Create two venvs: `venv-a` with pandas, `venv-b` without. Register
**both** as Jupyter kernels
(`ipykernel install --user --name a` / `--name b`). Start Jupyter,
open one notebook, switch kernels between a and b, and run
`import pandas` in each. Deliverable: transcript showing the
*identical notebook* succeeding and failing by kernel choice,
plus the `~/.local/share/jupyter/kernels/` listing that shows
what registration actually wrote. Cleanup: unregister with
`jupyter kernelspec uninstall`.

## C4 — Tunnel lifecycle automation

Script `tunnel.sh` (in your project's `scripts/`): starts
`ssh -L 9999:127.0.0.1:8888 user@vm -N` in the background,
records its PID, health-checks with
`curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:9999`
until 200/302 (max 10 tries), and on `stop` argument kills the
recorded PID. Deliverables: script + one full
start→health→stop→verify-closed cycle transcript. The skill:
background PIDs managed as *state*, not vibes (M18 + M22 §3).

## C5 — Data directory hardening

Take Lab 1's project: build `data/{raw,processed}` where `raw/`
is group-`research` with SGID and mode 2750, `processed/` is
2770, and `outputs/` is world-readable 755. As your user, drop a
file in each and list owner:group. Then `sudo -u qa bash` (the
Lab 1 QA user, in group `research`): write into `processed/`
(success), attempt write into `raw/` (denied), read from all
three. Deliverable: permission matrix table (dir × user →
rwx/-) + the `namei -l` output for one deep path
(`data/raw/sub/file.csv` — the traversal explainer from M13).

## C6 — Failure forensics on a batch job

Run Lab 3's nightly script, then sabotage it three ways, one at
a time, *capturing evidence each time*: (1) remove the CSV —
expect the `set -e` traceback and no promoted summary; (2) `chmod
-x` the script — expect cron's (or hand-run's) "Permission
denied" and *no log line*; (3) fill `outputs/` with a read-only
directory `summary.d/` colliding with the output name — observe
the `mv` failure. For each: the exact error, which layer caught
it (bash / kernel / Python), and the log evidence that would have
page-worthy details for a real incident (M24 §4 vocabulary).

## C7 — Large-file workout without the RAM myth

Generate a 2 GB synthetic CSV (e.g. shell loop + `head -c` on
repeated lines, or `python - <<EOF` writing in chunks — *not*
one giant string). Then compare three read strategies in a
notebook, timing each with `time` shell builtin or
`%%time` magic: (a) `pd.read_csv` whole file; (b)
`pd.read_csv(chunksize=100_000)` aggregation loop; (c) shell
pre-aggregation `awk -F, '{s[$1]+=$3} END {for (k in s) print
k, s[k]}' file.csv | head`. Deliverable: timings + peak RSS from
`/usr/bin/time -v` (or `ps` sampling) + one paragraph: where the
memory actually went and which strategy survives 100 GB.

## C8 — Design: the shared compute box (design challenge)

No execution required — a written design, the way M26/M29 cap the
other units. Six researchers, one Ubuntu GPU box, one shared
dataset tree, per-user venvs, Jupyter for each, nightly batch
aggregation, one backup. Specify: directory layout with owner:
group per level (M13), the permission modes and why (Q17), how
venvs avoid crosstalk (Q6), how each user's Jupyter binds and is
reached (Q7/Q8 — tunnels, no shared 8888), the nightly job's
scheduling and locking (M19 §3), and the backup's
schedule/restore-test plan (M24 lesson 5). Deliverable: the
one-page design + three risks you'd flag to the professor.

**Stretch** — personal cheatsheet: one page, `python3 -m venv`,
activation, freeze/recreate, ipykernel register, tunnel command,
cron+env-i rehearsal, SGID dataset mode. If it doesn't fit one
page, you don't know it yet.

---
*All challenges: own VM, loopback-only, no system packages, no
real datasets. Evidence in `lab-log.md`.*
