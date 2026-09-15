# Module 06 Quiz — Answer Key

1. The current working directory (the shell's location in the tree). Reflexive
   use because *every* relative path and every risky operation depends on it.
2. Up to `/home/dsstudent`, then into `data` → `/home/dsstudent/data`.
3. Any three: `-l` long listing; `-h` human sizes; `-a` include hidden;
   `-t` sort by mtime; `-r` reverse; `-d` describe the directory itself.
4. `ls /tmp` lists the *contents*; `ls -ld /tmp` describes *the directory
   itself* (its permissions, owner, dates).
5. Newest-modified first (`-t`); sizes in human units (`-h`, e.g. `117M`).
6. `.` = this directory; `..` = its parent — real entries, basis of relative
   paths.
7. Convention: `ls` (and globs) skip dot-prefixed names to keep views clean;
   `ls -a` (or `-A`) lists them.
8. Absolute: starts with `/`, same meaning from anywhere. Relative: from the
   current directory. Rule: scripts use absolute (they can't know the caller's
   cwd).
9. `..` (from `/usr/share/doc` up one level) — or `../` equivalently.
10. `~` → your home (`/home/dsstudent`); `~ben` → Ben's home (`/home/ben`).
11. `~` is *shell* expansion — done by bash before the program runs. Programs
    reading config files directly (or non-shell contexts) may never expand it;
    use full paths there.
12. `/etc/ssh` → up two → `/` (root).
13. `/etc`.
14. `/proc`, `/sys`, `/run` (and `/dev`'s nodes are device *files*, mostly
    generated too).
15. It's typically wiped (or at least *unreliable*) — scratch only; nothing
    valuable, no results, no secrets.
16. Symlinks are transparent: a request for `/bin/ls` resolves to
    `/usr/bin/ls`; old paths and docs keep working.
17. `-p` creates all missing parent directories and is idempotent — existing
    target: no error, exit 0.
18. Contents untouched (still 0 bytes if empty); the modification timestamp is
    updated.
19. Shell expands braces *before* mkdir runs: `p/a/c` and `p/b/c` plus all
    missing parents → 4 directories (`p`, `p/a`, `p/b`, `p/a/c`, `p/b/c`
    = 5 total if p was missing; 2 children + their parents).
20. Any two with reasons: `raw/` never modified (reproducibility — everything
    rebuilds from originals); dated experiment folders (filesystem as version
    history); logs accumulate in `logs/` (M24 evidence); lowercase-no-spaces
    (script safety).
