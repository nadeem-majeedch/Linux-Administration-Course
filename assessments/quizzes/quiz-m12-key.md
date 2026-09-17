# Quiz M12 — Answer Key

> Grading: reasoning-based answers earn full credit when the
> *mechanism* is correct, even if wording differs. Command answers
> are graded on "would it work if typed", not exact form.

## Section A — Evidence interpretation

**A1.** The mode `-rw-r-----` grants group `research` read but no
write; `other` nothing. Ben *is* in `research`, so the **group
triad** decides: he can read (`cat` succeeds) but not write. If Ben
were not in the group it would fail — class: **Permission denied**
(EACCES). Two fixes ranked least-privilege: (1) `chmod g+w` *only if*
write-for-group is actually intended; (2) `sudo usermod -aG research
ben` (needs re-login). Weakest: 6→664 or granting `other` anything.

**A2.** The `chgrp`/`chmod` are fine — the failure is that the
teammate is **not a member of `research`** (`groups` shows only
`teammate`). Group *ownership* of the file grants nothing to a user
who isn't in that group. The actual gate is group membership
resolved at access time, not at file-creation time. Fix:
`sudo usermod -aG research teammate` then re-login (`newgrp
research` for a shell only).

**A3.** `ls -l` resolves UIDs/GIDs to **names** via the local
user-database (NSS); `ls -ln` shows the **raw numeric IDs**. You
need `-n` when names can't be resolved or mislead: mounted disks
from another machine, containers, deleted users (shows orphaned
UIDs), or scripting where you care about the number.

**A4.** `d` directory; owner `rwx`; group `rws` → **SGID** on the
directory (new files inherit the directory's group); other `r-T` →
read, no execute-bit *for others* — and **sticky bit** (capital `T`
because other-execute is absent). Capital `T` vs lowercase `t`
encodes exactly that: sticky set, other-execute clear.

## Section B — Scenario diagnosis

**A5.** Reasons: (1) umask `0022` strips group-write and all of
other → mode `644` for the file… but the *execute* failure has two
independent layers: scripts created as `644` lack `x` entirely, and
even `chmod +x` only helps if the teammate can read it (they can,
644) — the real second reason is the mode is owner-writable-only so
a *teammate's* edit would be denied. Minimal fix: `chmod 755
deploy.sh` (or 750 if group-only). Preventive umask for a shared
group project: `0002` (group-write preserved via SGID dirs — see
Q6).

**A6.** **SGID on the directory is set (the `2`), but Ben's
*primary* group check isn't the mechanism — inheritance is**:
with SGID, new files take the *directory's* group. So if the file
lands as group `ben`, the directory **lacks the SGID bit** (or Ben
created it before the bit was set). The `2` in a correct `2770`
forces new entries to inherit group `research`. Check-order rule:
chmod on a directory only affects new files; existing files keep
their group until `chgrp -R`.

**A7.** `usermod -G` **replaces** the entire supplementary-group
list with just `docker` — removing the `sudo` membership. Recovery
(requires another admin or recovery shell):
`sudo usermod -aG sudo,docker ben`. Never-causes pair:
`-a` (append) with `-G`.

**A8.** For a **2-hour audit on production**, (b) ACL is correct:
`setfacl -R -m u:auditor:rx /srv/one-tree` grants exactly that tree,
no new group to clean up, revocation is one `setfacl -x`.
(a) forces a new group + chgrp -R (touches the tree, risks
collateral) then membership management; (c) copies data — for
production data that's a confidentiality and staleness problem.
(a) is the right tool for *standing* team access, not temporary.

## Section C — Design & justify

**A9.** Tree root: `root:project`, mode `2750` (SGID for group
consistency). Student folders: `2770`, owner the student, group
`project` — group can't write (owner-only write) but reads.
Data folder: `2540`/`0550` root-owned — read-only for group.
The `2` (SGID) keeps group inheritance coherent; the sticky bit on
shared *drop* dirs (1777-style) would let owners delete only their
own files. **Cannot deliver alone:** "only its owner may delete" in
a *group-writable* directory is the sticky bit's job — but for
group-writable project data, deletion is governed by directory
write permission; pure mode bits cannot express per-file delete
authority once the directory is writable (that's what the sticky
bit or ACLs are for).

**A10.** Three sentences, policy voice:
1. `chmod -R 777` grants read+write+execute to *every account on the
   system* — including service accounts — and makes every file
   world-writable, so the "fix" silently converts a one-file ticket
   into a whole-tree confidentiality/integrity exposure.
2. Its damage outlives the ticket because it erases the *original*
   modes (no record of what 640 vs 755 was), so you can't tell later
   which paths were intentionally open.
3. Policy: every chmod ticket starts with `ls -l`, `id`, and
   `namei -l` evidence — diagnose *which triad* fails, then grant
   the narrowest bit to the narrowest subject.
