# Lesson 2 — Fleet Consistency: Policy, Not Typing

> Extension A · Server Administration · Difficulty: Advanced
> Reading time: ~25 min · Lab: continues in [the provisioning lab](lab-01-provision-the-second-server.md)
> Up next: [The operations runbook](03-operations-runbook.md)

---

## 1. The N-servers problem

One server, hand-configured: fine. Ten servers, hand-configured: one
of them is different and nobody knows which. The problem isn't effort
— it's **drift**, the slow divergence of supposedly-identical systems
through ad-hoc fixes, forgotten patches, and undocumented "temporary"
changes. Fleet administration is the discipline of making
*"all servers identical in the ways that matter"* a **checkable
statement** rather than a hope.

The course's framing: every admin task you've learned is either an
*action* (install pandas) or a **policy** ("every ds-node has pandas
2.2.3"). Fleets run on policy. This lesson inventories the policy
surface; lesson 4 introduces the tools that enforce it.

## 2. The policy inventory (each topic you know, restated)

| Domain | Hand action (M-source) | Policy statement |
|---|---|---|
| **Users** | `useradd ds` (M12) | "roles: ds (admin-capable), qa (limited); no shared accounts; no empty passwords" |
| **SSH** | keys in `authorized_keys` (M22) | "key-only auth; no root login; known host keys distributed; agent forwarding disabled by default" |
| **Packages** | `apt install …` (M16) | "base set P; versions pinned in a lock file; security updates automatic (unattended-upgrades)" |
| **Firewall** | `ufw allow …` (M25) | "default deny; allow 22 from campus ranges; allow 8888 *nowhere* (tunnel-only, M27 posture)" |
| **Services** | unit files (M20/M29) | "units under version control; enabled: cron, jupyter, myapi; Restart=on-failure everywhere" |
| **Storage** | mounts, layouts (M17) | "datasets on /data (XFS), outputs on its own volume, tmp reaped weekly" |
| **Logs** | journald + files (M24) | "persistent journal, 1 GB cap; app logs rotate at 100 MB × 5; no log edits, ever" |
| **Backups** | tar/rsync schedules (M24 §5) | "nightly rsync --link-dest; monthly test-restore logged; 3-2-1 for datasets" |
| **Secrets** | env files (M25 §5) | "no secrets in repos; env files root/ds-only; rotation procedure documented" |

Read that table again as the *outline of a configuration-management
manifest* — because that's what it becomes in lesson 4. The policy
inventory is also the security review checklist (M25) generalized:
an auditor walks the left column and asks "show me the policy" — and
the mature answer is always a file.

## 3. Drift: how it happens, how it's caught

Drift sources, in honest order of frequency: emergency fixes ("just
this once, edit the unit directly"), undocumented hand changes, partial
rollouts (script ran on 8 of 10 boxes), and time (packages age
differently). The catches:

- **The source of truth**: policy lives in the repo; the servers are
  outputs. Anything done by hand is, by definition, drift — scheduled
  re-application of the manifest absorbs it.
- **Convergence checks** — the re-run discipline: `provision-ds-node.sh
  ds-analysis-01` on a *running* server should exit 0 changing nothing
  (idempotency proving consistency), and *report* anything it had to
  change ("ufw was inactive — re-enabled"). The diff output *is* the
  drift report.
- **Inventory honesty**: a simple fleet file — hostname, role, last
  verified, key fingerprint — kept in the repo. Even a CSV beats
  memory; Ansible's inventory (lesson 4) is this file grown up.
- **Canaries from M24**: the health kit runs fleet-wide; a box that
  stops checking in is the first drift signal that matters.

## 4. The fleet lessons the course has been teaching all along

It's worth saying explicitly: nothing in this lesson is new *content* —
it's new *scale*. The same principles, restated:

- **Least privilege** (M13/M25) becomes: role-based users *in policy*,
  sudo scopes *in policy*, key distribution *in policy*.
- **Reproducibility** (M27/M28) becomes: one manifest, N identical
  outputs — the requirements.txt instinct applied to whole servers.
- **Evidence-first** (M24/M32-clinic) becomes: convergence output,
  provisioning logs, health histories — the incident method's paper
  trail, continuous.
- **The untested-restore rule** (M24 §5) becomes: policy that isn't
  re-applied and verified regularly is a rumor — schedule the re-run.

---

## Key takeaways

- Fleets fail by **drift**; the cure is policy-in-a-repo plus scheduled
  convergence (re-apply the manifest), not vigilance.
- Every admin domain you know is restatable as policy — the inventory
  table is the manifest's outline and the audit checklist at once.
- Convergence checks (idempotent re-runs that report changes) turn
  consistency into a *command*.
- Nothing here is new content; it's your 28 modules at N-scale.

## Check yourself

1. Define configuration drift and name its two most common sources.
2. What is a convergence check, and what does its *output* constitute?
3. Your policy says "key-only SSH on all nodes". A teammate hand-added
   a password auth line on one box. Which mechanism catches it, when,
   and what artifact proves the catch?
4. Why does the course say the policy inventory doubles as an audit
   checklist?

*Answers:* (1) Divergence of supposed-identical systems via ad-hoc
fixes and undocumented changes (top sources: emergency hand-edits,
partial rollouts). (2) An idempotent re-application of the manifest on
live servers; its change-report is the drift finding — evidence, not
opinion. (3) The scheduled convergence re-run applies the repo's
sshd_config/unit policy and reports the diff; the repo's change history
plus the re-run log prove both the drift and its correction.
(4) Because every row pairs a domain with a checkable statement — an
auditor's walkthrough *is* the manifest review; maturity is them being
the same document.

Up next: [The operations runbook](03-operations-runbook.md) — operating
what you've provisioned.
