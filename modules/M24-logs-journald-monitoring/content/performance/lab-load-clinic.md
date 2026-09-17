# The Load Clinic — Diagnose Four Workloads Before You Check the Answer

> Performance Clinic · Module 24 · Difficulty: Advanced
> Time: ~75 min · Environment: your own VM
> Prerequisites: Lessons 1–4 of this clinic, M24 Lab 3's stress habits
> ⚠️ All load is this lab's own scripts: nice-19 burners, capped memory
> growth with a cleanup line, dd churn into `~/lab24/`, loopback-only
> network tests. Every script has a `timeout`. No system tuning.

Four rounds. In each: **start the workload, observe with the
instruments, write your diagnosis — then and only then read the
round's "truth note"** to check yourself. The skill being graded is
the *evidence chain*: claim → command → number.

## Setup (5 min)

```console
$ mkdir -p ~/lab24/clinic && cd ~/lab24/clinic
$ python3 -m venv .venv && source .venv/bin/activate    # M27 habits
(.venv) $ pip install -q pandas numpy
```

**`cpu_burn.sh`** — polite CPU load:

```bash
#!/usr/bin/env bash
# $1 = seconds, $2 = worker count (nice 19, capped)
timeout "${1:-60}" bash -c "for i in \$(seq ${2:-1}); do nice -n 19 bash -c 'while :; do :; done' & done; wait" &
```

**`mem_grow.sh`** — capped memory growth, self-cleaning:

```bash
#!/usr/bin/env bash
# $1 = seconds; grows to ~1.5 GB then holds; frees on exit
timeout "${1:-90}" python3 - <<'EOF'
import time
chunks = []
try:
    while True:
        chunks.append(bytearray(50_000_000))   # ~50 MB steps
        if sum(len(c) for c in chunks) > 1_500_000_000:
            break
except MemoryError:
    pass
time.sleep(int(__import__("sys").argv[1] if len(__import__("sys").argv) > 1 else 60))
EOF
```

**`io_churn.sh`** — small-random write churn (the IOPS killer):

```bash
#!/usr/bin/env bash
# $1 = seconds; many 4KB writes + fsync-ish flushes
timeout "${1:-60}" bash -c '
  F=~/lab24/clinic/ioload.bin
  while :; do
    dd if=/dev/urandom of=$F bs=4k count=64 oflag=direct status=none 2>/dev/null || \
    dd if=/dev/urandom of=$F bs=4k count=64 conv=fsync status=none
  done' &
```

**`net_loop.sh`** — loopback transfer (scope-safe):

```bash
#!/usr/bin/env bash
# $1 = seconds; loopback nc transfer, ~1 MB/s modest rate
timeout "${1:-45}" bash -c '
  (while :; do dd if=/dev/zero bs=1k count=1024 status=none; sleep 0.05; done | nc -l -p 9998 > /dev/null) &
  sleep 0.3
  while :; do dd if=/dev/zero bs=1k count=1024 status=none | nc -q 1 127.0.0.1 9998; sleep 0.05; done' &
```

`chmod +x *.sh`. Keep a second terminal (or tmux pane, M22 §4) open for
instruments — that's the professional shape of this work.

## Round A — CPU (10 min)

Start `./cpu_burn.sh 120 4` (4 workers on a 4-core VM). In the
instrument pane, capture: `uptime`, `top -b -n1 | head -12`, `vmstat 2
3`. Write your diagnosis **first**: load vs cores? `us` vs `wa`?
Run-queue field from `/proc/loadavg`?

> **Truth note A:** four nice-19 spinners on 4 cores → load ≈ 4 (÷
> cores ≈ 1.0: saturated but fluid), `%ni` ≈ 100, `wa` ≈ 0. The
> teaching point: this is *healthy full employment* — and `%ni` is the
> row that proves the load is polite (M18's design). If you wrote
> "CPU emergency", re-read Lesson 1 §2: busy ≠ broken.

Now the crossover: `./cpu_burn.sh 120 4` **plus** `./io_churn.sh 90`.
Re-read `top`: `wa` should climb and `%ni` share the CPU. Your
one-sentence verdict: *which resource is now the constraint?*

> **Truth note (crossover):** with disk in the mix, `wa` rises — the
> CPU is no longer the whole story; iostat becomes the relevant
> instrument. This is Lesson 1's "disk masquerading as load" live.

## Round B — memory & swap (15 min)

Snapshot first: `free -h`, `vmstat 2 3` (baseline `si/so`). Start
`./mem_grow.sh 120`. Watch `watch -d free -h` and `vmstat 2 2`: track
`available` as it falls and whether `si/so` stir at all. Write:
*at what `available` value did you start caring, and what would change
your diagnosis from "watching" to "intervening"?*

> **Truth note B:** 1.5 GB on an 8 GB VM shouldn't reach swap —
> `si/so` stays 0 and `available` dips then recovers when the script
> exits. The teaching point: **the intervention threshold is sustained
> `si/so` activity, not "free looks small"** (Lesson 2 §2). If your VM
> is smaller and swap *did* churn, that's the real symptom — quote the
> `si/so` numbers, then let the script's timeout clean up.

Then the OOM-adjacent exercise (no actual OOM): run
`/usr/bin/time -v python3 -c "x = [bytearray(10_000_000) for _ in range(200)]"`
and record **peak RSS** from `-v`. One sentence: what would this number
need to be before you'd worry about the OOM killer on *this* VM?

## Round C — disk I/O (15 min)

Snapshot: `iostat -xz 2 3` (idle baseline — save it). Start
`./io_churn.sh 120`. Capture iostat again. Write the four numbers that
matter — `await`, `aqu-sz`, `%util`, and the avg write size
(`wkB/s ÷ w/s`) — then classify: sequential or small-random? Busy or
slow? Compare `await` against your idle baseline (which was ~0: this
*is* the baseline exercise).

> **Truth note C:** 4 KB random-ish writes → tiny avg write size,
> IOPS-bound: `%util` pinned near 100, `await` elevated, throughput
> numbers unimpressive. The teaching point: this workload saturates
> IOPS long before MB/s — Lesson 3 §2's distinction, witnessed. Cleanup:
> `rm -f ~/lab24/clinic/ioload.bin` (your file, your delete).

Then `du -sh ~/lab24` and one `df -h` line for `/` — your disk-consumption
receipt for the whole clinic.

## Round D — network, loopback only (10 min)

Baseline: `ping -c 3 127.0.0.1` (the ~0.05 ms floor),
`ip -s link show <iface>` (note RX/TX drops), `ss -s`. Start
`./net_loop.sh 60`. Re-capture `ip -s link` deltas and try the ssh-pipe
rate check *while* the loopback load runs. Write: did loopback latency
move? Did drops climb? What would you *not* conclude from loopback
numbers?

> **Truth note D:** loopback latency stays ~0.05 ms; modest load moves
> few counters. The teaching point: **loopback proves the host's
> networking stack, not the LAN** — Lesson 4 §5's humility, in
> numbers. If drops *did* climb, quote before/after `ip -s link` — that
> delta *is* the evidence format.

## Round E — the full clinic (15 min)

Start `./cpu_burn.sh 150 3` **and** `./io_churn.sh 120` together. Your
task: one instrument-led paragraph in `lab-log.md` — load vs cores,
`us`/`ni`/`wa` split, `await`/`util`, and a final verdict naming *the*
bottleneck with the two numbers that justify it. Then the honest
post-check: which instrument told you first, and which number confirmed?

> **Truth note E:** with both loads running, expect load ≈ 4 (÷ cores
> → saturated), `%ni` high with `wa` climbing — CPU *and* disk
> contested, disk likely the felt bottleneck (everything soggy, not
> just compute). The grading bar isn't matching the note; it's a
> verdict whose numbers could survive cross-examination.

## Cleanup & done-when

```console
$ pgrep -af "cpu_burn|io_churn|mem_grow|net_loop"   # census: all dead (timeouts fired)
$ rm -f ~/lab24/clinic/ioload.bin
$ docker ps -a | grep lab24 || echo "nothing containerized here"
```

- [ ] Five rounds diagnosed **before** each truth note; predictions
      vs truths recorded
- [ ] Every verdict cites command + number (the evidence chain)
- [ ] Peak-RSS and baseline-iostat snapshots saved in `lab-log.md`
- [ ] Census clean; ioload.bin removed; one paragraph on which round
      changed your mental model most

**Where this feeds forward:** the
[troubleshooting capstone](../../../M23-linux-performance-troubleshooting/content/README.md)
assumes exactly these evidence chains — the clinic is its warm-up
round.
