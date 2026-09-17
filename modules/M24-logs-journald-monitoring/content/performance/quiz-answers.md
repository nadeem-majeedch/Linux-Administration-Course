# Performance Clinic Quiz — Answer Key

> Grading guide: any wording that shows the reasoning earns credit;
> command answers graded on "would it work if typed".

## Section A — CPU

**Q1.** No. `wa` 45% says the CPU is *idle waiting on disk*, and load
counts those uninterruptible waits — the CPU is the scapegoat, not the
cause. Redirect: `iostat -xz` for `await`/`%util`/`aqu-sz` (Lesson 3);
`vmstat`'s `b` column corroborates.

**Q2.** `%ni` is user CPU spent on niced (renice > 0) processes —
M18's nice-19 burners land here. Visibility in `%ni` proves the batch
load is *ranked below* interactive work: when contention hits, Jupyter
keeps its latency and the burners absorb the squeeze.

**Q3.** 3 tasks runnable at this instant out of 987 total tasks. It's
the instantaneous run queue — no averaging lag — hence the honest
"right now" against which the decayed 1/5/15-min figures are trends.

**Q4.** Waiting, not computing: wall (240 s) ≫ user+sys (46 s) means
~80% of the run was I/O or other blocking. Instrument: iostat during a
re-run (`await`), or strace-level awareness for syscall stalls.

**Q5.** numpy/BLAS thread pools default to one thread per core —
400% CPU is the library's *design*, not a runaway. Courtesies: (1)
`nice`/`renice +10` so interactive work outranks it (M18); (2) a cgroup
cap — `--cpus=2` in a container, or taskset pinning awareness (M28's
limits lesson).

## Section B — memory & swap

**Q6.** Healthy. The diagnosis comes from `available` (5.2G): most of
`free`'s smallness is `buff/cache` (page cache = disk blocks kept in
RAM for speed), reclaimable instantly under pressure. "free is low" is
the beginner's misread.

**Q7.** History: pages were swapped out at some point, are now cold,
and nothing is moving (`si/so` = 0). It becomes a problem when
`vmstat` shows **sustained nonzero `si/so`** — pages actively
migrating, i.e., thrashing.

**Q8.** (1) page-cache reclaim, (2) anonymous-page swap-out (`si/so`
begins), (3) kswapd churn, (4) OOM killer SIGKILLs the highest-badness
process. Verdict pair: `journalctl -k --since -1h | grep -i oom` (or
`dmesg -T | grep -i oom`) — the line names victim, PID, and size.

**Q9.** VSZ counts the whole address space — mmapped files, reserved
but untouched regions — which pandas/numpy inflate with mmaps that
never cost real RAM. Quote **RSS** (resident now) and **peak RSS**
(`/usr/bin/time -v` maximum resident set) — peak is the OOM-relevant
number.

**Q10.** Major faults = page-ins from disk: pages the process needs are
not in RAM (swapped out earlier, or file-backed and evicted). The two
resources: **memory** (the shortfall) and **disk** (the price paid) —
rising majfl is the memory pressure showing up as I/O.

## Section C — disk I/O

**Q11.** Employed, not sick: `%util` ~97% says saturated; `await` 4 ms
says it's *delivering* at its normal pace; shallow queue (`aqu-sz`
1.2) says requests aren't piling catastrophically. A sick disk shows
await far above the device's baseline at similar load. The fix
conversation is scheduling less I/O, not replacing hardware.

**Q12.** Small-random (4 KB average write) — the database/metadata
churn shape. It exhausts **IOPS** first: most storage does far better
on sequential MB/s than on many small operations, so `await` blows up
while throughput looks innocent.

**Q13.** Deleted-but-open: a process holds an unlinked file's inode
open, so its blocks stay allocated. The space returns only when the
holder closes/exits — find holders via `lsof +L1` (awareness), stop
the writer *first*, then clean.

**Q14.** `df -i` — inode exhaustion: IUse% ~100% means the *file count*
is the exhausted resource (millions of tiny files), not bytes. The
"No space" message names the wrong resource.

**Q15.** Removing the suspected cause and watching the symptom
*reproducibly vanish* is a controlled intervention — it establishes
causality (A→B), which waiting cannot. Evidence-first discipline:
baseline, change one thing, re-measure, keep the before/after pair.

## Section D — network & synthesis

**Q16.** Latency (RTT) — `ping` avg/mdev; throughput — controlled
loopback `nc` / ssh-pipe rate vs expectations; errors/drops — `ip -s
link` error/drop counters over time. Three properties, three
instruments, three different owners.

**Q17.** Load average and CPU first (Lesson 1's trap). If *loopback*
curl is slow, packet path and NIC are exonerated — the host is
starved; the network hypothesis dies before you open a single
interface counter.

**Q18.** The TX ring buffer filled faster than the interface drained
it — packets arrived for transmission with no buffer slot free. Fix
owner: the link/buffer configuration — the admin's layer, escalated
with the before/after counter deltas as evidence.

**Q19.** TIME-WAIT is healthy — the *client-side* cooldown after a
normal close (our side did everything right); CLOSE-WAIT is a leak —
the remote closed, our app never called close() on its side, so these
accumulate until resources exhaust. Churn vs bug, distinguished by
state counts in `ss -s`.

**Q20.** Format: verdict + led/confirmed. E.g., "Disk I/O is the felt
bottleneck: CPU saturated but polite (`%ni` ~60, load 4/4) while
`await` rose 0.3 → 45 ms at `%util` 99 — the soggy feeling tracks the
disk. `iostat await` *led* (it moved first, before load), and the
reproducible drop after stopping the churn *confirmed*."

Practice more: [challenges.md](challenges.md) ·
Back to the clinic: [README.md](README.md)
