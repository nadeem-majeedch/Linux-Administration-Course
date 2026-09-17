# Linux Server Hardening Checklist

> **Module 25 takeaway — printable, reusable.** Each item: what, why
> (one line), and its verification command. Scope: a single Ubuntu
> LTS server/workstation you administer. Target: a DS compute host
> or VM. Verify every item you claim — an unchecked box is fine; an
> unverified check is not.
>
> Usage: run top-to-bottom on a fresh host; re-run quarterly or
> after major changes. The M25 lab uses this as its rubric.

## 0. Before you start

- [ ] **Snapshot/checkpoint taken** — the ultimate rollback exists
  *before* changes.
- [ ] **Two sessions established** — one to change, one to verify
  (the M22/M25 rule for anything that can cut access).

## 1. Identity & access

- [ ] **SSH keys work for every real user** — passwordless, tested
  from a fresh terminal. `ssh <alias> 'echo ok'`
- [ ] **Private keys: `600`, passphrase-protected, agent-backed** —
  hygiene from M22. `ls -l ~/.ssh && ssh-add -l`
- [ ] **No shared accounts** — every login attributes to a person.
  `sudo last | head` (names, not "team")
- [ ] **sudo, not root shells** — admins escalate per-command, with
  logging. `grep -c COMMAND /var/log/auth.log` > 0
- [ ] **No unused accounts** — lock or remove; each account is a
  door. `sudo awk -F: '$3>=1000 {print $1}' /etc/passwd`

## 2. Network posture

- [ ] **Firewall active, default-deny incoming** — ufw (Ubuntu) /
  firewalld (RHEL). `sudo ufw status verbose`
- [ ] **Only needed ports allowed** — the rule list is the service
  inventory. `sudo ufw status numbered`
- [ ] **SSH source-scoped where possible** — campus/VPN subnet, not
  `Anywhere`, on real servers.
- [ ] **Services bind loopback unless network-facing** — Jupyter,
  DBs, dev servers. `ss -tlnp | grep -v 127.0.0.1` (every line here
  needs a written justification)

## 3. SSH hardening

- [ ] **`PasswordAuthentication no`** — brute-force door closed.
  `ssh -o PubkeyAuthentication=no <host>` → denied
- [ ] **`PermitRootLogin no`** — root unreachable over SSH; sudo is
  the path. `ssh root@<host>` → denied
- [ ] **`AllowGroups`/`AllowUsers` set** — explicit allowlist.
  `sudo sshd -G $USER | grep -i allowgroups`
- [ ] **`sshd -t` clean; drop-ins used** — not the main file;
  rollback `.bak` in place.
- [ ] **Rollback rehearsed** — you have *performed* the console →
  restore → reload path at least once (M25 Lab 1, Phase 6).

## 4. Services

- [ ] **Every listening service justified** — the audit table
  (process / bind / needed? / action) exists and is current.
  `ss -tulpn`
- [ ] **Unneeded services disabled or purged** — `--now` included.
  `systemctl list-unit-files --state=enabled`
- [ ] **No unexpected listeners** — anything unattributed is
  investigated (M24 method), then closed.

## 5. Updates & packages

- [ ] **Security updates automatic** — unattended-upgrades (Ubuntu)
  / dnf-automatic (RHEL) active.
  `systemctl status apt-daily-upgrade.timer`
- [ ] **Patch debt near zero** — checked on a schedule, not on a
  hunch. `apt list --upgradable | wc -l`
- [ ] **Reboots applied when required** — a patched kernel isn't
  running until then. `ls /var/run/reboot-required 2>/dev/null`
- [ ] **Third-party sources inventoried** — PPAs/external repos
  justified (M16 ledger). `grep -rh ^deb /etc/apt/sources.list /etc/apt/sources.list.d/ | grep -v ubuntu.com`
- [ ] **Downloads verified** — checksums (second channel) / GPG
  signatures for anything sensitive. `sha256sum`, `gpg --verify`

## 6. Secrets & credentials

- [ ] **No credentials in any repo** — code reads `os.environ`;
  values live outside. `grep -rInE '(token|secret|api[_-]?key)["'"'"']?\s*[:=]' --include="*.py" --include="*.ipynb" . | grep -v environ`
- [ ] **`.env` (if used): git-ignored before creation, mode 600**
  `git check-ignore .env && ls -l .env`
- [ ] **`.gitignore` covers key formats** — `*.pem *.key *.ppk`
  (the course's M04/M26 pattern).
- [ ] **Notebook outputs checked** — tokens echoed once persist in
  `.ipynb`; secrets never printed.
- [ ] **Revocation paths known** — for each provider/token, you can
  name where to rotate it without looking it up under pressure.

## 7. Monitoring

- [ ] **auth.log/journald reviewed on a schedule** — failed SSH,
  sudo use, new users. `sudo grep -c "Failed password" /var/log/auth.log`
- [ ] **fail2ban (real servers)** — sshd jail active.
  `sudo fail2ban-client status sshd`
- [ ] **auditd (when required)** — watched files tagged; searches
  rehearsed. `sudo auditctl -l`
- [ ] **MAC active** — AppArmor (Ubuntu) profiles enforcing /
  SELinux (RHEL) enforcing. `sudo aa-status | head`, `getenforce`
- [ ] **Persistence inventory clean** — crontabs, cron dirs, new
  units, `authorized_keys` growth all explainable.
  `crontab -l; ls /etc/cron*; journalctl -g authorized_keys`

## 8. Recovery

- [ ] **3-2-1 backups exist** — 3 copies, 2 media, 1 offsite
  (M17/M24).
- [ ] **One copy offline or immutable** — ransomware-era nuance;
  reachable-by-same-credentials doesn't count.
- [ ] **Restore tested** — timed, on real data, within the last
  quarter (the M24 lab standard).
- [ ] **Incident runbook exists** — who to tell, what to revoke,
  how to rebuild (Mini-Project D's runbook, extended).

## The scoring habit

Run quarterly: **X/Y items verified**. Anything unverified gets
either fixed or *explicitly accepted with a reason* — a checklist
with silent gaps is theater. Keep the filled copy with the host's
runbook (Mini-Project D pattern): documentation is what makes
hardening transferable when the machine's admin changes — including
when that admin is future you.
