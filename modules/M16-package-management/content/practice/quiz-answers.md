# Answer Key — Module 16 Quiz

Each answer cites the lesson to revisit.

1. Repository stores+signs packages; apt resolves deps, downloads,
   orchestrates; dpkg installs/removes files and owns the local database.
   (L1 §1)
2. `dpkg -S /path` = which installed package owns this file; `apt policy
   pkg` = which source would provide/win a package. (L1 §2, L2 §1)
3. `ii` = desired install, status installed; `rc` = removed, config
   files remain. (L1 §2)
4. dpkg does no dependency resolution; use `sudo apt install ./foo.deb`
   (the `./` makes it a path, not a package name). (L1 §2)
5. update refreshes the *lists*; upgrade performs the installs.
   "Unable to locate package" for software that exists = stale lists.
   (L1 §3)
6. remove uninstalls, keeps /etc config; purge uninstalls + config;
   autoremove clears dependencies nothing else needs. All three leave
   `/home` alone — user data is never package-owned. (L1 §3)
7. A dependency conflict wants to *remove* installed software; stop and
   read — never accept blind. (L1 §4)
8. **`apt install --dry-run pkg`** (or `-s`) — resolves and reports
   without touching the system. The line to read: "The following
   packages will be **REMOVED**" (and the upgrade count) — a silent
   cascade removal is exactly what the preview exists to catch. (L1 §4, Lab 1 Part D)
9. main (Canonical-supported, free), restricted (supported, proprietary),
   universe (community, free), multiverse (license-restricted). (L2 §1)
10. Much of the science stack (and its languages) lives in universe —
    community support means *your* security vigilance matters more. (L2 §1)
11. The repository's signed index (InRelease) against a trusted key in
    /etc/apt/keyrings (or legacy apt-key store). (L2 §2)
12. The index's signature has no matching trusted key — apt refuses the
    source (blocking forged repos). Legitimate fix: obtain the key from
    the *vendor's official instructions*, verify its fingerprint, install
    to /etc/apt/keyrings, reference via signed-by. Never disable checks.
    (L2 §2)
13. Operational: no update/security pipeline — maintainer vanishes, you're
    frozen. Security: maintainer scripts run as root at install/upgrade —
    a hostile or compromised PPA is arbitrary root code. (L2 §3)
14. `noble-security` (release-security suite); automated by
    `unattended-upgrades`. (L2 §1, §4)
15. `rpm -qf /path` (or `dnf provides`); `dnf install`; `dnf autoremove`.
    (L3 §2)
16. FHS designates /usr/local for locally-administered software, so it
    never collides with apt's /usr — dpkg-owned and hand-installed files
    stay separable. (L3 §1; M06)
17. Only `make install` (copying into /usr/local) needs root by default;
    a home prefix makes the copy target user-writable — no sudo, trivial
    removal. (L3 §1)
18. apt owns the OS + system libs; pip/conda own language packages
    *inside environments*. PEP 668 stops pip from overwriting
    apt-owned files in the system python (breaking OS tooling);
    venvs are the sanctioned space. (L3 §3)
19. A dev-headers package (`libpq-dev`; plus build tooling), found via
    `apt search`/`apt show` — and confirmed with `dpkg -S pg_config`
    once installed. (L3 §1, §3)
20. `--dry-run` = rehearsal: read the exact NEW/REMOVED summary before
    acting; `--no-install-recommends` = slimmer installs (containers,
    servers) when optional extras aren't wanted. (L1 §4, L3 §3)
