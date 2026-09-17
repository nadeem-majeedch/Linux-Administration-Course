# Lab 2 — Verify a Download Before You Trust It

> Module 02 · Unit 1 · Difficulty: Beginner · Est. time: 30 min
> Environment: any Linux with `sha256sum` and `gpg` (Ubuntu VM
> recommended). Network use is limited to *downloading one small
> official file*. No root.
> ⚠️ We verify a **checksum manifest** in an isolated directory. Do
> not run hash-checking against system files; do not install what you
> download unless the exercise says so.

## Objective

By the end you can *prove* a downloaded file is what the publisher
published — integrity (SHA-256) and, when offered, authenticity (GPG
signature) — the reflex behind every ISO, dataset, and base image.

## Part A — The safe object (10 min)

Use an Ubuntu ISO's published checksums — or any file from a
publisher that publishes SHA-256 lists (Ubuntu's `SHA256SUMS` for your
version's ISO is the canonical example; fetch it from the official
`cdimage`/`releases` server over HTTPS).

```console
$ mkdir -p ~/lab02-verify && cd ~/lab02-verify
$ # download (or choose) one ISO/image file + its SHA256SUMS file
$ sha256sum -c SHA256SUMS 2>&1 | head
```

- Did the target file verify? Was anything reported *FAILED* or
  missing (the list covers many files — unmatched lines are OK if the
  file you care about says `OK`)?

## Part B — Tamper theater (10 min, controlled)

In your lab directory only:

```console
$ cp your-download.iso tampered.iso   # tiny truncation:
$ truncate -s -1024 tampered.iso      # removes 1 KiB — an "accident"
$ sha256sum tampered.iso
```

- Compare with the recorded value for the original. Confirm the
  hashes differ, then **delete `tampered.iso`**.

## Part C — The signature layer (10 min)

If your publisher provides a *signed* manifest (Ubuntu publishes
`SHA256SUMS.gpg`):

```console
$ gpg --keyserver hkps://keyserver.ubuntu.com --recv-keys <KEYID-from-publisher-page>
$ gpg --verify SHA256SUMS.gpg SHA256SUMS
```

- What does `gpg` warn about the key's *trust*? (It doesn't know the
  key is really Ubuntu's — resolving that is the web-of-trust step
  from Lesson 3: check the fingerprint on the official site.)

## Deliverable

`verify-report.md`: the exact commands + outcomes, the tamper
comparison (hash A vs hash B), and a three-sentence answer: **why did
the tamper change the hash — and what attack would a signature stop
that a checksum cannot?**

## Troubleshooting

- `sha256sum: XXX: no properly formatted checksum lines` — you're
  pointing at the wrong manifest format; check the publisher's page
  for the file layout.
- `gpg: no ultimately trusted keys found` — expected on a fresh key
  ring; the fingerprint check from the publisher's page is the step
  that matters for this lab.
