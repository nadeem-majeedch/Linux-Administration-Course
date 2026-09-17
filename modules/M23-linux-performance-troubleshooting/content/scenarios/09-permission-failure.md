# Drill Card 9 — "Permission Failure"

> Scenario family: Identity & access · Difficulty: ●●○
> Source modules: [M12/M13](../../../M12-users-groups-permissions/README.md), [M14](../../../M14-sudo-root-principle/README.md)

## Symptom

`Permission denied` — on reading a file, entering a directory, running
a script, or binding a port. Three questions before any command: *who
am I, who owns it, which mode bit is missing?*

## Decision tree

```text
id                    → who am I (user, groups)?
ls -l <path>          → owner/group/mode of the object?
├─ missing w on file  → write denied
├─ missing x on dir   → traversal denied (can't cd INTO it)
├─ path works locally, fails in script → which directory level? namei -l
└─ "permanently" on everything → auth problem, not perms (ssh keys, sudoers)
```

## Evidence

```console
$ id                                   # your identity, the first fact
$ ls -ld data/raw data/raw/sales.csv   # -d for directories, both levels
$ namei -l data/raw/sub/file.csv       # EVERY component's perms on the path
$ sudo -l                              # what sudo MAY do (M14's check)
$ getfacl data/raw 2>/dev/null         # ACL layer, if present (M13 awareness)
```

`namei -l` is the card's superpower: it walks every component of the
path and shows *which level* actually denies — the file's `r--` is
irrelevant when the parent directory lost its `x`. Half of all
"permission denied" tickets die at this command.

## Fix pattern

- **Ownership wrong** (files created as root by a sudo'd job) →
  `sudo chown -R ds:ds ~/projects/…` — scoped to the affected tree,
  never `/`, never recursive on a path you didn't type in full.
- **Group access missing** → add the group (`sudo usermod -aG research
  ds`, re-login required) or fix the directory's group + SGID for
  shared datasets (M13's `2770` pattern).
- **The mode bit** → `chmod` the specific bit (`u+w`, `g+r`), not
  `777` — the blast-radius sentence (M25 §1) is mandatory before any
  mode change on shared paths.
- **sudo refuses** → `sudo -l` shows the policy; the fix is a policy
  conversation, not editing sudoers on a production box (M14's rule).
- **"Denied" for port bind** (<1024) → not file perms: bind-scope /
  capability question — card 8's rung 5 or a container port mapping.

## Verify

The *original operation* succeeds as the *original user* — not under
sudo (sudo "fixes" permission problems by ending the permission
system's involvement; that's a bypass, not a verification). Re-run the
failing command verbatim.

## Document

Quote the `id`, the `namei -l` line that denied, and the mode change.
Vocabulary: *"job ran under sudo, chowned outputs to root"*, *"parent
dir lost x"*, *"user absent from research group (needs re-login)"*.

**Done when:** you can reproduce a denied-then-fixed path in your own
home tree, with `namei -l` as the evidence centerpiece and the undo
recorded.
