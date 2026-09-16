# Lab 1 — Map Your Own Machine: The Network Passport

> Module 21 · Unit 6 · Difficulty: Advanced
> Time: ~45 min · Environment: your own VM/WSL2 — **read-only + two
> local servers you start yourself**
> Prerequisites: Lessons 1–5

You'll produce your machine's complete network passport — every layer,
documented — then run two local services and watch the layers work.
This is the lab to redo on every new machine you ever touch.

## Part A — link & address layers (L1–L2)

```console
$ ip -br link                     # interfaces + state (LOWER_UP?)
$ ip -br a                        # addresses per interface
$ ip neigh show                   # who's on the local wire
```

**Record:** each interface with its state, addresses, and one-line
role (loopback / wired / wireless / docker / VPN…). Flag anything
showing 169.254.x.x (and say what it would mean).

## Part B — route layer (L3)

```console
$ ip route show
$ ip route get 8.8.8.8
$ ip route get 127.0.0.1
$ ping -c3 $(ip route | awk '/default/ {print $3; exit}')    # gateway alive?
$ ping -c3 8.8.8.8 && ping -c3 -n pypi.org                   # note: second does DNS too
```

**Record:** your default gateway, the `route get` decisions (with
source addresses), ping loss/latency per rung — and one sentence on
what the last two pings differ in (`-n` matters — Lesson 3 §6).

## Part C — resolution layer (L3.5)

```console
$ cat /etc/hosts | grep -v "^#"
$ grep hosts /etc/nsswitch.conf
$ resolvectl status | grep -E "DNS Servers|DNS Domain" -A1
$ dig +short pypi.org; dig +short AAAA pypi.org; dig +short mx pypi.org | head -3
$ dig @1.1.1.1 +short pypi.org    # second opinion
$ host $(ip route | awk '/default/ {print $3; exit}')        # reverse lookup
```

**Record:** your resolver chain (files → resolved → DNS), the answers
from both resolvers (agreement?), and whether your gateway has a PTR
record.

## Part D — transport layer (L4): your listening sockets

```console
$ ss -tlnp                        # sudo for full process names
$ ss -ulnp                        # UDP census
$ ss -tan | awk 'NR>1 {print $1}' | sort | uniq -c
```

**Record:** the complete LISTEN table classified by binding
(loopback-only vs world-open) — with a verdict per world-open entry
("SSH: intended" / "why is this here?") — and your state census
numbers.

## Part E — watch the layers work (live services)

Two terminals; everything on loopback:

```console
# Terminal 1: the server
$ mkdir -p ~/www && echo "<h1>lab21</h1>" > ~/www/index.html
$ python3 -m http.server 8000 --bind 127.0.0.1
# Terminal 2: the probes
$ ss -tlnp | grep 8000                        # 1. is it LISTENing, on WHAT binding?
$ curl -s -o /dev/null -w "code=%{http_code} total=%{time_total}s\n" http://127.0.0.1:8000/
$ curl -s -o /dev/null -w "code=%{http_code}\n" http://127.0.0.1:9999/   # refused: why?
$ sudo tcpdump -i lo -n -c 6 port 8000        # 2. watch a request (run, THEN curl in 3rd terminal)
$ nc -zv 127.0.0.1 8000                       # 3. the port probe, confirmed
```

**Record:** the ss binding line, the refused message for :9999 with
your diagnosis (listening? no — *refused vs timeout* vocabulary), and
the tcpdump capture with all three handshake packets labeled.

## Part F — the network passport (deliverable)

One page in `lab-log.md`:

1. **Identity:** hostname, IPs (v4/v6), MAC of the main interface
2. **Routing:** default gateway, one `route get` verdict
3. **Resolution:** resolver chain, your DNS servers, one dig verdict
4. **Sockets:** listening table (classified), state census
5. **Health check:** the four-command check (Lesson 2 §8) — paste and
   verdict
6. **One risk finding:** anything bound wider than it should be, or
   any surprise — written as you'd report it to a sysadmin.

## Done when

- [ ] Parts A–E evidence recorded
- [ ] The refused-vs-timeout distinction demonstrated live
- [ ] The tcpdump handshake captured and labeled
- [ ] The passport written — including the risk finding
