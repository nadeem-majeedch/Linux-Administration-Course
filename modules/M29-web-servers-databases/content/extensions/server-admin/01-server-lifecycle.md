# Lesson 1 — The Server Lifecycle: Provisioning and Identity

> Extension A · Server Administration · Difficulty: Advanced
> Reading time: ~25 min · Lab: [Provision the second server](lab-01-provision-the-second-server.md)
> Up next: [Fleet consistency](02-fleet-consistency.md)

---

## 1. What "provisioning" actually means

Everything the course has done since M04 — install, users, packages,
services, hardening — was provisioning, performed by hand. Formally:

> **Provisioning** = producing a working, *documented, repeatable*
> server from nothing: hardware/VM → OS → identity → packages →
> configuration → services → verification.

The word *repeatable* is the whole discipline. A server configured by
typing has a secret configuration that exists only in the admin's
history; a server configured by *script* has its configuration as an
artifact — versionable (M26), reviewable, and re-runnable. The
lifecycle view:

```text
 provision ──► configure ──► operate ──► update/patch ──► decommission
     │             │            │             │                │
 OS install    packages      monitor       patch cadence    data archival
 identity      services      backup        config drift     teardown doc
 storage       hardening     incidents     (M25)            (M24 backups)
```

Two classes of provisioned state, and the distinction runs the rest of
this extension:

- **Golden-image thinking** — bake everything into a template (VM
  image, container base image, M28's pinned `FROM`) and stamp out
  copies. Fast to boot, but every change means a new image.
- **Configuration thinking** — start from a minimal base and apply a
  *script/manifest* that declares the desired state. Slower to boot,
  but every change is a diff.

Modern practice mixes both (base image + config layer); the course's
whole arc — Dockerfiles (M28), setup scripts, unit files — has been
configuration thinking all along.

## 2. Identity: hostname, hosts, and the fleet view

The first configuration act on any box, and the first thing to get
wrong at scale:

```console
$ sudo hostnamectl set-hostname ds-analysis-01
$ hostnamectl          # static/pretty/transient names
$ cat /etc/hosts       # the local resolver's map — M21 §3's first rung
127.0.0.1  localhost
10.0.2.15  ds-analysis-01      # ← self-reference: tools resolve their own name
```

Conventions worth adopting *now* (they cost nothing solo, save careers
in fleets): **role-location-number** (`ds-analysis-01`,
`jupyter-gpu-02`), because hostnames that encode role survive team
memory; and one line in `/etc/hosts` or DNS for every box you
administer, because "which machine was that?" is a resolution question
(M21), not a memory exercise.

`hostnamectl` also sets the *other* metadata fleets rely on:

```console
$ sudo hostnamectl set-deployment "BS-DS teaching fleet"
$ sudo hostnamectl set-location "campus-virtualization"
```

## 3. The provisioning script: the course's arc, artifact-ized

Every M25/M29 hand-configuration becomes a script with three
properties: **idempotent** (safe to re-run — M11's lesson), **logged**
(M24's fail-loudly contract), **verified** (the script ends by
checking its own work). The skeleton:

```bash
#!/usr/bin/env bash
# provision-ds-node.sh — minimal teaching-node provisioning
set -euo pipefail
log() { echo "[$(date -Is)] $*"; }

log "identity"
TARGET_HOST="${1:?usage: provision-ds-node.sh <hostname>}"
sudo hostnamectl set-hostname "$TARGET_HOST"

log "packages (M16: refresh, install, verify)"
sudo apt-get update -q
sudo apt-get install -y -q ufw python3-venv git
command -v git >/dev/null || { echo "git missing after install" >&2; exit 1; }

log "users & access (M12/M22)"
sudo useradd -m -s /bin/bash ds || log "user ds exists (idempotent)"
sudo install -d -m 700 /home/ds/.ssh
# authorized_keys copied from the provisioning repo — never typed:
sudo cp keys/ds.pub /home/ds/.ssh/authorized_keys
sudo chown -R ds: /home/ds/.ssh

log "firewall (M25: explicit allows, then enable)"
sudo ufw allow OpenSSH >/dev/null
sudo ufw --force enable

log "services (M20: enable, start, IS-ACTIVE check)"
systemctl is-active --quiet cron || sudo systemctl start cron

log "verify (the script grades itself)"
hostname | grep -q "$TARGET_HOST" || { echo "hostname mismatch" >&2; exit 1; }
sudo ufw status | grep -q "active" || { echo "ufw not active" >&2; exit 1; }
log "OK: $TARGET_HOST provisioned"
```

Idempotency carries the re-run guarantee (`||` on "already exists"
*is* the idempotent form); the verify block is step 7 of the
troubleshooting method (M32-clinic) built into the artifact; and the
log lines are the provisioning *documentation* generated as a
by-product. This script — improved incrementally for the rest of the
extension — is the lab's deliverable.

## 4. What provisioning leaves behind: the three artifacts

A provisioned server is a *triple*, and maturity is keeping all three
in version control (M26):

1. **The script/manifest** — what the server should be (the code
   above; later, Ansible's YAML — lesson 4).
2. **The runbook** — how to operate it (lesson 3's template).
3. **The evidence** — provisioning logs, `systemctl` states, `ufw
   status`, a `git log` of the repo that made it. When an auditor (or
   a professor, or you-in-six-months) asks "why does this server look
   like this?", the answer is a file, not a memory.

---

## Key takeaways

- Provisioning = repeatable production of a server; **the artifact
  (script) is the configuration, the server is its output.**
- Golden image vs configuration manifest is the speed-vs-diffability
  trade; mixed practice uses both layers.
- Hostname conventions and host resolution are fleet infrastructure —
  set them at birth.
- Idempotent, logged, self-verifying scripts: M11 + M24 + M32-clinic
  lessons fused into provisioning.

## Check yourself

1. Why is "I typed the commands, it works" not provisioning?
2. What makes the skeleton script safe to re-run after a partial
   failure — name the two mechanisms.
3. Where does the *verification* live in the script, and which
   methodology step is it?
4. What are the three artifacts a provisioned server should leave
   behind, and where do they live?

*Answers:* (1) The configuration exists only in history — undocumented,
unreviewable, non-repeatable; provisioning requires the artifact.
(2) Idempotent operations (`exists` checks / tolerant installs) so
re-runs skip completed work, and `set -euo pipefail` so failures stop
loudly instead of half-configuring. (3) A verify block at the end
asserting the declared state — methodology step 7 (verify), executed
by the artifact itself. (4) Manifest/script, runbook, evidence logs —
all in version control.

Up next: [Fleet consistency](02-fleet-consistency.md) — the same
server, times twenty.
