# Assignment 6 — Harden the Science Server

> Covers M25 + M31–M32 (security, server operations, incident method) ·
> enrichment or A3 extension (per instructor adoption) · pairs
> permitted with individually-written incident reports · evidence
> transcripts required.
>
> **The premise:** your VM is now "the lab's DS server." Apply the
> hardening checklist *with evidence*, survive a staged incident, and
> write the incident report the capstone will ask for at full scale.

## Learning objectives assessed

- Security hardening as *evidenced practice*, not claims (M25 checklist)
- SSH key-only policy with documented rollback
- Firewall minimalism with per-rule justification
- The 8-step incident method under a staged fault
- Operational etiquette: services, logs, backups that would survive
  your absence

## Part 1 — Hardening pass (with evidence, ~1 hour)

Apply the [M25 hardening checklist](../../../../modules/M25-security-firewall/content/hardening-checklist.md)
to your VM. For **every** checklist line, the transcript must show:
the check, the result, the change (if any), and the re-check. Minimum
scope:

1. **Updates**: `apt update && apt upgrade` state recorded
2. **SSH**: key-only login demonstrated; PasswordAuthentication
   decision *documented with rollback note* (change it in a sandbox or
   on your own VM only — with the second-session insurance taken)
3. **Firewall**: default-deny incoming; exactly the allows your server
   needs, each with a one-line justification; `ufw status verbose`
   evidence; the **second-session habit shown**
4. **Secrets**: any credentials in a `600` env file *outside* the repo;
   a grep proving no secret is in your project tree
5. **Permissions**: your dataset/project tree's permission design
   summarized and verified against `namei -l` reality

## Part 2 — The staged incident (~30 minutes)

Your instructor (or the M32 drill pack) plants one incident: a failed
service, a suspicious log pattern, a permission fault, or a resource
crisis. Run the **8-step method** and produce the incident report:

- Step 1–7 evidenced in the transcript (define, evidence, component,
  ranked hypotheses, safe test, fix, verify)
- Step 8 — the report (one page): timeline, evidence quoted, root
  cause, what prevented it, what would have detected it earlier

**Rules:** read-only until step 5; one change at a time; verification
re-tests the *original symptom*; if you break something while fixing,
say so in the report — honesty about blast radius is graded, hiding it
is not possible (the transcript shows everything).

## Part 3 — The operations note (~30 minutes)

Write `OPERATIONS.md` for your server (half page to one page):
what runs on it, how it's backed up (and *when the restore was last
tested*), where logs live and how to query them, who has access and
why, and the three commands you'd run first at 2 a.m. — with what each
rules out.

## Deliverables

1. `hardening.log` — transcript covering Part 1 (check → result →
   change → re-check per line)
2. `incident-report.md` — Part 2's step-8 report
3. `OPERATIONS.md` — Part 3
4. The incident *transcript* (`script a6-incident.log`) if the
   incident was run on your VM

## Rubric (20 pts)

| Area | Pts | Full credit |
|---|---|---|
| Hardening evidence completeness | 5 | every line: check/result/change/re-check |
| Firewall & SSH discipline | 4 | justified allows; key-only policy + rollback note; second-session shown |
| Method fidelity in the incident | 5 | ranked hypotheses; read-only first; verify-as-step-7 |
| Incident report quality | 3 | timeline + quoted evidence + prevention, peer-readable |
| OPERATIONS.md | 3 | a stranger could operate the server from it |

## Academic integrity

Pairs may share the *server*, never the incident report — reports
diverge because methods do. The transcript is the identity of your
work (see the [framework](../README.md#academic-integrity-guidance)).
