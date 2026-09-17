# M07 — Files, Directories & Text Files: content guide

> The operations module: create, copy, move, inspect, glob, link —
> and delete with a discipline that keeps you employed.

**Lessons**

| # | Lesson | You will be able to |
|---|--------|---------------------|
| 1 | [01-file-operations-cp-mv-rm.md](lessons/01-file-operations-cp-mv-rm.md) | Copy/move/remove with the safety protocols (`-i`, `-n`, `mv`-then-rm patterns) that make `rm` survivable |
| 2 | [02-inspecting-files-file-stat.md](lessons/02-inspecting-files-file-stat.md) | Identify what a file *is* (`file`) and read its full metadata (`stat`) before acting on it |
| 3 | [03-wildcards-globbing-quoting.md](lessons/03-wildcards-globbing-quoting.md) | Select file sets with globs and predict exactly what the shell expands — including the quoting that keeps it honest |
| 4 | [04-links-and-inodes.md](lessons/04-links-and-inodes.md) | Use symlinks vs hard links correctly and explain the inode model underneath |

**Labs** — [labs/README.md](labs/README.md): organizing datasets in
a sacrificial tree · metadata detective.

**Practice** — [practice/quiz.md](practice/quiz.md) (+ key),
[challenges.md](practice/challenges.md) (6 challenges).

## Learning objectives

By the end of this module you can:

1. **Operate** on files safely: `cp` (and `-a` for faithful copies),
   `mv` (rename *and* move, atomically within a filesystem), `rmdir`
   vs `rm -r`, with the confirmation habits that make destructive
   commands deliberate.
2. **Classify** files before acting: `file` for type, `stat` for the
   full metadata record (size, blocks, timestamps, inode, links).
3. **Predict** glob expansion: `*`, `?`, `[...]`, brace expansion —
   and the quoting/escaping rules (`"`, `'`, `\`) that decide what
   the shell sees vs what the command sees.
4. **Model** inodes: hard links as names-for-an-inode, symlinks as
   names-for-a-name, and the operational consequences (link counts,
   `rm` semantics, broken symlinks, directory hard-link ban).
5. **Manage** DS artifacts: datasets, experiment outputs, and logs —
   including timestamped names and safe archive/move patterns that
   M19's cleanup jobs and M26's backup discipline reuse.

## Command-line skills

`cp` (`-r -a -i -n -u`) · `mv` (`-i -n`) · `rm` (`-r -f -i` — and
when *never*) · `rmdir` · `mkdir -p` (from M06) · `file` · `stat` ·
`ls -li` (inode view) · `ln` / `ln -s` · `readlink -f` · globs and
brace expansion · quoting and escaping.

## Prerequisite map

M06 taught *where* files live; this module teaches *operations* on
them. Everything downstream consumes these: M08 reads them as
streams, M13 governs *who* may operate, M17 watches the space they
fill, M19 automates their lifecycle, M26 versions their *text*,
M31's data commons applies the link/permission model to shared
datasets.
