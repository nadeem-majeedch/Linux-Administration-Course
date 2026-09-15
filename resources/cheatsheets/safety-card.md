# Safety Card — Read Before Every Lab

## Before risky work (disks, partitions, configs, firewall)

- [ ] VM **snapshot taken** (named, dated)
- [ ] Backup of the exact files/dirs the command will touch
- [ ] Destructive command read **twice** — paths, globs, flags
- [ ] Second terminal open (firewall/SSH changes) — prove access before closing the first

## The command watchlist

| Command | Danger | Safeguard |
|---|---|---|
| `rm -rf PATH` | permanent, recursive delete | `ls` the glob first; sandbox dirs only; never `~`, `/`, or vars |
| `mkfs`, `parted`, `dd` | destroys a disk/filesystem | VM virtual disk only, never the system disk, after snapshot |
| fstab edits | a typo can block boot | backup the file; `findmnt --verify`; keep snapshot |
| `rsync --delete` | deletes extras on target | `--dry-run` first, read the list |
| `crontab -r` | removes ALL your jobs, silently | `crontab -l` first; edit with `-e` |
| `docker system prune` | deletes containers/images/volumes | read what it removes; use scoped flags |
| firewall enable over SSH | can lock you out | allow SSH rule first; second session open |
| `chmod -R` on wrong dir | can break system tools | explicit absolute paths, never `..`, check with `ls` first |
| `history` re-run of `!!` with sudo | repeats the WRONG command | read before Enter; don't chain `sudo !!` carelessly |

## Habits that keep you employed

1. **Never run what you can't explain.** Look it up; that's the course teaching you.
2. **Streams before files, copies before originals.** Work on copies; move into place.
3. **Dry-run flags exist — use them** (`rsync -n`, your own `--dry-run`).
4. **`-i`/interactive on deletes until reflex-level careful.**
5. **Absolute paths in scripts**, quoted variables everywhere.
6. **Secrets never in Git, never in commands with visible args** — env files, 600 perms.
7. **Snapshots are not backups.** Back up to a second location; test restores.
8. **On shared servers: ask before you elevate.** Your sudo is logged; your mistakes are shared.
