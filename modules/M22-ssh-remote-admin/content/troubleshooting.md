# Module 22 Troubleshooting — SSH Symptoms → Causes → Fixes

> Ten patterns, ordered by frequency in real life. Each: **symptom →
> cause → diagnosis → fix → prevention**. The evidence quartet opens
> every case: `ssh -v`, `ls -l ~/.ssh` (both machines), `ssh-add -l`,
> `ssh -G alias` — server's `auth.log` when the client side is clean.

## 1. "Password prompt where keys used to work"

**Cause (in frequency order):** private-key permissions loosened;
wrong/offered key (config or agent); `authorized_keys` modes or
ownership broken server-side; agent lost the key.
**Diagnosis:** `ssh -v user@host 2>&1 | grep -iE 'identity|offering|denied|permission'`
+ `ls -l ~/.ssh` on *both* ends + `ssh-add -l`.
**Fix:** whichever the evidence names (chmod 600; fix the config
line; server-side `chmod 700 ~/.ssh; chmod 600 authorized_keys;
chown`).
**Prevention:** Lab 1's two checks are the reflex — permissions
locally, `authorized_keys` modes remotely.

## 2. "Connection refused"

**Cause:** nothing listening — sshd not running/installed, or a
wrong port. *Refused = the machine answered.* (M21's distinction.)
**Diagnosis:** `ssh -vvv ... 2>&1 | grep -i connect`; on the server:
`systemctl status ssh; ss -tlnp | grep :22`.
**Fix:** install/start sshd (`sudo apt install openssh-server`);
correct the port (and `ssh -G` it).
**Prevention:** after any VM rebuild, `systemctl status ssh` is
check #1.

## 3. "Connection timed out"

**Cause:** packets not arriving — wrong address (NAT guest without
port forwarding), firewall drop, or the VPN/portal half-broken state
(M21 pattern #7).
**Diagnosis:** `ip route get <target>` (M21's rung 3); `nc -zv <host>
22`; on a VM: is this the *forwarded* port or the guest IP?
**Fix:** addressing/port-forwarding, not SSH — sshd is innocent.
**Prevention:** `ssh -G alias | grep hostname` — aliases that
silently point at stale IPs are the classic timeout generator.

## 4. "REMOTE HOST IDENTIFICATION HAS CHANGED!"

**Cause:** the server's host key differs from `known_hosts` —
rebuild/reinstall (benign, common), new machine behind a reused
name/IP, or interception (rare, serious).
**Diagnosis:** *out-of-band verification first* — VM console, admin,
change ticket. Did *you* rebuild it? Then it's benign by
construction.
**Fix (only after verification):** `ssh-keygen -R <host>` (or the
line-number edit the warning suggests), reconnect, accept, record
the new fingerprint.
**Prevention:** never disable host-key checking; treat the warning
as a process, not a nuisance.

## 5. "Permission denied (publickey)" — the server's view

**Cause:** the server saw no acceptable key: public key absent from
`authorized_keys`, wrong `authorized_keys` modes/ownership, or
selinux/apparmor edge (rare on Ubuntu labs).
**Diagnosis:** server-side, verbatim: `sudo tail -5
/var/log/auth.log` — the log names the *reason* (bad ownership,
no key matched). Compare the offered key's fingerprint (`ssh -v`)
against `authorized_keys` contents.
**Fix:** deploy the right `.pub` (ssh-copy-id), fix modes.
**Prevention:** ssh-copy-id over hand-rolled pipes — it exists
because of this entry.

## 6. "The agent has no identities" (mid-session surprise)

**Cause:** new shell session — agents don't survive reboots, and
`eval "$(ssh-agent)"` was never re-run; or the key was never
`ssh-add`ed.
**Diagnosis:** `ssh-add -l` (empty vs error distinguishes "no
identities" from "no agent").
**Fix:** `eval "$(ssh-agent)" && ssh-add ~/.ssh/lab_vm` — or rely on
`AddKeysToAgent yes` (Lesson 2's default block) so first use loads
it.
**Prevention:** the §2 `Host *` block; one `ssh-add` per session
becomes automatic.

## 7. "Too many authentication failures"

**Cause:** the client offered every agent-loaded key before yours —
servers count offers and slam the door at `MaxAuthTries`.
**Diagnosis:** `ssh -v ... | grep -c offering`.
**Fix:** `IdentitiesOnly yes` + explicit `IdentityFile` in the Host
block; or prune the agent (`ssh-add -d`).
**Prevention:** per-host `IdentityFile` + `IdentitiesOnly` — the
config discipline of Lesson 2 §2.

## 8. "scp worked; rsync says 'rsync: connection unexpectedly closed'"

**Cause:** rsync missing on the *remote* side (it must exist at both
ends), or a remote-shell/rc quirk emitting output before the rsync
protocol.
**Diagnosis:** `ssh vm 'rsync --version'` — absent = diagnosis; if
present, `ssh vm 'echo login-ok'` and look for shell rc noise.
**Fix:** install rsync remotely (M16's workflow); silence rc output
for non-interactive shells.
**Prevention:** the tool-exists-remotely check is part of any
rsync-based workflow's setup.

## 9. "Tunnel starts; the service is unreachable through it"

**Cause:** the *service behind* the tunnel died, isn't loopback-
bound on the remote, or a port collision on the local end.
**Diagnosis:** the M21 ladder at both ends: `ss -tlnp | grep <port>`
on the *remote* (is the service up? bound to what?) and on the
*local* (does ssh hold the forward?); `curl -v` for refused-vs-
timeout.
**Fix:** restart/rebind the service; free the local port; check the
`-L` argument order (local:remote-host:remote-port).
**Prevention:** "service up" is verified at the service, not the
tunnel — the clinic's patient #5.

## 10. "My session died and took the training with it"

**Cause:** work started in a bare SSH shell — HUP on disconnect
(M18) did the rest. The failure is upstream of SSH: session
management.
**Diagnosis:** retrospective — `journalctl --user -u <unit>` or the
absence of any tmux session (`tmux ls`).
**Fix (now):** nothing to fix; restart *in* tmux, re-run (M11
idempotency pays off here).
**Prevention:** the Lesson 4 reflex — no long remote work outside
tmux; `tmux new -s <project>` *before* the command, every time.

## When to escalate

| Evidence | Escalate to |
|---|---|
| Key rejected server-side with clean local state | Admin, with `ssh -v` tail + your key fingerprint |
| Repeated host-key changes on one host | Admin/security — immediately, this is theirs |
| Cluster timeout to jump host | Network/VPN owner — with `ip route get` + `nc -zv` outputs |
| Service down behind your tunnel | Service owner — with the remote `ss -tlnp` line |

> Every escalation carries the verbatim evidence — the M24 habit,
> applied at the network's edge.
