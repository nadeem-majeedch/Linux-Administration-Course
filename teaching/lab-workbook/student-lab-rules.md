# Student Lab Rules — The Safety Contract

> Read once before your first lab. These rules exist because the course
> teaches *genuinely dangerous operations* — that is what administration
> means — and the difference between a professional and a liability is
> exactly this list.

## The four-line rule for risky commands

Any command that can destroy or lock out gets stated in four lines
before you run it (and your labs state them for you):

| Line | Question it answers | Example (`mkfs` on a loopback disk) |
|---|---|---|
| **Purpose** | why this command exists | creating a filesystem — how disks are born |
| **Risk** | what it destroys, worst case | formatting the *named device*, permanently |
| **Safe environment** | why today's version is safe | the device is a **loopback file**, not a real disk |
| **Recovery** | how you undo the mistake | snapshot restore — or nothing, which is the lesson |

If you can't state all four, you're not ready to run it — ask.

## The seven habits (graded, not just advised)

1. **Transcript first.** `script labN.log` *before* any work — the
   transcript is your submission; late starts lose method marks.
2. **Predict before run.** One line: what will this output? Wrong
   predictions are *good* — they're the lesson being caught early.
3. **`ls` before `rm`.** Every glob expands before the command sees it.
   The reflex: `ls *.csv` → read → then `rm *.csv`.
4. **Dry-run before `--delete`.** rsync, cron-driven syncs, any
   mirror — the dry-run output gets *read*, not just produced.
5. **Second session before locks.** Firewall or auth lab? Open a second
   session *before* enabling anything restrictive. One day you'll be
   the admin locked out of production — the habit starts here.
6. **Census before teardown.** `ls` the path, confirm it's *yours and
   this session's*, then remove by exact name. `rm -rf ~/m23lab` only
   after printing and reading it.
7. **Checkpoint answers inline.** The Checkpoint questions in each lab
   are the assignment; commands are the easy part.

## Snapshot discipline

- **Snapshot points** are called during labs — take them even if you
  feel you don't need to
- **A snapshot is not a backup** — it lives on the same disk. When the
  course asks for backups (M19, M24, capstone), it means a *restored-
  and-verified* copy elsewhere. The distinction is graded.
- Broken VM before week 8? Rebuild from snapshot; nobody's grade cares.

## What's out of bounds (always)

- Nothing against the **host** OS (your laptop's real disk, real
  partitions, real boot)
- Nothing against **other students'** machines or accounts
- Nothing against **external systems** — network labs are loopback by
  design; scanning or connecting beyond `localhost`/your own VM is an
  academic-integrity matter, not just a safety one
- No **real credentials** anywhere — lab keys are lab keys; your
  personal GitHub keys never appear in course work

## Getting unstuck

1. Re-read the lab's **Troubleshooting hints** section — every lab has
   one
2. Check the module's **troubleshooting page** (linked from the unit
   index)
3. Ask with **evidence**: the exact command + the exact error, not "it
   doesn't work"
4. Office hours bring the **VM** — diagnosis together beats fixes done
   to you

## Why this page is graded culture, not decoration

Every LA circuit deducts for unsafe moves; the practical exam has
published zero-score triggers (dangerous commands, missing transcript);
the capstone rubric's security area reads your *habits*, not your
claims. The professional you're training to be starts with these seven
habits.
