# Unit 6 Labs — Services, Network & Security (M20–M25)

> Sessions S19–S24 · the serving-and-defending unit. **Second-session
> habit becomes mandatory** in firewall work. All network labs are
> loopback — the policy, not a preference.

| Lab | Module | Duration | Difficulty | Deliverable | Link |
|---|---|---|---|---|---|
| Unit lifecycle + failure triage | M20 | 30' | ★★ | broken unit fixed with journal evidence | [M20 labs](../../../modules/M20-systemd-services/content/labs/README.md) |
| Local network lab | M21 | 25' | ★★ | layer-by-layer connectivity evidence | [M21 lab 1](../../../modules/M21-networking-fundamentals/content/labs/lab-01-local-network-lab.md) |
| Diagnosis clinic | M21 | 25' | ★★★ | six-rung ladder applied to planted faults | [M21 lab 2](../../../modules/M21-networking-fundamentals/content/labs/lab-02-diagnosis-clinic.md) |
| Key workflow | M22 | 30' | ★★ | key-based localhost login + config alias | [M22 lab 1](../../../modules/M22-ssh-remote-admin/content/labs/lab-01-key-workflow.md) |
| SSH diagnosis clinic | M22 | 30' | ★★★ | 5 broken-SSH patients diagnosed | [M22 lab 2](../../../modules/M22-ssh-remote-admin/content/labs/lab-02-diagnosis-clinic.md) |
| Dataset sync circuit | M23 | 50' | ★★★ | scp/sftp/rsync evidence + sacrificial `--delete` | [M23 lab 1](../../../modules/M23-file-transfer/content/labs/lab-01-dataset-sync-circuit.md) |
| Transfer automation | M23 | 45' | ★★★ | sync-results.sh + verified weekly loop | [M23 lab 2](../../../modules/M23-file-transfer/content/labs/lab-02-transfer-automation.md) |
| Log forensics | M24 | 25' | ★★ | journalctl queries → quoted cause | [M24 labs](../../../modules/M24-logs-journald-monitoring/content/labs/README.md) |
| Monitoring under load | M24 | 25' | ★★★ | vital signs + method applied live | [M24 labs](../../../modules/M24-logs-journald-monitoring/content/labs/README.md) |
| Hardening lab | M25 | 30' | ★★★ | ufw policy + checklist with evidence | [M25 labs](../../../modules/M25-security-firewall/content/labs/README.md) |

## Session mapping

- **S19**: unit lifecycle + failure triage
- **S20**: local network lab + diagnosis clinic
- **S21**: key workflow (+ diagnosis clinic as HW)
- **S22**: dataset sync circuit (+ transfer automation as HW/next day)
- **S23**: log forensics (+ monitoring under load starts)
- **S24**: hardening lab

## The unit's safety architecture

- **Loopback only**: every "remote" is `localhost` inside the student's
  own VM — no external hosts, ever
- **Lab keys are lab keys**: generated fresh, passphrase-protected,
  never the student's personal keys
- **The second-session rule**: mandatory before `ufw enable` — the lab
  walks the self-lockout *rehearsal* deliberately
- **The `--delete` gate**: no rsync deletion without a read dry-run —
  both rules are graded language from here to the capstone

## Checkpoints that matter most

- M21 clinic: the *rung order* is the answer — right conclusion, wrong
  order, scores half
- M23: the slash rule "in your own words" + both speedup lines pasted
- M25: every allow rule carries a *justification* line

## Extension routing (★★★)

- M22: ProxyJump chains
- M23: the reproducibility-pack challenge
- M25: fail2ban concept + staged brute-force log analysis

## Instructor staging

- Crash-looping user unit + bloated journal (M24/LA-4) — pre-staged
- Host-key-changed choreography is *planned* in M22's lab — rehearse
  the recovery before class
- [Infrastructure checklist](../../setup-and-delivery/lab-infrastructure.md)
  items 7–8

## After this unit

**LA-4 (service & log forensics)** and **LA-5 (remote workstation)**
draw their tasks from exactly these labs; **A3** covers M20–M28. This
unit ≈ a third of the capstone rubric — the map slide in S24 says so.
