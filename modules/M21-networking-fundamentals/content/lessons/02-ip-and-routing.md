# Lesson 2 — The `ip` Toolkit: Inspecting Your Machine's Network

> Module 21 · Unit 6 · Difficulty: Advanced
> Reading time: ~35 min · Lab: [Lab 1](../labs/lab-01-local-network-lab.md)
> Prerequisites: [Lesson 1](01-networking-fundamentals.md)

> 🟢 Safety: `ip` in this lesson is **read-only** (addr/link/route/
> neigh). Changing addresses/routes is own-VM territory and mostly
> unnecessary — NetworkManager or systemd-networkd owns that job, and
> the course teaches you to *inspect* their results.

---

## 1. One command family to rule them all

Old tutorials show `ifconfig`, `route`, `arp` — the deprecated
net-tools package. The modern, complete replacement is **`ip`**
(iproute2), one binary with subcommands:

| Net-tools (legacy) | iproute2 (modern) | Question answered |
|---|---|---|
| `ifconfig` | `ip addr` / `ip a` | what addresses do I have? |
| `ifconfig eth0` | `ip link show dev eth0` | is the interface up? |
| `route -n` | `ip route` | how do packets leave? |
| `arp -a` | `ip neigh` | who's on my local wire? |

Course rule: **learn `ip`; read ifconfig on sight** (you'll meet it in
older docs and embedded systems).

---

## 2. ip addr: the full interface picture

```console
$ ip -br a                      # brief — the quick view
lo        UNKNOWN        127.0.0.1/8 ::1/128
enp3s0    UP             192.168.1.42/24 fe80::9c2a:70ff:fe12:3456/64
$ ip addr show dev enp3s0       # full detail on one interface
2: enp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP ...
    link/ether b4:2e:99:3a:7f:01
    inet 192.168.1.42/24 brd 192.168.1.255 scope global dynamic noprefixroute
       valid_lft 85996sec preferred_lft 85996sec
    inet6 fe80::9c2a:70ff:fe12:3456/64 scope link
```

Reading the flags line — `<BROADCAST,MULTICAST,UP,LOWER_UP>` — the two
that matter: `UP` (admin state: we enabled it) and `LOWER_UP` (the wire
actually carries a signal). **UP without LOWER_UP = cable unplugged /
wifi disconnected** — the L1 diagnosis that precedes everything else.

`dynamic` + `valid_lft` = this address came from DHCP and has a lease
(Lesson 1 §5). `scope global` vs `scope link` = routable vs
this-segment-only (the IPv6 story from Lesson 1 §4).

---

## 3. ip route: the decision table

```console
$ ip route show
default via 192.168.1.1 dev enp3s0 proto dhcp metric 100
192.168.1.0/24 dev enp3s0 proto kernel scope link src 192.168.1.42
$ ip route get 8.8.8.8          # ASK the kernel: which path for this destination?
8.8.8.8 via 192.168.1.1 dev enp3s0 src 192.168.1.42 metric 100
$ ip route get 192.168.1.7      # ...and for a local one
192.168.1.7 dev enp3s0 src 192.168.1.42
```

`ip route get <destination>` is the diagnostic gem: it asks the kernel
to *simulate* the routing decision and report the chosen interface,
gateway, and source address. Half of "why can't I reach X" is answered
here — wrong interface, no route, or an unexpected source address (VPN
split-tunnel quirks show up instantly).

Multiple routes and metrics: when two interfaces could reach the same
destination, **metric** breaks the tie (lower wins). VPN clients and
docker bridges add routes with metrics — reading `ip route` after
connecting a VPN explains the "why is my traffic going there?" puzzles.

---

## 4. ip neigh: the local wire census

```console
$ ip neigh show
192.168.1.1 dev enp3s0 lladdr a4:2b:b0:1d:2e:f0 REACHABLE
192.168.1.30 dev enp3s0 lladdr dc:a6:32:11:22:33 STALE
```

The **neighbor table** (ARP/NDP) maps local IPs → MACs. `REACHABLE`
 = recently talked to; `FAILED` = the host stopped answering (a quick
"machine left the network" signal for local diagnosis). Concept only —
`ip neigh` is L2 plumbing you'll read more than manage.

---

## 5. ping: is the path alive? (and what silence means)

```console
$ ping -c 3 192.168.1.1              # the gateway first, always
PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=2.31 ms
...
--- 192.168.1.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max = 2.31/2.55/2.90 ms
```

Read three numbers: **loss** (0% expected locally; >2% is a story),
**time** (latency — compare to baseline: campus LAN ~1–3 ms, same
country ~10–30 ms, intercontinental ~100–200 ms), and **ttl**
(diminishing per router hop; 64→57 means ~7 hops — the poor man's
traceroute).

`ping` uses **ICMP**, not TCP — so "ping works but the port is closed"
and "ping fails but the port works" are *both normal*: many hosts and
networks drop ICMP. Silence from ping is a hint, never a verdict — the
layered playbook (Lesson 5) exists because of exactly this.

```console
$ ping -c 3 -6 host.example.edu      # IPv6 variant
$ ping -c 3 127.0.0.1                # sanity: does MY stack work at all?
```

---

## 6. traceroute/tracepath: the path between

```console
$ tracepath -n 8.8.8.8 | head -6      # no root needed (vs traceroute's UDP/ICMP modes)
 1?: [LOCALHOST]                      pmtu 1500
 1:  192.168.1.1                        2.2ms
 2:  10.10.0.1                          9.8ms       ← ISP/campus edge
 3:  72.14.194.97                      10.9ms       ← provider backbone
```

Each line = one router hop, by decrementing TTL (Lesson 1: the same
TTL you read in ping). `tracepath` needs no privileges — the course
default; `traceroute -I` (ICMP mode) sometimes succeeds where the
default UDP probes are filtered; `-n` skips reverse-DNS (faster,
cleaner). Asterisks = a router dropping probes (often deliberate —
not automatically a failure; watch where latency *jumps* instead).

**DS use:** "the cluster is slow today" → tracepath to the cluster's
login node; a latency jump at hop 3 vs hop 12 tells you whether the
problem is your campus edge or the far internet. Pair with ping's
latency for the before/after story.

---

## 7. hostname: the names a machine answers to

```console
$ hostname                 # the kernel's name for this machine
labvm
$ hostname -f              # FQDN (fully qualified) if resolvable
$ hostname -I              # all this machine's IPs — the "which IP do I give out?" command
192.168.1.42
```

`hostname -I` is the practical one: before SSHing into your VM (M22)
or connecting a classmate to your local Jupyter, this is how you learn
what address to use. (Hostname *resolution* — how a name becomes an IP
— is Lesson 3's entire subject.)

---

## 8. The read-only network health check (assembling)

The Lesson-5 playbook needs a foundation check — four commands, in
order, each answering one layer:

```console
$ ip -br a                 # L3: addresses present? (no 169.254 = DHCP healthy)
$ ip route                 # L3: default route exists?
$ ping -c 3 <gateway>      # L2/L3: is the next hop alive?
$ ping -c 3 8.8.8.8        # L3: does the internet respond? (ICMP-permitting)
```

DNS and ports come next (Lessons 3–4). This quartet already localizes
the failure: no address = DHCP/link; address but no route = config;
route but gateway silent = local net; gateway fine but internet silent
= upstream or ICMP filtering. Lab 1 drills it; Lab 2 breaks it.

---

## Exercises (lab-log.md)

1. `ip -br a` vs `ip addr show dev <iface>` for your main interface —
   annotate flags, scopes, and lease times. Is your address dynamic?
2. `ip route get` for: your gateway, a public IP, and your own
   machine's own IP. Three outputs, one sentence each on what the
   kernel chose and why.
3. ping ladder: 127.0.0.1 → gateway → a public IP. Record loss/latency
   at each rung. Where does latency jump, and what does that tell you?
4. `tracepath -n <a public host>`: how many hops? Where's the biggest
   latency jump? (No external *scanning* — one tracepath is
   observation, not probing; keep it to one or two runs.)
5. Your VPN adds a route. After connecting one (or reading
   documentation), what changed in `ip route`? Predict before you look
   which line wins for 10.0.0.0/8 destinations.
6. Explain to a teammate why `ping` failing against a working web
   server proves nothing. (Two sentences: ICMP vs TCP + filtering.)

## Check yourself before Lesson 3

- [ ] I use `ip addr/link/route/neigh` and can read flags/scopes.
- [ ] `ip route get` is my "which path?" oracle.
- [ ] I read ping's loss/latency/ttl — and never treat ICMP silence as
      proof.
- [ ] The four-command health check is in my notes.

## Further reading (official sources)

- `man ip`, `man ping`, `man tracepath` (iproute2; iputils:
  https://github.com/iputils/iputils)
- Ubuntu Server Docs — networking config (NetworkManager /
  systemd-networkd): https://ubuntu.com/server/docs
- kernel route docs: https://docs.kernel.org/networking/
