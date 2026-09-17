# Practical Examination — Answer Key & Staging Guide

> For instructors. Student paper: [practical-exam.md](practical-exam.md).
> This file contains **both** the answer key and the snapshot staging
> script. Staging takes ~10 minutes on a clean Ubuntu Server/VM
> template; snapshot after staging, then restore per student.

## Part 0 — Staging script (run as root on the template)

```bash
#!/usr/bin/env bash
# stage-practical.sh — plant the 6 exam faults. Run ONCE on a clean
# Ubuntu template with docker preinstalled and a 'sam' user to create.
set -euo pipefail

# --- users/groups -------------------------------------------------
id -u sam &>/dev/null || useradd -m -s /bin/bash sam
groupadd -f labteam

# --- fault 1: upload-api unit points at a dead venv ---------------
useradd -m svc-upload 2>/dev/null || true
sudo -u svc-upload python3 -m venv /home/svc-upload/venv-broken \
  --without-pip 2>/dev/null || python3 -m venv /home/svc-upload/venv-broken
cat > /etc/systemd/system/upload-api.service <<'UNIT'
[Unit]
Description=Dataset upload API (exam)
After=network.target

[Service]
User=svc-upload
ExecStart=/home/svc-upload/venv-broken/bin/python -m http.server 8080 --directory /srv/uploads
Restart=on-failure

[Install]
WantedBy=multi-user.target
UNIT
mkdir -p /srv/uploads
chown -R svc-upload:svc-upload /srv/uploads
systemctl daemon-reload
systemctl enable upload-api --now 2>/dev/null || true
# ensure the venv python exists but the service still fails:
rm -f /home/svc-upload/venv-broken/bin/python3
# (ExecStart names `python`; symlink missing => unit fails, journal
#  shows "status=203/EXEC")

# --- fault 2: listener bound to loopback (T2) ----------------------
# http.server above binds 0.0.0.0 by default; to stage T2 properly we
# instead ship a wrapper that binds 127.0.0.1:
cat > /home/svc-upload/run-api.sh <<'WRAP'
#!/bin/bash
exec python3 -m http.server 8080 --bind 127.0.0.1 --directory /srv/uploads
WRAP
chmod +x /home/svc-upload/run-api.sh
sed -i 's|ExecStart=.*|ExecStart=/home/svc-upload/run-api.sh|' \
  /etc/systemd/system/upload-api.service
systemctl daemon-reload

# --- fault 3: journald vacuum-able bloat (T3) ----------------------
journalctl --rotate
for i in $(seq 1 40); do logger "exam noise line $i"; done
# (a course-sized stand-in for 1.2 GiB; on the real template, pre-fill
#  /var/log/journal with an exported 1.2 GiB from a prior cohort)

# --- fault 4: sam's ownership + mode faults (T4) -------------------
sudo -u sam mkdir -p /home/sam/bin /home/sam/data
sudo -u sam bash -c 'echo "echo hello" > /home/sam/bin/report.sh; chmod 600 /home/sam/bin/report.sh'   # not executable by owner? 600 => no x
sudo -u sam bash -c 'echo data > /home/sam/data/metrics.csv; chown root:root /home/sam/data/metrics.csv' # needs root: chown via sudo drop-in below
# NOTE: the chown above needs privilege; use:
chown root:root /home/sam/data/metrics.csv

# --- fault 5: disk "full" that is a deleted-open file (T7) ---------
fallocate -l 600M /var/tmp/examfill.bin
python3 - <<'PY' &
import time, os
f = open('/var/tmp/examfill.bin','wb')
os.unlink('/var/tmp/examfill.bin')   # deleted but open: df full, du blind
time.sleep(7200)
PY
echo $! > /run/examfill.pid

# --- fault 6: repo with a credential file (T11) --------------------
sudo -u sam bash -c '
  mkdir -p ~/examrepo && cd ~/examrepo && git init -q
  echo "print(1)" > run.py
  echo "flask==3.0" > requirements.txt
  echo "DATABASE_URL=postgres://admin:hunter2@db.local/ds" > secrets.env
  echo done > README.md
'
# git user config for commits:
sudo -u sam git config --global user.email sam@example.edu
sudo -u sam git config --global user.name "Sam Student"

# --- cron job that never fires (T10) -------------------------------
cat > /var/spool/cron/crontabs/sam <<'CRON'
# note: no newline-terminated line, and PATH lacks git -- classic
0 3 * * * /home/sam/backup.sh >> /home/sam/backup.log 2>&1
CRON
cat > /home/sam/backup.sh <<'BK'
#!/bin/bash
rsync -a ~/examdata/ ~/backups/
BK
chown sam:sam /home/sam/backup.sh && chmod 700 /home/sam/backup.sh
# fault: backup.sh not executable by sam? chmod 700 IS executable by owner.
# The real fault: the crontab file must be owned by sam and end with a
# newline; ensure ownership:
chown sam:crontab /var/spool/cron/crontabs/sam && chmod 600 /var/spool/cron/crontabs/sam
# The planted defect: rsync absent from cron PATH is NOT a thing
# (absolute path not needed since /usr/bin in default cron PATH);
# the actual planted fault is that ~/backups does not exist and rsync
# copies INTO it only with trailing slash semantics sam got wrong:
sudo -u sam mkdir -p /home/sam/examdata
sudo -u sam bash -c 'echo csv,content > /home/sam/examdata/a.csv'
# backup.sh uses `rsync -a ~/examdata/ ~/backups/` which works; the
# planted fault is therefore the MISSING newline above? No — keep the
# exam honest: the fault is backup.sh lacks +x:
chmod 600 /home/sam/backup.sh

# --- exam data tree (T9, T12) --------------------------------------
sudo -u sam bash -c '
  mkdir -p ~/examdata/{raw,proc}
  head -c 2048 /dev/urandom | base64 > ~/examdata/raw/big1.csv
  echo "id,v" > ~/examdata/proc/t.csv
  dd if=/dev/zero of=~/examdata/proc/huge.bin bs=1M count=2 2>/dev/null
'

echo "staging complete — snapshot now."
```

**Staging notes for the instructor**

- Snapshot **after** `stage-practical.sh` prints its final line; the
  python background job holding the deleted file must survive the
  snapshot (it does — process state is captured).
- If your template lacks Docker images, `docker pull
  python:3.12-slim` before snapshotting (offline exam rooms).
- Total planted faults: **6** — (1) unit ExecStart dead interpreter,
  (2) loopback-only bind, (3) journal bloat, (4) sam's mode+ownership
  pair, (5) deleted-open file eating disk, (6) `backup.sh` mode 600
  + cron never ran. The repo credential file (T11) and the
  dump_*.bin files (T6) are *workloads*, not faults.

## Part I — Service rescue (25 pts)

**T1 (10).** Evidence chain: `systemctl status upload-api` →
`systemctl journal -u upload-api` shows `status=203/EXEC` (the
dead `venv-broken/bin/python`). Fix options, any acceptable: point
`ExecStart` at the working `/home/svc-upload/run-api.sh` wrapper (it
exists) or repair the venv. Required proof: journal line quoted,
`daemon-reload` visible, `systemctl is-active` + `is-enabled` both
positive. **Cap 6/10** if only the wrapper switch is done with no
journal evidence. **Zero** if the student edits the unit at *system*
scope with `sudo systemctl edit` replacing User — the service must
stay `svc-upload` (least privilege).

**T2 (8).** Root cause: wrapper binds `--bind 127.0.0.1`. Evidence:
`ss -tlnp | grep 8080` shows `127.0.0.1:8080`. Fix: change the bind
to `0.0.0.0` in `run-api.sh` (or the unit), restart. Client-side
proof: from the VM, `curl http://<VM-own-LAN-IP>:8080/` succeeds
(proves non-loopback reachability); full marks also for stating
that on a real second machine `curl http://<server-ip>:8080/` is the
proof, and simulating it via the VM's own non-loopback address.
**Cap 4/8** if they only rebind but never show a non-loopback
curl.

**T3 (7).** Correct tool: `sudo journalctl --vacuum-time=7d` (and/or
`--vacuum-size=`), then make it permanent via
`/etc/systemd/journald.conf` → `MaxRetentionSec=7day` +
`SystemMaxUse=` (or a drop-in). Before/after:
`journalctl --disk-usage`. **Zero** if they `rm -rf` journal files
directly (taught anti-pattern); **cap 4/7** for deleting rotated
syslog files instead of using the journal's own vacuum.

## Part II — Identity & permissions (25 pts)

**T4 (9).** Two faults:
- `report.sh` mode `600` → owner has no `x`: sam's "can't run" —
  fix `chmod 700` (owner-exec only; `755` acceptable but wider than
  needed → **cap 7/9**).
- `metrics.csv` owned `root:root` → sam can't read "own" data — fix
  `sudo chown sam:sam` (or `chgrp` + group bits if framed as a
  group dataset). Least-privilege framing is graded: adding sam to
  `root` group = **0 for that fault**.
Evidence: `ls -l` before/after both files, `namei -l` accepted as
bonus diagnosis.

**T5 (8).** Required end state: `/srv/lab` → `chgrp labteam`,
`chmod 2770` (SGID + group write, no other), members in `labteam`.
Property proofs (2 pts each):
1. *both can create*: two `touch`es as different users, both succeed.
2. *files group-writable immediately*: `ls -l` after creation shows
   `rw-rw----`/group `labteam` — proving SGID inheritance (not a
   post-hoc chmod).
3. *no cross-delete*: as sam, `rm <other-user's file>` fails
   — requires the **sticky bit** `1` too, i.e. mode `3770`/`1770`
   … **instructor note**: with mode `2770` cross-delete *succeeds*
   (group write allows unlink). To make the third requirement
   achievable, the directory must be `chmod 3770` (SGID + sticky,
   group-writable). Accept either: student notices and uses
   `3770` (full marks), or correctly states the tension and
   documents the trade-off (7/8).

**T6 (8).** Dry-run first (the gradeable act):
```console
$ ls dump_*.bin            # SEE the expansion before deleting
$ ls dump_*.bin | wc -l    # 500 expected
$ ls dump_*.bin | xargs rm -v   # or find -name 'dump_*.bin' -delete
$ ls dump_*.bin 2>&1 | wc -l    # 0 after
```
Full marks: dry-run shown + exact-match pattern + final count 0 +
no other file touched (`ls | wc -l` before/after). Any wildcard
without prior listing = cap 3/8.

## Part III — Disk & data (25 pts)

**T7 (10).** Evidence path: `df -h` (full) vs `du -xsh /* 2>/dev/null
| sort -h` (no big dir) → the classic [deleted-but-open] signature;
confirm `sudo lsof +L1 | sort -k7 -h | head`. Safe fix: the holding
process is the staged filler (`/run/examfill.pid`) —
`kill $(cat /run/examfill.pid)` frees 600 MiB. No user data touched.
Proof: `df -h` after shows ≥500 MiB freed + one-line explanation.
**Cap 6/10** if they truncate logs instead (also valid in real life,
but here the pid file is the planted mechanism); **zero** if they
delete anything under `/home` or `/srv`.

**T8 (8).** Reference:
```console
$ dd if=/dev/zero of=~/examfs.img bs=1M count=100
$ mkfs.ext4 -F ~/examfs.img        # any course filesystem OK
$ sudo mount -o loop ~/examfs.img /mnt/examfs
$ sudo blkid ~/examfs.img          # grab UUID
$ echo "UUID=<uuid> /mnt/examfs ext4 loop 0 2" | sudo tee -a /etc/fstab
$ sudo umount /mnt/examfs && sudo mount -a
$ findmnt /mnt/examfs              # proof
```
Grading: `findmnt` proof (4), UUID-form (not device-path) fstab
entry (2), `mount -a` discipline before claiming success (2). One
typo tolerated **only** if the student ran `mount -a` and read its
error before fixing (the transcript shows it); two blind typos = cap
4/8. `nofail` option accepted as good practice (bonus +1, cap at 10).

**T9 (7).** Any correct pipeline; reference:
```console
$ cd ~/examdata
$ { printf 'total csv bytes: '; find . -name '*.csv' -printf '%s\n' | awk '{s+=$1} END{print s}';
    printf 'files > 1MiB: '; find . -type f -size +1M | wc -l;
    printf '%s\n' 'ten largest:';
    find . -type f -printf '%s %p\n' | sort -rn | head -10; } > report.txt
```
Graded on the three sections existing and being *true* for the tree
(2/2/2) + report in tree root (1).

## Part IV — Network & workflow (25 pts)

**T10 (8).** Fault: `backup.sh` is mode `600` — cron executes it as
sam and gets `Permission denied`; cron's mail (or absence of the log
file) is the evidence. Diagnosis: `crontab -l`, notice the log never
grew → `ls -l ~/backup.log` missing → test `~/backup.sh` manually →
`ls -l` shows non-executable. Fix: `chmod 700`. Proof of firing:
edit schedule to `* * * * *` (or `systemctl list-timers` if using a
timer), wait, show `backup.log` + `ls ~/backups` populated, then
*restore the nightly schedule*. Forgetting to restore = cap 5/8.

**T11 (9).** Reference:
```console
$ cd ~/examrepo
$ git status --short                # M run.py, M README.md, ?? secrets.env
$ git add run.py README.md          # explicit, not -A
$ git commit -m "Fix run script and add readme"
$ echo "secrets.env" >> .gitignore
$ git add .gitignore && git commit -m "Ignore local secrets file"
$ git log --oneline -3 && git status --short   # clean except nothing
```
Grading: explicit adds (3), durable ignore rule (3), both proofs
(3). Any `git add -A`/`git add .` = cap 4/9. If they *deleted*
`secrets.env` instead: 0 — the file must remain untracked (deleting
evidence, not securing it).

**T12 (8).** Reference:
```console
$ docker run --rm -v "$HOME/examdata:/data:ro" python:3.12-slim \
    sh -c 'find /data -name "*.csv" -type f -exec cat {} + | wc -l'
```
Key graded elements: `:ro` (2), bind mount path correct (2), count
output correct — the staged tree has 2 csv files, `big1.csv` is one
line, `t.csv` one line → expected `2` (2), `--rm`/clean exit (2).
Accept `wc -l < <(cat …)` variants and `xargs cat | wc -l`; the
count must match the tree (2 lines total).

## Zero-score triggers (whole-exam)

- `rm -rf` outside the three whitelisted areas.
- Any `mkfs`/`dd of=` aimed at a real block device instead of the
  loopback image file.
- Transcript gaps (session restarted without `script`) — the
  affected part is ungradeable and scores 0.
- Fixing faults by deleting the *evidence* (journal, logs) rather
  than the cause.
