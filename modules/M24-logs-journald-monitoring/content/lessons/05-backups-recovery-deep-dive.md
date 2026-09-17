# Lesson 5 — Backups and Recovery: The Deep Dive

> Module 24 · Unit 6 · Difficulty: Advanced
> Reading time: ~25 min · Exercises: [the six backup exercises](../labs/backup-exercises.md)
> Builds on: [Lab 4](../labs/lab-04-backup-test-restore.md) (tar + rsync + the
> test-restore), [M17](../../../M17-storage-and-filesystems/content/README.md)
> (virtual disks), [M19](../../../M19-scheduling-cron-timers/content/README.md)
> (scheduling the routine)

---

## 1. The sentence this lesson exists to teach

> **A backup that has never been restored (or verified) should not be
> assumed reliable.**

[M24's Lab 4](../labs/lab-04-backup-test-restore.md) proved it once:
the mirror with `--delete` propagated the disaster; only the
point-in-time archive held the deleted file — and only the *diff*
made the restore trustworthy. This lesson generalizes that lab into
the full discipline: strategy (what to back up, how often), method
(which tool, which compression), lifecycle (retention, rotation),
and recovery (the procedure, the testing, the disaster plan).
Everything targets **safe test directories** — `~/lab24/` — because
the habits must be rehearsal-safe.

## 2. Backup principles — the questions before the commands

Five questions define any backup strategy; skip them and you have
copying, not backup:

1. **What?** — the irreplacable set. Datasets you can't re-download
   *or can't afford to re-generate* (months of preprocessing),
   code, configs, keys (public halves!), the runbook. Explicitly
   *not*: caches, virtualenvs, anything re-creatable — [M25's](../../../M25-security-firewall/content/README.md)
   distinction between assets and rebuildables.
2. **When?** — RPO thinking: *how much data can you afford to
   lose?* Daily dataset changes → daily backups; monthly snapshots
   of rarely-touched archives → monthly. The interval IS the answer
   to "how much would you lose at 3 AM?".
3. **Where?** — the 3-2-1 rule: **3** copies, **2** different
   media, **1** offsite. Lab 4 mapped it honestly (second disk =
   different medium; "offsite" simulated) — in reality: an external
   disk *and* cloud/remote host, with the M22/M23 tools to reach
   it.
4. **How long?** — retention: versions kept per class (§5). Answered
   by policy, implemented by rotation.
5. **Restore how? — and has it been *tested*?** — the question that
   separates backup from wishful thinking. If the restore procedure
   exists only in your head, it doesn't exist.

**The rule, restated at every level:** an unverified backup is a
hope. Verification has three grades — checksum (integrity),
restore-to-scratch (usability), timed full rehearsal (operational
readiness). Lab 4 did grades 1–2; the
[exercises](../labs/backup-exercises.md) do all three.

## 3. Strategy: full, incremental, differential

The three shapes of "what goes in today's backup":

| Type | Contents | Restore needs | Cost per run | Cost per restore |
|---|---|---|---|---|
| **Full** | everything, every time | the latest full only | high (time, space) | lowest, fastest |
| **Incremental** | changes since the *last backup of any kind* | full + **every** incremental since | lowest | highest, chain-risky |
| **Differential** | changes since the *last full* | latest full + latest differential | medium | medium (2 artifacts) |

The trade-offs in one scenario — weekly full, daily variants:

- **Full + incrementals:** cheap nights, but Thursday's restore
  needs Sun-full + Mon + Tue + Wed — four artifacts, any one corrupt
  and the chain breaks.
- **Full + differentials:** Wednesday's restore = Sun-full + Wed-diff
  — two artifacts, one dependency. Differentials grow through the
  week (they re-include Monday's changes); that's the price of the
  short chain.

**rsync implements incremental-shaped backup natively** — it
transfers only changes (delta algorithm, M22/M23) — and the
`--link-dest` trick turns it into a full *snapshot* archive with
incremental *storage*:

```bash
rsync -a --delete \
  --link-dest=~/lab24/backups/latest \
  ~/lab24/precious/ ~/lab24/backups/$(date +%F)/
ln -sfn "$(date +%F)" ~/lab24/backups/latest
```

Each dated directory *looks* like a full snapshot; unchanged files
are hard links into the previous snapshot's inodes (M07's inode
concept, earning its keep) — near-incremental cost, full-snapshot
restore. This is the classic "rsnapshot" pattern, three lines of
it, and the strategy DS teams actually run.

## 4. The tools — tar, and the compression trio

**tar** (tape archive) is the bundler: many files → one stream,
preserving permissions, ownership, timestamps:

```console
$ tar -czf backup-$(date +%F).tar.gz -C ~/lab24 precious    # create, gzip
$ tar -tzf backup-$(date +%F).tar.gz | head                 # LIST before trusting
$ tar -xzf backup-$(date +%F).tar.gz -C ~/lab24/restore     # extract to a target dir
```

Flags worth their muscle memory: `-c` create, `-t` list, `-x`
extract; `-f file`; `-z` gzip; `-C` change-dir (relative paths in
the archive — the portability habit: extract *where you choose*,
not wherever the archive's absolute paths demand). The
list-before-extract rule is Lab 4's: never untar an archive you
haven't inspected.

**Compression** trades CPU for size — and the three levels of the
trade:

| Tool | Speed | Ratio | Typical use |
|---|---|---|---|
| `gzip` (`-z`) | fast | decent | daily defaults, logs |
| `bzip2` (`-j`) | slow | better | archives touched rarely |
| `xz` (`-J`) | slowest | best | long-term cold storage |

```console
$ tar -cf  b.tar   precious; tar -cjf b.tar.bz2 precious; tar -cJf b.tar.xz precious
$ ls -lh b.tar*      # the trade, measured on YOUR data
```

The decision rule: compression is chosen by *how often you'll read
it* — hot backups stay cheap to write (`gzip`), cold archives pay
CPU once (`xz`). And two honest caveats: compression is
**per-stream** in tar (one corrupt block can cost a whole archive —
another reason for checksums + tests), and already-compressed data
(DICOM, video, `.npz`) gains ~nothing — skip the flag, save the
CPU.

## 5. Retention and rotation — the lifecycle

Backups accumulate forever or are pruned by policy. **Retention**
= how long each class is kept (e.g., 7 dailies, 4 weeklies, 6
monthlies — grandfather-father-son); **rotation** = the mechanism
that enforces it. The naive mechanism, made safe:

```bash
#!/usr/bin/env bash
# rotate_backups.sh — enforce retention on ~/lab24/backups/daily/
set -euo pipefail
readonly KEEP=7
readonly DIR="${1:?usage: rotate_backups.sh BACKUP-DIR}"
[[ "$DIR" == "$HOME"/lab24/backups/* ]] || { echo "refusing: outside lab scope" >&2; exit 66; }

# oldest first; delete ONLY beyond KEEP; narrate every removal
mapfile -t old < <(ls -1d "$DIR"/*/ | head -n -"$KEEP")
for d in "${old[@]}"; do
    echo "removing: $d" >&2
    rm -r -- "$d"
done
```

The safety pattern (M25-grade, because rotation *deletes*): scope
guard (refuse paths outside the lab), pattern-exact matching
(`*/` only — never loose files), narration before deletion, and a
`--dry-run` variant for the first runs (M11's doorway). The
[M24 C6](../practice/challenges.md) rotator, promoted to backups.

**Scheduling** closes the loop — [M19](../../../M19-scheduling-cron-timers/content/README.md)'s
stagger doctrine applied: backup at 01:00, rotation at 03:00
(*after* the backup completes — rotating before backing up deletes
yesterday's copy first, the classic ordering bug), verification
weekly.

## 6. Off-site — the copy that survives the building

3-2-1's third leg. The lab simulated it with a directory; reality's
options, in rising sophistication:

1. **rsync to a remote host** — M22/M23's `rsync -avP --delete
   remote:backups/` over SSH: the university server, a friend's
   box, a cloud VM. The transfer is encrypted, authenticated by
   your key.
2. **Cloud object storage** — `s3`-compatible buckets; the
   security-relevant feature is **immutability** (object-lock/
   versioning) — ransomware-era backups must be un-deletable by
   the credentials that wrote them ([M25](../../../M25-security-firewall/content/README.md)
   Lesson 6).
3. **Physical rotation** — the external disk that goes in a drawer
   (offline!). Crude, immune to credential theft, and still what
   many institutions trust.

The offsite rule with teeth: **the offsite copy must not share
fate with the primary** — different credentials, different
location, ideally unreachable by the same compromise. A backup on
the same server (or the same account's cloud) is a copy, not an
offsite.

## 7. Recovery — the procedure and the drill

Restore is the part that matters; write it before you need it:

```text
Restore runbook — <what this backs up>
1. Locate: latest archive = ls -t backups/*.tar.gz | head -1
2. Verify: sha256sum -c backups/precious.sha256
3. Restore TO SCRATCH: mkdir restore-$(date +%F) && tar -xzf <archive> -C !$
4. Verify content: diff -r precious restore-*/precious && echo IDENTICAL
5. Promote: swap directories (mv the old aside — never in-place)
6. Log: timestamp, archive name, sha, result
```

Design rules: restore **to scratch, never over** the original
(the one unrecoverable mistake is restoring garbage onto good
data); verify *before* promoting; the runbook names commands, not
intentions. **Recovery testing** is the scheduled version: a
calendar entry (M19) that *performs* steps 1–6 on a scratch
directory monthly — the timed rehearsal from Lab 4 Part E, turned
into routine. Untested restore is the failure mode of every
"we had backups" postmortem.

## 8. Disaster recovery — when the whole machine dies

Beyond file restore: the machine itself (theft, disk death,
ransomware, fat-fingered `rm -rf ~`). The DR plan asks one
question — **how fast can you be productive on new hardware?** —
and answers it with four artifacts:

1. **Data** — the backups above (offsite).
2. **Environment** — the setup scripts/runbook to rebuild: package
   list (`apt list --installed` snapshot, or better: the M16
   install script), dotfiles in Git ([M26](../../../M26-git-dev-workflows/README.md)),
   the Mini-Project D runbook.
3. **Credentials** — revocable-and-re-issuable (M25's playbook);
   keys regenerated, not restored, onto a new machine.
4. **The plan on paper** — order of operations (new machine →
   updates → keys → data → verify), because 2 AM is not the time
   to design.

The DS framing: your *code* is in Git (M26), your *data* is in
backups, your *environment* is a script, your *results* are
synced (M22). A stolen laptop is an afternoon, not a thesis.

## 9. Try it now (20 minutes)

1. The trade, measured: create the three archives in §4 on your
   `~/lab24/precious` — record the three sizes and create times.
   Which would you ship offsite?
2. `--link-dest` snapshot: run the §3 snippet twice, second time
   after touching one file; `ls -li` both snapshots — identical
   files share inodes (witnessed), one file is new.
3. Retention rehearsal: build five dated dirs, run the rotator
   with `KEEP=2` — narrated removals only; then the scope-guard
   test (`./rotate_backups.sh /` → refused).
4. Write *your* restore runbook (§7's template, filled for
   `~/lab24/precious`) — then execute it once, timed, into a
   scratch dir. That's the untested-backup rule, discharged.

## 10. Common mistakes

- Backing up rebuildables and skipping irreplaceables — the
  inventory question (§2.1) prevents both waste and holes.
- Rotation *before* backup in the schedule (the ordering bug) —
  rotate at 03:00, back up at 01:00, never swapped.
- Restore in place, over the original — scratch first, verify,
  promote (§7's rule 3–5).
- Compression on already-compressed data — CPU spent, bytes
  unchanged.
- Offsite = same account, different folder — shared fate; the
  copy that shares credentials shares doom.
- The untested backup — §1's sentence, one last time: **a backup
  that has never been restored is a hope, not a backup.**

> **Practice:** [the six backup exercises](../labs/backup-exercises.md) —
> scheduled cleanup, dataset/experiment/config backup, the
> deleted-dataset restore, and integrity verification — rehearse
> every section of this lesson hands-on.
