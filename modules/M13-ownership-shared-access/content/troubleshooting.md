# Troubleshooting — Module 13

Format: symptom → likely cause → check → fix → prevention. Practice in
`lab-02-permission-clinic.md` uses these; resist looking until stuck.

## 1. "Directory deleted!" — the sticky-bit case

- **Symptom:** In `/tmp/scratch` (world-writable), a classmate deleted your
  `results.csv`.
- **Likely cause:** No sticky bit: `drwxrwxrwx` instead of `drwxrwxrwt`.
- **Check:** `ls -ld /tmp/scratch`
- **Fix:** `sudo chmod +t /tmp/scratch`
- **Prevention:** Every shared writable directory gets `1` in front of its
  mode (see [Lesson 2](lessons/02-acls-permission-clinic.md#6-sticky-bit-shared-but-safe)).

## 2. New files aren't shared with the group

- **Symptom:** You create files in a team directory; teammates can't edit
  them.
- **Likely cause:** Missing setgid bit → no group inheritance; private group
  is primary (Ubuntu default).
- **Check:** `ls -ld` — is there an `s` in the group's execute slot? Does the
  directory even *have* the right group (`ls -ldg`)?
- **Fix:** `sudo chgrp labteam DIR && sudo chmod 2770 DIR`
- **Prevention:** Default ACLs: `sudo setfacl -d -m g::rwx,o::--- DIR`
  ([Lesson 2, the constitutional tree](lessons/02-acls-permission-clinic.md#4-default-acls-newborns-scripted)).

## 3. Permission denied on a file that "looks fine"

- **Symptom:** `cat: /srv/lab/data/d.csv: Permission denied` but
  `ls -l` shows group `r--` and you're in the group.
- **Likely cause:** A *parent directory* lacks `x` for you — the file was
  never the problem.
- **Check:** `namei -l /srv/lab/data/d.csv` — walk from `/` down; the first
  non-traversable entry is your culprit.
- **Fix:** Grant `x` on the *chain*, not the file:
  `sudo setfacl -m u:YOURUSER:x /srv/lab /srv/lab/data`
  (least privilege: `x` only, not `r`, if they shouldn't list contents).
- **Prevention:** `namei -l` before `chmod` roulette. This is Lab 2 §A.

## 4. Someone else's ACL got wiped

- **Symptom:** After `chmod 770 shared/`, teammate's named-user ACL stopped
  working.
- **Likely cause:** `chmod` recomputes the ACL **mask** and can clamp
  named entries.
- **Check:** `getfacl shared/` — is `mask::` narrower than
  `group:TEAM::` or a named user?
- **Fix:** `setfacl -m m::rwx shared/`
- **Prevention:** Change access with `setfacl` when ACLs are in play;
  treat `chmod` on an ACL-bearing file as a mask edit.
  ([Lesson 2, mask](lessons/02-acls-permission-clinic.md#2-reading-acls-getfacl))

## 5. `chown: changing ownership: Operation not permitted`

- **Symptom:** As a normal user, you can't give your file to someone else.
- **Likely cause:** Only root changes file *ownership* — by design (quota and
  audit integrity).
- **Check:** `id` — are you root? (If yes, different problem.)
- **Fix:** `sudo chown ...` — or `chgrp` instead (owners may give files to a
  group they belong to — no sudo needed).
- **Prevention:** Know which operation is an ownership change vs a group
  change ([Lesson 1](lessons/01-ownership-chown-shared-dirs.md#2-chown-chgrp-moving-ownership)).

## 6. ACLs exist but group members still can't write

- **Symptom:** `getfacl` shows `group:labteam:rwx`, yet writes fail.
- **Likely cause:** Mask is narrower than the entry.
- **Check:** `getfacl` — `#effective` suffix on entries.
- **Fix:** `setfacl -m m::rwx FILE`
- **Prevention:** After any `chmod`, re-read `getfacl` before declaring
  victory ([Lesson 2, mask](lessons/02-acls-permission-clinic.md#2-reading-acls-getfacl)).

## 7. `setfacl: Option -m: Invalid argument near character ...`

- **Symptom:** The `setfacl` command fails immediately.
- **Likely cause:** Syntax: entries are `u:user:perm`, `g:group:perm`,
  `m::perm` — and perms are `rwx` letters or octal, with `X` (capital)
  meaning execute-if-any-directory-or-already-x. Also: `setfacl` needs
  write permission on the file — use `sudo` when it's not yours.
- **Check:** Re-read your command against
  [Lesson 2's syntax table](lessons/02-acls-permission-clinic.md#3-writing-acls-setfacl).
- **Fix:** Correct entry spelling; add `sudo` for non-owned files.
- **Prevention:** `setfacl` completions exist; lean on `man setfacl` §EXAMPLES.

## 8. Shared project on NFS: SGID not inherited

- **Symptom:** Same commands as Lesson 2, but group inheritance silently
  fails on a mounted network share.
- **Likely cause:** The NFS server/export doesn't honor setgid inheritance or
  squashes root (e.g., `root_squash`), or the mount lacks the needed
  semantics.
- **Check:** Create a test file in the mount; `ls -l` its group. If it's your
  private group → inheritance is off. `mount | grep <share>` to see options.
- **Fix:** Escalate to the sysadmin (this is exactly the
  [Lab 2 §C ticket](labs/lab-02-permission-clinic.md)) — often the export needs
  re-mounting or an ACL-capable filesystem.
- **Prevention:** Default ACLs *sometimes* survive NFSv4 where SGID doesn't —
  test both on your actual share before committing to a design
  ([Lesson 2](lessons/02-acls-permission-clinic.md#1-where-groups-run-out)).

## 9. `getfacl` shows exactly the mode bits — "where did my ACL go?"

- **Symptom:** You expected named entries but see only `user/group/other`.
- **Likely cause:** Wrong file; or entries were removed (`setfacl -b`
  somewhere in history); or you're reading the *default* section of a
  directory and expecting it to grant anything — defaults don't grant access
  to the directory itself.
- **Check:** `getfacl -p /exact/path` (absolute, no symlink resolution
  confusion); compare `getfacl DIR` vs `getfacl DIR/newfile`.
- **Fix:** Re-grant the needed entries.
- **Prevention:** `ls -l` trailing `+` is your "ACL present" tripwire — get
  in the habit of noticing it.

## 10. umask vs default ACL fight

- **Symptom:** You set default ACLs, but files still arrive `640` — group
  read only.
- **Likely cause:** umask `0027` intersects the default ACL: newborn mode =
  open mode ∩ ¬umask. Your umask removed group `w` before ACLs could add it.
- **Check:** `umask` in the creating user's shell.
- **Fix:** Loosen umask (`0022` or `0002` for shared teams) — the default
  ACL then has room to grant.
- **Prevention:** Diagnose with the
  [Lab 2 §B playbook](labs/lab-02-permission-clinic.md) — this is its exact
  scenario.
