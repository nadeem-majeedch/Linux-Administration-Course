# Lesson 6 — Monitoring Layers: auditd, MAC Frameworks, fail2ban and Recovery

> Module 25 · Unit 6 · Difficulty: Advanced
> Reading time: ~25 min
> Up next: [Lab 1 — the hardening lab](../labs/lab-01-hardening.md)

---

## 1. The layers that watch and the layers that recover

Lessons 2–5 *reduced* the attack surface. This lesson covers the two
remaining defense-in-depth layers from
[Lesson 1 §5](01-principles.md): **monitoring** (knowing what
happened) and **recovery** (surviving what happened anyway). Four
tools are introduced at the conceptual level the course promises —
auditd, AppArmor/SELinux, fail2ban — plus malware and backups
framed honestly. None requires deep hands-on mastery here; each is
*recognized* fluently, because every real job will name them.

## 2. auditd — the system-call-level recorder

[M24](../../../M24-logs-journald-monitoring/content/README.md)'s logs
record what *programs say*. **auditd** records what *the kernel
sees* — syscalls: file opens, permission changes, executions,
logins — regardless of whether any program logs it. It's the
difference between a service's own diary and a CCTV system covering
the whole building.

The mental model: **rules** name what to watch; the audit log
captures matching events; `ausearch`/`aureport` query them.

```console
$ sudo auditctl -w /etc/passwd -p wa -k identity-changes
#         watch file    write+attr   tag for searching
$ sudo ausearch -k identity-changes -i | tail    # -i = interpret, human-readable
$ sudo aureport --auth                            # login report
```

Conceptual fluency checklist: auditd is *rules-based*, *kernel-level*,
*tagged* for search, and **always-on by design** (unlike ad-hoc
`inotify` watching) — that's why compliance regimes love it and why
it costs disk and attention. Reading level for this course: *explain
the model, recognize a rule, run a search someone else's runbook
specifies*. Deep rule-writing is its own discipline; the DS-relevant
part is knowing that "who changed that file" has a tool beyond
file timestamps.

## 3. Mandatory Access Control — AppArmor vs SELinux

Everything since M12 has been **DAC** — Discretionary Access
Control: file *owners* decide permissions, and root overrides
everything. **MAC** (Mandatory Access Control) adds a second,
policy-driven gate the owner *cannot* waive: each program gets a
profile declaring exactly which files/capabilities it may touch;
violations are denied and logged — even for root-owned processes.

Why it matters: DAC is all-or-nothing per account — a compromised
web server process (running as `www-data`) can touch everything
`www-data` can. MAC confines the *program*: the compromised process
can touch what the *policy* allows — typically far less. It's
least-privilege for software, the natural endpoint of
[Lesson 1's](01-principles.md) master principle.

| | **AppArmor** (Ubuntu/Debian default) | **SELinux** (RHEL/Fedora default) |
|---|---|---|
| Policy shape | per-program **path-based** profiles | system-wide **label-based** (every file/process labeled) |
| Enforcement modes | enforce / complain (log-only) | enforcing / permissive |
| Simplicity | profiles readable as plain text; easy to write for your own app | powerful, fine-grained; steeper curve |
| Ubuntu presence | ships profiles for system services (`/etc/apparmor.d/`) | not installed |

```console
$ sudo aa-status | head -12          # which AppArmor profiles are loaded, enforcing?
$ cat /etc/apparmor.d/lsb_release    # a tiny profile: readable, path-based
$ getenforce                          # (RHEL machines) SELinux mode: Enforcing/Permissive
```

Conceptual fluency: explain DAC vs MAC in one sentence each;
recognize that Ubuntu = AppArmor by default and RHEL = SELinux by
default; know *complain/permissive* means "log violations, don't
block" (the debugging mode); know that "the app fails weirdly on
RHEL" is very often an SELinux denial you'll find via
`/var/log/audit/audit.log` — the auditd connection, completing the
circle.

## 4. fail2ban — the log-reading firewall

[M22](../../../M22-ssh-remote-admin/content/README.md) named it; here's
the model. **fail2ban** watches logs (auth.log, journald) for
failure patterns, and on enough hits from one source, tells the
firewall to block that source for a time. Log monitoring
([M24](../../../M24-logs-journald-monitoring/content/README.md)) wired
to enforcement (this module's Lesson 2) — automation of a rule a
human could apply, at machine speed.

```console
$ sudo apt install fail2ban                     # Ubuntu package exists; jail.local to configure
$ sudo systemctl status fail2ban                # (labs: install in your VM only if curious)
$ sudo fail2ban-client status sshd              # banned IPs, failure counts
```

Concepts to hold: **jail** = a log pattern + threshold + ban action;
**ban time / find time** shape the window; the default sshd jail is
the 90% use case. Relationship to `ufw limit` (Lesson 2): ufw's
limit is *connection-rate* throttling at the kernel, fail2ban is
*failure-pattern* banning from logs — overlapping but distinct
layers; real servers often run both. Note the Ubuntu config
etiquette: never edit `jail.conf`; write `jail.local` (the drop-in
pattern from sudoers and sshd, third appearance).

## 5. Malware — concepts and honest defenses

A conceptual map, deliberately without implementation detail:
malware on Linux servers is *rare relative to desktops*, and what
exists arrives overwhelmingly through **the channels you control**:

- **Supply chain** — the typosquat/trojan-package path
  ([Lesson 4](04-services-updates-packages.md)); the defense is
  source discipline.
- **Compromised credentials** — an SSH key or token stolen, then
  used to run things *as you*; defense is
  [Lesson 5](05-secrets-credentials.md) hygiene.
- **Unpatched services** — the classic; defense is Lesson 4's
  patching.

The detection story is everything this course already taught:
*unexpected listeners* (`ss -tulpn` — Lesson 4's audit), *unexpected
processes* (M18's `ps`/`top` fluency), *unexpected log lines* (M24),
*unexpected cron entries* (`crontab -l`, `ls /etc/cron*` — M19's
territory), unexpected *persistence attempts* (new units, new
`authorized_keys` lines — `journalctl -g authorized_keys` is a real
check). Linux malware that "phones home" or persists does it
through exactly these doors — your monitoring is the detection.
Course boundary: we detect and prevent; we do not build. Anything
beyond "report findings to the admin/IT" is IT-security territory,
and *should* be.

## 6. Backups — the control that survives everything

Every layer above can fail. **Backups are the control that turns
total compromise into an inconvenience** — and the course has
already done the hard parts:

- **3-2-1 with tested restores** —
  [M17](../../../M17-storage-and-filesystems/content/README.md)/[M24](../../../M24-logs-journald-monitoring/content/README.md):
  the backup lab *graded the restore*, because untested backups are
  hopes.
- **Offline/immutable copies** — the ransomware-era nuance: a
  backup reachable by the same compromised credentials gets
  encrypted too. One copy must be *offline* (disconnected disk) or
  *immutable* (object-lock on cloud storage). This is why 3-2-1's
  "one offsite, different medium" is security, not just disaster
  planning.
- **Restore speed as a metric** — the M24 lab's timing question
  was a security metric in disguise: recovery time *is* the outage.

The capstone thread: your DS project's backup plan (datasets,
environments, credentials *vaults* — not the secrets themselves)
will be graded as part of its security posture.

## 7. Try it now (10 minutes, read-only)

1. `sudo aa-status | head -12` — which AppArmor profiles enforce on
   your Ubuntu VM right now? (You've been running under MAC all
   course.)
2. `getenforce 2>/dev/null || echo "SELinux not present"` — the
   dialect check, witnessed.
3. `sudo auditctl -l 2>/dev/null` — probably empty: nothing watched
   yet. State in one sentence what a `-w /etc/passwd -p wa` rule
   *would* give you that dpkg.log doesn't.
4. Persistence inventory (detection rehearsal): `crontab -l;
   ls /etc/cron*; systemctl --user list-unit-files --state=enabled |
   head` — everything that *auto-runs* on your machine. On a
   compromised box, this list is where you'd look first.

## 8. Common mistakes

- Treating AppArmor/SELinux as "the thing to disable when apps
  break" — the *right* move is reading the denial and fixing the
  policy (or fixing the app's assumption); disabling MAC removes a
  layer because one layer chafed.
- Installing fail2ban without first having keys-only SSH — banning
  brute-force IPs while leaving passwords enabled is bailing, not
  plugging.
- Audit rules without tags (`-k`) — unsearchable logs are storage,
  not evidence.
- Backups reachable by the same credentials as production — the
  3-2-1 nuance most often skipped; name your offline copy.
- Confusing *monitoring* with *security* — monitoring without the
  earlier layers means you get excellent logs of the compromise.

> **Next:** [Lab 1 — the hardening lab](../labs/lab-01-hardening.md):
> lessons 1–6 applied to your VM in one documented, reversible pass.
