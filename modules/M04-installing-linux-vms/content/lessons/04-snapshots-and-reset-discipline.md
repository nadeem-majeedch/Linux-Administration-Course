# Lesson 4 — Snapshots and Reset Discipline

> Module 04 · Unit 1 · Difficulty: Beginner → Intermediate
> Reading time: ~20 min · Lab: [Lab 1](../labs/lab-01-provision-the-vm.md) (Part D)
> Up next: [Unit 2 — M05](../../../M05-terminal-and-shell/README.md)

---

## 1. What a snapshot actually is

A snapshot freezes the VM's **virtual disk state** at a moment. Run
one and the hypervisor stops writing new changes to the main disk
file; they go to a delta file. Reverting = discard the delta. The
original bytes were never modified.

Consequences worth knowing precisely:

- Snapshots are **instant** (no copy of 25 GiB happens) and
  **space-consuming** (deltas grow as the VM diverges).
- A long-lived delta chain *slows* disk I/O — snapshots are for
  milestones, not a permanent lifestyle.
- **Reverting deletes everything since the snapshot.** That's the
  feature *and* the discipline problem: revert carelessly and you
  lose a week of lab work along with the disaster.

## 2. Snapshot ≠ backup (the sentence M26 will expand)

| | Snapshot | Backup (M26) |
|---|---|---|
| Lives | inside the hypervisor, same host | on *different* storage |
| Protects against | "I broke the VM" | "the host died / was stolen / hit ransomware" |
| Granularity | whole VM disk state | chosen files, versioned, off-site |
| Restore speed | seconds | minutes to hours |

**The course rule:** snapshots give you the *license to experiment*;
backups give you the *right to survive*. M26 will build the second
system (tar/rsync/restic reasoning, restore drills, off-site copies).
This module builds the first.

## 3. The milestone snapshot policy

Name snapshots like an administrator, not like a tourist:

```
clean-install-2026-09-16    ← day zero, pristine
post-m04-2026-09-18         ← end of this module's labs
pre-m13-2026-10-02          ← before any module that says "dangerous"
working-2026-10-30          ← the monthly 'known good' you keep current
```

Three rules:

1. **Before** any lab whose title includes permissions on system
   files, storage, firewalls, or boot repair — take `pre-<module>`.
   Reverting to it is always cheaper than repairing.
2. **After** finishing each unit — update `working-…`, and delete the
   previous `working-` (one is enough; chains are slow).
3. **Never** snapshot *instead of* committing to Git (M26). Snapshots
   capture the disk; Git captures your *reasoning about changes* —
   and Git history survives even a total VM loss (it has a second
   home on a remote).

## 4. Reverting, demonstrated safely

Right now, in Lab 1's Part D, you'll do a controlled revert:

1. Take snapshot `pre-mess`.
2. Make an obvious mess: create `~/mess.txt`, install one harmless
   package (`sudo apt install -y sl`), verify it exists.
3. Revert to `pre-mess`.
4. Prove the revert: `ls ~/mess.txt` (gone) and `command -v sl`
   (absent).

The two proofs matter more than the trick: *evidence before and
after* is how you demonstrate a restore — the same grading standard
M26 applies to backups, and the capstone applies to you.

## 5. What belongs in `lab-environment.md`

The one-page record you'll keep for the rest of the course:

```markdown
# Lab environment
- Host: ThinkPad T14, 32 GiB RAM, Windows 11 + VirtualBox 7.1
- VM: ubuntu-server-24.04 · 2 vCPU · 4 GiB · 25 GiB · NAT
- User: ds (normal user; sudo group — M14)
- SSH: enabled at install; host-only adapter added for M22
- Snapshots: clean-install-2026-09-16 · working-2026-09-20
- Reset procedure: revert `working-…`; if VM unbootable, revert
  `clean-install-…`, then re-run notes/section-2 setup script
- Verification habit: ISO SHA256SUMS + signature — logged in lab log
```

The *reset procedure* line is the adult part: it says what you'd do
at 2 a.m. with a broken VM, without thinking. Every serious server
you'll ever administer deserves the same line.

## 6. DS connection

The workflow you just built — environment as code + snapshot + reset
procedure + evidence — is exactly what **M28's containers** and
**M29's cloud instances** industrialize. An image is a snapshot you
can share; cloud-init (M29-ext B) is "post-M04 setup" as a script; a
container registry is `clean-install` with a checksum. You are not
learning VM trivia; you are learning the primitive shape of
reproducible environments.

---

**Key takeaways**

- Snapshots are instant deltas for milestones — revert is *loud*
  (it deletes the divergent work) and never a backup.
- Milestone naming policy: `pre-<module>` before danger, one current
  `working-…`, never instead of Git.
- `lab-environment.md` — host, specs, user, snapshot names, reset
  procedure — is the first document of your admin career.

**Check yourself:** your VM's disk is corrupt *and* your host
physical drive failed last night. What do snapshots get you? What is
gone that only M26-style backups could have saved?

**Next:** [Unit 2 — M05](../../../M05-terminal-and-shell/README.md)
