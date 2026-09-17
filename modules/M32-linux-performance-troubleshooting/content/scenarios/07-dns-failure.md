# Drill Card 7 — "DNS Failure"

> Scenario family: Network · Difficulty: ●●○
> Source modules: [M21 lesson 3](../../../M21-networking-fundamentals/content/lessons/03-dns-resolution.md), [M21 troubleshooting](../../../M21-networking-fundamentals/content/troubleshooting.md)

## Symptom

`curl: (6) Could not resolve host: …`, pip/git "name or service not
known" — while plain IPs still work (the discriminator that makes this
card its own, separate from card 8).

## Decision tree

```text
dig +short <name>  →  answer?
├─ answer, but app fails     → app's resolver/hosts file (nsswitch, /etc/hosts)
├─ NXDOMAIN / no answer      → resolver config (stub? upstream?) → resolvectl
└─ SERVFAIL/timeouts         → upstream unreachable → is IP networking fine? (card 8)
```

## Evidence

```console
$ dig +short example.com            # the resolver's own answer
$ dig +short @1.1.1.1 example.com   # bypass the local resolver: same answer?
$ resolvectl status | head -20      # who IS the resolver? (M21 §3)
$ cat /etc/hosts | tail -5          # the override layer (a stale lab entry?)
$ time dig example.com              # resolution *latency*, distinct from failure
```

The `hosts`-file override is the classic lab trap — M21 Lab 2's
incident #1: a leftover `127.0.0.1 example.com` line makes every
resolver agree on the *wrong* answer. nsswitch consults hosts *first*
(`getent hosts example.com` shows what the system will actually use —
the command that ends most DNS arguments).

## Fix pattern

- **Stale /etc/hosts entry** → remove/correct the line (sudo, one
  edit, undo known).
- **Wrong resolver** → `resolvectl dns <iface>` to inspect; on
  lab VMs the fix is usually the network provider's DHCP config, not
  a hand-edit — document, don't hardcode.
- **Upstream SERVFAIL** → evidence to the admin/network owner (card
  8's escalation posture): timestamps, dig outputs, the @1.1.1.1
  contrast.
- **The flush**: `resolvectl flush-caches` after fixes — and the
  honesty note that this rarely *fixes* anything; it removes one
  variable for the re-test.

## Verify

Three levels: `dig +short` answers; `getent hosts` agrees (the
system-level resolution); **the original command works** (`pip
install`, `git fetch`). DNS "fixed" at dig-level but not app-level
means the app caches or pins — card 10's territory when it's pip.

## Document

Quote the before/after dig pair and the discriminating command
(`getent`). Vocabulary: *"stale hosts override"*, *"stub resolver
pointing at dead upstream"*, *"app-level cache, not resolver"*.

**Done when:** you can break your VM's resolution with a hosts entry,
diagnose it in ≤ 5 commands, and restore + verify at all three levels.
