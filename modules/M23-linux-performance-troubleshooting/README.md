# M23-Clinic — Linux Performance & Troubleshooting

> Unit 6 capstone companion · Difficulty: Advanced
> Prerequisites: M18, M20, M21, M24 (the Performance Clinic extension is assumed knowledge)
> Note: the *numbered* M23 in the roadmap is File Transfer; this directory is
> the clinic companion to it (see [COURSE-ROADMAP.md](../../COURSE-ROADMAP.md),
> Unit 6 notes).

## What this module covers

The capstone of diagnosis: the **eight-step troubleshooting methodology**
practiced end-to-end, and the **twelve canonical failure scenarios** of
Linux data-science work — each as a *drill card* (symptom → decision
tree → evidence → fix → verify → document) that reuses the ten-pattern
troubleshooting guides already built across M08–M28.

**Start here:** [content/README.md](content/README.md) — the module index.

| Piece | What you get |
|---|---|
| [Lesson — the eight-step methodology](content/lessons/01-methodology.md) | Define → evidence → component → hypotheses → safe test → fix → verify → document |
| [Scenario drill cards](content/scenarios/) | 12 drill cards across system, network, environment, and service failures |
| [The drill book](content/labs/README.md) | The multi-incident capstone lab: staged incidents, evidence-graded |
| [Practice](../M01-what-is-linux/content/practice/README.md) | Quiz + key, challenges |

## Safety contract

- Every scenario runs **on your own VM**, broken by *you*, fixed by *you*
- No scenario requires breaking system units, editing `/etc/fstab`, or
  touching another user's data
- The drill book's incidents are staged in your own user-scope services
  (M20), your own venvs (M27), your own containers (M28)

Definition of done: all four drill-book incidents solved with the
eight-step method evidenced in `lab-log.md`; ≥ 8 of 12 drill cards
self-assessed; quiz ≥ 16/22.

Module links: [COURSE-ROADMAP.md](../../COURSE-ROADMAP.md) ·
[SETUP.md](../../SETUP.md) · [CONTRIBUTING.md](../../CONTRIBUTING.md)
