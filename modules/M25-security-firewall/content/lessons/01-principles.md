# Lesson 1 — Security Principles: The Ideas That Organize Everything

> Module 25 · Unit 6 · Difficulty: Advanced
> Reading time: ~25 min · Lab: [Lab 1 — the hardening lab](../labs/lab-01-hardening.md)
> Up next: [Lesson 2 — firewalls & ufw](02-firewall-ufw.md)

---

## 1. Security as engineering, not fear

Linux security is often taught as a bag of commands. It's better
taught as a small set of *principles* that explain the commands —
every tool in this module (ufw, sshd directives, auditd, fail2ban)
is one principle wearing a config file. This lesson names the
principles; the rest of the module applies them. A second framing
rule: this module teaches **defense only**. There is no attack
instruction here — not as squeamishness but as scope: the skills a
DS-person needs are hardening, auditing, and recovery, all of which
are legal to practice on your own VM and useful on day one of any
job.

## 2. Least privilege — the master principle

Every account, process, and service should hold the *minimum*
authority needed for its task — no more, and only for as long as
needed. You have met it four times already; this module is where the
course's instances reveal themselves as one idea:

| Instance | Where taught | Security form |
|---|---|---|
| `sudo` over root shells | [M14](../../../M14-sudo-root-principle/content/README.md) | privilege per-command, logged, expiring |
| User services (`systemctl --user`) | [M20](../../../M20-systemd-services/content/README.md) | services run as *you*, not root |
| `AllowGroups ssh-users` | [M22](../../../M22-ssh-remote-admin/content/README.md) | network access limited to those who need it |
| `600` on keys, setgid data dirs | [M12/M13](../../../M12-users-groups-permissions/README.md) | files readable only by the right identities |

The DS translation: your training job doesn't need root; your
notebook doesn't need your *whole* home directory; your teammate
doesn't need write access to raw data they only read. When something
"needs root to work", the M14 reflex applies — it's usually a
permissions smell, not a requirement.

## 3. Authentication vs authorization — who are you vs what may you do

Two words, deliberately separated:

- **Authentication (authN):** proving identity. SSH keys (M22),
  passwords, sudo credentials. *Are you who you claim?*
- **Authorization (authZ):** deciding what that identity may do.
  File permissions (M12/M13), sudoers rules (M14), firewall rules
  (this module), `AllowUsers`. *May you do this?*

The separation matters because each fails differently: authN fails
to *theft* (stolen key/password — hence passphrases, agents, key
hygiene), authZ fails to *over-grant* (777 files, world-listening
services — hence least privilege). Hardening checklists (including
this module's) walk through both halves in order: first "who can get
in", then "what can they touch".

**Users and groups** (M12) are the machinery both run on: groups
name *roles* (`ssh-users`, `ds-team`), not people — so authorization
is granted to a role and membership is the only thing that changes.

## 4. Attack surface — everything an attacker can touch

The **attack surface** is the sum of reachable entry points:
listening services, open ports, accounts that can log in, files that
parse untrusted input, packages with vulnerabilities. The governing
equation of hardening:

> **Risk ≈ surface × exposure × value — and you control the first two.**

Concretely, on a default Ubuntu VM:

```console
$ ss -tlnp
State  Local Address:Port   Process
LISTEN 127.0.0.1:631          cupsd      ← print service: loopback only
LISTEN 0.0.0.0:22             sshd       ← the one real door
```

Two doors, not fifty — Linux's out-of-the-box surface is modest.
Hardening (Lab 1) walks it downward: close doors you don't use
(uninstall/disable services), narrow the ones you keep (`AllowGroups`,
bind to loopback), filter the network around them (ufw, next
lesson). [M21's](../../../M21-networking-fundamentals/content/README.md)
bind-scope lesson is attack-surface management in miniature: a
Jupyter bound to `127.0.0.1` has a surface of *this machine*; bound
to `0.0.0.0`, a surface of *the network* — same program, ten-thousand-
fold difference in exposure.

## 5. Defense in depth — layers, because single controls fail

No single control survives contact with reality: keys can leak,
firewalls misconfigure, patches lag. **Defense in depth** stacks
independent layers so a failure in one doesn't become a breach:

```text
network (ufw, bind scope)
  → service (sshd key-only, AllowGroups)
    → identity (keys + passphrases + sudo)
      → files (permissions, ACLs)
        → monitoring (auth.log, auditd, fail2ban)
          → recovery (backups, 3-2-1)
```

Each layer appears in this module. The design habit: for every
control, ask *"and if that fails?"* — if the answer is "nothing
else notices", there's a missing layer (that's why backups are a
security topic, Lesson 6).

## 6. The course's security story, recapped as one arc

Nothing in this module is new in isolation — it is the *compilation*
of the course:

1. **M04/M01:** updates and official sources — patching is security.
2. **M08–M11:** log/text fluency — evidence before verdicts.
3. **M12/M13:** permissions, ownership, ACLs — authZ machinery.
4. **M14:** sudo, sudoers, the root principle — least privilege.
5. **M16:** apt trust, unattended-upgrades, PPA policy — supply
   chain.
6. **M17/M24:** backups with tested restores, logs as evidence.
7. **M21:** ports, sockets, bind scope — exposure mechanics.
8. **M22:** keys, agents, sshd reading — remote authN.

This module adds the network filter (ufw), *applies* the sshd
hardening M22 only read, and organizes everything into checklists
and audits. The lesson: security isn't a module you take — it's a
thread you've been weaving, now pulled tight.

## 7. Threats a DS person actually faces

Not movie-hackers — the mundane, high-frequency list:

- **Brute force against SSH** — bots sweep every public 22/TCP
  continuously; keys + `PasswordAuthentication no` + fail2ban (M22
  reading, applied here) close it.
- **Credential leakage through Git** — an API token committed to a
  notebook repo; scanners find it within minutes of pushing public.
  Lesson 5's whole subject.
- **Supply-chain slip** — `pip install reqests` (typo package) or a
  PPA nobody vetted; M16's policy, extended in Lesson 4.
- **Over-exposed services** — "I'll open 8888 to the building for
  convenience" — the tunnel (M22) exists precisely to prevent this.
- **Losing the data anyway** — ransomware, rm accidents, dead disks;
  backups (M17/M24) are the recovery half of security.

Note what's *not* on the list: exotic kernel exploits. Real-world DS
security loss is overwhelmingly the boring stuff — which is exactly
what the hardening checklist covers.

## 8. Try it now (10 minutes)

1. Inventory your VM's doors: `ss -tlnp` — for each listening line,
   write one sentence: what service, whose port, bound where, does
   it *need* to face beyond loopback?
2. AuthN vs authZ sorting: classify — `chmod 640 data.csv`,
   `ssh-keygen`, `AllowGroups ssh-users`, `sudo visudo`,
   `ssh-copy-id`, `setfacl -m u:elena:r--`. (Answers: the first, the
   ssh-copy-id, and setfacl are authZ; the rest authN — feel why.)
3. Surface comparison: `systemctl list-unit-files --state=enabled |
   head -20` — which enabled units could listen on the network?
   (You don't act yet — Lesson 4 audits.)
4. Write your own one-sentence definition of least privilege *in DS
   terms* — you'll reuse it in the quiz.

## 9. Common mistakes

- Treating security as a product you install — it's properties you
  maintain (this module's checklist is a *routine*, not a rite).
- Confusing "nobody would bother attacking me" with "I am safe" —
  bots don't choose victims; they sweep everything.
- Adding controls without layers: a firewall in front of
  password-auth SSH still brute-forceable *through* the firewall.
- Practicing security only once — patch, audit, and backup are
  schedules, not events.

> **Up next:** [Lesson 2 — firewalls & ufw](02-firewall-ufw.md):
> default-deny at the network edge, with the syntax to do it safely.
