# Lesson 2 — Repositories, apt Security, PPAs & Updates

> Module 16 · Unit 5 · Difficulty: Intermediate
> Reading time: ~35 min · Lab: [Lab 3 — repo audit](../labs/lab-03-repo-audit.md)
> Prerequisites: [Lesson 1](01-apt-dpkg-fundamentals.md)

> 🔒 Safety: this lesson is about *trust* — who you let install software
> as root. The PPA walkthrough is done in a disposable VM with a
> check-first audit; on shared systems, PPAs are a sysadmin conversation,
> never a solo act.

---

## 1. What a repository actually is

A repository = a server holding packages + a **signed index** (metadata
with checksums and versions). `apt update` downloads the index; apt
verifies its signature *before* trusting anything in it. This is why a
repository can serve software to millions of root-privileged installs
without becoming the world's best malware distribution channel.

**Where Ubuntu gets its software** — the standard component list in
`/etc/apt/sources.list` (and per-file drops in `/etc/apt/sources.list.d/`):

```text
deb http://archive.ubuntu.com/ubuntu noble main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu noble-updates main restricted ...
deb http://archive.ubuntu.com/ubuntu noble-security main restricted ...
```

Decoding a source line: `deb` = binary packages (vs `deb-src` source);
URL = the mirror; `noble` = the release codename; the trailing words are
**components**:

| Component | Contents | Support |
|---|---|---|
| `main` | officially supported, free | full Canonical support |
| `restricted` | proprietary drivers etc. | supported |
| `universe` | community-maintained free software | *community* support |
| `multiverse` | software with legal/license restrictions | community, case-by-case |

This matters operationally: a package from `universe` receives
community-level security attention. On a data science VM you'll happily
use universe (much of the science stack lives there) — but you should
*know* that's what you're doing.

** Suites beyond the release:** `noble` (the frozen release),
`noble-updates` (stable fixes), `noble-security` (security fixes),
`noble-backports` (newer versions of select software). Security updates
are the non-optional suite — §4.

---

## 2. How apt decides what to trust

Every source line pairs with a **signing key**: apt checks the
repository's GPG signature against keys in `/etc/apt/keyrings/` (modern)
or `apt-key`-managed legacy stores (deprecated). The machinery:

1. `apt update` fetches `InRelease` (signed index) from each source.
2. Signature verified against a configured key → mismatch = hard error,
   nothing installed from that source.
3. Packages are checksum-verified against that signed index at download.

The errors you'll meet, decoded:

```text
E: The repository ... is not signed.            → key missing/mismatched
W: GPG error ... NO_PUBKEY ABCDEF0123456789     → third-party repo, key not installed
E: Release file expired                         → stale mirror or clock skew
```

Each is apt *working correctly* — refusing unverified software. The fix is
never "disable the check"; it's "install the key through a channel you
actually trust" (§3).

---

## 3. PPAs: power tool, sharp edges

A **PPA** (Personal Package Archive) is Canonical's hosting for
third-party apt repositories — typically a developer publishing builds
faster or newer than Ubuntu's archives (or builds for software Ubuntu
doesn't ship).

```console
$ sudo add-apt-repository ppa:deadsnakes/ppa   # the canonical example:
$ sudo apt update                              #   older/newer pythons for testing
$ apt policy python3.11                        # which source would win now?
```

**Why PPAs are simultaneously useful and dangerous — the honest ledger:**

- ✅ Software Ubuntu doesn't ship, or versions it lags on.
- ❌ **No security SLA.** Canonical signs `main`; a PPA is one maintainer's
  promise. If they vanish, you're pinned to a frozen repo.
- ❌ **Root-privileged installs from a personal account.** `add-apt-
  repository` + `apt install` executes maintainer scripts as root at
  install/upgrade time — the trust question is exactly M14's sudoers
  question with more steps.
- ❌ **Version conflicts:** a PPA python can shadow the system python's
  expectations (this is why the course pushes venv/conda in M27 —
  *isolate* language versions from the OS).

**Course policy for PPAs (write this on your wall):**

1. Prefer the official archives (`main/universe`) first.
2. Need it anyway? Use **well-known, long-lived PPAs only**
   (deadsnakes, graphics-drivers), added in a disposable VM first.
3. `apt policy <pkg>` after adding — *know which source wins* before
   installing.
4. Removal is the mirror of adding:
   `sudo add-apt-repository --remove ppa:...` (plus `ppa-purge` if you
   must downgrade what you installed from it).
5. On any shared/server machine: propose, don't do.

---

## 4. Security updates: the one non-optional habit

Unpatched software is the entry point for the majority of real-world
compromises; apt makes patching nearly free, which makes *not* patching a
choice. The checks:

```console
$ apt list --upgradable                              # what's pending
$ sudo apt update && sudo apt upgrade                # the weekly ritual
$ /usr/lib/update-notifier/apt-check --human-readable   # count only
$ sudo apt-get changelog openssl | head              # what did the fix fix?
```

**Ubuntu Pro / unattended-upgrades:** Ubuntu ships `unattended-upgrades`
(on by default in recent desktops; enable on servers):

```console
$ sudo apt install unattended-upgrades
$ sudo dpkg-reconfigure -plow unattended-upgrades    # enable
$ cat /etc/apt/apt.conf.d/20auto-upgrades            # the switches
$ cat /etc/apt/apt.conf.d/50unattended-upgrades      # the policy (which origins)
```

Default policy: security suite automatically, promptly. Know the boundary:
it won't reboot for kernel updates without `Automatic-Reboot true`, and it
won't help software installed from PPAs (their repos are outside the
default origins — one more PPA cost, §3).

**The DS-server reality:** GPU servers lag on updates because CUDA
pinning and reboot windows are annoying — so they accumulate a year of
unpatched CVEs. Your role as the data scientist in the room: ask for the
`apt list --upgradable | wc -l` number in standup. It's a five-second
question that changes infrastructure culture.

---

## 5. When the trust system breaks (preview)

Common, survivable failures — each has a full runbook in
[troubleshooting.md](../troubleshooting.md):

- **NO_PUBKEY** on a third-party repo → fetch the key from the *vendor's*
  official instructions (they publish a fingerprint; verify it), place in
  `/etc/apt/keyrings/`, reference in the source line with `signed-by`.
- **`apt update` frozen on a slow mirror** → `Ctrl-C`, then a legitimate
  regional mirror or back to archive.ubuntu.com.
- **The dpkg lock fight** (from M18 Lab 2 Ticket C) → diagnose the holder
  before touching anything.

The meta-skill: these errors are *information*. Read the repository URL
in the error; it tells you which trust decision needs revisiting.

---

## Exercises (lab-log.md)

1. `cat /etc/apt/sources.list | grep -v "^#" | head`. Decode one line
   completely (component by component). Is `universe` enabled on your VM,
   and what does that mean for support?
2. `apt policy curl` — output shows two priorities. Explain what
   priority 500 means here and which suite apt would take a new version
   from.
3. Why does the course say "the fix is never 'disable the check'"?
   Connect to one concrete attack the signature system prevents.
4. deadsnakes PPA: what does it exist for, why is it *usually* harmless,
   and what is the specific trap if you `apt install python3.11` over
   the system python3 on an Ubuntu where python3.11 *is* the system
   python?
5. `apt list --upgradable | wc -l` today vs last week (track it in
   lab-log). What changed? Anything security-flagged? (`apt-get changelog
   <pkg>` on the interesting one.)
6. Design question: your lab's server needs CUDA 12.4 but Ubuntu ships
   12.0. Lay out the three options (NVIDIA's official repo, a PPA,
   waiting for Ubuntu), with one risk sentence each. Which does the
   course policy point to, and why?

## Check yourself before Lesson 3

- [ ] I can decode a sources line: deb/URL/codename/components.
- [ ] I know what signing keys do and what NO_PUBKEY really means.
- [ ] I can state the five-point PPA policy from memory.
- [ ] I know what unattended-upgrades covers — and what it doesn't.

## Further reading (official sources)

- `man 5 sources.list`; Ubuntu Repositories docs:
  https://ubuntu.com/server/docs/about-apt-repositories (and PPA pages on
  launchpad.net)
- Debian SecureApt: https://www.debian.org/doc/manuals/apt-howto/
- Ubuntu Pro / esm & Livepatch: https://ubuntu.com/pro
