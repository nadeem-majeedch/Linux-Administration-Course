# Lesson 3 — DNS: How Names Become Addresses (and How to Diagnose Them)

> Module 21 · Unit 6 · Difficulty: Advanced
> Reading time: ~35 min · Lab: [Lab 2 — the diagnosis clinic](../labs/lab-02-diagnosis-clinic.md)
> Prerequisites: [Lesson 2](02-ip-and-routing.md)

> 🟢 Safety: DNS *queries* are ordinary internet behavior. What's off-
> limits for this course: zone transfers, mass enumeration, or querying
> systems you don't own beyond normal lookups. Everything in the labs
> resolves public names or localhost — normal user behavior.

---

## 1. The resolution chain (every lookup walks it)

`git clone https://github.com/…` needs an IP first. The chain, in
order:

```text
1. Application cache      (the browser's, getaddrinfo's nscd…)
2. /etc/hosts             (local static overrides — sysadmin territory)
3. systemd-resolved       (your machine's stub resolver + its cache)
4. The configured DNS     (campus/home recursive resolver, via DHCP)
    servers
5. The hierarchy          (root → TLD → authoritative — the resolver's job, not yours)
```

Your machine talks to **recursive resolvers** (steps 3–4) that do the
hierarchy walking for you. Records worth knowing by name:

| Type | Maps | Example use |
|---|---|---|
| **A** | name → IPv4 | the everyday lookup |
| **AAAA** | name → IPv6 | the v6 twin |
| **CNAME** | name → name (alias) | `cdn.example.com` → real host |
| **MX** | mail routing | "why isn't our mail arriving?" |
| **PTR** | IP → name (reverse) | logs that show names, not numbers |
| **TXT/SRV/NS** | metadata, service discovery, delegation | DKIM, `_service._tcp`, zone plumbing |

---

## 2. /etc/hosts and hostname resolution order

```console
$ cat /etc/hosts
127.0.0.1   localhost
127.0.1.1   labvm
#10.0.0.5   gpu-cluster-old     # a disabled override (commented)
```

`/etc/hosts` is checked *before* DNS (per nsswitch policy) — the
sysadmin's sledgehammer: instant overrides for testing, but a famous
source of "works on my machine" (a stale hosts entry pointing the
world somewhere wrong). The policy file:

```console
$ grep hosts /etc/nsswitch.conf
hosts: files mdns4_minimal [NOTFOUND=return] resolve [!UNAVAIL=return] dns
```

Read it left-to-right: files (hosts) → mdns → **resolved** (if
available, answers are final) → dns (classic resolv.conf path). On
modern Ubuntu, **systemd-resolved** runs the show:

```console
$ resolvectl status | head -12
Global
       Protocols: LLMNR=resolve -mDNS -DNSOverTLS DNSSEC=no/unsupported
Link 2 (enp3s0)
    Current Scopes: DNS
         DNS Servers: 192.168.1.1                      ← handed out by DHCP
          DNS Domain: lan
$ resolvectl query github.com           # ask the local resolver directly
github.com: 140.82.121.4                     -- link: enp3s0
```

(WSL2 quirk to recognize: it regenerates `resolv.conf` from Windows
 networking — the classic "WSL DNS broke after VPN" has its fix in
 troubleshooting #8.)

---

## 3. dig: the diagnostic instrument

`dig` asks a resolver a question and shows *everything*:

```console
$ dig github.com
;; QUESTION SECTION:
;github.com.                    IN      A

;; ANSWER SECTION:
github.com.             60      IN      A       140.82.121.4

;; Query time: 12 msec
;; SERVER: 127.0.0.53#53(urllib.resolver)   ← who answered
```

The three things to read: the **ANSWER** (with TTL countdown), the
**SERVER** that answered, and **Query time** (12 ms = cached nearby;
300 ms = asking far away). The flag set that covers daily work:

```console
$ dig +short github.com              # just the answer (scriptable!)
140.82.121.4
$ dig +short AAAA github.com         # the IPv6 record
$ dig +short mx github.com           # a different record type
$ dig @1.1.1.1 github.com            # ask a SPECIFIC resolver (bypass yours)
$ dig +trace example.edu | tail -8   # walk the hierarchy (educational; occasional)
```

**The DNS diagnosis drill** — three questions, three digs:

1. `dig +short name` — does *my* resolver answer at all? (Empty +
   status NXDOMAIN/SERVFAIL = resolver or record problem.)
2. `dig @1.1.1.1 name` — does the *public internet's* resolver answer?
   (Works here but not via mine → my resolver is the problem.)
3. `dig @<campus-DNS> name` — isolates which resolver in the chain
   lies/breaks.

Two dig facts that prevent confusion: TTLs count *down* in answers
(caches expire — the fix for bad DNS is patience or cache flush), and
a name can legitimately have *no* A record while working fine via
CNAME+AAAA (read the whole ANSWER section, or just use +short for
clarity).

---

## 4. host & nslookup: the quick tools

```console
$ host github.com                 # terse: name → addresses (+ mail route)
github.com has address 140.82.121.4
github.com mail is handled by 1 aspmx.l.google.com.
$ host -t AAAA github.com         # specific type
$ host 140.82.121.4               # REVERSE lookup (PTR) — logs' names
$ nslookup github.com             # the other classic; fine to read, dig to debug
```

`host` for one-liners, `dig` for understanding, `nslookup` for reading
in tutorials — the course hierarchy. Reverse lookups (`host <ip>`) are
the quiet workhorse: turning cluster log lines from `10.20.30.40` into
`gpu-04.cluster.edu`.

---

## 5. DNS in the DS world (where it bites you)

- **Package mirrors & PyPI:** `pip install` stalls → `dig
  pypi.org +short` first. A resolver outage looks exactly like a
  "slow mirror."
- **API endpoints with rotating IPs:** cloud services answer with
  short TTLs; a script caching an IP from Tuesday breaks Thursday.
  Resolve *per connection*, or use their SDKs.
- **University clusters:** `dig +short gpu-04.cluster.edu` before
  SSHing — and PTR in logs to see *which* node misbehaved.
- **Git remotes:** `ssh: Could not resolve hostname github.com` is a
  DNS diagnosis (Lesson 5's playbook), not a Git problem.
- **/etc/hosts override for testing:** point `jupyter.local` at
  127.0.0.1 to rehearse name-based config locally — the hosts file's
  legitimate superpower.

---

## 6. The DNS runbook (the lesson in five lines)

```console
$ dig +short NAME                 # 1. does my resolver answer?
$ dig @1.1.1.1 +short NAME        # 2. does another resolver agree?
$ resolvectl status | grep -A2 "DNS Servers"   # 3. who ARE my resolvers?
$ grep NAME /etc/hosts            # 4. am I being overridden locally?
$ ping -c1 -n NAME                # 5. -n: numeric — no DNS in the ping! (compare)
```

Step 5's `-n` flag is the subtle pro move: `ping NAME` *itself does
DNS* — a failing lookup looks like a network failure. `-n` separates
"can't resolve" from "can't reach."

---

## Exercises (lab-log.md)

1. `dig github.com` — annotate SERVER, TTL, and query time. Then
   `dig github.com` again: did TTL and time change? Why?
2. The three-question drill (§3) against `pypi.org`. Do your resolver
   and 1.1.1.1 agree? Record both answers.
3. `resolvectl status`: your actual DNS servers and their source
   (DHCP?). Then `resolvectl query pypi.org` — compare with dig's
   path.
4. `host` vs `dig +short` on three names. When would the terse view
   mislead? (Hint: multiple record types; CNAME chains.)
5. Reverse-lookup the gateway IP (`host 192.168.1.1` or your default
   GW). Named or empty — and what does an empty PTR tell you about
   the network's tidiness?
6. The `/etc/hosts` experiment: map `jupyter.test` → 127.0.0.1, start
   `python3 -m http.server 8000 --bind 127.0.0.1`, then
   `curl -I http://jupyter.test:8000`. Undo the hosts entry after.
   Two sentences: when is this trick legitimate?

## Check yourself before Lesson 4

- [ ] I can name the resolution chain and say where /etc/hosts sits.
- [ ] dig's ANSWER/SERVER/time trio is how I read every lookup.
- [ ] The three-question drill localizes a DNS failure to a resolver.
- [ ] I know why ping needs `-n` during DNS diagnosis.

## Further reading (official sources)

- `man dig`, `man host`, `man nslookup` (BIND tools:
  https://bind9.readthedocs.io/)
- `man 5 hosts`, `man nsswitch.conf`, `man resolvectl` (systemd docs:
  https://www.freedesktop.org/software/systemd/man/latest/resolvectl.html)
- Ubuntu Server Docs — DNS: https://ubuntu.com/server/docs
