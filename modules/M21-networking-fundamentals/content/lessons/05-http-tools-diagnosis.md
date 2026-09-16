# Lesson 5 — HTTP Tools, Packet Peeks & the Layered Playbook

> Module 21 · Unit 6 · Difficulty: Advanced
> Reading time: ~40 min · Lab: [Lab 2 — the diagnosis clinic](../labs/lab-02-diagnosis-clinic.md)
> Prerequisites: Lessons 1–4

> 🟡 Safety: curl/wget against public APIs is normal client behavior;
> **nc/tcpdump experiments bind to localhost**. Capturing packets on
> shared/campus networks raises policy and privacy issues — do capture
> exercises on your own VM's loopback only, and never tunnel traffic
> that isn't yours through lab experiments.

---

## 1. curl: the HTTP scalpel

curl makes *one request* and shows you everything — the tool for
APIs, health checks, downloads, and diagnosis:

```console
$ curl -I https://pypi.org                 # HEAD: headers only
HTTP/2 200
server: nginx
content-type: text/html; charset=utf-8

$ curl -s https://api.github.com/zen       # GET, quiet body
Keep it logically awesome.
```

The working flag set (memorize these nine):

| Flag | Effect | DS use |
|---|---|---|
| `-I` | HEAD request | health checks without payloads |
| `-s` / `-S` | silent / show errors | scripts (pair them!) |
| `-o FILE` | body to file | `-o /dev/null` = timing-only probe |
| `-w FORMAT` | write-out metrics after | latency/formatting reports |
| `-L` | follow redirects | APIs that 301 |
| `-H 'K: V'` | add a header | auth tokens, content-type |
| `-d 'x=1'` | POST data | API calls, webhooks |
| `--connect-timeout N` | cap the connect phase | fast-fail in scripts |
| `-x PROXY` | go via a proxy | behind campus proxies |

The `-w` one-liner is a transfer probe every script should steal:

```console
$ curl -s -o /dev/null -w "dns=%{time_namelookup}s connect=%{time_connect}s tls=%{time_appconnect}s total=%{time_total}s code=%{http_code}\n" https://pypi.org
dns=0.012s connect=0.091s tls=0.227s total=0.394s code=200
```

Read the phases: DNS slow → Lesson 3's problem; connect slow → L3/L4;
TLS slow → crypto/handshake path; all fast but total slow → the
server itself. **The playbook in one command** — and wget does the
job for plain downloads (`wget URL`, resumes with `-c`) while curl
diagnoses. Same core, different temperament: wget fetches; curl
interrogates.

### APIs from the shell (the DS working set)

```console
$ curl -s https://api.github.com/repos/pandas-dev/pandas | head -20    # JSON body
$ curl -s -H "Accept: application/vnd.github+json" -o /dev/null -w "%{http_code}\n" \
     https://api.github.com/rate_limit          # probe auth/rate state: 200
$ curl -s -d '{"q":"ubuntu"}' -H "Content-Type: application/json" \
     https://httpbin.org/post | head -3         # POST with a body
```

Reading an API interaction = status code (200/301/403/429/500), headers
(rate limits, content-type), body (JSON). When Python's `requests`
fails, the same request through curl shows whether the *request* or
the *code* is broken — curl as the control group.

---

## 2. nc: the raw TCP microscope (concept + two safe uses)

`nc` (netcat) connects TCP/UDP endpoints like a plain pipe. The
syllabus says *conceptually* — the two uses worth internalizing:

```console
# 1. The port probe (Lesson 4 §6): connect-only, honest result
$ nc -zv 127.0.0.1 8000
# 2. The one-packet protocol peek — speak HTTP by hand, loopback only:
$ nc -l 9009 &                    # a listener (this machine only)
$ curl -s http://127.0.0.1:9009/ -d '' >/dev/null   # ...wait — client first:
$ curl -s telnet://127.0.0.1:9009 </dev/null &
$ nc -l 9009 &
$ curl -s http://127.0.0.1:9009/ -o /dev/null
```

What nc *teaches* when you watch its output: HTTP is just text lines
(`GET / HTTP/1.1`, `Host: …`) over a TCP socket — no magic. That
demystification is the payload; real protocol work belongs to curl and
python.

---

## 3. tcpdump: the ten-minute introduction

`tcpdump` captures packets off an interface — the microscope of last
resort. Own-VM, loopback-first:

```console
$ sudo apt install tcpdump                     # if missing (M16 workflow!)
$ python3 -m http.server 8000 --bind 127.0.0.1 &
$ sudo tcpdump -i lo -n -c 8 port 8000         # capture 8 packets on loopback
listening on lo, link-type EN10MB ...
12:01:02.101 IP 127.0.0.1.44812 > 127.0.0.1.8000: Flags [S], seq 1...   ← SYN
12:01:02.101 IP 127.0.0.1.8000 > 127.0.0.1.44812: Flags [S.], seq 1...  ← SYN-ACK
12:01:02.101 IP 127.0.0.1.44812 > 127.0.0.1.8000: Flags [.], ack 1...   ← ACK: handshake!
12:01:02.101 IP 127.0.0.1.44812 > 127.0.0.1.8000: Flags [P.], ... "GET / HTTP/1.1"...
12:01:02.102 IP 127.0.0.1.8000 > 127.0.0.1.44812: Flags [F.]              ← FIN: clean close
```

Reading a capture — the flag vocabulary: `S` SYN, `S.` SYN+ACK, `.`
plain ACK, `P.` push(data), `F.` FIN(close), `R` **RST(refused!)**.
Lesson 4's handshake and refusal, now *visible as packets*.

The filter grammar (BPF) selects what you capture — these five
patterns cover most needs:

```console
$ sudo tcpdump -i lo port 5432                 # just the database traffic
$ sudo tcpdump -i any host 192.168.1.7         # everything to/from one host
$ sudo tcpdump -i lo -w dump.pcap port 8000    # capture to file (Wireshark reads it)
$ sudo tcpdump -i any -n icmp                  # ICMP only (ping, visible!)
```

Ethics/policy reminder (the course contract): capturing on loopback or
your own VM = fine. Capturing other people's traffic on shared
networks = don't; modern networks also encrypt (TLS) so payloads are
opaque anyway — you're reading *patterns*, not passwords, and patterns
are exactly what diagnosis needs.

---

## 4. The layered diagnosis playbook (the module's capstone)

Every network failure is one of five breaks. Walk the ladder in order;
stop at the first layer that fails:

```text
┌────────────────────────────────────────────────────────────────┐
│ 1 LINK    Is the wire up?       ip link  (LOWER_UP?)           │
│ 2 IP      Do I have an address? ip -br a; ip route (default?) │
│ 3 ROUTE   Can I reach the net?  ping -c3 <gateway>; ping 8.8.8.8│
│ 4 DNS     Does the name resolve? dig +short NAME; dig @1.1.1.1 │
│ 5 PORT    Is the service there? curl -v telnet://HOST:PORT    │
│           (refused = listening? timeout = firewalled/down)     │
│ 6 APP     Is the app healthy?   curl -I; status codes; logs    │
└────────────────────────────────────────────────────────────────┘
```

Worked example — "git clone hangs" against a university mirror:

1. `ip link` — LOWER_UP ✓ (not a cable problem)
2. `ip -br a` — address present, no 169.254 ✓ (DHCP fine)
3. `ping -c3 <gw>` 2ms ✓; `ping -c3 8.8.8.8` 30ms ✓ (routing fine)
4. `dig +short gitlab.uni.edu` → **empty**; `dig @1.1.1.1 +short …`
   → empty too → *the name itself is broken (NXDOMAIN)* — it's DNS
   data, not your stack. Fix: ask sysadmin / use the FQDN variant.
5. (Name fixed) `curl -v telnet://gitlab.uni.edu:22` → connected ✓
6. `git clone` works; curl -I on its web UI → 502 → the *application*
   behind the port is down (report to admins with this evidence).

Notice what the ladder did: converted "network is down" into "this
specific record doesn't exist, and separately their web app is 502" —
two precise findings a sysadmin can act on in minutes.

### The DS translation table

| Symptom | Ladder layer | First probe |
|---|---|---|
| `pip install` hangs | 4 (DNS) or 5 (port) | `dig +short pypi.org`; curl phase timing |
| Jupyter unreachable from laptop | 5 (binding!) | `ss -tlnp` grep 8888 → 127.0.0.1 = by design; tunnel it (M22) |
| `pd.read_sql` fails on cluster PG | 5 (port) | `curl -v telnet://dbhost:5432` |
| `git push` stalls | 3/4/5 ladder | the playbook, in order |
| API integration fails in code | 6 (app) or your headers | replay the request with curl -v |
| "Cluster is slow" | 3 (route/latency) | tracepath; compare hop latencies |

---

## Exercises (lab-log.md)

1. curl phase-timing against three hosts (pypi.org, github.com, one
   university host). Which phase dominates each? One sentence each.
2. Reproduce the §3 loopback capture verbatim (http.server + tcpdump
   -i lo). Identify all three handshake packets and the GET line in
   your paste.
3. The playbook, executed: pick *any* failing connection from your
   week (a timeout, a refused API) and run all six rungs. Deliverable:
   the ladder transcript + the one-sentence verdict (which layer,
   which fix).
4. `curl -w` timing on `http://127.0.0.1:8000/` vs a public HTTPS
   host: which phases exist locally that don't remotely, and
   vice versa?
5. nc demystification: run the §2 sequence and capture nc's output —
   paste the raw HTTP request your curl sent. One sentence on what
   this teaches about "the web."
6. (Stretch) `sudo tcpdump -i lo -n icmp` while `ping -c3 127.0.0.1`
   runs in another terminal. How many packets per ping? Why does
   loopback ICMP still "round-trip"?

## Check yourself before Lab 2

- [ ] curl's phase timing maps a problem onto the ladder.
- [ ] I've *seen* SYN/SYN-ACK/ACK and RST in a capture.
- [ ] The six-rung playbook is written in my own words.
- [ ] I know the capture policy boundary (loopback/own VM only).

## Further reading (official sources)

- `man curl` (https://curl.se/docs/), `man wget`, `man nc`,
  `man tcpdump` (https://www.tcpdump.org/)
- MDN HTTP status reference: https://developer.mozilla.org/docs/Web/HTTP/Status
- kernel packet docs: https://docs.kernel.org/networking/
