# Drill Book — Incident 3: The Unresolvable Host

> Setup time: 3 min · Solve time: ~20 min
> Cards: [7 — DNS failure](../scenarios/07-dns-failure.md)
> Scope: a `/etc/hosts` edit (sudo, single line, revertible — the setup
> *shows* you the undo). Nothing else on the system changes.

## Setup

```bash
#!/usr/bin/env bash
# setup-incident-3.sh — one poisoned hosts line (pypi.org → 127.0.0.1)
set -euo pipefail
sudo cp /etc/hosts ~/drill3-hosts.bak            # the undo, made in advance
echo "127.0.0.1 pypi.org files.pythonhosted.org" | \
  sudo tee -a /etc/hosts > /dev/null
echo "Incident 3 staged. Undo: sudo cp ~/drill3-hosts.bak /etc/hosts"
```

## The symptom

```console
$ python3 -m pip install -q pandas==2.2.3
WARNING: Retrying … /simple/pandas/ Could not resolve host? (or similar)
$ curl -sS https://pypi.org/simple/ -o /dev/null
curl: (7) Failed to connect to pypi.org port 443 …
$ curl -sS https://example.com -o /dev/null -w '%{http_code}\n'
200                                   # ← everything else works. Interesting.
```

**Your incident brief:** "pip is broken for one teammate on this VM —
'network is down' they said, but only for *some* sites. SSH, browsing,
and apt all work."

## Solving notes (for the grader in you)

- The discrimination is card 7's whole point: *IP-reachability works
  (`curl` example.com: 200), name-resolution for *specific* names
  doesn't* — and the selectivity (`pypi.org` fails, `example.com`
  works) is the hosts-override fingerprint. A resolver problem fails
  broadly; a hosts-poisoning problem fails *exactly where it was
  pointed*.
- The evidence chain: `dig +short pypi.org` (resolver says one thing)
  vs `getent hosts pypi.org` (the *system* says another) — when those
  two disagree, nsswitch is consulting `/etc/hosts` first, and the
  evidence is one `tail /etc/hosts` away.
- Safe test before the fix: `curl -s -o /dev/null -w '%{http_code}\n'
  --resolve pypi.org:443:$(dig +short pypi.org @1.1.1.1 | head -1)
  https://pypi.org` — reachability proven *around* the poisoned name,
  confirming the name layer as the only casualty.
- The fix is the pre-staged undo — and the verification is
  three-layer (card 7): dig, getent, *and the original pip command*.
- Prevention writes the card's moral: "selective failure with working
  IPs → check the hosts file first; it's the override layer everyone
  forgets they have."

**Done when:** pip succeeds verbatim, the three-layer verification is
quoted, and the journal names nsswitch's hosts-first order as the
mechanism.

Next: [Incident 4 — the phantom hang](lab-04-the-phantom-hang.md)
