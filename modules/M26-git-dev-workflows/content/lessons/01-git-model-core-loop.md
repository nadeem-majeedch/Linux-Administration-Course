# Lesson 1 — The Git Model and the Core Loop

> Module 26 · Unit 7 · Difficulty: Intermediate
> Reading time: ~30 min · Lab: [Lab 1](../labs/lab-01-version-your-work.md)
> Up next: [Lesson 2 — Branching and merging](02-branching-merging.md)

---

## 1. The problem Git solves

You already know the failure modes: `analysis_final.ipynb`,
`analysis_final_v2.ipynb`, `analysis_FINAL_v2_ACTUAL.ipynb`. Copy-of-a-copy
versioning loses three things no filename scheme can keep:

1. **History** — what changed, when, by whom, and *why* (the commit message).
2. **Integrity** — the ability to return to *any* previous state exactly, not
   approximately.
3. **Parallelism** — two lines of work at once without the copies colliding.

Git ([created by Linus Torvalds in 2005](https://git-scm.com/book/en/v2/Getting-Started-A-Short-History-of-Git)
for Linux kernel development) solves all three with one design decision that
surprises newcomers: **it doesn't store differences — it stores snapshots.**
Each commit records the complete state of every tracked file (with
unmodified files stored as a reference to the identical previous blob, which
is why repos don't bloat). History is therefore a graph of full states, not a
tape of patches — and almost every Git operation is a local graph walk. That
is why Git *feels* instant even on a laptop with no network: commits, logs,
branches, and diffs never leave your machine. The network appears only when
you explicitly sync with a remote (Lesson 3).

## 2. The three states (the model everything else hangs on)

Every file Git knows about lives in one of three places:

```
 working tree          index (staging area)         HEAD / repository
─────────────         ─────────────────────        ───────────────────
 your files as         what will be in the          the committed
 they are now    ──►   NEXT commit            ──►   history
   git add               git commit                 git checkout/reset
```

- **Working tree** — the files you actually see and edit.
- **Index** (staging area) — a deliberate, reviewed proposal for the next
  commit. You compose it with `git add`.
- **HEAD** — the latest commit of your current branch; the repository's
  committed history.

Every command you learn this module is just an arrow between states:

| Command | What it moves |
|---|---|
| `git add <file>` | working tree → index |
| `git commit` | index → HEAD |
| `git status` | shows the gaps between all three |
| `git checkout -- <file>` / `git restore <file>` | HEAD → working tree (discard edits) |
| `git log` / `git diff` | read-only views of history / of the gaps |

`git status` is the model made visible. Run it constantly — before anything
else, after everything else. It never changes anything; it only tells you
where your files sit among the three states.

## 3. First-time configuration

Git stamps every commit with your identity, so configure it once per machine
(stored in `~/.gitconfig` — a dotfile you now understand from M15):

```console
$ git config --global user.name "Ada Okoye"
$ git config --global user.email "ada@university.edu"
$ git config --global init.defaultBranch main
$ git config --global core.editor "nano"        # or vim/nano of your choice
$ git config --global --list
```

No `sudo` — this is user-level configuration in your home directory. The
`init.defaultBranch main` line only changes the *name* of the first branch;
you'll meet branch mechanics in Lesson 2.

## 4. The core loop, on a real repository

```console
$ mkdir -p ~/projects/git-lab && cd ~/projects/git-lab
$ git init
Initialized empty Git repository in /home/ds/projects/git-lab/.git/
$ git status
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

`git init` creates one thing: the hidden `.git/` directory — the entire
repository (history, index, configuration). Delete it and you have plain
files again; the *project* and the *repository* are separable, which is why
`.git/` itself never gets copied or committed anywhere.

Now the loop:

```console
$ echo "# Sales analysis" > README.md
$ git status                     # untracked file — Git sees it but tracks nothing yet
$ git add README.md              # working tree → index
$ git status                     # "changes to be committed" — the proposal is staged
$ git commit -m "Add README"
[main (root-commit) a1b2c3d] Add README
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
```

Then change the file and watch the vocabulary shift: the file moves from
*untracked* (first time) to *modified* (Git tracks it, edits are unstaged) to
*staged* (after `git add`) to *committed*. A **commit** needs a message; the
convention that survives every codebase: **subject line ≤ 50 chars, imperative
mood, blank line, then body explaining *why*** — "Add regional summary script"
beats "update".

Inspect history and the gaps:

```console
$ git log --oneline              # one line per commit
a1b2c3d (HEAD -> main) Add README
$ echo "pipeline notes" >> README.md
$ git diff                       # working tree vs index — your unstaged edits
$ git add README.md
$ git diff --staged              # index vs HEAD — the proposed commit
```

`git diff` with no arguments shows what you *haven't* staged;
`--staged` shows what you're *about to* commit. Reading both before every
commit is the review habit that keeps histories clean.

## 5. What a commit actually is

A commit is an immutable object containing: the full snapshot of tracked
files, the author/timestamp/message, and — the crucial part — the **hash of
its parent commit(s)**. History is therefore a chain (technically a
directed acyclic graph): each commit points backward. That single fact
explains half of Git's behavior:

- `a1b2c3d` in the output above is the **SHA-1 hash** — content-addressed:
  change one byte anywhere in the snapshot, get a different hash. Git's
  integrity check is cryptographic, not clerical.
- **HEAD** is just a pointer to the commit you have checked out; **a branch
  is just a pointer to a commit** (Lesson 2 exploits this ruthlessly).
- Nothing in `.git/` ever *changes* after it's written — commits can only be
  *added*, which is why "recovering" an old state is cheap and "losing"
  history takes deliberate effort (`git reflog` exists because even
  seemingly-lost commits linger).

**DS framing:** a commit of `analysis.py` plus its `requirements.txt` is a
*reproducibility checkpoint* — code, dependency pins, and (via the message)
context frozen together. That trio, not the notebook alone, is what makes a
result re-runnable by your supervisor in six months.

## 6. Commands you'll use every hour

| Command | Does | Notes |
|---|---|---|
| `git status` | where are my files? | run it compulsively |
| `git add <file>` | stage | stage by name; `git add -p` stages *hunks* interactively |
| `git commit -m "…"` | commit the index | message explains *why* |
| `git log --oneline --graph` | compact history | add `--all` to see branches |
| `git diff` / `--staged` | unstaged / staged changes | read before committing |
| `git show <hash>` | one commit in full | the audit tool |
| `git restore <file>` | discard working-tree edits | destructive: throws away edits — see the warning |
| `git rm <file>` | untrack *and* delete | plain `rm` leaves the file in the index |

> ⚠️ **Destructive-command note.** `git restore` discards *uncommitted*
> edits — unrecoverable, because the index never saw them. The course rule:
> commit early, commit small. Small commits make every recovery trivial and
> every mistake small. There is no prize for a beautiful history built on
> fear of committing.

## 7. The commit-message habit

Data-science histories die of "updates". Fix it with one discipline —
messages answer *why*, bodies carry *what*:

```text
Add region grouping to revenue summary

Group-by region before aggregation so per-region margins are
comparable; requested by Dr. Okoye for the Q3 review.
```

Six months later, that body is the only record of *why* the grouping
changed. `git log` on a repo with such messages is documentation; on a repo
of "fix", it's archaeology.

---

## Key takeaways

- Git stores **snapshots**, not diffs — history is a graph of full states,
  which is why everything is local and fast.
- Three states: **working tree → index → HEAD**; every command is an arrow.
- A commit is an immutable, hash-chained snapshot; **branches and HEAD are
  pointers**, not folders.
- Commit early and small; write messages that explain *why*.

## Check yourself

1. You edited a file, ran `git add`, then edited it *again*. What does
   `git commit` capture — and where does the second edit live?
2. Why does `git log` work with no network connection?
3. What exactly does `git init` create, and what happens to your files if
   you delete it?
4. Which command shows the changes you're *about to* commit?

*Answers:* (1) the staged version; the second edit remains unstaged in the
working tree — `git status` shows it as "changes not staged". (2) history is
a local graph in `.git/`; no network involved until you sync a remote.
(3) the `.git/` directory; your files remain but are no longer a repository —
no history, no index. (4) `git diff --staged`.

Up next: [Lesson 2 — Branching and merging](02-branching-merging.md) —
pointers, parallel worlds, and the art of putting them back together.
