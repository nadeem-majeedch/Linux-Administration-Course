# Module 02 Troubleshooting — Distribution Symptoms → Causes → Fixes

> Six patterns that bite beginners in their first week. Each:
> **symptom → likely cause → diagnosis → fix → prevention**.
> Every diagnosis command is safe on any machine.

## 1. "apt: command not found" (on Fedora/CentOS/Rocky)

**Cause:** you are on an RPM-family distro; `apt`/`dpkg` are
Debian-family tools ([M16](../../M16-package-management/README.md)).
**Diagnose:** `cat /etc/os-release` — `ID=fedora`/`rhel` answers it.
**Fix:** use the family's tool (`dnf`). On a course VM this shouldn't
happen — if you see it, you are on the wrong machine or SSH'd into
somewhere unexpected (run `hostname`, `who`).
**Prevent:** identify before you install. The [identification
circuit](labs/lab-01-identification-circuit.md) is a 5-minute habit.

## 2. Checksum mismatch when verifying an ISO

**Cause (in order of likelihood):** truncated download, wrong
algorithm (`sha256` vs `sha512` line), comparing against the
checksum of a different release/architecture.
**Diagnose:** compare file size against the publisher's listing;
re-run `sha256sum` and diff against the `SHA256SUMS` line, not memory.
**Fix:** re-download; if it fails twice from one mirror, switch
mirrors. Never proceed on a mismatch — see
[Lesson 3](lessons/03-checksums-and-signatures.md).
**Prevent:** download the `SHA256SUMS` file alongside the ISO, always.

## 3. `lsb_release: command not found`

**Cause:** modern minimal images and containers often ship without
the `lsb_release` utility.
**Diagnose:** it doesn't matter — `/etc/os-release` is the
always-present, standardized file (an LSB *specification*, present on
every mainstream distro).
**Fix:** `cat /etc/os-release` or `grep PRETTY_NAME /etc/os-release`.
Install nothing.
**Prevent:** teach scripts to read `/etc/os-release`; it is the
portable contract.

## 4. "My container says Ubuntu 24.04 but it isn't a VM"

**Cause:** `os-release` reports the *distribution of the root
filesystem*, which in a container is the distro image — not the
kernel, and not the virtualization type.
**Diagnose:** `uname -r` (kernel — shared with the host in a
container), `systemd-detect-virt` (`none` inside a typical
container, `kvm`/`oracle` in a VM).
**Fix:** none needed — a vocabulary correction. Say "Ubuntu container
on my host kernel", not "Ubuntu machine".
**Prevent:** Lesson 1's distinction: distribution ≠ kernel ≠ machine.

## 5. Version confusion: "24.04.3" vs "24.04" vs "26.04"

**Cause:** Ubuntu's release grammar (YY.MM, interim vs LTS, point
releases) read as arbitrary numbers.
**Diagnose:** `grep VERSION= /etc/os-release`; recall the policy from
[Lesson 1](lessons/01-what-is-a-distribution.md): LTS = every two
years (April of even years), 5 years of support, point releases are
bugfix rollups.
**Fix:** none required — but pin course work to an LTS so lab results
match the lessons.
**Prevent:** when a tutorial says "Ubuntu 22.04" and you run 24.04,
differences are usually small; when it says an interim release,
expect drift.

## 6. "which distro should I use for X?" paralysis

**Cause:** choice presented as a moral question instead of an
engineering one.
**Diagnose:** write down the actual constraints (course spec,
package availability, support lifetime, hardware).
**Fix:** the course's rule — Ubuntu LTS for coursework because the
lessons and package names match it; otherwise choose by support
lifetime and documentation, not hype.
**Prevent:** any "best distro" debate ends with: *what are you
optimizing for?*
