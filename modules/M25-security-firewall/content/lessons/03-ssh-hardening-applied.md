# Lesson 3 — SSH Hardening, Applied (with Rollback Discipline)

> Module 25 · Unit 6 · Difficulty: Advanced
> Reading time: ~25 min · Lab: [Lab 1 — hardening](../labs/lab-01-hardening.md)
> Up next: [Lesson 4 — services, updates & package security](04-services-updates-packages.md)

---

## 1. From reading to doing — with the safety net visible

[M22 Lesson 2](../../../M22-ssh-remote-admin/content/README.md) read
the four directives; this lesson makes you *apply* them to your own
VM — the course's one sanctioned moment of editing `sshd_config`
drop-ins. The lesson's real content, though, is the **discipline
around the edit**: backup, test, staged reload, second terminal,
rollback plan. That discipline transfers to every production change
you'll ever make — config files, firewall rules, deployment
manifests — which is why the lab grades the process, not the
outcome.

## 2. The target posture

End state on the lab VM:

```sshconfig
# /etc/ssh/sshd_config.d/10-hardening.conf
PasswordAuthentication no      # keys only — the brute-force door closes
PermitRootLogin no             # root is unreachable over SSH; sudo is the path
AllowGroups ssh-users          # explicit allowlist of who may even try
```

Each line's justification was argued in
[M22](../../../M22-ssh-remote-admin/content/README.md); here, the
addition is the *verification*: every hardening claim gets a
before/after command pair in your log. Unverified hardening is a
guess with better handwriting.

## 3. The prerequisites — checked, not assumed

Before touching sshd, confirm in this order:

1. **Key login works** — from a *second* terminal, freshly:
   `ssh vm 'echo key-auth-ok'` must succeed without password. (The
   M22 lab's end-state, now a gate.)
2. **The group exists and you're in it** —
   `sudo groupadd -f ssh-users && sudo usermod -aG ssh-users $USER`
   (M12's groupadd/usermod, deployed for a reason), then verify:
   `groups` — after re-login, since group membership refreshes at
   session start. **This is the step that saves you:** with
   `AllowGroups` set, membership *is* your access.
3. **A console escape hatch exists** — the VM window itself (not
   over SSH) can reach a root shell via recovery. The escape hatch
   you never use but always name in the rollback plan.

## 4. The change procedure — the five-beat config edit

The same dance for any critical config, rehearsed here on sshd:

```console
# 1. BACKUP — the rollback starts here
$ sudo cp /etc/ssh/sshd_config.d/10-hardening.conf{,.bak} 2>/dev/null || true
$ ls /etc/ssh/sshd_config.d/           # know exactly what's there

# 2. WRITE — into the drop-in, not the main file
$ sudo tee /etc/ssh/sshd_config.d/10-hardening.conf > /dev/null <<'EOF'
PasswordAuthentication no
PermitRootLogin no
AllowGroups ssh-users
EOF

# 3. TEST — the syntax gate, before any reload
$ sudo sshd -t && echo "config valid"

# 4. RELOAD — not restart: current sessions survive (M20's reload verb)
$ sudo systemctl reload ssh

# 5. VERIFY — from the SECOND terminal, before closing the first
$ ssh vm 'echo hardened-auth-ok'       # key path still works?
$ ssh -o PubkeyAuthentication=no vm    # should now FAIL with "Permission denied"
```

**The two-terminal rule**, stated once more because it's the
examination question: never close the session you're SSH'd in with
until a *new* session has proven the new config admits you. If step
5 fails, the first terminal is your workshop for rollback
(`sudo mv .../10-hardening.conf{.bak,} && sudo systemctl reload ssh`)
— and the VM console is the fallback. Every production SSH-lockout
story begins with someone skipping this paragraph.

## 5. Verifying each directive — evidence pairs

| Directive | Before | After (expected) |
|---|---|---|
| `PasswordAuthentication no` | `ssh -o PubkeyAuthentication=no vm` → password prompt offered | → `Permission denied (publickey)` — password no longer an option at all |
| `PermitRootLogin no` | `ssh root@vm` → password prompt | → `Permission denied` *immediately* (even with a key — the account is closed) |
| `AllowGroups ssh-users` | any user could attempt SSH | a non-member (`su - labuser` inside VM, then ssh localhost) → denied before auth completes |

Each row's *after* command goes in `hardening.md` (Lab 1's
artifact) with its real output. Bonus evidence: the auth.log line
(M24) recording the failed attempts — your hardened server is
already logging its own defense.

## 6. Rollback — rehearsed, not written

The rollback plan is one paragraph *plus one rehearsal*:

> *If SSH access is lost: use the VM console (host window) → log in
> locally → `sudo mv /etc/ssh/sshd_config.d/10-hardening.conf{.bak,}`
> or `sudo rm` the drop-in → `sudo systemctl reload ssh` → verify
> with `sudo sshd -G <user> 2>/dev/null | grep -iE 'password|root'`
> or a client attempt. Alternative off-switch: `sudo ufw disable` if
> the network layer is the suspect.*

Lab 1 makes you perform a deliberate rollback (disable the
hardening, confirm the old posture returns, re-apply) — because a
rollback you've never run is a plan you don't have. The M17
test-restore doctrine, applied to configuration.

## 7. Beyond the three lines — the extended checklist

Additional sshd hardening, each with its trade-off (adopt on real
servers, know the cost):

- **`limit OpenSSH` via ufw** (Lesson 2) or **fail2ban** (Lesson 6)
  — throttle/lock brute-force sources. Trade-off: you can throttle
  yourself while testing (known ufw behavior: 6 conns/30s/IP).
- **Source-restrict SSH** (`ufw allow from <subnet>`) — campus-only
  SSH on real clusters. Trade-off: you need the right subnet list.
- **`MaxAuthTries 3`**, **`LoginGraceTime 30`** — small sharpening
  of defaults. Trade-off: minimal.
- **Per-user keys, no shared accounts** — attribution stays intact
  (M24's auth.log reads *names*). Trade-off: none. Never do shared
  accounts.
- **Change the port?** Security theater mostly (bots scan all
  ports) — but it *does* cut log noise dramatically. Optional,
  honest about its value.

What's deliberately out of scope: port-knocking, disabling
`PubkeyAuthentication`, anything that trades auditability for
obscurity. Hardening that makes the system *harder to administer*
without making it *harder to attack* is entropy, not security.

## 8. Try it now (10 minutes, read-only)

1. `sudo sshd -G $USER | grep -iE 'passwordauthentication|permitrootlogin|allowgroups'`
   — print your *effective* sshd posture as applied to your user.
   (`sshd -G` is to sshd_config what `ssh -G` is to client config.)
2. Which drop-ins exist? `ls /etc/ssh/sshd_config.d/` — Ubuntu ships
   `50-cloud-init.conf` (often setting `PasswordAuthentication yes`
   on cloud images!). Note *precedence*: lexicographically later
   files win for a directive — your `10-` prefix vs their `50-`?
   Check before assuming your line wins. (This ordering trap is
   Lab 1's subtlety.)
3. Write your rollback paragraph *before* the lab — one sentence
   naming the console path, the file to remove, the reload command.
4. `last -5` and `sudo grep -c "Failed password" /var/log/auth.log`
   — a baseline of who's been knocking. (On a NAT VM: probably zero.
   On a real public server: thousands. The difference is exposure —
   M21's bind-scope, seen in logs.)

## 9. Common mistakes

- Editing `/etc/ssh/sshd_config` directly instead of a drop-in —
  upgrades and future admins lose the thread.
- Skipping `sshd -t` — a typo'd config + `restart` = no SSH at all.
- `restart` when `reload` suffices — you killed your own session to
  apply a change the reload would have applied safely.
- Forgetting the group-membership refresh (re-login) — `AllowGroups`
  then locks out the very user it was meant to allow.
- Dropping the `.bak` file in a world-readable location — your
  rollback artifact now leaks the *old* posture; keep it root-owned
  in place.

> **Up next:** [Lesson 4 — services, updates & package
> security](04-services-updates-packages.md): shrinking what listens,
> and keeping what stays patched.
