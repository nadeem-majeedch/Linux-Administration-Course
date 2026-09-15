# Module 12 — Troubleshooting Guide

Identity and permission failures at this stage — diagnose, then act.

## 1. "Permission denied" — the universal starting triage

Run all four: `id` (who am I), `ls -ld DIR` (parent's mode), `ls -l FILE`
(file's mode), then apply the check-order rule (owner→group→other, first
match wins). Most "mysteries" die at step 2: the fault is on a *parent
directory* (missing `x`), not the file.

## 2. I'm in the group but still denied

Check-order stall: if you *own* the file, owner bits apply even when they're
worse than group bits. Or: the group bits really are `---`. Or (classic):
`chgrp` happened *after* your session started — group membership changes
apply to *new* login sessions; `newgrp <group>` re-negotiates without
re-login (try it; or log out/in).

## 3. My `usermod -aG` "didn't work"

It did — but your *current session* doesn't carry the new supplementary
group. `id` in a **fresh login shell** (or `newgrp`). The Lab-1 lesson:
memberships are read at session creation.

## 4. `userdel` refuses / leaves files behind

Refusal = the user's processes are running (`userdel -r` after they log out,
or `pkill -u` in your VM) or the account's primary group is in use. Leftover
mail spools/cron: `ls /var/mail`, `ls /var/spool/cron/crontabs` (VM) —
`userdel` is narrower than its reputation; audit leftovers deliberately.

## 5. `sudo: unable to resolve host` / `sudo` oddly slow

WSL2/VM classic: hostname changed but `/etc/hosts` didn't. Fix: add the new
hostname to `127.0.1.1` line (VM). Harmless but noisy; M15/M17 territory for
the underlying naming, noted here because it *surfaces* at sudo.

## 6. adduser vs useradd confusion (and the missing-home login)

`useradd` without `-m` = no home, wrong-ish shell: sessions land in `/` with
a bare prompt (M12 Challenge C5 rehearses the repair). Rule: `adduser`
interactively; `useradd -m -s /bin/bash` in scripts; verify with `getent
passwd USER` before first login.

## 7. Locked out of my own VM user's sudo

You removed your user from `sudo` (the `-a` incident) or botched a group
edit. Recovery ladder: (1) another admin account? (2) VM snapshot restore
(M01 Lab 4 — this is why it exists), (3) boot to recovery/root shell from the
GRUB menu (VM: hold Shift at boot; Ubuntu recovery → root shell). *Never*
experiment with your primary account's sudo membership; test with throwaways
(Lab 1's pattern).

## 8. Files created in shared dirs get the "wrong" group

New files take your *primary* group, not the directory's group — M13's
setgid/default-ACL machinery fixes this systematically. Until then: `chgrp`
after the fact, or set the directory's group and rely on M13's lesson.
(This is the #1 real-world "permissions keep breaking" complaint.)

## 9. `chmod -R` hit more than I meant

Scope damage control: `ls -lR` the affected tree, re-set modes by category
(600 dotfiles, 644 data, 755 scripts/dirs). Prevention wins: run `chmod -R`
with absolute paths (M07's rules), verify with `ls` first, snapshot before
(M01). If it hit *system* dirs (`/usr` etc.): stop, restore snapshot —
re-setting thousands of system modes by hand is a bad afternoon.

## 10. `sudo` prompts for a password I "didn't set"

It's *your* user's password (Ubuntu default), not a separate root password.
Root's password is intentionally locked (`grep ^root /etc/shadow` shows `!`
or `*`). `sudo -i` in the VM gives a root *shell* — Lesson 4 explains why
that's for short, deliberate sessions only.
