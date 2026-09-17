# Consolidated Viva Bank

> Oral-examination questions for the capstone defense. The full,
> module-mapped bank with grading probes lives in
> [`projects/capstone/instructor/VIVA.md`](../projects/capstone/instructor/VIVA.md)
> (29 questions, follow-up probes, full-credit markers). This page is
> the examiner's quick index: the spine of that bank plus the
> follow-up discipline.

## The spine (one question per course pillar)

| # | Pillar | Spine question | Probes toward |
|---|---|---|---|
| 1 | Foundations | Your VM has 4 GiB. Walk me through what the installer *and* you each chose, and why those choices constrain every lab after. | M01–M04 |
| 2 | Files & paths | Show me a symlink and a hard link in your repo. What breaks if I `rsync` each across filesystems? | M06–M07 |
| 3 | Permissions | Your dataset dir is group-writable. Prove to me *why* your colleague can't accidentally delete your file — or concede they can. | M12–M13 |
| 4 | sudo | Read me your sudo drop-in. What can the service account do that it shouldn't — and what did you scope? | M14 |
| 5 | Scripting | Your pipeline script re-runs after a crash. Show me the mechanism that makes that safe, then the run that proves it. | M10–M11, M16 |
| 6 | Storage | `df` and `du` disagree on your box. Walk me through settling it live. | M17 |
| 7 | Services | Your unit failed overnight. Which journal line decided your fix, and why that one? | M20, M24 |
| 8 | Networking | Your API is `curl`-able locally, dead remotely. First three commands, in order, and what each rules out. | M21 |
| 9 | SSH/security | Why is password auth off, what breaks because of it, and what's your documented rollback? | M22, M25 |
| 10 | Scheduling/backup | Restore the file I name, from backup, now. Then tell me when you *last* drilled this. | M19, M23 |
| 11 | Python env | Your venv runs from cron but not systemd (or vice versa). Diagnose aloud. | M15, M27 |
| 12 | Git | Show me history that contains no secrets and *proves* it. | M26 |
| 13 | Docker | Your container and your unit serve the same app. What does each restart policy actually promise? | M28 |
| 14 | Capstone integration | A classmate reproduces your run from your repo alone. What did they need that you almost forgot to commit? | M30–M31 |

## Follow-up discipline

Every spine question carries three graded probes in the full bank:

1. **The evidence probe** — "show me the command/output" (claims
   score zero; this probe is where memorizers surface).
2. **The trade-off probe** — "what does that choice cost you?" (a
   student who can't state a cost memorized the rule).
3. **The failure probe** — "how does this break at 3 a.m.?" (moves
   the answer from recital to operation).

## Grading

Full bank: 29 questions, 100 points, rubric in
[`projects/capstone/instructor/VIVA.md`](../projects/capstone/instructor/VIVA.md).
Spine questions are the required 14; examiners sample the rest by
the student's capstone architecture. Pass rule: no pillar left at
zero with claims-only answers.
