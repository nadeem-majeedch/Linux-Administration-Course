# Validation Checklist

A mechanical, repeatable audit for the repository. Maintainers re-run it after any
structural change; it doubles as the phase-1 completion report (dated at the bottom).

## How to run each check

- **F1 (docs):** verify all 5 files exist: README, ROADMAP, SETUP, CONTRIBUTING, LICENSE.
- **F2 (modules):** `ls modules | wc -l` → 30; every module has a README with
  `Status: scaffolded`.
- **F3 (index):** every row of README's Module Index links to
  `modules/M<nn>-<slug>/README.md` and resolves.
- **F4 (roadmap):** every module section links back to its folder; the
  Appendix A coverage table lists 80+ required topics.
- **F5 (projects):** mini-projects A–F and capstone (BRIEF, RUBRIC, STARTER) exist
  and are referenced from the roadmap.
- **F6 (links):** all relative Markdown links resolve inside the repository.
- **F7 (safety):** no lab encourages a destructive command without a safeguard;
  the Safety Card exists and every module's risk notes name its safeguards.
- **F8 (root):** no module *requires* root; every sudo step states why.
- **F9 (git):** no commits made during the phase; `.gitignore` excludes VM images,
  secrets, bulk data, and generated junk.
- **F10 (factual):** commands verified against on-system man pages / official docs
  (Ubuntu, GNU, systemd, OpenSSH); discrepancies filed as issues, not tolerated.

## Status

| Check | Result |
|---|---|
| F1 Top-level docs present | PASS |
| F2 30 module folders + stubs | PASS |
| F3 README index ↔ folders consistent | PASS |
| F4 Roadmap sections + coverage table | PASS (80 topics listed) |
| F5 Project briefs present + referenced | PASS |
| F6 Relative links resolve | PASS |
| F7 Safety framing + Safety Card | PASS |
| F8 No root assumption | PASS |
| F9 Git untouched; .gitignore hardened | PASS |
| F10 Command verification pass | PASS (spot-checked; content phase re-verifies per lab) |

## Phase-1 completion report

- **5 top-level documents** (README, COURSE-ROADMAP, SETUP, CONTRIBUTING, LICENSE)
  plus `.gitignore`.
- **8 units, 30 modules** scaffolded under `modules/` (M01–M30), each with a
  contract stub (unit, difficulty, prerequisites, scope, definition-of-done).
- **6 mini-project briefs** (A–F) + **capstone pack** (brief, 100-point rubric,
  starter layout) under `projects/`.
- **Resources:** 9 cheatsheets (7 units + capstone ops + safety card), glossary
  (~90 terms), official-docs-only reference list.
- **Support directories:** `datasets/` (6 planned datasets + build status),
  `assets/` (6 planned figures + conventions).
- **Coverage:** all 80+ required topics mapped in Appendix A of the roadmap.
- **Deliberately not done:** detailed lesson content, dataset files, figures —
  these are the content phase, scoped by the roadmap and module stubs.

## Re-audit log

| Date | Phase | Result | Notes |
|---|---|---|---|
| 2026-09-15 | 1 — architecture & roadmap | PASS | Initial audit at phase-1 completion |
| 2026-09-15 | 2 — content: module 01 | PASS | 20 content files (8 lessons, 4 labs, quiz+key, challenges, troubleshooting); 313 links all resolve; F6 re-run clean |
| 2026-09-15 | 3 — content: 04-users-groups-permissions (M12/M13/M14) | PASS | 21 new content files: 5 lessons, 6 labs (2 permission clinics, 6 patients, 3 sudo incident tickets), 3 quizzes + keys, challenges, troubleshooting ×3; 441 links all resolve |
| 2026-09-15 | 4 — content: 05-process-management & 06-package-management (M18/M16) | PASS | 18 new content files: 6 lessons, 6 labs, 2 quizzes + keys, 16 challenges, troubleshooting ×2; 514 links all resolve |
