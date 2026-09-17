# FINAL-TEACHING-PACKAGE-AUDIT

> **Date:** 2026-09-17 · **Scope:** the teaching package (`teaching/`, 103 files)
> plus its integration points (root `README.md`, `mkdocs.yml`,
> `scripts/build-site.sh`, `WORK-INVENTORY.md`).
> Course content untouched — **0 tracked files deleted**, verified via
> `git status`. Every status below reflects a check actually run in this
> session; nothing is claimed without an executed command.

---

## Executive summary

**Overall status: PASS WITH WARNINGS** (warnings are documented
limitations, not failures — see §Known limitations).

The teaching package is complete and integrated: a 16-week / 32-session
delivery plan, 8 unit-level slide decks with matching speaker notes, an
instructor manual (4 course guides + 8 unit teaching guides), a lab
workbook routing to the repository's 72 module labs, 10 scripted
demonstrations, an assessment layer (quiz bank v2 + key, assignments
A4–A6 + keys, exam/viva/capstone pointers, grading sheets), a student
revision room, and environment/delivery guides — all built around the
existing course content without modifying it.

| Deliverable | Files | Status |
|---|---|---|
| Teaching plan | 5 (`teaching-plan/`) | PASS |
| Lecture decks | 8 + index | PASS |
| Speaker notes | 8 + index | PASS |
| Instructor manual | 13 (`instructor-manual/`) | PASS |
| Lab workbook | 12 (`lab-workbook/`) | PASS |
| Demonstrations | 12 (`demonstrations/`) | PASS |
| Assessment layer | 16 (`assessments/`) | PASS |
| Instructor-only | 8 (`instructor-resources/`) | PASS |
| Revision room | 8 (`revision/`) | PASS |
| Setup & delivery | 5 (`setup-and-delivery/`) | PASS |
| Package docs (README, audit, nav plan) | 3 | PASS |

---

## Validation results (all executed this session)

| # | Check | Method | Result |
|---|---|---|---|
| 1 | MkDocs strict build | `bash scripts/build-site.sh && .docs-venv python -m mkdocs build --strict --clean` | **PASS** — exit 0, 0 warnings; 642 md files in `site-src` (525 course + 102 teaching + site pages) |
| 2 | `teaching/` copied into site | `ls site-src/teaching/` | PASS — byte-for-byte tree, links resolve 1:1 |
| 3 | Relative links, teaching tree | Python crawler over 528 links | **PASS — 0 broken** |
| 4 | Anchor links (GitHub slug rule) | Slug checker over 10 `#`-links | **PASS — 0 broken** |
| 5 | Code-fence balance, teaching tree | Triple-backtick parity scan, 102 files | **PASS — 0 unbalanced** |
| 6 | Shell syntax | `bash -n` over every ```bash block (7 blocks) | **PASS after 2 fixes** (Unit-03 slides: placeholder `{ ...; }` bodies made executable) |
| 7 | Workflow YAML | `yaml.safe_load`; triggers + least-privilege asserted | **PASS** — `push`→main + `workflow_dispatch`, `contents: read` |
| 8 | Build script syntax | `bash -n scripts/build-site.sh` | PASS |
| 9 | Nav leak check (keys in nav) | grep of `mkdocs.yml` for key paths | **PASS — no instructor-only file in nav** |
| 10 | Student quiz key leakage | `quiz-bank-v2.md` contains no key link/content | PASS |
| 11 | Secrets scan | Pattern scan over `teaching/**.md` | PASS — none |
| 12 | Deletion proof | `git status` deleted-file count | **PASS — 0 tracked files deleted** |
| 13 | Attendance template | CSV header sanity | PASS |

Fixes made during validation (all content-quality, not suppression):
- 5 stale/wrong link depths in teaching files (see §Inventory below).
- 2 un-runnable bash skeletons in the Unit-03 slide deck replaced with
  equivalent executable forms (placeholders `{ ...; }` → real bodies).

---

## Inventory

**Created (103 files):** the full `teaching/` tree per the map above +
root `WORK-INVENTORY.md`. Key student-facing artifacts: quiz bank v2
(120 questions, style-matched to module quizzes), assignments A4
(shell automation), A5 (network & services), A6 (DS server hardening),
each with separate key; viva prep guide; 12 troubleshooting practice
scenarios; 41-concept exam list; 20 practice questions with
hint-gated hints; last-week revision checklist.

**Modified (3 files):**
- `mkdocs.yml` — one new nav section (`Teaching Package`, 13 entries),
  placed before `About:`; existing nav untouched.
- `scripts/build-site.sh` — whitelist extended with `teaching` (one
  word, one line); byte-for-byte copy design unchanged.
- `README.md` — one Documentation bullet pointing to the teaching
  package and the instructor-only policy.

**Preserved:** all 525 course markdown files, all keys, all modules —
verified 0 deletions.

**Intentionally not changed:** CI workflow (no new assertions needed;
strict build passes on merit), `assessments/` originals (the teaching
layer links to them rather than duplicating), `accreditation/` (CLO
status remains *proposed*).

---

## CLO alignment

The teaching package references CLOs only as **proposed for
instructor review**, consistent with `accreditation/CLO-ASSESSMENT-ALIGNMENT.md`.
Assignments A4–A6 map to CLO 4/5/6 evidence; the 16-week plan's
assessment schedule references the existing exam papers. No new CLO
claims were invented.

---

## Public/private separation

- Student-facing nav includes: teaching-plan, slides, speaker notes,
  instructor manual, lab workbook, demonstrations, assessment
  framework (question papers only), revision room, setup guides.
- Excluded from nav (policy: `teaching/instructor-resources/INSTRUCTOR-ONLY.md`):
  all `*-key.md` files, `quiz-bank-v2-key.md`, `instructor-resources/`
  (grading sheets, attendance, policy).
- Enforced by nav curation; **documented honestly** that GitHub Pages
  is public and URL-guessing reaches unlisted files — the policy file
  prescribes private-repo/LMS distribution for sealed keys.
- `.docs` build whitelist means instructor-only trees still build into
  the site (for URL convenience) but appear in **no** navigation, per
  the MKDOCS-NAV-PLAN decision recorded in `teaching/MKDOCS-NAV-PLAN.md`.

---

## Known limitations (honest)

1. **Slide decks are unit-level, not per-session** — 8 decks for 32
   sessions; the 16-week plan maps sessions to deck sections. A
   per-session split is future work if a lecturer wants 1:1 decks.
2. **Assignments A4–A6 are unexercised** — written against verified
   module content and `bash -n`-checked scripts, but no cohort has
   sat them yet. Marking time estimates are informed guesses.
3. **Speaker notes match decks, not live classroom reality** — they
   encode the intended demo sequence; first delivery will surface
   timing drift (plan allocates slack, but real sections vary).
4. **Instructor-only material on a public site** remains accessible
   by URL — mitigated and documented, not solved (unsolvable on
   Pages); use the private-repo option for sealed exams.
5. **Attendance template is generic** — no SIS integration attempted.
6. **Quiz bank v2 answers live in one instructor file** — convenient,
   but graders must keep it out of projected screens; split-per-module
   keys remain the module `quiz-answers.md` files.

---

## Recommended next steps (prioritized)

1. **Dry-run Week 1** with the deck + notes + setup session against a
   fresh VM snapshot; adjust timing columns in the 16-week plan.
2. **Pilot A4** with a TA before term; calibrate its rubric anchors.
3. **Decide sealed-exam storage** (private instructor repo vs LMS) and
   execute the INSTRUCTOR-ONLY.md checklist.
4. Optional: split unit decks into 32 session files via a generator
   script if 1:1 decks are pedagogically required.
5. Optional: per-module attendance sheets with CLO roll-up for
   accreditation evidence packets.

---

**Final status: PASS WITH WARNINGS** — complete, validated, integrated;
warnings are documented limitations for the first delivery cycle, none
blocking publication.
