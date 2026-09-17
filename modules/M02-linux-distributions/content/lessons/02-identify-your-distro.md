# Lesson 2 — Identify Your Distro (From Files, Not Memory)

> Module 02 · Unit 1 · Difficulty: Beginner
> Reading time: ~15 min · Lab: [the identification circuit](../labs/README.md)
> Up next: [Checksums & signatures](03-checksums-and-signatures.md)

---

## 1. The scenario: you're on an unfamiliar box

Day one on the university cluster. The welcome email says "Linux," the
prompt says something unhelpful, and your instructions say "install the
dependencies." Before you run a single package command, you need the
system's identity — because **every command you're about to type
depends on it** (`apt`? `dnf`? which repos? how old is this thing?).

The professional rule: **identify from files on the machine, not from
memory or the hostname.** Hostnames lie (`prod-ubuntu-03` running
Debian 11 is a real ticket); files don't.

## 2. The one file that answers almost everything

`/etc/os-release` is the standard (freedesktop.org) identity file —
present on effectively every modern distro:

```console
$ cat /etc/os-release
PRETTY_NAME="Ubuntu 24.04.1 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.1 LTS (Noble Numbat)"
ID=ubuntu
ID_LIKE=debian
VERSION_CODENAME=noble
```

Read it as a structured ID card: `NAME`/`VERSION_ID` — what and how
old; `ID_LIKE` — **the family** (`debian` → apt-world; `rhel, fedora`
→ dnf-world); `VERSION_CODENAME` — the release name that apt sources
and many docs reference. The machine-readable format (shell-sourceable
`KEY=value` lines) means scripts can use it:

```console
$ . /etc/os-release && echo "$ID $VERSION_ID"
ubuntu 24.04
```

On Red Hat family the same file says `ID="rhel"` (or `rocky`,
`almalinux`) with `ID_LIKE="rhel fedora"` — same reading skill, so the
skill transfers across families.

## 3. The supporting cast

| Command / file | Answers | Notes |
|---|---|---|
| `cat /etc/os-release` | distro, version, family, codename | the first command, always |
| `uname -r` | **kernel** version | the kernel ≠ the distro version (M03's distinction) |
| `uname -m` | architecture | `x86_64` vs `aarch64` — matters for wheels/binaries |
| `cat /proc/version` | kernel + compiler + build host | corroboration |
| `ls /etc/*release* /etc/*version*` | family-specific files | `redhat-release`, `debian_version`, `alpine-release` |
| `apt --version` / `dnf --version` / `apk --version` | the package manager, by experiment | the family's fingerprint, confirmed |

`uname -r` deserves its warning: on Ubuntu 24.04 you might see
`6.8.0-45-generic` — a *kernel* version from the 6.8 series, unrelated
to "24.04". Beginners conflate them constantly; kernel versions matter
for driver compatibility (M31's GPU stack), distro versions for
package/support questions.

Age check — the question that matters on servers: Ubuntu 24.04's LTS
window runs to 2029 (five years from 2024 release, per Ubuntu's
published policy); a machine on Ubuntu 20.04 in 2026 is inside its
window; one on 18.04 is past standard support. The distro version +
release-model knowledge from lesson 1 turns `os-release` into a
**support window**, which is what "should we update this box?" is
really asking.

## 4. The identification circuit (60 seconds, any box)

The lab drills this as muscle memory; the circuit:

```console
$ cat /etc/os-release                    # identity + family
$ uname -r && uname -m                   # kernel + architecture
$ command -v apt dnf apk zypper pacman   # which package manager exists
$ uptime                                 # how long since a reboot (M24's habit)
```

Four commands, and you can speak about the machine: *"Ubuntu 24.04
LTS, Debian family, kernel 6.8, x86_64, apt as the manager, up 46
days."* That sentence is the difference between "I know Linux" and "I
can administer *this* Linux."

---

## Key takeaways

- `/etc/os-release` is the standard identity card — **`ID_LIKE` gives
  the family**, which predicts the package manager.
- `uname -r` is the *kernel* version; don't conflate it with the
  distro version.
- Version + release model = **support window** — the real question
  behind "how old is this box?"
- The 60-second circuit (os-release → uname → package-manager probe →
  uptime) works on any distro you'll ever meet.

## Check yourself

1. A machine's `os-release` says `ID_LIKE="rhel fedora"`. Which
   package manager do you expect, and what would you run to confirm?
2. Why is `uname -r` a *bad* answer to "what distro is this?"
3. You find Ubuntu 18.04 in 2026. What's the support-window question,
   and where does the answer come from?
4. Why is sourcing `os-release` in a script better than grepping
   `PRETTY_NAME`?

*Answers:* (1) dnf (or microdnf in minimal images); confirm with
`command -v dnf` or `dnf --version`. (2) It reports the kernel series,
which is independent of the distro release — many distros ship many
kernels. (3) Is it still inside its support window? — answered from
the release date + Ubuntu's published LTS policy (18.04 standard
support ended April 2023). (4) The file is documented as
machine-readable `KEY=value`; sourcing is stable across distros and
escapes correctly — `PRETTY_NAME` parsing is cosmetic and brittle.

Up next: [Checksums & signatures](03-checksums-and-signatures.md) —
trusting what you download.
