# Lab 1 — Navigation Drills & Your Project Tree

> Lessons 1, 2, 4 · Time: ~45 min · Risk: zero — creates empty dirs/files only

## Goal

Make `pwd`/`ls`/`cd` reflexive, prove you can address any target three ways, and
build the course's standard project skeleton that M07+ will fill with real data.

## Part 1 — The relay (15 min)

Follow this `cd` relay *using Tab completion only* — no full path typing. Record
`pwd` after each hop.

```
Start: ~            (bare cd gets you here)
1. /usr/share/doc
2. /var/log
3. /etc
4. back to the previous directory   (which command?)
5. ~
6. /home
7. your home's parent               (relative spelling!)
8. ~
```

Checkpoint questions (log one line each):

- After step 7, which spelling did you use — and what does it resolve to?
- What does `cd -` do *right now*? Verify.

## Part 2 — Three addresses for one target (10 min)

Target: `/var/log` (readable? try `ls /var/log | head -3`).

From your home directory, reach it with:

1. an absolute path,
2. a tilde-relative path is *impossible* here — write down why in one sentence
   (hint: tilde means *your home*),
3. a relative path from `/usr` (i.e., `cd /usr` first, then `cd` to /var/log
   relatively — what's the spelling?).

## Part 3 — Build the course skeleton (15 min)

One command, then verify:

```console
$ mkdir -p ~/projects/eds-01/{data/{raw,processed},logs,notebooks,experiments}
$ tree ~/projects/eds-01
```

Then the touch pass:

```console
$ touch ~/projects/eds-01/README.md ~/projects/eds-01/data/raw/.keepme
$ ls -a ~/projects/eds-01/data/raw
```

(Why `.keepme`? Git and some tools skip empty dirs; a hidden placeholder is the
common idiom — M26 will use it in earnest.)

Record the `tree` output in `lab-log.md`. This tree is referenced by M07–M09
labs; keep it.

## Part 4 — Drill: error reading (10 min)

Run each, read the error, log *what it tells you* before fixing:

```console
$ cd /etc/Host
$ cd ~/projects/eds-01/data/Raw
$ ls ~/data/Raw
```

For each: was it case, spelling, or a missing parent? Fix by Tab completion
(no retyping from memory).

## Wrap-up checklist

- [ ] Relay completed with Tab only; `pwd` trail recorded
- [ ] Three-address exercise logged with the impossibility argued
- [ ] `~/projects/eds-01` skeleton exists; `tree` output in log
- [ ] All three Part-4 errors explained by cause, not by guessing
- [ ] `cd -` used at least three times during the lab
