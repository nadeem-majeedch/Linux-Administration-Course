# Final Examination — Units 4–7 (M14–M31)

> **Format:** 3 hours · closed book · 100 points. Section D runs live
> on a staged VM snapshot (start `script final.log` first).
> **Coverage:** M14–M31 — sudo → systemd → storage → networking →
> logs/monitoring → scripting → SSH → security → cron/backup →
> web/DB → Python/Jupyter → Git → Docker → performance → DS server.
> Every scenario below was *simulated* in some module lab; none is a
> verbatim repeat. Key: [final-key.md](final-key.md).

## Section A — Reasoning (30 pts, 10 × 3)

**A1.** A service "works" via `systemctl start` but is gone after
reboot. Name the missing `systemctl` verb and state precisely what
it changes on disk.

**A2.** `df` says a filesystem is 100% full; `du -sh /` totals far
less. Give the two classic causes and the command that separates
them.

**A3.** Why does `journalctl -u myapp` show nothing even though the
service is logging — and what flag pair do you reach for when a
user-level unit is the subject?

**A4.** `ss -tlnp` shows your app on `127.0.0.1:8000`; a colleague
on another machine cannot connect even after `ufw allow 8000`. State
the *actual* fix and the bind-address rule behind it.

**A5.** A cron job "works when I run it, fails from cron". Give the
three most likely environment differences, in diagnosis order.

**A6.** Why is `crontab -r` a trap, and what habit (one flag, one
backup pattern) neutralizes it?

**A7.** An rsync backup completes in seconds on the second run.
Explain the mechanism, and state what this same mechanism makes
rsync a *poor* choice for.

**A8.** You must give a partner container read access to a dataset
on the host. Compare a bind mount and a named volume for this case:
one reason each, then your pick for *read-only* sharing.

**A9.** Load average is 8.0 on a 4-core VM but CPU `%idle` is 90%.
What is the load actually counting, and which column of which tool
confirms it in one look?

**A10.** `ssh server` prompts for a password despite your key being
in `authorized_keys`. List the three most common causes in the order
you check them with `ssh -v`.

## Section B — Diagnosis from evidence (30 pts, 6 × 5)

Each item gives terminal evidence only. Name the failing component,
the decisive line, and the fix class. No command lists required.

**B1.**
```console
$ systemctl status model-api
   Loaded: loaded (/etc/systemd/system/model-api.service; disabled)
   Active: failed (Result: exit-code)
$ journalctl -u model-api -n 5
ModuleNotFoundError: No module named 'pandas'
```

**B2.**
```console
$ free -h
       total  used  free  buff/cache  available
Mem:    3.8G  3.7G   60M        80M       55M
Swap:   2.0G  2.0G   0B
$ journalctl -k -g oom | tail -2
Out of memory: Killed process 2417 (python3)
```

**B3.**
```console
$ ping -c1 data.uni.edu
ping: data.uni.edu: Temporary failure in name resolution
$ resolvectl status | grep -A2 'DNS Server'
   no servers configured
```

**B4.**
```console
$ ssh -v gpu01 2>&1 | tail -4
debug1: Offering public key: /home/u/.ssh/id_ed25519
debug1: Authentications that can continue: publickey,password
debug1: No more authentication methods to try.
Permission denied (publickey,password)
```

**B5.**
```console
$ iostat -x 1 2 | tail -4
Device  r/s  w/s  await  aqu-sz  %util
vda     2.0  450  180.3   82.1   99.5
avg-sz: 4.00 KB
```

**B6.**
```console
$ curl -m 3 http://localhost:8888/api
curl: (7) Failed to connect: Connection refused
$ ss -tlnp | grep 8888
(no output)
$ systemctl --user status jupyter
Active: activating (auto-restart) (Result: exit-code)
```

## Section C — Design (20 pts, 2 × 10)

**C1.** Write a **runbook skeleton** (headings + one sentence each)
for "dataset ingest pipeline dies overnight" that an on-call
classmate could follow with zero context. It must include: symptom
definition, first five evidence commands (names only), safe
first-action, escalation boundary, and the post-incident note that
protects the next person.

**C2.** A teammate proposes this `crontab` line:
```
0 3 * * * rm -rf /srv/inbox/* >> /var/log/cleanup.log 2>&1
```
Rewrite it defensively and justify every change: the glob-guard, the
log target, the exit-status question, and the test-first schedule
you'd use for a week before trusting it.

## Section D — Live terminal (20 pts)

Staged VM: a user unit `~/config/systemd/user/ds-agent.service` that
references a broken venv path, a 200 MiB `fatdir/` of rotating logs,
and a git repo with one uncommitted secret-looking file.

**D1 (10).** Repair `ds-agent` end-to-end: find the unit, read its
error from the journal, fix the path (the correct venv exists at
`~/venvs/agent`), reload, restart, and show the running proof.
Document each step in one line of your transcript.

**D2 (5).** Without deleting anything, prove which subdirectory of
`fatdir/` dominates and by what margin (du with sort and head).

**D3 (5).** In the repo: stage *only* the safe files, show a status
proving the secret file is excluded (not via `git add -A`), and add
the `.gitignore` line that makes the exclusion durable.

---

## Grading notes (instructor)

- Section A: 1 pt mechanism, 1 pt consequence, 1 pt tool/flag named
  correctly. "Restart the server" earns zero everywhere.
- Section B: 5 pts = component (1) + decisive evidence line quoted
  (2) + fix class (2). Quoting the *wrong* line but right component
  caps at 3.
- Section C: rubric is structure presence (5) + defensibility of
  each choice (5). C2 must *remove* or guard the glob, not reformat
  it.
- Section D: end-state caps at 6/10 for D1; the journal-and-fix
  chain must be visible in the transcript.
