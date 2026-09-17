# Final Examination — Answer Key & Grading Guide

> For instructors. Student paper: [final.md](final.md).
> Bracketed [keywords] must appear; wording is free.

## Section A (30 pts — 3 each)

**A1.** [`systemctl enable`] — creates the [symlink in
`/etc/systemd/system/multi-user.target.wants/`] that pulls the unit
into the boot dependency graph. `start` only runs it now; nothing is
written about the future.

**A2.** (1) [deleted-but-open files] — a process holds the fd, space
freed only at exit: `lsof +L1` (or restart the holder); (2) [`du`
as-root gap] — files unreadable as your user are under-counted:
re-run `sudo du -xsh /`. Separator: run both fresh and compare;
`df` counts blocks, `du` counts visible files.

**A3.** The messages are in the journal under a different unit or
identity than you think, or you're reading the *system* journal for
a [user-level unit]. Flag pair: `journalctl --user -u myapp`
(run as that user) — and `journalctl _UID=$(id -u)` as the
identity-level fallback.

**A4.** The app is bound to [loopback only]. Fix: reconfigure the
app to bind `0.0.0.0` (or the LAN address) *in its config*, restart.
Rule: `ufw allow` opens the door, but the listener must be standing
in the doorway — bind address governs who can even reach it.

**A5.** Diagnosis order: (1) [`PATH` differs] — cron's minimal
env lacks your directories; (2) [relative paths] — cron's cwd is
`$HOME`, not your project; (3) [shell/rc files never sourced] —
venvs/aliases/`~/.bashrc` exports absent (also: `MAILTO`/output
never checked). Evidence-first: log stderr+stdout from the cron
line before theorizing.

**A6.** `crontab -r` [erases the whole crontab with no prompt and no
undo]. Habit: [`crontab -e` only, plus `crontab -l >
~/crontab.backup` after every edit] (accept: keep crontab in Git and
reinstall from the file).

**A7.** Mechanism: [rsync's delta algorithm + mtime/size quick
check] — unchanged files transfer zero bytes. Poor choice for:
[atomic versioned backups / tamper-evident archives] — rsync
*mirrors* deletions and corruption from the source on the next run
(accept: ransomware/accidental `rm` propagates; snapshots/Borg-style
dedup retain history).

**A8.** Bind mount: [live host path, no copy] — right when the
partner must see edits immediately; also where the data already
lives. Named volume: [managed, container-owned, snapshot-friendly].
For **read-only** sharing: [bind mount with `:ro`] — zero
duplication and the `ro` contract is enforced by the runtime.

**A9.** Load counts [runnable + uninterruptible (D-state) tasks],
not CPU time; with 90% idle the queue is [blocked on I/O], not
compute. Confirmation: the [`wa` column in `top`/`vmstat`] — high
`wa` + high load = disk wait, not CPU saturation.

**A10.** Order with `ssh -v`: (1) [wrong key offered] —
`debug1: Offering…` shows *which*; (2) [permissions wrong] on `~/.ssh`
(700) or `authorized_keys` (600) — sshd silently refuses; (3)
[sshd config] restricts the user (`AllowUsers`, `PubkeyAuthentication
no`) or the key isn't actually in the file (trailing whitespace /
wrong user). Accept any defensible ordering if the checks are the
right three.

## Section B (30 pts — 5 each)

**B1.** Component: [Python environment of the service]. Decisive
line: `ModuleNotFoundError` — the unit's `ExecStart` venv lacks
pandas (wrong/bare interpreter). Fix class: correct the
`ExecStart`/`Environment` to the intended venv, `daemon-reload`,
restart — or install the dependency *into that venv*.

**B2.** Component: [memory + swap exhaustion]. Decisive line: the
kernel OOM kill (`Killed process … (python3)`) with swap 100% used
and `available` 55M. Fix class: cap or split the workload (ulimit,
smaller batch), add memory/swap headroom, or schedule the job
off-peak — not "buy RAM" as the first answer.

**B3.** Component: [DNS resolution / DHCP-learned resolver]. Decisive
line: `no servers configured`. Fix class: restore resolver config
(`resolvectl dns <iface> …` or fix the netplan/network source) —
ping was never a connectivity test here; the name simply can't be
resolved.

**B4.** Component: [sshd-side key acceptance]. Decisive line:
server echoes `publickey,password` but rejects the offered key. Fix
class: server-side `authorized_keys`/permissions/`sshd_config`
audit on the account you're hitting — client is doing its job
(offering) and being refused.

**B5.** Component: [disk I/O saturation]. Decisive line: `%util`
99.5 with await 180 ms and 4 KB average request — a small-random-I/O
workload pegging the disk. Fix class: find the writer
(`iotop`/`pidstat -d`), batch or cache the workload, move hot data
to faster storage.

**B6.** Component: [the service behind the port]. Decisive line:
`ss` shows *no listener* while the unit is in
`activating (auto-restart)` — crash loop, so nothing to connect to.
Fix class: read the unit's journal for the crash reason; connection
"refused" was a symptom, not a network fault.

## Section C (20 pts — 10 each)

**C1.** Rubric — all six headings present = 5 pts; each *defensible*
entry = 1 pt each for first-five-commands and safe-first-action
quality. Expected shape:

```
# Runbook: dataset ingest pipeline dies overnight
## Symptom (what page looks like)
  - "pipeline" unit failed / no new files in /srv/processed since T
## First evidence (in order, read-only)
  1. systemctl status <unit>        2. journalctl -u <unit> --since -2h
  3. df -h /srv                     4. free -h
  5. ls -lt /srv/inbox | head       (read-only, cheap, local → outward)
## Safe first action
  - restart the unit ONCE (systemctl restart) only after journal
    read; never while a related job is mid-write
## Escalation boundary
  - journal shows data corruption / disk >90% / repeated crash-loop
    → stop, page owner, attach evidence bundle
## Post-incident note (append-only)
  - what failed, decisive evidence line, the change made, how to
    detect it earlier next time
```

Full credit requires the *order* rationale (local & read-only
first) to be stated anywhere.

**C2.** Reference rewrite with per-change justification:

```
# test-first week: run in a sandbox dir with intentionally
# doomed content before pointing at /srv/inbox
0 3 * * * /usr/local/bin/clean-inbox >> /var/log/cleanup.log 2>&1
```

- [glob-guard]: move the `rm -rf` into a script that checks the
  target is non-empty, matches an exact path list, and refuses when
  `$1` is missing (`set -u` + `: "${INBOX:?}"` + `rm -rf -- "$INBOX"/*`
  with nullglob/`find -maxdepth 1 -delete`). Bare `rm -rf /srv/inbox/*`
  + empty glob = `rm -rf /srv/inbox/*` with literal `*` at best,
  disaster with a reset `PATH`/alias at worst.
- [log target]: cron's cwd/env minimal — absolute script path and
  absolute log path; or rely on cron's own mail instead of a log
  that grows unchecked.
- [exit status]: script must `exit` non-zero on partial failure and
  the log line must end with the status — "it ran" is not "it
  worked".
- [test-first]: schedule `*/10 * * * *` against a *copy* of the
  inbox for a week; inspect the log, then promote to `0 3 * * *`.

## Section D (20 pts) — staged-VM reference solution

**D1.**
```console
$ systemctl --user status ds-agent          # find the unit (user scope)
$ journalctl --user -u ds-agent -n 20       # journal shows the bad venv path
$ edit ~/.config/systemd/user/ds-agent.service  # ExecStart -> ~/venvs/agent
$ systemctl --user daemon-reload
$ systemctl --user restart ds-agent
$ systemctl --user status ds-agent          # Active: running
```
One-line documentation per step is the transcript requirement
(6/10 cap without it). Partial credit: journal-read (2), correct
line edited (3), reload+restart+proof (5 — but only with the
`--user` scope shown; system-scope edits score 0 here).

**D2.**
```console
$ du -h --max-depth=1 fatdir | sort -rh | head -3
```
Margin must be stated (e.g. "subdir X is 180 MiB of 200 MiB — 90%").

**D3.**
```console
$ git status --short
$ git add run.py requirements.txt        # explicit adds only
$ git status --short                     # secret file still untracked
$ echo "secrets.env" >> .gitignore && git add .gitignore
```
Cap at 3/5 if `git add -A` or `git add .` was used even once.

## Common failure patterns to watch

- A9 answered as "CPU is overloaded" — mechanism error, cap 1.
- B4 answered with client-side fixes (`ssh-keygen` again) — missed
  the decisive server-side line, cap 3.
- C2 "rewrites" that keep the bare glob without a guard — 0 for the
  glob-guard point.
- D1 performed with `sudo systemctl` at system scope — scope error,
  0 for D1 (the staged unit is a user unit; that's the test).
