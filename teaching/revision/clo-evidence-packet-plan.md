# CLO Evidence Packet Plan

> Purpose: make the course's CLO claims **auditable** — every claim
> traceable to a concrete artifact, collected by a method an external
> reviewer could repeat. Companion documents (repository-authoritative):
> [CLO-MAPPING-MATRIX.md](../../accreditation/CLO-MAPPING-MATRIX.md) ·
> [CLO-ASSESSMENT-ALIGNMENT.md](../../accreditation/CLO-ASSESSMENT-ALIGNMENT.md) ·
> [ACCREDITATION-ONE-PAGER.md](../../accreditation/ACCREDITATION-ONE-PAGER.md).
>
> **Status:** plan + blank templates only. **No student evidence exists
> yet** (no cohort has been taught from this package); nothing here
> asserts achievement, percentages, or performance. The matrix's
> *mapping* rows are traceable; any *attainment* row stays blank until
> a real cohort generates artifacts.

## 1. Packet structure (one folder per CLO)

```text
clo-evidence/
├── README.md                        ← this packet's index + collection calendar
├── CLO-1/
│   ├── 01-clo-statement.md          ← verbatim CLO + measurable verb analysis
│   ├── 02-module-mapping.md         ← modules/weeks that teach it (from matrix)
│   ├── 03-learning-objectives.md    ← session objectives lines (plan refs)
│   ├── 04-lecture-evidence.md       ← deck slide refs + demo index rows
│   ├── 05-lab-evidence.md           ← workbook rows + module lab files
│   ├── 06-assessment-evidence.md    ← instrument IDs + item refs (key stays instructor-side)
│   ├── 07-rubric-criteria.md        ← rubric rows used to score it
│   ├── 08-artifact-examples.md      ← DE-IDENTIFIED student artifacts (post-term)
│   ├── 09-collection-method.md      ← who collects what, when, into where
│   └── 10-review-status.md          ← instructor review record (blank template)
├── CLO-2/ … (same skeleton)
```

## 2. Collection method (per artifact class)

| Artifact class | Source | Collector | When | Stored as |
|---|---|---|---|---|
| Lecture evidence | deck slide IDs + demo-index rows | instructor | course prep | file refs in `04` |
| Lab evidence | unit workbook rows + module lab gates | instructor | per unit | lab file refs + gate names in `05` |
| Assessment evidence | instrument + item numbers (LA-1…5, A1–3, quizzes, exams) | instructor | per instrument | item refs in `06` (keys never in the packet) |
| Rubric criteria | capstone RUBRIC.md rows + LA rubrics | instructor | per instrument | row refs in `07` |
| Student artifacts | transcripts, runbooks, incident reports | instructor, **de-identified** | post-term | excerpts + file names in `08` |
| Attainment record | grade distribution per CLO-mapped item | instructor | post-term | counts in `10` (no names) |

## 3. Blank templates (copy per CLO; fill nothing until taught)

### 10-review-status.md template

```markdown
# CLO-__ Review Status

| Field | Value |
|---|---|
| CLO statement (verbatim) | |
| Term delivered | |
| Cohort size | |
| Evidence items collected (IDs) | |
| Mapped items scored (IDs) | |
| Attainment summary (counts only) | |
| Reviewer | |
| Review date | |
| Gaps noted → action | |
```

### 08-artifact-examples.md template

```markdown
# CLO-__ Artifact Examples (de-identified)

> Rule: include only artifacts from students who consented per course
> policy; strip names/IDs; quote transcripts, never paraphrase.

| Artifact | Source instrument | What it evidences | Why it is sufficient |
|---|---|---|---|
| | | | |
```

## 4. Traceability rules (the packet's integrity)

1. Every claim in `02–07` must name a repository path + row/slide/item —
   no "see course materials".
2. Student artifacts appear **only** in `08`, de-identified, and only
   after the term (nothing pre-term is "evidence of attainment").
3. Answer keys stay instructor-side; the packet references items, not answers.
4. Mapping status per CLO = `mapped (traceable)` vs `attainment (measured)`
   — never conflate the two; the matrix's mapping is not proof of learning.
5. The packet is **generated at term end**, not before; a pre-filled packet
   is fabrication.

## 5. Instructor decision required

- Confirm CLO list/wording from the institutional syllabus before packet
  generation (the repo's accreditation docs were written from the course,
  not from the registrar's record).
- Decide the consent/de-identification policy for `08` per institutional rules.
