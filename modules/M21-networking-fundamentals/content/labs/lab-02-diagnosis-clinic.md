# Lab 2 — The Diagnosis Clinic: Three Local Incidents

> Module 21 · Unit 6 · Difficulty: Advanced
> Time: ~50 min · Environment: your own VM — incidents are local
> services **you** start, then break **on purpose**
> Prerequisites: [Lab 1](lab-01-local-network-lab.md), [Lesson 5's playbook](../lessons/05-http-tools-diagnosis.md)

Three incidents, each a different layer. You get symptoms only; the
six-rung playbook (link → IP → route → DNS → port → app) is your only
doctor. Every incident needs the five-part writeup: **symptom →
diagnosis (with commands) → fix → verification → prevention.**

## Setup — the lab's little fleet (all loopback)

```console
$ mkdir -p ~/lab21 && cd ~/lab21
$ echo "api v1" > api/index.html 2>/dev/null || (mkdir -p api && echo "api v1" > api/index.html)
$ echo '{"status":"ok"}' > api/health.json
$ python3 -m http.server 8000 --bind 127.0.0.1 --directory ~/lab21/api &
$ echo "127.0.0.1 api.local" | sudo tee -a /etc/hosts     # the name under test
$ curl -s http://api.local:8000/health.json               # baseline: {"status":"ok"}
```

Record the baseline. **Now your patient is healthy — each incident
breaks exactly one thing.**

## Incident 1 — "the API hostname stopped resolving"

**Symptom (reported):** `curl http://api.local:8000/health.json`
→ `Could not resolve host: api.local`.

**Your job:** which rung? Prove it:

```console
$ dig +short api.local            # does DNS answer?
$ grep api.local /etc/hosts       # where SHOULD the answer come from?
$ getent hosts api.local          # what does the resolution chain say?
```

**The hidden break (a TA applied it):**

```console
$ sudo sed -i 's/^127.0.0.1 api.local/#127.0.0.1 api.local/' /etc/hosts
```

**Diagnose → fix → verify:** expect `dig` to find *nothing* (hosts
entries aren't DNS — the resolver reads files first!), the nsswitch
chain to fail, and the fix to be re-enabling the hosts line. Write the
prevention: why a "DNS problem" that only affects one made-up name is
a hosts-file problem by definition.

## Incident 2 — "connection refused on port 8000"

**Symptom:** the server process is dead:

```console
$ pkill -f "http.server 8000"     # (the TA's "fix")
$ curl http://api.local:8000/health.json   # refused!
```

**Your job:** refused or timeout? What's the difference *here*?

```console
$ ss -tlnp | grep 8000            # LISTEN? no → nothing to connect to
$ curl -v telnet://api.local:8000 </dev/null 2>&1 | grep -iE "refused|timeout"
$ nc -zv 127.0.0.1 8000           # the port probe's verdict
```

**Diagnose → fix → verify:** restart the server; re-verify with ss +
curl. Write the prevention: "refused" meant *machine fine, port
empty* — the fix is a service restart (M20 echo: `systemctl --user`
would have kept it alive).

## Incident 3 — "it works on localhost but not via the name"

**Symptom:** TA re-added the hosts entry — but pointing at the wrong
address:

```console
$ pkill -f "http.server 8000" || true
$ python3 -m http.server 8000 --bind 127.0.0.1 --directory ~/lab21/api &
$ sudo sed -i 's/^#127.0.0.1 api.local/127.0.0.2 api.local/' /etc/hosts
$ curl http://api.local:8000/health.json    # hangs/times out — but localhost works?!
```

**Your job:** the subtlest one — same port, same server, one name
fails. Layered diagnosis:

```console
$ curl http://127.0.0.1:8000/health.json    # works → server fine
$ getent hosts api.local                    # 127.0.0.2 — is that loopback? (127.0.0.0/8 IS loopback…)
$ ss -tlnp | grep 8000                      # bound to WHICH address exactly?
```

The teaching point: the server binds **127.0.0.1 only**; 127.0.0.2 is
also loopback, but *nothing listens there on :8000* — connection
refused at a different address. Binding scope (Lesson 4 §3) meets
hosts overrides (Lesson 3 §2).

**Diagnose → fix** (hosts entry → 127.0.0.1) **→ verify → prevention**
(one sentence: why "bind wider" is the *wrong* fix).

## Wrap-up — the clinic report

One table, three rows: incident / failing rung / the single command
that revealed it / fix / prevention. Then the meta-question: incident
1's symptom *claimed* DNS; was it? What does that say about trusting
error messages versus running the ladder?

## Done when

- [ ] All three incidents have five-part writeups
- [ ] Every diagnosis cites the rung and the revealing command
- [ ] `/etc/hosts` restored (`grep api.local /etc/hosts` → clean or
      correct), no stray servers running (`pgrep -af http.server`)
- [ ] The meta-question answered in two sentences
