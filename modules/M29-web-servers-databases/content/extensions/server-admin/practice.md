# Extension A Practice — Server Administration

## Quiz (10 questions)

Answer first; key at the bottom.

1. Define provisioning in one sentence. Which word in your sentence is
   the whole discipline?
2. Golden image vs configuration manifest: state the trade-off and the
   modern mixed practice.
3. Why set `hostnamectl set-deployment`/`set-location` on even a
   single VM?
4. What makes the provisioning script safe to re-run after a partial
   failure? Name the two mechanisms and their M-sources.
5. Define configuration drift; name its two most common sources.
6. What is a convergence check, and what does its output *prove*?
7. In the runbook template, why is the change log append-only?
8. The backup has run nightly for a year. Which calendar item makes
   that claim operational, and what does it produce?
9. Name the two design axes of configuration-management tools and
   place Ansible on both.
10. In the example playbook, which four course modules (M-numbers) do
    the `authorized_key`, `ufw`, `copy`, and `systemd` tasks encode?

### Key (sketch answers; your wording may be better)

1. Producing a working, **repeatable** server from nothing —
   repeatability requires the artifact, not the history.
2. Bake-all (fast boot, expensive changes) vs declare-all (diffable,
   slower boot); modern practice: minimal base image + declarative
   config layer.
3. Fleet metadata (role/location) is cheap now and load-bearing later —
   inventories, monitoring labels, and billing groups all read it.
4. Idempotent operations (existence-guarded actions, M11) and
   fail-loudly `set -euo pipefail` (M24) — partial failures leave
   completed work intact and stop at the broken step.
5. Divergence of supposed-identical systems; sources: emergency
   hand-edits, partial rollouts.
6. Re-applying the manifest on live nodes; a no-change run *proves*
   current consistency; changes reported are the drift findings.
7. History is data — a mutable log invites narrative cleanup that
   destroys the audit trail.
8. The monthly **timed test-restore**; it produces a logged RTO and
   checksum verification — "backups work" becomes evidence.
9. Imperative-vs-declarative and agent-vs-agentless; Ansible:
   declarative, agentless (push over SSH).
10. `authorized_key` → M22; `ufw` → M25; `copy` → M20/M29 unit
    deployment (and M13 ownership); `systemd` → M20 enablement.

## Challenges

**C1 — Idempotency audit.** Run your provisioning script three times
in a row; classify every log line as *created*, *skipped (already
true)*, or *error*. Any line not in the first two classes is a latent
non-idempotency — fix it. Deliverable: the three-run table.

**C2 — The drift hunt.** Have a classmate (or future-you, with a
schedule delay) make three secret changes to a node: delete a package,
edit a config, remove a file. Run convergence; produce the drift
report *only from the script's log* — no memory allowed. Deliverable:
the report + one paragraph on what it missed.

**C3 — Runbook rehearsal.** Hand your RUNBOOK.md to a classmate: they
must perform two operations (health check, node re-provision) using
*only* the document, then report every point of confusion. Fix the
doc. Deliverable: their friction list + your edits.

**C4 — The ansible reading exam.** Take lesson 4's playbook and add —
*on paper* — the tasks for: nightly backup timer (M19/M24), log
rotation cap (M24 lesson 2), and outputs directory with SGID (M13).
For each: module choice, the M-source, and why declarative beats the
bash equivalent here.

---
*Back to: [Extension A index](README.md) · [M29 extensions](../README.md)*
