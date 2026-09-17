# Performance Clinic Challenges — C1–C8

> Same rules as the Load Clinic: your own VM, this clinic's capped
> scripts only, every verdict cites command + number, cleanup by
> census (`pgrep -af`) at the end.

## C1 — Trend or state?

Collect `uptime` every 10 s for 5 minutes while running
`./cpu_burn.sh 60 4` once, mid-collection. Plot or tabulate the three
load figures over time; identify exactly when the burn started and
stopped **from the numbers alone**, and explain in two sentences which
of the three averages responded fastest and why (decay!).

## C2 — The nice differential

Rerun M18's latency loop (or a simple `while` timing loop) while
launching `./cpu_burn.sh 60 4` — once un-niced (edit a copy to drop
`nice`), once nice-19 as shipped. Record max loop latency under each.
Deliverable: the two numbers + one sentence on what the difference
*is* (scheduler ranking made measurable).

## C3 — Cache theater

Run `cat ~/lab24/churnfile > /dev/null` (or any ~200 MB file) twice in
a row, timing both. Then explain the delta using one `free -h`
snapshot pair (before/after). Stretch: `vmstat 2` during the first read
— where do the read IOPS go on the second pass?

## C4 — The IOPS ceiling

Run `./io_churn.sh 60` twice: once as-is (4 KB), once with a copy of
the script edited to `bs=1M count=64` (sequential-ish). Record `await`,
`%util`, and effective MB/s for both. Deliverable: the four-row table
proving small-random saturates before sequential — Lesson 3's central
distinction, quantified on *your* disk.

## C5 — Peak-RSS census

Using `/usr/bin/time -v`, measure peak RSS for: (a) `python3 -c "import
pandas"`, (b) the Load Clinic's mem_grow python, (c) `python3 -c
"x=[bytearray(10_000_000) for _ in range(100)]"`. Tabulate; then write
the "fits on this VM?" verdict for a colleague who wants to run
something **10× (c)** on the shared 8 GB box.

## C6 — Error-counter forensics

`ip -s link show` snapshot before and after two minutes of
`./net_loop.sh 90`, plus `ss -s` both times. Write the three-line
"admin handoff" for any counter that moved: what changed, by how much,
during what window. (This *is* the evidence format from Lesson 4 §5.)

## C7 — The two-sentence incident note

A colleague reports: "the shared box felt slow around 14:00, something
about pandas." Given *only* these facts — load was 5.8/4 cores at
14:05, `wa` was 40%, and a 12 GB `groupby` job started at 13:58 —
write the two-sentence evidence note: which resource, which two
numbers, which one command would confirm. No verdict without numbers.

## C8 — Design: the shared-server performance policy

One page, no execution required: for a 6-person research box (8 cores,
32 GB, SSD), specify the evidence-backed policy — load-vs-cores alert
threshold, the `si/so` rule for memory, the `await`-vs-baseline rule
for disk, who runs what under nice/cgroup caps, and the weekly
`docker system df` + `df -i` hygiene. Every threshold must cite the
lesson that justifies it. Deliverable: the policy + the three risks
you'd flag to the professor.

---
*All challenges: own VM, capped scripts, evidence in `lab-log.md`,
census-clean exit.*
