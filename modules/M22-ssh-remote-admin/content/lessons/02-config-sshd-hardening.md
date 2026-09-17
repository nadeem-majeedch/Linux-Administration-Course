# Lesson 2 — ssh_config, sshd_config and the Hardening Mindset

> Module 22 · Unit 6 · Difficulty: Advanced
> Reading time: ~25 min · Up next: [Lesson 3 — remote execution & tunnels](03-remote-execution-tunnels.md)

---

## 1. Two config files, two sides of the connection

SSH has a **client** side and a **server** side, each configured by a
file the other never sees:

| File | Whose | What it decides |
|---|---|---|
| `~/.ssh/config` | *your* ssh client | which key, which user, which name for **each host you connect to** |
| `/etc/ssh/sshd_config` | the **server** (sshd) | who may log in, how, and what they may do |

The client config is yours to write freely (this lesson's first half).
The server config requires root and admin judgment — the course has
you *read and analyze* it now, and *apply* hardening in
[M25](../../../M25-security-firewall/README.md), once firewalls complete
the picture.

## 2. ssh_config — the client config that makes you fast

Every lab command so far spelled out everything:

```console
$ ssh -i ~/.ssh/lab_vm -p 2222 ds@localhost
```

The client config gives names to that ceremony. `~/.ssh/config`
(600, owned by you — same rules as keys):

```sshconfig
# ~/.ssh/config — client-side, per-host settings

Host vm                      # the alias you type
    HostName localhost       # the real address
    User ds                  # the login user
    Port 2222                # VM's forwarded port (Lab 1 sets this up)
    IdentityFile ~/.ssh/lab_vm
    IdentitiesOnly yes       # offer ONLY this key — no agent spray

Host *
    ServerAliveInterval 60   # keep long sessions alive behind NAT
    ServerAliveCountMax 3
    AddKeysToAgent yes       # use-once keys join the agent automatically
```

The alias changes the daily command to `ssh vm` — and, critically,
**every other tool that uses SSH honors it too**: `scp ... vm:~/`,
`rsync ... vm:`, `git clone git@vm:repo.git`, file managers, IDE
remotes. You configure once; the whole toolchain inherits.

**Precedence:** command-line flags beat `~/.ssh/config` beats the
system-wide `/etc/ssh/ssh_config`. First-obtained value wins, so a
`Host vm` block overrides the `Host *` defaults — hence the
convention: specific blocks on top, wildcard defaults at the bottom.

### Host blocks, patterns, and ProxyJump

`Host` lines take patterns, and blocks stack — later *matching*
blocks fill in values the earlier ones didn't set:

```sshconfig
Host gpu*                    # gpu01, gpu02, ...
    ProxyJump jump           # reach them THROUGH the bastion below
    User ds

Host jump
    HostName bastion.university.edu
    User ds
    IdentityFile ~/.ssh/lab_vm

Host vm
    HostName localhost
    Port 2222
    User ds
    IdentityFile ~/.ssh/lab_vm
    IdentitiesOnly yes
```

`ssh gpu01` now connects **via** `jump` automatically — the
ProxyJump pattern that models every university cluster: a bastion
faces the internet; the compute nodes face the bastion. One config
line replaces the port-forwarding acrobatics that used to be the
manual alternative.

`ssh -G vm` prints the *effective* configuration for an alias — the
diagnostic command for "why is it using that key/port?" (Lab 2,
patient #4).

## 3. sshd_config — reading the server's rulebook

On the *server*, `/etc/ssh/sshd_config` (root-owned, 600) decides
who gets in. Read yours:

```console
$ grep -Ev '^\s*(#|$)' /etc/ssh/sshd_config
Include /etc/ssh/sshd_config.d/*.conf
```

Modern Ubuntu keeps defaults in `/usr/share/doc/openssh-server/` and
ships **drop-ins** — `/etc/ssh/sshd_config.d/*.conf` (the
`Include` line) — where admins layer settings without editing the
main file. Same pattern as sudoers drop-ins from
[M14](../../../M14-sudo-root-principle/content/README.md): main file
pristine, intent in reviewed drop-ins.

The four directives that define the security posture:

| Directive | Values | Meaning |
|---|---|---|
| `PasswordAuthentication` | yes/no | are passwords accepted *at all*? |
| `PubkeyAuthentication` | yes (default) | are keys accepted? |
| `PermitRootLogin` | yes / no / prohibit-password | may anyone log in **as root** over SSH? |
| `AllowUsers` / `AllowGroups` | names | whitelist of accounts allowed to SSH in |

Ubuntu's defaults: passwords yes, keys yes, root `prohibit-password`
(root may enter with a key but never a password). After your Lab 1
key works, the end-state hardening is three lines in a drop-in:

```sshconfig
# /etc/ssh/sshd_config.d/10-hardening.conf  (M25 applies this — shown, not done)
PasswordAuthentication no
PermitRootLogin no
AllowGroups ssh-users
```

**Why each line is what it is:**

- `PasswordAuthentication no` — with keys working for every real
  user, passwords only exist for attackers to brute-force. This is
  the single highest-value line in remote-Linux security. The
  *order of operations* is the safety rule: **verify key login from
  a second terminal before** applying, and keep a console
  (VM window) open — the escape hatch that makes this reversible.
- `PermitRootLogin no` — root is the account every brute-force
  script tries by name ([M14's](../../../M14-sudo-root-principle/content/README.md)
  least-privilege principle applied to the network edge: log in as
  yourself, `sudo` for privilege, audit trail included).
- `AllowGroups ssh-users` — an explicit allowlist: accounts that
  don't need SSH (service accounts, data users) can't be targeted
  with it ([M12/M13's](../../../M12-users-groups-permissions/README.md)
  group thinking, reused).

Changes require `sudo systemctl reload ssh` (a *reload* applies
config without dropping existing sessions — [M20's](../../../M20-systemd-services/content/README.md)
`reload` verb earning its keep) and `sshd -t` (config syntax check)
before it — the discipline: **test config, then reload, with a
second session open.**

## 4. Password vs key — the attacker's view

Why keys win, quantified:

- **Passwords over SSH** face unbounded online guessing — automated
  bots sweep every public 22/TCP continuously (read a fresh server's
  `/var/log/auth.log` for a day — [M24](../../../M24-logs-journald-monitoring/content/README.md)
  shows the storm). Weak password = days; strong-but-typed = friction
  every single login, so humans weaken them.
- **ed25519 keys** face a keyspace no online guessing can traverse;
  the attack shifts from *guessing* to *stealing the file* — which
  the passphrase, the 600, and the never-leaves-the-laptop rules
  (Lesson 1 §7) address.

The residual risks of keys are real but *local*: a copied unencrypted
key, an agent you left unlocked on a shared machine, a key committed
to a repo. All three are file- and habit-problems — which is why this
module's labs grade permission bits and `.gitignore` hygiene, not
just connectivity.

**fail2ban awareness** (one paragraph, no labs): on real servers,
`fail2ban` watches auth logs and firewalls repeat offenders
automatically — the log-monitoring of
[M24](../../../M24-logs-journald-monitoring/content/README.md) wired to
[M25's](../../../M25-security-firewall/README.md) firewall. Know it
exists; meet it properly in M25.

## 5. Least privilege, the SSH edition

The hardening directives are one expression of a broader rule the
course has been building since M12:

- **Named accounts, not shared ones** — every action in auth.log
  must attribute to a person (who logged in, who sudo'd).
- **Minimal SSH exposure** — `AllowGroups` limits who can even
  *try*; the M25 firewall limits *from where*.
- **Minimal privilege after login** — sudo (M14), not root shells;
  user services (M20) for personal work.
- **Minimal trust in the other direction** — `IdentitiesOnly yes`
  stops your client offering keys the server shouldn't see;
  host-key verification stops impostors. Trust is configured, not
  assumed.

## 6. Try it now (15 minutes)

1. Write the `Host vm` block from §2 (after Lab 1 gives the key a
   working target). `ssh vm` — then `ssh -G vm | grep -E
   'hostname|user|identityfile'` to see what the client *resolved*.
2. `grep -Ev '^\s*(#|$)' /etc/ssh/sshd_config` and list your
   server's `sshd_config.d/` — which of the §3 directives does your
   VM currently set, explicitly or by default?
3. Config translation: express `ssh -i ~/.ssh/lab_vm ds@localhost`
   as a Host block — then express the block back as a command
   (`ssh -G` is the grader).
4. Read one real `auth.log` line from your VM
   (`sudo tail -5 /var/log/auth.log | grep sshd`) — find the
   `Accepted publickey` line and identify which key logged in.

## 7. Common mistakes

- `~/.ssh/config` with wrong permissions (must be 600/700 — ssh
  ignores or warns otherwise).
- `Host *` blocks placed *above* specific ones, silently winning
  first-match.
- Applying `PasswordAuthentication no` with only one terminal open —
  and no console. The two-session rule is not optional.
- `reload` vs `restart` confusion — reload re-reads config without
  killing your session; either way, `sshd -t` first.
- Editing the main `sshd_config` when a drop-in was the right tool —
  upgrades overwrite; drop-ins persist.

> **Up next:** [Lesson 3 — remote execution &
> tunnels](03-remote-execution-tunnels.md): commands and files across
> the wire, and ports that appear where you need them.
