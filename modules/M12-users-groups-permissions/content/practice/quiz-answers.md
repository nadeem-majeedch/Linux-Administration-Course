# Module 12 Quiz — Answer Key

1. username, password-placeholder (x), UID, GID, GECOS/comment, home, shell.
2. root = UID 0; humans start at 1000.
3. `/etc/passwd` must be world-readable (tools map names→UIDs constantly);
   keeping hashes in root-only `shadow` removes offline cracking material
   from every user's reach.
4. Exactly one primary GID per user (stamps new files — M13 exploits this);
   supplementary groups only *grant* access, stamp nothing.
5. All supplementary groups are replaced by just `students` (e.g., `sudo`
   revoked silently). `-aG` appends instead.
6. `useradd` (primitive) and `adduser` (Ubuntu/Debian-friendly, prompts,
   skeleton home).
7. The account exists to *own things* (services, robots), not to log in
   interactively.
8. Could have removed `o+w`, `o+x`, and any combination — `=` sets others to
   *exactly* read, clearing write and execute. (Owner/group untouched.)
9. (a) 600 (b) 664 (c) 755.
10. Create, rename, **delete entries** in it — including files owned by
    others. Directory-write is the delete-decider.
11. `x` = traverse (pass through, reach known children); `r` = list names.
    111: cd works, ls denied.
12. No. Check order: you're the owner (owner bits apply: `rw-` — wait, owner
    is you: 604 → owner rw → you CAN read... the *trap* version: if the mode
    were `--4` with you owner, owner bits `---` win and group/other never
    consulted). Rule: first matching audience wins; no fall-through.
13. 666 for files, 777 for directories.
14. Files: 666−027 = 640 (`rw- r-- ---`). Dirs: 777−027 = 750.
15. The parentheses run it in a *subshell*; the mask change dies with it.
16. `664` (or 66x-variants) with **group bits doing the work** — and the
    folder's group set to the lab group (M13 makes this systematic).
17. It grants everyone everything because the *group design* wasn't done —
    it trades an access problem for an audit/ownership hole (anyone may
    plant/replace/delete files; directory-w deletes others' work).
18. `chgrp`; `chown` (owner+group: `chown user:group`); `passwd`.
19. `who`: logged-in sessions; `w`: same + their activity/load; `whoami`:
    just my own effective username.
20. Sample: `jupyter` service account, nologin, UID<1000, owns
    `/srv/jupyter`; students UIDs ≥1000, shells, own `~` homes; groups:
    `students` (r on datasets), `staff` (rw on datasets); dataset dirs
    750/640, homes 700; staff in both groups. (M13 formalizes the
    setgid/default-ACL machinery that keeps it self-maintaining.)
