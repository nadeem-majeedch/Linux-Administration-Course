# Unit 4 Lecture Slides — System Administration (M12–M15)

> **Delivery:** Sessions 11–12 · Speaker notes:
> [../speaker-notes/unit-04-system-administration-notes.md](../speaker-notes/unit-04-system-administration-notes.md)

---

# Slide 1 — Title

## Slide Content
**Unit 4 — System Administration**
Users · Groups · Permissions · Shared access · sudo · Environment (M12–M15)
*From user of the machine → responsible for who-can-do-what*

## Instructor Delivery Notes
Framing: "Units 1–3 made you capable. This unit makes you
*accountable* — every command now has an identity attached."

## Visual or Demonstration Suggestion
`id` output projected — "this is who the machine thinks you are."

## Student Question
"Who is allowed to read your browsing history on a shared machine? What enforces that?"

---

# Slide 2 — Identity: users, UIDs, groups

## Slide Content
- Every process runs **as a user**; every file is **owned** by a user+group
- `id` → uid, gid, supplementary groups · `whoami` · `groups`
- Humans live in `/home`; **root (uid 0)** is the administrator — the exception to every rule
- System users (uid < 1000 on Debian/Ubuntu — a packaging convention, not kernel law) run services, not people

## Instructor Delivery Notes
Run `id` live; decode every field. The root-is-not-a-user point matters:
it's a *role with a number*. uid<1000 systems-users pays off in M20.

## Visual or Demonstration Suggestion
`cat /etc/passwd | tail -5` — identify the system users in the list.

## Student Question
"Why does PostgreSQL get its own user account?"

---

# Slide 3 — The permission triplet

## Slide Content
```
-rw-r----- 1 dsstudent research 10485760 Mar 3 09:14 sales.csv
 │  │  └── other:  r--      (read only)
 │  └───── group:  r--      (research team)
 └──────── owner:  rw-      (dsstudent)
```
- Files: `r` read, `w` write, `x` execute
- **Directories**: `r` list names · `w` create/delete entries · `x` *enter & reach*
- The `x`-on-directory surprise: without it, `r` shows names but nothing opens

## Instructor Delivery Notes
Decode the string interactively, one triplet per volunteer. The
directory-x idea is the unit's classic wall — the M12 quiz drills it;
preview that now.

## Visual or Demonstration Suggestion
Live: `chmod 600` vs `chmod 000` on a *directory* — list fails at a different point than open fails.

## Student Question
"Mode `--x` on a directory: what can you do? What can't you?"

---

# Slide 4 — Changing permissions: symbolic & numeric

## Slide Content
- Symbolic: `chmod u+x script.sh` · `chmod g-w,o-r file` · `chmod +x` (all)
- Numeric: `r=4 w=2 x=1` → `rw-r-----` = **640**
- Compute, don't memorize: 7=rwx, 6=rw-, 5=r-x, 4=r--
- umask: what's *removed* from new files (022 → 644/755; 027 → 640/750)

## Instructor Delivery Notes
Drill 640/755/600 aloud until reflexive. umask subtraction direction
("which base?") is a known trap — the M12 quiz asks why files and dirs
start from different bases (no execute-by-default for files).

## Visual or Demonstration Suggestion
`umask 027; touch f; mkdir d; ls -l` — verify the arithmetic live.

## Student Question
"Your umask is 077. What mode do your new scripts get — and can your *teammate* run them?"

---

# Slide 5 — Knowledge check

## Slide Content
1. `-rw-r-----` and you're in the file's group, not the owner: read? write?
2. `(umask 077; touch x)` — does your shell's umask change?
3. Design: dataset shared read/write by a 5-person team, invisible to others.

## Instructor Delivery Notes
Q1's answer (yes read, no write — permission *source of truth* is the
matching triplet) settles a decade of confusion. Q3 previews the SGID
slide deliberately — park answers there.

## Visual or Demonstration Suggestion
— (Q3 answers go on the board, revisited at Slide 7)

## Student Question
(Q1 is the check)

---

# Slide 6 — Shared access: groups, SGID, sticky

## Slide Content
- Shared dirs live under a **group**: `chgrp research dir` + `chmod 2770 dir`
- **SGID on a directory**: new files inherit the *group* — the team's files stay the team's
- **Sticky bit (`1770`, /tmp-style)**: only the file's owner (or admin) may delete — protects teammates from each other
- ACLs (getfacl/setfacl) when one team isn't enough — M13 has the clinic

## Instructor Delivery Notes
This is Mini-Project B territory: 6-person team, mixed access. The
2770 vs 1770 trade-off ("can Elena delete Ben's files?") is the best
10 minutes of the unit — stage it as a scenario vote.

## Visual or Demonstration Suggestion
Two-file demo in a 2770 dir: teammate-created file deleted by *you* — then sticky set, retried, blocked.

## Student Question
"In a 2770 folder, who can delete *your* files? Fix it with one digit."

---

# Slide 7 — root, sudo, and the policy of least privilege

## Slide Content
- Root bypasses permissions — power with no seatbelt
- `sudo command` = do this one thing with authority, **logged**
- Policy lives in `sudoers` — edited **only** via `visudo` (syntax-checked)
- Drop-ins in `/etc/sudoers.d/` — scoped, named, reviewable
- Least privilege: grant the *command*, not the kingdom

## Instructor Delivery Notes
Read an M14 incident aloud (they exist as teaching material) — the
NOPASSWD-for-everything story. The `sudo command > file` redirection
trap belongs on the board: *your shell* opens the file, so sudo doesn't
help.

## Visual or Demonstration Suggestion
`sudo -l` — "what am I *allowed* to do?" — and a real drop-in file shown via `visudo -f`.

## Student Question
"A teammate asks for sudo ALL 'just to install stuff'. What do you grant instead?"

---

# Slide 8 — Environment variables & PATH

## Slide Content
- Environment = the variables every child process inherits
- `echo $HOME $USER $PATH` · `env` · `export VAR=value` (export = children see it)
- **PATH**: colon list of where executables are searched, in order
- `type -a python3` shows *which one wins* — and shadows are how tools "mysteriously differ"
- `sudo cmd` often resets env — script paths differ between you and cron/sudo

## Instructor Delivery Notes
The PATH murder-mystery (two `python3`s, one venv) is the set-up for
M27's venv work — plant it now, resolve it in week 13. `sudo`-env
interaction previews M19's cron trap: same disease.

## Visual or Demonstration Suggestion
Prepend a dir with a fake `python3` to PATH — `type -a` shows the shadowing live.

## Student Question
"Your script runs fine interactively and fails in cron. First suspect?"

---

# Slide 9 — Common mistakes (Unit 4)

## Slide Content
- `chmod -R 777` as a solution — a confession, not a fix (M13's line)
- Forgetting `x` on directories → "I set r! why can't they cd?"
- Editing sudoers with a plain editor (a typo locks everyone out)
- `export` without export — works in your shell, vanishes in the script
- Granting sudo ALL when a single command was needed

## Instructor Delivery Notes
All five have graded consequences in LA-3 — say so; alignment motivates
attention.

## Visual or Demonstration Suggestion
The `777` confession meme-worthy line: "when everyone can write, no one is accountable."

## Student Question
"Which mistake is *recoverable* with a snapshot and which isn't?"

---

# Slide 10 — Data Science connection

## Slide Content
- Real labs: shared dataset trees with per-team groups — exactly M13's model
- Model/experiment dirs: sticky bit so nobody nukes a colleague's run
- venvs & per-user Jupyter (M27) rest on *user separation* you just learned
- Secrets hygiene starts here: config files `600` (M25 builds on this)

## Instructor Delivery Notes
Map each bullet to its capstone rubric row (permission matrix vs
`namei -l` reality) — the payoff of this unit is literally a graded
capstone area.

## Visual or Demonstration Suggestion
A real `/srv/datasets` listing annotated with the design decisions.

## Student Question
"What permission design would *your* final-project dataset directory need?"

---

# Slide 11 — Summary & exit ticket

## Slide Content
**Summary:** identity (uid/gid) → triplet decode → chmod/umask → shared
design (SGID/sticky) → sudo with policy → environment & PATH shadows
**Exit ticket:** decode `2770`; name the flag that makes new files
inherit the team group; one-line: why not sudo ALL?
**HW:** M12–M15 quizzes · Mini-Project B · **midterm prep sheet** (S13)

## Instructor Delivery Notes
The prep-sheet assignment is the consolidation week's engine — one page,
own words, allowed into the exam per the midterm rules.

## Visual or Demonstration Suggestion
— 

## Student Question
(exit ticket is the question)

---

## Deck references
- Modules: [M12](../../modules/M12-users-groups-permissions/README.md) · [M13](../../modules/M13-ownership-shared-access/README.md) · [M14](../../modules/M14-sudo-root-principle/README.md) · [M15](../../modules/M15-environment-variables/README.md)
- Next: [Midterm consolidation → exam](../teaching-plan/16-week-course-plan.md), then [Unit 5](unit-05-software-storage-time-slides.md)
