# Module 07 Quiz — Answer Key

1. `-r` (recursive). Without `-i`, an existing DEST is **silently overwritten**.
2. `mv` rewrites a *name→inode* mapping in the directory table; no bytes are
   copied. (Across filesystems it *does* copy-then-delete.)
3. `pwd` (where am I) → `ls` the exact targets (see what I affect) → then run;
   verify with `ls` after.
4. Refusal: `rmdir: failed to remove ...: Directory not empty` — by design.
5. A *name* (directory entry). The link count decrements; data is freed only
   when the count reaches zero.
6. Real type — e.g. "CSV text" vs "data" or UTF-16/BOM detection — because
   pandas would otherwise mis-decode or fail on an assumption from the name.
7. atime (last read — "was it touched?"), mtime (last content change —
   sorting/backup decisions), birth/crtime (lineage). (ctime = metadata change
   — acceptable extra.)
8. mtime. `touch` updates mtime (and atime) without touching contents.
9. The link count (how many names point at that inode).
10. `app-2026-09-01.log app-current.log` (alphabetical; `*` matches both).
11. Feature: glob expansion skips leading-dot names, so casual globs can't eat
    your configs; `.*` reaches them deliberately.
12. The literal string `*.xlsx` — expansion failed, pattern passed through;
    `rm` errors "No such file or directory".
13. Double quotes (single quotes are fully literal).
14. `touch` → one file (quotes). `rm my file.txt` → two arguments → two errors
    (neither `my` nor `file.txt` exists); the real file survives.
15. `rm -- -r` (end-of-options) or `rm ./-r` (path prefix).
16. Appending via either name changes the shared data (same inode); deleting
    one name decrements the count — data intact until zero.
17. Survives deletion: **hard**. Crosses filesystems: **symlink**. Directories:
    **symlink only**.
18. With `-sfn`: replaced cleanly each time — still one link to 2026-09-15.
    Without `-n`: the second command creates a link *inside* the directory the
    first link points to (matryoshka).
19. A symlink is a tiny file whose *content is the target path* — its size is
    the path's length; the target's size belongs to the target's inode.
20. Hard links (same filesystem) — one 40 GB on disk, three views. Wrong
    choice (`cp` ×3): 120 GB and a full volume mid-training.
