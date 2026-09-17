# Lab 1 — Version Your Work: A Real History, Built by Hand

> Module 26 · Unit 7 · Difficulty: Intermediate
> Time: ~45 min · Environment: your own VM
> Prerequisites: [Lesson 1](../lessons/01-git-model-core-loop.md), [Lesson 2](../lessons/02-branching-merging.md)
> ⚠️ Everything under `~/projects/git-lab`. Destructive commands are
> reserved for Lab 2's disposable repo — here you only *build*.

You will build a small analysis project with a genuine, well-messaged
commit history — then branch, diverge, and merge it back. The skill being
installed: the core loop as reflex, not recitation.

## Setup (3 min)

```console
$ mkdir -p ~/projects/git-lab && cd ~/projects/git-lab
$ git init
$ git status                  # expect: "No commits yet"
```

If `user.name` isn't configured, do it now (Lesson 1 §3) — commits will
fail without it.

## Part A — three commits, three stories (15 min)

Create `pipeline.sh` (you can write shell now — use it):

```bash
#!/usr/bin/env bash
set -euo pipefail
# Sum sales by region from the CSV named on the command line.
csv="${1:?usage: pipeline.sh <csv>}"
awk -F, 'NR>1 {s[$1]+=$2} END {for (r in s) printf "%s\t%d\n", r, s[r]}' "$csv"
```

Then stage and commit it *alone*:

```console
$ chmod +x pipeline.sh
$ git add pipeline.sh && git commit -m "Add regional revenue pipeline"
```

Now the data, the ignore rule, and a README — **three separate commits**,
each with a message explaining why:

```console
$ printf 'region,revenue\nnorth,1200\nsouth,850\nnorth,300\n' > sales.csv
$ printf '.venv/\noutputs/\n*.log\n.ipynb_checkpoints/\n' > .gitignore
$ echo "# Regional sales pipeline" > README.md
$ git add sales.csv     && git commit -m "Add sample dataset for pipeline testing"
$ git add .gitignore    && git commit -m "Ignore environments and derived outputs"
$ git add README.md     && git commit -m "Document purpose and usage"
```

Four commits, four reasons — run `git log --oneline` and read your own
history. This granularity is what makes `git show <hash>` a usable audit
tool later.

## Part B — watch the three states (10 min)

Deliberate choreography; record what `git status` says at each step:

```console
$ echo "# Regional sales pipeline (v2)" >> README.md   # modified, unstaged
$ git status && git diff                                # working tree vs index
$ git add README.md && git diff --staged                # index vs HEAD
$ git commit -m "Expand README with v2 notes"
```

**The checkpoint:** edit README again, `git add` it, then edit it *again*.
`git status` must show it in *both* sections ("to be committed" and "not
staged"). That's Lesson 1's Q1 made physical: the index holds one version,
the working tree another. Commit the staged version; confirm the second
edit survives in the working tree.

## Part C — branch, diverge, merge (15 min)

```console
$ git switch -c add-validation
$ cat >> pipeline.sh <<'EOF'

# Fail loudly if the CSV header is malformed.
validate() {
  head -1 "$csv" | grep -q '^region,revenue$' || { echo "bad header" >&2; exit 1; }
}
validate
EOF
$ sed -i 's/^awk/# validate first\nawk/' pipeline.sh   # call validate() before awk
$ git add pipeline.sh && git commit -m "Validate CSV header before processing"
$ git switch main
$ echo "# Regional sales pipeline (usage: pipeline.sh <csv>)" >> README.md
$ git add README.md && git commit -m "Document usage in README"
```

Two branches, both advanced. Predict the merge type (three-way — both
moved), then:

```console
$ git merge add-validation            # editor opens for the merge message
$ git log --oneline --graph --all     # the diamond: two parents
$ git branch -d add-validation        # merged → safe delete works
```

Run the pipeline end-to-end and the validation path too:

```console
$ ./pipeline.sh sales.csv
$ printf 'wrong,header\n' > bad.csv && ./pipeline.sh bad.csv; echo "exit: $?"
```

## Done when

- [ ] Five commits, each a separate story; `git log --oneline` pasted
- [ ] Part B's two-section `git status` recorded and explained in one line
- [ ] Merge commit visible in `--graph` output; branch deleted with `-d`
- [ ] Both pipeline runs recorded — including the non-zero exit on bad input
- [ ] One line per commit in your `lab-log.md`: why *that* commit exists
      separately

Up next: [Lab 2 — the break/repair clinic](lab-02-break-repair-clinic.md) —
now we break things on purpose.
