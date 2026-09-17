# Lesson 4 — Services, Updates and Package Security

> Module 25 · Unit 6 · Difficulty: Advanced
> Reading time: ~25 min · Lab: [Lab 1 — hardening](../labs/lab-01-hardening.md)
> Up next: [Lesson 5 — secrets & credentials](05-secrets-credentials.md)

---

## 1. Attack surface, the operational half

Lesson 1 defined the attack surface; this lesson manages its two
biggest components: **what runs** (services) and **what's current**
(updates). The running joke of sysadmin security — "it's always
either a stale service or an unpatched bug" — is really a statement
that these are the two controls with the highest return on minutes
spent.

## 2. The listening-service audit

The audit that Lab 1 formalizes — read every door, justify it or
close it:

```console
$ ss -tulpn            # all listening TCP+UDP sockets, with owners (sudo for process names)
Netid State  Local Address:Port   Process
tcp   LISTEN 127.0.0.1:631        cupsd            ← print service, loopback: local-only risk
tcp   LISTEN 0.0.0.0:22           sshd             ← the intended door
tcp   LISTEN 127.0.0.1:8000       python3          ← my lab server, loopback: fine
```

The three questions per line (the audit rubric):

1. **What is it?** (process name — M18/M20 skills identify it.)
2. **Bound where?** — `127.0.0.1` = local-only exposure
   ([M21](../../../M21-networking-fundamentals/content/README.md) bind
   scope); `0.0.0.0`/`[::]` = network-facing. A `0.0.0.0` line you
   can't justify is a finding.
3. **Needed?** — justify or close.

Closing the unneeded — the spectrum of escalation:

```console
$ sudo systemctl disable --now cups.service   # stop NOW + stop at boot (if truly unneeded)
$ sudo apt purge cups                          # remove entirely (surface: zero)
$ sudo systemctl mask cups.service             # refuse to start even if something asks
```

`mask` is the strongest non-removal move — it symlinks the unit to
`/dev/null` so nothing (including a dependency's activation) can
start it. Trade-off to state in the audit log: disabling a print
service on a *server* is routine; on the machine you print from, it
isn't — the audit records the *reasoning*, not just the action.

**Services you didn't start** deserve special respect: anything
listening that you can't attribute is investigated (M24's method:
`journalctl -u <unit>`, dpkg.log for what installed it) before it's
closed — closing is easy, but *knowing what you closed* is the
audit's point.

## 3. Updates — patch management as a security control

Unpatched software is the surface that *grows by itself*: every CVE
published for something you run increases your risk without you
touching anything. The controls:

```console
$ sudo apt update && sudo apt upgrade        # the discipline: update index, then apply
$ apt list --upgradable                       # what's pending (the M16 read-only view)
$ sudo apt install unattended-upgrades        # automatic SECURITY patches
$ sudo dpkg-reconfigure -plow unattended-upgrades   # enable the daily timer
$ systemctl status apt-daily-upgrade.timer    # verify the machinery runs
```

The policy this course teaches — and it *is* a policy choice:

- **Security patches: automatic** (`unattended-upgrades` defaults to
  the `-security` pocket). Weeks-old CVEs on internet-facing
  machines are how most compromises happen; this one line closes
  the majority of them.
- **Everything else: scheduled, supervised** — feature upgrades
  change behavior; they get a maintenance window, not a cron job.

The [M16](../../../M16-package-management/content/README.md) "security
debt" habit returns as a *scheduled* check: `apt list --upgradable |
grep -ci security` in your weekly routine (M19 will schedule it for
real). Reboot discipline belongs to the same topic — a patched
kernel isn't *running* until rebooted (`uptime` vs
`/var/run/reboot-required` or `cat /var/run/reboot-required.pkgs` —
Ubuntu's gentle nag file).

## 4. Package security — trust, verification, supply chain

[M16 Lesson 2](../../../M16-package-management/content/README.md)
covered apt's signature trust and the PPA ledger. The security
framing completes it — **the supply chain is part of your attack
surface**:

- **Official repos** — GPG-signed, curated, patch-monitored. The
  trust anchor. Stay here for system software.
- **PPAs/third-party apt sources** — trust the *maintainer* as you
  trust root on your machine (that's the privilege you grant their
  packages). The M16 ledger policy, restated as risk management.
- **pip/conda from the internet** — PyPI is uncurated; the
  [M27](../../../M27-python-jupyter-data/README.md) stack's hygiene
  (pinned versions, known indexes, virtualenvs) is supply-chain
  security. **Typosquatting** — `reqests`, `python-csv` — is the
  documented, successful attack on exactly this channel: a typo'd
  package name resolving to a malicious lookalike. The defenses:
  slow down, tab-complete, verify the project before the install.
- **Scripts from the internet** — `curl | sudo bash` executes
  unreviewed code as root. Course policy: download, *read* (skim at
  minimum), then run — the curl-pipe-to-shell pattern is banned
  except from sources you'd already trust with root.

### Verifying a download — checksums and signatures

```console
$ sha256sum dataset.tar.gz                     # compare against the publisher's hash
3f7a...  dataset.tar.gz
$ gpg --verify dataset.tar.gz.asc dataset.tar.gz   # cryptographic signature check
gpg: Good signature from "Producer <key@producer.example>"
```

`sha256sum` detects *corruption* (and hash-mismatch tampering when
you obtain the hash over a second channel); `gpg --verify` detects
*tampering* cryptographically — a signature only the holder of the
private key could produce. The [M24 backup
lab](../../../M24-logs-journald-monitoring/content/README.md) already
made sha256 a habit; here it earns its security meaning. Know both,
use checksums reflexively, use signatures for anything
sensitive.

## 5. Ubuntu/Debian vs Red Hat — patch and audit dialects

| Task | Ubuntu/Debian | Red Hat family |
|---|---|---|
| Security updates, auto | `unattended-upgrades` | `dnf-automatic` |
| Apply all updates | `apt update && apt upgrade` | `dnf upgrade` |
| Update history | `/var/log/apt/history.log`, `dpkg.log` | `dnf history` |
| Verify package integrity | `debsums` (optional pkg) | `rpm -Va` (built-in) |
| MAC framework | **AppArmor** (default) | **SELinux** (default) |

The last row previews
[Lesson 6](06-monitoring-layers.md)'s deep dive — but notice the
pattern holding across both lessons: *same kernel machinery,
different front-ends*, and a competent admin translates between
dialects by naming the concept, not the command.

## 6. Try it now (15 minutes)

1. Full audit table for your VM: `ss -tulpn` → for each line,
   record process / bind address / needed? / action. (Lab 1 uses
   this exact table as its baseline artifact.)
2. Patch status: `apt list --upgradable` — how many pending? How
   many `-security`? If unattended-upgrades isn't active
   (`systemctl status apt-daily-upgrade.timer`), note it as a
   finding.
3. The reboot check: `ls /var/run/reboot-required 2>/dev/null &&
   cat /var/run/reboot-required.pkgs` — is a patched kernel waiting?
4. Supply-chain drill: pick one Python package you'd actually
   install; check its canonical name on PyPI's website vs a
   typo'd variant. Feel how close the names sit — that's the
   typosquatting surface, witnessed safely.

## 7. Common mistakes

- `disable` when you meant `disable --now` — the service stops at
  next boot but keeps running *today*.
- Auditing only TCP — `ss -tulpn` includes UDP; DNS-ish and
  discovery services lurk there.
- "No news is good news" for updates — pending security patches
  announce nothing; you must look (or automate the looking).
- Trusting a checksum posted next to the download — same channel,
  same compromise. Second channel (publisher's HTTPS page, signed
  release email) or it doesn't count.
- Purging a service without recording *why* — six months later the
  audit log is the only memory of the decision.

> **Up next:** [Lesson 5 — secrets &
> credentials](05-secrets-credentials.md): the half of security that
> lives in your notebooks, scripts, and .gitignore.
