# Lab 2 — The Space Audit: df, du & the Cleanup Plan

> Module 17 · Unit 5 · Difficulty: Intermediate
> Time: ~40 min · Environment: your own VM/WSL2 · **Read-only until the
> final section**, where you execute *your own* plan on *your own*
> directories
> Prerequisites: [Lesson 1](../lessons/01-block-devices-topology.md), [Lesson 4](../lessons/04-swap-lvm-raid-ssd.md)

Storage administration's most common real task isn't formatting disks —
it's answering "why is the disk full?" without breaking anything. This
lab runs that investigation on your own machine and ends with an
executed, evidenced cleanup.

## Part A — the filesystem view (df)

```console
$ df -h | grep -v tmpfs          # real filesystems only
$ df -i | grep -v tmpfs          # inode headroom
$ findmnt | head -12             # what's mounted where (tree)
```

**Record:** total capacity, the most-full real filesystem and its %,
inode use% on `/`, and one sentence: which filesystem would feel a
1-GB dataset upload first?

## Part B — the ownership view (du)

```console
$ sudo du -h --max-depth=1 / 2>/dev/null | sort -rh | head -10
$ du -h --max-depth=1 ~ | sort -rh | head -10
$ sudo du -h --max-depth=1 /var 2>/dev/null | sort -rh | head -6
```

**Record:** the top consumers at each level (system, home, /var), and
the *one* entry that surprised you. Common suspects on a course VM:
`/var/cache/apt` (Lesson: `apt clean` from M16), `~/.cache`,
`/var/log/journal` (M24's `journalctl --vacuum-size`), old kernels in
`/boot`, and — in WSL2 — everything, because the virtual disk only
grows.

## Part C — the df/du mystery hunt (guided)

Reproduce the classic disagreement safely:

```console
$ sleep 600 &                       # a process that lives 10 minutes
$ tail -f /var/log/syslog > /tmp/holder.log 2>/dev/null || tail -f /var/log/syslog > ~/holder.log
$ df -h /tmp | tail -1              # note Used
$ rm ~/holder.log /tmp/holder.log 2>/dev/null    # delete it out from under tail
$ df -h /tmp | tail -1              # same Used! the space is "gone"
$ lsof +L1 2>/dev/null | grep -E "tail|holder"   # the holder, revealed
```

Kill the `sleep`/`tail` pair and re-run `df` — space returns. **Record:**
the before/after numbers and the one-sentence explanation (open file
descriptors keep blocks allocated until the last holder exits). This is
the #1 real-world "df says full, du says fine" cause on servers.

## Part D — the cleanup plan (the deliverable)

Write, in `lab-log.md`, a prioritized plan: **five** cleanup actions,
each with — command, expected reclaim, risk note (`none/low/why`). Use
this menu as a starting point, but *your* machine's Part-B evidence
should reorder it:

```text
1. sudo apt clean                     # apt archives — ~N MB — none (re-fetchable)
2. rm -rf ~/.cache/pip                # pip wheels — ~N MB — none
3. journalctl --vacuum-size=100M      # old logs — ~N MB — low (recent logs kept)
4. docker system prune (if M28 done)  # dangling layers — ~N MB — low (rebuildable)
5. rm old files in ~/scratch          # my own junk — ~N MB — MY judgment call
```

**Rules for the plan:** nothing outside your home without a
sudo-*readable* justification; nothing that isn't re-fetchable,
regenerable, or explicitly yours; and every action reversible or
honestly marked otherwise.

## Part E — execute and verify (only your own actions)

Run your plan's items **one at a time**, re-running
`df -h <filesystem>` after each:

```console
$ df -h / | tail -1          # before
$ <action 1>
$ df -h / | tail -1          # after — record the delta
```

**Record:** a before/after table with per-action deltas and the total
reclaimed. If an action reclaimed nothing, say so — negative results
are evidence too.

## Wrap-up — the monitoring habit

The audit is a snapshot; fullness is a *trend*. Set a calendar habit
(or, after M19, a cron line): weekly `df -h | grep -vE "tmpfs|loop"` +
`du -h --max-depth=1 ~ | sort -rh | head -3` pasted into lab-log. Two
commands, thirty seconds, and "disk full" incidents become schedule
entries instead of emergencies.

## Done when

- [ ] df/du evidence from Parts A–B recorded
- [ ] The df/du mystery reproduced, explained, and cleaned up (Part C)
- [ ] Five-action cleanup plan written with risk notes (Part D)
- [ ] Plan executed one-by-one with before/after deltas (Part E)
- [ ] Monitoring habit noted
