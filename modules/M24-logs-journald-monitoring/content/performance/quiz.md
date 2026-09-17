# Performance Clinic Quiz — CPU, Memory, Disk I/O, Network

> 20 questions. Answer first, then check [quiz-answers.md](quiz-answers.md).
> Scope: clinic lessons 1–4 + the Load Clinic. Evidence-chain rules
> count as quiz material.

## Section A — CPU (Q1–5)

**Q1.** Load average 6.0 on 4 cores with `top` showing 15% `us` and 45%
`wa`. Is the CPU the bottleneck? Name the two numbers that redirect
the diagnosis and where they lead.

**Q2.** Decode `%ni` — what shows up there, and why would a well-run
shared server want its batch jobs visible in that column?

**Q3.** What is the run-queue field `3/987` in `/proc/loadavg` saying,
and why is it a more honest "right now" than the 15-minute load?

**Q4.** `/usr/bin/time -v` on a workload: user 40 s, sys 6 s, wall 240
s. Classify the delay and name the instrument that finds its cause.

**Q5.** A colleague's "Python script" pegs 400% CPU on a shared box.
Explain the mechanism, and name the two courtesy options (one from
M18, one from M28).

## Section B — memory & swap (Q6–10)

**Q6.** `free -h`: `free` 300M, `buff/cache` 2.8G, `available` 5.2G.
State the diagnosis and the column that earns it.

**Q7.** Swap `used` = 1 GB with `si/so` = 0 for an hour. Problem or
history? What would upgrade it to a problem?

**Q8.** List the OOM sequence's four stages in order, and give the one
command pair that finds the kernel's verdict after a victim dies.

**Q9.** Why is VSZ (total-vm) misleading for pandas workloads, and
which two numbers do you quote instead?

**Q10.** A process shows rising major faults (`majfl/s`) mid-run. What
is physically happening, and which two resources sit on either side of
that event?

## Section C — disk I/O (Q11–15)

**Q11.** `await` 4 ms, `%util` 97%, `aqu-sz` 1.2 during a nightly
import. Sick or employed? Defend with all three numbers.

**Q12.** Avg write size = 4 KB. What workload class is this, and which
resource ceiling does it exhaust first on most storage?

**Q13.** `df -h` shows 400M free; `du` accounts for 30G less than the
filesystem total. Name the mechanism and why the space won't return
while the writer runs.

**Q14.** `pip install` fails "No space left on device" but `df -h` is
fine. Which check runs next, and what does it reveal?

**Q15.** Why does a *dropped* `await` after removing one cron job prove
more than a `wait`-and-see? (Think: evidence, intervention, causality.)

## Section D — network & synthesis (Q16–20)

**Q16.** Split "the network is slow" into its three measurable
properties and name one instrument for each.

**Q17.** `curl 127.0.0.1` is slow on a "network problem" box. What do
you check first, and what does that result prove about the network
hypothesis?

**Q18.** TX `dropped` climbs 12 → 800 during a large rsync. Mechanism
in one sentence, plus who owns the fix.

**Q19.** Thousands of sockets in TIME-WAIT vs thousands in CLOSE-WAIT:
which is healthy, which is a leak, and what is each state *saying*?

**Q20.** The Load Clinic's Round E ran CPU burners and I/O churn
together. Write the two-sentence verdict format you'd stand behind —
including which number *confirmed* vs which *led*.

Check answers: [quiz-answers.md](quiz-answers.md) ·
Practice more: [challenges.md](challenges.md)
