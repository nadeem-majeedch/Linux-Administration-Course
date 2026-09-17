# Lab — Provision the Second Server (and Prove It's Consistent)

> Extension A · Server Administration · Time: ~60 min · Environment: your own VM
> ⚠️ The "second server" is a **second user account + a container**, both
> yours. No system services, no other users, no network beyond loopback.

The lesson's claim made physical: write the provisioning script,
provision a "new node" with it, then *break* it and watch convergence
catch the drift.

## Part A — the manifest becomes a script (20 min)

Build `~/extensions/provision-node.sh` from lesson 1's skeleton, extended
with your real course habits:

```bash
#!/usr/bin/env bash
# provision-node.sh — provision a teaching ds-node (idempotent, logged, self-verifying)
set -euo pipefail
log() { echo "[$(date -Is)] $*"; }
require() { command -v "$1" >/dev/null || { echo "FAIL: $1 missing" >&2; exit 1; }; }

NODE_NAME="${1:?usage: provision-node.sh <name> <home-prefix>}"
PREFIX="${2:-$HOME/nodes}"
NODE_HOME="$PREFIX/$NODE_NAME"

log "identity"
mkdir -p "$NODE_HOME"/{bin,data,logs,backups}
echo "$NODE_NAME" > "$NODE_HOME/.node-identity"

log "packages (apt set — idempotent by design)"
sudo apt-get update -q
sudo apt-get install -y -q git python3-venv tree

log "environment (M27 pattern, per node)"
python3 -m venv "$NODE_HOME/venv"
"$NODE_HOME/venv/bin/pip" install -q -r "$NODE_HOME/../requirements.txt" 2>/dev/null \
  || log "no requirements.txt yet — skipping pins (note this in the runbook)"

log "service (M20 user-unit, per node)"
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/health@"$NODE_NAME".service <<EOF
[Unit]
Description=Health reporter for $NODE_NAME
[Service]
Type=oneshot
ExecStart=%h/extensions/health.sh %h/nodes/$NODE_NAME
EOF
systemctl --user daemon-reload
systemctl --user enable --now health@"$NODE_NAME".timer 2>/dev/null \
  || log "timer template not installed — documented for the runbook"

log "verify (the script grades itself)"
require git; require python3
test -d "$NODE_HOME/venv" || { echo "FAIL: venv missing" >&2; exit 1; }
grep -q "$NODE_NAME" "$NODE_HOME/.node-identity" || { echo "FAIL: identity" >&2; exit 1; }
log "OK: $NODE_NAME provisioned at $NODE_HOME"
```

Install the health helper (`health.sh` from M24's kit, parameterized
to the node path), and provision **two nodes**:

```console
$ chmod +x provision-node.sh
$ ./provision-node.sh ds-analysis-01
$ ./provision-node.sh ds-analysis-02
$ tree ~/nodes -L 2           # two identical trees — the fleet, born
```

## Part B — the convergence proof (15 min)

Run the script **again** against a provisioned node. Idempotency means
it exits 0 changing nothing meaningful. Then break the node exactly
like real drift happens:

```console
$ rm -rf ~/nodes/ds-analysis-01/venv          # "someone" cleaned disk space
$ sudo apt-get purge -y -q tree               # a package vanishes
$ ./provision-node.sh ds-analysis-01          # re-apply
$ tree ~/nodes/ds-analysis-01 -L 2 && ls ~/nodes/ds-analysis-01/venv/bin/python
```

The re-run *repaired* both — that's convergence. Capture the re-run's
log: the lines where it reinstalled/recreated are the **drift report**.
One journal sentence: what would this look like across ten nodes with
Ansible's `changed=N` summary?

## Part C — the runbook is born (15 min)

Write `~/nodes/RUNBOOK.md` from lesson 3's template, but *only* with
entries your evidence supports: identity table (two nodes, prefixes),
service table (the health timer — with its `systemctl --user status
health@*` check), routine operations (re-provision command!), and a
change log with today's entry. The honesty test: every command in the
runbook must have been *run* in this lab — no aspirational entries.

## Part D — the fleet inventory (10 min)

`~/nodes/FLEET.md`:

```markdown
| node | home prefix | venv python | health timer | last verified |
|------|-------------|-------------|--------------|---------------|
| ds-analysis-01 | ~/nodes/ds-analysis-01 | 3.12.x | active | 2026-09-… |
| ds-analysis-02 | ~/nodes/ds-analysis-02 | 3.12.x | active | 2026-09-… |
```

Fill it by *checking*, not by memory: `ls venv/bin/python`,
`systemctl --user is-active health@…`. This two-row table is the
inventory file that Ansible's `inventory.ini` grows from (lesson 4) —
the habit is the point.

## Done when

- [ ] Two nodes provisioned by the same script; trees identical
- [ ] Convergence proven: break → re-run → repaired, log captured as
      the drift report
- [ ] RUNBOOK.md contains only evidence-backed entries; change log
      started
- [ ] FLEET.md filled by inspection; one sentence on what this becomes
      at N nodes (lesson 4's answer)

**Stretch:** parameterize the script to provision a *third* node with a
different package set via a per-node config file — the first step
toward "roles", and the exact problem Ansible's `host_vars` exists for.
