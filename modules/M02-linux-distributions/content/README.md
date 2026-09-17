# Module 02 — Linux Distributions · Content Index

> **Status:** Content complete — 3 lessons, 2 labs, quiz + key, 4 challenges.
> Module contract: [../README.md](../README.md) · Difficulty: Beginner.

## Learning objectives

By the end of this module you can:

- Explain what a distribution is and how the kernel, userland, and package
  ecosystem compose into one.
- Place the major families (Debian/Ubuntu, Red Hat/Fedora, SUSE, Arch, Alpine)
  by package manager, release model, and typical use.
- Identify the distribution, version, and support window of *any* system you
  land on — from files, not memory.
- Verify an ISO's integrity and authenticity with checksums and GPG — and
  explain why both steps exist.

## Files

| # | File | Topic |
|---|------|-------|
| 1 | [lessons/01-what-is-a-distribution.md](lessons/01-what-is-a-distribution.md) | Kernel + userland + package manager = distro; families and release models |
| 2 | [lessons/02-identify-your-distro.md](lessons/02-identify-your-distro.md) | `/etc/os-release`, `uname`, `lsb_release`-style discovery; support windows (LTS policy) |
| 3 | [lessons/03-checksums-and-signatures.md](lessons/03-checksums-and-signatures.md) | sha256 verification, GPG signatures, why both; the supply-chain framing |
| Labs | [labs/README.md](labs/README.md) | Two labs: identify-the-system circuit; verify-a-Downloaded-ISO drill |
| Practice | [practice/quiz.md](practice/quiz.md) → [key](practice/quiz-answers.md) · [challenges](practice/challenges.md) | 16-Q quiz + key; 4 challenges |
| Troubleshooting | [troubleshooting.md](troubleshooting.md) | Six distro symptoms → causes → fixes (wrong package manager, checksum mismatches, os-release confusion) |

## DS connection

You will meet Debian-family servers, RHEL-family HPC clusters, and
Alpine containers — often in the same month. Reading a system's identity
from files (not from a cheatsheet) is the first administration skill, and
checksum verification is the supply-chain habit that M16 and M28 extend.

## Cross-references

- [M01](../../M01-what-is-linux/README.md) — what Linux is; this module:
  which Linux.
- [M16](../../M16-package-management/README.md) — apt in depth; here:
  ecosystems compared.
- [M28](../../M28-docker-containers/README.md) — Alpine/Debian bases and
  why the choice matters.
