# Lab 1 — The Package Explorer (Read-Only)

> Module 16 · Unit 5 · Difficulty: Beginner
> Environment: your own VM/WSL2 · Time: ~30 min
> **Zero system changes** — every command below only *queries*. If a
> command in your transcript includes `install`, `remove`, `purge`, or
> `upgrade`, you've left the lab's safety envelope.

## Part A — the dpkg database

```console
$ dpkg -l | wc -l                          # how much software is on this machine?
$ dpkg -l | grep -v "^ii" | head           # anything NOT fully installed?
$ dpkg -l coreutils nano curl 2>/dev/null  # specific checks
```

**Record:** the total count; whether the second command shows anything
with a non-`ii` prefix and what that prefix means (Lesson 1 §2).

Reverse lookups — the superpower:

```console
$ dpkg -S /bin/ls
$ dpkg -S /usr/bin/python3
$ dpkg -L coreutils | wc -l
$ dpkg -L coreutils | grep "bin/" | head -8
```

**Record:** one sentence each: what `-S` and `-L` do, and two distinct
*kinds* of paths you saw in the `-L` list.

## Part B — the apt catalog (fresh lists first)

```console
$ sudo apt update          # the ONLY sudo in this lab: refreshes lists, installs nothing
$ apt search image resize | head -6
$ apt show imagemagick | grep -E "^(Package|Version|Depends|Installed-Size)"
$ apt policy imagemagick   # which source would serve it? what's installed?
```

**Record:** for imagemagick — version, dependency *count* (count the
comma-separated entries), installed size. Then the judgment call: is that
dependency weight acceptable for a machine whose job is data science?
Would `--no-install-recommends` change the bill (re-run `apt show` and
look for Recommends)?

## Part C — read the pending work

```console
$ apt list --upgradable 2>/dev/null | tail -n +2 | wc -l
$ apt list --upgradable 2>/dev/null | head -8
```

**Record:** the count (your machine's security debt) and — for any two
packages — a one-line guess of what they are, from the name alone. You'll
revisit this list in Lab 3.

## Part D — the dependency tree

Pick a small uninstalled package (suggest `jq` or `tree`):

```console
$ apt show tree | grep -E "Depends|Recommends|Suggests"
$ apt install --dry-run tree | head -12    # SIMULATION: changes nothing
```

`--dry-run` is the safe rehearsal of Lesson 1 §4's step 4 — the exact
summary line `apt install` would show, without acting.

**Record:** paste the dry-run's NEW-packages block. Compare against the
`Depends:` line — do they match? Why might the dry-run list *more* than
Depends (pre-depends, recommends)?

## Done when

- [ ] All four parts' recorded answers are in `lab-log.md`
- [ ] Transcript contains zero state-changing apt commands (grep your own
      history: `history | grep -E "apt (install|remove|purge|upgrade)"`)
- [ ] The `--dry-run` block is pasted and annotated
