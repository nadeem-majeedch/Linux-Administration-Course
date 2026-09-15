# Lab 2 — The Safe Lifecycle: Install → Verify → Remove

> Module 16 · Unit 5 · Difficulty: Beginner-Intermediate
> Environment: your own VM/WSL2 · Time: ~40 min
> Prerequisites: [Lab 1](lab-01-package-explorer.md)
> We install one tiny, boring, well-known tool (`tree`), learn what the
> system does at each beat, then remove every trace. Every state-changing
> command is previewed first.

## Part A — before: know the baseline

```console
$ dpkg -l tree || echo "not installed"     # baseline state
$ which tree || echo "not on PATH"
$ apt show tree | grep -E "Depends|Installed-Size"
```

**Record:** baseline — not installed (presumably), size, deps.

## Part B — the check-first install

```console
$ sudo apt update                          # fresh catalog
$ apt install --dry-run tree | tail -4     # rehearse: what exactly will change?
$ sudo apt install tree                    # read the summary line before Y
```

During the install, *watch the output*: the line
`Setting up tree (1.2.x ...)` is dpkg running the package's configure
step. **Record** the summary block verbatim.

## Part C — verify like a professional

```console
$ dpkg -l tree                             # ii now?
$ dpkg -L tree                             # every file it owns
$ dpkg -s tree | grep -E "Status|Version"
$ which tree && tree --version
```

Also inspect the *receipts*: `/var/lib/dpkg/info/tree.list` is the same
list dpkg stored (compare with `-L`), `/var/lib/dpkg/status` is the whole
database. **Record:** how many files did this tiny package install, and
in which four directory families (bin/man/share/doc) do they live —
connect each to [M06's FHS tour](../../../M06-filesystem-hierarchy/content/lessons/03-filesystem-hierarchy-tour.md).

## Part D — the removal spectrum

The three removal verbs, tested in order on the *same* package (we
reinstall between tests so each verb's behavior is visible):

```console
$ sudo apt remove tree                     # remove: config stays?
$ dpkg -l tree | tail -1                   # status: 'rc'? (removed, config-files remain)
$ ls /etc/tree* 2>/dev/null || echo "(no config to keep for tree — fine; learn the verbs, not this package)"
$ sudo apt install tree                    # reinstall — instant? why? (cache!)
$ sudo apt purge tree                      # purge: everything gone
$ dpkg -l tree || true                     # finally: gone from the database
```

Then the orphan sweep:

```console
$ sudo apt install --dry-run autoremove | tail -3   # preview what autoremove would remove
$ sudo apt autoremove                       # remove dependencies nothing else needs
```

**Record:** the three status codes you observed (`ii` → `rc` → absent)
and one sentence each on what remove/purge/autoremove are *for*. Why does
`apt install` after `apt remove` finish instantly (hint:
`/var/cache/apt/archives/`)?

## Part E — reflection

1. Which step, if skipped, most risks installing something you didn't
   intend — and what exactly did that step show you this time?
2. In one sentence each: why the course says *never* `sudo apt
   autoremove` blindly on a shared server (preview first), and why
   `--dry-run` is the cheapest insurance in this module.
3. `history | grep apt` — paste your lifecycle transcript. Annotate the
   one moment you were glad you previewed.

## Done when

- [ ] Baseline, install summary, and verify outputs recorded
- [ ] `ii` → `rc` → absent progression captured
- [ ] autoremove *previewed* before running
- [ ] Reflection written
- [ ] System end-state identical to start: `dpkg -l tree` says absent
