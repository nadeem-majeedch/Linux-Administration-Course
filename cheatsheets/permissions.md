# 3 — Permissions

> Learn it: [M12 — Users, Groups & Permissions](../modules/M12-users-groups-permissions/content/README.md) ·
> [M13 — Ownership & Shared Access](../modules/M13-ownership-shared-access/content/README.md) ·
> Lookup, not understanding.

## Reading a mode

```text
- rw-  r--  ---
│  │    │    └── other: no access
│  │    └─────── group: read only
│  └──────────── owner: read + write
└ file (-) / directory (d) / link (l)
```

Directory bits mean **traverse** (`x`: enter, reach things inside),
**list** (`r`: read names), **create/delete** (`w`: modify entries).
A directory without `x` is a locked door even with `r`.

## chmod — change mode

| Style | Syntax | Example |
|---|---|---|
| symbolic | `chmod WHO OP MODE FILE` | `chmod g+w data/` · `chmod o-r secrets.txt` · `chmod a+x run.sh` |
| numeric | `chmod NNN FILE` | `644` files · `755` scripts/dirs · `600` private |
| recursive | `chmod -R` | ⚠️ audit with `find … -type f`/`-type d` first — files and dirs want different modes |

| Who | `u` owner · `g` group · `o` other · `a` all |
|---|---|
| Op | `+` add · `−` remove · `=` set exactly |

## umask — what new files *won't* get

```console
$ umask            # show (bits REMOVED from 666/777 defaults)
0022
```
| umask | new file | new dir | character |
|---|---|---|---|
| `022` | `644` | `755` | default: private-ish |
| `002` | `664` | `775` | group-collaborative |
| `077` | `600` | `700` | maximum privacy |

Set per-session (`umask 002`) or in `~/.profile`. It cannot grant
bits — only withhold them.

## chown / chgrp — change ownership

| Command | Syntax | Notes |
|---|---|---|
| `chown USER FILE` | `sudo chown ana data.csv` | needs root (or `sudo chown ana:team f` for user+group) |
| `chgrp GROUP FILE` | `chgrp team data.csv` | you may chgrp to a group *you belong to* without sudo |
| recursive | `-R` | ⚠️ same audit-first rule; chown -R on the wrong path is a classic incident |

## Special bits

| Bit | On a file | On a directory | Numeric |
|---|---|---|---|
| SUID (`u+s`) | runs as file's owner (root-owned ones = power) | — | `4NNN` |
| SGID (`g+s`) | runs as file's group | **new files inherit the dir's group** | `2NNN` |
| sticky (`+t`) | — | only owner (and root) may delete entries | `1NNN` |

Shared-team directory, the course recipe:
```console
$ sudo chgrp team /srv/project
$ sudo chmod 3770 /srv/project      # SGID + sticky + rwx for group
```
`2770` inherits the group; the extra `1` stops cross-deletion.

## Diagnosing access failures — the order

```console
$ id                        # who am I, what groups
$ ls -l FILE                # which triad should grant me
$ namei -l /srv/deep/path   # every directory on the way
```
Fix the **narrowest** failing subject: membership (`usermod -aG`)
> group bits (`chgrp`+`chmod g+…`) > ACL > ⚠️ never `chmod -R 777`
— it grants everyone write *and erases the original modes*, so the
damage outlives the ticket.

## ACLs (when triads aren't enough)

```console
$ getfacl FILE                          # view
$ setfacl -m u:bob:rx FILE              # grant bob read+execute
$ setfacl -x u:bob FILE                 # revoke
$ setfacl -R -m g:team:rwx /srv/proj    # recursive grant ⚠️ audit first
```
