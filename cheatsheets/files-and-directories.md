# 2 — Files and Directories

> Learn it: [M06 — Filesystem Hierarchy](../modules/M06-filesystem-hierarchy/content/README.md) ·
> [M07 — Files and Directories](../modules/M07-files-and-directories/content/README.md) ·
> Lookup, not understanding.

## Create, list, move

| Command | Purpose | Syntax | Important options | Example |
|---|---|---|---|---|
| `mkdir` | make directory | `mkdir DIR…` | `-p` nested + no-error-if-exists | `mkdir -p ds/{data,src,reports}` |
| `touch` | empty file / update mtime | `touch FILE…` | — | `touch notes.md` |
| `cp` | copy | `cp SRC DST` | `-r` recursive · `-i` ask · `-p` preserve mode/times · `-a` archive | `cp -a raw/ backup/` |
| `mv` | move / rename | `mv SRC DST` | `-i` ask · `-n` no-clobber | `mv draft.md final.md` |
| `rm` | delete | `rm FILE…` | `-r` recursive · `-i`/`-I` ask · `-f` force | ⚠️ see below |
| `rmdir` | delete **empty** dir | `rmdir DIR…` | — | `rmdir old/` (refuses if not empty) |

⚠️ **`rm` has no trash can.** Reflexes that keep you employed:
quote globs after looking at them (`ls *.csv` → ↑ → swap `ls` for
`rm`), prefer `rm -i`/`-I` in scripts' interactive runs, and never
`sudo rm -rf` a path you haven't `pwd`'d. Variables used in `rm -rf
"$DIR"` must exist — `set -u` makes typos fail loudly.

## Copying with intent

| Goal | Command |
|---|---|
| copy a tree, preserving everything | `cp -a src/ dst/` |
| copy only `.csv` | `cp data/*.csv dst/` |
| ask before overwriting | `cp -i src dst` |

## Where files live (FHS landmarks)

| Path | Holds | Example tenant |
|---|---|---|
| `/home/USER` | user files | your projects |
| `/etc` | system configuration | `ssh/`, `systemd/` |
| `/var/log` | logs | `journal/`, `syslog` |
| `/tmp` | scratch, wiped on reboot | nobody's promises |
| `/usr` | distro-installed software | `/usr/bin/python3` |
| `/usr/local` | your hand-installed software | source builds |
| `/opt` | third-party bundles | browsers, IDEs |
| `/srv` | served data | web roots |
| `/dev` | devices as files | `/dev/sda`, `/dev/null` |
| `/proc`, `/sys` | kernel/process views | `/proc/cpuinfo` |
| `/run` | runtime state (tmpfs) | pid files, sockets |

## Links

| Type | Create | Key facts |
|---|---|---|
| hard link | `ln FILE LINK` | same inode, shared content, no directories, no cross-filesystem; survives original's deletion |
| symlink | `ln -s TARGET LINK` | own inode, a pointer; dangles if target moves; follows across filesystems |

```console
$ ls -li
123 -rw-r--r-- 2 ana ana 14 … hard2      ← same inode as hard1 (count 2)
456 lrwxrwxrwx 1 ana ana  6 … sym -> file ← its own inode, type l
```

## Finding files

| Command | Purpose | Example |
|---|---|---|
| `find DIR -name '*.csv'` | by name | `find . -name '*.log' -mtime -7` |
| `find … -size +100M` | by size | plus `-type f` for files only |
| `find … -exec CMD {} \;` | act on results | `find . -name '*.tmp' -delete` ⚠️ list first |
| `locate PATTERN` | instant (indexdb) | `sudo updatedb` refreshes |
| `which CMD` | where's the executable | `which python3` |
| `type CMD` | what kind of thing is it | `type ll` |

⚠️ `find … -delete` deletes in find's traversal order — always run
the same find **without** `-delete` first and read the list.
