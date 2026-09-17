# Lab 2 — The Break/Repair Clinic: Remotes and Recovery

> Module 26 · Unit 7 · Difficulty: Intermediate
> Time: ~60 min · Environment: your own VM
> Prerequisites: [Lesson 3](../lessons/03-remotes-gitignore-auth.md); Lab 1 complete
> ⚠️ First half of this lab builds a **disposable** repo (`~/projects/git-clinic`)
> whose entire purpose is to be broken. Recoveries that would be reckless in
> a real project are the *curriculum* here. The second half (remote sync)
> runs on the Lab 1 repo you want to keep.

Part 1 syncs a repo with a local bare remote — the no-network "Git server".
Part 2 hands you five real failure scenarios with symptoms only; you
diagnose from evidence before repairing. The reflexes built here are why
Git stops being scary: *nothing in a commit is ever truly lost*.

## Part A — the remote loop (15 min)

```console
$ git init --bare ~/repos/git-clinic.git      # the "server"
$ git clone ~/repos/git-clinic.git ~/projects/git-clinic
warning: You appear to have cloned an empty repository.   # expected
$ cd ~/projects/git-clinic
$ echo "work" > file.txt && git add file.txt && git commit -m "First"
$ git push origin main                        # ← clone pre-wired 'origin'
$ git log origin/main --oneline               # remote's state, visible locally
```

Then the two-user dance, from two clones (your stand-in for two
researchers):

```console
$ git clone ~/repos/git-clinic.git ~/projects/git-clinic-b
$ cd ~/projects/git-clinic-b
$ echo "teammate work" >> file.txt && git add -A && git commit -m "Teammate change"
$ git push origin main                        # teammate lands first
$ cd ~/projects/git-clinic
$ echo "my work" >> file.txt && git add -A && git commit -m "My change"
$ git push origin main                        # REJECTED — fetch first
$ git pull origin main                        # integrate, then…
$ git push origin main                        # …accepted
```

Read the pull's output: it performed a *merge* (or fast-forward) — Lesson 2
mechanics on the network stage. This reject→pull→push triple is the single
most common remote situation in existence; experience it here, smile at it
later.

## Part B — the clinic (35 min)

Five patients. For **each**: diagnose from evidence (write what you ran and
what it said), repair, verify. Solution sketches are at the bottom — no
peeking until you've committed to a diagnosis.

**Patient 1 — the vanished commit.** Your teammate (clone B) committed the
winsorization step, pushed, then *their* repo did
`git reset --hard HEAD~1` before pulling. Their working copy is missing the
work. Is it gone? Find it with `git reflog`, restore it onto a branch
(`git switch -c recovered <hash>`), and `git push origin recovered`.

**Patient 2 — the accidental commit.** Clone A: you committed
`credentials.env` (fabricated content: `API_KEY=pretend`) and pushed. You
cannot rewrite the remote's history (rule: never force-push shared main) —
so: remove it from tracking going forward (`git rm --cached`,
`.gitignore` entry, commit, push), then **rotate the credential** (delete
the file's key entirely — the committed copy must be treated as burned;
M25 §5). Write the two-line incident note you'd send your PI.

**Patient 3 — the merge with a conflict.** Engineer divergent edits to the
same line of `file.txt` from both clones (clone B: `version = 2`, clone A:
`version = 3`, both commit & push, A pulls). Resolve the conflict *as you
judge it*, `add`, `commit`, push. Record the three marker lines verbatim
in your log — recognizing markers on sight is half the skill.

**Patient 4 — detached HEAD panic.** In clone A: `git checkout
HEAD~2` (read-only visit to the past — Lesson 1 §5). Now `git status`
says HEAD is detached, and a naive `git commit` here orphans the commit.
Experience it: commit, note the warning, then rescue the commit the same
way as Patient 1 (branch from its hash). Then return properly:
`git switch main`.

**Patient 5 — the deleted branch.** Clone B creates `hotfix` with a
commit, pushes, then someone runs `git branch -D hotfix` *after switching
away* (unmerged → force delete needed). Recover: the hash is in the
pushed remote's ref or your `reflog` — `git switch -c hotfix2 <hash>`,
push. Then explain in one sentence why `-d` exists as the default.

**Solution sketches** (compare — don't grade yourself on identical
commands): 1) reflog is the safety net for *any* lost-pointer situation.
2) `--cached` untracks without deleting locally; rotation is mandatory
because history retains the secret. 3) edit → add → commit; markers are
`<<<<<<<`/`=======`/`>>>>>>>`. 4) detached HEAD commits are reachable only
by hash until branched. 5) `-D` skips the merged-check; reflog/remote refs
make it survivable anyway.

## Part C — the recovery mindset (5 min)

Write your `lab-log.md` coda: three sentences on what `git reflog` + the
immutability of commits (Lesson 1 §5) imply about when Git work is *ever*
unrecoverable. (Hint: only the never-committed working tree is
endangered — which is why Lab 1 ended with "commit early, commit small".)

## Done when

- [ ] Reject→pull→push transcript recorded from Part A
- [ ] All five patients: evidence, repair, verification in `lab-log.md`
- [ ] Patient 2's incident note written (untrack + rotate, never force-push)
- [ ] Part C coda: your recovery-mindset statement

Next: [Lab 3 — the end-to-end DS workflow](lab-03-end-to-end-ds-workflow.md),
where all of Unit 7 clicks together.
