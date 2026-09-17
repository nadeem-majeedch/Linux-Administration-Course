# 8 — Networking

> Learn it: [M21 — Networking Fundamentals](../modules/M21-networking-fundamentals/content/README.md) ·
> Lookup, not understanding.

## Interfaces & addresses

| Command | Purpose | Examples |
|---|---|---|
| `ip a` / `ip addr` | addresses per interface | `ip -4 a show eth0` |
| `ip link` | interface state (UP/DOWN) | `ip -s link` adds counters |
| `ip r` / `ip route` | routing table | find the default gateway line |
| `hostname` / `hostname -f` | machine's name / FQDN | — |
| `resolvectl status` | DNS servers in use (systemd-resolved) | `resolvectl query NAME` |

Concepts: **MAC** = hardware address of the NIC (local link only) ·
**IPv4/IPv6** = routable address (changes per network via DHCP) ·
**/NN** = prefix length (`/24` = 254 usable hosts) · **gateway** =
the door off this network.

## Reachability

| Command | Purpose | Key options | Example |
|---|---|---|---|
| `ping` | is it up (ICMP) | `-c N` stop after N · `-i` interval | `ping -c3 example.edu` |
| `ping IP` vs `ping NAME` | splits routing vs DNS failure | — | name fails + IP works ⇒ DNS problem |
| `tracepath HOST` | path to host (no root) | — | `tracepath example.edu` |
| `traceroute HOST` | same, UDP/ICMP variants | `-I` ICMP mode | — |
| `mtr HOST` | traceroute, live | `-r` report | press `q` to quit |

No reply isn't proof of death — firewalls commonly drop ICMP; test
the actual service too.

## Ports & sockets

| Command | Purpose | Key options | Example |
|---|---|---|---|
| `ss -tlnp` | **listening** TCP sockets + owning process | `-t` tcp · `-u` udp · `-l` listen · `-n` numeric · `-p` process | `ss -tlnp \| grep 8888` |
| `ss -tan` | all connections | state column: ESTAB, TIME-WAIT, LISTEN | count ESTAB per peer |
| `nc -zv HOST PORT` | port probe | `-z` scan, `-v` verbose | `nc -zv localhost 8000` |

Read `ss` like this: nothing listening + "connection refused" ⇒
service down; listening on `127.0.0.1` only ⇒ unreachable from
other machines (fix bind address); listening on `0.0.0.0` + refused
remotely ⇒ firewall.

## DNS

| Command | Purpose | Example |
|---|---|---|
| `dig NAME` | full resolution answer | `dig +short NAME` for just the record |
| `dig NAME A` / `dig NAME AAAA` | specific record type | — |
| `dig -x IP` | reverse lookup | — |
| `host NAME` | compact answer | — |
| `nslookup NAME` | legacy interactive tool | fine for quick checks |

| Record | Maps | Notes |
|---|---|---|
| A / AAAA | name → IPv4 / IPv6 | the workhorses |
| CNAME | name → name | alias |
| MX | domain → mail server | — |
| TXT | free text | SPF/DKIM live here |

## HTTP as a diagnostic tool

| Command | Purpose | Key options | Example |
|---|---|---|---|
| `curl URL` | fetch / probe API | `-I` headers only · `-s` silent · `-o FILE` save · `-L` follow redirects · `-m N` timeout | `curl -I http://localhost:8000/health` |
| `curl -w '%{http_code}'` | status code only | for scripts | — |
| `wget URL` | download (resumes, mirrors) | `-c` continue | `wget https://…/data.tar.gz` |

Status families: `2xx` ok · `3xx` redirect · `4xx` **your** request
(404 no such path, 403 forbidden, 429 slow down) · `5xx` **their**
server (500 error, 502/504 upstream/proxy trouble).

## Diagnostics ladder (low → high)

1. `ip a` — do I have an address? interface UP?
2. `ip r` — is there a default route?
3. `ping -c3 GATEWAY` — does the first hop answer?
4. `ping -c3 IP` — does routing work beyond it?
5. `dig NAME` / `ping NAME` — does *resolution* work?
6. `ss -tlnp` (server) + `nc -zv` (client) — is the service up and
   reachable?
7. `curl -v URL` — does the application answer correctly?

Each rung rules out a layer — climb only as far as the evidence
forces.

##tcpdump in one line

```console
$ sudo tcpdump -i any -nn port 443 -c 20      # first 20 TLS-handshake packets
```
Read-only sniffing on **your own machine/VM**; scanning networks
you don't own is out of bounds everywhere in this course.
