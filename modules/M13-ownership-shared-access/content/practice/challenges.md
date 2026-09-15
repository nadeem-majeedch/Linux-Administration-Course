# Challenge Problems — Module 13

Do these after the quiz. Report each in `lab-log.md` like a mini-incident.

- [ ] **C1 — one-liner verdicts.** For each, state what changed and whether
  it was enough:
  a) `chmod 770 data/` on a decayed tree.
  b) `chgrp -R labteam data/` only.
  c) `setfacl -R -m g::rwX,d:g::rwX data/` (upper-case X) only.
  d) All three, in the order a→b→c.
- [ ] **C2 — the reviewer clause.** Rework Lab 2's tree so `reviewer` gets
  `r-x` on `projects/spam/` *and* on files created there **after today**,
  without adding them to any team group. Verify with a probe.
- [ ] **C3 — least-privilege audit.** Write `audit.sh`: walks a given tree
  and prints any path where *other* has more than read (`---`). Bonus: also
  flag world-writable dirs lacking sticky. Run on `/tmp/lab-tree`.
- [ ] **C4 — mask mechanics.** Create the L1 §4 file; `setfacl -m m::--- f.txt`;
  verify Alice still edits (owner escapes the mask). Then `setfacl -m m::rwX`
  and show `#effective` disappearing. Write 3 sentences on why.
- [ ] **C5 — SUID inventory.** `find / -xdev -perm -4000 2>/dev/null` on your
  VM. Pick two binaries, `ls -l` them, and explain *why* each legitimately
  holds the bit (man page). One paragraph.
- [ ] **C6 — sticky experiment.** Build `inbox` (`3770`, two test users).
  As user A: touch + chmod 600 a file. As user B: try overwrite, append,
  delete, rename A's file; try on *your own* file. Tabulate: sticky blocks
  which, not which — and why that's the *right* set.
- [ ] **C7 — the constitutional tree, generalized.** Extend Lab 1's Lab 2
  tree: a new `public/` (world-readable, group-writable, sticky) inside the
  team root — the "we publish, but nobody unpublishes each other" corner.
  Every mode/default-ACL decision justified in comments.
- [ ] **C8 — decode-acls.** `getfacl -p /tmp /usr/bin/sudo` — explain the
  `other::r-x` on sudo's *directory* vs the SUID mode on the binary; why
  world-execute on the dir is required for the SUID trick to be usable.
- [ ] **C9 — break-fix acls.** Have a partner (or your other user) set:
  named user ACL + mask `rwx`, then run `chmod 700`. Write the one-liner
  that restores effective rights *without* re-granting: `setfacl -m m::rwx`.
  Explain the interplay.
- [ ] **C10 — capstone seed.** Create `/srv/capstone/{data,models,reports}`
  with: data = `2770` + default ACLs (team rw, students rx), models =
  `2770` mlserve-ready, reports = `2771`... — wait, that's *execute-without-
  read* for others: justify or reject that choice in one paragraph (hint:
  `771` + sticky? Compare). Deliverable: `capstone-perms.md` + the
  `setfacl`/`chmod` script.

C1 in the wild: production trees decay the *day* a new person joins —
C4/C9 turn "mask is magic" into "mask is a gate I can reset."
