# Instructor Demonstrations

> Live, in-class demonstrations are the course's highest-bandwidth
> teaching moments — a command *failing* on stage, diagnosed calmly,
> teaches more than a slide. This directory holds the flagship demo
> scripts: setup, procedure, expected output, the questions to ask, the
> common errors, and the cleanup.

## The demo contract (every script follows it)

1. **Title + learning objective** — what single idea the demo installs
2. **Prerequisites** — what must be true before you start
3. **Setup commands** — pre-staged, rehearsed, on the room's image
4. **Step-by-step procedure** — with the *narration line* for each step
5. **Expected output** — real, from the module content (marked when
   variable)
6. **Explanation** — what each part of the output means
7. **Questions to ask** — where students do the thinking
8. **Common errors** — what usually goes wrong, and the recovery
9. **Recovery steps** — how *you* come back if it fails on stage
10. **Cleanup** — census, exact paths, snapshot restore if needed
11. **Optional extension** — the stretch version for a strong room

## The index

**[demo-index.md](demo-index.md)** — all ten flagship demos with
session mapping, duration, risk level, and fallback status.

## Demo principles (from the [methodology](../instructor-manual/teaching-methodology.md))

- **Predict → Run → Explain** — students predict before you run; the
  prediction is the engagement, the diff is the lesson
- **Failure is content** — the planned-failure demos (redirection trap,
  self-lockout rehearsal, unescaped `%`) are the most valuable in the
  course; rehearse the *recovery*, not just the demo
- **Never dangerous against the host** — loopback disks, snapshots,
  user units, `~/` scratch; the [student rules](../lab-workbook/student-lab-rules.md)
  apply to the instructor's stage too
- **Fallback recordings** exist for the two demos the session can't
  survive losing (loopback mkfs lifecycle, ufw two-terminal drill)
