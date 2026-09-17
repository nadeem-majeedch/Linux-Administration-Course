# Troubleshooting Practice — 12 Scenarios

> The exam format, in practice form: **symptom first**, *hint on
> request* (indent), and the **approach skeleton** — deliberately
> incomplete, because memorized answers don't survive contact with a
> real system. Practice each in your own VM: several are reproducible
> with a few safe commands.

## Boot the ladder first

Network problems: rung order is **link → resolution → route → port →
service → application** (M21 L5). Non-network problems: **evidence →
component → hypothesis → safe test → fix → verify** (M24 L4).

---

**S1.** Your script ran all night; this morning `df -h /` shows 99%.
> *Hint:* what did the script write, and where does output go when
> nobody's watching? (Two classic suspects: unbounded logs, and the
> deleted-but-open file — `lsof +L1`.)

*Approach:* quantify with `du -x -d2 /` → find the grower → check for
holders of deleted files before deleting → reclaim → verify threshold.

---

**S2.** `ssh lab` now says `Permission denied (publickey)`.
> *Hint:* three layers: does the key exist/decrypt, is it offered
> (`ssh -v` shows the offer), does the server accept it
> (`authorized_keys` perms must not be group-writable)?

*Approach:* `ssh -v lab` → watch the key offer → check server-side
`~/.ssh` perms 700 / `authorized_keys` 600 → test with `ssh -i` explicit key.

---

**S3.** The API unit restarts every 5 seconds, healthy for ~3.
> *Hint:* `systemctl status api` then `journalctl -u api -n 50
--no-pager` — a crash-loop with short uptime is an exec/import/exit
problem, not a resource one.

*Approach:* read the *first* failure's stack (not the restart noise)
→ classify: exec path? missing module? port already bound? → fix →
`systemctl is-active` + one request.

---

**S4.** `curl https://pypi.org` fails on the VM; `ping 8.8.8.8` works.
> *Hint:* ladder rung 2 — resolution. `resolvectl status`; is the
> DNS server reachable (`dig @ip pypi.org`)?

*Approach:* name resolution → resolver config → upstream reachability
→ only then touch proxy/hosts overrides.

---

**S5.** Cron job silent for a week; interactive run works fine.
> *Hint:* what differs in cron's environment — PATH, HOME, cwd, TTY?
> Which of your script's assumptions breaks first?

*Approach:* make cron observable: `* * * * * /abs/path/run.sh
>/tmp/dbg 2>&1` for one minute → read the error → fix with absolute
paths + PATH line → remove the debug line.

---

**S6.** Teammates report the shared dir is suddenly writable by
*everyone*.
> *Hint:* someone "fixed" a permission error with a broad flag.
> Audit first: `ls -ld`, then find the over-broad bits — and restore
> the *design* (SGID + group), not just the number.

*Approach:* identify scope (`find` by mode bits) → restore dir 2775 /
files 664 per design → set the shared umask policy → write the
one-line prevention note.

---

**S7.** Jupyter was closed, but RAM never came back.
> *Hint:* notebooks end; kernels persist. Who's holding it —
> `ps aux | grep jupyter`? Which PID outlived its notebook?

*Approach:* identify orphaned kernel processes → verify their
`--cwd`/ports → kill the specific PID → confirm memory returned.

---

**S8.** A container writes results nightly; results vanish sometimes.
> *Hint:* where does the process write inside the container, and what
> happens to the writable layer on recreate? Which `-v` line fixes it
> permanently?

*Approach:* inspect `docker inspect` mounts → distinguish bind mount
vs layer → add the explicit mount → re-run one cycle → verify on host.

---

**S9.** `git pull` says your local changes would be overwritten.
> *Hint:* what does `git status` say — staged? unstaged? Which two
> honest options exist (commit first / stash), and which preserves
> nothing?

*Approach:* status → decide keep/discard *from evidence* → commit or
stash → pull → pop/verify → never `checkout -- .` reflexively.

---

**S10.** `pip install` on the server: "externally-managed-environment".
> *Hint:* Ubuntu 23.04+ protects system Python (PEP 668). What is the
> sanctioned scope for your deps — and why is `--break-system-packages`
> the *last* resort?

*Approach:* create venv → source it → install inside → confirm with
`which python3` + `pip -V` paths.

---

**S11.** After `ufw enable`, your SSH session froze mid-command.
> *Hint:* default-deny inbound included *your* rule-less port 22.
> What must exist before enable on a remote box — and why do cloud
> consoles exist?

*Approach:* recover via console (or VM-local access) → `ufw allow
OpenSSH` first → re-enable → verify rule order with `ufw status
verbose`.

---

**S12.** The weekly rsync to the GPU box doubled in time this week.
> *Hint:* what did rsync *say* it sent (read the summary lines as
> data)? Deltas miss when mtimes churn — what rewrote every file?
> (A chmod -R, a re-download, an editor touching everything.)

*Approach:* read speedup/bytes summary → diff mtimes (`ls -l`) → find
the churner → `--checksum` for the affected tree → restore normal
schedule.
