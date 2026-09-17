# Teaching Package — Linux Administration: Zero to Hero

> A complete university delivery layer around the course. The course
> content (32 modules, `COURSE-ROADMAP.md`, `assessments/`, capstone) is
> the **source of truth**; this package tells an instructor *how to
> teach it* and a student *how to prepare* — it never re-teaches or
> replaces module content.

## Package map

| Directory | What's inside | Audience |
|---|---|---|
| [teaching-plan/](teaching-plan/README.md) | 16-week plan (32 × 90-min sessions), weekly outcomes, lecture↔module map | instructor |
| [lecture-slides/](lecture-slides/README.md) | 8 unit-level Markdown slide decks with delivery notes, knowledge checks, exit tickets | instructor → students |
| [speaker-notes/](speaker-notes/README.md) | Per-deck teaching guidance: openings, misconceptions, demos, timing, transitions | instructor |
| [instructor-manual/](instructor-manual/README.md) | Course delivery guide, methodology, misconception bank, teaching troubleshooting, 8 unit teaching guides | instructor |
| [lab-workbook/](lab-workbook/README.md) | Lab rules, delivery guide, per-unit lab indexes → **links to the real 72 module labs** | students |
| [demonstrations/](demonstrations/demo-index.md) | 10 flagship in-class demo scripts with setup/expected-output/cleanup | instructor |
| [assessments/](assessments/README.md) | Assessment framework: quiz bank v2, 3 new assignments (A4–A6), exam pointers, CLO mapping, rubrics | both — keys separated |
| [instructor-resources/](instructor-resources/README.md) | Key inventory, marking schemes, gradebook & attendance templates | **instructor-only** |
| [revision/](revision/README.md) | Practice questions, viva prep, common mistakes, rapid scenarios, final checklist | students |
| [setup-and-delivery/](setup-and-delivery/README.md) | Instructor/student environment setup, lab infrastructure, delivery checklists | both |

Supporting docs: [AUDIT-REPORT.md](AUDIT-REPORT.md) (pre-build audit) ·
[MKDOCS-NAV-PLAN.md](MKDOCS-NAV-PLAN.md) (site integration + public/private policy) ·
the root [WORK-INVENTORY.md](https://github.com/nadeem-majeedch/Linux-Administration-Course/blob/main/WORK-INVENTORY.md) (build inventory; repo-only — not part of the site).

## Start here by role

**New instructor, course inherited next week:**
1. [instructor-manual/course-delivery-guide.md](instructor-manual/course-delivery-guide.md)
2. [teaching-plan/16-week-course-plan.md](teaching-plan/16-week-course-plan.md)
3. [setup-and-delivery/instructor-environment-setup.md](setup-and-delivery/instructor-environment-setup.md)
4. Skim [instructor-manual/common-misconceptions.md](instructor-manual/common-misconceptions.md) before Week 1.

**Teaching assistant running labs:**
1. [lab-workbook/lab-delivery-guide.md](lab-workbook/lab-delivery-guide.md)
2. [lab-workbook/student-lab-rules.md](lab-workbook/student-lab-rules.md)
3. [setup-and-delivery/lab-infrastructure.md](setup-and-delivery/lab-infrastructure.md)

**Student revising:**
1. [revision/final-revision-checklist.md](revision/final-revision-checklist.md)
2. [revision/practice-questions.md](revision/practice-questions.md)
3. Existing [cheatsheets](../cheatsheets/README.md) — lookup, not understanding.

## Instructor-only material — read this

Answer keys, assignment keys, and marking materials are gathered under
`teaching/instructor-resources/` and `teaching/assessments/**/keys-instructor/`.
They are **excluded from the site navigation on purpose**, but this
repository and its GitHub Pages site are **public** — see
[instructor-resources/INSTRUCTOR-ONLY.md](instructor-resources/INSTRUCTOR-ONLY.md)
for what that means operationally and how to distribute keys safely.

## Ground rules the package follows

- Module content is never duplicated — every lab/deck/assessment links to its module source.
- Every risky command carries **Purpose → Risk → Safe environment → Recovery**.
- CLOs are referenced as **proposed** (pending instructor review), matching `accreditation/`.
- Ubuntu LTS is the assumed environment; deviations are stated inline.
