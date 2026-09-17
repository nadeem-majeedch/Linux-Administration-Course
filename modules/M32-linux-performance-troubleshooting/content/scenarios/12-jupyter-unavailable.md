# Drill Card 12 — "Jupyter Unavailable"

> Scenario family: Composite · Difficulty: ●●●
> Source modules: [M27 lesson 2](../../../M27-python-jupyter-data/content/lessons/02-jupyter-on-linux.md), [M22](../../../M22-ssh-remote-admin/README.md), [M21](../../../M21-networking-fundamentals/README.md)
> This is the *composite* card: it composes cards 6, 8, and 10 along the
> client→browser→tunnel→server→kernel chain.

## Symptom

"The notebook won't open." Four distinct layers hide under that
sentence, and the client's error message usually names the layer — if
you know the mapping.

## Decision tree (walk the client→kernel chain)

```text
Browser error / curl code?
├─ connection refused / timeout   → layers 1–3: network or server
│   ├─ server-side: ss -tlnp | grep 8888  → listener? bound WHERE?
│   ├─ bound 127.0.0.1, remote client → TUNNEL up? (layers 2–3)
│   └─ no listener at all        → server process: card 6
├─ 403 / token prompt loop       → layer 4: auth (token/cookie stale)
└─ opens, kernel dead / import fails → layer 5: kernel-venv: card 10
```

## Evidence (server-side first — it's where the truth lives)

```console
$ ss -tlnp | grep 8888             # layer 1: process alive, bound WHERE?
$ ps aux | grep -i jupyter | grep -v grep   # duplicates? (card's classic: TWO servers)
$ curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8888   # server sees itself?
# client-side (physical machine):
$ curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:9999    # through the tunnel
$ ssh -v ds@vm-ip 2>&1 | tail -3   # if the tunnel itself is down: M22's sweep
```

The **duplicate-server trap** (M27 troubleshooting #8): an old Jupyter
still holds the port with a dead session list, while your "new" one
failed to bind silently. Two processes in `ps`, one listener in `ss` —
that asymmetry *is* the diagnosis.

## Fix pattern

- **No listener** → the service failed: card 6 (unit/journal) or
  restart the headless process with evidence (`nohup` + PID file +
  log, M27 Lab 2 Part E).
- **Listener on loopback, remote client, no tunnel** → *posture, not
  bug*: re-establish the tunnel (`ssh -L 9999:127.0.0.1:8888 … -N`,
  M22 §3) and use `127.0.0.1:9999`. Never "fix" by binding
  `0.0.0.0:8888` — that trades an access problem for a security
  incident (M25).
- **403/token loop** → the token lives in the server's startup log
  (`jupyter lab list`, or the nohup log's URL); a stale browser cookie
  clears with a fresh incognito window. Quote the token URL's
  origin — the *running* server's, not yesterday's.
- **Opens but kernel dies / imports fail** → kernel↔venv mismatch:
  card 10's sweep *inside* the failing kernel (`sys.executable` in a
  cell), re-register the venv kernel.

## Verify

The original user experience, reproduced: from the *client machine's
browser*, open the notebook through the tunnel, run a cell that
imports the project venv's stack, save. (Server-side green checks
while the browser still fails is the #1 incomplete verification in
this entire deck — layers 2–5 can each fake it.)

## Document

Name the deepest layer that failed. Vocabulary: *"stale server held
port (duplicate process)"*, *"tunnel absent, client hit LAN address"*
(posture working as designed), *"kernel registered to system python"*.
Prevention: one-server discipline, PID+log launch pattern, the
kernel-registration step in project setup.

**Done when:** you can stage and fix **two** of the four layers in
your own VM (e.g., kill the server; then break the tunnel), and write
the five-layer chain from memory with the discriminating command per
layer.

---

*Cards 1–12 complete. The [Drill Book](../labs/README.md) strings four
of these into independent, staged incidents — method-graded.*
