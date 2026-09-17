# Module 23 Troubleshooting — Transfer Symptoms → Causes → Fixes

> Eight patterns, ordered by how often they hit real users. Every
> diagnosis is safe on your own VM; nothing here touches a shared
> system. Each: **symptom → likely cause → diagnosis → fix →
> prevention**.

## 1. `ssh: connect to host ... port 22: Connection refused`

**Cause:** sshd not running/not installed on the remote (or wrong
port).
**Diagnose:** `ssh vm 'systemctl is-active ssh'` (Ubuntu service
name: `ssh`); locally `ss -tlnp | grep :22`.
**Fix:** on the remote, `sudo systemctl enable --now ssh`.
**Prevention:** M22's key-setup lab ends with a connectivity test —
make it part of every environment checklist.

## 2. `Permission denied (publickey)` — but the key works elsewhere

**Cause:** remote `~/.ssh` or `authorized_keys` permissions are too
open (M14/M22 rules: `.ssh` 700, `authorized_keys` 600), or the key
isn't being offered.
**Diagnose:** `ssh -v vm 2>&1 | grep -i 'offering\|denied'` — see
which identity is offered.
**Fix:** on the remote, correct modes (`chmod 700 ~/.ssh; chmod 600
~/.ssh/authorized_keys`).
**Prevention:** never debug file transfers by *loosening* remote
permissions; fix the modes.

## 3. rsync: `skipping directory` or empty transfer with exit 0

**Cause:** the trailing-slash trap in reverse — you synced the
*directory entry* to a path that already existed, or sourced a
pattern that matched nothing.
**Diagnose:** re-run with `-vvv` (or `-n -v`) and read the
*destination paths*, not just the summary.
**Fix:** decide the shape deliberately (contents vs container) and
re-run; verify with `find dest -type f | head`.
**Prevention:** the two-line slash rule from Lesson 2, applied
every time; dry-run is not optional.

## 4. Transfer "succeeds" but the file is missing on the remote

**Cause:** relative-path drift — the remote `rsyncd`/ssh session
started in a different home directory than assumed, or `~`
expanded differently (remote shell changed).
**Diagnose:** `ssh vm 'pwd; ls -la'` immediately after the run;
check your log's destination line.
**Fix:** use explicit absolute destinations (`vm:/home/dsstudent/...`)
for anything scripted.
**Prevention:** scripts always use absolute remote paths; `~` only
in interactive one-offs.

## 5. `rsync error: some files/attrs were not transferred` (exit 23)

**Cause:** permission problems on the destination — often an M13
shared tree where your account lacks write on *some* subdirectories,
or the sync tried to preserve ownership it cannot set.
**Diagnose:** run with `-v`; the failing paths are named. Check
with `namei -l <path>` (M06) to see every directory's permissions
along the way.
**Fix:** sync to a location you own, or have the dataset admin add
your group (M13), not sudo-force.
**Prevention:** check destination writability with a 1-byte
`touch` test before a 5 GB sync.

## 6. Sync finishes but the remote copy "looks different"

**Cause:** metadata-only changes (touch/mtime churn from builds) —
size+mtime comparison re-sent everything, or conversely an
in-place same-size edit slipped past size+mtime.
**Diagnose:** your `speedup is` trend; then an audit-grade
`rsync -avhc --dry-run` or the sha256 manifest diff.
**Fix:** for claims, not syncs — always the manifest check.
**Prevention:** `--exclude` build outputs; audit with checksums
when it *matters*.

## 7. Huge tree sync is glacial despite gigabit link

**Cause:** per-file negotiation (tens of thousands of small files),
or `-z` burning CPU on incompressible data, or excluded-noise
inflation.
**Diagnose:** the log's files/sec; try `tar cf - . | ssh vm 'tar
xf -'` for comparison.
**Fix:** archive-stream for one-shots; aggressive `--exclude`;
drop `-z` for compressed formats.
**Prevention:** measure first (Challenge 2); choose the tool by
*file count*, not habit.

## 8. Unattended rsync hung for hours, did nothing

**Cause:** no SSH key on the cron account → the job is blocked on a
password prompt no one will ever answer.
**Diagnose:** `ps aux | grep rsync`; inspect the child `ssh`
process; run the exact command once interactively.
**Fix:** install key auth for the service account (M22); add
`-o BatchMode=yes` so failure is immediate next time.
**Prevention:** every automation transfer uses `BatchMode=yes` —
loud failure beats silent hang.
