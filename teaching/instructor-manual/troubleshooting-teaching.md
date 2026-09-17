# Troubleshooting the Teaching

> When the *course delivery* fails — not the students' VMs (that's the
> unit guides) and not the servers (that's M32). A playbook for the
> failure modes that hit instructors.

## 1. Mass VM breakage (lab day, 30 seats, nothing boots)

**Likely causes:** host update broke VirtualBox; the lab image changed;
network license/NAT issue; ISO corruption.
**Triage order:**
1. Confirm scope: one seat or many? (One → seat triage. Many → infra.)
2. Instructor VM boots? If yes, it's seat-local (BIOS VT-x, RAM, host
   disk space — the top three).
3. If *no* image boots: fall back to the USB ISOs (why you carry two).
**Never** let week-2 students reinstall alone — pair them; the demo of
a calm rebuild is itself a lesson.
**Recovery:** SETUP.md's troubleshooting section covers the top three
seat-local causes with exact fixes.

## 2. The on-stage demo fails

**Rule:** never skip it silently and never apologize twice. One honest
diagnosis, using the students' own method, is worth more than the demo
succeeding.
**Choreography:**
1. Name it: "The demo failed. Let's use the method."
2. Read the evidence aloud (the actual error, not a summary).
3. Form one hypothesis, test it, fix or pivot to the backup recording.
4. Debrief: *this* was step 1–7 in real life.
Keep a **pre-recorded fallback** for the two demos you cannot afford to
lose (the loopback mkfs lifecycle, the ufw two-terminal drill).

## 3. A lab runs long (and it's always the same labs)

**The chronic three:** M08's pipeline mini-project, M10's fix-the-bug
set, M23's sync circuit. Budget them ±15 minutes and pre-decide the
**cut slice** (documented in each unit's speaker notes).
**In-flight decision rule:** when 40% of the room has reached the
checkpoint, debrief *that* checkpoint and assign the remainder as
homework — partial completion with evidence beats rushed completion
without.

## 4. Assessment-day infrastructure failures

- **Exam VM snapshot won't restore:** keep one cold-spare prepared
  machine per room; move the student, not the fix.
- **Network died mid-practical:** the practical's tasks are evidence-
  based and *local* by design; if the fault itself was network-dependent,
  switch to the documented alternate task set (in the practical key).
- **A student's transcript (`script`) wasn't started:** the exam rules
  say the transcript *is* the submission — accept end-state checks
  scored at the transcript cap (documented in the key). Do not improvise
  leniency; apply the published rule.

## 5. Academic-integrity incidents in transcripts

The transcript format makes integrity *checkable*:
- **Identical command histories** across submissions: the probability
  argument is decisive; compare checkpoint *answers*, which diverge even
  when commands match.
- **Copy-pasted outputs** (timestamps impossible, paths from another
  machine): the transcript indicts itself.
- **Process:** per institutional policy; the course's contribution is
  the evidence bundle (transcripts + hashes of submission time).
- **Prevention that works:** rotating lab datasets per cohort, the
  predict-before-run culture (you can't copy understanding), and saying
  in week 1 *exactly* how detection works.

## 6. Mid-semester rescheduling pressure

The 16-week plan's compression notes exist for this. Priorities when a
week is lost:
1. **Never cut:** M12–M14 (midterm scope), M19 (capstone pipeline
   dependency), M23 (capstone transfer dependency), M24 (observability).
2. **Cuttable to reading-assignments:** M11 depth, M29 reverse-proxy
   theory, nbconvert.
3. **Compress by merging:** M15 into M14's session (already designed
   that way), M32 into S29's drill (already designed that way).
Document any deviation on the [assessment schedule](../teaching-plan/assessment-schedule.md)
copy the students see — they forgive changes, not surprises.

## 7. The student who is drowning (the silent tail)

**Signature:** labs past deadline, copy-paste transcripts, absence of
questions.
**Protocol (from the delivery guide §6, expanded):**
1. Week-4 1:1 — triage *their* VM with them driving; find the one
   broken foundational reflex (usually paths or cd).
2. Assign a **buddy** from the confident band (both benefit).
3. Give skeleton labs (TODO-marked) for two weeks — rebuild success
   before rebuilding rigor.
4. Oral check-ins replace written quizzes where writing is the blocker.
5. If still sinking by week 8: institutional support referral — the
   course's evidence format makes the case documentable.

## 8. The confident student disrupting labs

Not a discipline problem — an engagement problem. The fix is
[extension challenges](../lab-workbook/lab-delivery-guide.md#extension-challenges)
(★★★ items exist in every module) and the deputy role: they pre-stage
lab infrastructure, which *is* advanced practice (that's literally the
Level-4 lab).

## 9. When you inherit the course mid-semester

1. Read the [16-week plan](../teaching-plan/16-week-course-plan.md) for
   the current week's session only — don't re-plan backwards.
2. Verify the assessment calendar next two weeks ([schedule](../teaching-plan/assessment-schedule.md)).
3. Skim this file and the current unit's speaker notes — that's the
   minimum viable context.
4. Run the current unit's *next* lab yourself the night before. The
   repository's labs are validated; your environment isn't yet.
