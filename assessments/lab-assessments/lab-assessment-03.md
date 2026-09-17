# LA-3 — Permissions Repair (15 min)

> Assesses: M12–M14 labs · 10 points · evidence transcript required.
> Setup (instructor pre-stages per pair): a scratch user `checker`
> plus the three broken states below. Snapshot and restore between
> students.

## Given (staged states)

```text
~/check/
├── run.sh        # mode 600, owned by checker — "checker can't run it"
├── data.csv      # mode 640, group proj, owned by root — "checker can't read it"
└── shared/       # mode 775, group proj — "checker's new files aren't group-writable"
```

`checker` is NOT yet in group `proj`. You have full sudo on this
machine only.

## Tasks

**T1 (3).** Make `run.sh` runnable by `checker` *and* by `proj`
members, with the narrowest mode that does both.

**T2 (4).** Give `checker` read access to `data.csv` by **group
membership** (not by opening `other` bits, not by chown to checker).
Two commands minimum membership change + re-login proof.

**T3 (3).** Fix `shared/` so files created by anyone in `proj` land
group-`proj` and group-writable immediately. Prove by creating a
file as `checker` and showing the `ls -l` line.

## Rubric

| Points | Requirement |
|---|---|
| 1 | T1 mode is exactly `750` (or `740`+group-exec reasoning) — not `777` |
| 1 | T1 evidence: `ls -l` before/after |
| 1 | T2 uses `usermod -aG proj checker` (with `-a`!) |
| 1 | T2 proves membership (`id checker` or re-login `newgrp`) |
| 1 | T2 does not chmod the file to 604/644 (that's the anti-answer) |
| 1 | T3 sets SGID (`chmod g+s` / `2775`) |
| 1 | T3 proof file shows group `proj` on a *new* file |
| 1 | T3 file shows group-write bits without a post-hoc chmod |
| 1 | Transcript ordered, no history gaps |
| 1 | Any `sudo` use is scoped (no `chmod -R 777` anywhere) |
