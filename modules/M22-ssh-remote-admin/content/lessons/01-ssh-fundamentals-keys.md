# Lesson 1 — SSH Fundamentals and Keys

> Module 22 · Unit 6 · Difficulty: Advanced
> Reading time: ~25 min · Lab: [Lab 1 — the key workflow](../labs/lab-01-key-workflow.md)
> Up next: [Lesson 2 — config & sshd hardening](02-config-sshd-hardening.md)

---

## 1. What SSH is

**SSH** (Secure Shell) is the encrypted protocol — and the `ssh`
command — that gives you a shell on a remote machine over a network.
It is *the* tool of Linux administration: every GPU server, cloud
instance, and shared dataset host in a DS career is reached this way.
Modern SSH (OpenSSH, which Ubuntu ships) provides three jobs at once:

1. **Remote shell** — an encrypted, authenticated terminal elsewhere.
2. **Command transport** — run one command remotely (`ssh vm 'df -h'`).
3. **Encrypted tunneling** — forward arbitrary TCP ports through the
   connection ([Lesson 3](03-remote-execution-tunnels.md)).

The architecture is client/server: your `ssh` is the client; the
remote machine runs **sshd** (the SSH daemon, an [M20](../../../M20-systemd-services/content/README.md)
system service listening on port 22/TCP by default — everything from
[M21](../../../M21-networking-fundamentals/content/README.md) applies:
ports, sockets, `ss -tlnp | grep :22`).

## 2. The first connection — host keys and the trust decision

```console
$ ssh ds@localhost
The authenticity of host 'localhost (::1)' can't be established.
ED25519 key fingerprint is SHA256:nThbg6kXUpJWGl7E1IGOCspRomTxdCARLviKw6E5SY8.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

That prompt is the **host key exchange** — SSH proving the server is
who it was last time, and asking you to record who it is the first
time. Saying yes stores the server's *public* host key in
`~/.ssh/known_hosts`; every later connection verifies the server's
key against that record. The trust model is **TOFU** — Trust On First
Use — reasonable *if* the first connection is made over a channel
you trust (a lab VM's own host: perfect; a café's captive portal:
not).

When a previously-seen server presents a **different** key, SSH
refuses loudly with the famous **REMOTE HOST IDENTIFICATION HAS
CHANGED** warning. Two legitimate causes: the server was rebuilt
(reinstalled VM — the daily reality of labs), or something is
intercepting the connection. The professional response is
*verification, then update*: confirm the new fingerprint out-of-band
(you just rebuilt the VM yourself — the console shows its new
fingerprint), then remove the stale line:

```console
$ ssh-keygen -R localhost        # removes the recorded key (safe, surgical)
```

What you *never* do: disable host-key checking to "fix" the warning
(`StrictHostKeyChecking no` in a config is the course's marked
anti-pattern — the one switch that turns SSH's authentication into
a suggestion).

## 3. Password vs keys — the authentication spectrum

| Method | What proves you | Weakness |
|---|---|---|
| Password | something you know | guessable, phishable, typed on every login, brute-forceable over the wire |
| Key pair | something you **have** (private key) + optional *something you know* (passphrase) | the private file — hence file permissions and passphrases |
| Key + agent | the key, unlocked once per session | agent compromise (rare, local) |

A **key pair** is asymmetric cryptography in daily clothes: the
**private key** (a file only you possess) signs a challenge; the
**public key** (freely shareable, stored on servers) verifies it.
The private key never crosses the network — that's the whole
security argument over passwords, which *do* cross it (encrypted,
but present on the server's side for checking).

The DS reality: university clusters and cloud GPUs either require
keys outright or beg for them. This course's standard from Lab 1 on:
**keys, passphrase-protected, agent-unlocked**.

## 4. ssh-keygen — making a key pair

```console
$ ssh-keygen -t ed25519 -C "ds-lab-vm 2026-09" -f ~/.ssh/lab_vm
Generating public/private ed25519 key pair.
Enter passphrase (empty for no passphrase): ********
Your identification has been saved in: /home/ds/.ssh/lab_vm
Your public key has been saved in: /home/ds/.ssh/lab_vm.pub
```

Dissected:

- `-t ed25519` — the algorithm: modern, fast, small keys. (RSA
  3072+ remains acceptable legacy; ed25519 is the course default.)
- `-C comment` — *which* key/when; your future self's archaeology.
- `-f ~/.ssh/lab_vm` — the output path. **Never overwrite an
  existing key** (`ssh-keygen` asks; read before answering). Lab
  gets its own name so the lab never touches personal keys.
- The **passphrase** encrypts the private key at rest. No passphrase
  = whoever copies the file *is* you. The passphrase costs one
  unlock per session (the agent, §5) — pay it.

The pair on disk:

```console
$ ls -l ~/.ssh/
-rw------- 1 ds ds  444 Sep 15 21:04 lab_vm        ← PRIVATE: 600, never shared
-rw-r--r-- 1 ds ds  96  Sep 15 21:04 lab_vm.pub    ← public: shareable
```

The permissions are not decoration — sshd *refuses* keys with lax
private-file modes, and [M17/M12's](../../../M17-storage-and-filesystems/content/README.md)
`chmod 600` finally has its reason: `600` = owner read/write only.

## 5. ssh-agent — unlock once, use all day

```console
$ eval "$(ssh-agent)"       # starts the agent, sets SSH_AUTH_SOCK
$ ssh-add ~/.ssh/lab_vm
Enter passphrase for /home/ds/.ssh/lab_vm: ********
$ ssh-add -l                # list loaded keys — verify
```

The agent holds **decrypted** keys in memory; subsequent ssh/scp/
rsync/Git-over-SSH use them without re-typing the passphrase. On
Ubuntu desktop sessions a per-session agent usually runs already —
`ssh-add -l` tells you ("The agent has no identities" = agent exists,
empty; connection refused = none). Course pattern: `eval "$(ssh-agent)"`
once per session, `ssh-add` once, work all day.

## 6. authorized_keys — installing the public half

A server accepts your key when your **public key** appears in the
target account's `~/.ssh/authorized_keys`, one per line. The blessed
installer:

```console
$ ssh-copy-id -i ~/.ssh/lab_vm.pub ds@localhost
Number of key(s) added: 1
```

`ssh-copy-id` handles the details that trip everyone when done by
hand: creating `~/.ssh` with `700`, `authorized_keys` with `600`,
correct ownership ([M13's](../../../M13-ownership-shared-access/content/README.md)
ownership rules, now load-bearing), no duplicate lines. By hand it's:

```bash
cat ~/.ssh/lab_vm.pub | ssh ds@localhost \
  'mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys'
```

Which is why the tool exists. Then the moment:

```console
$ ssh ds@localhost 'echo connected as $(whoami)@$(hostname)'
connected as ds@ds-lab
```

No password: **key-based authentication works.** (If a password is
still requested — that's Lab 2's patient #1.)

## 7. Key hygiene — the rules that keep keys worth having

1. **Private keys never leave your machine** — not into repos
   (`.gitignore`-ed at [M04](../../../M04-installing-linux-vms/README.md) and
   [M26](../../../M26-git-dev-workflows/README.md) for exactly this), not
   into chats, not onto shared servers. `authorized_keys` gets
   *public* keys only.
2. **`chmod 600` on private keys, `700` on `~/.ssh`** — enforced by
   ssh on both ends.
3. **A passphrase per key** — and different keys for different
   contexts (lab ≠ personal ≠ work) so one leak isn't total.
4. **Key = identity.** Whoever holds the file logs in as you. Lost
   key? Remove its public line from `authorized_keys` everywhere it
   was deployed (one line, instantly revocable — another argument
   over passwords).
5. **`ssh-keygen -y -f ~/.ssh/lab_vm`** prints the public half from a
   private key — for verifying a `.pub` matches, not for sharing
   carelessly.

## 8. Try it now (10 minutes)

1. `ls ~/.ssh/` — inventory what exists *before* generating anything
   (never overwrite). Then generate `lab_vm` per §4.
2. `ssh-keygen -lf ~/.ssh/lab_vm.pub` — print the key's fingerprint;
   compare its shape to the host-key fingerprint from §2 (same
   format, different role: *your* identity vs *the server's*).
3. `ssh-add -l` — what does your agent hold right now? Start one if
   needed, add the lab key, re-check.
4. The permissions test: `chmod 644 ~/.ssh/lab_vm` then `ssh
   localhost`. Read the warning — ssh refusing *you* is the security
   working. Restore `600`.

## 9. Common mistakes

- Overwriting an existing key pair at generation time (the `-f`
  prompt is not a formality).
- Typing the **private** key's contents into `authorized_keys` —
  it's the `.pub` file that installs.
- Treating "no passphrase" as convenience — it converts your key
  file into your password, lying on disk.
- Trusting a changed host key blindly — §2's procedure: verify
  out-of-band, then `ssh-keygen -R` + reconnect.
- `~/.ssh` or `authorized_keys` with wrong modes/ownership on the
  *server* side — sshd silently ignores the file; Lab 2's clinic
  makes this muscle memory.

> **Up next:** [Lesson 2 — ssh_config & sshd
> hardening](02-config-sshd-hardening.md): the client config that
> makes you fast, and the server config that makes the server safe.
