# Lab 1 — sudo Practice, Safely

> Module 14 · Unit 4 · Difficulty: Intermediate
> Environment: **your own VM or WSL2 instance only**
> Prerequisites: [Lesson 1](../lessons/01-root-sudo-sudoers.md)
> ⚠️ Nothing here touches the main sudoers file destructively; we break a
> *drop-in*, in a VM you can reset.

## Setup (3 min)

```console
$ mkdir -p ~/lab14 && cd ~/lab14
$ echo "# lab14 scratch" > note.txt
$ sudo -v            # warm the credential cache
```

Record everything in `lab-log.md` — this lab's deliverable is evidence, not
a working config.

---

## Part A — observe the mechanics (no config changes)

```console
$ sudo -l                       # 1. what may I run?
$ sudo -k                       # 2. kill the credential cache
$ sudo -n true                  # 3. non-interactive check: expect failure
sudo: a password is required
$ sudo -v                       # 4. re-auth, then check again
$ sudo -n true && echo cached
```

**Questions for `lab-log.md`:**
1. After `sudo -k`, why does `sudo -n true` fail *before* asking anything?
2. Run `sudo -v`, then immediately `sudo -n true`. What does this prove
   about where the credential lives (per-user, per-terminal, or global)?
   (Hint: try it again from a *second* SSH/WSL terminal to the same VM.)

## Part B — the audit trail

```console
$ journalctl _COMM=sudo --no-pager | tail -8
```

Note your `sudo -l`, `sudo -k` and password entries. Now find the auth-log
side:

```console
$ sudo grep sudo /var/log/auth.log | tail -5     # native Ubuntu
$ journalctl -u sudo --no-pager | tail -5        # journald alternative
```

**Deliverable:** in `lab-log.md`, quote one line and annotate it field by
field (who, from which TTY, which directory, which command).

## Part C — the redirection wall (the classic)

Predict each, *then* run:

```console
$ echo "test" > /etc/hostname.scratch
bash: /etc/hostname.scratch: Permission denied      # your shell, your rights
$ sudo echo "test" > /etc/hostname.scratch
bash: /etc/hostname.scratch: Permission denied      # SAME failure — why?
```

Explanation (write it in your own words first): the shell opens
`/etc/hostname.scratch` for writing **before** `sudo` even starts — the
redirection is performed by your unprivileged shell. `sudo` only elevates
the command on its left.

Three correct patterns — use and compare:

```console
$ echo "test" | sudo tee /etc/hostname.scratch          # tee writes as root
$ sudo sh -c 'echo "test" > /etc/hostname.scratch'      # whole shell elevated
$ sudo install -m 644 /dev/null /etc/hostname.scratch   # create via install
```

Cleanup: `sudo rm /etc/hostname.scratch` (safe: file you just created, name
visible in `ls` first).

## Part D — a scoped drop-in, done properly

Goal: your user may run **one specific script** as root without a password —
the least-privilege pattern from Lesson 1 §4.

```console
$ sudo tee /usr/local/bin/hello-admin >/dev/null <<'EOF'
#!/bin/bash
# hello-admin — lab14 demo script; prints root identity and a timestamp
id -u
date -Is
EOF
$ sudo chmod 755 /usr/local/bin/hello-admin
$ sudo visudo -f /etc/sudoers.d/lab14-hello
```

In visudo, add exactly (replacing `dsstudent` with your username):

```
dsstudent ALL=(root) NOPASSWD: /usr/local/bin/hello-admin
```

Save — visudo syntax-checks. Then verify both the grant and the boundary:

```console
$ sudo -l | grep -A1 hello        # the specific rule appears
$ sudo /usr/local/bin/hello-admin # works, no password
$ sudo -n /usr/local/bin/hello-admin && echo "NOPASSWD confirmed"
$ sudo -n whoami                  # still demands a password — boundary holds
```

That last pair is the whole lesson in two commands: **one** command is
passwordless, everything else still asks.

## Part E — safe break-and-repair (in your VM only)

We disable a *drop-in* the supported way, then restore it. The main
sudoers file is never touched.

```console
$ sudo mv /etc/sudoers.d/lab14-hello /etc/sudoers.d/lab14-hello.bak
$ sudo -l | grep -c hello || echo "grant gone (dot-names are ignored)"
$ sudo /usr/local/bin/hello-admin    # now demands password again
```

**Why the rename worked:** sudoers ignores files whose names contain `.` —
the documented way to retire a rule without deleting it (Lesson 1 §4).

Restore:

```console
$ sudo mv /etc/sudoers.d/lab14-hello.bak /etc/sudoers.d/lab14-hello
$ sudo visudo -c                     # verify the whole policy parses
/etc/sudoers: parsed OK
/etc/sudoers.d/lab14-hello: parsed OK
```

**Never do this experiment on `/etc/sudoers` itself.** If a lab machine's
sudo ever breaks: reboot, hold Shift in GRUB → *Advanced options* →
*recovery mode* → *root shell*, then `visudo -f /etc/sudoers` to repair.
In WSL2: `wsl -u root` from Windows PowerShell. Practice the recovery once,
on purpose, so it's boring when it matters.

## Part F — prove the boundary (reflection)

In `lab-log.md`, answer:

1. Why does `NOPASSWD` make sense for `hello-admin` but would be reckless
   for `ALL`?
2. Your teammate's drop-in says `%students ALL=(ALL) NOPASSWD: ALL`. State
   the two concrete risks, then write the corrected line for "students may
   run `/usr/bin/apt update` only".
3. `secure_path` stopped you from `cd ~/evil && sudo ./apt`. Explain the
   attack that default defeats.

## Done when

- [ ] `sudo -l` output pasted and decoded in `lab-log.md`
- [ ] One annotated auth-log line
- [ ] Redirection-wall experiment with your written explanation
- [ ] Drop-in created, boundary proven (`sudo -n whoami` asks password)
- [ ] Break-and-repair executed via the rename pattern; `visudo -c` clean
- [ ] Part F reflections written
