# Module 25 Quiz — Answer Key

> Reasoning graded; rules/commands on "would it work if typed".

## Section A — principles

**A1.** Every account/process/service holds the minimum authority
needed, only while needed. Instances: M14 (sudo per-command
privilege), M20 (user services, not root), M22 (`AllowGroups`
network allowlist), M12/M13 (file permissions/ACLs — least
privilege on data).

**A2.** AuthN = proving *who you are*; authZ = deciding *what you
may do*. authZ: `setfacl`, `AllowGroups`, `chmod 640`. authN:
`ssh-copy-id` (installs an identity credential), `passwd` (changes
an authN secret).

**A3.** Exposure went from *this machine only* (loopback) to *every
network the host touches* (all interfaces). Same service, same
port — the reachable set multiplied; the surface is bound-scope,
not the program.

**A4.** Network (ufw/bind scope) → service (sshd directives,
service audit) → identity (keys/sudo) → files (permissions/ACLs) →
monitoring (logs/auditd/fail2ban) → recovery (backups). Each
catches the failure of the layer(s) inside it: e.g. monitoring
catches a misconfigured firewall; recovery catches everything.

**A5.** Because every preventive layer can fail, and backups are
the control that converts total compromise into data restoration
(downtime, not loss). Nuance: a backup reachable by the same
compromised credentials gets encrypted too — one copy must be
offline or immutable.

## Section B — firewall

**B6.** Default-allow fails *open* (forgotten threats are open);
default-deny fails *closed* (forgotten services are unreachable).
The course mandates default-deny: the rule list becomes a positive
inventory and mistakes fail safe.

**B7.** Correct order: `default deny incoming` → `allow OpenSSH` →
`enable`. The order is load-bearing because `enable` activates the
policy *immediately* — default-deny without the SSH allow first
locks out your own session at the moment of enabling.

**B8.** `limit` = kernel-level connection-rate throttle (~6
connections/30s per source) — prevents floods mechanically.
fail2ban = log-pattern detection → temporary firewall ban — reacts
to *failed authentication*, not connection rate. Different layers
(kernel throttle vs log-driven enforcement).

**B9.** `sudo ufw allow from 10.0.2.0/24 to any port 22 proto tcp`

**B10.** ufw filters packets *crossing network interfaces*;
loopback traffic never does — a `127.0.0.1`-bound service is
unreachable from outside by construction. Implication: bind scope
is itself a network control (often the strongest one) — "don't
expose" beats "expose then filter".

## Section C — SSH & services

**C11.** Before applying sshd (or any access-critical) changes:
keep the *current* session open as the working/escape terminal, and
perform the change plus verification from a *second*, fresh
session. Never close the first until the second has authenticated
under the new config. (Plus the VM console as final backstop.)

**C12.** Backup → write (drop-in) → test (`sshd -t`) → reload →
verify (from the second terminal).

**C13.** `sshd -t`: parse/config-test only — nothing applied.
`reload`: re-read config; existing sessions *survive*. `restart`:
stop+start — kills current sessions. `reload` is right because the
change must apply without severing the session you're working
through.

**C14.** `50-cloud-init.conf` wins — sshd_config directive
resolution takes the *last-obtained* value across drop-ins in
lexicographic order (opposite of client-config first-match).
Fix: rename yours to `99-hardening.conf` (or remove/shadow the
cloud-init line), `sshd -t`, reload, re-verify.

**C15.** Per line: (1) what is it? (2) bound where — loopback or
network-facing? (3) needed? Escalation to close: `disable --now`
(stop + boot) → `purge` (remove) → `mask` (refuse even on request)
— each recorded with its reasoning.

## Section D — secrets & monitoring

**D16.** Best: `os.environ` injection (no secret at rest in the
repo at all). Then: ignored `600 .env` (on-disk secret, protected
and invisible to git). Then: tracked `.env` (git-bound leak).
Worst: hardcoded in a notebook (leaks into git *and* cached cell
outputs). Justification tracks exposure-at-rest and copy-count.

**D17.** Because git history retains every prior commit — the
`.env` is still retrievable at old hashes; ignore affects only
future tracking. Steps: (1) revoke/rotate the credential at the
provider, (2) purge current state (rm from tracking, env pattern),
(3) history rewrite (filter-repo/BFG) as a coordinated, non-urgent
event once revocation has contained the risk.

**D18.** Because the leaked value is *usable until rotated*
regardless of git state — scanners don't need your repo clean,
they need the token live. Revocation converts a live leak into
dead data; every later step becomes calm cleanup.

**D19.** Syscall events — file opens/writes, permission changes,
executions — regardless of whether any program chose to log them.
`-k` tags label rule hits so `ausearch -k <tag>` can find them —
untagged audit logs are storage, not evidence.

**D20.** Ubuntu: AppArmor; RHEL: SELinux. Policy shape:
path-based per-program profiles (AppArmor) vs system-wide labels
on every object (SELinux). Complain/permissive = *log* violations
without blocking — the debugging mode.

**D21.** ufw `limit` — prevent (kernel rate throttle). fail2ban —
prevent (log-driven, automated firewall ban; sits between
detect and prevent). auditd — detect (kernel-level recording).
(If scored strictly: limit=prevent, fail2ban=prevent-via-detect,
auditd=detect.)

**D22.** Any four: unexpected listeners (`ss -tulpn`), unexpected
processes (M18 tools), unexpected log lines (M24), cron/crontab
entries, new systemd units, new `authorized_keys` lines
(`journalctl -g authorized_keys`), new user accounts
(`/etc/passwd` diff).

## Bonus (Q23) — model answer

The gap is **Recovery**: the backup shares fate with the machine —
same host, same credentials — so a compromise (or rm, or ransomware)
takes original *and* copy. The control: 3-2-1 with one copy
**offline or immutable** and on different credentials — then the
checklist's "restore tested" line makes it real. (Lesson 6 §6's
nuance, word for word.)

## Score guide

| Score | Meaning |
|---|---|
| 20–23 | Hardening habits installed — run the checklist on your real machine |
| 15–19 | Re-read flagged lessons; redo the matching lab phase |
| < 15 | Repeat lessons 1–3 — the principles carry everything else |
