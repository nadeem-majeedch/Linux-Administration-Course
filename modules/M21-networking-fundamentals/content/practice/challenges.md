# Module 21 Challenges — Networking

> Eight challenges. Everything binds to `127.0.0.1`, probes loopback or
> your own VM, and generates no traffic toward external systems. The
> module [safety contract](../README.md) applies to every task.
> Record evidence in `lab-log.md` — a claim without a command output
> isn't an answer here.

## C1 — The address inventory

Produce a three-line inventory of your VM: **one** interface that has a
global (non-loopback) IPv4 address, **one** default gateway, and **one**
DNS server in use. Each line must end with the command that produced it.
Then the twist: which of the three would be *different* on a bridged VM
on the same LAN, and why? (One sentence, [Lesson 2](../lessons/02-ip-and-routing.md) §4.)

## C2 — The sub-minute health check

In **under 60 seconds and four commands**, decide whether a freshly
booted VM has: link up, an address, a route, and working DNS resolution.
Write the four commands in the order you'd type them and the one-word
verdict each must yield for "healthy". (Hint: the ladder from
[Lesson 5](../lessons/05-http-tools-diagnosis.md) collapses into four rungs here.)

## C3 — Loopback multiplexing

Create **three** virtual server names — `a.test`, `b.test`, `c.test` —
that all resolve to distinct `127.x.x.x` addresses, then run three
`python3 -m http.server` instances on port **8080**, each bound to a
different one of those addresses (serve three different directories so
the content proves which is which). Demonstrate with `curl` that all
three names answer on the *same* port. Explain in one sentence why
`127.0.0.1:8080` now serves nothing.

## C4 — The DNS cache probe

Using `dig` only: (a) show that a repeated lookup is served from cache
(compare a field that changes when a query hits the network vs the stub
cache), (b) flush the systemd-resolved cache with `resolvectl`, and
(c) prove the flush worked. Evidence: the two dig outputs side by side
with the changed field highlighted, plus the flush command. (Which
field? [Lesson 3](../lessons/03-dns-resolution.md) §4 — it's in the
footer of dig's output.)

## C5 — Port occupied!

Start a server on port 9090, then (deliberately) start a second one on
the same port and capture the error verbatim. Now diagnose *without
starting anything*: which command shows who owns the port, and what
exact output does it give? Write the one-line answer you'd give a
teammate: "port 9090 is taken by ______, PID ______; kill it with
______ or pick another port." (Rehearse the M18 preview→scope→TERM
ladder before killing anything.)

## C6 — The TIME-WAIT harvest

Run a short loop of `curl -s http://127.0.0.1:8080 >/dev/null` against
your C3 server (say, 20 requests), then immediately: (a) count sockets
in `TIME-WAIT` state, (b) identify *which side* is in TIME-WAIT
(client or server) for loopback connections, and (c) explain why this
is correct and harmless and not a connection leak. (One `ss` filter and
one sentence each; [Lesson 4](../lessons/04-ports-tcp-udp-sockets.md) §6.)

## C7 — Read the resolver's mind

Configure nothing; *observe* everything. Using `resolvectl status` and
`/etc/nsswitch.conf`, produce a two-paragraph description of exactly how
your VM resolves `www.ubuntu.com` right now: which file is checked
first, which resolver address answers, which link owns the query, and
what would change if a VPN link with `Domains=~corp` appeared. (This is
a reading challenge — zero changes, pure evidence.)

## C8 — The five-minute packet diary

With your C3 server running: capture **loopback only**, capped at 40
packets, while making one `curl` request, then answer from the capture:
(a) which TCP flag sequence opens the connection, (b) one line showing
the HTTP request leaving and its reply returning, and (c) the FIN or
RST that closes it. Present three annotated excerpts, not the whole
dump. (`tcpdump -i lo -c 40 -A` is your friend; port filter makes it
readable.)

## Stretch — the interpreter (C9, optional)

Take the whole clinic from [Lab 2](../labs/lab-02-diagnosis-clinic.md)
and compress it into a **single page**: the six-rung ladder as a
flowchart (text arrows are fine), one command per rung, and the one
output fragment that "proves" the rung's verdict. This page becomes
your personal cheatsheet — compare it with
[resources/cheatsheets/](../../../../resources/cheatsheets/) once done.
