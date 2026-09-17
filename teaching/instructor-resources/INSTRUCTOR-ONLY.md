# INSTRUCTOR-ONLY MATERIAL — Policy & Storage Guide

## Which files are instructor-only?

Anything containing answers, keys, staging instructions, rubric
thresholds, or grading guidance. Canonical list:

| Location | Nature |
|---|---|
| `modules/M*/content/practice/quiz-answers.md` (30 files) | quiz keys |
| `assessments/examinations/midterm-key.md`, `final-key.md`, `practical-key.md` | exam keys + staging |
| `assessments/quizzes/quiz-answers.md` | cross-module quiz bank key |
| `assessments/lab-assessments/LA-*/…-key.md` | lab assessment keys |
| `projects/*/RUBRIC.md`, `projects/*/SOLUTION-NOTES.md` | project grading |
| `teaching/assessments/assignments/new/*-key.md` | assignment keys (this package) |
| `teaching/assessments/quizzes/keys-instructor/` | quiz bank v2 key (this package) |
| `teaching/instructor-resources/` (all) | grading workflow sheets |
| `teaching/lecture-slides/…-slides.md` | the `Instructor Delivery Notes` sections |
| `teaching/speaker-notes/` (all) | delivery guidance |

Student-facing materials never link into these paths — verified each
release by the navigation leak check (`mkdocs.yml` review + link
crawler over student nav).

## Why the public website cannot protect these files

GitHub Pages serves **every file under the published path to anyone
with the URL**. There is no authentication, no per-path ACL, no
"hidden until enrolled" mechanism. MkDocs navigation merely *omits*
links — it does not remove pages. Concretely: a student who guesses or
shares the URL `…/teaching/instructor-resources/grading-sheets/…` can
read it.

Therefore the honest options are:

### Option A (recommended) — private instructor distribution

- **Do not deploy `teaching/instructor-resources/**` or any `*-key.md`
  to Pages at all.** The `build-site.sh` whitelist is the enforcement
  point: instructor trees are excluded from `site-src/` (see
  `scripts/build-site.sh` and `teaching/MKDOCS-NAV-PLAN.md`).
- Keys live in the **repository** for versioning, but a public
  repository + public Pages means the repo itself is also readable.
  For a genuinely closed cohort, keep the instructor materials in a
  **separate private repository** (e.g.
  `linux-admin-course-instructor`) and merge at grading time, or use
  a **private repo with Pages off** and distribute PDFs via the LMS.
- Keys that are already public in this repo's history are treated as
  *practice* keys — acceptable because the course philosophy is
  evidence-based assessment (answers are reasoning, not strings to
  memorize), but formal exam keys must never be published before the
  sitting. If this repository is public and the formal papers must
  stay sealed, move `assessments/examinations/*-key.md` to the private
  instructor repo for the term and restore after.

### Option B — LMS-only distribution

Upload per-assessment keys as LMS files restricted to the
instructor/TA role. Simple, access-controlled, no repo surgery — at
the cost of losing version control on the keys themselves.

### What is *not* an option

Relying on MkDocs nav omission, `robots.txt`, or "security through
unlisted URL" on a public Pages site. This document exists so no one
has to rediscover that the hard way.

## Practical checklist each term

1. [ ] Confirm `build-site.sh` whitelist excludes instructor trees →
       `mkdocs build --strict` output contains no key pages
2. [ ] Spot-check deployed site: search for `quiz-answers`, `-key.md`
       under the published domain
3. [ ] Distribute sealed exam keys only via Option A/B above
4. [ ] After the sitting, return keys to the repo if they were pulled
5. [ ] Audit: no secrets/tokens/passwords in any instructor file
       (they never belong in this repository at all)
