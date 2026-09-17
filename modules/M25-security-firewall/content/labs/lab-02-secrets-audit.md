# Lab 2 — The Secrets Audit: Find, Rotate, Verify

> Module 25 · Unit 6 · Difficulty: Intermediate
> Time: ~45 min · Environment: your own VM (git installed)
> Prerequisites: [Lesson 5](../lessons/05-secrets-credentials.md)
> ⚠️ Every credential in the seeded repo is **fabricated** for this
> lab. The skills — pattern search, history reasoning, the rotate-
> and-recover playbook — are the real deliverable. Nothing here
> touches external systems.

A teammate hands you their project repo and says, "I *think* I
committed a token once. Can you check?" — the most realistic
security request a DS person gets. Build the seeded repo, audit it,
then rehearse the response playbook end-to-end.

## Setup — seed the patient (10 min)

```console
$ mkdir -p ~/lab25/auditme && cd ~/lab25/auditme && git init -q
$ printf 'import os\ntoken = "kaggle_live_9f3Xb7Qm"\nprint("ok")\n' > fetch_data.py
$ printf 'DB_URL=postgres://ds:S3cr3tPw@10.0.2.15/dsdb\n' > .env
$ printf 'AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI\nendpoint=https://s3.example\n' > upload.cfg
$ printf '# project\nplaceholder: <YOUR_TOKEN>\n' > README.md
$ git add -A && git commit -qm "initial upload"      # everything, mistakes included
$ printf 'token = "kaggle_live_9f3Xb7Qm"\n' >> fetch_data.py   # (and a second copy)
$ git add -A && git commit -qm "tweaks"
$ git log --oneline                                   # two commits; the secrets are IN history
```

Record: which files *should* be secrets, and which commits hold
them — your prediction before the mechanical audit.

## Part 1 — the mechanical audit (10 min)

The Lesson 5 sweep, tuned:

```console
$ grep -rInE '(api[_-]?key|token|secret|password|passwd|pwd)["'"'"']?\s*[:=]' . \
    --include="*.py" --include="*.ipynb" --include="*.cfg" --include="*.md" \
  | grep -vE '<YOUR_|placeholder' | head -20
$ git log -p | grep -nE 'kaggle_live|S3cr3tPw|wJalr'     # the history view — where it really lives
```

The second command is the teaching moment: **history holds what
`rm` erased.** Even if your teammate "deleted the token file last
week", `git log -p` shows it at every commit that contained it.
Fill in the audit table: *secret / file / in which commits / live
or placeholder*.

## Part 2 — classify (5 min)

For each finding: **live credential** (revoke required),
**placeholder/false positive** (none), or **structural problem**
(a real secret's *shape* in a tracked file — the `.env` tracked at
all is the finding regardless of content). Real audits live or die
on this step: a hundred grep hits usually hide three real findings.

## Part 3 — the playbook, rehearsed (15 min)

Lesson 5 §5's four steps, executed on the fake secrets:

1. **Revoke** (simulated): write the *actual* provider action as a
   sentence — "rotate `kaggle_live_9f3Xb7Qm` at kaggle.com →
   settings → API tokens"; for the SSH-key class, name the exact
   `authorized_keys` line removal. Revocation is a sentence on
   paper because it's an *external* action — knowing it is the
   point.
2. **Purge current state:** remove the secrets from working files;
   move the real values into a git-ignored `.env` (600) +
   `os.environ` reads — the Lesson 5 §3 pattern, implemented:

   ```console
   $ printf '.env\n' > .gitignore
   $ chmod 600 .env
   $ git rm --cached .env 2>/dev/null; git add -A && git commit -qm "secrets to env"
   ```

3. **History:** reason before acting — with revocation done, is a
   history rewrite *urgent*? (No: the old tokens are dead.) Note
   the tools you *would* use (`git filter-repo` / BFG) and the
   caveat they share (history rewrite invalidates clones — a
   team-coordination event, never a solo emergency move).
4. **Postmortem:** five lines per M24's format — how it leaked
   (no .gitignore at init), why it could (secrets-in-code habit),
   the fix (env pattern), the prevention (`.env` ignored *before*
   it exists; pre-commit grep in CI).

## Part 4 — verify (5 min)

```console
$ git log -p | grep -cE 'kaggle_live|S3cr3tPw|wJalr'    # still in HISTORY (expected >0)
$ git status                                              # .env invisible (ignored)
$ grep -rInE 'kaggle_live|S3cr3tPw|wJalr' --exclude-dir=.git .   # working tree: clean
```

The three-line state that *should* bother you — history still
holds the dead tokens — is the lab's final lesson: hygiene prevents
the leak; revocation contains it; history rewrite (a team event)
erases it. Record which of the three you'd prioritize in a real
incident and why.

## Done when

- [ ] Audit table complete (secret / file / commits / class)
- [ ] The env-pattern fix implemented and verified (`.env` ignored,
      600, code reads `os.environ`)
- [ ] The revocation sentences written for each live secret
- [ ] The three-command verification pasted, with the history
      question answered
- [ ] The postmortem written (five lines, prevention included)
