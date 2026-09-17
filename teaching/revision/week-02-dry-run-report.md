# Week 2 Dry-Run Report — Installing Ubuntu & Snapshots (M04)

> **Date:** 2026-09-18 · **Standard:** same method as
> [week-01-dry-run-report.md](week-01-dry-run-report.md) — every finding
> below cites the exact file/line evidence it came from, every fix is
> traceable, nothing was claimed executed that was only inspected.
> **Status: PASS WITH WARNINGS** (2 real defects found and fixed; the
> rest were consistency drift between the plan, slides, notes, labs
> and checklist).

---

## 1. Executive summary

Week 2 delivers M04 in two sessions: **S3 = guided Ubuntu install
(hands-on)**, **S4 = snapshot/restore discipline + boot recap**. The
material is technically sound and the snapshot pedagogy (break-and-
restore, restore race) is excellent. The dry-run found two genuine
defects:

1. **Flavor conflict (HIGH):** the course canon split in two —
   SETUP.md routes students to the **Ubuntu 24.04 Desktop** ISO, while
   M04's lessons and lab 1 teach the **Ubuntu Server (Subiquity)**
   installer with "no GUI" as a stated principle, and the plan's S4
   homework even said "explore the desktop." A beginner following both
   documents would hit a screen that matches neither set of
   instructions.
2. **Lab mislabel (HIGH):** the plan, workbook and teaching guide all
   point S4 at "M04 lab 2 = snapshot drills," but the repository's
   lab 2 is the **WSL2 track**; the drills are lab 1 Part D. Every
   dependent pointer was corrected and the WSL2 track is now routed
   explicitly instead of being invisible.

Both fixed. Nine smaller consistency/correctness items fixed or
documented (§8). MkDocs strict build green, 0 broken links, 0
unbalanced fences, **0 files deleted**.

---

## 2. Files reviewed

| File | Role | Read |
|---|---|---|
| `teaching/teaching-plan/16-week-course-plan.md` | S3–S4 rows + Week-3 boundary (S5–S6) | full S1–S6 + week list |
| `teaching/lecture-slides/unit-01-foundations-slides.md` | Slides 11–18 (S3–S4) | full deck |
| `teaching/speaker-notes/unit-01-foundations-notes.md` | S3–S4 sections + demo choreography | full file |
| `teaching/lab-workbook/module-labs/unit-01-foundations.md` | Week-2 lab index + session mapping | full file |
| `teaching/instructor-manual/module-teaching-guides/unit-01-foundations.md` | M04 teaching guide | full file |
| `teaching/setup-and-delivery/delivery-checklist.md` | Week 1–3 blocks | full file |
| `teaching/setup-and-delivery/student-environment-setup.md` | 8-check gate (Week-1 carry-over) | verified unchanged |
| `SETUP.md` | Paths A/B, username convention, toolchain line | relevant sections |
| `modules/M04…/lessons/01-why-a-lab-not-a-laptop.md` | flavor choice (§4) | full |
| `modules/M04…/lessons/02-provision-the-vm.md` | sizing + Subiquity answers | full |
| `modules/M04…/lessons/03-verify-and-first-boot.md` | ISO naming, `hostnamectl` | targeted |
| `modules/M04…/lessons/04-snapshots-and-reset-discipline.md` | snapshot ≠ backup | referenced |
| `modules/M04…/labs/lab-01-provision-the-vm.md` | Parts A–E (the install + drills) | full |
| `modules/M04…/labs/lab-02-wsl2-track.md` | WSL2 track, parity circuit | full |
| `modules/M04…/content/practice/` | quiz/answers/challenges exist | verified |
| `resources/glossary.md` | initramfs entry (S4 revision line) | verified present |
| `FINAL-TEACHING-PACKAGE-AUDIT.md` + week-01 report | standards & carry-overs | re-read |

**Week-1 carry-over checks:** the 8-check gate (now `/etc/os-release`
based) is compatible with both Server (console-first) and Desktop;
the S1-HW toolchain line exists in SETUP.md; the `lsb_release` fix did
not reappear outside the week-1 report's own text.

---

## 3. Coverage audit (13-element checklist)

| Element | Present? | Evidence / note |
|---|---|---|
| Clear learning outcomes | ✅ | plan S3/S4 objectives; weekly-outcomes M04 rows |
| Beginner-friendly explanations | ✅ | "Erase disk" talk; virtual-vs-real disk slide |
| Logical teaching sequence | ✅ | concepts (15′) → install → snapshot → recap |
| Prerequisites | ⚠️→✅ | S3 prep line omitted the ISO; **fixed** (now names Path A/B ISO states) |
| Installation/setup guidance | ⚠️→✅ | dual-flavor gap — **fixed** (F1) |
| Lecture activities | ✅ | sizing mini-lecture; peer-check config critique |
| Demonstrations | ✅ | projector-on-partitioner; break/restore choreography |
| Practical lab tasks | ⚠️→✅ | lab-2 mislabel — **fixed** (F3) |
| Student preparation | ✅ | S4 prep = "VM snapshotted (S3 HW)" — chain verified |
| Formative assessment | ✅ | peer-check (S3); restore race (S4) |
| Homework/practice | ⚠️→✅ | "explore the desktop" contradicted Server canon — **fixed**; M04 quiz HW is real |
| Estimated timing | ⚠️ | S3 had zero buffer for the riskiest step — **mitigated** (§4) |
| Instructor notes | ✅ | SN §5 + guide M04 section; loaner-VM fallback present |

No duplicated content found; M03 recap in S4 is a deliberate bridge,
not duplication.

---

## 4. Timing analysis

### Session 3 — guided install (plan: 15 lecture · 60 hands-on · 15 formative)

| Activity | Planned | Recommended | Overrun risk | Adjustment |
|---|---|---|---|---|
| VM-sizing mini-lecture | 15′ | 15′ | low | cut to 10′ if BIOS/setup issues ate time at the door |
| Guided Ubuntu install (hands-on) | 60′ | 55′ | **high** | 5′ now explicit buffer; instructor installs in parallel on the projector; **unfinished installs finish as HW** (nothing after Gate 3 needs live class time) |
| Peer-check: "3 things wrong with this config" | 15′ | 15′ | low | screenshot-based; students with slow installs critique the *instructor's* config |
| Recap + bridge out | — | 5′ | low | absorbed from buffer |
| **Total** | 90′ | 90′ | — | plan row now states the buffer + HW-gate rule |

**Applied:** plan S3 time-allocation row rewritten (15 · 55 · 15 with
buffer note); S3 prep line now includes the verified ISO.

### Session 4 — snapshots & boot recap (plan: 30 lecture · 45 lab · 15 formative)

| Activity | Planned | Recommended | Overrun risk | Adjustment |
|---|---|---|---|---|
| Recap question | 3′ | 3′ | low | — |
| Four-act boot play + typed-command anatomy | 30′ | 25′ | medium | SN already prescribes: if the demo runs long, the recap slide becomes assigned reading |
| Break/restore demo (`hostnamectl` choreography) | 15′ | 15′ | medium | pre-recorded fallback (guide recommends; keep it staged) |
| Restore race (formative) | 15′ | 15′ | low | pairs; students without VMs judge and call the winner |
| M04 lab 1 Part D drills | (in 45′) | 20′ | medium | drills in-class only for students whose S3 install finished; others pair with a finished seat |
| Exit poll + M04 quiz assignment | 5′ | 5′ | low | quiz is HW (~20–30′) |
| **Total** | 90′ | ~83–90′ | — | WSL2 lab 2 explicitly moved to HW (Path B) |

**Verdict:** both sessions fit 90′ **after** the buffer/track changes;
before them, S3 realistically overran to ~105′ for anyone with a slow
ISO or a BIOS detour.

**Homework workload (S3+S4):** finish-install gates + first snapshot +
M04 quiz + (Path B) WSL2 parity circuit ≈ 60–90′ total. Reasonable;
flagged so Path B students don't do *both* tracks' deliverables in one
night — the workbook now routes lab 2 as Path-B homework explicitly.

---

## 5. Technical and environment review

### Executed checks (this session, this machine)

| Check | Result |
|---|---|
| Relative-link resolution across all 9 touched files | **0 broken** (105 links scanned) |
| Code-fence balance, 9 files | **0 odd counts** |
| Residual-drift scan (`clean-baseline`, `lsb_release`, "explore the desktop") | **0 hits** outside the week-01 report's own text |
| `bash scripts/build-site.sh` + `mkdocs build --strict` | **exit 0**; two pre-existing INFO messages (directory-style links in `projects/README.md`, `resources/README.md`) — informational, not warnings |
| Deletion check (`git status`) | **0 deleted files** |

### Inspection-based checks (verified against in-repo canon + documented upstream behavior — NOT executed)

- `sha256sum -c`, `gpg --keyserver hkps://keyserver.ubuntu.com`, `gpg --verify` — consistent with M02 lab 2 and Ubuntu's published `SHA256SUMS` procedure.
- `sudo apt-get update && sudo apt-get install -y sl` — added `apt-get update` first (F6): on a freshly installed Server/WSL image with stale package lists, `install` alone can fail with 404s on first use.
- `hostnamectl set-hostname lab-broken` — replaces SN's `sudo hostname lab-broken` (transient; relogin unaffected on Server); `hostnamectl` output is already the S4 exit-ticket artifact.
- Subiquity answers table (entire virtual disk, OpenSSH server = yes, no snaps) — matches Ubuntu Server 24.04 installer flow; Desktop-ISO parity note added.
- WSL2: `wsl --status/--list --verbose`, `wsl.conf` `[boot] systemd=true`, `wsl --shutdown` + 8 s wait, `/proc/1/comm` = `systemd` — matches SETUP.md and Microsoft WSL documentation.
- **Elevated privileges:** only `sudo` inside the student's own VM (apt, hostnamectl) — appropriate and stated; **no host-system commands introduced**.
- **Destructive operations:** "Use entire disk" concerns only the *virtual* disk; the double-read warning was already present and is preserved.

### NOT RUN (no VM provisioned in this session)

- An actual Ubuntu install (either flavor) end-to-end.
- Live snapshot/revert cycle in VirtualBox.
- The `wsl --shutdown` cycle on a real Windows host.
- The restore race with real students.

These remain marked NOT RUN exactly as in the week-01 report; nothing
above claims their execution.

---

## 6. Teaching-quality findings

**Strong (kept as-is):**
- The "Erase disk" misconception talk is the right first move; the
  virtualization slide is correctly positioned *before* the installer.
- Break-and-restore choreography is memorable and safe; the restore
  race converts knowledge into reflex.
- Server-as-rehearsal argument (lesson 1 §4) is honest and forward-
  linked to M31.

**Fixed:**
- **Flavor whiplash:** slides promised a desktop and `Ctrl+Alt+T`;
  lesson 1 said "no GUI… practicing on Server from day one." Lesson 1
  now carries the Path-B/Desktop note pointing at the lab's Desktop-
  ISO variant; the plan's "explore the desktop" homework was rewritten
  for path accuracy.
- SN's demo used the transient `hostname` command and a
  non-canonical snapshot name — now `hostnamectl` +
  `clean-install-<date>` so students watching the demo see exactly the
  command and name they themselves used in lab 1.
- SN's "we can try dangerous things" now constrains scope aloud:
  *in the VM only; the host never sees any of this.*

**Documented, not changed:**
- **Username split (LOW, accepted):** SETUP.md suggests `dsstudent`;
  M04 uses `ds`. Both are examples, both are lowercase-no-spaces, and
  66 files use one vs a larger set using the other in *paths* like
  `/home/ds/...`. A repo-wide rename is a publication-scale change
  outside a week-2 dry-run's mandate; recorded as a known
  inconsistency with a recommendation (§11).

---

## 7. Lab and assessment findings

**Labs:**
- Lab 1 (install + Parts A–E) is achievable in-session **only with
  the buffer change**; gates 1–4 are evidence-based and correctly
  ordered; `lab-environment.md` deliverable threads to the capstone.
- Lab 1 Part A now has the Desktop-ISO note (same `SHA256SUMS`
  procedure beside the Desktop download); Part D now updates package
  lists first (F6).
- Lab 2 (WSL2) was **unreachable from the teaching layer** — the
  plan/workbook said "lab 2 = snapshot drills." Fixed: plan row,
  workbook table row + session mapping, and the Path-B homework line
  all point at the correct files. Lab 2's deliverable gained a
  self-written row on **what stands in for the snapshot on WSL2**
  (honest answer: nothing full-machine — documented commands are the
  real reset button), closing the biggest Path-B pedagogy gap.
- **No solutions leaked into student-facing material**; no answer keys
  touched; no instructor-only material exposed (leak scan clean).

**Assessment:**
- M04 quiz exists (`content/practice/quiz.md` + key, separate); plan
  S4 assigns it as HW — appropriate difficulty for week 2 (scenario
  questions: sizing, snapshot semantics, boot acts).
- S3 formative (config critique) and S4 restore race both assess the
  week's actual outcomes, not recall.
- S4's revision line ("glossary: initramfs, snapshot") is now
  truthful — the `initramfs` glossary entry exists (week-1 fix
  verified in place).

---

## 8. Corrections applied (all traceable)

| # | File | Change |
|---|---|---|
| 1 | `modules/M04…/lessons/01-why-a-lab-not-a-laptop.md` | §4: Path-B/Desktop note — flavor choice documented, links to lab variants |
| 2 | `modules/M04…/lessons/02-provision-the-vm.md` | Subiquity answers table: Desktop-flavor parity note |
| 3 | `modules/M04…/labs/lab-01-provision-the-vm.md` | Part A: Desktop-ISO verification note; Part D: `apt-get update` before install; `touch` split from the install line |
| 4 | `modules/M04…/labs/lab-02-wsl2-track.md` | Deliverable: snapshot-equivalent row (Path-B reset-button honesty) |
| 5 | `teaching/teaching-plan/16-week-course-plan.md` | S3: prep line (ISO), timing row (buffer + HW gates); S4: lab pointer → lab 1 Part D ("lab 2 is the WSL2 track"); HW "explore the desktop" → path-accurate wording |
| 6 | `teaching/lab-workbook/module-labs/unit-01-foundations.md` | Snapshot-drills row → lab 1 Part D; new WSL2 row; S4 session mapping updated |
| 7 | `teaching/speaker-notes/unit-01-foundations-notes.md` | `clean-install-<date>`; `hostnamectl` choreography; VM-scope constraint made audible |
| 8 | `teaching/instructor-manual/module-teaching-guides/unit-01-foundations.md` | Snapshot flag → canonical `clean-install-<date>` name |
| 9 | `teaching/setup-and-delivery/delivery-checklist.md` | Week 2 block rewritten for M04 (was M05–M06 content); Week 3 rebuilt as M05–M07 (merging the drifted rows); numbering-drift note added ("plan governs") |

Files modified this session: **9** (+ this report). Deleted: **0**.

---

## 9. Validation results

| Check | Tool | Result |
|---|---|---|
| Links (all touched files) | link checker (temporary script, removed) | 0 broken / 105 scanned |
| Anchors | n/a — no new anchors introduced | — |
| Fences | counter | 0 unbalanced |
| Residual drift patterns | grep-based scan | 0 (week-01 report's own citation expected) |
| Shell syntax | no new standalone bash blocks (edits are prose/console lines) | bash check not applicable |
| MkDocs strict build | `build-site.sh` + `mkdocs build --strict` | **exit 0** (2 pre-existing INFO lines, not warnings) |
| Nav / leak / secrets | grep scans | clean |
| Deletions | `git status` | 0 deleted files |

---

## 10. Checks not run, and reasons

- **Fresh-VM execution** (install, snapshot/revert, WSL2 cycle): no VM
  provisioned in this session — same honest NOT RUN marking as week 1.
- **Live classroom timing:** requires real students; the tables in §4
  are instructor-estimates from the materials, not observations.
- **Second-path walkthrough** (Desktop ISO end-to-end): the parity
  notes were verified by inspection against documented installer
  behavior, not executed.

---

## 11. Remaining risks

1. **Username split (`ds` vs `dsstudent`)** — accepted for now;
   recommend a one-line cross-reference in both files at the next
   content-maintenance pass, or a pre-publication repo-wide decision.
2. **Flavor dual-track is now documented but untested** — the Desktop
   parity notes should be exercised once on a real Desktop-ISO install
   before Week 2 delivery (30 min, one loaner VM).
3. **S3 remains the course's riskiest session** even with the buffer:
   a whole class installing simultaneously saturates mirrors/campus
   bandwidth. Loaner VMs with pre-staged installs remain the pressure
   valve (checklist now lists them in Week 2 prep).
4. **INFO-level MkDocs messages** (`projects/README.md`, `resources/
   README.md` directory-style links) are pre-existing and harmless;
   listed here so they aren't mistaken for new.

---

## 12. Recommendations for Week 3 (terminal fluency, M05–M07)

1. **Open S5 with the 8-check as a timed race** (week-1 carry-over,
   now `/etc/os-release`-based) — it doubles as attendance.
2. Pre-stage the loaner VMs with the **desktop-flavor difference
   noted** in their `lab-environment.md` so navigation drills behave
   identically on both tracks.
3. Have two loaner VMs physically staged for BIOS-locked laptops
   *before* S5 (these students missed both S3 and S4 installs).
4. Verify the M07 "messy tree" starter dataset exists in `datasets/`
   before S6 (plan references it; workbook routes to it).
5. Reconcile the remaining checklist week-blocks against the plan's
   module mapping (the Week 3+ blocks predate the final module
   numbering; only Weeks 1–3 are now verified aligned).
