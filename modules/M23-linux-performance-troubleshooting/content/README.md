# Module 23 — Linux Performance & Troubleshooting · Content Index

> Unit 6 capstone · Difficulty: Advanced
> Time: ~7 hours total · Environment: your own VM
> Prerequisites: [M18](../../M18-processes-jobs-signals/README.md), [M20](../../M20-systemd-services/README.md), [M21](../../M21-networking-fundamentals/README.md), [M24](../../M24-logs-journald-monitoring/README.md) incl. the [Performance Clinic](../../M24-logs-journald-monitoring/content/performance/README.md)

Twenty-eight modules of tools; one module of *method*. This is where
the course's scattered troubleshooting wisdom — the symptom tables,
the evidence rules, the six-rung network ladder, the incident method —
consolidates into a single repeatable practice, then gets stress-tested
against the twelve failures a working data scientist actually meets.

**The module's premise:** troubleshooting is not a bag of commands —
every previous module gave you those. It is an *order of operations*
that keeps you honest when stressed, and a *documentation habit* that
converts each incident into institutional memory.

## Files in this module

| Path | Contents |
|---|---|
| [lessons/01-methodology.md](lessons/01-methodology.md) | The eight-step methodology, with anti-patterns and the evidence journal |
| [scenarios/](scenarios/) | **Twelve drill cards** — each: symptom → decision tree → evidence commands → fix → verify → document |
| [labs/README.md](labs/README.md) | **The Drill Book** — four staged, independent incidents graded on method |
| [practice/quiz.md](practice/quiz.md) → [quiz-answers.md](practice/quiz-answers.md) | 22 questions, method-graded |
| [practice/challenges.md](practice/challenges.md) | Eight challenges, C1 (drills) → C8 (design) |

## The twelve scenarios (drill cards)

**System & resources:**
1. [Server is slow](scenarios/01-server-slow.md) — the general case: which resource?
2. [Disk full](scenarios/02-disk-full.md) — including deleted-open and inode traps
3. [Memory exhausted](scenarios/03-memory-exhausted.md) — swap churn, OOM post-mortems
4. [CPU saturated](scenarios/04-cpu-saturation.md) — real vs masquerading load
5. [Process hanging](scenarios/05-process-hanging.md) — D-state, wedged pipes, signals
6. [Service failed](scenarios/06-service-failed.md) — systemctl → journalctl chain

**Network:**
7. [DNS failure](scenarios/07-dns-failure.md) — the M21 ladder's DNS rungs
8. [Connectivity failure](scenarios/08-connectivity-failure.md) — link → route → port

**Environment & access:**
9. [Permission failure](scenarios/09-permission-failure.md) — EACCES forensics, namei
10. [Python environment failure](scenarios/10-python-env-failure.md) — the M27 split-brains
11. [Package installation failure](scenarios/11-package-install-failure.md) — apt & pip classes
12. [Jupyter unavailable](scenarios/12-jupyter-unavailable.md) — the composite: kernel, server, tunnel, auth

Each card is deliberately *short*: a flowchart, six to ten commands,
a verify step, and the documentation template. Depth lives in the
linked source modules; the card is the reflex.

## How to use this module

1. Read the methodology lesson once, slowly.
2. Work 3–4 drill cards per sitting; self-assess each against its
   "done when".
3. Take the quiz.
4. **The Drill Book** — book a 2-hour block, run all four incidents
   fresh (no peeking), grade yourself on method, not speed.

## The safety contract (same as every module)

- Incidents are staged **by you, on your VM** — the Drill Book's setup
  scripts create the broken states; nothing here asks you to break a
  system unit, edit `/etc/fstab`, or touch another user's data.
- Fixes are revertible by construction: user-scope services (M20), own
  venvs (M27), own containers (M28), own directories.
- Destructive commands appear in cards only with their blast radius
  stated, per the course's M06-era rule.
