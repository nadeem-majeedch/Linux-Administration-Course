# Assignment 5 Key — The Network Doctor

> **INSTRUCTOR ONLY.** Student paper: [assignment-5-network-and-services.md](assignment-5-network-and-services.md).
> Contains the incident answers and the staging design. Do not distribute.

## Staging design (`stage-incidents.sh` essentials)

The pack script (shipped with the assignment) creates five states on
the *student's own VM*:

| Incident | Planted fault | Reversibility |
|---|---|---|
| 1 | user unit `health.service` with `ExecStart` pointing to a script that exits 1 (bad interpreter path), `Restart=on-failure` → crash-loop | delete unit + `daemon-reload` |
| 2 | a tiny python http.server *running* but bound to `127.0.0.2:8080` while the "dashboard" claims 8080 on localhost — or a systemd unit started with the wrong `--port` flag | kill + relaunch with right port |
| 3 | sandbox `sshd_config` copy with `PubkeyAuthentication no` + a second sshd on port 2222 using that config — the *real* sshd untouched | stop sandbox sshd, delete copy |
| 4 | rsync target directory's files replaced by *newer-stamped but stale-content* copies after the last sync; the sync script lacks `-c`/manifest check | re-run correct sync; content restored from `incoming/` copy |
| 5 | the API service listening on `127.0.0.1:5000` only (bind address), tested with `curl http://<vm-ip>:5000` from another terminal/host-only network | change bind to `0.0.0.0` or the VM IP, restart |

All faults are student-VM-local; no system sshd is modified; teardown
script reverses everything.

## Expected evidence chains (grade the *chain*, not just the verdict)

**Incident 1 — crash-looping unit**
1. `systemctl --user status health` → `activating (auto-restart)`
2. `journalctl --user -u health -n 20` → exec/format error quoted
3. Fix: correct the ExecStart path/interpreter → `daemon-reload` → start
4. Verify: `is-active` = active; ticks in the journal
*Common wrong path:* reinstalling the service; rebooting (zero for the incident).

**Incident 2 — running but unreachable**
1. `ps aux | grep <proc>` → it runs (so not a crash)
2. `ss -tlnp | grep 8080` → listener exists but on the wrong address/port
3. Fix: relaunch bound to the intended port/address
4. Verify: `curl` the dashboard URL, content served
*Discriminator:* students who first check DNS/firewall violated rung order — cap at half marks for the incident.

**Incident 3 — password prompt instead of key**
1. `ssh -v localhost` → `Offering public key` absent or refused
2. Sandbox config shows `PubkeyAuthentication no` (or wrong authorized_keys modes in the sandbox home)
3. Fix: sandbox config corrected, sandbox sshd restarted
4. Verify: `ssh -i key -p 2222` authenticates without password
*Discriminator:* touching the real `sshd_config` = zero; the sandbox is the assignment's safety architecture.

**Incident 4 — "up to date" but stale**
1. `rsync -avhn` shows nothing to do (size+mtime agree)
2. sha256 manifest diff shows content mismatch (the student must
   *choose* a stronger comparison — this is the lesson)
3. Fix: re-sync (optionally `--checksum`), restore correct content
4. Verify: manifest diff clean, "VERIFIED IDENTICAL"
*Discriminator:* accepting rsync's word without the manifest = half marks.

**Incident 5 — local answers, remote doesn't**
1. Works on `curl localhost:5000`; fails from `<vm-ip>:5000`
2. `ss -tlnp` → bound to `127.0.0.1:5000` only
3. Fix: bind `0.0.0.0` (or VM IP), restart; firewall already allows (or
   `ufw allow` justified — note which)
4. Verify: curl from the second terminal/edge succeeds
*Discriminator:* firewall-first debugging without `ss` = rung-order violation.

## Marking map (20 pts total, per the rubric)

- **Ladder discipline (5):** deduct per out-of-order diagnosis (−1
  each, floor 1). Evidence must be *quoted* in notes.
- **Root-cause accuracy (5):** 1/incident.
- **Fix minimality (4):** rebuild-instead-of-repair or reboot = 0 for
  that incident's fix share.
- **Verification (3):** each incident's original symptom re-tested;
  missing verification = −1 per incident.
- **Notes (3):** four elements present; prevention lines that a
  teammate could act on.

## Quick-triage of transcripts

- Five labeled sections present? (organization mark)
- First command of incident 1 is `status`/journal, not `restart`?
  (read-only discipline)
- Any `kill -9` as first reflex? (⚠ mark; discuss in feedback)
- Sandbox respected in incident 3? (hard gate)

## Viva probes

- "Incident 2: why was 'the process is running' insufficient evidence?"
- "Incident 4: name the two comparison levels and when each is the
  right claim."
- "Incident 5: what would have made the bind-address fault *invisible*
  on a single-user laptop?" (loopback-only use — real servers expose it)
