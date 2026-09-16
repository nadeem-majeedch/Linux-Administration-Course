# Troubleshooting — Module 20

Symptom → cause → check → fix → prevention. Own VM for anything
state-changing; five-part writeups per the labs.

## 1. `Failed to start …: Unit not found`

- **Cause:** typo in the unit name, or the unit file isn't where
  systemd looks (or wasn't reloaded).
- **Check:** `systemctl list-unit-files | grep <name>`; `ls
  ~/.config/systemd/user/` (user) or `/etc/systemd/system` (system).
- **Fix:** fix the name/path; `systemctl --user daemon-reload` if a new
  file.
- **Prevention:** tab-complete unit names; daemon-reload after
  authoring (Lab 2 incident 1).

## 2. Status shows `failed (Result: exit-code)` with code 203/EXEC

- **Cause:** ExecStart path doesn't exist or isn't executable (or
  starts with a shell construct — ExecStart doesn't run a shell).
- **Check:** the journal line names the exact path; `ls -l <path>`;
  `systemd-analyze --user verify <unit>`.
- **Fix:** correct the path, `chmod +x`, or wrap in
  `/bin/bash -c '…'` when shell syntax is needed.
- **Prevention:** verify before start; absolute paths (with %h for
  user units).

## 3. Service enters `activating (auto-restart)` forever

- **Cause:** process exits immediately (self-daemonizing script +
  Type=simple is the classic) or crashes on startup; Restart= keeps
  rescheduling.
- **Check:** `journalctl --user -u UNIT -n 20` — read the *process's*
  error before the restart lines; check Type= vs actual behavior.
- **Fix:** fix the script (stay in foreground) or set the honest
  Type=; add RestartSec= to slow the churn while diagnosing.
- **Prevention:** the Type= decision tree; test the raw command by
  hand first (Lab 1 Station 3 did exactly this).

## 4. "My edit has no effect"

- **Cause:** no daemon-reload, or you edited a file systemd isn't
  reading (wrong dir, or a drop-in overriding you).
- **Check:** `systemctl --user show UNIT -p <Property>` — loaded value
  vs file; `systemctl cat UNIT` shows the *effective* merge.
- **Fix:** `daemon-reload` (+ restart); move the edit into a proper
  drop-in.
- **Prevention:** `systemctl edit` (auto-reloads, merges visibly).
  (Lab 2 incident 3.)

## 5. User service dies at logout

- **Cause:** no lingering — the user manager shuts down with the last
  session.
- **Check:** `loginctl show-user $USER -p Linger`.
- **Fix:** `sudo loginctl enable-linger $USER`; confirm the service is
  `enable`d too (lingering alone doesn't start units).
- **Prevention:** linger + enable are a pair; set them together.

## 6. `sudo systemctl restart ssh` hung the session / dropped connection

- **Cause:** restarting the daemon *you are connected through*; or
  restart instead of reload while sessions were live.
- **Check:** reconnect on a second terminal *before* touching ssh;
  `systemctl cat ssh -p ExecReload` for reload support.
- **Fix:** reconnect (the old session died with the restart);
  prefer `reload` for config changes.
- **Prevention:** the two-terminal rule for ssh changes; Lab 1
  Station 2 rehearses it.

## 7. Boot waits ~90s then drops to emergency shell

- **Cause:** fstab entry for a missing device without `nofail` (M17's
  echo), or a failed mount unit.
- **Check:** the emergency console names the failing unit
  (`mnt-data.mount`); `journalctl -b | grep -i mount`.
- **Fix:** `mount -o remount,rw /`, fix/comment the fstab line,
  `mount -a`, reboot. Or boot GRUB-edit `rescue.target`.
- **Prevention:** M17's verify workflow; `nofail` on all non-root
  mounts.

## 8. `journalctl -u X` says "No journal files were found" (as user)

- **Cause:** user journaling off / no entries yet, or you queried a
  *system* unit without sudo (permission model).
- **Check:** `journalctl --user -u UNIT` vs `sudo journalctl -u UNIT`;
  `ls /var/log/journal` (persistent storage present?).
- **Fix:** the right namespace + sudo for system units; enable
  persistent storage (`sudo mkdir -p /var/log/journal` +
  `systemctl restart systemd-journald`) if needed.
- **Prevention:** know the user/system journal split (M24 goes deep).

## 9. Clock wrong after VM pause/resume — TLS/cron errors

- **Cause:** guest clock drift; NTP not re-syncing.
- **Check:** `timedatectl` (synchronized? NTP active?);
  `journalctl -u systemd-timesyncd -n 10`.
- **Fix:** `sudo timedatectl set-ntp true`; if stuck,
  `systemctl restart systemd-timesyncd`. On hypervisors, install
  guest additions/integration tools for clock sync.
- **Prevention:** `timedatectl` in the morning routine; UTC everywhere
  on servers.

## 10. `systemctl` works as root, `--user` says "Failed to connect to bus"

- **Cause:** running `systemctl --user` from a context without your
  user session (sudo shell, cron, some SSH configs).
- **Check:** `echo $XDG_RUNTIME_DIR` (unset in the broken context);
  `loginctl show-user $USER -p Linger`.
- **Fix:** run from a real login session; with lingering on,
  `sudo machinectl shell $USER@` or `systemctl --user -M $USER@`
  reaches the manager properly.
- **Prevention:** automation that manages user units should target the
  user manager explicitly (`-M user@host` style), not assume a session.
