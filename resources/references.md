# References — Official Documentation

Curated, primary-source links only. Where a tool has a manual page, the man page on
your own system is the most authoritative source for your exact version: `man <command>`.

## General Linux

- **Ubuntu documentation** — <https://documentation.ubuntu.com/>
- **Ubuntu Server documentation** — <https://documentation.ubuntu.com/server/>
- **The Linux man-pages project** — <https://www.kernel.org/doc/man-pages/>
- **The Linux Kernel documentation** — <https://docs.kernel.org/>
- **GNU Coreutils manual** (ls, cp, mv, rm, chmod, sort, …) —
  <https://www.gnu.org/software/coreutils/manual/>
- **Filesystem Hierarchy Standard** — <https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html>

## Unit 1–2 (Foundations, Command Line)

- **GNU Bash manual** — <https://www.gnu.org/software/bash/manual/>
- **GNU Grep manual** — <https://www.gnu.org/software/grep/manual/>
- **GNU Sed manual** — <https://www.gnu.org/software/sed/manual/sed.html>
- **Gawk (GNU awk) manual** — <https://www.gnu.org/software/gawk/manual/>
- **GNU Findutils** (find, xargs) — <https://www.gnu.org/software/findutils/manual/>
- **Vim documentation** (course text editor) — <https://www.vim.org/docs.php>
- **nano documentation** — <https://www.nano-editor.org/docs.php>

## Unit 3–4 (Scripting, Administration)

- **ShellCheck** (script linter) — <https://www.shellcheck.net/> and
  <https://github.com/koalaman/shellcheck>
- **sudo manual** — <https://www.sudo.ws/docs/man/sudo.man/>
- **ACL (setfacl/getfacl) man pages** — on your system: `man setfacl` (POSIX ACLs
  for Linux are documented in the acl package man pages)

## Unit 5 (Packages, Storage, Processes, Scheduling)

- **Debian apt documentation** (Ubuntu's package tooling) —
  <https://wiki.debian.org/Apt> and `man apt`, `man sources.list`
- **Ubuntu community docs: apt** — <https://help.ubuntu.com/community/AptGet/Howto>
- **System administration guide (Ubuntu Server)** —
  <https://documentation.ubuntu.com/server/server-administration/>
- **GNU tar manual** — <https://www.gnu.org/software/tar/manual/>
- **procps** (ps, top, kill, …) — `man ps`, `man top`; procps upstream:
  <https://gitlab.com/procps-ng/procps>
- **systemd-cron/timer references:** see systemd section below

## Unit 6 (systemd, Networking, SSH, Logs, Security)

- **systemd documentation** — <https://systemd.io/> and on-system `man systemd.unit`,
  `man systemd.service`, `man systemd.timer`, `man journalctl`
- **iproute2** (ip, ss) — `man ip`, `man ss`
- **OpenSSH manual** — <https://www.openssh.com/manual.html> and `man ssh`,
  `man ssh_config`, `man sshd_config`
- **rsync manual** — <https://download.samba.org/pub/rsync/rsync.html> and `man rsync`
- **ufw (Uncomplicated Firewall)** — <https://launchpad.net/ufw> and `man ufw`
- **Ubuntu Server security guide** —
  <https://documentation.ubuntu.com/server/how-to/security/>
- **journald / logrotate** — `man systemd-journald`, `man logrotate`

## Unit 7 (Data Science Stack)

- **Git documentation** — <https://git-scm.com/doc> (the Pro Git book is free:
  <https://git-scm.com/book>)
- **Python documentation** — <https://docs.python.org/3/>
- **venv tutorial** — <https://docs.python.org/3/tutorial/venv.html>
- **pip documentation** — <https://pip.pypa.io/en/stable/>
- **Jupyter documentation** — <https://docs.jupyter.org/>
- **Docker documentation** — <https://docs.docker.com/> (Engine install for Ubuntu:
  <https://docs.docker.com/engine/install/ubuntu/>)
- **PostgreSQL documentation** — <https://www.postgresql.org/docs/>
- **nginx documentation** — <https://nginx.org/en/docs/>
- **scikit-learn documentation** — <https://scikit-learn.org/stable/documentation.html>
- **pandas documentation** — <https://pandas.pydata.org/docs/>
- **NVIDIA driver + CUDA for Ubuntu** (GPU awareness) —
  <https://documentation.ubuntu.com/server/how-to/software/nvidia-drivers/>

## Keeping versions honest

Docs move; commands change defaults. Course rules:

1. When docs and this course disagree, **check your own man page first** — it matches
   your installed version, then file an issue (CONTRIBUTING.md).
2. Ubuntu-specific pages above are for **Ubuntu LTS**; other distros have their own
   equivalents (Debian wiki, Fedora docs, Arch Wiki are good but not the course's
   primary sources).
3. Never trust a tutorial that tells you to bypass package management or disable
   security controls "to make it work" — including ours; if we err, we want the issue.
