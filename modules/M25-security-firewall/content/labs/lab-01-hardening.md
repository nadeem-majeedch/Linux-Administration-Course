# Lab 1 — The Hardening Lab: Open to Hardened, Documented, Reversible

> Module 25 · Unit 6 · Difficulty: Advanced
> Time: ~75 min · Environment: your own VM
> Prerequisites: [M22 Lab 1](../../../M22-ssh-remote-admin/content/labs/lab-01-key-workflow.md)
> working (key login); all six M25 lessons
> ⚠️ **Defense only.** Every change is on your VM, every change has a
> rollback, and the rubric is [the checklist](../hardening-checklist.md)
> used as a worksheet. The two-terminal rule is in force from Phase 3
> to the end.

Take your VM from course-default to hardened — one documented pass,
each phase verified before the next. The artifact you build
(`hardening.md`) is a template for every real hardening you'll do
in a career.

## Phase 0 — snapshot (5 min)

Take a VM checkpoint/snapshot (VirtualBox: *Machine → Take
Snapshot*; the rollback of last resort). Record its name. Everything
else this lab does is reversible *within* the session; the snapshot
reverses the whole lab.

## Phase 1 — baseline audit (15 min)

Record the *before* state in `hardening.md` — each with real output:

```console
$ ss -tulpn                                    # every listening door
$ sudo systemctl list-unit-files --state=enabled | head -20
$ sudo ufw status verbose                      # firewall posture (likely inactive)
$ sudo sshd -G $USER | grep -iE 'passwordauthentication|permitrootlogin'
$ apt list --upgradable 2>/dev/null | wc -l    # patch debt
$ groups                                       # your memberships
```

Then the audit table (Lesson 4's rubric): *service / bound to /
needed? / action* — one row per listening line. The baseline is the
evidence that hardening *changed* something.

## Phase 2 — patch the debt (10 min)

```console
$ sudo apt update && sudo apt upgrade          # apply what's pending
$ sudo apt install unattended-upgrades         # if absent
$ systemctl status apt-daily-upgrade.timer     # verify the auto-security timer
```

Record: packages upgraded count, timer state. (Reboot if
`/var/run/reboot-required` exists — do it *after* Phase 5's ssh
work so the session survives; note it in the log if deferred.)

## Phase 3 — firewall: default-deny with explicit allows (15 min)

The Lesson 2 choreography, in order:

```console
$ sudo ufw default deny incoming
$ sudo ufw allow OpenSSH                       # BEFORE enable — never lock out
$ sudo ufw --dry-run allow OpenSSH >/dev/null  # (optional) read what would be written
$ sudo ufw enable
$ sudo ufw status verbose                      # the verification pair
```

**Verify from a second terminal before closing the first:**
`ssh vm 'echo fw-ok'` (via the M22 alias). If the second terminal
can't get in: `sudo ufw disable` from the first — the rollback is
one command, and you *rehearse* it in Phase 6.

Add the lab service rule (from M22's tunnel exercise, now
network-legal): `sudo ufw allow 8888/tcp comment 'lab compute'` —
then the *scoping refinement*: replace it with
`sudo ufw allow from 10.0.2.0/24 to any port 8888` (your host-only
subnet — check with `ip route` on the host) and note the difference
in your log. Source-scoped rules are the craft.

## Phase 4 — SSH hardening (20 min)

Prerequisites gate (from Lesson 3): key login confirmed from a
second terminal; group created and *membership refreshed*:

```console
$ sudo groupadd -f ssh-users
$ sudo usermod -aG ssh-users $USER
$ exit          # re-login for group refresh — then verify:
$ groups        # ssh-users present?
```

The change (Lesson 3's five beats — backup, write drop-in, test,
reload, verify):

```console
$ sudo cp -n /etc/ssh/sshd_config.d/10-hardening.conf{,.bak} 2>/dev/null || true
$ sudo tee /etc/ssh/sshd_config.d/10-hardening.conf > /dev/null <<'EOF'
PasswordAuthentication no
PermitRootLogin no
AllowGroups ssh-users
EOF
$ sudo sshd -t && echo valid
$ sudo systemctl reload ssh
```

**The verification trio — from the second terminal, before closing
the first:**

```console
$ ssh vm 'echo key-auth-still-works'                    # key path: must succeed
$ ssh -o PubkeyAuthentication=no vm                      # password path: must FAIL (publickey)
$ ssh root@vm                                            # root: must FAIL outright
```

Precedence check (Lesson 3's trap): `ls /etc/ssh/sshd_config.d/` —
if a `50-cloud-init.conf` (or similar) sets `PasswordAuthentication
yes`, it *wins* over your `10-` file. Fix by renaming yours to
`99-hardening.conf` (later file wins) or removing the shadowing
line; re-run `sshd -t && reload` and the trio. Record which you did
— this subtlety is the lab's hidden lesson.

## Phase 5 — service audit closes (10 min)

From Phase 1's table: act on every "not needed" row. Typical on a
lab VM: nothing listens beyond sshd + your lab services — which is
*itself* the finding (Ubuntu's surface is small). If cups or
anything else listens and is unneeded:
`sudo systemctl disable --now <svc>` and record the reasoning. Then
the post-audit: `ss -tulpn` again — the *after* table, beside the
baseline.

## Phase 6 — rollback rehearsal (10 min)

The discipline that makes the rest safe. Rehearse *both* rollback
layers:

1. **Config rollback:** `sudo mv
   /etc/ssh/sshd_config.d/10-hardening.conf{,.disabled} && sudo
   systemctl reload ssh` → verify the old posture returns
   (`sshd -G` shows passwords accepted) → then **re-apply** (restore
   name, `sshd -t`, reload, verify the trio again). You've now run
   the rollback once, calmly, by choice.
2. **Network rollback:** `sudo ufw disable` → `ssh vm 'echo
   no-fw-ok'` → `sudo ufw enable` → verify again. Same muscle.

Record both rehearsals. A rollback performed is a rollback believed.

## Done when (`hardening.md` is the deliverable)

- [ ] Baseline + post tables (before/after `ss`, ufw, sshd -G,
      patch counts)
- [ ] The verification trio's real outputs (from a second terminal)
- [ ] The precedence issue found and resolved (or explicitly noted
      as absent)
- [ ] Both rollback rehearsals logged
- [ ] The [checklist](../hardening-checklist.md) filled in as the
      closing summary — every box checked or an explicit
      "N/A + why"
- [ ] Snapshot retained until the module's quiz is done
