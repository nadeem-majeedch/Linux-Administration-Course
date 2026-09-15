# Mini-Project B — Shared Dataset Server Design (M13)

> Module: M13 — Ownership and Shared Access · Unit 4 · Difficulty: Intermediate
> Prerequisites: M12, M13 in progress; all work in your own VM

## Brief

A fictional six-person research team shares one Ubuntu server for their datasets:

- **Dr. Ada Okoye** (principal investigator)
- **Ben, Chen, Devi** (PhD students — read/write on all project data)
- **Elena** (MSc student — read-only on all project data, writes only in her own folder)
- **Farid** (external collaborator — access to exactly one dataset, nothing else)

Design and implement the access model: users, groups, directory tree, ownership,
permissions, and ACLs. Every decision must be justified in writing.

## Deliverables

1. **`access-plan.md`** — the design document:
   - group design (which groups, who is in which, why)
   - directory tree with target ownership/permissions per level
   - where classic permissions suffice and where ACLs are required (and why)
   - umask assumptions for shared directories
   - how new files land group-writable (setgid, default ACLs)
   - least-privilege rationale: what you deliberately did *not* grant
2. **`setup_shared_tree.sh`** — scripted demo that builds the whole structure:
   creates users and groups, the tree, applies ownership/permissions/ACLs.
   Must be idempotent (safe to re-run) and pass `shellcheck`.
3. **`verification.md`** — evidence: as each user, show what they can and cannot do
   (command + outcome pairs proving the matrix below).

## Required access matrix (verify all cells)

| Path | Ada | Ben/Chen/Devi | Elena | Farid | Others |
|---|---|---|---|---|---|
| `/srv/team` | rwx | r-x | r-x | — | — |
| `/srv/team/datasets` | rwx | rwx | r-x | — | — |
| `/srv/team/datasets/shared-metrics` | rwx | rwx | r-x | r-- (ACL) | — |
| `/srv/team/elena-sandbox` | rwx | — | rwx | — | — |
| `/srv/team/archive` | rwx | r-x | r-x | — | — |

(`rwx` on a directory means traversal + listing + creation as applicable; `—` means
no access. Farid's single-dataset access must be granted via ACL, not group membership.)

## Constraints

- Runs entirely in your VM; test users are created by your script.
- No password sharing between users; no `chmod 777` anywhere (justify every world-access bit — the correct answer is usually "none").
- The script must not fail on re-run (check-before-create patterns).

## Rubric

| Criterion | Weight |
|---|---|
| Access matrix verified with evidence | 35% |
| Design rationale (least privilege, group model, ACL choices) | 30% |
| Script correctness and idempotency | 20% |
| shellcheck clean + style | 15% |

## Stretch goals

- Add a "leaver" procedure: a script that revokes one member's access completely.
- Add a default-ACL design so *future* subdirectories inherit correctly.
