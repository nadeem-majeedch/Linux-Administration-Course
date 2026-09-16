# Lesson 1 — Networking Fundamentals: Addresses, Layers & Routing

> Module 21 · Unit 6 · Difficulty: Advanced
> Reading time: ~40 min · Lab: [Lab 1 — the local network lab](../labs/lab-01-local-network-lab.md)
> Up next: [Lesson 2 — the ip toolkit](02-ip-and-routing.md)

> 🟢 Safety: this lesson is concepts + read-only observation of *your
> own* machine. The course-wide rule bears repeating: **no probing or
> scanning of external systems** — every exercise here is localhost or
> your own VM.

---

## 1. Why a data scientist needs this module

Every remote thing you touch is networking: `git pull` (DNS + TCP 443),
`pip install` (a package mirror), `jupyter lab` (a listening socket),
`pd.read_sql('postgres://…')` (TCP 5432), `requests.get(api)` (DNS →
TCP → HTTP). When one fails, the error message rarely says *why* — this
module gives you the layered diagnosis that turns "ConnectionError"
into "your DNS is fine, the port is closed."

The organizing idea, borrowed from every network textbook but kept
practical:

```text
L2 link      — MAC addresses, the local wire         (same network only)
L3 internet  — IP addresses, routing between nets    (the internet layer)
L4 transport — TCP/UDP ports, connections            (who gets which stream)
L5+ app      — HTTP, SSH, DNS protocols              (what the bytes mean)
```

Diagnosis always walks this ladder bottom-up: *link* → *IP* → *port* →
*application*. Lesson 5 turns it into the playbook; every lab drills it.

---

## 2. MAC addresses: the local wire's identity

Every network interface has a **MAC address** — 48 bits, written as six
hex pairs (`b4:2e:99:3a:7f:01`), burned in by the manufacturer and used
*only* on the local network segment. Routers strip Layer-2 framing as
they forward — your MAC never crosses the internet; your IP does.

```console
$ ip link show
2: wlp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 ...
    link/ether b4:2e:99:3a:7f:01 brd ff:ff:ff:ff:ff:ff
```

Know it for: identifying interfaces in logs/dhcp leases, and the
`link/ether` line meaning "this is the Layer-2 identity of interface
2." That's all a working admin needs daily.

---

## 3. IPv4: addresses, masks, subnets

An IPv4 address is 32 bits, written as four octets: `192.168.1.42`.
The **subnet mask** splits it into a *network* part and a *host* part —
modern notation collapses both into **CIDR**: `/24` means "the first
24 bits are the network."

```text
192.168.1.42/24
└── network: 192.168.1.0    host range: 192.168.1.1 – .254
    broadcast: 192.168.1.255 (everyone on the subnet, at once)
```

The three CIDRs you must compute fluently:

| CIDR | Mask | Hosts | You meet it as |
|---|---|---|---|
| /24 | 255.255.255.0 | 254 | home/office LANs |
| /16 | 255.255.0.0 | 65,534 | big private nets (10.0.0.0/16) |
| /32 | single host | 1 | firewall rules, host routes |

**Private ranges** (RFC 1918) never route on the public internet —
your VM, home, and campus use these; the cloud NATs them outbound:

```text
10.0.0.0/8          172.16.0.0/12          192.168.0.0/16
```

Plus two special addresses: `127.0.0.1` (**loopback** — "this machine
itself"; §6) and `169.254.x.x` (**link-local** — DHCP failed; seeing
this on an interface *is* a diagnosis).

### The arithmetic drill (30 seconds, done mentally)

"Is 10.0.5.23 in 10.0.0.0/16?" — first 16 bits: `10.0` vs `10.0` → yes.
"Is 10.1.5.23 in 10.0.0.0/16?" — second octet differs → no, it needs a
router. That question shape ("same subnet or do I need the gateway?")
is half of all network diagnosis.

---

## 4. IPv6: recognition level

IPv6: 128 bits, eight hex groups (`2001:db8::8a2e:370:7334`), invented
because 32 bits ran out. You need *recognition*, not mastery:

```console
$ ip -6 addr show | head -5
    inet6 fe80::9c2a:70ff:fe12:3456/64 scope link      ← link-local (every interface has one)
    inet6 2001:db8:1234:5678::1000/128 scope global    ← a real global address
```

The working facts: `fe80::/10` is link-local (never routed — the IPv6
of "this cable only"); `::1` is IPv6 loopback; a host typically has
several IPv6 addresses at once (privacy extensions rotate one); and
`ping -6`, `dig AAAA` are the v6 variants of tools you already know.
When a connection is flaky-v4-but-fine-v6 (or vice versa), "happy
eyeballs" is the name of the dual-stack race your apps are running —
recognizing the symptom is the deliverable here.

---

## 5. Interfaces, gateways & routing

An **interface** is the OS's name for a network attachment point:
`eth0`/`enp3s0` (wired), `wlp3s0` (wifi), `lo` (loopback), `docker0`,
`veth…` (containers — M28's world), `tun0` (VPN). Linux is *proud* of
its interfaces and will show you all of them (Lab 1 maps yours).

**The gateway** is the router on your subnet that forwards traffic
destined *elsewhere*. Your machine's routing table answers the only
question routing ever asks:

```console
$ ip route
default via 192.168.1.1 dev wlp3s0 proto dhcp metric 600
192.168.1.0/24 dev wlp3s0 proto kernel scope link src 192.168.1.42
```

Read it as a decision list, **most-specific match wins**:

1. "Destination 192.168.1.x?" → directly on `wlp3s0` (same subnet — no
   router; that's why the ARP/MAC world exists).
2. "Anything else?" → `default`: hand to 192.168.1.1 (the gateway) and
   trust it onward.

Every "the internet is down" incident reduces to auditing these two
lines: do I have a route to the destination, and is the gateway alive?

### DHCP: how addresses arrive

**DHCP** is how interfaces *get* their IP/gateway/DNS automatically —
`proto dhcp` in the route above is its signature. The DORA dance
(Discover, Offer, Request, Acknowledge) is worth knowing by name; the
operational facts: no DHCP → typically a `169.254.x.x` link-local
address (§3's diagnostic), and on university networks DHCP also hands
out the campus DNS servers (Lesson 3's resolvers).

---

## 6. localhost & loopback: your own machine as a network host

`lo` is a virtual interface for the machine to talk to itself; the
whole `127.0.0.0/8` block routes to it (127.0.0.1 by convention).
Applications use it constantly: a local database, `jupyter lab`'s
default server (127.0.0.1:8888), a dev API on :8000.

Two facts with teeth:

- **Loopback traffic never touches the wire** — it can't be sniffed
  from outside, needs no firewall path, and is why local services work
  with the network cable unplugged.
- **Bound-to-127.0.0.1 means private.** A service listening only on
  loopback is unreachable from other machines *by design* — which is
  the correct default for a Jupyter server until you deliberately
  tunnel it (M22's SSH forwarding does exactly that). "Is my notebook
  listening on loopback or all interfaces?" is a security question
  with this lesson's answer.

```console
$ ss -tlnp | grep 8888          # (Lesson 4's tool, previewed)
LISTEN 0 5 127.0.0.1:8888 ...   ← loopback-only: private by design
```

---

## Exercises (lab-log.md)

1. `ip link show` — list your interfaces with their MACs. Which is
   loopback, which is your real network, and what are the rest?
2. `ip route`: state your default gateway and subnet. Then answer:
   is 192.168.1.200 (adjust to your subnet) reachable *without* the
   gateway? Why?
3. Compute: how many hosts in a /26? Write the host range for
   192.168.1.64/26. (Drill until it's 30 seconds.)
4. `ip -6 addr`: identify one link-local and (if present) one global
   IPv6 on your machine. Which one would survive moving to another
   network, and why not the other?
5. Why does a machine with no DHCP lease show 169.254.x.x? What is
   that address *for*, one sentence?
6. (Stretch) `python3 -m http.server 8000 --bind 127.0.0.1` in one
   terminal; from another, `curl -s http://127.0.0.1:8000/ -o /dev/null
   -w "%{http_code}\n"`. Then reason (don't run): what would a
   classmate's laptop need to reach this server? What did
   `--bind 127.0.0.1` change?

## Check yourself before Lesson 2

- [ ] I can walk the L2→L3→L4→app ladder and say what each layer adds.
- [ ] CIDR arithmetic for /24 /16 /32 (and /26 under pressure).
- [ ] I read `ip route` as a decision list, most-specific first.
- [ ] I know what 127.0.0.1, 169.254.x.x, and fe80:: each *mean*.

## Further reading (official sources)

- `man ip` (iproute2: https://wiki.linuxfoundation.org/networking/iproute2)
- RFC 1918 (private address space): https://datatracker.ietf.org/doc/html/rfc1918
- kernel networking docs: https://docs.kernel.org/networking/
- Ubuntu Server Docs — networking: https://ubuntu.com/server/docs
