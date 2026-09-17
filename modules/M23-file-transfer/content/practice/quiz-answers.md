# Module 23 Quiz — Answer Key & Grading Guide

> **Instructor material** — not for distribution with the quiz.
> Grading: command answers are judged on "would it work if typed",
> not exact form; reasoning answers are judged on the *mechanism*.
> Student paper: [quiz.md](quiz.md).

## Section A — Tool selection

**A1 (Q1).** `rsync --partial --progress` (resume the partial file
on retry; `--append-verify` would go further for stable files but
is not the default answer here). scp's fundamental lack: **no
destination-side state awareness** — it streams to a fresh
temporary copy and cannot continue from transferred bytes; a new
invocation restarts from offset zero because it never inspects what
already exists.

**A2 (Q2).** Bottleneck = **per-file negotiation latency** (round
trip + fs metadata operations per file), not bandwidth. 40,000
files → 40,000 handshakes; one tar stream amortizes everything over
a single sequential transfer. Accept: "metadata/RTT dominates for
small files".

**A3 (Q3).** (1) `-z` compresses in flight, but `.gz` data is
already compressed — CPU spent for ~0% size reduction; (2) `-h`
affects *display only*, harmless but pointless in scripts. Corrected:
`rsync -av --progress data.csv.gz vm:~/`. (Full credit: identifying
-z as the waste; noting -h is cosmetic.)

**A4 (Q4).** Any concrete lab-evidenced scenario: e.g. browsing
`/data/incoming` to *find* the right files before pulling, mixing
`get`/`put`/`rm` in one authenticated session, or when the exact
remote paths aren't known in advance. Accept any answer whose core
is "interactive discovery with one connection".

**A5 (Q5).**

```
rsync -a src dst/   →   dst/src/<files>      (nested)
rsync -a src/ dst/  →   dst/<files>          (merge)
```

Fix: add the trailing slash to the *source*: `rsync -a src/ dst/`.

## Section B — Flags & semantics

**B6 (Q6).** `-a` ≡ `-rlptgoD`: recursive, symlinks as symlinks,
permissions, times, group, owner, device/special files. Root-only on
destination: **owner (`-o`) and group (`-g`)** — a normal user can't
chown/chgrp to arbitrary principals. Course purposes are unaffected:
files land owned by the receiving account, modes and times still
preserved, which is exactly the M13 expectation for personal trees.

**B7 (Q7).** `-P` (capital) = port for scp; `-p` = preserve
times/modes. Typo: `scp -p 2222 file vm:` — silently preserves
timestamps instead of using port 2222 (and then fails to connect if
22 is closed — the danger is the *silent* semantic switch on hosts
where port 22 also answers).

**B8 (Q8).** Comparison pair: **size + mtime** — `touch` changed
mtime only, rsync assumes "changed" and re-sends. Avoidance:
`--checksum` (reads every byte both sides — much slower, use for
audit-grade verification, not routine sync).

**B9 (Q9).** Ambiguity: is an excluded file's absence at the source
a *deletion to propagate* or a *file to leave alone*? Explicit flag:
`--delete-excluded`. Safer alternative: `--backup --backup-dir=...`
so removals are archived, not destroyed.

**B10 (Q10).** Push-with-`--delete` risk: the **server** loses files
deleted locally (source-of-truth = laptop). Pull-with-`--delete`
risk: the **laptop** loses files deleted server-side. Same command,
opposite casualty — decide the master side first.

**B11 (Q11).** `--append-verify` assumes the existing destination
bytes are a valid prefix of the source; a concurrently appended
destination has extra trailing bytes that aren't in the source
prefix → "resume" produces interleaved/corrupt content even after
verification detects a mismatch (or worse, passes on changed
prefixes). Correct choice: copy live files **whole** (no append
resume).

**B12 (Q12).** The **`speedup is`** ratio. Intuition: 1.0 means
"transferred everything, no savings"; a *dropping* trend across
nightly runs (e.g. 3.0 → 1.2) means timestamps/content churn —
builds rewriting files wholesale. Investigate excludes.

## Section C — Verification & provenance

**C13 (Q13).** rsync compared size+mtime and saw a match (the edit
preserved both — e.g. same-size in-place edit with preserved
timestamp, or clock skew); the sha256 manifest compares *content
digests* and cannot be fooled by metadata. Catch command:
`rsync -avhc --dry-run` (or the full manifest diff, which is what
the lab does).

**C14 (Q14).** Reproducibility: it answers "which exact bytes did
the analysis consume?" — a provable fingerprint of the input state
at analysis time, enabling bit-level re-verification and audit
(M19's unverified-claim rule applied to inputs, not just backups).

**C15 (Q15).** In `diff a b`, `<` lines come from the *first* file
(local.sha256) — so the **local** copy has the changed file; the
server's version differs. (Accept: "< = present in local, not
matching remote".)

**C16 (C16).** The laptop gets the 14:00 state restored over the
17:00 state (pull enforces server-as-master); a real conflict.
Policy word: **immutable snapshots** (accept: versioned/immutable
datasets; the M19 principle that a shared dataset never mutates
under analysts).

## Section D — Safety & automation

**D17 (Q17).** (1) **Argument guards** (`${1:?...}` + `set -euo
pipefail`) — prevents running with a silent empty source (which
with `--delete` would wipe the destination); (2) **dry-run
rehearsal shown to the operator** — prevents unreviewed deletions
and wrong-destination surprises; (3) **explicit y/N confirmation +
timestamped log** — prevents accidental applies and unprovable
claims later.

**D18 (D18).** Modes: (a) the job hangs forever waiting on a
password prompt that never arrives (annoying, eventually killed);
(b) a well-meaning admin "fixes" it by embedding credentials in the
script (dangerous: password at rest in a file, in history, in
backups). `BatchMode=yes` makes key-less runs **fail immediately
and loudly** — no prompt, no hang, no credential temptation.

**D19 (D19).** Two-line policy, e.g.:
> "No `--delete` runs unattended without a same-command `--dry-run`
> executed and archived first. All deletions use
> `--backup --backup-dir` for one retention cycle."
(Full credit for both the dry-run evidence requirement and the
non-destructive backup gate.)

**D20 (D20).** Denominator = the bytes that would move on a full
copy (naive total); `speedup = total_size / sent`. 1.0 = no savings
(first sync or full churn); higher = more reuse of existing
destination state.

---
*Grading note: Q10, Q13, Q17, Q18 discriminate well — students who
memorized flags but not mechanisms reliably miss these.*
