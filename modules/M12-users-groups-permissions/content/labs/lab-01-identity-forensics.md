# Lab 1 — Identity Forensics

> Lesson 1 · Time: ~45 min · Risk: zero (Parts 1–2, read-only everywhere);
> low (Part 3, VM-only throwaway accounts)

## Goal

Read the identity layer like an auditor, then exercise the account toolkit on
disposable users inside your own VM — creating the mental model M13's shared
server depends on.

## Part 1 — The catalog (15 min, read-only, anywhere)

1. `id`, `id -u`, `id -g`, `id -Gn` — record all four; mark which group is
   primary and *how you know*.
2. `grep ^$USER /etc/passwd` — decode all seven fields in your log.
3. `awk -F: '$3 < 1000 {print $1, $3}' /etc/passwd | head -15` — system
   accounts. Pick three; `grep` each in `/etc/group`. Are any of them groups
   *your* user belongs to? (On Ubuntu: the `sudo` group question.)
4. `grep -c nologin /etc/passwd` and `grep -c /bin/bash /etc/passwd` — the
   service-vs-human ratio on your machine.
5. `who; w` — your sessions. WSL2 users: explain each pts/tty line you see.

## Part 2 — The group map (10 min)

`getent group | grep $USER` vs `groups` vs `id -Gn` — three views of one fact.
Log what each shows that the others don't (one line per command). Then the
ownership question: `ls -ln /etc/hostname` — *numeric* owner/group view; which
numbers correspond to names you know?

## Part 3 — Account surgery (20 min, VM ONLY)

> **Environment gate:** run this part only in your course VM. If you're on a
> lab machine or don't have sudo, complete Parts 1–2 and read along here.

```console
$ sudo adduser t-alpha        # interactive; set a simple password
$ id t-alpha
$ sudo adduser t-beta
$ sudo groupadd t-team
$ sudo usermod -aG t-team t-alpha
$ sudo usermod -aG t-team t-beta
$ getent group t-team
```

Then the incident, deliberately:

```console
$ sudo usermod -G t-team t-alpha      # NOTE: no -a!
$ id t-alpha                          # what groups vanished?
```

Record exactly which memberships were destroyed by the missing `-a` — and
rebuild them. Then the lifecycle:

```console
$ sudo userdel -r t-beta
$ ls /home                            # home gone with -r
$ sudo groupdel t-team
$ sudo userdel -r t-alpha
$ getent passwd t-alpha               # silence = clean removal
```

Log the full sequence. This lab's value is the *scar tissue*: the `-aG` lesson
only sticks when you've watched the alternative eat a membership.

## Wrap-up checklist

- [ ] All five Part-1 probes recorded with one-line reads
- [ ] The three-views-of-membership compared
- [ ] Part 3 executed in the VM only; the `-a` incident documented and repaired
- [ ] Clean removal verified (`getent` silence, `/home` empty)
- [ ] One paragraph: how today's group design will show up in M13's shared
      dataset tree
