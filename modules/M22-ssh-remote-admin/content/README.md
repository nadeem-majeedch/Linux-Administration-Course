# Module 22 — SSH & Remote Administration · Content Index

## Objectives & navigation

The module's formal **learning objectives, concepts, command-line skills,
laboratory, exercises, and Data Science connection** are specified in the
roadmap: [COURSE-ROADMAP.md — Unit 6 · Services, Networking & Security](../../../COURSE-ROADMAP.md#unit-6--services-networking--security-m20m25).
This page indexes the material; the lessons deliver it.

| Layer | Where |
|---|---|
| Objectives & module contract | [Roadmap](../../../COURSE-ROADMAP.md#unit-6--services-networking--security-m20m25) + [module README](../README.md) |
| Lessons | below, in order — do the end-of-lesson self-checks |
| Labs | [labs/README.md](labs/README.md) |
| Practice | [practice/](practice/) — quiz (+ instructor key), challenges |
| Troubleshooting | [troubleshooting.md](troubleshooting.md) |

> **Status:** Content complete — 4 lessons, 2 labs (incl. a 5-patient
> diagnosis clinic), quiz + key, 8 challenges, troubleshooting guide,
> Mini-Project D.
> Module contract: [../README.md](../README.md) · Difficulty: Advanced.

> 🟡 **Module safety contract:** every lab's "remote" machine is the
> student's **own VM**, addressed as `localhost`/`vm` from its own
> host or via loopback inside it. No real credentials, no external
> hosts, no university servers beyond read-only policy-permitted use.
> Keys created in labs are **lab keys** — never the student's personal
> or GitHub keys. Nothing in sshd_config is applied (read/analyze
> only); hardening *applies* in [M25](../../M25-security-firewall/README.md).

## Lessons

| # | File | Topic |
|---|------|-------|
| 1 | [01-ssh-fundamentals-keys.md](lessons/01-ssh-fundamentals-keys.md) | how SSH works, host keys & known_hosts, key pairs, ssh-keygen, authorized_keys, agent & passphrases, permissions |
| 2 | [02-config-sshd-hardening.md](lessons/02-config-sshd-hardening.md) | ssh_config (Host blocks, aliases, wildcards, ProxyJump) + sshd_config at reading level: password vs key auth, root login, least privilege |
| 3 | [03-remote-execution-tunnels.md](lessons/03-remote-execution-tunnels.md) | remote one-liners, exit codes, scp/rsync-over-ssh, file permissions on transfer, local/remote forwarding, jump hosts |
| 4 | [04-tmux-ds-workflow.md](lessons/04-tmux-ds-workflow.md) | tmux sessions, detach/attach, scrollback; the DS remote-workstation loop: train detached, tunnel Jupyter, sync results |

## Labs

| # | File | Task |
|---|------|------|
| 1 | [lab-01-key-workflow.md](labs/lab-01-key-workflow.md) | The full key workflow against your own VM: generate → deploy → agent → ssh-config aliases → passwordless login verified |
| 2 | [lab-02-diagnosis-clinic.md](labs/lab-02-diagnosis-clinic.md) | Five broken-SSH patients (permissions, agent, known_hosts, config, tunnel) — symptoms only, evidence-first diagnosis |

## Mini-Project

- [Mini-Project D — Remote compute workstation](mini-project-d-remote-compute-workstation.md):
  documented end-to-end SSH workstation — keys, config, tmux loop, a
  tunneled M20 service, and a written operations runbook.

## Practice & Support

- [Quiz](practice/quiz.md) (22 Q) · [Answer key](practice/quiz-answers.md)
- [Challenges](practice/challenges.md) (C1–C8)
- [Troubleshooting](troubleshooting.md) — 10 symptom→cause→fix patterns

## Cross-references

- [M21 networking](../../M21-networking-fundamentals/content/README.md) —
  ports, loopback, and the ladder; SSH runs on 22/TCP.
- [M20 systemd](../../M20-systemd-services/content/README.md) —
  sshd is a service; user units become remotely-managed services.
- [M17 storage](../../M17-storage-and-filesystems/content/README.md) —
  key permissions are file permissions, enforced for real here.
- [M18 signals](../../M18-processes-jobs-signals/content/README.md) —
  tmux answers the "processes die when the session closes" problem.
- [M23 file transfer](../../M23-file-transfer/README.md) — depth on
  rsync/SFTP; this module teaches scp + rsync-over-ssh basics.
- [M25 security](../../M25-security-firewall/README.md) — where
  sshd hardening gets *applied* and firewall'd.
