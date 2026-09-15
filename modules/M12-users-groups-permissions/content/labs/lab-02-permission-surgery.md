# Lab 2 — Permission Surgery

> Lesson 2 · Time: ~50 min · Risk: low — operates only on files created inside
> this lab (`~/scratch/perm-lab`)

## Goal

Convert the rwx model into hands: symbolic and numeric `chmod` fluency, umask
computation, and the check-order stall demonstrated on your own filesystem.

## Part 1 — Build the surgery table (10 min)

```console
$ mkdir -p ~/scratch/perm-lab && cd ~/scratch/perm-lab
$ touch secret.env dataset.csv run.sh README.md
$ mkdir team-vault
$ ls -l
```

Target state (write the chmod for each *before* running):

| File | Target mode | Your command (symbolic *or* numeric) |
|---|---|---|
| `secret.env` | 600 | |
| `dataset.csv` | 664 | |
| `run.sh` | 750 | |
| `README.md` | 644 | |
| `team-vault/` | 750 | |

Execute, then `ls -l` to verify each landed. Any misses: re-read the mode and
retry — misses *are* the learning.

## Part 2 — Prove the verbs (15 min)

**Directory-w removes files you don't own:**

```console
$ sudo touch team-vault/rootfile        # root-owned file inside YOUR writable dir
$ rm team-vault/rootfile
rm: remove write-protected regular empty file 'team-vault/rootfile'? y
$ ls team-vault                         # it worked! whose permission decided this?
```

Log the answer via §1's table: `w` on the *directory* is the delete-decider —
the file's own mode barely mattered.

**Directory-x without r:**

```console
$ chmod 111 team-vault && ls team-vault          # denied: cannot list
$ cat team-vault/rootfile 2>/dev/null            # (recreate first if needed)
$ cd team-vault && pwd                           # traversal still allowed!
$ cd .. && chmod 750 team-vault
```

**The group-stall (check order):**

```console
$ sudo chgrp sudo dataset.csv     # put it in a group you're in
$ chmod 604 dataset.csv           # group gets NOTHING, others get read
$ cat dataset.csv                 # denied?! — §4's rule, demonstrated
$ chmod 640 dataset.csv           # fix via the group, the RIGHT way
```

Log each block with the *rule* that explains it, not just the result.

## Part 3 — umask arithmetic (10 min)

```console
$ umask                            # record the session default
$ (umask 077; touch priv.txt; mkdir privdir; ls -l priv.txt; ls -ld privdir)
$ touch after.txt                  # outside the subshell: default again?
```

Before looking, *compute* what 077 must yield for file (666−) and dir (777−).
Log prediction, then reality. Then the subshell lesson: `ls -l after.txt` —
why did the parentheses matter?

## Part 4 — Repair round (10 min)

Deliberately break, then fix by diagnosis only:

```console
$ chmod 000 secret.env
$ cat secret.env                    # error? record it
$ ls -l secret.env                  # diagnose from the mode line
$ chmod 600 secret.env              # repair; verify
```

Then without `-v` tools: can you *rename* a file you can't read? (`chmod 000
dataset.csv; mv dataset.csv dataset2.csv` — allowed?! Why, per directory-w?)
Restore everything to the Part-1 table's final state.

## Wrap-up checklist

- [ ] Part-1 table complete with commands *and* verified results
- [ ] All three proof-blocks logged with their governing rules
- [ ] umask 077 computed before observed
- [ ] Repair round: error → diagnosis → fix, all documented
- [ ] Final `ls -lR ~/scratch/perm-lab` pasted as the end-state receipt
