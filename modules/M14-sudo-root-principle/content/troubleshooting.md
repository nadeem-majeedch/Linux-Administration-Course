# Troubleshooting — Module 14

Symptom → cause → check → fix → prevention. VM/WSL2 scoped, as always.

## 1. `user is not in the sudoers file. This incident will be reported.`

- **Cause:** policy has no matching rule for you — group membership,
  drop-in, or both are missing/misnamed.
- **Check:** `groups | grep -w sudo`; `sudo -l` (as another admin if you
  have one); `sudo visudo -c` for parse errors.
- **Fix (your VM, from recovery or another admin):**
  `sudo usermod -aG sudo YOURUSER` — then log out/in (group changes apply
  at next login; see M12).
- **Prevention:** know *where* your grant lives: group rule in
  `/etc/sudoers`, or a drop-in in `/etc/sudoers.d/` (Lab 2 Ticket B).

## 2. `sudo: command not found` — for a command you can normally run

- **Cause:** `secure_path` (Default) replaces your `PATH` under sudo;
  tools installed in `~/.local/bin`, `~/bin`, or a conda env aren't on it.
- **Check:** `echo $PATH` vs `sudo printenv PATH`.
- **Fix:** call by absolute path (`sudo /usr/local/bin/mytool`), or install
  the tool system-wide (apt), or add a scoped `Defaults secure_path`
  addition in visudo — never blanket-disable `secure_path`.
- **Prevention:** privileged operations should use system-installed tools.

## 3. Redirection "Permission denied" under sudo

- **Cause:** the *shell* (running as you) opens the target file before
  sudo starts.
- **Check:** you're actually root in the failing command? (`sudo whoami`)
- **Fix:** `sudo sh -c 'cmd > file'` or `cmd | sudo tee file`
- **Prevention:** understand the parse order — Lesson 1 §6; it never
  surprises you again.

## 4. Sudo hangs, then: `sudo: unable to stat /var/db/sudo/...`

- **Cause:** the timestamp/lecture directory is on a filesystem that went
  read-only, or perms on `/var/db/sudo` (some systems `/run/sudo`) broke.
- **Check:** `mount | grep ' / '` — look for `ro`; `ls -ld /run/sudo`.
- **Fix:** reboot after fixing the underlying disk error (fsck) — don't
  chown system dirs ad hoc.
- **Prevention:** a read-only root is the *real* incident; sudo symptoms
  just surface it.

## 5. Every sudo asks for password immediately (no 15-min cache)

- **Cause:** `timestamp_timeout=0` (or a very small value) in a
  `/etc/sudoers.d/` drop-in; some tutorials do this.
- **Check:** `sudo grep -r timestamp_timeout /etc/sudoers /etc/sudoers.d/`
- **Fix:** edit that drop-in via `visudo -f`, remove/adjust the line.
- **Prevention:** test hardening tutorials in a VM first (Lab 2 Ticket A).

## 6. WSL2: `sudo: unable to resolve host <name>`

- **Cause:** hostname in Windows changed; WSL's `/etc/hosts` still has the
  old one.
- **Check:** `hostname` vs `cat /etc/hosts`.
- **Fix:** `echo "127.0.1.1 $(hostname)" | sudo tee -a /etc/hosts` (or
  edit via `wsl -u root`).
- **Prevention:** it's cosmetic, but fix it — logs fill with noise.

## 7. `sudo: /usr/bin/sudo must be owned by uid 0 and have the setuid bit set`

- **Cause:** sudo itself lost its SUID bit or ownership (disk corruption,
  a reckless `chown -R`, or a filesystem copied with metadata mangled).
- **Check:** `ls -l /usr/bin/sudo` — should be
  `-rwsr-xr-x root root`.
- **Fix:** from recovery: `chown root:root /usr/bin/sudo && chmod 4755
  /usr/bin/sudo` (or `apt install --reinstall sudo`). This is *why* the
  SUID concept from M13 exists — sudo is itself a setuid binary.
- **Prevention:** never `chown -R` system trees; operate on paths you
  named explicitly.

## 8. `E: Could not get lock /var/lib/dpkg/lock-frontend`

- **Cause:** another apt/dpkg runs (or crashed); the lock is held.
- **Check:** `sudo lsof /var/lib/dpkg/lock-frontend`;
  `pgrep -a apt; pgrep -a dpkg`.
- **Fix:** wait for the live process; if stale:
  `sudo dpkg --configure -a && sudo apt --fix-broken install`.
- **Prevention:** let unattended-upgrades finish before installing
  (Lab 2 Ticket C).

## 9. `sudo -l` shows your rule, but the command still asks for a password

- **Cause:** NOPASSWD rules match the *exact* command string — you ran it
  with arguments, or via a different path (symlink, relative).
- **Check:** compare your command against the rule character-for-character;
  `sudo -l /usr/local/bin/hello-admin` shows what matches.
- **Fix:** wrap arguments *inside* the helper script (root-owned), and
  grant the script only.
- **Prevention:** design rules around zero-argument wrapper scripts
  (Lesson 1 §4).

## 10. After editing sudoers, NOTHING can sudo anymore

- **Cause:** a syntax error written with a plain editor (this is what
  `visudo` prevents).
- **Check (if you still have one root path):** `visudo -c` via recovery.
- **Fix:** GRUB recovery → root shell → `visudo -f /etc/sudoers` repair, or
  WSL: `wsl -u root`. Restore from `/etc/sudoers.pre-*` backups if present.
- **Prevention:** `visudo` always; `visudo -c` after batch changes; keep a
  recovery route practiced (Lab 1 Part E) *before* you need it.
