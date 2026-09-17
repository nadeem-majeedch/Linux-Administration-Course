# Unit 3 Teaching Guide — Scripting & Automation (M10–M11)

> Sessions S9–S10 · companions: [speaker notes](../../speaker-notes/unit-03-scripting-notes.md) · [deck](../../lecture-slides/unit-03-scripting-automation-slides.md)

## M10 Bash Scripting (S9–S10, two sessions)

**Objectives.** The guarded-script skeleton as memorized standard;
quoting mastery; exit-code honesty; the debugging *method* (trace →
minimize → fix → re-verify).

**Sequence.** S9: anatomy → quoting → exit codes → control flow.
S10: functions/arrays → debugging live demo → M11 automation patterns →
fix-the-bug lab.

**Difficult concepts.**
- *Word splitting* — the quoting wall. The spaced-filename demo is the
  scaffold; run it twice.
- *What `set -e` does not guard* — the exemption list (`|| true`,
  `if`-conditions, command substitution). Covered honestly in the lab
  discussion; don't oversell the flag.
- *Exit-code semantics* — "0 is success" is backwards from every other
  convention they know; repeat it until it stops sounding strange.

**Common mistakes.** Unquoted variables in loops; missing shebang
(sh/bash mismatch); testing only happy paths; `chmod +x` forgotten (the
"Permission denied" that isn't about permissions).

**Demo plan.** The live debug of one broken script *with the method
narrated* is the session's center — the fix-the-bug lab copies the
process. shellcheck runs *after* manual fixing to close the loop.

**Activity.** Spot-the-bug trio (S9 formative); skeleton recitation
(S10 warm-up).

**Assessment hook.** M10 quiz (script debugging format); fix-the-bug
lab; feeds A1's script section and A2 entirely.

**Extension.** ★★★: M10 challenges — the strict-mode refactor and the
shellcheck-zero mandate.

**Troubleshooting (in class).** Windows line endings in student scripts
(CRLF → `\r` errors) — the `dos2unix`/`sed -i 's/\r$//'` fix is a
teachable moment, not an interruption. Editor config pointers in
SETUP.md.

**Cut slice.** Arrays (S10) can compress to "arrays exist; the labs use
them" if behind.

## M11 Advanced Shell & Automation (S10, second half)

**Objectives.** Idempotency as a *design property*; batch patterns with
failure isolation; report generation.

**Difficult concepts.** Idempotency — run-it-three-times demo makes it
concrete. Cron-preview: "nightly jobs meet yesterday's output" — the
stakes are state pollution, not syntax.

**Common mistakes.** Append-mode in log-creation scripts (non-idempotent
by construction); no per-file failure isolation in batch loops.

**Assessment hook.** M11 quiz (automation design); feeds A2's
"unattended-safe" grading.

**Extension.** ★★★: M11's challenge set (the idempotent-deploy items).

**Troubleshooting.** Students over-engineering: rein in with the
skeleton — the course standard is *small, guarded, boring* scripts.

---

## Unit-level notes

- **A1 releases in S10.** Read its integrity section aloud; the
  transcript-detection framing (from [troubleshooting-teaching](../troubleshooting-teaching.md#5-academic-integrity-incidents-in-transcripts))
  belongs in week 5, not after the first incident.
- **The skeleton is the course's longest-lived artifact** — M19 cron
  jobs, M23 sync script, capstone health.sh all reuse it. The recitation
  drill is not theater.
- **Slow is fast:** quoting mastery costs one session and saves the
  semester. If S9 must shed content, shed arrays and `case`, never
  quoting reps.
