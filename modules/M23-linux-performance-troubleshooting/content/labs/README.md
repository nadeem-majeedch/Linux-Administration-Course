# The Drill Book — Four Independent Incidents

> Module 23 capstone lab · Difficulty: Advanced · Total: ~2 hours
> Environment: your own VM · Prerequisites: the [methodology](../lessons/01-methodology.md)
> and all [twelve drill cards](../README.md#the-twelve-scenarios-drill-cards)

Four incidents, staged independently, solved fresh. Each has a setup
script that *breaks something you own* in a specific, revertible way;
your job is to go from symptom to documented fix using the eight-step
method. **The grading rubric grades the method, not the speed** —
inference before action, evidence before verdict, verification of the
original symptom, documentation a stranger could follow.

## The rules

1. Run setup scripts in order, one incident at a time; **solve
   (including verification) before starting the next**.
2. Everything is in your home tree or your user-scope units (M20) —
   the scripts never touch system units, other users, or `/etc`.
3. Read the setup script *after* solving it (it's the answer key) —
   or run in "blind" mode by a classmate running setup for you.
4. The deliverable is `lab-log.md`: one eight-step block per incident.

## The incidents

| # | File | Broken | Card |
|---|------|--------|------|
| 1 | [lab-01-the-vanished-service.md](lab-01-the-vanished-service.md) | Your user-scope analysis service won't start; the reason is in the journal, the cause is in the venv | [6](../scenarios/06-service-failed.md) + [10](../scenarios/10-python-env-failure.md) |
| 2 | [lab-02-the-full-disk-that-isnt.md](lab-02-the-full-disk-that-isnt.md) | Writes fail on a loopback filesystem that `du` says is half-empty | [2](../scenarios/02-disk-full.md) |
| 3 | [lab-03-the-unresolvable-host.md](lab-03-the-unresolvable-host.md) | pip and curl resolve to the wrong place; IPs still work | [7](../scenarios/07-dns-failure.md) |
| 4 | [lab-04-the-phantom-hang.md](lab-04-the-phantom-hang.md) | A "hung" process that's stopped, a peer that died, and one red herring | [5](../scenarios/05-process-hanging.md) + [8](../scenarios/08-connectivity-failure.md) |

## Per-incident deliverable (the rubric's checklist)

- [ ] **Step 1** — the one-sentence problem definition, written *first*
- [ ] **Step 2** — evidence commands with outputs, time-ordered
- [ ] **Steps 3–4** — the named component and ≥ 2 ranked hypotheses
- [ ] **Step 5** — the safe test, its blast-radius sentence, and what
      it killed/confirmed
- [ ] **Steps 6–7** — the fix, the *undo* (if unused), and verification
      of the **original symptom**
- [ ] **Step 8** — the documentation block (stranger-readable,
      root-caused, prevention-concrete)

Score: 8 rubric items × 4 incidents = 32 points; 24+ is a pass, and
the honest self-grade is the point — the rubric is the method.
