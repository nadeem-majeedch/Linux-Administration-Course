# Capstone Viva — Oral Examination Question Bank

> 10 minutes; draw 4–6 questions spanning ≥ 3 outcome areas, always including
> one **security** and one **recovery** question. Grade 0–5 per answer:
> 5 = mechanism + evidence source; 3 = mechanism, vague evidence; 1 = command
> without the why; 0 = memorized incantation. Follow-ups marked ↳ probe depth.

## A. Deployment & environment (LO1)

1. Walk me through rebuilding your system from a fresh clone. Where does it
   first *need* something that isn't in Git?
   ↳ What is that something, and where does it live? Why there?
2. Why did you choose your track (VM/WSL2/Docker)? What can the other two
   tracks do that yours can't?
3. Your setup script re-runs on a configured system. What happens, and how do
   you know?
4. Where do your packages come from — and what prevents `apt update` from
   changing your system's behavior between Tuesday and Friday?

## B. Identity, access, permissions (LO2)

5. Your permission matrix claims X. Show me, from the live system, that
   reality agrees — what command proves it for a deep path?
   ↳ Your `svc` identity needs to *read* data but never write. Which bits
   enforce that, and what would `chmod 777` cost you beyond security?
6. Why a separate service identity (or user units) instead of running
   everything as yourself? What one incident does that separation prevent?
7. Your SSH is key-only. You lose the key tonight. What is the documented
   recovery, and why did you document it *before* losing it?

## C. Data engineering (LO3)

8. Your validation step found dirty rows. What happened to them — exactly,
   with paths and file names — and how would I count them from the artifacts?
9. The schedule fires at 02:15. Why that time, what prevents overlapping
   runs, and what happens if a run takes 25 minutes?
10. Show me idempotency: you ran the pipeline twice on the same data. Prove
    it changed nothing the second time.
    ↳ Which of your scripts was hardest to make idempotent, and why?

## D. Model & serving (LO4)

11. Your model artifact claims to be reproducible. What would I need — list
    the artifacts — to re-derive it exactly?
12. Your API runs as a user unit behind nginx. Walk a request from
    `curl localhost/health` to the response, naming every socket and process
    boundary.
    ↳ The API dies. What does systemd do, and what does the *user* see in
    the browser during each phase?
13. Why nginx in front of a FastAPI app that could bind 8080 itself? Name
    two things the proxy layer owns that the app shouldn't.

## E. Security (LO5 — always include one)

14. Justify every listening port on your system — the command you'd run, and
    the reason for each non-loopback listener.
15. Where are your secrets right now — physically, with permissions — and
    what is your procedure the moment one appears in a log file?
    ↳ Why *rotate first* rather than delete-and-recommit?
16. Your firewall is default-deny. What breaks for a legitimate colleague,
    and how did you test that before they found out?
17. What is your system's biggest *remaining* attack surface — the thing the
    checklist can't fix — and what compensating control did you choose?

## F. Observability (LO6)

18. "Something was wrong at 02:00 last night." Show me, from logs alone, how
    you'd answer that in under a minute.
    ↳ What makes your logs answerable *in under a minute* rather than "in
    ten"? Name the property and where you enforced it.
19. Your health script reports green. Name two ways it could be lying — and
    which one you chose to defend against.
20. What did the watchdog/resource trace tell you about your model run that
    the training log did not?

## G. Recovery (LO7 — always include one)

21. Tell me about the injected incident — what did the evidence say first,
    and which hypothesis died because of it?
    ↳ Which step of your method would have caught it sooner if run earlier?
22. Your backup is verified restorable. Say precisely what that claim means —
    what was restored, how verified, how long it took, and what was *not*
    backed up by choice.
23. The disk filling incident (or the one you got): what is the *policy*
    fix, versus the fix you performed? Who owns that policy on a real team?

## H. Automation & packaging (LO8)

24. Read this line from your own `ingest.sh` and tell me why it's written
    the way it is. *(Instructor picks: the strict-mode line, the lockfile, an
    idempotency guard, a trap.)*
25. Which component did you containerize (or why none), and what does the
    image pin — and *not* pin — about your environment?
26. Your reproducibility statement promises a fresh-clone rebuild. Which
    single missing step would most likely break a classmate's rebuild, and
    how did you find out?

## I. Documentation & presentation (LO9)

27. Your runbook was peer-tested. What did your peer get wrong — and what
    did you change because of it?
28. Who is your runbook's reader at 3 a.m., and what did you do differently
    because the reader is *tired and stressed*?
29. If you had one more week, what is the first operational weakness you'd
    fix — and what evidence made you rank it first?
    *(Tests honest self-assessment; "nothing" or "security theater" answers
    score low.)*

## Grading notes for examiners

- The strongest signal is **evidence fluency**: students who built it cite
  the artifact ("the quarantine count is in
  `logs/validate-2026-09-20.json`") without hesitation; students who watched
  it built cite the concept.
- Accept *different valid architectures* — the rubric grades the defense, not
  the choice. A well-defended Docker-track "user units don't exist, here's
  the translation" is a 5.
- Score the **method**, not just the fact: an eight-step narrated recovery
  with one wrong command outranks a lucky fix with no narration.
- Where a student's answer is better than the rubric's expectation, note it
  — the viva bank is a floor, and the course's best artifact is the student
  who surprises the examiner with evidence.
