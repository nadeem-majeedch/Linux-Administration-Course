# Lab Infrastructure — Room, Snapshots, Staging, Exam Stations

> The course's infrastructure philosophy in one line: **students break
> things on purpose, so restores must be cheaper than repairs.**
> Everything below serves that.

## 1. Room profile

| Requirement | Minimum | Comfortable |
|---|---|---|
| Student machines | 8 GiB RAM, 25 GiB free disk, VT-x on | 16 GiB RAM |
| Projector | 1080p, shows terminal 20 pt+ | + a second display for YOUR VM |
| Network | outbound HTTPS (pypi, ubuntu archive) | no inbound needed, ever |
| Accounts | students are **not** machine-admin on lab PCs | VirtualBox portable on USB |

**No inbound network is a feature:** every SSH/transfer/netcat lab in
this course runs **inside one VM** (loopback, VM-to-host, VM-to-VM) —
the lab path never requires students to reach each other's machines.
That keeps the course legal on any campus network by default.

## 2. Snapshot strategy (the load-bearing wall)

Teach this as a *lifecycle*, not a feature:

```text
pristine  →  CLEAN+USERS  →  per-module checkpoint
   │              │                  │
   │              │                  └─ taken at END of each module's
   │              │                     lab; named MXX-done
   │              └─ after users/packages pre-installed (instructor)
   └─ before ANY lab touches users/services/disks
```

- **Rule for students:** snapshot before the lab, restore *forward
  only* — reverting to an old checkpoint to dodge a mistake costs the
  practice that mistake was for. (Break-and-repair is the curriculum;
  snapshot-escape is its enemy.)
- **Rule for instructors:** exam/LA stations restore from a *staged
  fault* snapshot, never from student state.
- **Storage math:** ~2–4 GiB per snapshot chain per term; compact
  (`VBoxManage modifymedium --compact`) after term end.

## 3. Shared-dataset staging (for M08/M13/M23/M31 labs)

Labs that need a "shared" dataset simulate the share **inside each
student's VM** — a `/srv/datasets`-style tree owned by a lab user,
with the student's user gaining group access. Staging script (runs
once per student VM, ~1 min):

```bash
#!/usr/bin/env bash
# stage-datasets.sh — instructor provides; student runs in THEIR VM.
set -euo pipefail
sudo groupadd -f dsdata
sudo usermod -aG dsdata "$USER"
sudo mkdir -p /srv/datasets && sudo chown root:dsdata /srv/datasets
sudo chmod 2775 /srv/datasets
sudo -u root bash -c 'for f in sales.csv sensors.csv; do
  head -c 200000 /dev/urandom | base64 > "/srv/datasets/$f"; done'
sudo chown root:dsdata /srv/datasets/*.csv && chmod 664 /srv/datasets/*.csv
echo "done — log out & back in for group membership"
```

This gives every permissions/transfer lab its realistic multi-user
texture **without any real shared server**. If your program *does*
have a real teaching server, M22/M31 labs document the SSH flows —
but nothing requires one.

## 4. Exam & LA stations

Per the [practical exam's staging guide](../../assessments/practical/practical-key.md):

- One Ubuntu **Server** (no desktop) template VM per station
- Staging script applied → snapshot `EXAM-FAULTS-IN` → verify once
  yourself against the answer key
- Per candidate: restore → hand out → 90 min → collect
  `script` transcript → restore
- The transcript **is** the submission: one shared folder export or
  `scp` off the VM at collection; the grading
  [checklist](../instructor-resources/grading-sheets/practical-checklist.md)
  assumes it exists.

## 5. Contingencies

- **Projector dies:** all demos in [`demonstrations/`](../demonstrations/demo-index.md)
  list their commands inline — run the session from a single printed
  demo sheet.
- **Network outage:** offline alternates are marked per lab; the core
  weeks (1–6) need no network after install. Package weeks (M15/M16)
  do — schedule them when the archive mirror is reachable, or use the
  apt-cacher note in `SETUP.md` troubleshooting.
- **Student VM destroyed beyond repair:** restore `pristine`, replay
  only the current module's setup (≤ 10 min by design — this is why
  per-module checkpoints exist).
