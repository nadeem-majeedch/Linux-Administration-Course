# Answer Key — Module 14 Quiz

Each answer cites the lesson to revisit.

1. **UID 0.** The kernel exempts UID 0 from permission checks. (L1 §1)
2. **Because humans can't be trusted to be careful — by design.** A locked
   root forces *deliberate, per-command, logged* elevation via sudo; a
   root password invites whole-session root shells with no audit trail.
   (L1 §1)
3. **No valid password hash** — password login for root is disabled.
   (L1 §1)
4. `su -` requires **root's password** and hands over a full root session
   (one secret, many actions, per-session). `sudo -i` requires **your own**
   password plus a policy match, and each subsequent command is still
   individually logged. (L1 §2, 3)
5. who=`wheel` group; from-host=`ALL`; as-who=`(ALL:ALL)` any user, any
   group; command=`ALL`. (L1 §4)
6. **A group** (vs a bare username). (L1 §4)
7. **Journald = fast local query; auth.log = the canonical audit file
   sysadmins/export/SIEM collect.** Two views, one event; on shared servers
   the audit trail is the point. (L1 §3, Lab 1 Part B)
8. **Any command, as any user and any group, from any host** — full
   administrator. (L1 §4)
9. **`sudo visudo -c`** — parses everything, edits nothing: it is a
   validator, never a writer, so it cannot itself corrupt a policy
   even on a machine whose sudoers is already broken. (L1 §4)
10. **Files with `.` or `~` in their names are ignored by the includedir**
    — so renaming `foo` → `foo.bak` (or `foo.old`) disables a rule without
    deleting it. (L1 §4, Lab 1 Part E)
11. ```text
    %sync ALL=(root) NOPASSWD: /usr/local/bin/mirror-datasets
    ```
    Risk: whatever that script can do, the group can now do unattended.
    Compensating controls: the script itself is root-owned and
    non-writable by the group (755), does one scoped thing, and every run
    lands in the sudo log. (L1 §4, Lab 1 Part D)
12. **The shell performs the redirection — opening `/etc/hosts` for
    writing — before sudo runs**, so the write is attempted with *your*
    credentials. Remedies: `sudo sh -c '...'` or `... | sudo tee -a`.
    (L1 §6)
13. **PATH-injection via sudo.** A hostile directory containing a fake
    `apt`/`ls`; without secure_path, sudo could resolve to the attacker's
    binary and hand it root. (L1 §4)
14. `env_reset` drops your environment — including proxy variables — from
    privileged commands. Behind a proxy, `sudo pip install` may fail to
    reach the network. The deliberate escape hatch: `sudo -E` (or finer,
    `env_keep` in sudoers). (L1 §4)
15. **Not really.** `apt` executes maintainer scripts (pre/postinst) as
    root and can install packages that themselves ship code — so granting
    "apt" is effectively granting arbitrary code execution. Scoping the
    *operation* (`apt update` only, via a wrapper script) is the honest
    fix. (L1 §5, Lab 2 Ticket B)
16. (a) `sudo` in a cron line with NOPASSWD. (b) A scoped drop-in running
    *one helper script* that reads the file and writes it where the
    pipeline's user can read it — or, better, fix the underlying perms with
    an ACL (`setfacl -m u:svc:rx`). (b): root is a means, not a design.
    (L1 §5)
17. Because root bypasses permissions rather than configuring them; a
    targeted grant (group membership or ACL) achieves the same access with
    a smaller blast radius and a cleaner audit story. (L1 §1, 5)
18. **journald** (and auth.log). One-liner:
    `journalctl _COMM=sudo --no-pager | tail`. (L1 §3)
