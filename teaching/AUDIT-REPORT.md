# Pre-Build Audit Summary — Teaching Package

> Condensed, execution-verified audit performed 2026-09-17 before any
> teaching-package file was generated. Full detail and plans:
> root `WORK-INVENTORY.md`. Nothing in this audit is
> claimed without a corresponding command run against the working tree
> (commit `c9c5f59`, clean).

## 1. Repository shape at audit time

| Area | Finding (verified) |
|---|---|
| Modules | 32 directories, M01–M32 unique IDs, no collision (M23 collision closed 2026-09) |
| Learning content | 114 lesson pages, 72 module lab files, 29 troubleshooting pages, 30 challenge sets |
| Quizzes | 30 student quizzes, 30 instructor keys, 0 embedded answer sections |
| Cheatsheets | 31 files (20 topical in `cheatsheets/`, unit-level in `resources/cheatsheets/`) |
| Central assessment | 23 files in `assessments/` (quizzes exemplar+index, midterm/final + keys, practical exam + key + staging script, LA-1…LA-5, A1–A3, rubric/viva pointers) |
| Course labs ladder | `labs/` README + Level 1–5 circuits (5 levels) |
| Capstone | 6 files incl. instructor RUBRIC, VIVA (29 Q), INCIDENTS |
| Accreditation | 3 files — proposed CLOs, CLO×assessment alignment, module×CLO mapping, one-pager |
| Validation history | 23 entries in `resources/validation-checklist.md`; QA-REPORT, FINAL-AUDIT, FINAL-AUDIT-CLOSURE |
| Site | MkDocs strict, README-as-index, byte-copy `site-src` via `scripts/build-site.sh`, GitHub-compatible slugs |
| CI | `.github/workflows/publish.yml`: push + workflow_dispatch → generate → strict build → Pages; least-privilege |

## 2. Assessment weightings documented in-repo (reused, not invented)

Quizzes 10% · Lab assessments 10% · Assignments 3×5% · Midterm 20% ·
Final 25% · Practical 15% · Capstone per its 5-phase rubric.

## 3. Gaps the teaching package closes

G1 16-week session plan · G2 decks + speaker notes (unit-level) ·
G3 instructor manual + unit teaching guides · G4 lab workbook front-matter
(indexing existing labs) · G5 demo scripts · G6 MCQ/interpretation quiz
formats + assignment keys/rubrics · G7 gradebook/attendance/key inventory ·
G8 student revision set · G9 environment & delivery checklists ·
G10 build/nav awareness of `teaching/`.

## 4. Public/private separation policy (decided pre-build)

- Instructor-only files: `teaching/assessments/**/keys-instructor/`,
  `teaching/assessments/assignments/new/*-key.md`,
  `teaching/instructor-resources/**`.
- They receive **no mkdocs nav entries** and are linked from student pages
  only as "held by your instructor".
- `instructor-resources/INSTRUCTOR-ONLY.md` explains why GitHub Pages
  cannot enforce access and recommends LMS/private-repo distribution.

## 5. Integrity of the build

- No existing course file is rewritten; only 4 files are modified
  (build whitelist, mkdocs nav, README, validation checklist).
- All 71 planned new files are enumerated in `WORK-INVENTORY.md` §4.
- Validation battery (links, anchors, fences, `bash -n`, secrets, quiz-leak,
  nav-vs-tree diff, strict build) runs after every major phase and finally;
  results land in `FINAL-TEACHING-PACKAGE-AUDIT.md`.
