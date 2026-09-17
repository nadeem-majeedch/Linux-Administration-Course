# Unit 4 Labs — System Administration (M12–M15)

> Sessions S11–S12 · identity and access: staged multi-user labs —
> snapshots per pair, restore between, the second-session habit begins.

| Lab | Module | Duration | Difficulty | Deliverable | Link |
|---|---|---|---|---|---|
| Permission repair clinic | M12 | 30' | ★★ | broken modes fixed *with justification per fix* | [M12 labs](../../../modules/M12-users-groups-permissions/content/labs/README.md) |
| Shared-tree design | M13 | 30' | ★★★ | group/SGID/sticky design + verification | [M13 labs](../../../modules/M13-ownership-shared-access/content/labs/README.md) |
| sudo drop-in workshop | M14 | 25' | ★★★ | scoped drop-in, `visudo -c` proof, `sudo -l` evidence | [M14 labs](../../../modules/M14-sudo-root-principle/content/labs/README.md) |
| sudo incidents | M14 | 20' | ★★★ | three failure tickets diagnosed | [M14 labs](../../../modules/M14-sudo-root-principle/content/labs/README.md) |
| Environment forensics | M15 | 15' | ★★ | PATH/env inheritance evidence | [M15 labs](../../../modules/M15-environment-variables/content/labs/README.md) |
| Mini-Project B | M13 | HW | ★★★ | shared dataset server *design* (6-person team) | [M13 practice](../../../modules/M13-ownership-shared-access/content/practice/challenges.md) |

## Session mapping

- **S11**: permission repair clinic + shared-tree design; Mini-Project B
  assigned
- **S12**: sudo drop-in workshop + incidents + environment forensics

## The safety architecture of this unit

- All labs run on **staged snapshots** — breakage is the pedagogy,
  restore is the reflex (LA-3's staged faults use the same pattern)
- The sudo workshop uses a **drop-in file**, never the main sudoers;
  `visudo -c` proof is a deliverable, not decoration
- The second-session habit is *introduced* in the sudo context and
  becomes mandatory in M25's firewall work

## Checkpoints that matter most

- Every repair in the clinic carries a **justification line** — "777
  works" is not an answer; "g+rw because the research group needs write,
  o= because the dataset is private" is
- The sudo incidents: name the *policy* failure, not just the typo

## Extension routing (★★★)

- M13: the ACL clinic (getfacl/setfacl) — beyond-course-scope but fully
  supported by the module
- M14: write the policy fix for a real-world sudoers incident

## Instructor staging

Multi-user accounts and broken states are **pre-staged per pair** — run
the staging the afternoon before and snapshot; restore between pairs. The
[infrastructure checklist](../../setup-and-delivery/lab-infrastructure.md)
covers it; the staging pattern mirrors LA-3's.

## After this unit

**Midterm consolidation (S13) + Midterm (S14)** — Units 1–4 are the
paper's scope; the prep-sheet HW (S12) and the station circuit (S13)
are the bridge. M14/M15 are *in* scope — the last two modules before
the exam.
