# Troubleshooting — Module 16

Symptom → cause → check → fix → prevention. Own VM/WSL2; on shared
machines, diagnose then escalate.

## 1. `E: Unable to locate package foo`

- **Cause:** stale lists, typo'd name, or the package lives in a
  component your sources don't have.
- **Check:** `sudo apt update && apt search foo`; `apt policy foo`.
- **Fix:** correct the name; enable `universe` if that's where it lives;
  or accept that no configured repo has it (then: official third-party
  repo per vendor docs).
- **Prevention:** update lists daily, not before every search.

## 2. `E: Could not get lock /var/lib/dpkg/lock-frontend`

- **Cause:** another apt/dpkg is running (or crashed mid-run).
- **Check:** `sudo lsof /var/lib/dpkg/lock-frontend`; `pgrep -a apt;
  pgrep -a dpkg`.
- **Fix:** wait for a live process; if stale:
  `sudo dpkg --configure -a && sudo apt --fix-broken install`. Deleting
  lock files is the last resort, only after confirming no package
  manager runs.
- **Prevention:** one package manager at a time; let unattended-upgrades
  finish (M18 Lab 2 Ticket C drills this).

## 3. `W: GPG error ... NO_PUBKEY ABCD1234`

- **Cause:** a third-party repo whose signing key isn't installed.
- **Check:** which source line the error names — that's the trust
  decision to revisit.
- **Fix:** follow the *vendor's official* key-install instructions
  (fingerprint verify; `/etc/apt/keyrings/` + `signed-by=`). Never
  `--allow-unauthenticated` your way past it.
- **Prevention:** add third-party repos in a disposable VM first (Lab 3).

## 4. `E: You don't have enough free space in /var/cache/apt/archives`

- **Cause:** the small boot/OS partition filled with cached .debs.
- **Check:** `df -h /var`; `du -sh /var/cache/apt/archives`.
- **Fix:** `sudo apt clean` (empties the cache — safe; downloads are
  re-fetchable), then retry.
- **Prevention:** `apt clean` periodically on small-disk VMs; check disk
  before big installs (`df -h` — M17).

## 5. `dpkg: error processing package X (--configure):` / half-installed

- **Cause:** interrupted upgrade (power loss, killed terminal, full
  disk).
- **Check:** `dpkg -l | grep -v "^ii"` — the census of unfinished
  business; `sudo dpkg --audit`.
- **Fix:** `sudo dpkg --configure -a` → `sudo apt install -f` → free disk
  if that was the cause → re-run upgrade.
- **Prevention:** never Ctrl-C an upgrade mid-configure; keep /var
  breathing room.

## 6. `apt update` hangs forever on one URL

- **Cause:** a dead mirror, a captive portal, or a proxy WSL2 inherited.
- **Check:** `Ctrl-C` then re-run with `apt update -o
  Acquire::http::Timeout=5`; note which URL stalls.
- **Fix:** comment out the dead source (reversible, `#`), or switch to
  archive.ubuntu.com / a regional mirror; for WSL2 proxy issues, fix the
  proxy env, not apt.
- **Prevention:** keep sources minimal and official.

## 7. PPA installed, now `apt upgrade` wants to replace system packages

- **Cause:** the PPA's versions out-rank the archive's (same package,
  newer version) — `apt policy` shows who wins.
- **Check:** `apt policy <pkg>` — look at priority + versions.
- **Fix:** prefer `ppa-purge` (downgrades PPA packages properly) over
  hand-removal: `sudo ppa-purge ppa:user/name`.
- **Prevention:** after adding *any* repo, `apt policy` before install
  (Lab 3 Part C).

## 8. `sudo apt upgrade` broke the system python (module errors)

- **Cause:** pip installed into the system python; the upgrade overwrote
  versions pip had replaced.
- **Check:** `pip list 2>/dev/null | head` outside any venv; the
  externally-managed marker: `ls /usr/lib/python3.12/EXTERNALLY-MANAGED`.
- **Fix:** rebuild the system state is painful — the real fix is *move
  the work*: venv/conda (M27), then `sudo apt install --reinstall
  python3-<name>` for OS-broken modules.
- **Prevention:** the course's division rule (Lesson 3 §3) — never
  `sudo pip`.

## 9. WSL2: `apt` can't reach the internet, browser can

- **Cause:** proxy/metrics interference, stale resolv.conf, or
  Windows-side VPN.
- **Check:** `curl -I http://archive.ubuntu.com` inside WSL;
  `cat /etc/resolv.conf`.
- **Fix:** regenerate resolv.conf (or point at 1.1.1.1 as a test),
  unset `http_proxy` if set wrongly; reboot WSL (`wsl --shutdown`) after
  VPN changes.
- **Prevention:** when the network changes, test with curl before apt.

## 10. "I removed it but it's still on disk"

- **Cause:** `remove` keeps config; or you removed the *package* but its
  data lives in a data dir (`/var/lib/postgresql/...`); or it was a snap
  (`snap list`) all along.
- **Check:** `dpkg -l name`; `ls /etc/name /var/lib/name`;
  `snap list | grep name`.
- **Fix:** `sudo apt purge name` for config; delete *data dirs*
  deliberately and only after confirming they're disposable; snap:
  `snap remove name`.
- **Prevention:** know remove vs purge (Lab 2 Part D) and which package
  *format* you installed.
