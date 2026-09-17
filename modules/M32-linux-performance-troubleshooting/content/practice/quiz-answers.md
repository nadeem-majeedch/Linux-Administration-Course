# Module 23 Quiz — Answer Key

> Method-graded: any wording demonstrating the reasoning earns credit.

## Section A — the methodology

**Q1.** Define → Evidence → Component → Hypotheses → Test safely →
Fix → Verify → Document. The fatal reordering is *fixing before
evidence* (6 before 2): the casual restart destroys the journal tail,
exit codes, and open-state evidence that would have named the cause —
converting one diagnosable failure into recurring mystery.

**Q2.** *What* is broken (the observable failure, specifically),
*since when* (correlates with journal/deploy timeline), *for whom /
what scope* (one user vs system-wide changes which ladders apply).
Scope changes the ladder; timing changes the evidence window; the
"what" decides whether it's even this incident.

**Q3.** Because some evidence is *state*, not record: (1) the
journal's final lines / dmesg tail with the original stack trace and
exit code; (2) live process state — open FDs, memory maps, the exact
`ss`/`ps` fingerprint of the wedged service. Both evaporate on
restart; both are the diagnosis.

**Q4.** Testable (you can name the confirming/killing command),
specific (names the exact misconfiguration), ranked (explicit order
by probability × cheapness). "The venv lost pandas" is testable
(`.venv/bin/python -c "import pandas"`); "misconfigured somehow" is a
story until it names a config and a check — it's not yet a
hypothesis.

**Q5.** One sentence spoken *before* the mutating command: what it
can affect and what the undo is ("`systemctl --user restart X` affects
only my user unit; undo is restart again"). Before, because its whole
value is consent-and-reversibility *prior* to the change — after, it's
just a confession.

**Q6.** It verifies the *process*, not the *symptom*. The original
claim was client-side reachability; verification must traverse the
same path — tunnel up, `curl` from the client machine returning the
expected code, notebook opens and a kernel cell runs. Green systemctl
is step 7's layer-one, at best.

## Section B — performance signatures

**Q7.** The disk, not the CPU: `wa` 42% (CPU idle *with* pending I/O)
and load 7.0 on 4 cores counts those uninterruptible waits. Confirm
with `iostat -xz`: expect high `await`/`%util`.

**Q8.** Size = how much swap is *occupied* (history — cold pages
evicted sometime); activity = pages *moving now*. Symptom columns:
`vmstat`'s `si/so` — sustained non-zero is thrashing; `swpd` alone is
not.

**Q9.** The OOM killer (137 = 128+9, SIGKILL, and in containers the
cgroup variant). Verdict: `journalctl -k --since -1h | grep -i oom` (or
`dmesg -T | grep -i oom`) — the line names victim, PID, size.

**Q10.** First is *busy* (saturated but delivering: shallow queue,
normal latency); second is *sick*/congested (`await` 90 ms with queue
6 — requests piling far beyond the device's service rate). `%util`
alone can't distinguish them; queue depth + latency vs baseline does.

**Q11.** Healthy: Linux uses spare RAM as page cache (`buff/cache`),
which is reclaimable instantly — `available` is the honest headroom
number, and 5.0G is plenty.

**Q12.** The TX ring buffer filled faster than the interface drained
it — burst/saturation over buffer capacity; zero `errors` exonerates
the physical layer. Owner: the link/buffer configuration — the
admin's layer, handed over with the before/after counter deltas.

## Section C — the cards

**Q13.** Order: `uptime` (ratio + trend) → `vmstat` (all four
resources' tells in one glance) → `top` (the CPU row + who) → `free`
(available) → `iostat` (if `wa`/`b` pointed at disk). The redirecting
column: `wa` — the CPU report card's disk fingerprint.

**Q14.** Deleted-but-open: blocks held by an unlinked-but-open file —
`lsof +L1` (or `/proc/*/fd` hunt) finds the holder. `rm` of the
*(already unlinked)* name is a no-op; the space returns only when the
*holder* closes/exits — stop the writer first.

**Q15.** `ls -l` shows one object's mode; "denied" can come from *any*
component of the path (a parent's missing `x` is the classic).
`namei -l` walks every component and marks the denying level — it
localizes the failure instead of re-describing the symptom.

**Q16.** It's enforcing PEP 668 — protecting apt-managed system
Python from pip clobbering it. The fix, two words: **the venv**.

**Q17.** The application gets the `getent` answer — nsswitch consults
`/etc/hosts` before the resolver, and `getent` reproduces exactly
that ordering. The file: `/etc/hosts` — the override layer everyone
forgets they have.

**Q18.** An older server still runs and *owns the port*; the newer
launch couldn't bind and (per the M27 pattern) its error went to a
log nobody tails. The `ps`/`ss` asymmetry is the tell: two
processes, one listener — kill the stale PID politely, start one
server.

## Section D — synthesis

**Q19.** The method treats verification (step 7) as the gate: the
first fix was *a* cause, not *the* cause, and verify-against-original-
symptom is precisely the mechanism that forces hypothesis #2 instead
of declaring victory. Stopping after one fix trades a two-line
investigation for a recurring ticket.

**Q20.** (1) `crontab -l` — is the line even installed (rules out
never-scheduled); (2) `journalctl -u cron --since -24h` (or
`grep CRON /var/log/syslog`) — did cron *invoke* it, with what exit
(rules out scheduler vs script); (3) `env -i HOME=… PATH=/usr/bin:/bin
/abs/path/script.sh` — the cron-environment rehearsal (rules out
PATH/venv/shebang assumptions). Order matters: cheapest, most
exonerating first.

**Q21.** Because the *cost* of an incident is its recurrence risk — a
fix without a canary is a repair, not a resolution. Concrete canary
for card 2: a cron'd `df -h` threshold check on the analysis
filesystem that logs at 80% and pages at 90% (M24's health.sh
pattern) — the next "disk full" arrives as a warning, not an outage.

**Q22.** "The API failed after the venv was recreated without pinned
dependencies; the journal's final line was
`ModuleNotFoundError: pandas` (exit 1), confirmed by `pip list` in the
venv. Recreated the venv from `requirements.txt` and re-registered
the kernel; health endpoint returned 200 through the original URL.
Prevention: `pip freeze` is part of the deploy, and the unit's
ExecStart uses the absolute venv python path."

Practice more: [challenges.md](challenges.md) ·
Back to the [module index](../README.md)
