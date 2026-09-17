# The Performance Clinic — CPU, Memory, Disk I/O, Network (Performance Extension)

> Module 24 extension · Unit 6 · Difficulty: Advanced
> Time: ~5 hours · Environment: your own VM
> Prerequisites: [Lessons 3–4](../README.md) (toolkit + incident method), [M18](../../../M18-processes-jobs-signals/README.md), [M17](../../../M17-storage-and-filesystems/README.md)

The monitoring toolkit lesson taught you to *read* the instruments over a
controlled load. This clinic goes further: the **four resource streams**
one at a time — CPU, memory/swap, disk I/O, network — each with its own
lesson, its own bottleneck signatures, and a graded drill, then one
**multi-instrument load clinic** where you diagnose which resource is
hurting before you look at the answer.

**The standing question for every stream:** *utilization → saturation →
errors.* A resource is only "the problem" when it's saturated (queueing)
or erroring — utilization alone proves nothing (a busy-but-fluid CPU is
healthy). This is the USE method framing, applied per resource.

## Files

| # | File | Stream |
|---|------|--------|
| 1 | [01-cpu-performance.md](01-cpu-performance.md) | Load average decoded, run queue, top/htop/ps/time, nice recaps, CPU bottleneck signatures |
| 2 | [02-memory-swap.md](02-memory-swap.md) | free decoded, cache vs used, swap activity vs swap size, the OOM sequence, page-cache intuition |
| 3 | [03-disk-io.md](03-disk-io.md) | iostat decoded, await vs util%, throughput vs latency, df/du triage, deleted-open & inode traps |
| 4 | [04-network-performance.md](04-network-performance.md) | latency/throughput/errors split, ping decoded, ip -s link counters, loopback throughput tests |
| 5 | [lab-load-clinic.md](lab-load-clinic.md) | **The clinic:** four workloads + crossover round, diagnose-then-verify truth notes |

## Practice

- [Quiz](quiz.md) (20 Q, evidence-chain graded) → [answer key](quiz-answers.md)
- [Challenges C1–C8](challenges.md) — trend decoding, nice differential, cache
  theater, IOPS ceiling quantification, peak-RSS census, counter forensics,
  the two-sentence incident note, the shared-server performance policy

## The clinic contract

- Load comes only from the lab's own scripts: nice-19 CPU burners, capped
  memory growth with cleanup, dd churn into `~/lab24/`, loopback-only
  network tests. Every script has a timeout; every round ends with a
  `pgrep` census.
- No tuning of system settings (`sysctl`, swappiness, governors) — this
  clinic *diagnoses*, it doesn't tune. Tuning discussions are marked as
  "what your admin would decide".
- Every claim in `lab-log.md` cites the command that produced the number.
  A diagnosis without evidence is a guess with punctuation.

**Where this feeds forward:** the
[Linux Performance & Troubleshooting capstone](../../../M23-linux-performance-troubleshooting/content/README.md)
assumes exactly these evidence chains — this clinic is its warm-up.

Up next: [Lesson 1 — CPU performance](01-cpu-performance.md)
