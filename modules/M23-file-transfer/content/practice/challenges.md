# Module 23 Challenges — File Transfer & Synchronization

> Attempt [the quiz](quiz.md) first. Challenges are ★★–★★★;
> all work stays inside your own VM. Evidence transcripts required.

## 1. The delete-proof sync (★★)

Extend `sync-results.sh` into `mirror.sh` supporting an optional
`--mirror` flag that enables `--delete` — but *only* through all
three gates: (a) dry-run output saved to `mirror-rehearsal.log`,
(b) the apply requires a separate explicit `--go` flag on a second
invocation that first diffs the new rehearsal against the archived
one, (c) `--backup --backup-dir=../trash/%Y%m%d/` so nothing is
ever destroyed. Deliverable: the script plus a transcript
demonstrating an aborted apply, an approved apply, and the trash
dir containing a rescued file.

## 2. Speedup forensics (★★)

Seed two directories: one of 2,000 small files, one single 200 MB
file, identical total bytes. Time both `rsync` runs; compute
throughput (MB/s). Then transfer each as a `tar` stream:
`tar cf - dir | ssh localhost 'tar xf - -C dest'`. Produce a
four-row results table with one conclusion sentence about when
archiving beats syncing. Deliverable: table + transcript timings.

## 3. The reproducibility pack (★★★)

Create `pack-dataset.sh <dir>`: builds `dataset.tar.gz` *and*
`SHA256SUMS` (relative paths only, sorted), verifies the archive by
extracting to a temp dir and re-hashing (`diff` must be empty),
prints a final `pack: VERIFIED` line or exits 1. Then round-trip
the pack through localhost and have a classmate verify your pack
with only the two files. Deliverable: script, verification
transcript, and the classmate's one-line confirmation. (This is
M19's restore test and M23's manifest verification, fused.)

---
*Solutions stay with the instructor; your transcript is the
evidence. Cross-checks: [quiz](quiz.md) · [lessons](../lessons/01-transfer-toolbox.md)*
