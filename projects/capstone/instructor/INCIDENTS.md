# Capstone Incident Bank — Injected Incidents for Phase 3

> The instructor stages ONE incident per student (unannounced, from a
> different category than the student's own drill-card practice if known).
> The student receives the **symptom only**; grading follows the eight-step
> method (M23-clinic): evidence-first, hypotheses, safe tests, verify the
> *original symptom*, document.
>
> All incidents are staged on the student's own VM, touch only lab-created
> or student-owned state, and are fully revertible. Setup commands assume
> you know the student's paths from their proposal; the placeholders are
> marked.

## Incident selection matrix

| # | Incident | Class | Difficulty | Classic student failure |
|---|----------|-------|------------|------------------------|
| I1 | The disappearing dependency | Python env | ●●○ | reinstall blindly instead of reading `sys.executable` |
| I2 | The full disk that isn't | Storage | ●●○ | `du` vs `df` confusion; deleting the open file's name |
| I3 | The poisoned name | DNS/hosts | ●●○ | blaming the network; missing `getent` vs `dig` |
| I4 | The wedged service | Services | ●●● | restart-first (destroys evidence); reading no journal |
| I5 | The silent port | Networking | ●●○ | firewalling reflex; never checking bind scope |
| I6 | The drifting permissions | Identity | ●●○ | `chmod 777` instead of `namei -l` + minimal bit |
| I7 | The memory leech | Resources | ●●● | killing the top process before identifying *whose* it is |

---

## I1 — The disappearing dependency

**Staging (as root or the student's sudo):**

```bash
# Break the venv the API runs from (find it from their unit file: ExecStart)
VENV=/home/<student>/capstone/service/.venv
rm -f "$VENV"/lib/python3*/site-packages/pandas/core/frame.py   # subtle: package present, module broken
# If their unit has Restart=on-failure, the API crash-loops; if not, it dies once.
```

**Symptom the student receives:** "Your API returns 502 through nginx since
~10 minutes ago. It worked an hour ago. Nobody changed anything."

**Answer key (expected evidence chain):**

1. *Define:* API 502 via nginx, started ~10 min ago, no known change.
2. *Evidence:* `systemctl --user status app` → **exit 1** (or crash-loop
   `start-limit`); `journalctl --user -u app -n 30` →
   `ModuleNotFoundError`/`AttributeError` naming pandas;
   `nginx error.log` shows upstream connect failures (secondary evidence —
   the 502 is nginx *describing* the dead upstream).
3. *Component:* the app service, not nginx (the proxy is the messenger).
4. *Hypotheses:* H1 broken venv content (module present, file corrupted);
   H2 wrong interpreter (ExecStart repointed); H3 pip removal.
   Ranked by test cost: read the unit (`cat`), run the venv python's import
   by hand, `pip list` in the venv.
5. *Safe test:* `.venv/bin/python -c "import pandas"` — reproduces the exact
   traceback outside the service. No mutation yet.
6. *Fix:* recreate from pins — `pip install -r requirements.txt` into the
   venv (or full rebuild). **Full credit requires citing the pin file as the
   repair source** — reinstalling "whatever pip finds" is half credit.
7. *Verify:* the ORIGINAL symptom — `curl` through nginx (not just the port)
   returns 200; `systemctl --user is-active` green.
8. *Document:* prevention = the pin file + a post-deploy import smoke test.

**Full-credit markers:** journal quoted with the traceback; *no* blind
`pip install pandas` into the wrong interpreter; nginx ruled out as a
*hypothesis* with evidence, not assumed.

---

## I2 — The full disk that isn't

**Staging:**

```bash
# Uses their capstone scratch/backups dir (from their proposal)
dd if=/dev/zero of=/home/<student>/capstone/backups/.staging.bin bs=1M count=200 status=none
tail -f /home/<student>/capstone/backups/.staging.bin > /dev/null 2>&1 &
echo $! > /root/.incident-i2.pid        # the holder
rm /home/<student>/capstone/backups/.staging.bin
# For a sharper version on a VM: stage on a small loopback volume they made (M17).
```

**Symptom:** "Your scheduled pipeline failed at the write step — 'No space
left on device'. But you swear the box has space; `df` for root says 40%."

**Answer key:**

1. `df -h` on the *affected filesystem* first — which mount is the pipeline
   writing to? (Students must read their own config; the incident may be on
   the volume, not `/`.)
2. `du` vs `df` mismatch → deleted-but-open (or inode exhaustion — the
   discriminator: `df -i`).
3. `lsof +L1 <dir>` (or `/proc/*/fd` hunt) → the holder PID and the deleted
   file name.
4. *Causality test:* reproduce the write failure, identify holder, then
   **stop the holder** (their own backup job's stale run — or, as staged, the
   `tail -f`) → space returns → write succeeds.
5. *Document:* root cause "writer holds unlinked inode"; prevention = log
   rotation (M24 lesson 2) / staging-file cleanup in `backup.sh`.

**Full-credit markers:** the deleted-open mechanism named; holder identified
by PID; *no* `rm` of the (already unlinked) name performed as a "fix"; the
policy-level prevention stated.

---

## I3 — The poisoned name

**Staging (needs the student's sudo; do it while they're out):**

```bash
sudo cp /etc/hosts /root/.hosts.bak
echo "127.0.0.1 <their-registry-host-or-pypi-mirror>" | sudo tee -a /etc/hosts
```

**Symptom:** "Your scheduled pipeline failed to fetch its data source this
morning — 'could not resolve/connect'. Other sites work. Your VM, your
problem."

**Answer key:**

1. The *selectivity* is the fingerprint: one name fails, everything else
   works → not connectivity (card 8's rungs pass), not the resolver broadly →
   the override layer.
2. `dig +short <name>` (resolver's answer) vs `getent hosts <name>` (what
   applications actually get) — they disagree → nsswitch hosts-first →
   `tail /etc/hosts`.
3. Safe test: `curl --resolve <name>:443:<real-ip>` works around the poison —
   proving only the name layer is broken.
4. Fix: remove the hosts line (with the backup/undo noted *before* editing).
5. Verify three layers (card 7): dig, getent, **the original pipeline
   command**.
6. Document: prevention = "selective failure with working IPs → check the
   hosts file first"; the *policy* question — who can edit /etc/hosts on this
   box, and is that logged?

---

## I4 — The wedged service

**Staging (subtle — the API *hangs*, it doesn't die):**

```bash
# In their API code, nothing. Instead: starve its dependency.
sudo systemctl stop postgresql     # Pattern 2 students: DB gone → app hangs on connect
# OR for Pattern 1: fill their API's socket backlog:
# (a loop of un-accepted connections to their API port — instructor-run)
```

**Symptom:** "The API is 'up' — `systemctl --user status` says active — but
every request hangs until timeout. curl to the port connects but never
answers."

**Answer key:**

1. The state mismatch is the lesson: *active ≠ serving* (M24's distinction;
   M31 card 12's composite).
2. Evidence: the app's own logs stop mid-request; DB-dependent request paths
   hang (`pg_isready` fails or the socket state shows the peer problem);
   `ss -tnp` shows connections ESTABLISHED-but-stalled.
3. Hypotheses: H1 dependency down (DB stopped); H2 app deadlock; H3 backlog
   exhaustion. Ranked: `pg_isready` costs nothing.
4. Safe test per hypothesis; the *dependency* is the root cause — the app
   merely confesses it.
5. Fix: start the dependency; **then the deeper fix**: the app needs connect
   timeouts + the runbook needs the dependency order — restart ordering and
   healthchecks (M28 §1 / M29) named as prevention.
6. Verify: original symptom gone *through the public path*.

**Full-credit markers:** "active but not serving" articulated; dependency
checked before the app is restarted; the *ordering* fix (healthchecks/`After=`
/ connect-timeout) named as prevention, not just "I started the DB."

---

## I5 — The silent port

**Staging:**

```bash
# Rebind their API to loopback only (edit their unit's app args or config),
# OR (iptables flavor) drop one port at the INPUT chain for their test range.
sudo ufw delete allow 8000/tcp        # quietly removes the allow rule they justified
```

**Symptom:** "Your teammate can't reach your API from their VM anymore —
connection refused/timeout. From *your* VM, `curl localhost:8000` is fine."

**Answer key:**

1. The local/remote split is the tell: works from loopback, fails from
   outside → the *edge* (ufw rule or bind scope), not the app.
2. Evidence: `ss -tlnp` (listener present — and on which address?),
   `sudo ufw status verbose` (the rule that vanished), the M21 six-rung
   ladder with the failure at the firewall rung.
3. Hypotheses: H1 ufw rule removed; H2 bind scope changed; H3 colleague's
   network. Ranked by test cost: local `ss` first, `ufw status` second,
   colleague's network last.
4. Fix: restore the justified rule (`ufw allow from … to any port 8000`) —
   with the *justification line* from their own docs, not a bare allow.
5. Verify from the *original client*, not localhost (card 12's lesson).
6. Document: prevention = the firewall config in version control + the
   convergence habit (M29-ext A lesson 2): hand-edits get re-absorbed, and
   the diff *is* the drift report.

---

## I6 — The drifting permissions

**Staging:**

```bash
# Their data directory: drop the group-execute bit on a parent (or chown a
# subdir to root via a "fix" their svc account can't traverse).
sudo chmod o-x,g-x /home/<student>/capstone/data/processed
sudo chown root:root /home/<student>/capstone/data/processed/2026-09-21 2>/dev/null
```

**Symptom:** "The pipeline can't write today's processed files — 'Permission
denied' — but it wrote there fine yesterday. You didn't change anything."

**Answer key:**

1. `namei -l <path>` — the card-9 centerpiece: find *which level* denies (it
   won't be the leaf).
2. The two mechanism families: a missing `x` on a parent directory vs an
   ownership change — the incident stages one; a complete answer *checks for
   both* and names which it found.
3. Fix: the minimal bit (`chmod g+x` on that directory) or `chown` back to
   the service identity — **never `chmod -R 777`** (the rubric's destructive-
   without-safeguards deduction applies).
4. Verify: the original write succeeds as the *original identity* (not sudo).
5. Document: prevention = the permission matrix in the repo + the convergence
   re-run that would have reported the drift; the audit question "who can
   chmod my tree?" answered honestly.

---

## I7 — The memory leech

**Staging:**

```bash
# A reniced, unowned-looking memory eater with a misleading name:
sudo -u nobody nice -n -5 bash -c 'trap "" TERM; a=(); while :; do a+=("$(head -c1M /dev/zero | base64)"); sleep 2; done' &
# (Adjust to your VM's RAM; keep ~30% headroom so the student can still work.)
```

**Symptom:** "The box is slow and you suspect someone's job. Your own
pipeline is due to run in 20 minutes and you're worried it'll OOM."

**Answer key:**

1. The four-instrument sweep first (M24-clinic): load vs cores, `free`
   available trend, `top` sorted by RSS, `vmstat si/so`.
2. The trap: the leech runs as `nobody` with **negative nice** — the student
   must notice (a) it's not theirs, (b) it outranks everything, (c) killing
   another user's process is an *escalation*, not a command.
3. The evidence pack: PID, owner, RSS trend, nice value, command line — the
   "admin handoff" (M31 lesson 2 §5 / challenge C6's format).
4. *The grading fork:* on their own VM they hold sudo — but the **correct
   action** is the evidence-first conversation: document, then act. Full
   credit: kill only after the note is written (or simulate the
   notification); killing first with no evidence pack = half credit; killing
   with the *wrong* process = fail.
5. Verify: `available` recovers, `si/so` quiets, the pipeline runs.
6. Document: prevention = resource limits/cgroups for long jobs (M28/M18),
   and the policy answer: on a real shared box, whose job is it to kill?

---

## Incident report grading (applies to all)

| Element | Points (of the area-9 slice) |
|---|---|
| Step-1 definition, written as a stranger could act on | 1 |
| Evidence: commands + outputs, time-ordered | 3 |
| ≥2 ranked, *testable* hypotheses | 2 |
| Safe test with blast-radius sentence; no evidence-destroying restarts | 2 |
| Fix = cause not symptom; undo noted | 2 |
| Verify = original symptom, through the original path | 2 |
| Documentation: root cause + concrete prevention | 2 |
| **Method bonus** | +1 (evidence collected *before* any mutation) |
