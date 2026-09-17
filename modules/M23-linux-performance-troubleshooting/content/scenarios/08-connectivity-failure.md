# Drill Card 8 — "Network Connectivity Failure"

> Scenario family: Network · Difficulty: ●●○
> Source modules: [M21 lessons 1–2, 5](../../../M21-networking-fundamentals/content/README.md) — this card *is* the six-rung ladder, operationalized

## Symptom

`curl: (7) Failed to connect`, ssh times out, `git clone` hangs at
connect — the app-level refusal that hides a layer question.

## Decision tree (the six rungs, compressed)

```text
1 link     → ip -br link          (eth0 UP?)
2 IP       → ip -br addr          (address present? ping the gateway)
3 route    → ip route             (default via … exists?)
4 DNS      → dig +short           (name resolves? — else card 7)
5 port     → ss -tlnp | grep 8888 (server even listening? WHERE?)
6 app      → curl -v / ssh -v     (the verbose layer: exact refusal text)
```

## Evidence

```console
$ ip -br link && ip -br addr && ip route     # rungs 1–3 in one breath
$ ping -c 3 $(ip route | awk '/default/{print $3; exit}')   # gateway reachable?
$ ss -tlnp | grep <port>                      # rung 5 — listener, and bound WHERE?
$ curl -sv http://127.0.0.1:8888 -o /dev/null 2>&1 | tail -5   # rung 6's verdict
$ ping -c 3 1.1.1.1                           # beyond the gateway? (scope test)
```

The **bind-scope check** is this card's signature move (M21 Lab 2's
incident #3): server listening on `127.0.0.1:8888` while the client
knocks on `<vm-ip>:8888` is not "the network is down" — it's a
loopback-bound service, and the fix is the tunnel (M22/M27 posture),
not a firewall change. Read `ss`'s address column *first*.

## Fix pattern

- **Rung 1–2** (link down, no address): VM network mode (NAT vs
  bridged — M21 §2's DHCP discussion), provider reconnect. These are
  yours in a lab VM, an admin's elsewhere.
- **Rung 3** (no default route): DHCP didn't deliver or the interface
  didn't come up — restart the network provider, re-check.
- **Rung 5** (nothing listening): the *service* is the incident —
  card 6, not this card. The referral is the fix.
- **Rung 5b** (listening, wrong scope): bind the service properly or
  tunnel — never "open it to 0.0.0.0" reflexively (M25's posture).
- **Firewall**: `sudo ufw status` — a default-deny that lost its allow
  rule is a two-minute fix with a two-second undo (`ufw allow from …
  to any port 22 proto tcp`).

## Verify

The *client's* original command succeeds — and from the original
client, not the server's localhost (that's card 12's lesson).
Re-run the six-rung sweep as the before/after artifact.

## Document

Name the *rung* where it broke — that's the root-cause vocabulary:
*"dead at rung 5: listener bound to loopback only"*, *"rung 3: no
default route after provider restart"*. A card that names rungs
teaches; a card that says "network was down" doesn't.

**Done when:** you can walk all six rungs from memory on a live VM,
and place three of the course's past incidents onto their rungs.
