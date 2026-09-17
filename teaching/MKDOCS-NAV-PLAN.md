# MKDOCS-NAV-PLAN — Teaching-Package Integration

> The exact, minimal changes to the website pipeline so the teaching
> package is browsable without touching course navigation or exposing
> instructor-only material. Written before Phase 9 executes the changes.

## 1. Current pipeline (unchanged in principle)

```text
repository markdown
  └─ scripts/build-site.sh   (byte-for-byte copy of whitelisted trees → site-src/)
       └─ mkdocs build --strict  (docs_dir: site-src, curated nav in mkdocs.yml)
            └─ GitHub Pages via .github/workflows/publish.yml
```

Two whitelists exist and both must be extended in lockstep:

1. `scripts/build-site.sh` copies **only** `modules projects assessments datasets resources cheatsheets labs accreditation` (+ root pages).
2. `mkdocs.yml` nav lists specific files — unlisted files are built but unnav'd.

## 2. Change 1 — `scripts/build-site.sh` (one line)

```diff
-cp -r modules projects assessments datasets resources cheatsheets labs accreditation "$DST/"
+cp -r modules projects assessments datasets resources cheatsheets labs accreditation teaching "$DST/"
```

Byte-for-byte copying is preserved: relative links inside `teaching/`
(e.g. `../../assessments/quizzes/quiz.md`) keep resolving because the
tree shape is copied 1:1.

## 3. Change 2 — `mkdocs.yml` (one new section)

Inserted after the existing `Resources:` section and before `About:`
(exact placement keeps course nav untouched and first):

```yaml
  - Teaching Package:
      - Overview: teaching/README.md
      - 16-Week Teaching Plan: teaching/teaching-plan/16-week-course-plan.md
      - Weekly Outcomes: teaching/teaching-plan/weekly-learning-outcomes.md
      - Lecture↔Module Map: teaching/teaching-plan/lecture-to-module-mapping.md
      - Lecture Slides: teaching/lecture-slides/README.md
      - Speaker Notes: teaching/speaker-notes/README.md
      - Instructor Manual: teaching/instructor-manual/README.md
      - Lab Workbook: teaching/lab-workbook/README.md
      - Demonstrations: teaching/demonstrations/demo-index.md
      - Assessment Framework: teaching/assessments/README.md
      - Revision Room: teaching/revision/README.md
      - Setup & Delivery: teaching/setup-and-delivery/README.md
```

## 4. Public / private separation (enforced by omission)

| Material | In nav? | Rationale |
|---|---|---|
| Quiz bank v2 (questions) | yes | student-facing |
| Quiz bank v2 answer key (`teaching/assessments/quizzes/keys-instructor/`) | **no** | instructor-only |
| Assignment keys (`teaching/assessments/assignments/new/*-key.md`) | **no** | instructor-only |
| Instructor resources (`teaching/instructor-resources/**`) | **no** | instructor-only |
| Everything else in `teaching/` | yes | student-facing or instructor-facing-but-safe |

Because `mkdocs` nav is curated, unlisted files are still *reachable by
URL* if someone guesses the path. `INSTRUCTOR-ONLY.md` states this
plainly: GitHub Pages is public hosting — genuine access control
requires an LMS, a private repo, or direct distribution. The course
treats nav-omission as *hiding the candy store*, not as security.

## 5. What is explicitly NOT changed

- Existing Units/Practice/Resources nav — untouched.
- CI workflow assertions — untouched (the strict build must pass on
  merit; if it flags teaching files, content/links get fixed, not CI).
- Any module, assessment, or accreditation file — untouched.
- The README-as-index design — `teaching/` subdirectories use explicit
  nav paths (deeper directories are reachable from their parents' pages).
