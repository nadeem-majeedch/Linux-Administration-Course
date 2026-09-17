# 6 — Package Management

> Learn it: [M16 — Package Management](../modules/M16-package-management/content/README.md) ·
> Lookup, not understanding.

## apt — the daily set (Ubuntu/Debian)

| Command | Purpose | Notes |
|---|---|---|
| `sudo apt update` | refresh package **index** | does not upgrade anything; run first |
| `sudo apt upgrade` | upgrade installed packages | read the REMOVED line before `y` |
| `sudo apt full-upgrade` | upgrades that may remove packages | ⚠️ read carefully |
| `apt search TERM` | search names/descriptions | no sudo |
| `apt show PKG` | details, version, deps | no sudo |
| `sudo apt install PKG…` | install | add `--dry-run` to preview |
| `sudo apt remove PKG` | uninstall, keep config | — |
| `sudo apt purge PKG` | uninstall **with** config | ⚠️ removes `/etc` settings |
| `sudo apt autoremove` | drop orphaned dependencies | review list |
| `apt list --installed` | what's here | grep-able |
| `apt list --upgradable` | what update found | — |

Preview habit on production: `apt install --dry-run PKG`, then read
"the following packages will be **REMOVED**" before saying yes.

## dpkg — the low level

| Command | Purpose | Example |
|---|---|---|
| `dpkg -l` | installed packages | `dpkg -l \| grep python3` |
| `dpkg -S FILE` | **which package owns this file** | `dpkg -S /usr/bin/curl` |
| `dpkg -L PKG` | what did that package install | `dpkg -L nginx` |
| `dpkg -I pkg.deb` | inspect a .deb file | before installing it |
| `sudo dpkg -i pkg.deb` | install a .deb | ⚠️ does **not** resolve dependencies — follow with `sudo apt -f install` if it complains |

Status codes in `dpkg -l`: first char `ii` = installed fine,
`rc` = removed but config remains (`purge` clears it).

## Repositories — where packages come from

| File/path | Role |
|---|---|
| `/etc/apt/sources.list` + `sources.list.d/` | repository URLs & suites |
| `/etc/apt/keyrings/` | signing keys (referenced by `signed-by`) |
| suites | `noble` (release) · `noble-updates` · `noble-security` — the security suite is what unattended-upgrades uses |

```console
$ sudo apt edit-sources        # edit with validation
$ apt policy PKG               # which repo would provide which version
```

⚠️ **PPAs & random repos**: a PPA is one person's apt repo. Adding
one runs their maintainer scripts as root at install/upgrade and
points your update pipeline at their goodwill. Prefer official
Ubuntu repos; for ML packages prefer pip/conda *in environments*
over system PPAs.

## Security updates

```console
$ sudo apt update && apt list --upgradable
$ sudo unattended-upgrade          # the tool Ubuntu automates with
$ cat /var/log/unattended-upgrades/unattended-upgrades.log
```
`unattended-upgrades` package ships enabled for the `-security`
suite on Ubuntu Server.

## Other families (concept map)

| World | Frontend | Low-level |
|---|---|---|
| Debian/Ubuntu | apt | dpkg (.deb) |
| RHEL/Fedora | dnf | rpm (.rpm) |
| Arch | pacman | pacman |
| openSUSE | zypper | rpm |

Translation: `apt install` ↔ `dnf install`; `dpkg -S` ↔ `rpm -qf`;
`apt search` ↔ `dnf search`.

## Where source builds fit

```console
$ ./configure --prefix=/usr/local    # FHS default keeps your build out of apt's way
$ make
$ sudo make install                  # only this step needs root in the default flow
$ sudo apt remove …                  # apt cannot uninstall it — dpkg/apt don't track it
```
Prefer `--prefix=$HOME/.local` on shared machines: no sudo, and
your build stays yours.

## The apt / pip / conda division (course rule)

apt owns the OS and system libraries. pip/conda own language
packages **inside environments**. PEP 668 (`externally-managed`) is
Ubuntu protecting apt-owned system Python from pip — the fix is a
virtualenv, never `--break-system-packages` as a habit.
