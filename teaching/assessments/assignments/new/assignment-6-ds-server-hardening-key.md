# Assignment 6 Key — Harden the Science Server

> **INSTRUCTOR ONLY.** Student paper: [assignment-6-ds-server-hardening.md](assignment-6-ds-server-hardening.md).
> Evidence expectations, incident design, and grading notes. Do not
> distribute.

## Part 1 — Hardening evidence expectations (per checklist line)

The bar is **check → result → change → re-check** for *every* line. A
claim without all four marks ▲ (caps at half for that line).

| Line | Acceptable evidence | Common gaps |
|---|---|---|
| Updates | `apt update && apt list --upgradable` (state recorded); upgrade run or consciously deferred *with reason* | "I ran update" without the upgradable count |
| SSH key-only | key login demonstrated; `PasswordAuthentication` decision documented **with rollback** (sandbox sshd test or own-VM change with the inverse command written down); second session held open *shown in transcript* | changing real sshd with no rollback note = deduct; no second session = deduct |
| Firewall | `ufw status verbose` before/after; every allow rule has a justification line naming the service and audience; default-deny incoming stated | "allow 80,443,22,3000,8888..." shotgun rules = deduct per unjustified port |
| Secrets | `ls -l` showing the env file at 600 outside any repo tree; grep sweep of the project tree for secret patterns returning clean | file at 644; grep absent |
| Permissions | design summary (who/what/why) + `namei -l` output for one deep path proving reality matches intent | design claims contradicted by namei (the classic) |

## Part 2 — Incident design (instructor options)

Pick **one**; the M32 drill pack incidents all fit (they're staged
scripts on the student's own VM):

- **Option A (recommended):** a user unit that crash-loops with a
  *misleading* first hypothesis (e.g., looks like a bad path but the
  real cause is a missing dependency dir) — rewards evidence-first.
- **Option B:** a full-disk-shaped fault via a large log (df full, du
  small) — deleted-but-open; rewards the df/du contradiction work.
- **Option C:** a permission fault where a "helpful" 777 fix *appears*
  to work — rewards root-cause vs symptom discipline.

**Grading method fidelity (5):** the four-step ladder from the [A5
key](assignment-5-network-and-services-key.md) applies plus:
*ranked* hypotheses (list ordering is the evidence), read-only until
step 5, verification re-tests the original symptom. Honesty about
self-inflicted blast radius: full credit; concealment impossible —
the transcript shows it, and *that* is the pedagogical point.

**Report quality (3):** timeline with timestamps, evidence *quoted*,
prevention that references the checklist line that would have caught
it, and the earlier-detection answer ("what would have caught it
first" — health.sh, log alert, quota).

## Part 3 — OPERATIONS.md expectations (3)

A stranger-operable page contains:

1. **Inventory:** services on the box (units, ports, what they serve)
2. **Backups:** what, where, *when last restored* (a date or "never —
   and that is a finding" both score; the false claim scores zero)
3. **Logs:** where + the two query lines they'd actually run
4. **Access:** accounts/groups and the reason each exists
5. **2 a.m. triad:** three first commands with what each rules out
   (uptime/vmstat, free -h, df -h is the expected spine)

Deduct for: aspirational commands (never run), missing access section,
backup section without a restore date or honest "never".

## Quick-triage of submissions

- Transcript shows check→result→change→re-check rhythm, or a flat list
  of changes? (the flat list is ▲ across the board)
- Second session visible *before* the ufw enable line?
- Does the incident report quote the journal, or summarize it?
- Does OPERATIONS.md name a real restore date tied to a real command
  in the transcript? (cross-check — the strongest integrity signal)

## Integrity notes

Pairs share the server; reports must diverge (different incidents or
independently-written reports — spot-check with a viva probe: "walk me
through *your* ranked hypotheses"). The OPERATIONS.md cross-check
against the transcript is the primary authenticity test.

## Viva probes

- "Line 3 of your firewall: justify port X to me as if I were your
  security officer."
- "Your SSH rollback note — read it. Would it *actually* restore
  access from a third terminal?"
- "Which checklist line would have caught the incident earlier?"
