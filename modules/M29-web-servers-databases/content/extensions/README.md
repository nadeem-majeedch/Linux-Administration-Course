# Module 29 Extensions — Server Administration, Cloud Linux, DevOps

> Module 29 extensions · Unit 7→8 bridge · Difficulty: Advanced
> Time: ~12 hours total · Environment: your own VM (local LXC/QEMU demos where noted — no paid cloud anywhere)
> Prerequisites: M20, M25, M26, M27, M28, and [M29 core](README.md)

The core module deployed one service on one box. These three extensions
zoom out to the three scales a working data scientist eventually meets:
**the fleet** (server administration — making N servers consistent),
**the cloud** (where the fleet actually runs — provider-neutral), and
**the pipeline** (DevOps — how changes flow from Git to servers).

**The unifying thread — and this course's most important career lesson:**
at every scale, the *same Linux* applies. A cloud VM is your VM with a
different hypervisor; a security group is ufw moved to the network edge;
CI/CD is the runbook you already write, executed by a robot. The
extensions teach the vocabulary and the concepts; the instincts are the
28 modules you already own.

## The three extensions

| # | Extension | Time | Files |
|---|-----------|------|-------|
| A | [**Server Administration**](server-admin/README.md) — provisioning, fleet consistency, configuration management concepts | ~4 h | 4 lessons + provisioning lab + practice |
| B | [**Cloud Linux**](cloud/README.md) — instance lifecycle, cloud-init, security groups, storage & networking models | ~4 h | 3 lessons + local cloud-init lab |
| C | [**DevOps on Linux**](devops/README.md) — CI/CD, IaC, containers in the pipeline, GitHub Actions concepts | ~4 h | 3 lessons + local CI lab |

**Provider neutrality is a hard rule** (per the module contract): cloud
concepts are taught against the *generic* cloud model (VMs, block
storage, VPCs, IAM) with AWS/GCP/Azure named only as examples of the
same concept. Every lab runs locally: cloud-init is exercised against
a local QEMU/LXC VM or a container that runs cloud-init's
`nocloud` datasource; CI runs in a container "runner"; Terraform and
Ansible are taught conceptually with worked *reading* examples — no
accounts, no spend, no keys.

## The extension contract (same as every module)

- No cloud accounts are created, no credentials exist, no paid
  services are touched — the cloud lessons are **simulated and
 conceptual by design**.
- Provisioning labs re-image only lab VMs/containers you own.
- "Provisioning" means *documented, scripted, reversible changes* —
  the M25 discipline scaled up, never `rm`-and-pray.
- Every clinic file's commands are the course's existing toolbox; new
  tools (`cloud-init`, Ansible, Terraform, `act`-style local runners)
  are introduced conceptually with *reading* exercises, and the one
  hands-on tool per extension (`cloud-init` locally, a local Actions
  runner) is fully safe.

Start with [Extension A — Server Administration](server-admin/README.md)
