# Printable Lab Workbook Recommendation

> Question: should the course produce a **printable lab workbook** in
> addition to the digital-first lab workbook that already exists?
> **Recommendation: no standalone printable workbook. Print per-week
> lab sheets from the existing files instead** — one small, evidence-
> supported addition (below) makes the digital workbook print-clean.

## 1. What the review checked

| Check | Finding (evidence) |
|---|---|
| Page structure | Workbook = one index file per unit + per-lab module files; a "complete workbook" would be ~120 printed pages of nested tables and deep links — unusable on paper |
| Lab numbering | Consistent: unit index tables + module lab files numbered (`lab-01…`); print-ready as-is |
| Space for student responses | Digital workbook expects evidence transcripts (`script` logs, end-state checks) — the response space is *the transcript*, which printing cannot provide; printed response blanks would duplicate what the module labs already structure as "Deliverable / Gate / Done when" |
| Command formatting | Fenced console blocks render cleanly in print (verified across workbook + module labs during this review's fence checks) |
| Tables | Unit tables are wide (6–7 columns); at A4 portrait they compress poorly — the one real print defect |
| Checkboxes | Evidence gates are prose ("Gate 1: paste the OK line…"), not checkboxes — fine on paper |
| Evidence submission fields | Submission = transcript + end-states; already documented per lab |
| Instructor/student separation | Module labs are student-facing and contain **no answer keys** (verified in this review's leak checks); a merged printable would *raise* leak risk by making wholesale copying the default workflow |
| Excessive page length | Index (1–2 pp) + 1 p/lab is the natural print unit; a merged volume is not |
| Broken links | Print cannot carry relative links; every printed sheet would need the "link dies on paper" caveat or printed URLs (noise) |
| Printing limitations | Course-first environment is the terminal; paper labs would imply headless answering, which contradicts the evidence-transcript pedagogy |

## 2. Decision table (options considered)

| Option | Verdict | Why |
|---|---|---|
| Complete printable workbook (one volume) | **Rejected** | page length + wide tables + transcript-based evidence + leak risk |
| Separate module workbooks | Rejected | duplicates module labs; two sources to keep in sync |
| Separate lab sheets (per-week, generated on demand) | **Adopted (instructor workflow, no new repo files)** | each unit index + its linked labs print cleanly enough for a lab-day handout; instructor prints per week from the live files — always in sync, zero duplication |
| Digital-first only | Rejected as *sole* answer | some rooms want paper for the lab brief; the per-week sheet covers it |

## 3. The one change worth making (applied this review)

Add a print note to the workbook README so the per-week workflow is
discoverable: print **unit index + that week's lab files**, never the
whole tree; transcripts remain digital. (README edit applied in this
review — see FINAL report §files-modified.)

## 4. If a printable volume is ever demanded

Requirements it must meet before it is built: generated **from** the
existing files (never hand-copied), tables reflowed to ≤4 columns,
answers verifiably absent (automated leak scan), and a regeneration
step in CI so it cannot drift. Until then, the per-week sheet is the
honest answer.
