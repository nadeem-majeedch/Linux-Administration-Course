# Demo Index

> Ten flagship demonstrations mapped to sessions. Every entry links its
> script; scripts follow the [demo contract](README.md#the-demo-contract-every-script-follows-it).

| # | Demo | Session | Duration | Risk | Fallback | Script |
|---|---|---|---|---|---|---|
| 1 | Filesystem navigation: paths that lie | S5 | 8' | none | not needed | [01](module-demos/01-filesystem-navigation.md) |
| 2 | The permission matrix: decoding & breaking | S11 | 12' | low (VM) | rehearsed recovery | [02](module-demos/02-permissions-matrix.md) |
| 3 | Users & groups: the shared folder | S11 | 10' | low (VM, staged users) | planned-failure demo | [03](module-demos/03-users-and-groups.md) |
| 4 | Processes & signals: TERM vs KILL | S17 | 10' | low (VM) | trap script ships | [04](module-demos/04-processes-and-signals.md) |
| 5 | Package management: the dependency negotiation | S15 | 8' | low (VM, snapshot) | — | [05](module-demos/05-package-management.md) |
| 6 | Pipes & redirection: where bytes go | S8 | 12' | low (sacrificial files) | planned-failure demo | [06](module-demos/06-pipes-and-text-processing.md) |
| 7 | SSH & file transfer: keys, tunnels, verified sync | S21–S22 | 15' | low (loopback) | rehearsed recovery | [07](module-demos/07-ssh-and-file-transfer.md) |
| 8 | systemd services & logs: break, read, fix | S19/S23 | 12' | low (user units) | rehearsed recovery | [08](module-demos/08-systemd-services-and-logs.md) |
| 9 | Storage & backups: the loopback lifecycle | S16 | 15' | **medium** (mkfs — loopback only) | **recording exists** | [09](module-demos/09-storage-and-backups.md) |
| 10 | Docker & the DS workflow: containerized Jupyter | S27 | 12' | low (VM+Docker) | non-Docker fallback path | [10](module-demos/10-docker-ds-workflow.md) |

## Session coverage check

Every unit's most load-bearing idea has a live demonstration: paths (U2
S5), permissions (U4), signals (U5), packages (U5), redirection (U2),
SSH/transfer (U6), services/logs (U6), storage (U5), containers (U7).
Unit 8's "demos" are the drill incidents themselves — see the [M32
teaching guide](../instructor-manual/module-teaching-guides/unit-08-capstone.md).

## Risk notes

- **Medium (demo 9):** `mkfs` is genuinely destructive *as a command*;
  the loopback-file object makes it safe. The four-line rule is recited
  on stage. A recording exists — use it if the room's state is wrong.
- **Planned-failure demos (3, 6):** the *failure* is the content; the
  recovery choreography is rehearsed, and cleanup is a printed-path
  census.
- Everything else runs inside student-equivalent VMs with snapshot
  points.

## Scheduling flexibility

Demos map to *sessions*, not minutes — if a session runs short, demo 6
(dual) and demo 4 (dual) each split cleanly across two visits; the
scripts mark their natural halves.
