# Practical Lab Assessments (LA Circuits)

> Five graded 20–30-minute lab circuits — one per major unit — each a
> 10-point task sheet with an evidence rubric. The papers live in the
> repository's assessment bank; this page is the delivery wrapper.

| Circuit | Assesses | When | Paper |
|---|---|---|---|
| LA-1 — Navigation & Files Circuit | M05–M07 | week 4 | [lab-assessment-01](../../../assessments/lab-assessments/lab-assessment-01.md) |
| LA-2 — Pipeline Fluency | M09–M10 | week 8 | [lab-assessment-02](../../../assessments/lab-assessments/lab-assessment-02.md) |
| LA-3 — Permissions Repair | M12–M14 | week 12 | [lab-assessment-03](../../../assessments/lab-assessments/lab-assessment-03.md) |
| LA-4 — Service & Log Forensics | M20, M24 | week 12 | [lab-assessment-04](../../../assessments/lab-assessments/lab-assessment-04.md) |
| LA-5 — Remote Workstation | M22, M31 | week 13 | [lab-assessment-05](../../../assessments/lab-assessments/lab-assessment-05.md) |

(Weights: the LA pool = 10% of the course grade, per the repository's
[assessment scheme](../../../assessments/README.md).)

## Submission requirements (every circuit)

1. **Transcript first**: `script laN.log` before any task; the
   transcript is the submission
2. **Labeled tasks**: T1, T2… visibly separated (a comment line per
   task is enough)
3. **End state + evidence**: where a task produces state (a file, a
   mode, a running service), the transcript shows the verification
   command too — end state alone caps below full marks
4. **Safety choreography visible**: any destructive step shows its
   ls-first / dry-run / printed-path ritual

## Evidence standard (what graders reward)

| Mark | Pattern |
|---|---|
| ✓ | correct outcome + verification command + correct method |
| ▲ | correct outcome, method invisible or verification missing |
| ✗ | wrong outcome or missing task |
| ⚠ | unsafe sequence — survived, but deducted (published in advance) |

Partial credit follows method: a wrong diagnosis with a sound evidence
chain outscores a lucky correct guess without one.

## Integrity guidance

- Circuits are staged per pair/seat with snapshots — seat-neighbor
  answers diverge by design; identical transcripts are examined at the
  justification level
- The predict-before-run lines (where present) are personal evidence
- Policy for notes/open-book: each circuit's header states it; default
  is closed-book except the student's own one-page prep sheet where
  the paper allows it
- Detection and process: [troubleshooting-teaching §5](../../instructor-manual/troubleshooting-teaching.md#5-academic-integrity-incidents-in-transcripts)

## Instructor logistics

Staging (snapshots, staged users, crash-loop units) per the
[infrastructure checklist](../../setup-and-delivery/lab-infrastructure.md);
keys and per-circuit common-failure notes are instructor-held
([answer-keys inventory](../../instructor-resources/README.md)).
