# Module 21 Troubleshooting — Network Symptoms → Causes → Fixes

> Ten patterns, ordered roughly by how often they bite real users.
> Each: **symptom → likely cause → diagnosis → fix → prevention**.
> Every diagnosis command is safe on your own VM; every fix stays
> within localhost/own-machine scope. The six-rung ladder lives in
> [Lesson 5](lessons/05-http-tools-diagnosis.md); this page is its
> symptom index.

## 1. "Could not resolve host: anything.example.com"

**Cause:** resolver unreachable, or the name genuinely doesn't exist.
**Diagnose:** `resolvectl status` (any DNS servers configured?);
`dig +short anything.example.com` (SERVFAIL/NXDOMAIN/timeout?); try a
known-good name (`dig +short www.ubuntu.com`) to separate "DNS broken"
from "name wrong".
**Fix:** if no servers are configured, re-connect the interface / renew
DHCP (rebooting a VM is an honest fix while learning). If only *your*
name fails, it's a typo or a missing `/etc/hosts` entry, not DNS.
**Prevention:** pin lab names in `/etc/hosts`; test two names before
blaming the resolver.

## 2. "It resolves for everyone else, not for me" (split-DNS)

**Cause:** your default resolver doesn't know the internal zone
(`corp`, university, VPN).
**Diagnose:** `dig +short name @<internal-DNS>` works but the plain
lookup doesn't; `resolvectl status` shows no `~corp` routing domain.
**Fix:** bring up the VPN that pushes its resolver and routing domains
(or add the host to `/etc/hosts` for a one-off).
**Prevention:** `resolvectl status` *before* the meeting, not during.

## 3. Connection refused — instantly

**Cause:** nothing is listening on that address:port; the machine is
fine and answered you — that's what "refused" means.
**Diagnose:** `ss -tlnp 'sport = :<port>'` (empty → nothing there);
check the service itself (`systemctl --user status <svc>` or the
process list).
**Fix:** start the service; if it binds `127.0.0.1` and you asked for
another address, that's the real problem (see #5).
**Prevention:** after every service restart, one `ss -tlnp` glance is
the "did it actually come up" reflex.

## 4. Connection times out — silently

**Cause:** packets die on the way: wrong address, dead route, firewall
drop, or service on a different machine than you think.
**Diagnose (localhost/own VM only):** `ip route get <target>` (which
route would be used?); `nc -zv <host> <port>` (verdict in one line);
remember NAT VMs (10.0.2.x) are unreachable *inbound* by design.
**Fix:** address/route/firewall — whichever rung failed. A timeout on
a NAT guest usually means "use port forwarding or bridged mode," not
"restart the server."
**Prevention:** `ip route get` before every remote-connection
assumption.

## 5. "Works on localhost, not through the name"

**Cause:** binding scope. The service listens on `127.0.0.1` only, but
the name (or the peer) reaches a different address.
**Diagnose:** `ss -tlnp` shows `127.0.0.1:8000` — the *whole* listening
address matters, not just the port; `getent hosts <name>` shows which
address the name actually yields.
**Fix:** align the name's address with a bound address (hosts entry →
`127.0.0.1`), or rebind the service deliberately (`--bind 0.0.0.0`
**only** with a firewall you understand — M25 territory).
**Prevention:** when writing "connect via `<name>:<port>`" docs,
record the bind address beside it.

## 6. Port already in use / "Address already in use"

**Cause:** another process holds the port — often a *previous instance
of the same server you forgot*, or a service that auto-started.
**Diagnose:** `sudo ss -tlnp 'sport = :<port>'` → process name and PID;
`pgrep -af <pattern>` for strays.
**Fix:** terminate the true owner (M18 ladder: preview → scope → TERM →
wait → KILL only if needed) or pick a different port.
**Prevention:** one command to start, the same habit to stop; never
blindly `kill -9` the PID `ss` shows — read *whose* process it is first.

## 7. DNS answers, everything else dies (the half-broken link)

**Cause:** resolver works (small UDP packets flow) but bulk traffic
doesn't — classic VPN/MTU or captive-portal symptom.
**Diagnose:** `ping -c3 <gateway>` (link OK?), then a small vs larger
fetch to a host you control on the lab network (MTU). On campus Wi-Fi,
open the captive portal — it's not your machine.
**Fix:** environment-side (portal login, VPN reconnect). Don't chase
your stack when the portal is the problem.
**Prevention:** know what "normal" looks like — the health check from
Lab 1 makes anomalies visible in seconds.

## 8. Intermittent name failures ("works, then doesn't")

**Cause:** two resolvers disagree — e.g. `/etc/hosts` override vs DNS,
or the VPN resolver flapping, or a stale resolved cache after a change.
**Diagnose:** `getent hosts <name>` vs `dig +short <name>` — if they
differ, you have *two* answers from *two* sources; `resolvectl flush-caches`.
**Fix:** remove the stale override, or flush caches and retest.
**Prevention:** one source of truth per name in lab environments.

## 9. `ss` shows the socket but curl still refuses

**Cause:** address-family or scope mismatch — service on IPv6 only
(`[::]:8000`), or bound to a specific address you're not contacting.
**Diagnose:** read the full `ss` line: `127.0.0.1:8000`,
`[::]:8000`, and `0.0.0.0:8000` are **three different answers**; try
`curl http://[::1]:8000/` explicitly.
**Fix:** bind the service to both stacks or connect to the matching
address.
**Prevention:** quote the *listening line*, not just "the port", in
notes and tickets.

## 10. "The internet is down" (it usually isn't)

**Cause:** almost always one rung, not "the network": portal, VPN, DNS,
or one dead route — while everything else is fine.
**Diagnose the ladder, in order, out loud:** `ip -brief link` →
`ip -brief address` → `ip route` → `resolvectl query www.ubuntu.com`
→ one `curl -sI http://www.ubuntu.com` (or a controlled local target).
**Fix:** whatever rung failed — and *say so* in the ticket: "link up,
address OK, DNS dead" is a fixable report; "internet down" is not.
**Prevention:** the four-command health check (Lab 1 §4) as a
written alias/note; muscle memory beats panic.

## When to escalate

| Evidence | Escalate to |
|---|---|
| Rung 1–3 fail on hardware that used to work | IT / instructor (possible hardware/port issue) |
| Rung 4–5 fail only off-campus | VPN/portal admin |
| Everything local green, one service unreachable | Service owner (with your `ss` + `curl -v` transcript) |
| Repeatedly broken after reboots | Save `ip addr`, `resolvectl status`, `journalctl -u NetworkManager -b` output and attach it |

> Escalating with evidence *is* the skill. A transcript beats a shrug.
