# Module 21 Quiz — Answer Key

> Grading guide: A/B are factual; C/D accept any wording that
> demonstrates the *reasoning*. Command answers are graded on "would it
> work if typed", not on matching this exact form.

## Section A — Fundamentals

**A1.** The **IP address changes** (DHCP assigns per-network); the MAC
usually stays — it's burned into the NIC/virtual adapter. MAC gets you
onto the local link; IP is what routes across networks.

**A2.** `/24` ⇔ `255.255.255.0` → 254 usable host addresses
(256 minus the network and broadcast addresses).

**A3.** `lo` on `127.0.0.1`; the whole `127.0.0.0/8` range is loopback,
so **yes, 127.0.0.2 is valid loopback** (a common trick: multiple local
services on distinct 127.x addresses).

**A4.** The **default gateway**. Learned from the routing table —
`default via …` in `ip route`, installed by DHCP on DHCP-managed links.

**A5.** Downward: **TCP socket → IP header → router → NIC (MAC frame)**.
(Encapsulation: payload wrapped by TCP, then IP, then a MAC frame per
hop; routers strip/rebuild the frame, not the IP header.)

**A6.** TCP: ordered, reliable, connection-oriented. UDP: fast,
connectionless, no delivery guarantee. Course pairings: **SSH (TCP)**,
**DNS lookups (UDP)**; Jupyter's HTTP/WebSocket is TCP.

## Section B — the `ip` toolkit

**B7.** `ip -brief address` — interfaces, link state, addresses in one
compact view.

**B8.** No frames will be sent or received on that interface —
connectivity via it is impossible regardless of addressing. First thing
to fix (link/`ip link set dev X up`), before anything else.

**B9.** The **default gateway** — the router this host forwards
all off-subnet traffic to.

**B10.** NAT (e.g. 10.0.2.x in VirtualBox/QEMU): the guest is behind
the host's private translation; the LAN sees only the host's IP, and
there is **no inbound route** to 10.0.2.15. (Bridged mode or port
forwarding would expose the guest.)

**B11.** Table: `ip neigh` (or `ip neighbour`). Hostname overrides:
`/etc/hosts`.

## Section C — DNS

**C12.** `hosts`, then `dns` — configured in `/etc/nsswitch.conf`.
(The full chain may include `resolve [!UNAVAIL=return]` and `files`:
`files` = `/etc/hosts` first, then the resolver.)

**C13.** The **systemd-resolved stub listener** (local caching resolver
every Ubuntu resolver points to). Speed comes from its **cache** —
repeat queries don't leave the machine.

**C14.** `A` → IPv4 · `AAAA` → IPv6 · `CNAME` → alias (e.g. `www` →
the main name).

**C15.** It proves the failure is **which resolver is being used**, not
the record itself: the default path can't reach/split-route to the
corporate namespace. `systemd-resolved`'s **per-domain routing** (domains
pinned to specific resolvers, e.g. via `Domains=` on the VPN interface)
fixes exactly this. Quick check: `resolvectl status` — see which link
claims `~corp`.

**C16.** (1) `nslookup` **doesn't consult `/etc/hosts` or nsswitch** —
it's raw DNS, so its answers can contradict what apps actually get;
(2) it ignores systemd-resolved's split-DNS and gives a different view
of "the answer" than the resolver apps use.

## Section D — Ports & sockets

**D17.** 45000 falls **inside the default ephemeral range**
(32768–60999): at any moment the OS may hand that exact port to an
outbound connection, and your server would fail to bind — a
probabilistic, maddening failure. Pick outside the range (e.g. 8888,
9443) or reserve it.

**D18.** `ss -tlnp`. You need root (or the socket's owner) to see the
process name for sockets owned by other users — `sudo ss -tlnp`.

**D19.** `LISTEN` = accepting connections on that port; `ESTAB` =
established, live connection; `TIME-WAIT` = closed from our side, in
the timeout that guarantees the peer's final packets drain. A busy
*client* shows **lots of TIME-WAIT, correctly** — it's the normal end
of short-lived connections, not an error.

**D20.** Refused on 127.0.0.1 → **nothing is listening on that
port/address** (service dead or bound elsewhere). Confirm:
`ss -tlnp 'sport = :8000'`. Timeout on 10.0.2.15 from another VM → the
NAT guest's address isn't reachable inbound (no route/forwarding) — a
different disease than refused.

**D21.** **`-i lo`** — loopback only — and `-c 20` (or `-c 50`) to cap
the packet count so output stays digestible while learning. Nothing
against external hosts, ever.

**D22.** E.g.: **link rung** — `ip -brief link` (is the interface even
up?); **port/service rung** — `ss -tlnp` on the target (is anything
listening at all?). Any two of: interface state, addresses, routes,
DNS, the specific service's port. "Network down" is a claim, not a
diagnosis — the ladder produces the diagnosis.

## Score guide

| Score | Meaning |
|---|---|
| 19–22 | Command reflexes are in place — move to M22 |
| 14–18 | Re-read the flagged lesson sections, redo the relevant lab drill |
| < 14 | Repeat lessons 2–5, then retake — networking compounds |
