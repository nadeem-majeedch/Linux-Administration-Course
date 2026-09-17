# Module 25 — Security & Firewall · Content Index

> **Status:** Content complete — 6 lessons, 2 labs (the hardening lab
> + the secrets audit), quiz + key, 8 challenges, troubleshooting
> guide, and the **server hardening checklist** artifact.
> Module contract: [../README.md](../README.md) · Difficulty: Advanced.

> 🟡 **Module ethics & safety contract:** this module teaches
> *defense*. Every exercise lives inside the student's own VM; there
> is no scanning, exploitation, credential capture, persistence,
> malware, or evasion content — not because the techniques are
> secret, but because they are off-mission and off-limits. Attacking
> systems without authorization is a crime and a course-expelling
> offense; here you learn to make systems *hard to attack*, with
> every change documented and reversible.

## Lessons

| # | File | Topic |
|---|------|-------|
| 1 | [01-principles.md](lessons/01-principles.md) | least privilege, defense in depth, authN vs authZ, attack surface, the course's security story so far |
| 2 | [02-firewall-ufw.md](lessons/02-firewall-ufw.md) | packet-filter model, default-deny, ufw syntax/app profiles/limit, nftables & iptables beneath, Ubuntu-vs-RHEL (firewalld) |
| 3 | [03-ssh-hardening-applied.md](lessons/03-ssh-hardening-applied.md) | M22's reading → practice: sshd drop-ins, key-only, no-root, the two-terminal rule, rollback discipline |
| 4 | [04-services-updates-packages.md](lessons/04-services-updates-packages.md) | the listening-service audit, attack-surface reduction, unattended-upgrades, apt trust (GPG, checksums), supply-chain thinking |
| 5 | [05-secrets-credentials.md](lessons/05-secrets-credentials.md) | secrets vs config, env vars, file permissions, .env & .gitignore discipline, API keys in notebooks, the secrets checklist |
| 6 | [06-monitoring-layers.md](lessons/06-monitoring-layers.md) | logs & auditing (auditd), MAC frameworks (AppArmor vs SELinux), fail2ban, malware concepts & backups as recovery |

## Labs

| # | File | Task |
|---|------|------|
| 1 | [lab-01-hardening.md](labs/lab-01-hardening.md) | The hardening lab: snapshot → baseline audit → ufw default-deny → sshd key-only/no-root (with the two-terminal rule) → service audit → post-audit → rollback rehearsal |
| 2 | [lab-02-secrets-audit.md](labs/lab-02-secrets-audit.md) | Audit a provided (fake, seeded) repo for leaked credentials; fix; verify with git history tools |

## The Checklist

- [Server hardening checklist](hardening-checklist.md) — the
  module's one-page takeaway: baseline → network → ssh → services →
  updates → secrets → monitoring → recovery, each item with its
  verification command. Printable; used as Lab 1's rubric.

## Practice & Support

- [Quiz](practice/quiz.md) (22 Q) · [Answer key](practice/quiz-answers.md)
- [Challenges](practice/challenges.md) (C1–C8)
- [Troubleshooting](troubleshooting.md) — 10 symptom→cause→fix patterns

## Cross-references

- [M22 SSH](../../M22-ssh-remote-admin/content/README.md) — Lesson 3
  *applies* what M22 read; the two-terminal rule comes from there.
- [M24 logs](../../M24-logs-journald-monitoring/content/README.md) —
  auth.log, journald and the incident method are this module's eyes.
- [M21 networking](../../M21-networking-fundamentals/content/README.md) —
  ports, sockets, bind scope; the firewall filters what that module
  explained.
- [M14 sudo](../../M14-sudo-root-principle/content/README.md) and
  [M12/M13 permissions](../../M12-users-groups-permissions/README.md) —
  least privilege's local form.
- [M16 packages](../../M16-package-management/content/README.md) —
  apt trust, unattended-upgrades, PPA policy.
- [M26 Git](../../M26-git-dev-workflows/README.md) — where secret
  hygiene meets version control (.gitignore discipline).
- [M17 backups](../../M17-storage-and-filesystems/content/README.md) &
  [M24 3-2-1](../../M24-logs-journald-monitoring/content/README.md) —
  recovery is a security control.
