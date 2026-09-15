# Lesson 2 — ACLs, Special Bits & the Permission Clinic

> Module 13 · Unit 4 · Difficulty: Intermediate → Advanced
> Reading time: ~35 min · Lab: [Lab 2 — The Permission Clinic](../labs/lab-02-permission-clinic.md)
> Up next: [M14 — Sudo & the root principle](../../../M14-sudo-root-principle/content/lessons/01-root-sudo-sudoers.md)

---

## 1. Where groups run out

The 9-bit model has exactly **one** group per file. Real labs hit the wall fast:

> The dataset is group `lab`. A *external collaborator* needs read on exactly
> one subdirectory. Options: add them to `lab` (too much), create a nested
> group maze (fragile), or copy the data (drift). None is good.

**ACLs (Access Control Lists)** extend the model: per-file lists of extra
users and groups with their own modes. M12's Challenge C3 asked you to guess
at `+` in `ls -l` — that's the ACL marker.

## 2. Reading ACLs: getfacl

```console
$ getfacl /srv/lab/datasets/shared-metrics
# file: srv/lab/datasets/shared-metrics
# owner: alice
# group: labteam
user::rwx
user:farid:r-x              # ← the ACL entry: one specific extra user
group::rwx
group::---
mask::r-x
other::---
```

Read it as the 9-bit model **plus appendices**: `user::` (owner), `group::`
(owning group), `other::` — the classic three — then named entries
(`user:farid:`, `group:analysts:`) and the **mask**, the ceiling for all named
entries + owning group. `ls -l` shows it as a trailing `+`:

```console
$ ls -ld /srv/lab/datasets/shared-metrics
drwxrwx---+ 2 alice labteam 4096 ...        # the + says: ask getfacl
```

## 3. Writing ACLs: setfacl

```console
$ setfacl -m u:farid:r-x /srv/lab/datasets/shared-metrics   # -m = modify: grant
$ setfacl -m g:analysts:rx  /srv/lab/datasets/shared-metrics # a whole extra group
$ setfacl -x u:farid        /srv/lab/datasets/shared-metrics # -x = remove one entry
$ setfacl -b                /srv/lab/datasets/shared-metrics # -b = strip all ACLs
```

(`setfacl` for others' files needs sudo; for your own files it doesn't. Ubuntu
ships the `acl` userspace; the filesystem support is on by default for ext4.)

**The mask, demystified:** the *effective* rights of named entries (and the
owning group!) are their entry AND-ed with the mask. `setfacl` recalculates the
mask automatically on `-m`; it exists so bulk re-tightening (one chmod of the
mask) can throttle every named entry at once. When `getfacl` shows
`#effective:r--` next to an entry, the mask is the throttle.

## 4. Default ACLs: newborns, scripted

M13 Lesson 1's setgid fixed *group* inheritance; **default ACLs** fix the
*whole mode* of newborns — including granting specific users automatically:

```console
$ sudo setfacl -d -m u:farid:rx /srv/lab/datasets/shared-metrics
$ getfacl /srv/lab/datasets/shared-metrics | grep default
default:user::rwx
default:user:farid:r-x        # every future child inherits this grant
default:group::rwx
default:mask::rwx
default:other::---
```

Now any file/subdir created inside carries the grant *without anyone doing
anything* — the "pattern never decays" guarantee, expressed as metadata. Default
ACLs appear on directories only; files inherit *access* ACLs from them.

## 5. Special permission bits on *files*: SUID & SGID

M12's C3 guesses, graded. On executables:

| Bit | Symbolic | Effect |
|---|---|---|
| **SUID** | `u+s` (shows as `s` in owner-triplet) | the program runs with the **owner's** (usually root's) identity |
| **SGID** | `g+s` (group-triplet `s`) | runs with the **group's** identity; on *directories*: M13 L1's inheritance |

```console
$ ls -l /usr/bin/passwd /usr/bin/sudo
-rwsr-xr-x 1 root root 59976 ... /usr/bin/passwd
-rwsr-xr-x 1 root root 232416 ... /usr/bin/sudo
```

`passwd` must edit `/etc/shadow` (root-only, M12) yet users run it daily —
SUID-root *is* the mechanism: brief, audited, purpose-built elevation.
That's also the security lens: **every SUID-root binary is a potential
privilege path**, which is why servers audit them
(`find / -perm -4000 2>/dev/null` — try it in the VM) and why you *never*
`chmod u+s` anything yourself in this course.

## 6. Least privilege: the design principle that decides everything

Now that you own the whole toolbox (modes, groups, setgid, sticky, ACLs),
here's the rule that keeps deployments safe:

> **Grant the minimum access that lets the work happen — to roles (groups),
> not individuals — and nothing else.**

In practice, on shared DS servers:

- Students: read datasets, write their own spaces (`r-x` on data, `rwx` on
  their dirs) — *not* `sudo`, not staff groups.
- Service accounts (Jupyter, backup robot): own exactly their directories,
  nothing else, `nologin`.
- Staff: write where the work is, read everywhere below it.
- World (`o`): nothing, unless the contract *says* public (exports: `r-x`).
- Every exception: one ACL entry, documented, with an expiry note.

When an exception is granted per-person forever, access management decays;
when it's a *role with a definition*, it survives personnel churn. That's the
whole argument of Unit 4.

## 7. The Permission Clinic: diagnosis as a repeatable method

Labs 1–2 of this module are "clinics": broken setups you must repair. The
method (memorize the acronym — **I-G-A-T-E**):

1. **Identity** — `id`, `id USER`: who is acting, in which groups? (Fresh
   session? M12's relogin trap.)
2. **Group/mode of the path** — `namei -l /srv/lab/datasets/x.csv`: permissions
   of *every* component of the path at once. (The single most useful
   permission tool most people never learn.)
3. **ACL layer** — `getfacl` (a trailing `+` in `ls -l` demands it).
4. **Try as the victim** — `sudo -iu USER` then the actual failing command:
   evidence beats theory.
5. **Effect the minimal fix** — group bit? setgid? one ACL entry? Never
   `777` (M12's confession rule).

```
$ namei -l /srv/lab/datasets/shared-metrics/sales.csv
f: /srv/lab/datasets/shared-metrics/sales.csv
drwxr-xr-x root   root    /
drwxrwsr-x root   labteam srv          ← setgid visible in the path!
drwxrws--- alice  labteam datasets     ← ← the stall is HERE: bob has no x on this
drwxrwsr-x+ alice  labteam shared-metrics
-rw-rw-r-- bob    labteam sales.csv    ← file was never the problem
```

One `namei -l` read the entire path and located the stall two directories up —
the diagnosis that takes 40 minutes of guessing takes 40 seconds with the tool.

## Exercises (lab-log.md)

1. In the VM (users from Lab 1): grant `u:t-bob:r-x` on a subdirectory of the
   shared tree *without* adding him to the team group. Verify with `getfacl`
   and by acting as t-bob. Then remove the entry (`-x`) and re-verify.
2. Default-ACL lab: set `d:u:t-bob:rx` on a directory; create a file as
   t-alice; `getfacl` the newborn. Who granted what to whom, mechanically?
3. The mask in action: after a grant, `chmod g-rx` the directory — read
   `getfacl`'s `#effective` lines. Restore. Explain the mask in two sentences.
4. SUID census: `find / -perm -4000 -type f 2>/dev/null | wc -l` in your VM —
   how many SUID binaries? Pick three, `ls -l` them, and state in one line
   each why its designers elevated it.
5. `namei -l` your own home path end to end (`/home/you/projects/...`). Which
   components are world-traversable, and what does that say about home-dir
   privacy defaults (Ubuntu makes homes 750 — verify with `ls -ld /home/you`)?
6. ACL vs group: for the external-collaborator case in §1, argue both
   solutions (extra group vs ACL) in three lines each, then pick one with the
   least-privilege rule. What tips it? (Auditing? Expiry? Reuse?)
7. Clinic dry-run: a teammate reports "can't write to results/". Write the
   exact five I-G-A-T-E commands you'd run, in order, *before* proposing any
   fix.

## Check yourself before M14

- getfacl/setfacl: I can read a full ACL (including mask and `#effective`)
  and grant/revoke named entries.
- Default ACLs: I can make grants that survive every newborn file.
- SUID/SGID on files: I can explain the mechanism, name the canonical
  examples, and state why self-made SUID is forbidden.
- **I-G-A-T-E**: I can run the clinic method unaided — Lab 2 will grade that.

## Further reading (official sources)

- `man acl` (the POSIX ACL model), `man setfacl`, `man getfacl`, `man namei`
- Ubuntu Server docs: security — <https://documentation.ubuntu.com/server/how-to/security/>
- `man 8 find` (`-perm` for the SUID/SGID/sticky audits)

Next: [M14 Lesson 1 — Root, sudo & sudoers](../../../M14-sudo-root-principle/content/lessons/01-root-sudo-sudoers.md)
