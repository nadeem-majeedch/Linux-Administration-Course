# Cheatsheet — Unit 4: Users, Permissions, sudo, Environment

## Reading `ls -l` (M12)

```
-rw-r--r-- 1 ada staff  4096 Sep 15 10:00 data.csv
│└┬┘└┬┘└┬┘   └──┬──┘ └─┬─┘
│user group other│     └ group
└ type: - file, d dir, l link
```

- `r` read=4, `w` write=2, `x` execute=1 → `rw-r--r--` = `644`.
- Directory `x` = may enter/traverse. No `x` = no access even with `r`.

## chmod, umask, ownership

```bash
chmod 644 file           # owner rw, others r
chmod u+x script.sh      # add execute for owner
chmod -R g+rX DIR/       # recursive: group read, X = dirs/already-exec only
umask                    # bits REMOVED from new files (022 -> 644/755)
sudo chown user:group file      # change owner and group (admin)
chgrp team file                 # change group (if you own it)
```

## Users & groups

```bash
whoami; id; groups                        # identity
getent passwd ada                         # user record (/etc/passwd fields)
getent group datasets                     # group members (/etc/group)
```

## Shared-directory pattern (M13)

```bash
sudo chgrp -R datasets /srv/team/datasets
sudo chmod -R g+rwX /srv/team/datasets
sudo chmod g+s /srv/team/datasets         # setgid: new files inherit group
setfacl -m u:farid:r-x /srv/team/datasets/shared-metrics   # one extra user
setfacl -d -m g::rwx /srv/team/datasets   # default ACL: inherited by new files
getfacl file                              # audit
```

## sudo (M14)

```bash
sudo -l                  # what may I run as root?
sudo command             # run one command elevated
sudo -i                  # root shell (avoid; prefer per-command)
!!                       # repeat last command with sudo
```

Rules: escalate one command, not a session · read before you paste ·
`sudo` output you own as root (`chown` back) · never edit sudoers except via `visudo`.

## Environment (M15)

```bash
printenv PATH            # show a variable;  env | sort  for all
export EDITOR=vim        # set + pass to children (current shell only)
echo $PATH               # colon-ordered command search dirs
PATH="$HOME/.local/bin:$PATH"    # prepend a dir
alias ll='ls -lah'       # personal shortcuts (in ~/.bashrc)
cp .bashrc .bashrc.bak-$(date +%F)   # ALWAYS back up before editing dotfiles
```
