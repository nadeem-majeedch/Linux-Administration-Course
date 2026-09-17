# Quiz M12 — Users, Groups & Permissions (exemplar format)

> 10 questions · 20 minutes · closed book.
> Every question gives evidence or a scenario; answers are graded on
> reasoning. Key: [quiz-m12-key.md](quiz-m12-key.md).

## Section A — Evidence interpretation

**Q1.** You run:

```console
$ ls -l /srv/datasets/sales.csv
-rw-r----- 1 ana research 10485760 Mar  3 09:14 /srv/datasets/sales.csv
$ id
uid=1002(ben) gid=1002(ben) groups=1002(ben),1005(research)
```

Ben runs `cat /srv/datasets/sales.csv`. What happens, and *which*
permission bit decides it? If it fails, state the exact error class
and the two distinct fixes, ranked by least privilege.

**Q2.** After a `chgrp research sales.csv; chmod 640 sales.csv`, a
teammate reports "still can't write". You see:

```console
$ ls -l sales.csv
-rw-r----- 1 ana research 10485760 …
$ groups teammate
teammate : teammate
```

Diagnose precisely. Why did the `chgrp` change *nothing* about their
access, and what single fact about group membership is the actual
gate?

**Q3.** Explain the difference between what these two listings tell
you, and when you'd need each:

```console
$ ls -l /home
drwxr-x--- 42 ana    ana    4096 Mar  3 09:14 ana
$ ls -ln /home
drwxr-x--- 42 1001 1001 4096 Mar  3 09:14 ana
```

**Q4.** A directory shows `drwxrwsr-T`. Decode every letter — type,
each triad, and both special characters — and state what the `T`
implies about the `other` execute position.

## Section B — Scenario diagnosis

**Q5.** New script `deploy.sh` is created on a shared box with
default umask `0022`. A teammate gets *Permission denied* on
`./deploy.sh`. Give the two independent reasons (mode bits), the
minimal fix, and the umask that would have prevented the surprise
for a shared *group* project.

**Q6.** Ben, a member of `research`, creates a file inside
`/srv/research/` (directory group `research`, mode `2770`). The file
lands as group `ben`, not `research`. What single missing
ingredient explains this, and what does the `2` in `2770` do in the
*correct* configuration? State the check-order rule your explanation
relies on.

**Q7.** `usermod -G docker ben` was run (no `-a`). Ben reports he
lost `sudo`. Explain the mechanism — what `-G` does to supplementary
groups — and give the recovery command plus the flag pair that never
causes this.

**Q8.** You must give *one* external auditor read access to exactly
one directory tree, without adding them to any team group. Compare:
(a) add to a new group + chgrp, (b) ACL entry, (c) copy the tree to
a permissioned area. Pick one for a 2-hour audit on a production box
and justify against the other two.

## Section C — Design & justify

**Q9.** A PI wants: "students can read all project data, write only
in their own folders; nothing in the project tree may be deleted by
anyone except its owner." Specify owners, groups, modes (including
special bits) for the tree root, student folders, and data folder —
and name the one requirement this permission model *cannot* deliver
alone.

**Q10.** Junior admin proposes fixing every "Permission denied"
ticket with `sudo chmod -R 777 /srv`. Write the three-sentence
policy response: what this actually grants (decode 777 in a shared
context), which failure it causes that *outlives* the ticket, and
the diagnostic step that should precede any chmod.
