# Lab 2 — FHS Scavenger Hunt

> Lesson 3 · Time: ~45 min · Risk: zero — strictly read-only

## Goal

Prove the FHS map by *finding real evidence* for each directory's contract. This
is the read-only tour that makes /etc, /var, /proc et al. familiar before any
module asks you to modify anything.

## Rules

- **Read-only commands only**: `ls`, `cat`, `head`, `tree`, `stat`, `file`.
- Anything you can't read (permission denied) is itself an answer — log it as such.
- Every find gets recorded: path + one line of what it proves.

## Hunt list (10 finds)

| # | Find | Hint |
|---|---|---|
| 1 | The file that names your distro and version | M01 used it |
| 2 | The hostname config file — and its owner/group from `ls -l` | /etc |
| 3 | Any *log file* that grew today (check the date column) | /var/log |
| 4 | Evidence that /bin is a symlink — where does it point? | `ls -ld /bin` |
| 5 | A program that lives in /usr/bin — pick one, run `which` on it | any tool from M01 |
| 6 | The kernel's live CPU view — via /proc this time, not lscpu | M01 again |
| 7 | Your own process's "directory": find your shell's PID in /proc | M18 preview |
| 8 | A device file for your disks — *look, don't touch* | /dev, M17 preview |
| 9 | Proof that /tmp is world-writable (first field of `ls -ld`) | note the `t` at the end |
| 10 | One *third-party* program under /opt (or prove none is installed) | many fresh VMs have none — that's a valid finding |

## Decode challenge (10 min)

For these three `ls -ld` readings of *scratch-like* directories, state who may
write each and what happens at reboot (use Lesson 3's map; we formalize the
permission letters in M12):

```console
$ ls -ld /tmp /var/tmp /run
drwxrwxrwt 12 root root 40960 Sep 15 21:10 /tmp
drwxrwxrwt  2 root root  4096 Sep  1 09:00 /var/tmp
drwxr-xr-x 25 root root     0 Sep 15 20:05 /run
```

## Wrap-up checklist

- [ ] 10 finds logged with paths and proof lines
- [ ] Permission-denied stops (if any) logged as findings, not failures
- [ ] Decode challenge answered for all three directories
- [ ] One line: which FHS area surprised you most, and why
