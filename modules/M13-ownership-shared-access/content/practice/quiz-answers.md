# Answer Key — Module 13 Quiz

Each answer also cites the lesson to revisit.

1. **Root only for chown; chgrp works for owners *toward a group they belong
   to*.** Changing *who* a file belongs to is a security decision; giving away
   your *own* membership-based group is not. (L1 §2)
2. **UPG.** Ubuntu's `USERGROUPS_ENAB yes` makes the private group primary;
   mode `0022` then keeps group/world at `-`, so the team group only grants
   what a default ACL or setgid setup adds. (L1 §1, 2)
3. **`2`=setgid**, owner `7`=rwx, group `7`=rwx, other `0` — team rwx, others
   nothing, and everything new inside lands in `labteam`. (L2 §2)
4. **New files inherit the directory's group** (UPG/setgid). It does **not**
   make members of the old group lose access or add anyone — `getfacl` after
   `chgrp` shows why rights can change while bits look the same. (L1 §1)
5. **Sticky bit** (`+t`, mode `1xxx`). Ubuntu ships it on `/tmp` and
   `/var/tmp`. (L2 §3)
6. **Read and write yes; delete no** — sticky removes `w`'s delete power on
   others' files. Deliverables, not drafts. (L2 §3)
7. **Decay:** without setgid, files arrive group-`alice`; without default
   ACLs / umask discipline, they arrive group-blind. Fixing the *directory*
   is cheaper than chasing files forever. (L2 §4)
8. **An access ACL exists** on that file/dir — `getfacl` to inspect.
   (L2 §1)
9. **The mask** caps named users/groups and owning group (`@mask` in `ls -l`
   comments). Effective rights = entry ∩ mask. (L2 §1)
10. **Farid loses effective access** (unless `o` still grants it): the
    `chmod` rewrites the mask to `rwx` minus... precisely, to the union
    without `r`. The `#effective` marker on `u:farid` shows it. Fix:
    `setfacl -m m::rx`. (L2 §1)
11. **Default ACLs are directory-only**; they stamp mode bits onto newborn
    files/dirs (request ∩ default, mask-included). (L2 §1)
12. **Run with the file owner's (root's) identity.** `passwd`, `sudo`.
    (L3 §3)
13. **Attack surface / provenance:** SUID-root code must be flawless;
    privilege is borrowed from ownership, so a compromised binary escalates
    its *runner*. Never craft your own. (L3 §3)
14. **`-4000`** SUID; **`-2000`** SGID; **`-1000`** sticky (no errors, 2>/dev/null).
    (L3 §3)
15. **Minimum access to do the job.** Data Science students: read on
    datasets, write only in their own experiment dirs — never both on the
    same tree without reason. (L3 §5)
16. **Traversal dies at `/srv/lab`** for non-`alice` users; `d` and deeper
    are unreachable for others (team members can, if their ACLs/grants hold
    on `d`/file). (L3 §4)
17. **Groups:** `proj-staff` (rw), `proj-students` (r). Root: `2770`,
    default ACL `d:g:proj-staff:rwx,d:g:proj-students:r-x`. One reviewer:
    `setfacl -m u:reviewer:rx` on `SUBDIR` (+ default mirror if they need to
    see future files there). (L3 §2, 4)
18. **`2770 group:mlserve`**, trainer in `mlserve`; serving layer gets read
    via group `r` if bits are `2640` on files... practically: keep `2770` on
    dir, rely on umask `0027`-style defaults or a default ACL
    `d:g:mlserve:rx` so the server can read checkpoints. (L3 §4; M29 next)
19. **Reason 1:** least privilege — people change roles, so file grants lag.
    **Reason 2:** hygiene — `ls -l`/audits show intent, not a pile of
    user-ACLs; removal is one `gpasswd -d`. (L3 §2)
20. **setgid + default ACLs (a "constitutional" tree).** Newborns are born
    shared; humans stop hand-chmod'ing. (L2 §4)
