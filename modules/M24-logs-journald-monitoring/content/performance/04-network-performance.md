# Network Performance — Latency, Throughput, Errors, Drops

> Performance Clinic · Module 24 · Difficulty: Advanced
> Reading time: ~25 min · Drill: [Load Clinic](lab-load-clinic.md) (Part D)
> Up next: [The Load Clinic](lab-load-clinic.md)

---

## 1. The three numbers: latency, throughput, errors

Network complaints usually arrive as one word — "slow" — but split into
three measurable, independent properties:

- **Latency** — time for one round trip (RTT). Feels like: *every
  interaction has a delay*, even tiny transfers. Measured: `ping`.
- **Throughput** — bytes per second once flowing. Feels like: small
  files fly, big downloads crawl (or everything crawls uniformly).
  Measured: loopback/controlled copies (§4).
- **Errors/drops** — packets lost or rejected. Feels like: *flaky* —
  retries, stalls, intermittent failures that "fix themselves".
  Measured: `ss -s`, `ip -s link` (§3).

The diagnostic matrix is the point: **high latency + normal throughput
is a distance/routing story; normal latency + low throughput is a
bandwidth/window story; errors and drops are a *health* story** — and
each has a different owner (your app, your network, your admin's link).

## 2. Latency: ping, honestly read

```console
$ ping -c 5 1.1.1.1
rtt min/avg/max/mdev = 12.8/13.4/14.9/0.7 ms
```

Read it as: **avg** is the story, **mdev** (jitter) is the reliability
subplot, **max spikes** are the "why did my SSH stutter" answers. A
stable 13 ms ± 1 is a healthy link; 13/60/13 avg/min/max with wild mdev
is lossy-neighbor territory even with zero packet loss.

`ping` against the *loopback* path (`ping -c 3 127.0.0.1`, ~0.05 ms)
is your sanity floor: if that's slow, it's not the network — it's the
host (CPU starvation, load 40 — Lesson 1's trap, found in the last
place people look).

DNS latency is its own measurement (M21 Lesson 3): `time dig
example.com` shows resolution time distinctly from transfer time — the
difference between "slow DNS" and "slow site".

## 3. Errors and drops: the interface's confessions

```console
$ ip -s link show eth0
    RX: bytes  packets  errors  dropped  overrun  mcast
    …          982k     0       41       0        1.2k
    TX: bytes  packets  errors  dropped  overrun  carrier
    …          741k     0       12       0        0
```

- **`errors`** — checksum/f framing problems: nonzero *and growing* =
  hardware/driver/host-neighborhood issue (admin conversation).
- **`dropped`** — the buffer was full when the packet arrived. A few
  thousand over a week is noise; climbing during load is your
  throughput ceiling confessing (buffers too small for the burst, or
  genuinely saturated link).
- **`overrun`** — the host couldn't take delivery fast enough: CPU
  starvation wearing a network costume (see Lesson 1's trap again).

`ss -s` gives the socket-population summary — thousands of sockets in
TIME-WAIT is *healthy churn* (M21), but thousands in CLOSE-WAIT is a
leaking app not closing connections. The counts discriminate.

## 4. Throughput: measuring without touching foreign hosts

Course-scoped measurement — everything lands on your own VM:

```console
# Loopback: the host's ceiling, no NIC involved (~GB/s; a floor, not a network test)
$ dd if=/dev/zero bs=1M count=500 status=none | nc -l -p 9999 > /dev/null &
$ dd if=/dev/zero bs=1M count=500 status=none | nc -q 1 127.0.0.1 9999

# SSH to your own VM: the encrypted-copy rate you'd actually feel (scp/rsync class)
$ dd if=/dev/zero bs=1M count=200 status=none | \
    ssh ds@localhost 'cat > /dev/null'
```

The loopback number calibrates; the ssh-pipe number is the one that
maps to "my dataset copy is slow" — it includes encryption and the SSH
channel's windowing. If a real transfer to the university server runs
at a fraction of this same-machine rate, the suspects narrow to the
path (latency/bandwidth, §2/§1) — not your host.

`nc` (netcat) is M21's conceptual tool promoted to a lab instrument:
`-l -p 9999` listens, piping to it sends. It exists here only against
`127.0.0.1` — the loopback-only rule from M21 carries verbatim.

## 5. Bottleneck signatures (network edition)

| Symptom | Likely story | Confirm with |
|---|---|---|
| every interaction delayed, transfers fine | latency (distance/routing) | ping avg/mdev |
| big copies crawl, small ops fine | throughput/bandwidth or TCP window | ssh-pipe rate vs loopback |
| intermittent stalls, retries | drops/errors climbing | `ip -s link` deltas over time |
| even loopback is slow | it's the *host*, not the network | load average (Lesson 1), CPU |
| `dig` slow, `ping` fine | DNS resolution, not connectivity | `time dig` (M21 §3) |
| TIME-WAIT thousands | normal churn (M21 §4) | `ss -s` — leave it alone |
| CLOSE-WAIT thousands | app leaking sockets | restart the app; fix the code |

**One paragraph of humility:** the network is the resource you *least*
own — path, routers, and neighbors are the university's. The clinic's
scope ends at your VM's interfaces and the loopback; beyond that, your
job is to arrive at the admin with evidence ("dropped TX climbing from
41 to 900 during 14:00–15:00, error-free before") instead of a mood.

---

## Key takeaways

- Split "slow" into **latency / throughput / errors** before diagnosing
  — each has different instruments and different owners.
- `ping`'s avg + mdev + max tell health, stability, and stutter
  separately; loopback is the sanity floor that proves it's *not* the
  network.
- `ip -s link` errors = health, drops = buffers/saturation, overruns =
  host CPU wearing a network costume; `ss -s` counts discriminate churn
  from leaks.
- Measure throughput only against your own VM (loopback `nc`, ssh
  pipe); beyond your interfaces, deliver *evidence* to the admin.

## Check yourself

1. `ping` to the world: avg 14 ms, mdev 0.8. Transfers top out at a
   fraction of expectations. Which property is failing, and which §4
   measurement brackets it?
2. `ip -s link` TX `dropped` climbs from 12 to 800 during a big rsync.
   Explain the mechanism in one sentence, and who owns the fix.
3. Everything is network-slow — including `curl 127.0.0.1`. What do
   you check first, and why does the answer embarrass the network
   hypothesis?
4. What separates thousands of TIME-WAIT from thousands of CLOSE-WAIT,
   and why is one healthy and the other a bug?

*Answers:* (1) Throughput — bracket with the loopback `nc` floor vs the
ssh-pipe rate; if loopback is fast and ssh-to-self is fast, the path
(latency/bandwidth/link) owns the shortfall. (2) The TX ring buffer
filled faster than the interface drained it — burst over buffer, i.e.
saturation or undersized buffers; the fix belongs to the link owner
(admin), not the app. (3) Load average/CPU first (Lesson 1's trap) —
if *loopback* is slow, packets aren't the problem; a starved host is.
(4) TIME-WAIT is the *client-side* closed-connection cooldown after a
normal close (the app did its job); CLOSE-WAIT means the *remote* closed
and the local app never did — a leak that grows until sockets or memory
exhaust.

Up next: [The Load Clinic](lab-load-clinic.md) — four workloads, four
instruments, and your first evidence-only diagnoses.
