# Final Course-Wide Teaching Review

> **Date:** 2026-09-18 · **Scope:** the complete teaching package (`teaching/`),
> its integration points (`SETUP.md`, `mkdocs.yml` untouched this pass,
> `scripts/build-site.sh` untouched this pass), and the course content the
> teaching layer references — reviewed week-by-week for **Weeks 2–16** plus
> the package-level reviews (environment verification, deck splitting,
> printability, CLO evidence).
>
> **Method:** repository inspected before any change (see
> [course-wide-review-inventory.md](course-wide-review-inventory.md)); every
> finding cites file evidence; every correction is traceable; validation
> results below are from commands actually executed this session. Nothing
> was claimed executed that was only inspected, and nothing was fabricated —
> including one finding from my own inventory that verification *disproved*
> (F9, recorded honestly as withdrawn).
>
> **Overall status: PASS WITH WARNINGS** — no blockers; every HIGH finding
> fixed; warnings are documented instructor decisions and NOT-RUN items.

---

## 1. Executive summary

The course-wide pass reviewed Weeks 2–16 session-by-session against the
Week-1/2 standard (14-section reports per week), then executed the four
package-level reviews. It found and fixed **one genuine three-way
contradiction** (the A1 assignment due window), **one lab misattribution**
(the end-to-end DS workflow lab is M26 lab 3, not M27 lab 3), **one
stale-numbering defect across the delivery checklist's Weeks 4–15 blocks**,
two **technical-precision fixes** (tilde-expansion quiz item; uid<1000
convention; `--since` quoting), two **missing-documentation gaps** (SETUP.md
Docker section; dataset delivery path), and anchored the **capstone
milestones** the deck and rubric imply but the plan never stated.

Week 2's report is preserved unchanged; its corrections are the baseline.
Weeks 7 and 16 (exam weeks) required no corrections — verification-only.

## 2. Overall status

| Area | Status | Basis |
|---|---|---|
| Week-by-week dry-run (2–16) | **PASS WITH WARNINGS** | 16 reports; 14 new this pass; findings corrected or documented |
| Learning alignment | PASS | outcomes↔labs↔assessments chain verified per week |
| Technical accuracy | PASS WITH WARNINGS | 3 precision fixes; all other commands verified by inspection against module labs (previously execution-audited) |
| Safety | PASS | loopback-only networks, staged snapshots, dry-run gates, rehearsal-before-risky demos — all verified in place |
| Lab quality | PASS | all referenced lab files exist; no solutions leak into student material |
| Assessment quality | PASS WITH WARNINGS | windows now consistent; keys instructor-side; one instructor decision pending (midterm scope header, §18) |
| Consistency (plan↔slides↔notes↔labs↔checklist) | PASS | after the checklist realignment; verified per week |
| Environment verification | **NOT RUN** (by design) | fresh-VM checklist prepared, explicitly not executed — no VM provisioned |
| Session decks | PASS (keep as-is) | evidence-based recommendation; no split |
| Printable workbook | PASS (per-week sheets) | no duplicate volume created |
| CLO evidence packet | PASS (plan only) | templates blank; no attainment claimed |
| Site build | PASS | `mkdocs build --strict` exit 0 |

## 3. Weeks reviewed

Weeks 2–16, sessions S3–S32. Week 2: preserved (previous pass). Weeks 3–16:
reviewed this pass — reports
[week-03](week-03-dry-run-report.md) ·
[week-04](week-04-dry-run-report.md) ·
[week-05](week-05-dry-run-report.md) ·
[week-06](week-06-dry-run-report.md) ·
[week-07](week-07-dry-run-report.md) ·
[week-08](week-08-dry-run-report.md) ·
[week-09](week-09-dry-run-report.md) ·
[week-10](week-10-dry-run-report.md) ·
[week-11](week-11-dry-run-report.md) ·
[week-12](week-12-dry-run-report.md) ·
[week-13](week-13-dry-run-report.md) ·
[week-14](week-14-dry-run-report.md) ·
[week-15](week-15-dry-run-report.md) ·
[week-16](week-16-dry-run-report.md).

## 4. Files reviewed

- Teaching plan: all 32 session rows + week structure + assessment schedule
- All 8 lecture decks + all 8 speaker-notes files (full read)
- All 8 workbook unit indexes + lab-delivery guide
- Delivery checklist (full), setup-and-delivery guides, lab-infrastructure (targeted)
- Referenced course content: 30 module lab indexes (existence), M04/M21/M22/M23/M26/M27/M28/M31/M32 specific labs (names verified), M08 data directory (delivery verified), M24 lesson 1 (quoting), M22/M23/M26/M27/M28 lab listings
- Assessment instruments: midterm/final papers + keys (structure, scope), practical exam (parts, tasks, faults), A1–A3 specs (windows), LA-1…5, capstone RUBRIC/INCIDENTS/VIVA
- Datasets documentation (README/STATUS) and `.gitignore` interplay
- Prior audits: FINAL-TEACHING-PACKAGE-AUDIT.md, week-01 report

## 5. Files created (20)

| File | Purpose |
|---|---|
| `teaching/revision/course-wide-review-inventory.md` | findings register + weeks↔files map (mandated) |
| `teaching/revision/week-03…week-16-dry-run-report.md` (14) | per-week 14-section dry-run reports |
| `teaching/revision/timing-observation-sheet.md` | actual-vs-planned session log (mandated) |
| `teaching/revision/session-deck-splitting-recommendation.md` | deck feasibility review (mandated) |
| `teaching/revision/printable-lab-workbook-recommendation.md` | print review (mandated) |
| `teaching/revision/clo-evidence-packet-plan.md` | CLO packet plan + blank templates (mandated) |
| `teaching/setup-and-delivery/fresh-environment-verification-checklist.md` | consolidated pre-term environment pass (mandated) |
| `teaching/revision/FINAL-COURSE-WIDE-TEACHING-REVIEW.md` | this file |

## 6. Files modified (14) — all corrections traceable

| File | Corrections (finding IDs from the inventory) |
|---|---|
| `teaching/teaching-plan/16-week-course-plan.md` | A1 window ×2 (F1); S26 end-to-end lab pointer (F4); capstone milestones ×4 (gap 3) |
| `teaching/teaching-plan/assessment-schedule.md` | A1 row header (F2); A3 row window (F2) |
| `teaching/setup-and-delivery/delivery-checklist.md` | Weeks 4–15 blocks realigned to the plan (F3), incl. A3 window (F10) and M32-clinic placement (F11) |
| `teaching/lecture-slides/unit-02-command-line-slides.md` | `~../bin` quiz item corrected to the true bash mechanism; LA-1 timing line (F5) |
| `teaching/lecture-slides/unit-04-system-administration-slides.md` | uid<1000 convention clarified (F7) |
| `teaching/lecture-slides/unit-06-services-network-security-slides.md` | `--since "-1h"` quoting (F6) |
| `teaching/speaker-notes/unit-02-command-line-notes.md` | session-8 slide-range header (10–16) |
| `teaching/lab-workbook/module-labs/unit-02-command-line.md` | dataset delivery path documented (gap 1) |
| `teaching/lab-workbook/module-labs/unit-04-system-administration.md` | "beforenoon" typo (F8) |
| `teaching/lab-workbook/module-labs/unit-07-data-science-stack.md` | end-to-end row → M26 lab 3 (F4) |
| `teaching/lab-workbook/module-labs/unit-08-capstone.md` | "beforenoon" typo (F8) |
| `teaching/lab-workbook/lab-delivery-guide.md` | "beforenoon" typo (F8) |
| `SETUP.md` | Docker section added (gap 2) |
| `teaching/revision/README.md` · `teaching/setup-and-delivery/README.md` · `teaching/lab-workbook/README.md` | new documents indexed; print note added |

Plus the previous pass's files (Week 2 + earlier), unchanged this pass:
M04 lessons/labs, glossary, student setup guide, workbook unit-01.

## 7. Corrections applied (by severity)

**HIGH (2) — fixed**
1. **A1 due-window contradiction** — plan said "due W8" (twice) while the assignment spec, assessment schedule, and workbook all said "due end of week 6." The majority + the spec govern: plan rows corrected; schedule row header fixed to match its own logistics.
2. **End-to-end DS workflow lab misattribution** — plan S26 and workbook U7 pointed at "M27 lab 3," which is actually *Batch Scheduling*; the end-to-end workflow lab is **M26 lab 3** (title verified). Both pointers corrected; M27 lab 3 remains legitimately used elsewhere (A2/batch context).

**MEDIUM (5) — fixed**
3. Delivery-checklist Weeks 4–15 described stale module numbering (pre-final plan); all blocks rewritten to the plan's actual modules, with a "plan governs" note retained from the week-2 pass.
4. Assessment-schedule row headers contradicting their own logistics (A1 "4–7"→"5–6"; A3 "14–15"→"11–15").
5. A3 release window (checklist W10 → W11/S22, matching plan+schedule).
6. M32-clinic placement (checklist W12 → W15/S29).
7. Capstone milestones absent from the plan (Proposal/Build/Operate/Document+viva) — anchored to S25/S28/S29/S30 HW lines; SETUP.md Docker gap closed.

**LOW (4) — fixed**
8. `~../bin` quiz item (unit-02 deck) — rewritten to the true bash mechanism (tilde-prefix doesn't expand for `..`); instructor note aligned.
9. uid<1000 system-user claim — Debian/Ubuntu convention stated as such.
10. `journalctl --since -1h` → `--since "-1h"` with the shell-quoting reason.
11. "beforenoon" ×3 → "the afternoon before"; LA-1 "next week" → "this unit's end"; SN slide-range header.

**Withdrawn (1) — honesty record**
12. Inventory F9 listed seven "typos"; grep verification found six of them existed only in my own inventory note. F9 recorded as withdrawn; only "beforenoon" was real. (Kept visible so the review's own QA is auditable.)

## 8. Timing findings (course-wide)

- The two-90′ cadence fits **every week** only with the speaker-notes' prescribed cuts honored; the SNs already encode where to cut (verified for all 8 units).
- Remaining structural pressure points, in order: **S8** (pipeline day), **S9** (scripting core — 50′ lab-start rule), **S26** (end-to-end centerpiece), **S29** (drill day). All four have explicit cuts; none require plan changes.
- S3's buffer fix (Week-2 pass) remains the model: risky steps get explicit slack.
- Every weekly report carries the planned/recommended/risk/adjustment table; the [timing-observation sheet](timing-observation-sheet.md) turns future deliveries into evidence.

## 9. Technical findings

- **Verified correct by inspection:** bash skeleton and guards; permission arithmetic and umask bases; apt lifecycle; fstab fields; signal semantics and the TERM→KILL ladder; cron syntax (`0 4 * * 1-5`, `30 3 * * 6`, `%` escaping, environment trap); systemd enable≠start; `ss`/port semantics and refused-vs-timeout; ssh-keygen/authorized_keys modes; rsync slash semantics and the `--delete` dry-run gate; venv/`python3 -m pip` mechanics; Docker run/volume basics; nginx/PostgreSQL lifecycle; the 8-step incident method.
- **Fixed:** the three precision items in §7.
- **Verified correct cross-artifact:** the capstone deck's rubric table is line-accurate against `RUBRIC.md`; the practical exam's "6 faults, 12 tasks" and final's "Sections A–D" descriptions match the actual papers.
- **Assumption inventory:** all labs assume Ubuntu LTS in a student-owned VM (or WSL2 with the M04-lab-2 parity work); elevated commands appear only inside student-VM contexts; network work is loopback-only by policy; RPM/dnf appears only as identify-not-administer.

## 10. Lab findings

- Every lab referenced by the workbook, plan, and decks exists (30 module lab indexes; M31's ds-server-lab; M32's four incidents; Level-5 ladder).
- Evidence-first deliverables throughout (transcripts, gates, end-states); **no solutions or answer keys in student-facing labs** (scan: clean).
- The strongest safety architectures verified in place: loopback-only networking; mkfs-on-loopback-only; staged snapshots per pair; lab keys never personal; two-terminal ufw rehearsal; sacrificial `--delete` after read dry-run.

## 11. Assessment findings

- Instrument chain complete and weighted coherently (quizzes pool · LA-1–5 · A1–A3 5% each · midterm 20% · practical 15% · final 25% · capstone rubric).
- Windows now consistent across plan/schedule/workbooks after the A1/A3 fixes; cadence principle (no double-heavy weeks) verified.
- Keys instructor-side everywhere; student pages point at instruments, never answers.
- One instructor decision pending (midterm scope header — §18.1).

## 12. Environment verification status

**NOT RUN — by design, honestly marked.** No fresh VM was provisioned in this
review. The mandated consolidated checklist was created
([fresh-environment-verification-checklist.md](../setup-and-delivery/fresh-environment-verification-checklist.md)):
43 checks across base system, VM layer, WSL2, identity, storage, network/services,
Python/Jupyter/Git, Docker, and datasets — each with ID, purpose, prerequisites,
command, expected result, acceptable variation, safety note, week dependency,
and pass/fail + notes fields. Its header states plainly that it was prepared by
inspection and executed by no one yet.

Executed this session (host, read-only): build, links, fences, bash-syntax,
leak, secret, and deletion checks (§16).

## 13. Session-deck recommendation

**Keep the unit-level decks; split nothing.** Full evidence in
[session-deck-splitting-recommendation.md](session-deck-splitting-recommendation.md):
10–18 slides per 2–6 sessions (4–9 slides/90′), per-session load already
carried by the speaker notes, navigation/maintenance/duplication costs of
splitting outweigh benefits. Designated seams recorded if a future half-pace
variant ever needs them (U6 at slide 6; U1 at slide 11) — an instructor
decision, not required now.

## 14. Printable workbook recommendation

**No merged printable volume.** Print per-week lab sheets (unit index + that
week's labs) from the live files; evidence stays digital. Full evidence in
[printable-lab-workbook-recommendation.md](printable-lab-workbook-recommendation.md);
the workbook README now carries the print note. A generated-from-source
volume is the only acceptable form if one is ever demanded (requirements in
the recommendation).

## 15. CLO evidence packet recommendation

Plan created ([clo-evidence-packet-plan.md](clo-evidence-packet-plan.md)):
per-CLO folder skeleton with ten artifact classes, collection method, blank
templates, and integrity rules — including the core distinction that
*mapping* (traceable now) is not *attainment* (measurable only after a real
cohort). **No student evidence exists; none is claimed.** Instructor must
confirm CLO wording against the registrar's syllabus before packet generation.

## 16. Validation results (all executed this session)

| Check | Scope | Result |
|---|---|---|
| MkDocs strict build | `build-site.sh` + `mkdocs build --strict` | **exit 0** (two pre-existing INFO lines on directory-style links in `projects/README.md`, `resources/README.md` — informational, not warnings) |
| Relative links | `teaching/` + `SETUP.md` (636 links) | **0 broken** — the final report's own creation resolved the weekly reports' forward references; per-phase checks also clean |
| Code fences | all `teaching/**.md` | **0 unbalanced** |
| Bash syntax | all ```bash blocks in `teaching/` (7 blocks) | **0 failures** (`bash -n` via Git-bash; the first run's 7 "failures" were a WSL-launcher artifact of this Windows session — diagnosed with a control test and re-run with the explicit `/usr/bin/bash` path; documented here so the anomaly is traceable) |
| Answer-key leak scan | student-facing teaching dirs | **0 key links** (one initial hit was a false positive — `lab-01-key-workflow.md` matched "key"; it is a student lab, not a key) |
| Secret patterns | `teaching/`, `SETUP.md`, build script | **0 hits** |
| Deletions | `git status` | **0 deleted files** (25 modified, 22 new — all listed in §5–6) |
| Anchor spot-checks | new documents | no new cross-file anchors introduced (plain links only) |

## 17. Remaining limitations

1. **Environment-dependent behavior remains NOT RUN** (installer screens, WSL cycles, Docker pulls, staged faults, exam snapshots) — the fresh-env checklist exists precisely to convert these into executed checks before term.
2. **Timing tables are estimates** — honest per the Week-1 standard; the observation sheet is the corrective instrument.
3. **The midterm scope header** ("Units 1–3 (M01–M13)") predates M14/M15 landing in W6 — defensible as written (its items sample that material), but amending it is an exam-paper change outside this teaching-layer pass (§18.1).
4. **Username split `ds` vs `dsstudent`** — carried from the Week-2 report as an accepted LOW inconsistency (§18.2).
5. **The withdrawn-finding episode (F9)** — recorded in the inventory as a QA honesty marker; no content impact.
6. Two datasets remain pending per `datasets/STATUS.md` (incl. `syslog-sample.log`) — pre-existing, documented, with an instructor substitution decision recorded (fresh-env checklist I3).

## 18. Instructor decisions required

1. **Midterm scope header** — keep "Units 1–3 (M01–M13)" as written or amend to include M14/M15 in the next exam-paper revision (content change; out of this pass's scope by rule).
2. **Username canon** — adopt `ds` (module-canonical) or `dsstudent` (SETUP.md suggestion) course-wide at the next content-maintenance pass.
3. **Deck splitting / printables / CLO packet** — no action required for the standard cadence; revisit under the documented triggers only (§13–15).
4. **Fresh-VM day** — schedule one pre-term pass of the verification checklist and archive the signed sheet with the course file.
5. **Dataset substitution** — approve the `syslog-sample.log` substitute (or deliver the pending generator) before W12's log-triage labs.

## 19. Recommended next steps

1. Run the fresh-environment checklist on one loaner VM (30–60 min) and file the signed sheet.
2. Teach Week 1–2 with the timing-observation sheet open; fold actuals back into the plan before Week 3.
3. After term: generate the CLO evidence packet from real artifacts; fold observation-sheet actuals into every weekly report's timing table.
4. At the next content-maintenance pass: resolve the username split and the midterm scope header in one small, traceable change-set.

---

*Nothing in this review commits, pushes, or modifies Git history. All work is
in the working tree; every check above was executed this session unless
explicitly marked NOT RUN.*
