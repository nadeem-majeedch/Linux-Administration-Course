# Lesson — The Eight-Step Troubleshooting Methodology

> Module 23 · Unit 6 capstone · Difficulty: Advanced
> Reading time: ~30 min · Applied throughout: the [drill cards](../README.md#the-twelve-scenarios-drill-cards) and [The Drill Book](../labs/README.md)
> Prerequisites: [M24's six-step incident method](../../../M24-logs-journald-monitoring/content/lessons/04-incident-methodology.md) — this lesson generalizes and extends it

---

## 0. Why a methodology at all (recap, then extend)

M24 Lesson 4 said it plainly: under pressure, the untrained run random
commands ("have you tried restarting?"), form theories before facts
("it's definitely DNS"), and fix symptoms while the cause survives.
This module's eight steps exist as *the thing you do instead* — the
extension from six steps adds the two that make troubleshooting a
*practice* rather than a rescue: **testing hypotheses safely** (most
skipped step) and **documenting** (the one that turns incidents into
institutional memory).

The steps are a loop, not a line — but the *order* is load-bearing:

```text
1 Define  →  2 Evidence  →  3 Component  →  4 Hypotheses
                                                 │
8 Document ←  7 Verify  ←  6 Fix  ←  5 Test safely
```

## 1. Define the problem

**Deliverable: one sentence a stranger could act on.** Not "it's
broken" but *what* is broken, *for whom*, *since when*:

> "Since ~14:00, the shared analysis server's Jupyter (port 8888) is
> unreachable from the office network; SSH still works."

Squeeze out three facts at definition time — they shape everything
after: **what changed** (deploy, update, new dataset, nothing known?),
**scope** (one user, one service, the whole box?), and **when**
(correlate with M24's journal timeline). The discipline: *write the
sentence before typing any command.* If you can't, you don't yet know
what you're troubleshooting — and that's fine; defining it is step 1.

## 2. Gather evidence (before theorizing)

Evidence first; theories earn their place only *on top* of evidence.

- **Read-only commands are free**: `uptime`, `free -h`, `df -h`, `ss
  -tlnp`, `systemctl status`, `journalctl -u X --since -2h`, `ip -s
  link`. Take the snapshot set *before* anything mutates state — some
  evidence evaporates (PIDs die, caches flush, logs rotate).
- **Time-ordering is evidence**: `journalctl --since "-3h"` and read
  *what happened when* — M24's timeline skill. Incidents are stories;
  stories have sequence.
- **Write it down as you go**: the evidence journal (§6 of this
  lesson) is filled during step 2, not reconstructed at the end.
- **The performance floor**: on "it's slow", run the Performance
  Clinic's four-instrument sweep (load/`top`, `free`+`vmstat`,
  `iostat`, `ip -s link`) — ten commands that exonerate or indict each
  resource in order.

> 🟡 The "snapshot before you touch anything" rule has saved more
> admins than any tool: the first `restart` destroys the very state
> that would have explained the failure.

## 3. Identify the affected component

Reduce the system to the **layer** that's actually failing. The course
gives you a ladder for each family:

| Family | The ladder (test top-down or bottom-up) |
|---|---|
| Network | link → IP → route → DNS → port → application ([M21's six rungs](../../../M21-networking-fundamentals/content/README.md)) |
| Storage | space (`df`) → inodes (`df -i`) → latency (`iostat await`) → health vs busy |
| Compute | load vs cores → run queue → who (`pidstat`) → waiting-on-what (`wa`, D-state) |
| Services | unit enabled? → active? → exit code → journal tail → dependency ([M20](../../../M20-systemd-services/content/README.md)) |
| Identity | whoami → membership (`id`) → mode bits → ACL/parent (`namei -l`) (M13) |
| Python | which python → which kernel → which venv → which pip (M27's split-brains) |

The drill cards (§ of this module) are these ladders
pre-chewed per scenario. The skill this step trains is *choosing the
ladder* — one symptom, one family; don't grep the whole system when
`ss -tlnp` answers in one line.

## 4. Form hypotheses (plural)

From the evidence, write **two or three candidate causes**, ranked by
probability and cheapness-to-test:

> Evidence: Jupyter unreachable; `ss -tlnp` shows nothing on 8888;
> `systemctl --user status jupyter` says *failed (exit 1)*; journal
> tail: `ModuleNotFoundError: pandas`.
>
> H1 (likely): the service's venv lost pandas (env drift).
> H2: wrong interpreter in the unit's ExecStart.
> H3: port conflict — something else bound 8888 first.

Rules for good hypotheses: **each is testable** (you can name the
command that would confirm/kill it), **each is specific** ("the unit
points at system python" not "python is broken"), and **ranking is
explicit** (test cheapest-and-most-likely first). A hypothesis you
can't test is a story, not a hypothesis.

## 5. Test safely (the step everyone skips)

The difference between an admin and an admin-shaped liability:

- **Prefer read-only tests**: `ss`, `cat` the unit, `python3 -c
  "import pandas"` in the suspect venv, `journalctl -b -u X`. Most
  hypotheses die here, without touching anything.
- **Test one variable at a time** — the C7 lesson from the Performance
  Clinic: change one thing, re-measure, keep the before/after.
- **Reversibility before action**: for any mutating test, know the
  undo *before* doing it. `systemctl --user restart` (safe, restarts
  again), `mv` instead of `rm` (renames are undoable), container/venv
  recreation from pinned files (M27/M28's whole point).
- **Snapshot first** (§2): if the test might change state, the
  pre-state is already in your journal.
- **The blast-radius sentence**: say what the command can affect.
  "`systemctl --user restart jupyter` affects only my user service" is
  a safe test; `sudo systemctl restart postgresql` on a shared box is
  a *conversation*, not a test.

## 6. Fix (the smallest sufficient change)

The fix should be **proportionate, principled, and principled *why***:

- Smallest change that addresses the *cause* — not the symptom. The
  service died of missing pandas: fix the venv/pin, don't wrap the
  unit in `|| true` retries.
- Prefer declarative fixes: pin the requirement (M27), fix the unit
  file (M20), correct the mode bits (M13) — imperative one-off patches
  rot.
- **One fix at a time**, even when confident. Two simultaneous changes
  and the next failure is unattributable.
- If the "fix" needs `sudo rm`-class actions or history rewrites
  (M26's rule) — stop. Escalation table, M24 §9: some fixes belong to
  other people, and evidence-not-mood is how you hand them over.

## 7. Verify

**Verify the *original* symptom, not the patch's local effect** — the
step that separates "seems better" from "fixed":

> Original: "Jupyter unreachable from the office." Verification isn't
> `systemctl status` green — it's `curl -s -o /dev/null -w '%{http_code}'
> http://127.0.0.1:8888` *from the client's path* (the tunnel), returning
> 200. M21 Lab 2's diagnosis reports, M24's incident method, and the
> capstone's [Lab 3](../../../M26-git-dev-workflows/content/labs/lab-03-end-to-end-ds-workflow.md)
> all grade exactly this.

Add the regression check: what would have *caught this earlier*? (A
healthcheck, a cron'd `pg_isready`, a disk threshold.) Verification
that doesn't leave a canary behind is half a verification.

## 8. Document

The step that pays your whole career. The template (the drill cards
end with it; the Drill Book grades it):

```markdown
## Incident: <one-line title>  (date, VM/host)
**Symptom:** <the step-1 sentence>
**Evidence:** <commands + key outputs, time-ordered>
**Root cause:** <the specific cause the evidence supported>
**Fix:** <the change made, and why it's the cause not the symptom>
**Verification:** <the check that reproduced the ORIGINAL symptom's absence>
**Prevention:** <the canary/threshold/habit that catches it next time>
```

Three properties of good documentation: a *stranger* could follow it;
the **root cause is named** (not "restart fixed it" — why did restart
fix it?); and **prevention is concrete** (a command, a threshold, a
file), because "be careful" is not a control.

## The evidence journal (the habit under all eight steps)

One file, `lab-log.md`, kept since M24; in incidents it gains a
structure: *timestamped entries, command → output → inference*, with
inferences marked as such (`// inference:`). The journal is why step 8
takes ten minutes instead of an evening — and why postmortems can be
written by people who weren't there. In the Drill Book, the journal
**is** the deliverable.

---

## Key takeaways

- The order is load-bearing: **definition before evidence, evidence
  before hypotheses, safe tests before fixes, verification of the
  *original* symptom before closure, documentation always.**
- Every family of failure has a **ladder**; the skill is choosing the
  ladder and running its read-only rungs first.
- **Test one variable, know the undo, say the blast radius.**
- Documentation turns incidents into infrastructure: stranger-readable,
  root-caused, prevention-concrete.

## Check yourself

1. A teammate's first act on a broken service is `sudo systemctl
   restart`. Which step did they skip, and what evidence died in the
   process?
2. What makes a hypothesis *good*? Give the three properties.
3. Why is "`systemctl status` is green" an incomplete verification for
   "Jupyter unreachable from the office"?
4. What three properties does incident documentation need, and which
   step of the method supplies each?

*Answers:* (1) Step 2/5 — the snapshot and the safe test; the journal
tail with the original stack trace, exit code, and corrupted-state
evidence often vanish on restart, converting a diagnosable failure
into a mystery that recurs. (2) Testable (name the command), specific
(the exact misconfiguration), ranked (order by probability × cheapness
to test). (3) It verifies the service process, not the original
symptom — reachability from the client's path (tunnel, port, auth) is
the original claim; `curl` through that path is the verification. (4)
Stranger-readable (steps 2/5's journal), root cause named (steps 4–6's
hypothesis testing), prevention concrete (step 7's regression canary).

Next: the [twelve drill cards](../README.md#the-twelve-scenarios-drill-cards) —
the method, pre-chewed per scenario.
