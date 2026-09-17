# Extension A — Server Administration

> M29 extensions · Difficulty: Advanced · Time: ~4 hours
> Environment: your own VM · Prerequisites: M20, M25, M29 core

One server is a pet; a fleet is cattle — and *administration* is the
discipline of making the second kind survivable. This extension
consolidates the course's per-topic skills (users, SSH, packages,
firewall, services, storage, logs, backups) into the **server
lifecycle**: provision → configure → operate → document, with
configuration management as the concept that makes consistency
possible at all.

## Files

| # | File | Topic |
|---|------|-------|
| 1 | [01-server-lifecycle.md](01-server-lifecycle.md) | Provisioning concepts, hostname/identity, the golden image vs configuration split |
| 2 | [02-fleet-consistency.md](02-fleet-consistency.md) | The N-servers problem: users, SSH, packages, firewall, services, storage as *policy*, not typing |
| 3 | [03-operations-runbook.md](03-operations-runbook.md) | Logs, monitoring, backups, security reviews, and documentation as the operation |
| 4 | [04-config-management-concepts.md](04-config-management-concepts.md) | Why configuration management exists; declarative vs imperative; Ansible's model (conceptual) |
| 5 | [lab-01-provision-the-second-server.md](lab-01-provision-the-second-server.md) | Provision a "second server" (second user/container) from a script you write — then prove it's consistent |
| — | [practice.md](practice.md) | 10 questions + key, 4 challenges |

## The extension's claim

Everything here is already in your hands *for one box*: M20 units,
M25 hardening, M24 logs, M19 backups. The new skill is **turning
actions into artifacts** — the provisioning script, the runbook, the
config-as-code — so that a second server, or a rebuilt one, is a
command and not a week.

Start: [Lesson 1 — the server lifecycle](01-server-lifecycle.md)
