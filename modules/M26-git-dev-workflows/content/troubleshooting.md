# Module 26 Troubleshooting — Git Symptoms → Causes → Fixes

> Ten patterns, ordered by how often they hit real students. Each:
> **symptom → cause → diagnosis → fix → prevention**. Git's saving
> grace: *anything committed is almost certainly recoverable* — the
> dangerous zone is only the never-added working tree.

## 1. `fatal: not a git repository (or any of the parent directories)`

**Cause:** you're not inside a repo — most often you're in a *parent*
or *sibling* directory of it, or you cloned to a different path than
you `cd`'d to.

**Diagnosis:** `pwd` and `ls -a` — no `.git/` here means no repo here.
`git rev-parse --show-toplevel` shows where Git thinks the repo root
is (errors out if nowhere).

**Fix:** `cd` into the actual repo directory, or `git init`/`git clone`
if you meant to create one.

**Prevention:** the habit from M06 — know your path; `ls -a` before
mystery-debugging.

## 2. `error: failed to push some refs ... (fetch first)`

**Cause:** the remote has commits your local doesn't — someone (or
you, from another clone) pushed first.

**Diagnosis:** `git fetch origin` then `git log HEAD..origin/main
--oneline` — see exactly what you're missing.

**Fix:** `git pull origin main` (resolve conflicts if they arise,
Lesson 2 §4), then `git push origin main`.

**Prevention:** pull before you start and before you push (Lesson 3
§4). Never "fix" this with `--force` — that erases the teammate's
commits from the shared branch.

## 3. Merge conflict markers look like garbage (`<<<<<<< HEAD`)

**Cause:** not garbage — *the merge paused for you*. Both branches
edited the same lines; Git wrote both versions into the file between
markers and stopped.

**Diagnosis:** `git status` lists "both modified" files. The markers
are in the working tree only — the repo is mid-merge.

**Fix:** edit each conflicted file to the content you want (delete all
three marker lines), `git add <file>`, `git commit`. Escape hatch:
`git merge --abort` restores the pre-merge state cleanly.

**Prevention:** pull early and often so divergences stay small; commit
small so conflicts touch few lines.

## 4. `detached HEAD` after `git checkout <hash or tag>`

**Cause:** you checked out a *commit*, not a branch — HEAD now points
at history rather than a ref. Normal and read-only *until you commit*.

**Diagnosis:** `git status` says it in so many words; `git branch`
shows no `*` marker next to any branch.

**Fix:** just looking? `git switch main` to return. Made commits
already? Rescue before switching: `git switch -c kept-work` (branches
from where you are — commits become reachable).

**Prevention:** visit the past with `git switch -c visit-<topic>`
from the start; detached inspection is for reading, not building.

## 5. "I committed to the wrong branch"

**Cause:** HEAD was on `main` when you meant to be on a feature branch.

**Diagnosis:** `git log --oneline -3` — your commit is on top of the
wrong branch's tip.

**Fix:** if not pushed: `git switch -c right-branch` (carries the
commit), then `git switch main && git reset --hard HEAD~1` to rewind
main. If already pushed to shared main: *don't rewind* — `git revert
<hash>` creates an undo commit, which is the shared-history-safe
cancel.

**Prevention:** `git status` shows the branch in its first line — read
it before committing. (The two-command fix is also why "commit early,
commit small" pays: rewinding one small commit disturbs nothing.)

## 6. Committed a secret (`.env`, key, token)

**Cause:** it was present during `git add -A` before `.gitignore`
existed — the exact ordering mistake Lesson 3 §2 warns about.

**Diagnosis:** `git log --all -p -- .env` — see every commit that
touched it.

**Fix:** treat the secret as **burned first** — rotate/revoke it
before touching history (M25 §5; the commit message and any clone may
already carry it). Then stop future tracking: `git rm --cached .env`,
add to `.gitignore`, commit, push. *If* the repo is private and young
and you coordinate with every cloner, history rewrite
(`git filter-repo`) plus force-push is the thorough option — with the
re-clone-everyone cost, and rotation is still mandatory.

**Prevention:** `.gitignore` before the first `git add`; `git status`
review before every commit; secrets in `.env` files that are ignored
from birth.

## 7. `warning: adding embedded git repository: ...`

**Cause:** you `git add`ed a directory that is itself a repo (it has
its own `.git/`) — Git records it as a *gitlink* (submodule-shaped
pointer) instead of copying its files.

**Diagnosis:** `git ls-files -s | grep ^160000` — mode 160000 entries
are gitlinks; `git status` shows them oddly, and clones get an empty
directory.

**Fix:** undo the add (`git rm --cached <dir>`), decide what you
meant: vendoring the code → remove the nested `.git/` and re-add;
true dependency → learn submodules deliberately, don't fall into them.

**Prevention:** clone *into* sibling directories, not inside the repo;
`ls -a` anything you're about to add wholesale.

## 8. `error: Your local changes ... would be overwritten` on switch/pull

**Cause:** Git refuses to lose data: the checkout/merge would clobber
edits you haven't committed.

**Diagnosis:** `git status` and `git diff` — see what's uncommitted
and whether you want it.

**Fix:** three honest options: commit it (`git add` + `commit`),
stash it temporarily (`git stash`, later `git stash pop`), or discard
deliberately (`git restore <file>` — destructive, only if truly
unwanted).

**Prevention:** finish-or-commit before switching contexts; the
working tree is not a filing cabinet.

## 9. Large repo, slow clone, history full of binaries

**Cause:** datasets, model files, and notebooks with embedded outputs
committed over months — history carries every version of every binary
forever.

**Diagnosis:** `git count-objects -vH` (repo size), and
`git rev-list --objects --all | sort -k2 | uniq -f1 -d` style hunting
or `git log --stat` for the biggest offenders.

**Fix:** going forward — ignore the categories (Lesson 3 §2), move
artifacts to object storage with hashes recorded in a manifest,
clear notebook outputs before committing. Existing history: same
rewrite caveat as pattern 6 (coordination required, clones invalidated).

**Prevention:** this is precisely why `.gitignore` is written *first*
in the end-to-end lab — prevention costs one file, cure costs a team
re-clone.

## 10. `Permission denied (publickey)` on push/clone-over-SSH

**Cause:** the server doesn't recognize your key — agent not running,
key not loaded, wrong key offered, or your public key never made it
into the server's `authorized_keys`.

**Diagnosis:** `ssh -T git@<host>` reproduces it outside Git (narrowing
to SSH itself); `ssh-add -l` shows loaded keys; `ssh -v git@<host>
2>&1 | grep -i offering` shows which keys were tried.

**Fix:** load your key (`ssh-add ~/.ssh/id_ed25519`), verify the
public half is registered server-side (M22 §1), retry. Multi-key
machines: `~/.ssh/config` `IdentityFile` per host (M22 §2).

**Prevention:** one key test (`ssh -T`) right after any key or config
change — before Git is in the loop.

## Escalation table

| Layer | Evidence command | Hands off / escalate when |
|---|---|---|
| Location | `pwd`, `git rev-parse --show-toplevel` | Repo ownership unclear — ask, don't init over it |
| States | `git status`, `git diff [--staged]` | Uncommitted work you didn't author — don't discard |
| History | `git log --graph --oneline --all`, `git show`, `git reflog` | Shared history rewrites — coordinate or don't |
| Remotes | `git fetch`, `git log HEAD..origin/main` | Force-push requests on shared branches — refuse, escalate |
| SSH | `ssh -T git@host`, `ssh-add -l`, `ssh -v` | Key material management — M25 §5 rules |
| Repo size | `git count-objects -vH` | History rewrites — team coordination required |

Related modules: [M22](../../M22-ssh-remote-admin/content/troubleshooting.md)
(SSH layer), [M25](../../M25-security-firewall/content/troubleshooting.md)
(secrets), [M27](../../M27-python-jupyter-data/content/troubleshooting.md)
(the environment half of the repo).
