# Module 16 — Package Management · Content Index

> **Status:** Content complete — 3 lessons, 3 labs, quiz + key, 8
> challenges, troubleshooting guide.
> Module contract: [../README.md](../README.md) · Difficulty: Beginner-Intermediate.

## Lessons

| # | File | Topic |
|---|------|-------|
| 1 | [01-apt-dpkg-fundamentals.md](lessons/01-apt-dpkg-fundamentals.md) | packages & dependencies, dpkg, apt, repos/sources, install/remove/upgrade/search/info |
| 2 | [02-repositories-security-ppas.md](lessons/02-repositories-security-ppas.md) | repository anatomy, apt security (signing), PPAs & risks, security updates, unattended-upgrades |
| 3 | [03-beyond-apt-rpm-source.md](lessons/03-beyond-apt-rpm-source.md) | compiling from source (concept + safe walkthrough), DEB vs RPM conceptual map, the DS toolchain: Python/Git/Jupyter/conda & venv |

## Labs

| # | File | Task |
|---|------|------|
| 1 | [lab-01-package-explorer.md](labs/lab-01-package-explorer.md) | Read-only exploration: dpkg queries, apt search/show, dependency trees |
| 2 | [lab-02-safe-lifecycle.md](labs/lab-02-safe-lifecycle.md) | Install→verify→remove a small tool, the safe way (simulation first) |
| 3 | [lab-03-repo-audit.md](labs/lab-03-repo-audit.md) | Audit sources.list(.d), test a PPA safely in a VM, dry-run security upgrades |

## Practice & Support

- [Quiz](practice/quiz.md) (20 Q) · [Answer key](practice/quiz-answers.md)
- [Challenges](practice/challenges.md) (C1–C8)
- [Troubleshooting](troubleshooting.md) — 10 symptom→cause→fix patterns

## Cross-references

- [M18 processes](../../M18-processes-jobs-signals/content/README.md) —
  what packages leave running after install.
- [M27 Python & Jupyter](../../M27-python-jupyter-data/README.md) — deep
  dive on environments; this module covers the *system* side.
- [M25 security & firewall](../../M25-security-firewall/README.md) —
  updates as a security control.
