# Unit 4 Teaching Guide — System Administration (M12–M15)

> Sessions S11–S12 · companions: [speaker notes](../../speaker-notes/unit-04-system-administration-notes.md) · [deck](../../lecture-slides/unit-04-system-administration-slides.md)

## M12 Users, Groups & Permissions (S11)

**Objectives.** Triplet decoding as reflex; numeric/symbolic chmod; the
directory-x mechanism; umask arithmetic with *why*.

**Sequence.** Identity (id/passwd fields) → triplet ritual → chmod
both forms → directory-x demo → umask → shared-access design begins.

**Difficult concepts.**
- *Directory x* — the traverse-vs-list distinction. The chmod-000-on-a-
  directory demo shows both failures with different messages; the
  messages name the missing bits.
- *umask bases* — 666 for files, 777 for dirs; the *why* (execute never
  granted by default) converts arithmetic into mechanism.

**Common mistakes.** Recursive 777; `chmod +x` on data files; symbolic
mode typos silently doing nothing (chmod doesn't error on no-op).

**Demo plan.** Directory-000 demo; umask verify (`umask 027; touch f;
mkdir d; ls -l`).

**Activity.** Permission-decoding sprints (8 lines, 20 s each).

**Assessment hook.** M12 quiz (evidence-interpretation format — the
course exemplar); LA-3 in week 12 builds on this lab's repair patterns.

**Extension.** ★★★: M12 challenges (the umask forensics items).

**Troubleshooting (in class).** The multi-user lab needs pre-staged
accounts — verify the staging script ran *before* the session (the
[infrastructure checklist](../../setup-and-delivery/lab-infrastructure.md)).

## M13 Ownership & Shared Access (S11, second half)

**Objectives.** Group-based sharing as *design*; SGID inheritance;
sticky-bit semantics; the Mini-Project B design task.

**Difficult concepts.** SGID-on-directory inheritance (new files get the
*team's* group) — demo by touch-in-dir-then-ls -l. Sticky bit: the
delete-the-teammate's-file demo, then the one-digit fix.

**Common mistakes.** Designing with owner-permissions instead of groups;
forgetting that *existing* files don't retroactively inherit SGID (chmod
-R g+s or relink needed).

**Assessment hook.** M13 quiz (SGID/sticky/ACL trade-offs); Mini-Project
B is the design artifact.

**Extension.** ★★★: the ACL clinic items (getfacl/setfacl) from M13.

**Discussion.** "When is 1770 *wrong* even for a team?" (shared
executable drop zones vs document folders).

## M14 Sudo & the Root Principle (S12)

**Objectives.** sudo as policy engine; drop-in authoring with
`visudo -c` verification; the redirection trap; least-privilege as
graded language.

**Difficult concepts.** The `sudo cmd > file` open-by-whose-shell
mechanism — draw it (two processes, one file open). `sudo sh -c` as the
correct pattern and *why*.

**Common mistakes.** Editing sudoers directly (a typo = locked-out
root); NOPASSWD sprawl; granting ALL for "installing stuff".

**Demo plan.** Scoped drop-in authored live, `visudo -c` check, `sudo
-l` verification from the student side.

**Assessment hook.** M14 quiz (policy reasoning + incident reading);
midterm scope *ends* at M14/M15 — say so.

**Extension.** ★★★: M14's incident set — write the policy fix for a
real-world sudoers failure.

**Troubleshooting.** A broken drop-in can lock the *lab* user — staging
snapshots are the insurance; never debug live sudoers in front of the
class on your only admin session (the second-session rule applies to
instructors too).

## M15 Environment Variables (S12, second half)

**Objectives.** Inheritance model; PATH resolution order; the sudo/cron
env interactions (planted for M19/M27).

**Difficult concepts.** Inheritance *per-process* — the `export`
without-export demo (works in shell, gone in child).

**Common mistakes.** Editing PATH by replacement (`PATH=dir`) instead
of prepend; expecting `.bashrc` changes in already-open shells.

**Assessment hook.** M15 quiz (inheritance diagnosis); the PATH mystery
resolves in M27 (venv mechanism) — plant now.

**Extension.** ★★★: M15 challenges (the env-forensics scenario).

---

## Unit-level notes

- **Midterm consolidation follows (S13).** These two sessions *are* the
  syllabus's first half — the prep-sheet HW (S12) is the bridge.
- **The staged multi-user labs need infrastructure:** pre-run the
  staging, snapshot per pair, restore between — the
  [lab infrastructure page](../../setup-and-delivery/lab-infrastructure.md)
  has the checklist.
- **Graded language warning:** "allow with justification," "least
  privilege," "scoped grant" — these phrases *are* the LA-3 and capstone
  rubric vocabulary; model them in every answer you give.
