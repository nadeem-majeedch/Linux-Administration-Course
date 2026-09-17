# Level 1 — Beginner: The First Session

> Assumes M01–M07 · 60–90 min · your own VM · `script level-1.log`
> first. You are a new analyst on day one; this is the orientation
> tour a colleague would give you, except you drive.

## Part 1 — Orient (15 min)

1. Print who you are (`whoami`, `id`), where you are (`pwd`), and
   what machine this is (`hostname`, `uname -a`). One line each —
   you'll need these four facts in every support ticket you ever
   file.
2. Explore by *looking*, not by opening: list your home directory
   with sizes and hidden files; then `ls` `/etc`, `/var/log`,
   `/tmp` — note in `findings.md` one thing each directory is *for*
   (one line, your own words).
3. Create the day's workspace in one command:
   `mkdir -p ~/day1/{raw,work,notes}`.

## Part 2 — Handle files like you mean it (25 min)

Your instructor distributes `day1-bundle.tar.gz` (or you make the
content yourself):

1. Unpack into `~/day1/raw/`. Inventory it: file count, total size,
   the three largest files, the count of `.csv` vs `.txt` — save as
   `notes/inventory.txt` (pipelines welcome; `wc`+`du`+`ls -S`
   suffice).
2. Move all `.csv` into `work/` with one glob. Rename any filename
   containing spaces to use underscores (`mv` with quoting).
3. Copy (not move) the two oldest files into `notes/` as backups —
   prove oldest with `ls -lt | tail`.
4. Make `~/day1/work` read-only *to yourself* (`chmod u-w`),
   attempt to create a file there, capture the error, then restore
   the write bit. Paste both the error and the fix into
   `findings.md` — this is your first diagnostic reflex.

## Part 3 — Look inside (20 min)

1. `cat` one CSV, then view it again with `less` — exit with `q`.
   In `findings.md`: when is `less` the right tool and `cat` the
   wrong one?
2. Show the first two and last five lines of the largest CSV
   (`head`, `tail`).
3. Count its lines (`wc -l`). Then verify your count a *second
   way* (e.g. `awk 'END{print NR}'`) — trust, but verify, is a
   Level-1 skill.

## Part 4 — Clean up like a professional (15 min)

1. Delete the `raw/` copies of files you moved (none should remain
   — prove with `find raw/ -type f | wc -l` → 0).
2. Use `rmdir` (not `rm -r`) on any now-empty directory. In
   `findings.md`: what does `rmdir` refuse to do, and why is that
   refusal a *feature*?
3. Final state proof: `tree ~/day1` (or `find ~/day1 -print`).

## Findings file

`findings.md` in `~/day1/notes/` — every part writes something into
it. Six entries minimum, each: **what you did → what you saw → one
sentence of why it matters**.

## Rubric (10 pts)

| Pts | Requirement |
|---|---|
| 2 | Part 1 facts + one-line "purpose" notes |
| 2 | Part 2 glob move + space-rename with correct quoting |
| 1 | Part 2 read-only experiment: error captured, restore shown |
| 2 | Part 3 double-count verification |
| 1 | Part 4 `rmdir` discipline |
| 1 | findings.md entries in the required shape |
| 1 | Transcript complete from before step 1 |
