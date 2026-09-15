# Lab 2 — Sudo Incidents: Diagnose & Repair

> Module 14 · Unit 4 · Difficulty: Advanced
> Format: three tickets, escalating. Each gives you symptoms only; you
> diagnose on **your own VM**, reproduce where safe, and write a fix the
> way you'd hand it to a sysadmin.
> Prerequisites: [Lab 1](lab-01-sudo-practice.md)

Work in `lab-log.md` under headings `Ticket A/B/C`. For each: **evidence →
diagnosis → fix → verification → prevention**. That five-part structure is
the same one M25's security triage and the capstone post-mortem use.

---

## Ticket A — "sudo suddenly asks for a password every 30 seconds"

**Reported by:** MSc student, own WSL2 instance.
**Symptoms:** after following an online tutorial, every `sudo` prompts
again almost immediately; previously it remembered for a session.

**Investigate:**

```console
$ sudo grep -r timestamp_timeout /etc/sudoers /etc/sudoers.d/
```

A tutorial had them add `Defaults timestamp_timeout=0` to a drop-in —
defensible on a *shared admin box*, terrible for a personal VM.

**Fix (choose and justify):** delete the line in the drop-in, or set
`timestamp_timeout=15` (the Ubuntu default). Use `visudo -f`.

**Verification:** `sudo -v && sudo -n true` twice, two minutes apart.

**Prevention:** where should "hardening tutorials" be tested first? (Answer
in one sentence: a VM snapshot, never the main workflow machine.)

---

## Ticket B — "user can't sudo, and we can't find why"

**Reported by:** a course TA; a student *is* in group `sudo` but gets
"not in the sudoers file".

**Reproduce the shape of it** (in your VM, safely, with a throwaway user):

```console
$ sudo adduser probe --disabled-password --gecos "probe"    # create test user
$ sudo usermod -aG sudo probe
$ sudo su - probe -c 'sudo -l'        # probe CAN sudo: baseline established
$ sudo mv /etc/sudoers.d/90-cloud-init-users /etc/sudoers.d/90-cloud-init-users.bak 2>/dev/null
```

The realistic breakage: on some cloud/WSL images, user grants live in a
drop-in (e.g. `90-cloud-init-users`) rather than group `sudo` in the main
file — someone "tidied" it and dropped the `@includedir` line from
`/etc/sudoers`, silently unloading every drop-in.

Simulate exactly that (reversible, in your VM):

```console
$ sudo cp /etc/sudoers /etc/sudoers.pre-lab14B
$ sudo sed -i 's/^@includedir/#&/' /etc/sudoers
$ sudo su - probe -c 'sudo -l'        # now: not in the sudoers file
```

**Diagnose with:** `sudo visudo -c` (parses, so not a syntax issue — a
*scope* issue), then `sudo grep -r "%" /etc/sudoers /etc/sudoers.d/ | grep
sudo` — the group rule is there, so why does `probe` fail? Read Lesson 1 §4
again: includedir processing. Restore:

```console
$ sudo sed -i 's/^#@includedir/@includedir/' /etc/sudoers
$ sudo visudo -c && sudo su - probe -c 'sudo -l'   # grant restored
$ sudo userdel -r probe                            # clean up the test user
```

**Deliverable:** explain, in `lab-log.md`, why the group membership wasn't
enough — and what the *actual* load-bearing line was.

---

## Ticket C — "apt fails mid-install; dpkg locked"

**Reported by:** you, eventually, on every machine you own.
**Symptoms:** `sudo apt install htop` dies mid-flight (laptop slept); now:

```
E: Could not get lock /var/lib/dpkg/lock-frontend. It is held by process 4123 (apt)...
```

**Diagnose first — never kill blindly:**

```console
$ sudo lsof /var/lib/dpkg/lock-frontend     # who holds it?
$ ps -p 4123 -o pid,cmd                      # what were they doing?
```

- If a real `apt`/`dpkg` is alive and downloading — *wait*; the lock is
  doing its job.
- If the process is gone (stale lock): the safe sequence is

```console
$ sudo dpkg --configure -a        # finish half-configured packages
$ sudo apt --fix-broken install   # repair dependency state
```

Killing processes or deleting lock files is the *last* resort and only
after confirming no package manager runs (`pgrep -a apt; pgrep -a dpkg`).

**Deliverable:** write the 4-line runbook you'd paste for the next student,
ordered: check → wait-or-repair → verify → only-then force.

---

## Wrap-up

Each ticket maps to a permanent habit:

| Ticket | Habit |
|---|---|
| A | Test hardening changes in a snapshot/VM first |
| B | `visudo -c` + `sudo -l` are the diagnostics; know where grants live |
| C | Diagnose the lock before touching it; `dpkg --configure -a` before force |

Done when all three tickets have the five-part structure and Ticket B's
explanation names the includedir mechanism explicitly.
