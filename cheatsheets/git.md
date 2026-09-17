# 15 — Git

> Learn it: [M26 — Git & Development Workflows](../modules/M26-git-dev-workflows/content/README.md) ·
> Lookup, not understanding.

## First-time setup

```console
$ git config --global user.name "Ana Student"
$ git config --global user.email "ana@uni.edu"
$ git config --global init.defaultBranch main
```

## The core loop

| Command | Purpose | Notes |
|---|---|---|
| `git status` | **run this constantly** | the ground truth |
| `git init` | new repo here | `.git/` is created |
| `git clone URL` | copy a remote repo | also sets `origin` |
| `git add FILE` | stage | **explicit adds beat `add -A`** — you see what you're committing |
| `git add -p` | stage in hunk-sized pieces | the reviewed-commit habit |
| `git commit -m "msg"` | snapshot staged | present tense: "Fix column-count validation" |
| `git log --oneline` | history compactly | `--stat` adds changed files |
| `git diff` | unstaged changes | `--staged` for what you've staged |
| `git restore FILE` | discard working-tree changes ⚠️ | irreversible — status first |
| `git restore --staged FILE` | unstage (keeps changes) | undo of `add` |

## Branches

| Command | Purpose |
|---|---|
| `git branch` | list (`-a` all incl. remotes) |
| `git branch NAME` | create |
| `git switch NAME` / `git switch -c NAME` | change to / create-and-switch |
| `git merge NAME` | merge into current branch |
| `git branch -d NAME` | delete merged branch |

A branch is a **movable pointer** to a commit — branching copies
nothing. Conflicts: edit the marked file, `git add` it, `git
commit` — conflict resolution is just a commit you co-author.

## Remotes & sync

| Command | Purpose | Notes |
|---|---|---|
| `git remote -v` | list remotes | — |
| `git remote add origin URL` | attach a remote | — |
| `git push -u origin main` | upload + set upstream | first push tracks |
| `git pull` | fetch + merge | read the output — it's telling you what it did |
| `git fetch` | download **without** merging | look before integrating |

Authentication: HTTPS = token; SSH = your key (`git@…` URLs) —
course standard is SSH keys (see [ssh.md](ssh.md)).

## `.gitignore` — from the first commit

```text
.venv/            # environments are rebuilt, not committed
__pycache__/
*.pyc
data/             # datasets live by reference, checksums in README
models/           # binaries don't belong in history
secrets.env
*.pem
```
`.gitignore` protects *untracked* files. ⚠️ If a secret was already
committed, ignoring it does nothing: rotate the credential **first**,
then rewrite history (`git rm --cached secrets.env` +
`git filter-repo`), then push. Rotation before remediation — the
order that ends the argument.

## Inspecting & history surgery

| Command | Purpose |
|---|---|
| `git show COMMIT` | one commit's full diff |
| `git log --oneline --graph --all` | the branch picture |
| `git blame FILE` | who last touched each line |
| `git commit --amend` | fix the **last** commit (pre-push only) |
| `git revert COMMIT` | **safe undo**: new commit that inverts an old one |
| `git reset --soft HEAD~1` | uncommit, keep changes staged |
| `git reset --hard` | ⚠️ destroys changes — the last resort with a checked status |

## Workflows you'll meet

| Flow | Shape |
|---|---|
| feature branch | branch per task → PR → merge — the default in teams |
| trunk-based | short-lived branches straight to main |
| fork + PR | no write access: fork, push to fork, PR upstream |

## Hygiene rules that are graded rules

- Meaningful messages (`--stat` should be readable as a story).
- Commit increments, not day-end blobs.
- Never commit: venvs, datasets, model binaries, `secrets.env`,
  `.env` — `.gitignore` from commit one.
- `git status` clean before switching branches.
- ⚠️ No history rewriting on shared branches (`revert` exists for
  that).
