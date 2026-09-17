# Lesson 2 — Firewalls: The Model and ufw

> Module 25 · Unit 6 · Difficulty: Advanced
> Reading time: ~25 min · Lab: [Lab 1 — hardening](../labs/lab-01-hardening.md)
> Up next: [Lesson 3 — SSH hardening applied](03-ssh-hardening-applied.md)

---

## 1. What a firewall actually is

A **firewall** is the kernel deciding, packet by packet, what to
accept, forward, or drop — based on rules matching source/destination
address, port, protocol, and (with statefulness) connection history.
In Linux the machinery is **netfilter**; the tool that programs it
has changed names over the years — **iptables** (the classic),
**nftables** (its modern successor, Ubuntu's backend since 20.04) —
and each distro ships a friendlier front-end.

For an administrator you mostly touch the front-end; you need the
model beneath it to understand *what the front-end is doing*:

- **Rules** match packets (from where, to where, which port).
- **Policies** state the default for unmatched packets — the
  load-bearing decision (next section).
- **Stateful inspection** — the firewall tracks connections, so
  "allow established traffic" is one rule, not thousands.

## 2. Default-deny — the posture that does the work

Firewalls come in two postures:

| Posture | Default | Management cost | Failure mode |
|---|---|---|---|
| **Default-allow** | accept everything, block known-bad | rules grow forever (chasing threats) | every *forgotten* threat is open |
| **Default-deny** | drop everything, allow known-good | rules = the service inventory | a forgotten *service* is simply unreachable |

Default-deny wins structurally: your rule list becomes a *positive
inventory* of what the machine offers, and mistakes fail closed.
The cost is the discipline of explicitly allowing what you need —
and the classic self-lockout (firewall on, SSH rule forgotten) is
why Lab 1 has you **allow SSH before enabling ufw**, and rehearse
the recovery, not merely read about it.

## 3. ufw — the Ubuntu front-end

**ufw** (Uncomplicated Firewall) wraps nftables/iptables in
service-shaped commands. On Ubuntu it's preinstalled (inactive by
default — security-relevant to *know* your machine's posture, not
assume it):

```console
$ sudo ufw status verbose
Status: inactive
```

### The core vocabulary

```console
$ sudo ufw default deny incoming      # the posture (default already; explicit anyway)
$ sudo ufw default allow outgoing     # reasonable for a workstation/lab
$ sudo ufw allow OpenSSH              # service profile — port 22/tcp, by name
$ sudo ufw enable                     # arm it — firewall live
$ sudo ufw status verbose             # verify, always
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere
```

The enabling order — **default-deny → allow SSH → enable → verify
from a live session** — is the safety choreography Lab 1 drills.
`ufw disable` is the instant off-switch (and, with the M22 two-
terminal rule, a lockout becomes a lesson instead of a crisis).

### Rules: services, ports, sources

```console
$ sudo ufw allow 8000/tcp                    # raw port (the http.server from M22)
$ sudo ufw allow from 10.0.2.0/24 to any port 22 proto tcp   # SSH from the lab subnet only
$ sudo ufw deny 3306/tcp                     # explicit deny (MySQL: loopback-only service)
$ sudo ufw limit OpenSSH                     # rate-limit: 6 connections/30s per IP — bot-throttle
$ sudo ufw delete allow 8000/tcp             # remove a rule
$ sudo ufw insert 1 allow from 10.0.2.15     # ordering matters: first match wins
$ sudo ufw status numbered                   # rules with indices (for delete/insert)
```

Reads worth memorizing: `limit` is fail2ban-lite at the kernel layer
(throttling connection floods without reading logs); **source-scoped
rules** (`from <subnet>`) express "SSH from campus only" in one
line — the difference between a door and a door with a guest list.

### App profiles — service-shaped rules

Packages ship profiles declaring their ports, so rules reference
*services*, not numbers:

```console
$ sudo ufw app list
Available applications:
  OpenSSH
  CUPS
$ sudo ufw app info OpenSSH                  # what the profile opens
$ sudo ufw allow "Nginx Full"                # (M29 will use exactly this)
```

### What ufw does NOT do

Know the boundary: ufw filters **incoming** (and outgoing) network
packets. It does not harden services, patch software, read logs, or
limit what an allowed user may do — layers, per Lesson 1 §5. And it
cannot filter what never crosses it: loopback traffic (a service
bound to `127.0.0.1` needs no firewall rule — its exposure is local
by construction, M21 §3).

## 4. Beneath ufw — nftables/iptables, named for recognition

```console
$ sudo nft list ruleset | head -20           # what ufw actually wrote
```

Every ufw rule compiles into nftables tables/chains. You rarely
edit nftables directly on Ubuntu; you read it when debugging
("is the packet being dropped by ufw or something else?") and when
reading documentation for other stacks.

## 5. Ubuntu/Debian vs Red Hat — the same model, different front-ends

| Layer | Ubuntu/Debian | Red Hat family (RHEL, Fedora, CentOS Stream) |
|---|---|---|
| Kernel filter | netfilter | netfilter (same) |
| Direct tool | iptables/nftables | iptables/nftables (same) |
| **Front-end** | **ufw** | **firewalld** |
| Concept shape | flat rules, app profiles | zones (public/home/internal) + services, runtime vs permanent |
| Status | `sudo ufw status` | `firewall-cmd --state`, `--list-all` |
| Allow a service | `sudo ufw allow OpenSSH` | `firewall-cmd --permanent --add-service=ssh && firewall-cmd --reload` |

The translation is one-for-one at the *model* level (default-deny,
explicit allows, service profiles) — only the CLI dialect differs.
A DS person meeting a Red Hat compute cluster recognizes firewalld's
zones as firewalld's idea of source-scoped rules; the concept from
this lesson transfers whole. (Same pattern as apt vs dnf from M16:
kernel concepts shared, front-ends dialect.)

## 6. Try it now (15 minutes, inside your VM)

1. Posture check: `sudo ufw status verbose` — active or not? Record
   it. (An *inactive* firewall on a VM reachable by NAT-forwarded
   SSH is today's baseline; Lab 1 changes it.)
2. Dry-run thinking: `sudo ufw --dry-run allow OpenSSH` — read the
   nftables it *would* install. The M11 dry-run doctrine, at the
   kernel layer.
3. Design three rules on paper for your own VM: SSH (from your host
   subnet only), the 8000/tcp lab service (allow), 3306 (deny —
   justify with bind scope from M21). Lab 1 implements exactly this
   set.
4. `sudo ufw app list` and `sudo ufw app info OpenSSH` — which
   installed packages declare profiles? Profiles are documentation
   packaged with code.

## 7. Common mistakes

- Enabling ufw *before* allowing SSH — the self-lockout; the order
  above is the entire point of Lab 1's choreography.
- `allow 22` without protocol (`22/tcp`) or without a source when
  one was intended — rules are cheap; *precise* rules are the craft.
- Believing `ufw disable` lost your rules — it doesn't; `enable`
  re-arms them (and `reset` is the true wipe, needing confirmation).
- Forgetting ufw is stateful: you never add "allow established"
  rules by hand — the front-end handles it.
- Firewalld confusion on RHEL machines — translating `ufw allow X`
  literally; use the zone/service table in §5 instead.

> **Up next:** [Lesson 3 — SSH hardening
> applied](03-ssh-hardening-applied.md): M22's read-only directives
> become your VM's actual posture — with rollback plans.
