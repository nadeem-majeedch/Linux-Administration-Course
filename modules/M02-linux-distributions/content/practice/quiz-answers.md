# Module 02 Quiz — Answer Key

## Section A

**Q1.** Linux is a *kernel* — the program managing hardware and
processes. A distribution is the complete operating system built
around it: shell, utilities, libraries, package manager, installer,
and a support promise — curated and tested by a vendor/community.

**Q2.** Package manager/format, release model, defaults & provenance
(libc, init, who stands behind it). The package manager changes your
daily typing most (`apt` vs `dnf` vs `pacman`).

**Q3.** The predictability argument: rolling releases move the floor
under colleagues' scripts, vendor tooling, and reproducibility
contracts; on a shared server, "always newest" means *someone else can
change your environment by updating* — the drift problem (M29-ext A)
by design. Point/LTS releases let you freeze and verify.

**Q4.** Because the bases are tiny, stable, extremely well-tested, and
their package ecosystems (apt) are what DS tooling targets first —
plus digest-pinnable reproducibility. Choosing an exotic base buys
novelty at the price of every dependency question.

**Q5.** A *support window*: you can plan updates years ahead, pin a
version knowing security fixes will arrive for it, and build
procedures (vendor docs, team scripts) against a floor that will not
move for five years.

## Section B

**Q6.** `cat /etc/os-release` (identity + family via `ID_LIKE`) →
`uname -r && uname -m` (kernel + architecture) →
`command -v apt dnf apk zypper pacman` (which manager exists) →
`uptime` (how long since reboot). Together: one speakable identity
sentence.

**Q7.** You know it's the Red Hat family: expect `dnf` (or `microdnf`)
and `.rpm`-based tooling; predict RHEL-family file locations. Confirm
with `command -v dnf` or `dnf --version`.

**Q8.** `6.8.0-45-generic` is the *kernel* series/version — many
distros ship many kernels; "24.04" is the distro release. The two
number systems answer different questions (driver compatibility vs
package/support).

**Q9.** `os-release` is documented as machine-readable `KEY=value` —
sourcing is stable, correctly escaped, and portable across distros;
parsing a cosmetic string (`PRETTY_NAME`) breaks when wording changes.

**Q10.** Is it still within its support window? Answer from the
release date + Ubuntu's published LTS policy (20.04 standard support
ends April 2025). If past: no security fixes — the box must be
upgraded or isolated; running it exposed is the finding.

**Q11.** Hostnames lie or rot (`prod-ubuntu-03` running Debian; renamed
machines; cloned VMs). Identity comes from files on the machine.

## Section C

**Q12.** Integrity = the bytes are exactly what was published
(*checksum*, e.g. SHA-256). Authenticity = the publisher is really the
publisher (*digital signature*, e.g. GPG over the manifest).

**Q13.** The checksum matches because the attacker computed it over
*their* file — the list validates whatever it lists. You're saved by
the **signature on the manifest**: they can't forge the publisher's
private-key signature, so `gpg --verify SHA256SUMS.gpg SHA256SUMS`
fails before any checksum is trusted.

**Q14.** MD5/SHA-1 are collision-broken — an adversary can craft
different files with the same hash, so a match doesn't prove
non-malice. Your backup's realistic enemy is bitrot/partial writes
(accidents), which MD5 detects; the adversarial case needs SHA-256 +
separate (ideally signed) manifests.

**Q15.** Cryptographically the signature *is* valid — it was made by
the matching private key. Undone: your *web of trust* — you haven't
certified that this key belongs to the publisher. Action: compare the
key's fingerprint against the publisher's website, then certify
(locally sign) it — or at minimum record the cross-check.

**Q16.** apt: repos are GPG-signed, apt verifies signatures +
checksums on every fetch (the `signed-by=` keyring, M16 Lab 0). Docker:
base images pinned by digest `@sha256:…` (M28 lesson 1 §4). Also
acceptable: pip `--require-hashes`, your own backup manifests
(M24/M26).

Practice more: [challenges.md](challenges.md)
