# Lesson 2 — Branching and Merging

> Module 26 · Unit 7 · Difficulty: Intermediate
> Reading time: ~30 min · Lab: [Lab 1](../labs/lab-01-version-your-work.md) (Part C), [Lab 2](../labs/lab-02-break-repair-clinic.md)
> Up next: [Lesson 3 — Remotes, .gitignore and authentication](03-remotes-gitignore-auth.md)

---

## 1. A branch is a pointer, not a copy

The fear every beginner has: *"if I branch, won't it copy all my files?"*
No. From Lesson 1 you know a commit is an immutable snapshot chained to its
parent. A **branch is just a movable pointer to one commit** — stored as a
41-byte file in `.git/refs/heads/`. Creating one writes that one file:

```console
$ git branch experiment
$ ls .git/refs/heads/
experiment  main
$ cat .git/refs/heads/experiment
a1b2c3d4e5f6...        # same hash main points at — one line, zero copies
```

**HEAD** is the pointer that says which branch you're *on*; `git checkout`
(or the modern `git switch`) moves HEAD. "Checking out a branch" = "pointing
HEAD at that branch's commit and populating the working tree from its
snapshot" — files appear to change, but Git is simply materializing the
snapshot you asked for.

Why this matters practically: branching is **free**, so the correct response
to "should I branch for this?" is almost always yes. Experiments that might
break things, new analysis directions, dependency upgrades — all of them
happen on branches, keeping `main` perpetually in a known-good state. The
DS habit worth building now: `main` always runs; experiments are cheap and
disposable.

```console
$ git switch -c experiment        # create (-c) and switch in one step
Switched to a new branch 'experiment'
$ git switch main                 # back — files revert to main's snapshot
$ git branch                      # * marks where HEAD is
  experiment
* main
```

## 2. Two lines of work, side by side

Branches only earn their keep when they *diverge*. Concrete scenario, typed
rather than imagined:

```console
$ git switch -c add-outliers          # branch off main
$ echo "winsorize outliers" >> pipeline.txt && git add pipeline.txt
$ git commit -m "Add winsorization step"
$ git switch main
$ echo "fix column dtype" >> pipeline.txt && git add pipeline.txt
$ git commit -m "Fix revenue dtype to int64"
```

Now `main` and `add-outliers` each have one commit the other lacks — the
graph has forked:

```text
      C1 ── C2 (main: dtype fix)
         └── C3 (add-outliers: winsorize)
```

`git log --oneline --graph --all` draws exactly this. Each branch can
commit, test, and even break independently; nothing you do on
`add-outliers` touches `main` until you *merge*.

## 3. Merging: two ways to come together

`git merge <branch>` integrates `<branch>` into your **current** branch.
Two outcomes, depending on whether main moved:

**Fast-forward** — main hasn't moved since the branch. Git just slides the
`main` pointer forward; no new commit, no merge machinery:

```text
      C1 ── C2 ── C3 (add-outliers)
            ▲
            main        →  merge  →  C1 ── C2 ── C3 (main, add-outliers)
```

**Three-way merge** — both branches advanced (the scenario above). Git
computes a *merge commit* with **two parents**, combining both lines using
their common ancestor as the base:

```text
      C1 ── C2 ────── C4 (main: merge commit, parents C2 & C3)
         └── C3 ──────┘
```

The two-parent commit is Git's proof that *both* histories are preserved —
this is why you never lose work in a proper merge. Watch which one you got:
`git log --oneline --graph` shows the diamond for three-way, a straight
line for fast-forward.

> 💡 `git merge --no-ff <branch>` forces a merge commit even when a
> fast-forward is possible — useful when you want the merge itself
> (the moment a feature landed) visible in history. Teams codify this
> choice in policy; solo, either is fine.

## 4. Conflicts: normal, mechanical, survivable

A conflict happens only when **both branches modified the same lines**
(chaotic-neutral alternative: both edited the same file on different lines
— Git merges that cleanly). Conflicts are not errors; they're Git being
honest that it can't read minds.

```console
$ git merge add-outliers
Auto-merging analysis.py
CONFLICT (content): Merge conflict in analysis.py
Automatic merge failed; fix conflicts and then commit the result.
$ git status            # "both modified" — the files needing your judgment
```

Open the conflicted file; Git has marked the battlefield:

```text
<<<<<<< HEAD
model = RandomForest(n_estimators=100)
=======
model = GradientBoosting(max_depth=3)
>>>>>>> add-outliers
```

Read it as HEAD's version vs the incoming branch's version. Resolution is a
human decision, executed in three steps:

1. **Edit** the file to the content you actually want — keeping one side,
   combining both, or writing something new. Delete all three marker lines.
2. **`git add analysis.py`** — marks the conflict resolved.
3. **`git commit`** — completes the merge (Git pre-fills the message).

Abort switch, for when you opened a conflict you're not ready to judge:
`git merge --abort` returns both branches to pre-merge state. Nothing is
lost; the conflict will wait for a calmer day.

The DS version of a conflict is usually real: two teammates tuned the same
hyperparameter differently. The marker syntax is Git's way of putting both
proposals on the table — the conversation happens in the file.

## 5. Merge vs rebase — one sentence, then a rule

`git rebase <branch>` replays your branch's commits *on top of* the target,
producing a linear history. It rewrites the commits you replay (new hashes),
which is why the course rule for your first year of Git is: **merge freely;
use rebase only on commits you haven't shared** — and when you meet shared
history rewriting, do it in Lab 2's disposable repo first. Linear history is
a preference, not a virtue; nobody ever lost data to a merge commit.

## 6. Deleting and renaming branches

```console
$ git branch -d add-outliers    # safe delete: refuses if unmerged work
$ git branch -D add-outliers    # force: work is genuinely abandoned
```

`-d` (lowercase) is the everyday tool — it's a seatbelt, checking that the
branch's commits are reachable from somewhere else. After a merge, `-d`
works fine. Merged branches delete cleanly because their commits live on in
main's history — the pointer was the only thing being removed.

---

## Key takeaways

- A **branch is a pointer** — creation is one file write; branching is free,
  so branch for every experiment.
- **Fast-forward** = pointer slide; **three-way** = two-parent merge commit
  preserving both histories.
- Conflicts mean *same lines, two versions* — resolve by editing, `add`,
  `commit`; `--abort` is always available.
- Rebase rewrites history: shared commits stay merged until you're ready.

## Check yourself

1. Why is creating a branch instant, even in a repo with years of history?
2. What does a merge commit's *second parent* record?
3. Both branches edited the same file, different regions. Conflict or
   clean merge?
4. You ran a merge, hit a conflict, and need lunch. What command, and
   what state do you return to?

*Answers:* (1) it writes one 41-byte ref file; no data is copied. (2) the
other branch's tip — the commit whose work is being joined in. (3) clean
merge — Git merges hunks that don't overlap; only identical-line-region
edits conflict. (4) `git merge --abort`; both branches back to their exact
pre-merge states, conflict unresolved and waiting.

Up next: [Lesson 3 — Remotes, .gitignore and authentication](03-remotes-gitignore-auth.md) —
taking your history to a server and keeping junk out of it.
