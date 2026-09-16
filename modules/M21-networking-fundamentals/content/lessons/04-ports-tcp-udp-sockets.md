# Lesson 4 — TCP, UDP, Ports & Sockets: Reading `ss`

> Module 21 · Unit 6 · Difficulty: Advanced
> Reading time: ~35 min · Lab: [Lab 2 — the diagnosis clinic](../labs/lab-02-diagnosis-clinic.md)
> Prerequisites: [Lesson 2](02-ip-and-routing.md)

> 🟢 Safety: `ss` observes *your* machine. The lab's client/server
> experiments bind to **localhost only**. Port-scanning other hosts is
> against the course contract (and most employers') — don't.

---

## 1. Ports: addressing *within* a machine

An IP delivers a packet to a machine; a **port** delivers it to a
*program* on that machine. One number, 0–65535, per protocol family:

- **0–1023** — privileged (well-known): 22 SSH, 80 HTTP, 443 HTTPS,
  53 DNS, 5432↔ (Postgres is 5432 but unprivileged — the lists overlap)
- **1024–49151** — registered: 3306 MySQL, 8080 alt-HTTP, 8888
  **Jupyter's default**
- **49152–65535** — ephemeral: the OS grabs these for *outgoing*
  connections

Memorize the working half-dozen: **22/80/443/53/8888/8000** — SSH, web,
web-secure, DNS, your notebook, your dev API. (M29 uses 80/443/5432;
M22 tunnels 8888.)

**Sockets** are the endpoints themselves: a *local* socket is
`IP:port` on this machine; a *connection* is the pair
`(local IP:port, remote IP:port)`. One listening port, thousands of
concurrent connections — the 4-tuple distinguishes them.

---

## 2. TCP vs UDP: two contracts

| | **TCP** | **UDP** |
|---|---|---|
| Contract | ordered, reliable, connection-oriented | fire-and-forget, connectionless |
| Setup | 3-way handshake (SYN, SYN-ACK, ACK) | none |
| Overhead | more (acknowledgments, retransmits) | minimal |
| You meet it | SSH, HTTP/S, git, databases, Jupyter | DNS queries, video streams, telemetry |

The handshake matters operationally: every TCP connection you see in
`ss` went through SYN → SYN-ACK → ACK, and a failed connect shows its
failure mode in that vocabulary (§5's states). UDP has no handshake —
a UDP "port open" tells you almost nothing (which is why DNS diagnosis
uses dig, not port checks).

**DS translation:** training data over NFS, notebooks over HTTP,
checkpoints to object storage — TCP, because bytes must arrive
*exactly once, in order*. Sensor telemetry (M08's sensor-telemetry.tsv
is exactly this) — often UDP, because a dropped packet is older news
than the next one.

---

## 3. ss: the socket census

`ss` (socket statistics — netstat's modern replacement) lists every
socket:

```console
$ ss -tlnp
State   Recv-Q  Send-Q  Local Address:Port   Peer Address:Port   Process
LISTEN  0       4096        127.0.0.1:631        0.0.0.0:*      users:(("cupsd",pid=912))
LISTEN  0       4096        0.0.0.0:22           0.0.0.0:*      users:(("sshd",pid=845))
LISTEN  0       4096             [::]:22              [::]:*      users:(("sshd",pid=845))
```

Decode the flag bundle first: `-t` TCP, `-l` listening, `-n` numeric
(no DNS! — Lesson 3's lesson applied), `-p` process names (sudo for
other users' processes), `-u` UDP, `-a` all (adds established).

**The security-relevant column: Local Address.**

- `127.0.0.1:8888` — bound to **loopback**: only this machine can
  reach it. Correct default for dev servers.
- `0.0.0.0:22` — bound to **all IPv4 interfaces**: the world can knock
  (firewall permitting — M25). Correct for SSH; scandalous for a
  dev database.
- `[::]:22` — the IPv6 twin (often dual-stack for the same service).

Lesson 1 promised this question; here is the answer pattern: **"is my
notebook listening on loopback or all interfaces?" = read the Local
Address column.** A data-exfiltration incident report starts with
`0.0.0.0:8888` more often than anyone admits.

---

## 4. Connections: the ESTABLISHED view

```console
$ ss -tn state established
Recv-Q   Send-Q   Local Address:Port    Peer Address:Port
0        0        192.168.1.42:44812    140.82.121.4:443      ← my git push, mid-flight
0        0        192.168.1.42:ssh      192.168.1.7:52344     ← someone SSHed IN
```

This is the machine's *live conversation list*. The DS moment: "what
is my training script actually talking to?" — `ss -tnp | grep python`
answers with remote IP:port; add `host <ip>` (Lesson 3 §4) for the
reverse name.

**Recv-Q/Send-Q:** bytes received-but-unread / sent-but-unacked.
Persistently non-zero Send-Q on a slow link = the remote side can't
keep up (or the link can't); Recv-Q filling = *your* process isn't
reading fast enough (a stalled Jupyter kernel shows exactly this).

---

## 5. Connection states (reading the lifecycle)

TCP states you'll actually see in `ss -tan`:

| State | Meaning |
|---|---|
| `LISTEN` | server waiting for connections |
| `ESTABLISHED` | the conversation is live |
| `TIME-WAIT` | *we* closed first; lingering to catch late packets (normal, ~60s, numerous) |
| `CLOSE-WAIT` | **the other side closed; our app hasn't** — a pile of these = a leaked-connection bug |
| `SYN-SENT` | we sent SYN, no answer yet — the remote is down/filtered |

Two diagnostic gems:

- **Many CLOSE-WAIT** = your code forgot to close connections (the
  requests-without-session-leak pattern). The fix is in *your* Python.
- **SYN-SENT then timeout** = the port is unreachable: remote down,
  firewalled, or wrong port — the handshake's first step never
  completed. This is precisely what "connection refused vs timed out"
  (Lesson 5) distinguishes.

```console
$ ss -tan | awk 'NR>1 {print $1}' | sort | uniq -c    # the state census
     12 LISTEN
      4 ESTAB
     18 TIME-WAIT
      3 CLOSE-WAIT      ← if this grows, look at your code
```

---

## 6. curl's port check (the honest one-port probe)

`nc` gets the reputation; for TCP "is this port accepting?" curl is
clearer and already everywhere:

```console
$ curl -sS --connect-timeout 3 -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/
000            ← connected to nothing (or: 200 = answered!)
$ curl -v telnet://127.0.0.1:8000 </dev/null 2>&1 | grep -i connected
Connection refused          ← the machine IS up, nothing LISTENS there
```

**Refused vs timed out — the distinction that halves diagnosis time:**

- **Connection refused** = your packet reached the machine; *nothing is
  listening on that port* (RST came back). Fix: start the service /
  check the port number.
- **Timed out** = no answer at all: host down, firewalled (drop), or
  routing broken. Fix: earlier ladder steps (link → route → remote
  firewall).

nc completes the picture (conceptual, per the syllabus):

```console
$ nc -zv 127.0.0.1 8000       # -z: scan-mode connect only; -v: say it
Connection to 127.0.0.1 8000 port [tcp/*] succeeded!
$ nc -l 9000                  # tiny server: listens, echoes what arrives (localhost labs only)
```

Lab 2 uses both against *your own* listeners — never against other
hosts.

---

## Exercises (lab-log.md)

1. `ss -tlnp`: list every listening socket with its binding. Which
   are loopback-only, which are world-open (`0.0.0.0`/`[::]`)? For
   each world-open: what service, and should it be?
2. The state census pipeline (§5). Report your counts and interpret
   any CLOSE-WAIT above zero (which process owns them? `-p` it).
3. Start `python3 -m http.server 8000 --bind 127.0.0.1`; curl it; then
   `curl -v telnet://127.0.0.1:9999` — capture the *refused* message.
   Now kill the server and curl :8000 — *still* refused. Write the
   one-sentence diagnosis for each case.
4. `ss -tnp` during a `git fetch`: what remote IP:443 connection
   appears? Reverse-lookup the IP. (The machine's conversation list,
   caught live.)
5. Why does `ss -tln` (no -n) sometimes *hang or misname* entries?
   (Hint: what does it do that -n skips — and which lesson taught
   that?)
6. (Stretch) UDP sockets: `ss -ulnp`. Why are there almost no
   "connections" (hint: no handshake)? Find the DNS listener on
   127.0.0.53 — what daemon owns it? (Lesson 3's resolver, met again.)

## Check yourself before Lesson 5

- [ ] Ports: ranges, my working six, ephemeral vs listening.
- [ ] TCP vs UDP in one sentence each, with a DS example of each.
- [ ] I read Local Address bindings as a security statement.
- [ ] Refused vs timed out — I can name both failure modes on sight.

## Further reading (official sources)

- `man ss` (iproute2), `man 7 socket`, `man nc`
- kernel docs — TCP states: https://docs.kernel.org/networking/
- IANA service name/port registry: https://www.iana.org/assignments/service-names-port-numbers/
