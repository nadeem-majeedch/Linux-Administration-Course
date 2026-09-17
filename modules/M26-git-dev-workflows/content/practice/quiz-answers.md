# Module 26 Quiz — Answer Key

> Grading guide: Sections A–C are factual; D accepts any wording that
> shows the *judgment*. Command answers graded on "would it work if
> typed", not exact form.

## Section A — the model

**Q1.** A commit contains the complete snapshot of every tracked file
(unchanged files referenced back to identical prior blobs), plus
author/timestamp/message and the **parent commit's hash**. The parent
link is what turns isolated snapshots into a *graph*: it's how Git
knows the order of history, enables branches to diverge from a shared
past, and makes every commit auditable back to the root.

**Q2.** Working tree, index, HEAD. `git add` moves working tree →
index; `git commit` moves index → HEAD; `git restore <file>` (or
`git checkout -- <file>`) moves HEAD → working tree, discarding edits.

**Q3.** `git diff` compares working tree vs **index** (your not-yet-
staged edits). The other pair — index vs HEAD, i.e. what's *about to*
be committed — is `git diff --staged`.

**Q4.** History is a local graph of objects inside `.git/`; log,
diff, branch, and commit are all local operations. The network appears
only in remote syncs — `git push`, `git pull`/`fetch`, and `git clone`
(Lesson 3 §1).

**Q5.** A branch is a single 41-byte ref file holding one commit hash —
`.git/refs/heads/<name>`. `git switch` moves **HEAD** (the pointer to
your current branch) and materializes that branch's snapshot into the
working tree. No files are copied; pointers move.

**Q6.** Every object's name *is* its SHA-1 hash of its content —
content-addressed storage. If a file's bytes were altered anywhere in
history, its hash would change and no longer match the recorded tree.
Corruption detection is cryptographic by construction.

## Section B — branching & merging

**Q7.** Fast-forward: the target branch hasn't moved since the branch
point, so Git just slides the pointer forward — no new commit. Three-
way: both branches advanced, so Git computes a **merge commit with two
parents** — the second parent records the other branch's tip, i.e.
*whose* work is being joined. Both histories remain reachable; nothing
is discarded.

**Q8.** Clean merge. A conflict requires **the same lines** of the same
file modified in both branches (Git merges non-overlapping hunks
automatically). Different regions don't overlap, so Git combines them.

**Q9.** (1) Edit the conflicted file to the content you want, deleting
all `<<<<<<<`/`=======`/`>>>>>>>` markers; (2) `git add <file>` marks
it resolved; (3) `git commit` completes the merge. Back-out:
`git merge --abort` returns to the exact pre-merge state.

**Q10.** `-d` deletes only if the branch's commits are merged (reachable
elsewhere); `-D` deletes unconditionally. Lowercase is the seatbelt —
it refuses to orphan unmerged work, which is exactly the mistake tired
humans make at 6 p.m. on a Friday.

**Q11.** Rebase replays your commits on top of the target branch,
creating **new commits with new hashes** — the originals are abandoned.
Safe rule: rebase only commits that have never been pushed/shared;
anything others may have based work on must stay merge-only. (Shared
rewrites are a coordinated team event, not a Tuesday fix.)

**Q12.** Detached HEAD — HEAD points at a commit rather than a branch.
A commit made here is reachable only by hash; a later `git switch main`
orphans it. Rescue: `git reflog` (or the printed hash) then
`git switch -c rescue <hash>`. The commit isn't lost — it's
unreferenced, and reflog remembers it.

## Section C — remotes, ignore, auth

**Q13.** A repo without a working tree — history and refs only. Servers
use bare repos because nobody edits "on the server": all changes arrive
via push. A working tree there would invite divergence between the
server's checkout and what's committed — bare removes the ambiguity.

**Q14.** The remote gained commits you don't have (someone pushed while
you worked). Sequence: `git pull origin main` (integrate; resolve any
conflict per Q9), then `git push origin main`. The rejection is Git
refusing to guess how two diverged histories combine.

**Q15.** `.gitignore` affects only **untracked** files; the CSV is in
history, so it's ignored-but-tracked — every clone still downloads 2 GB
forever. Options: (a) live with it — costly, permanent; (b) rewrite
history to excise it (`git filter-repo` et al.) — changes every commit
hash, requires all clones to re-clone, and is precisely the
force-push-class operation the course says never to do casually on
shared history. Prevention (ignore-first) was the cheap answer.

**Q16.** Environments (`.venv/`), raw datasets, derived
outputs/artifacts, secrets (`.env`, keys, tokens), and editor/OS
debris. For raw datasets: a **provenance note** (`data/README.md` —
source, date, license, collection method) belongs in the repo instead;
the data itself is re-obtainable by the documented path.

**Q17.** Both are sshd authenticating the same user against the same
`authorized_keys`. Git-over-SSH is an SSH session whose command is
restricted to Git's transport (`git-upload-pack`/`git-receive-pack`) —
same key, same daemon, different command.

**Q18.** SSH on machines holding your key (your VM, administered
servers): strongest credential, no per-push secret entry. HTTPS+token
on borrowed machines and CI: a token grants only repo access, is
revocable in seconds without touching key infrastructure, and doesn't
require installing your private key anywhere untrusted. Passwords in
URLs or scripts: never (M25 §5).

## Section D — workflow & synthesis

**Q19.** Example (subject imperative, ≤50 chars; body explains why):

```text
Fix revenue dtype to int64 before aggregation

CSV parsing read revenue as strings, so monthly totals concatenated
instead of summing ("1200850"). Cast on load; verified against the
Q3 regional report.
```

**Q20.** Pull-early: starting work from everyone else's current state
means your branch diverges less — conflicts, when they come, are small
and fresh. Pull-before-push: the rejection means the remote moved while
you worked; integrating *before* pushing keeps shared history linear
and keeps the surprise in your hands rather than your teammates'.

**Q21.** "Binaries don't belong in Git — every retrain bloats every
future clone and diffs are meaningless. What *does* give
reproducibility: the training script, `requirements.txt`, the config
with all hyperparameters, the seed, and the provenance note for the
data — enough for anyone to re-derive the model; the artifact itself
lives in object storage with its hash recorded."

**Q22.** Explicit `git add outputs/summary.csv` **overrides** the
ignore rule (ignore rules apply to untracked adds like `git add -A`;
named adds are deliberate). Right decision: the summary is small, is
the analysis's citable result, and lets the fresh-clone verification
compare numbers without re-running anything. The PNG is regenerable by
re-running the committed notebook — derived, bulky, binary: history
doesn't need it.

Check understanding in practice: [challenges.md](challenges.md) ·
Symptoms: [../troubleshooting.md](../troubleshooting.md)
