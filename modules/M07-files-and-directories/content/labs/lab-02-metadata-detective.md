# Lab 2 — Metadata Detective

> Lessons 2, 4 · Time: ~45 min · Risk: zero (read-only + links built in your own
> scratch tree)

## Goal

Prove the inode model with your own experiments, and build the *inspection
first-minute* reflex for any new dataset.

## Part 1 — Type vs name (10 min)

```console
$ mkdir -p ~/scratch/detective && cd ~/scratch/detective
$ cp /etc/os-release fake.csv
$ file /etc/os-release fake.csv
```

Now the two-way test:

```console
$ mv fake.csv real.csv       # rename it back to a lie... or a truth?
$ file real.csv
```

Log: what does `file` key on — the name or the bytes? Then the empty case:
`touch empty.bin` → `file empty.bin` — quote the exact wording and explain it.

## Part 2 — The mtime/atime pair (10 min)

```console
$ stat -c '%x | %y | %z' real.csv
$ cat real.csv > /dev/null          # read it (output discarded harmlessly)
$ stat -c '%x | %y | %z' real.csv
```

Which of the three timestamps moved? (`%x` atime, `%y` mtime, `%z` ctime.)
Then `touch real.csv` and re-stat — which moved now? Write the three-timestamp
glossary in your log: access / modify / change, one line each. (Yes, *ctime is
"change", not "creation"* — `stat`'s birth line covers creation; the naming
confuses everyone once.)

## Part 3 — The inode twins (15 min)

```console
$ echo "v1" > original.txt
$ ln original.txt hardlink.txt
$ ln -s original.txt symlink.txt
$ ls -li
```

Record: inode numbers of `original` and `hardlink` (identical? must be), the
link count (3 names? check the count line's arithmetic: original + hardlink +
...wait — does the symlink count? **Why not?**), and the `l` type on the symlink.

Experiments, each logged:

1. `echo v2 >> hardlink.txt` → `cat original.txt` (sees it? why?)
2. `rm original.txt` → `cat hardlink.txt` (works? link count now?)
3. `cat symlink.txt` → still works (why? it pointed at original.txt!)
   Then `ls -l symlink.txt` — what color/state does a *dangling* link show?
4. Rebuild: `echo v1 > original.txt && ln -sf original.txt symlink.txt` —
   verify all three names serve the same content again.

## Part 4 — The latest-pointer pattern (10 min)

Build it as M19's cron jobs will use it:

```console
$ mkdir -p runs/{2026-09-14,2026-09-15} runs/current-test
$ ln -sfn runs/2026-09-15 runs/current
$ ls -l runs/ | grep current
$ ln -sfn runs/2026-09-14 runs/current        # flip to yesterday's run
$ ls -l runs/ | grep current
```

Now the matryoshka trap, on purpose:

```console
$ ln -s runs/2026-09-15 runs/current-test     # no -n, target is a dir
$ ln -s runs/2026-09-15 runs/current-test     # again!
$ ls -l runs/current-test                     # read the arrow carefully
```

Explain what the second `-s` without `-n` did *inside* the first link. Rebuild
`current-test` cleanly with `-sfn`.

## Wrap-up checklist

- [ ] Part 1: `file` beats names — demonstrated both directions
- [ ] Three timestamps glossary written; each experiment's before/after logged
- [ ] Inode twins: all four experiment results explained via the inode model
- [ ] `latest`-pointer built, flipped, and the matryoshka bug reproduced+explained
- [ ] `ls -li` output pasted once as evidence of same-inode twins
