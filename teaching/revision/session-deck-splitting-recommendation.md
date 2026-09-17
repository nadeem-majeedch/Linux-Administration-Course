# Session-Deck Splitting Recommendation

> The package ships **unit-level decks** (one per teaching unit, covering
> 2–6 sessions). This review decides, with evidence, whether any unit
> should be split into per-session decks. **Recommendation: keep the
> unit-level decks; split nothing.** Evidence below; a per-unit decision
> table follows for the instructor who disagrees.

## 1. Feasibility review (the requested checks)

| Check | Finding (evidence) |
|---|---|
| Slides per unit | U1: 18 · U2: 16 · U3: 12 · U4: 11 · U5: 13 · U6: 15 · U7: 12 · U8: 10 (grep `^# Slide`) — **10–18 slides per 2–6 sessions** |
| Estimated teaching time | Session blocks run 12–18 slides over 2–6 × 90-min sessions — i.e. **4–9 slides per 90 minutes**; well under lecture-load; the plan's time allocations give labs 30–55′ per session |
| Conceptual density | Highest-density units (U2: text processing; U6: six modules in six sessions) already carry **per-session speaker-note sections** (U2 notes: S5/S6/S7+S8; U6 notes: per-slide + per-session demo table) — the density lives in the notes, not unmanageably in the deck |
| Practical activity placement | Decks already mark knowledge checks and activities *inside* the session flow; the lab workbook is the per-session instrument, and it is already session-mapped |
| Speaker-note alignment | Every deck's notes are sectioned by session (verified for U1–U8); splitting decks would require re-sectioning notes 1:1 — pure duplication cost |
| Navigation impact | `mkdocs.yml` nav has one Slides + one Notes entry per unit; splitting would multiply 8 entries into ~20, densifying student/instructor navigation for no new capability |
| Maintenance burden | A correction (as in this review: F5/F6/F7) currently touches **one** deck; per-session decks would scatter unit-wide fixes across 2–6 files each |
| Duplication risk | Unit summary/reference slides (e.g. U2 slide 15–16) are unit-scoped; per-session decks would either duplicate them per session or lose the unit wrap-up |

## 2. Per-unit decision table

| Unit | Sessions | Slides | Verdict | Rationale |
|---|---|---|---|---|
| U1 Foundations | S1–4 | 18 | **Keep** | largest deck but its two halves (S1–2, S3–4) are already cleanly sectioned in notes; splitting adds a seam mid-VM-install narrative |
| U2 Command Line | S5–8 | 16 | **Keep** | densest unit; notes carry per-session load; the S8 relay/pipeline narrative spans slides 10–13 and should not be severed |
| U3 Scripting | S9–10 | 12 | **Keep** | single narrative arc (commands → scripts → automation); a split would interrupt the skeleton-recitation design |
| U4 SysAdmin | S11–12 | 11 | **Keep** | two-session unit, 11 slides — nothing to gain |
| U5 Software/Storage/Time | S15–18 | 13 | **Keep** | four sessions but notes' demo-error table already indexes by session |
| U6 Services/Net/Sec | S19–24 | 15 | **Keep (watch)** | six sessions on one deck is the stretch case; if a future cohort needs slower pacing, split at slide 6 (network boundary) — recorded as the designated seam, an instructor decision |
| U7 DS Stack | S25–28 | 12 | **Keep** | the integrated-loop slide (11) is the unit's payoff and needs the whole deck before it |
| U8 Capstone | S29–30 | 10 | **Keep** | S30 is student-driven; deck is briefing material, not a lecture |

## 3. What would justify revisiting

- A cohort teaching **one session per week** (half-pace variant): then
  per-session decks match the calendar, and the seams above are the split points.
- Any deck exceeding ~20 slides or a unit exceeding 6 sessions.
- Adoption by instructors without the speaker-notes habit: the notes are
  what make unit decks teachable; without them, split decks + per-session
  notes would be safer.

## 4. Instructor decision required

None for the two-90′ cadence this package assumes. If the two-semester
variant (assessment schedule §"two-semester") is adopted, revisit U6
(split at slide 6) and U1 (split at slide 11, the S3 install boundary).
