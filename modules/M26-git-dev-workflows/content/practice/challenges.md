# Module 26 Challenges — Git and Development Workflows

> Eight challenges, C1 (drills) → C8 (design). All inside your own VM,
> all in disposable practice repos, evidence in `lab-log.md` per the
> course convention. No external hosting, no real credentials, no
> history rewriting on any repo you care about.

## C1 — Status reflex drill

One repo, ten minutes, no `git status` blindness. Perform this exact
sequence, writing *before each command* what you predict `git status`
will say, then compare: create file → edit → `add` → edit again →
`commit` → new file → `add` new file → `rm` old file (plain `rm`) →
`git add -A`. Deliverable: the ten predictions vs ten actuals, plus a
one-line note on every mismatch. (Bonus: what *extra* step does the
plain-`rm` state demand that students always miss?)

## C2 — Merge conflict speedrun

Two clones, one bare remote (Lab 2 §A setup). Engineer a conflict on
purpose: both sides change the same line of `config.txt` to different
values. Resolve three times — keep left, keep right, blend both — and
push each resolution as its own commit. Deliverable: the three marker
blocks pasted, plus one paragraph on which resolution you'd *argue for*
in a real review and why.

## C3 — The reflog rescue

In a disposable repo: make 3 commits, note the tip hash, then do
`git reset --hard HEAD~2`. The two commits are now unreachable by
branch. Recover them: `git reflog` to find the hash, `git switch -c
restored <hash>`. Deliverable: before/after `git log --oneline` of the
branch, plus one sentence answering: *what is the only Git state that
reflog cannot save?* (Hint: it never got added.)

## C4 — `.gitignore` gauntlet

Build a repo containing: `analysis.py`, `.venv/` (with a dummy file
inside), `data/raw/big.csv`, `outputs/result.png`, `.env`
(`FAKE_TOKEN=xyz`), `notes.md`. Write a `.gitignore` such that
`git add -A` stages **exactly** `analysis.py` and `notes.md` — verify
with `git status` and `git status --ignored`. Then prove the override
rule: `git add -f .env` stages it, `git restore --staged .env` un-stages
it. Deliverable: the `.gitignore`, both status outputs, and one line on
why `-f` existing at all is a footgun worth knowing about.

## C5 — Branching architecture

From a fresh repo with one commit, build this history exactly:

```text
main:     A ── B ────── F (merge, two parents)
                    ── E
branch-1:    └─ C ─ D ─┘   (merged into F)
branch-2:    └─ G          (never merged)
```

Any file content works; the *shape* is the deliverable. Then: `git
log --oneline --graph --all` proving the shape, `git branch -d
branch-1` succeeding, and `git branch -d branch-2` **failing** — explain
the refusal in one sentence. Bonus: what one flag makes `log` show G
still?

## C6 — Remote protocols

Point one practice repo's `origin` at a local bare repo **by absolute
path**, then (no network needed) read the difference: `git remote -v`
shows the path form. Add a *second* remote named `mirror` pointing at a
second bare repo, `git push mirror main`. Deliverable: proof both
remotes hold the same history (`git log mirror/main --oneline`) plus
one paragraph: in a real deployment, what would `mirror` correspond to
— and why do teams keep one? (Think backup and migration.)

## C7 — Commit archaeology

Create a repo with six commits across two branches, where one commit
*deliberately introduces a bug* into `calc.py` (e.g. changes `+` to
`-`). Then, playing detective with no prior knowledge: use `git log
--oneline`, `git log -p calc.py`, and `git show` to find **exactly
which commit** broke the file and what line changed. Deliverable: the
culprit hash, the `git show` excerpt, and the command sequence you'd
teach a teammate for future archaeology. (This is `git bisect`'s job
at scale — name it, look it up, one line on when it earns its keep.)

## C8 — Design: the research team's repo policy

No execution — a written policy. Five-person research group, shared
GitLab (bare repo pattern), one dataset directory, notebooks everywhere,
weekly model retrains. Write the one-page policy: default branch and
protection rules; feature-branch naming; commit-message convention; the
`.gitignore` (five categories minimum); what gets committed vs object
storage (models, datasets) and how provenance is recorded; the notebook
hygiene rule (outputs cleared); the "never force-push shared refs"
clause with its one sanctioned exception and its procedure. Deliverable:
the policy document + three risks you'd flag to the professor.

**Stretch** — personal Git cheatsheet: one page. Three states + the
commands between them; branch/merge/conflict trio; reject→pull→push;
reflog rescue; your five `.gitignore` categories. If it doesn't fit
one page, you don't know it yet.

---
*All challenges: own VM, disposable repos, evidence in `lab-log.md`.*
