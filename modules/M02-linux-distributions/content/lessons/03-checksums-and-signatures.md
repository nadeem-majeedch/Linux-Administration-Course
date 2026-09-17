# Lesson 3 — Checksums and Signatures: Trusting What You Download

> Module 02 · Unit 1 · Difficulty: Beginner
> Reading time: ~20 min · Up next: [Lab — identification circuit](../labs/README.md)
> DS framing: this is the supply-chain habit that M16 (packages) and M28
> (image digests) will assume.

---

## 1. Two different questions, two different tools

You've downloaded an Ubuntu ISO (or a dataset, or a model checkpoint).
Two questions matter, and they are *not* the same question:

1. **Is this file exactly what was published?** — *integrity* — answered
   by a **checksum** (a fingerprint of the bytes).
2. **Did the right party publish it?** — *authenticity* — answered by a
   **digital signature** (cryptography binding the file to a key you
   can verify).

A checksum alone tells you the download matches *the list you
downloaded* — but if an attacker swapped both the file *and* the list
(and the list traveled the same compromised channel), the checksum
quietly validates the malware. The signature closes that hole: it's
made with the publisher's **private** key and verified with their
**public** key, so a man-in-the-middle can alter the file but cannot
forge the signature. **Checksum = accident detector; signature =
attacker detector.** Mature verification does both, and the order
matters: verify the *signature on the checksum file*, then the
checksums.

## 2. Checksums in practice

```console
$ sha256sum ubuntu-24.04.1-desktop-amd64.iso
e240e4b4...  ubuntu-24.04.1-desktop-amd64.iso     # the fingerprint (256 bits)

$ sha256sum -c SHA256SUMS                          # verify a whole list
ubuntu-24.04.1-desktop-amd64.iso: OK
```

`sha256sum -c` re-computes each fingerprint and compares — one command
for a directory of downloads. The M26/M31 habit you already know is
this exact tool: dataset manifests (`SHA256SUMS` next to shared data)
and backup verification. Same command family, same discipline: *a
transfer isn't done until the checksum passes.*

Why SHA-256 specifically: MD5 and SHA-1 are **broken for adversarial
use** (researchers can construct *different* files with the same
hash — "collisions"), so a matching MD5 proves accidental corruption
but not malicious substitution. Use MD5/SHA-1 only to detect bitrot;
use SHA-256 for anything a stranger could have touched.

## 3. Signatures in practice (GPG, the distro way)

Distributions sign their checksum files. The verification dance, seen
once slowly:

```console
$ gpg --keyserver hkps://keyserver.ubuntu.com \
      --recv-keys 0x46181433FBB75451 0xD94AA3F0EFE21092     # 1. get Ubuntu's release keys
$ gpg --verify SHA256SUMS.gpg SHA256SUMS                    # 2. verify the list is signed
gpg: Good signature from "Ubuntu CD Image Automatic Signing Key"
$ sha256sum -c SHA256SUMS                                   # 3. NOW the checksums mean something
```

Three steps: fetch the publisher's public key (from a keyserver —
*and* cross-check the fingerprint against the publisher's website,
because keyservers accept anyone's uploads), verify the signature on
the checksum list, then trust the list's contents. Ubuntu publishes
the expected fingerprints on its download page — that cross-check is
the "verify the verifier" step that makes the chain honest.

The helpful warning in the middle of `gpg --verify` output —
*"This key is not certified with a trusted signature!"* — is GPG
saying: the signature is *cryptographically* valid, but you haven't
told me you trust this key. Reading that line correctly (it's about
your web of trust, not about failure) is the lesson's small
literacy milestone.

## 4. The habit, generalized (where you'll use it next)

| Context | Integrity tool | Authenticity upgrade |
|---|---|---|
| ISO/dataset download | `sha256sum -c` | GPG signature on the manifest |
| apt packages | apt's internal checksums | the repo's GPG signature (M16 Lab 0's `signed-by`) |
| pip packages | pip's hash checking | PyPI's infrastructure; `--require-hashes` for strict pins |
| Docker images | registry checksums | **digest pinning** (`@sha256:…`, M28 lesson 1 §4) |
| Your own backups | `sha256sum -c` after restore | your checksum file, stored separately |

The pattern is identical at every layer — fingerprint + signature +
a trusted key — which is why learning it once, here, on an ISO, pays
for the whole course. The failure mode it prevents has a name you'll
hear in security contexts: **supply-chain attack** — the compromise of
something *before* you download it. The M25 course-frame applies from
day one: your security is only as good as the provenance of what you
installed.

---

## Key takeaways

- **Checksum = integrity** (detects accidents); **signature =
  authenticity** (detects attackers); do both, signature on the
  manifest first.
- `sha256sum -c SHA256SUMS` is the one-command verify; MD5/SHA-1 are
  collision-broken and only detect bitrot.
- GPG verification = fetch the *real* public key (cross-check the
  fingerprint) → verify the manifest's signature → then the checksums
  mean something.
- The same pattern recurs at every layer of the course — apt's
  `signed-by`, pip hashes, Docker digests, your own backup manifests.

## Check yourself

1. An attacker replaces both the ISO and the `SHA256SUMS` on a mirror.
   Which step of the full verification catches them, and why?
2. Why is a passing MD5 check still worth doing on your own backup,
   even though MD5 is broken for adversarial use?
3. GPG says "Good signature … not certified with a trusted signature."
   Did verification fail? What is the message actually about?
4. Where does the same integrity+authenticity pattern appear inside
   apt, and which course lab made you type it?

*Answers:* (1) The signature verification — the attacker can't forge
Ubuntu's private-key signature on their fake `SHA256SUMS`, so
`gpg --verify` fails before any checksum is trusted. (2) Because your
backup's realistic enemy is bitrot and partial writes (accidents),
which MD5 detects fine; the adversarial case is covered by storing the
checksum manifest separately (and ideally signed). (3) No — the
signature is cryptographically valid; the message is about your *web
of trust*: you haven't marked that key as trusted/signed. The fix is
verifying the key's fingerprint against the publisher's site and
certifying it locally. (4) apt repos are GPG-signed and apt verifies
signatures + checksums on every fetch; M16 Lab 0's `signed-by=`
keyring line in the Docker repo setup was this pattern's apt form.

Up next: [the labs](../labs/README.md) — run the identification circuit
and verify a download for real.
