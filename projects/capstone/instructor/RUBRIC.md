# Capstone Rubric — 100 Points (Instructor Edition)

> Evidence-based: if it isn't demonstrated (log, transcript, diff, live demo),
> it doesn't score. Partial credit follows the tables. Pairs with
> [VIVA.md](VIVA.md) and [INCIDENTS.md](INCIDENTS.md).

## Phase weighting

| Phase | Weight | When |
|---|---|---|
| 1. Proposal | 5% | week 1 |
| 2. Build | 25% | weeks 2–3 (rubric areas 1–4) |
| 3. Operate | 30% | week 4 (areas 5–7, 9) |
| 4. Document | 20% | week 5 (areas 8–10) |
| 5. Demo + viva | 20% | week 5 (protocol below + VIVA bank) |

The area scores below are the 100-point rubric applied at phase
checkpoints; record checkpoint scores per phase and average with the
weights (a phase-3 incident disaster caps the final at B-range even if
week-5 polish is perfect — operating is the point).

## Area rubric

| # | Area | Pts | Full credit | Common gaps |
|---|---|---|---|---|
| 1 | Pipeline correctness | 15 | Scheduled runs complete end-to-end; ≥3 logged runs; validation report produced; dirty rows **quarantined with evidence**; idempotency proven (double-run, no drift) | silent row drops; runs only ever run by hand |
| 2 | Storage design | 8 | Designed layout documented; dedicated volume with `nofail` (or justified alternative); DB loaded via `\copy`; usage visible | layout invented after the fact; no volume rationale |
| 3 | Model job | 8 | Pinned env; scripted train; artifact + metadata sidecar (code SHA, data checksum, config); run logged; < 2 min CPU | unpinned env; artifact without provenance |
| 4 | Serving stack | 12 | API as systemd user unit behind nginx; health endpoint; survives `systemctl --user restart`; 502 diagnosed live if induced | root-run service; "it works" without restart-survival proof |
| 5 | Security hardening | 12 | M25 checklist applied *with evidence*; SSH key-only + rollback documented; secrets in `600` env files outside repo; ufw minimal + justified; permission matrix matches `namei -l` reality | checklist *claimed* not shown; one "temporary" port open |
| 6 | Observability | 10 | `health.sh` accurate; structured, queryable logs; watchdog CSV; operator answers "what happened at 02:00?" from logs alone, in under a minute | prose logs; health script that never ran |
| 7 | Backup & restore | 10 | Snapshots + DB dump on second location; retention stated; **restore performed, diff-verified, model-loads proven, RTO timed** | the rumor backup — snapshots never restored (score 0, per non-negotiables) |
| 8 | Reproducibility | 8 | Fresh clone → working system in ≤ documented steps; a classmate's successful rebuild cited; Docker track: image tagged by SHA, compose healthchecks | "steps" that skip the hard part (secrets placement, volume setup) |
| 9 | Documentation | 12 | Runbook passes the **peer test** (peer performs 2 ops using only the doc); architecture diagram complete; incident report follows the eight-step method with quoted evidence | runbook written week 5 from memory; aspirational commands never run |
| 10 | Git hygiene | 5 | Small described commits; sensible branches; no secrets, no bulk data, no generated junk | mega-commits; `.venv`/datasets committed |

## Non-negotiables (automatic deductions)

- **Secret committed to Git:** −15 + mandatory history-remediation exercise
  (rewrite demo on a scratch clone + rotation plan).
- **Restore claim without a performed restore test:** backup area scores 0.
- **Destructive commands without safeguards** (dry-run/snapshot/explicit
  paths): −10 first occurrence.
- **`curl | sudo bash`-class patterns** in shipped scripts: −10.
- **Service running as root** where a user unit was available: −5 (area 4).

## Live demo protocol (10 minutes — both rubric and viva gate)

1. **Healthy system** (2 min): health report + service status — the student
   narrates *what each line means*.
2. **Pipeline run** (2 min): trigger live, or show the three most recent
   logged runs end-to-end.
3. **Break & recover** (4 min): instructor picks one benign break (kill the
   API / fill a small partition / corrupt a config); student recovers **using
   their own runbook**, narrating with the eight-step method's vocabulary.
   Grading: recovery + *narration quality* (evidence-first, no flailing).
4. **Log query** (2 min): one question about last night's run answered from
   logs alone.

Demo scoring: 10 points within the phase-5 weight; a failed recovery that
*still narrates correctly* earns partial — flailing without method earns
none, regardless of eventual success.

## Viva (10 minutes)

Draw 4–6 questions from [VIVA.md](VIVA.md) across at least three outcome
areas (LO1–LO9), always including one from **security** and one from
**recovery**. Grade 0–5 per answer on the rubric: 5 = names the mechanism
*and* the evidence source; 3 = correct mechanism, vague evidence; 1 = the
command without the why; 0 = the memorized incantation.

## Grade bands

| Band | Meaning |
|---|---|
| 90–100 | Boringly reliable: runs, logs, restores, and explains itself. Ready for a real team. |
| 75–89 | Solid, with gaps in one or two operational areas (usually restore testing or runbook depth). |
| 60–74 | Core pipeline works; operations thin (monitoring/backups/docs incomplete). |
| < 60 | Unstable or evidence missing. Retake with fixes; the rubric doubles as the improvement list. |

## Academic integrity notes

- The **injected incident** must be diagnosed from *evidence gathered after
  injection* — a pre-written report reproducing the incident at home is
  detectable (timestamps) and scores 0 for area 9's incident quality.
- Classmate rebuild citations must be honest — the rebuilder's own log is the
  citation; rubric-area 8 requires *their* artifact, not a claim.
- Collaboration on *concepts* is the course's culture; collaboration on
  *artifacts* is plagiarism. The viva resolves ambiguity: the student who
  built it can defend any line they submitted.
