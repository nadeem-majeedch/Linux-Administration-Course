# Unit 6 Speaker Notes — Services, Network & Security (M20–M25)

> Companion to [../lecture-slides/unit-06-services-network-security-slides.md](../lecture-slides/unit-06-services-network-security-slides.md).
> Six sessions; the course's highest-stakes unit (≈⅓ of capstone rubric weight).

## Sessions 19–24 overview

**Teaching purpose.** Cross the boundary: the machine now *serves*
(services, ports) and *defends* (auth, firewall, evidence). Everything
here is judged on **evidence-first method** — the journal quote, the
`ss` line, the dry-run output — not on memorized flags.

**Opening question (S19).** "Who started the programs running on your VM
right now?" After the laugh: systemd did — "you've had a service manager
all along; this week you get to *supervise the supervisor*."

## Per-slide guidance

- *S2 (systemctl):* enable-vs-start is drawn as two graphs (runtime
  tree vs boot symlink). The broken-ExecStart demo teaches status
  *reading*: `activating (auto-restart)` means "crash-looping" before
  the journal confirms why — state first, cause second.
- *S3–S4 (network):* layer discipline (street/town/phonebook) then the
  refused-vs-timeout hinge. The http.server demo on 8000 makes `ss`
  *move* — students never forget a listener they watched appear.
- *S6 (SSH):* key anatomy as lock/key; passphrase-on-disk question is a
  values probe (expect "it's already safe" — counter with a stolen
  laptop). TOFU framed as *fingerprint bookkeeping*, not ceremony.
- *S7 (transfer):* the interrupt-and-resume race is the session's
  centerpiece; run it honestly at 200 MB and read the numbers. The
  `--delete` policy slide is graded language — recite it: "no delete
  without a read dry-run."
- *S9 (journalctl):* build the query live from symptom to cause. Sell
  the interface idea: binary index beats raw grep; the anti-pattern
  slide exists because seniors still do it.
- *S10 (monitoring):* free's available-vs-used is the decisive misread
  fix. The memory-hog demo: watch available fall, si/so wake — "the
  server dying politely."
- *S11 (security):* every rule with its *why*. The two-terminal ufw
  habit is taught as professional muscle — the practical exam stages a
  firewall task, and the habit is what survives pressure.

## Misconceptions (unit-wide)

1. "enable = run at boot *now*" — two different graphs.
2. "Ping failing = network down" — rung order exists because ping
   success/failure is *one* rung, not the verdict.
3. "Private keys are safe because they're on my computer" — passphrase +
   file mode 600 + never copying are the actual controls.
4. "`journalctl` is just grep with extra steps" — structured fields,
   boot scoping, unit filtering: grep can't do any of it on binary
   journals.
5. "Firewall = one rule" — default-deny *plus* justified allows *plus*
   verification is the shape.

## Expected responses & probes

- S5 Q3 (no listener on 8888): most students debug *networking* — the
  probe "which rung would have caught it?" teaches that rung 4 assumes
  rung 1–3 results. Listen for the flipped insight: "the app isn't
  listening — it's not a network problem."
- S7 delete-story: students should name *both* skipped rules (dry-run
  and read-the-output). Only naming "be careful" is the tell of
  memorized policy — re-anchor to the two-step choreography.

## Demo choreography & error table

| Session | Demo | Failure beat | Recovery |
|---|---|---|---|
| S19 | broken ExecStart unit | activating (auto-restart) loop | fix path, daemon-reload, start |
| S20 | ss + http.server | connection refused with no listener | start listener, retry |
| S21 | host-key-changed choreography | scary MITM-looking warning | verify out-of-band, re-issue |
| S22 | interrupt-and-resume race | scp restarts, rsync resumes | — (the contrast *is* the point) |
| S23 | crash-loop unit forensics | journal exec error | one-line fix + reload |
| S24 | ufw two-terminal habit | self-lockout rehearsal | second session as insurance |

## Classroom activities

- S20: six-rung ladder worksheet on a printed failure case (pairs).
- S22: tool-selection scenarios (5 cards: one file, 40k files, flaky
  link, browse-then-get, nightly mirror).
- S24: hardening checklist line-by-line "justify or reject" drill.

## Timing & cuts

Six sessions have no slack by design. If S20 runs long, the tcpdump
mention compresses to one sentence. S24's checklist walk never cuts —
it's the graded artifact's rehearsal.

## Transition

"Your machine serves and defends. Unit 7: the *workloads* it serves —
Git, Python, Jupyter, containers, deployments. The DS stack is now a
system-administration problem, which was always the point."
