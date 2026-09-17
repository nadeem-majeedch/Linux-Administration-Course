# Lab 1 — The Key Workflow: Zero to Passwordless

> Module 22 · Unit 6 · Difficulty: Advanced
> Time: ~50 min · Environment: host + your own VM
> Prerequisites: [Lesson 1](../lessons/01-ssh-fundamentals-keys.md),
> [Lesson 2](../lessons/02-config-sshd-hardening.md), VM with sshd
> running (`sudo systemctl status ssh` inside the VM)
> ⚠️ Lab key only (`lab_vm`), never a personal key. If your VM's
> sshd isn't installed: `sudo apt install openssh-server` inside the
> VM (the M16 five-beat workflow).

Five stages, each *verified* before the next. The deliverable is not
"a working login" — it's the *muscle memory plus evidence trail*
that makes the university-GPU-server version of this routine
boring.

## Setup — pick your path (5 min)

**Path A (recommended, no VM networking needed):** work *inside* the
VM, SSHing to itself — `ds@localhost` as both ends.

**Path B (the real shape):** host → VM over the loopback port
forwarding every VM app provides (VirtualBox NAT: host port 2222 →
guest 22). Everything below says `Port 2222` for Path B; skip it
for Path A.

Confirm the target first:

```console
$ ssh ds@localhost 'echo ok'      # Path A — password login expected
# or, Path B from the host:
$ ssh -p 2222 ds@localhost 'echo ok'
```

Record this **baseline**: password login works. (If it doesn't,
stop and fix — a clinic before the lab is a lesson, not a delay.)

## Stage 1 — generate (5 min)

On the *client* machine (host for B, VM for A):

```console
$ ls ~/.ssh/                        # inventory FIRST — never overwrite
$ ssh-keygen -t ed25519 -C "lab22 $(date +%F)" -f ~/.ssh/lab_vm
$ ssh-keygen -lf ~/.ssh/lab_vm.pub  # record the fingerprint in lab-log.md
$ ls -l ~/.ssh/                     # verify: lab_vm is 600, lab_vm.pub is 644
```

Passphrase: **required** in this lab — you'll type it exactly twice
(ever), and the agent (Stage 3) makes it twice.

## Stage 2 — deploy (10 min)

```console
$ ssh-copy-id -i ~/.ssh/lab_vm.pub -p 2222 ds@localhost
$ ssh -i ~/.ssh/lab_vm -p 2222 ds@localhost 'echo KEY-LOGIN-OK'
```

If a password was still requested: check the *server* side before
moving on — `ls -ld ~/.ssh ~/.ssh/authorized_keys` on the VM (700 on
the dir, 600 on the file, owned by `ds`), and the auth.log line
(`sudo tail -3 /var/log/auth.log`) naming why the key was rejected.
Those two checks are 90% of all real key failures; note them now,
rely on them in Lab 2.

Then verify the *decisive* property: exit, re-connect — **no
password**. Record both sides: `~/.ssh/authorized_keys` line on the
VM (`cat ~/.ssh/authorized_keys`), and the matching fingerprint.

## Stage 3 — agent (10 min)

```console
$ eval "$(ssh-agent)"        # skip if ssh-add -l says an agent already runs
$ ssh-add ~/.ssh/lab_vm      # passphrase: second and last time
$ ssh-add -l                 # the fingerprint matches Stage 1's record
```

Now prove the passphrase-free reality: new terminal →
`ssh -p 2222 ds@localhost 'echo agent-ok'` — instant, silent. Two
lines in `lab-log.md`: the fingerprint, and "agent holds it, typing
ended."

## Stage 4 — ssh-config (10 min)

`~/.ssh/config` (create it; `chmod 600 ~/.ssh/config`):

```sshconfig
Host vm
    HostName localhost
    User ds
    Port 2222                     # omit for Path A
    IdentityFile ~/.ssh/lab_vm
    IdentitiesOnly yes

Host *
    AddKeysToAgent yes
    ServerAliveInterval 60
```

```console
$ chmod 600 ~/.ssh/config
$ ssh -G vm | grep -E '^hostname|^port|^user|^identityfile'   # what the client resolved
$ ssh vm 'echo alias-works'     # the new daily form
```

Then the payoff test — other tools inherit the alias:

```console
$ scp ~/some-file.txt vm:~/          # scp via alias
$ ssh vm 'rm ~/some-file.txt'        # clean up via alias
```

## Stage 5 — first contact & the break-glass rehearsal (10 min)

1. **Fingerprint decision:** if this VM prompted `authenticity`
   (fresh `known_hosts`), record the prompt and your yes — with the
   *reason* it was trustworthy (you own the machine). If no prompt
   appeared, print the stored record instead:
   `ssh-keygen -lf ~/.ssh/known_hosts` (or grep localhost) and note
   where trust came from (TOFU, earlier).
2. **Rebuild rehearsal:** inside the VM,
   `sudo rm /etc/ssh/ssh_host_*` + `sudo systemctl restart ssh`
   (regenerates host keys — a *rebuild in miniature*). Reconnect:
   the **HOST KEY CHANGED** warning, verbatim into `lab-log.md`.
   Since *you* caused the change, verification is trivially
   satisfied → `ssh-keygen -R localhost` → reconnect → accept →
   document the full sequence. This is the one time you should ever
   see that warning; knowing its choreography is the point.

## Done when

- [ ] All five stages' evidence in `lab-log.md` (fingerprints,
      permission listings, `ssh -G` output, the warning text)
- [ ] `ssh vm 'echo ok'` passwordless from a fresh terminal
- [ ] The rebuild rehearsal documented end-to-end
- [ ] No `~/.ssh` permissions loosened anywhere except the Stage-5
      deliberate break (all restored — verify with `ls -l ~/.ssh`)
