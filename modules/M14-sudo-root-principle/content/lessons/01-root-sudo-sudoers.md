# Lesson 1 — Root, sudo & the sudoers File

> Module 14 · Unit 4 · Difficulty: Intermediate
> Reading time: ~30 min · Lab: [Lab 1 — sudo practice](../labs/lab-01-sudo-practice.md)
> Prerequisites: [M12 identity](../../../M12-users-groups-permissions/content/lessons/01-identity-users-groups.md),
> [M13 shared dirs](../../../M13-ownership-shared-access/content/lessons/01-ownership-chown-shared-dirs.md)

> ⚠️ **This module handles real power.** Every command in it is scoped to *your
> own VM or WSL2 instance*. Never practice sudo on a shared university server
> beyond what your instructor authorized — and never reconfigure sudo on any
> machine you don't own.

---

## 1. Who is root?

**Root** is the account with **UID 0** — the administrative superuser. Root
is not "a user with all permissions"; it is the identity the kernel treats as
exempt from permission checks altogether:

- reads and writes any file, regardless of mode bits or ACLs
- kills any process, binds any port, loads/unloads kernel modules
- changes ownership of anything, mounts and formats disks

Check on your own system:

```console
$ grep "^root:" /etc/passwd
root:x:0:0:root:/root:/bin/bash
```

Fields: name `root`, UID `0`, GID `0`, home `/root`, shell `/bin/bash`.

**Why root exists:** some operations must be possible but must not be
possible for *everyone* — changing other users' passwords, installing
software, configuring network interfaces. Unix resolves this with a single
privileged identity rather than a matrix of per-task powers.

**Why you must not *log in* as root:**

1. **No undo, no questions.** `rm -rf /` as root just… runs. Typos are
   unrecoverable; `sudo` at least makes each privileged action deliberate.
2. **No audit trail.** Shared servers need to know *who* did what. If
   everyone is root, nobody is accountable.
3. **Malware and mistakes run with full power.** A single
   `curl evil.sh | bash` as root ends the machine's trustworthiness.
4. **Habit formation.** Admins who live as root eventually run a data-deletion
   loop with the wrong variable. This is not folklore; it is why every
   distribution ships with root login disabled by default (Ubuntu: root has
   no password and cannot log in — see `/etc/shadow`'s `!` in its hash
   field).

```console
$ sudo grep "^root:" /etc/shadow
root:!:19800:0:99999:7:::
```

The `!` (or `*`) means "no valid password hash" — password login for root is
locked. Ubuntu's model: **humans log in as themselves; root acts through
sudo.**

### DS framing

On a university GPU server, root is held by the sysadmin alone. If a
dataset pipeline "needs root", that's usually a *design smell* — a
permissions problem (M13) masquerading as a privilege problem. Lesson 2
shows the legitimate exceptions.

---

## 2. su: switch user (the old way)

`su` ("substitute user") starts a shell as another user:

```console
$ su - alice          # become alice with her full environment (login shell)
$ su alice            # alice's shell, but YOUR environment lingers
$ su -                # become root (asks for ROOT's password)
```

- The `-` (login shell) matters: without it you keep your `PATH`, umask and
  working directory — a classic source of "works with `su -`, fails with
  `su`".
- `su -` needs root's password. On Ubuntu that password doesn't exist
  (locked account), so `su -` fails by design.

**When `su` is still the right tool:** testing "what does this service see?"
— `su - postgres -s /bin/bash` (many service accounts have no usable shell)
to inspect a database's environment exactly as the daemon experiences it.
That diagnostic trick returns in M20.

**For daily administration, use `sudo` instead.** Reasons follow.

---

## 3. sudo: do one thing as root

`sudo` ("superuser do") executes **one command** with another identity —
root by default:

```console
$ whoami
dsstudent
$ sudo whoami
[sudo] password for dsstudent:
root
$ sudo -u alice whoami     # run as a *specific* user, not necessarily root
alice
```

Key properties, each worth memorizing:

1. **You type YOUR password**, not root's. Root stays locked; the right to
   escalate is granted per-user by policy, not by knowing a secret.
2. **Every use is logged.** Ubuntu ships `sudo` logging via journald:
   `journalctl -e _COMM=sudo` shows who ran what, when (full commands are
   in the auth log — M26 revisits).
3. **The grant expires.** Default timestamp: 15 minutes per terminal
   (`timestamp_timeout`). Walk away, and the next `sudo` re-asks. You can
   end it early: `sudo -k`.
4. **Policy decides.** Whether you're allowed *at all*, and *what*, is
   written in the sudoers file (next section) — not in what you know.

### sudo vs su — the one-paragraph version

`su` hands over a whole identity on presentation of *root's* secret;
`sudo` lends specific power on presentation of *your own* identity and a
matching policy rule. The first makes accountability impossible; the second
makes it automatic. That is why Ubuntu disables root and configures sudo
out of the box — and why this course never uses `su -` except for
diagnostics.

---

## 4. The sudoers file: /etc/sudoers

sudo's policy lives in `/etc/sudoers` (plus fragments in `/etc/sudoers.d/`).

**Rule one: never edit it with a normal editor.** A syntax error can lock
*everyone* out of root on a machine whose root password is disabled. The
`visudo` command exists precisely to prevent that:

- `sudo visudo` — edits the main file, **syntax-checks on save**, refuses a
  broken file.
- `sudo visudo -f /etc/sudoers.d/ds-lab` — same safety for a drop-in.
- `sudo visudo -c` — check-only (verify before rebooting).

**Reading the base rule:**

```console
$ sudo grep -v "^#" /etc/sudoers | grep -v "^$"
Defaults env_reset
Defaults mail_badpass
Defaults secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
root    ALL=(ALL:ALL) ALL
%sudo   ALL=(ALL:ALL) ALL
@include /etc/sudoers.d/*
```

Decoding `%sudo   ALL=(ALL:ALL) ALL` — the four fields:

| Field | Example | Meaning |
|---|---|---|
| who | `%sudo` | the `sudo` **group** (`%` = group; no `%` = user; `%` + `#` forms also exist) |
| from-host | `ALL` | valid on any host this file applies to |
| as-who | `(ALL:ALL)` | may run as any user **and** any group |
| command | `ALL` | may run any command |

So on Ubuntu: **membership in group `sudo` is what makes you an
administrator.** Verify your own grant:

```console
$ groups | tr ' ' '\n' | grep -x sudo && echo "you can sudo" || echo "no sudo"
$ sudo -l            # what exactly may I run?
Matching Defaults entries for dsstudent on labvm:
    env_reset, mail_badpass, secure_path=...
User dsstudent may run the following commands on labvm:
    (ALL : ALL) ALL
```

`sudo -l` is the polite way to answer "can I?" before trying and burning a
failed attempt into the logs.

### Drop-ins: /etc/sudoers.d/

Fragments are merged lexically; **file names must not contain `.` or `~`**
(a `foo.bak` is ignored — a gift when you want a rule temporarily off:

```console
$ sudo visudo -f /etc/sudoers.d/researcher-rota
# on-call researchers may refresh the shared dataset mirror without a password
%researchers ALL=(root) NOPASSWD: /usr/local/bin/sync-datasets
```

This is the least-privilege pattern: a **specific group**, running a
**specific script**, **as root only for that script**, no password needed
for automation. Compare with `%sudo ALL=(ALL:ALL) ALL` — the difference is
the blast radius.

**NOPASSWD deserves respect, not fear:** it trades the password prompt for
log-everything. For an unattended nightly sync, a password prompt would
simply break the job; the command itself is the gate. For interactive
`ALL`, NOPASSWD would remove the "am I sure?" pause — don't.

### Defaults worth knowing

- `secure_path` — sudo resets `PATH` so you can't be tricked into running a
  planted `sudo ./malware` from a hostile directory.
- `env_reset` — your environment variables don't leak into the privileged
  command (credential variables, proxies, `PYTHONPATH`).
- `!visiblepw`, `mail_badpass` — repeated failures notify admins.

**Practice editing sudoers only inside your own VM** — and first snapshot
it: `sudo cp /etc/sudoers /etc/sudoers.bak-$(date +%F)` is a *file copy*,
not a sudoers change; `visudo` still guards the real edit. If you break
sudo in your VM: reboot to recovery mode (GRUB → root shell) or use the
VM host to restore the backup. Lab 1 walks a *safe* break-and-repair on a
throwaway drop-in, never the main file.

---

## 5. The sudo workflow you should build into your hands

Before pressing Enter on any sudo command, run this five-beat check:

1. **Why root?** Name the permission that requires it. If none comes to
   mind, you don't need sudo — plain command probably fails for a *reason*
   worth understanding first.
2. **What exactly will it touch?** `apt install` = package + deps;
   `chmod -R` = whole tree; `userdel -r` = user + home. Scope the blast
   radius before, not after.
3. **Can I preview?** `apt install -s` (simulate), `ls` the target of a
   move, `--dry-run` when a tool offers one. Root removes the "oops" from
   undo; previews are your undo.
4. **Read the prompt back.** `sudo rm -rf $FOO/ *` — that stray space turns
   "delete folder contents" into "delete everything from root". Root makes
   that immediate.
5. **Log it.** After the fact, `journalctl _COMM=sudo | tail` — a habit
   that makes audits boring later.

### DS framing: when a data scientist legitimately needs sudo

On your own machines (VM, WSL2, cloud instance you own), routinely:

- `sudo apt install python3.12-venv build-essential` — toolchains
- `sudo usermod -aG docker $USER` — container access (M28)
- `sudo mkfs.ext4 /dev/sdb1` — formatting a scratch data disk (M16/M17)
- `sudo setfacl` on shared trees (M13)

On shared servers: almost never. If a pipeline needs root there, the fix is
usually a sudoers *drop-in* scoped to a helper script — the
`sync-datasets` pattern above — negotiated with the sysadmin, not a request
for group membership in `%sudo`.

---

## 6. Common sudo moments and what they mean

```console
$ sudo apt update
[sudo] password for dsstudent:
```
Normal. Your password; nothing echoes — not even asterisks. That is
`getpass` behavior, not a hung terminal.

```console
$ sudo -v
Sorry, try again.
```
Wrong password, three tries, then sudo logs the failure and exits.

```console
$ dsstudent is not in the sudoers file. This incident will be reported.
```
Policy says no. On your own VM: add yourself via recovery or (from another
admin account) `sudo usermod -aG sudo dsstudent` — note `usermod`, not
editing sudoers, for plain group membership. On a shared server: that
message is the system working; contact the admin.

```console
$ sudo: unable to resolve host labvm: Name or service not known
```
Harmless-but-noisy WSL2/VM artifact: the hostname isn't in `/etc/hosts`.
Fix (your own machine): `echo "127.0.1.1 $(hostname)" | sudo tee -a /etc/hosts`.
Notice the pattern — `sudo tee` instead of `sudo echo >` (the `>` redirect
happens in *your* shell, unprivileged; `tee` receives the file as root).

That last point is the classic beginner wall: **redirection happens before
sudo applies.** `sudo echo "x" > /etc/hosts` writes nothing privileged.
Remedies: `sudo sh -c 'echo "x" > /etc/hosts'` or `echo x | sudo tee -a
/etc/hosts`. Understanding *why* (the shell parses `>` before sudo runs)
is precisely the shell fluency M09 built.

---

## Exercises (lab-log.md)

1. Explain, in your own words, why Ubuntu locks root's password instead of
   just trusting users to be careful.
2. `sudo -l` on your VM. Paste the output and decode every field of the
   matching rule.
3. Why does `su -` fail on a stock Ubuntu VM? What would `sudo su -`
   (or better, `sudo -i`) do instead — and when would a sysadmin use it?
4. Write the sudoers drop-in for: "members of `bench` may run
   `/usr/bin/jupyter-lab` as user `svc-notebooks` with no password." Then
   answer: why is `NOPASSWD` acceptable *here* but dubious for
   `ALL=(ALL) NOPASSWD`?
5. Your teammate proposes `sudo chmod -R 777 /srv/projects` "to stop the
   permission tickets". Write the 3-sentence reply a sysadmin would send.
6. Predict, then verify: does `sudo echo hi > /etc/hostname.scratch`
   (in your VM) create the file? Where does the file land, and why?

## Check yourself before M15

- [ ] I can explain the four fields of a sudoers rule.
- [ ] I know why `visudo` exists and can name what it prevents.
- [ ] I know where sudo logs go and how to look at my own entries.
- [ ] I can articulate when a DS workflow legitimately needs root — and
      when it's a permissions smell instead.

## Further reading (official sources)

- `man 8 sudo`, `man 5 sudoers`, `man 8 visudo`
- Ubuntu Server Docs — *Security*: https://ubuntu.com/server/docs
- Debian policy roots (upstream of Ubuntu's model): https://www.debian.org/doc/manuals/debian-reference/
- The sudo project's own docs: https://www.sudo.ws/docs/man/sudoers.man/
