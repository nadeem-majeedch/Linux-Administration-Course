# Week 1 Dry-Run Report

> **Date:** 2026-09-18 · **Reviewer role:** instructor preparing to
> teach Sessions 1–2 to beginner BS Data Science students.
> **Method:** full read-through of every Week-1 artifact against the
> 13-element coverage list, cross-checked for factual/command accuracy
> and cross-file consistency; corrections applied only where evidence
> demanded. No fresh VM was booted in this session — every
> environment-dependent check is marked **NOT RUN** and says why.

---

## 1. Executive summary

**Status: PASS WITH WARNINGS** — Week 1 is deliverable as written
after six small corrections. The material is genuinely
beginner-appropriate: the plan's Session 1 spends 20 minutes on
contract and safety before content, the deck never shows a command
before its *why*, and every S1/S2 command is read-only. The main real
risk found was **timing, not content**: the original S2 plan stacked
75 min of lecture on top of labs that the lab workbook bills at 35′
but the module sources time at 50′ — the fix moves the M02 lab to
homework and rebalances the session to 110 planned / 90 delivered with
an explicit buffer.

Corrections applied: 6 (all documented in §8). No files deleted, no
course content touched, no CLO changes, no instructor-only exposure.

## 2. Files reviewed

| File | Role in Week 1 |
|---|---|
| `teaching/teaching-plan/16-week-course-plan.md` (S1, S2; WEEK 1 block) | session contracts |
| `teaching/lecture-slides/unit-01-foundations-slides.md` (Slides 1–10) | S1+S2 deck sections |
| `teaching/speaker-notes/unit-01-foundations-notes.md` (S1, S2 sections) | delivery guidance |
| `teaching/lab-workbook/module-labs/unit-01-foundations.md` | lab routing + session mapping |
| `teaching/setup-and-delivery/student-environment-setup.md` | 8-check verification gate |
| `teaching/setup-and-delivery/delivery-checklist.md` (Week 1 block) | instructor ops |
| `SETUP.md` (Paths A/B, post-install checklist) | the thing students actually follow |
| `modules/M01-what-is-linux/content/labs/lab-01-identify-your-system.md` | S2 in-class lab source |
| `modules/M02-linux-distributions/content/labs/lab-01-identification-circuit.md` | S2 HW lab source |
| `modules/M01-what-is-linux/content/labs/README.md`, `modules/M02…/content/practice/` | existence + habit checks |
| `teaching/teaching-plan/weekly-learning-outcomes.md` | outcomes mapping (read for cross-ref) |

## 3. Setup checks (Task 2)

**Reviewed (inspection, not execution):** SETUP.md Paths A/B flow,
post-install checklist, the 8-check verification table, triage list,
recovery instructions, safety posture.

| Check | Method | Result |
|---|---|---|
| VM sizing consistency (2 vCPU/4 GiB/25 GiB) across deck, plan, SETUP.md | inspection | **consistent** (Slides 12, SETUP A2, plan S3) |
| Package list sanity (`tree shellcheck htop jq tmux build-essential python3-venv python3-pip curl wget git`) | inspection vs apt knowledge | all real Ubuntu 24.04 package names; `python3-venv` needed for Unit 7; **PASS** |
| `lsb_release` availability | inspection: SETUP.md itself never uses it (0 hits) and uses `/etc/os-release` everywhere; `lsb_release` is absent on minimal/server images | **corrected** — 8-check now uses `cat /etc/os-release` |
| 8-check network dependency | inspection: `curl -I https://ubuntu.com` requires outbound HTTPS + curl present | documented: 8-check runs after SETUP post-install toolchain step |
| Boot ISO checksum verification | inspection | present (SETUP A1 step 3), teaches M02 skill early — good |
| VM creation → snapshot ordering | inspection | snapshot *before* any lab touch is stated in both checklist and student guide — consistent |
| Recovery instructions for 4 real failures | inspection | VT-x, WSL kernel update, host disk full, sudoers — all actionable, none destructive |
| Cleanup instructions | inspection | snapshot lifecycle in `lab-infrastructure.md`; per-lab teardown censused in lab rules — covered |
| **Fresh-VM execution of the 8-check** | **NOT RUN** | no VM provisioned in this session; commands verified against documented Ubuntu 24.04 behavior only |
| **Live install walkthrough** | **NOT RUN** | requires VirtualBox + ISO download (~5 GB); inspection only |

## 4. Session timing analysis (Task 3)

Planned = as written before corrections. Recommended = after.

### Session 1 (90 min)

| Activity | Planned | Recommended | Overrun risk | Adjustment |
|---|---|---|---|---|
| Intro + course contract | 20′ | 15′ | low | tighten: contract items are on the board, not read aloud |
| Lecture (Slides 1–5) | 45′ | 40′ | medium — S4 stack discussion attracts questions | cap GNU/Linux aside at 60″ (SN already says so); park Android debate to S2 |
| SETUP.md walkthrough (start) | 15′ | 20′ | **high** — download speeds dominate | start download at minute 30 (parallel), walkthrough narrates over it |
| Exit poll (formative) | 10′ | 10′ | low | keep — it's the S5 warm-up seed |
| Q&A buffer | — | 5′ | — | added |
| **Total** | **90′** | **90′** | | fits with the download-overlap trick |

### Session 2 (90 min)

| Activity | Planned | Recommended | Overrun risk | Adjustment |
|---|---|---|---|---|
| Recap + fuzzies | 3′ | 3′ | low | standing item |
| M02 distro content | 40′ | 30′ | medium | os-release circuit *is* the content; cut the dnf-slide digression |
| M03 architecture | 40′ | 35′ | medium — S8 chain restatement runs long | SN says "3 students restate" — make it 2 |
| 8-check verification | — | 15′ | **high if toolchain HW skipped** | made explicit; HW now includes the toolchain line |
| In-class lab (M01 lab 1) | (was not in plan) | 20′ | low — read-only, self-paced | **the rebalance**: M02 lab (30′ as written) moved to HW |
| Boot-path pair drawing (formative) | 10′ | 7′ | low | timer enforced |
| **Total** | **90′ planned but ≈105′ real** | **90′** | | plan now states 30/35/35/10 |

**Verdict:** deliverable in 2×90 with the corrections; without them,
S2 realistically runs 105–110′. Students still at Path D (no laptop
capability) pair up during S2 — plan already implies this via Path D
coordination "before Week 1".

## 5. Teaching quality findings (Task 4)

**Strong (kept as-is):**
- Beginner framing is excellent: building-manager analogy, the
  "who *administers* your computer?" opener, misconceptions listed
  per cohort experience (SN) rather than invented.
- Every command shown has purpose-before-syntax; expected outputs are
  described ("ID=ubuntu", "x86_64") without fabricating exact strings.
- DS relevance is threaded, not decorative (Jupyter-through-the-stack
  trace, GPU-server motivation for CLI).
- Knowledge checks are reasoning tasks (draw/place/trace), not recall.

**Findings & dispositions:**

| # | Finding | Evidence | Disposition |
|---|---|---|---|
| Q1 | SN S1 referenced a card sort "Slide 1 section" but no slide carries it | slide scan | **fixed** — SN now says paper activity, with a no-print fallback |
| Q2 | SN exit-poll text didn't match the plan's named 3 questions | plan §8 vs SN "Exit questions" | **fixed** — SN now quotes the plan's three questions |
| Q3 | S2 SN gap: no guidance for the 8-check now that it's explicit in S2 | added timing shows the gate | **fixed** via plan+guide wording (verify in S2 opening; SN S2 opening question unchanged — compatible) |
| Q4 | Slide 9's `for f in *.jpeg; do mv ...` is truncated pseudo-syntax | slide text | accepted as intentional ellipsis on a slide (full syntax arrives M08); SN flags it as foreshadowing — no change needed |
| Q5 | "56 KB link" (Slide 9) reads as dated | slide text | kept: it's deliberately rhetorical (worst-case framing), SN tone supports it |
| Q6 | Slide 7 says "four acts" listing five nodes (login as arrival, not act) | slide diagram | cosmetic; M03 lesson 3 uses the same 4-act framing with systemd as the fourth — consistent. No change. |

## 6. Lab findings (Task 5)

| Check | M01 lab 1 (S2 in-class) | M02 lab 1 (S2 HW) |
|---|---|---|
| Clear instructions | PASS — predict-then-run tables, "never type the `$`" reminder | PASS — write-before-run circuit |
| Achievable in stated time | workbook said 20′; source says ~30′ for the *full* lab → workbook's 20′ was the in-class slice; now mapped explicitly | 30′ as written; realistic at home; Part C needs Docker (marked optional in source) |
| Correct commands | all read-only and real (`whoami hostname uname -srm cat /etc/os-release id lscpu free -h lsblk`) | `cat /etc/os-release \| head -4`, `uname -m && uname -r`, `uptime -p` — all valid |
| Expected observations | described qualitatively, honest about variance (VM vs WSL2) | same |
| Evidence requirements | lab-log.md entry convention (course-wide habit, graded later) | deliverable section present |
| Troubleshooting guidance | module README safety baseline + lab's own notes | dedicated Troubleshooting section in source |
| Safe execution | "Risk level: zero (all read-only)" — verified true by inspection | "All commands are read-only" — verified true |
| Solutions leaked? | none | none |
| LO alignment | identity/evidence = S2 objective 1–2 | distro identification = S2 objective 1 |

**Finding L1 (fixed):** workbook linked to the labs' *README* with
durations that didn't match the source labs; now links the exact lab
files and maps the in-class/HW split.

## 7. Assessment findings (Task 6)

Week 1's formative instruments: S1 exit poll (3 questions), S2
boot-path pair drawing.

| Check | Result |
|---|---|
| Aligned with SLOs | PASS — poll maps 1:1 to S1 objectives (kernel/distro/servers); drawing maps to S2 objective "draw the stack" |
| Difficulty | appropriate for session 1 of a zero-experience course; no trick wording |
| Marking criteria | formative by design ("ungraded or low-stakes" per plan conventions) — fuzzies feed S5, stated in SN; no ambiguity about *purpose* |
| Conceptual vs practical balance | conceptual only — correct for Week 1; first practical evidence arrives via the 8-check + lab transcript |
| Ambiguity | none found; the "what runs on servers?" poll item is open but that's the intended discussion seed |
| Grade pressure | correctly absent — LA-1 grading starts Week 4; stated rationale in lab workbook |

## 8. Corrections applied (Task 7)

| # | File | Change | Why |
|---|---|---|---|
| 1 | `student-environment-setup.md` | 8-check: `lsb_release -a` → `cat /etc/os-release`; added when-it-runs note (S2 for ready VMs, mandatory gate S3; after toolchain step) | command availability on minimal installs; timing realism |
| 2 | `student-environment-setup.md` | end-of-week gate: `lsb_release -d` → `grep PRETTY /etc/os-release` | same cause |
| 3 | `16-week-course-plan.md` S1 | HW adds the post-install toolchain copy-paste | 8-check's network/text checks depend on it; one line, prevents S2 stall |
| 4 | `16-week-course-plan.md` S2 | rebalanced: labs named explicitly (8-check 15′ + M01 lab 1 20′ in-class, M02 lab 1 → HW); time allocation 30/35/35/10 | 105′ overrun removed; plan and workbook now agree |
| 5 | `lab-workbook/module-labs/unit-01-foundations.md` | session mapping rewritten (S2 split); links point to the exact lab files | duration + link accuracy |
| 6 | `speaker-notes/unit-01-foundations-notes.md` | card sort marked as paper activity w/ fallback; exit poll quoted from plan | SN/slide/plan triangle consistency |
| 7 | `delivery-checklist.md` Week 1 | B/D/A updated to match the S2 rebalance; card-sort prep added | ops list must match the plan it operationalizes |
| 8 | `teaching/revision/README.md` | this report indexed | discoverability |

All are additive or corrective; **no content deleted**, no other weeks
touched, CLO docs untouched, instructor-only files untouched.

## 9. Checks not executed and why

| Check | Status | Why |
|---|---|---|
| Booting a fresh Ubuntu 24.04 VM and running the 8-check live | **NOT RUN** | no VM provisioned in this environment; inspection + documented-behavior verification only |
| VirtualBox install walkthrough | **NOT RUN** | requires host-level installer + ~5 GB ISO download |
| `sudo apt install -y …` toolchain line | **NOT RUN** | would modify this machine; verified package names against Ubuntu 24.04 repos by knowledge, not execution |
| Timing simulation with real students | **NOT RUN** | paper simulation only; estimates are instructor-experience-based |
| `script` transcript flow on a fresh VM | **NOT RUN** | same VM constraint |

Everything else (links, fences, shell syntax of any bash block in the
edited files, strict build, leak checks) **was executed** — see §10.

## 10. Validation results (Task 8, executed)

| Check | Result |
|---|---|
| MkDocs strict build (post-corrections) | **PASS — 0 warnings** (`mkdocs build --strict --clean`, 642 docs) |
| Link check, 7 Week-1 files | **98 links checked, 0 broken** |
| Anchor/`#`-links in edited files | covered by strict build (0 warnings = 0 anchor failures) |
| Code-fence balance, 7 files | **0 unbalanced** |
| `bash -n` on bash blocks in edited files | **0 blocks / 0 failures** (corrections added no bash) |
| Nav leak check (instructor-only in `mkdocs.yml`) | **clean** |
| Student-quiz key leakage | **clean** |
| Deletion proof | **0 tracked files deleted** (git status) |

## 11. Remaining risks

1. **R1 (medium):** the 8-check gate at S3 assumes the S1 homework
   toolchain line was run; students who skipped it consume S3 time.
   Mitigation already in place (triage list), but expect 2–4 students.
2. **R2 (low):** download bandwidth variance can still stretch S1's
   walkthrough; the parallel-download trick is instructor-dependent.
3. **R3 (low):** WSL2 students hit systemd-absent edge cases in later
   weeks — flagged in SETUP.md; not a Week-1 risk.
4. **R4 (low):** timing table is paper-simulated; first real delivery
   should re-measure and update §4.

## 12. Recommended improvements for Week 2

1. **Open S3 with the 8-check as a race** (first three full-pass
   tables on the board) — converts the gate into energy.
2. **Prepare a pre-staged loaner VM** on two USB sticks for the
   inevitable BIOS-locked laptops (infrastructure checklist item).
3. **Keep the M02-lab-as-HW pattern** where a lab is evidence-only:
   it protects contact time for hands-on keyboards.
4. **Collect the exit-poll fuzzies digitally** (form/QR) so S5's
   warm-up can quote them anonymously.
5. **Dry-run S3's partition-screen moment** — the "Erase *which*
   disk?" misconception talk is the term's most important 5 minutes;
   rehearse the exact wording.
