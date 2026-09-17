# Module 25 Labs — Security & Firewall

> Two labs, both inside your own VM. Lab 1 is the course's sanctioned
> sshd/ufw application moment — with snapshot, verification gates,
> and a rehearsed rollback. Lab 2 audits a seeded (fake) repository.
> No attack exercises, no external targets, no real credentials —
> defense only, per the module's ethics contract.

| # | Lab | Focus | Time |
|---|-----|-------|------|
| 1 | [lab-01-hardening.md](lab-01-hardening.md) | The hardening lab: snapshot → baseline audit → ufw default-deny → sshd key-only/no-root → service audit → post-audit → rollback rehearsal | ~75 min |
| 2 | [lab-02-secrets-audit.md](lab-02-secrets-audit.md) | Find leaked (fake) credentials in a seeded repo, rotate-and-recover playbook, verify history handling | ~45 min |

Standing rules (recap):

- **Snapshot before Lab 1** (VM checkpoint) — the ultimate rollback.
- The **two-terminal rule** governs every sshd step: never close a
  session until a new one has authenticated.
- Every hardening claim ships a before/after command pair in
  `hardening.md`.
- Lab 2's credentials are fabricated for the exercise; the *tools*
  are real (git history, grep, provider-log reasoning).
