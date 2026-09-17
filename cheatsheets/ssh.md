# 11 — SSH

> Learn it: [M22 — SSH & Remote Administration](../modules/M22-ssh-remote-admin/content/README.md) ·
> Lookup, not understanding.

## Connecting

| Command | Purpose | Examples |
|---|---|---|
| `ssh USER@HOST` | log in | `ssh ana@gpu01.cs.uni.edu` |
| `ssh HOST` | uses config alias / current username | `ssh mlsrv` |
| `ssh -p PORT HOST` | non-default port | `ssh -p 2222 vm` |
| `ssh -v HOST` | verbose (the diagnostic) | `-vv` for deeper |
| `ssh HOST CMD` | run one command, exit | `ssh mlsrv 'uptime'` |

## Keys — the course standard

```console
$ ssh-keygen -t ed25519                       # one pair per machine/role
$ ssh-copy-id USER@HOST                       # install the public half
$ ssh -i ~/.ssh/id_ed25519 USER@HOST          # explicit key (if needed)
```

| File | Must be | Holds |
|---|---|---|
| `~/.ssh/` | `700` | everything ssh |
| `~/.ssh/id_ed25519` | `600` | **private** key — never leaves the machine |
| `~/.ssh/id_ed25519.pub` | `644` | public half — goes on servers |
| `~/.ssh/authorized_keys` | `600` | public keys allowed IN (server side) |

Wrong permissions are the #1 "my key is right but it asks for a
password" cause — sshd silently refuses loose keys.

## `ssh-agent` — don't retype passphrases

```console
$ eval $(ssh-agent)
$ ssh-add ~/.ssh/id_ed25519
$ ssh-add -l        # loaded keys
```

## `~/.ssh/config` — write it once

```text
Host mlsrv
    HostName gpu01.cs.uni.edu
    User ana
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60      # keep long sessions alive
```
Now `ssh mlsrv`, `scp … mlsrv:`, `rsync … mlsrv:` all just work.
First connection stores the host key; a **changed host key warning
means the server changed** — verify out-of-band before accepting
(mitM detection, not an error to autoskip with
`-o StrictHostKeyChecking=no` ⚠️).

## Moving files

| Command | Purpose | Examples |
|---|---|---|
| `scp FILE HOST:PATH` | copy up | `scp model.pkl mlsrv:~/runs/` |
| `scp HOST:PATH FILE` | copy down | `scp mlsrv:results.csv .` |
| `scp -r DIR HOST:PATH` | recursive | — |
| `sftp HOST` | interactive (get/put/ls) | type `help` inside |
| `rsync -av SRC HOST:PATH` | **sync** — deltas, resumes, preserves | `rsync -av --progress data/ mlsrv:backup/` |
| `rsync -avz --delete SRC HOST:PATH` | mirror | ⚠️ `--delete` removes extras at the target — dry-run with `-n` first |

Trailing-slash semantics: `src/` = contents; `src` = the directory
itself. The most common rsync surprise.

## Tunnels — reach loopback services

| Form | Effect | Use |
|---|---|---|
| `ssh -L 9999:localhost:8888 HOST` | local:9999 → host's 8888 | reach Jupyter bound to 127.0.0.1 on the server |
| `ssh -L 5432:localhost:5432 HOST` | tunnel a DB port | psql "as if local" |
| `ssh -D 1080 HOST` | SOCKS proxy | browsing via the server |

Client connects to `localhost:9999`; the server-side hop is
**ssh-authenticated** — this is why services stay bound to loopback
on shared machines.

## Server-side hardening (what you'll be asked to do)

| Where | What |
|---|---|
| `/etc/ssh/sshd_config` + `sshd_config.d/` | policy drop-ins |
| `PasswordAuthentication no` | key-only (scope per-user via `Match` blocks where possible) |
| `PermitRootLogin no` | never SSH as root directly |
| validate | `sudo sshd -t` before restarting sshd |
| rollback | keep the exact change + its inverse in your runbook — a hardening step without a rollback path is a lock without a key |

⚠️ Editing sshd from a remote session: keep your current session
open, test a **new** login before logging out.

## Failure triage with `ssh -v`

1. Which key was *offered*? (`debug1: Offering public key: …`)
2. Which methods does the server allow? (`Authentications that can
   continue: publickey,password`)
3. Permission denied after offering ⇒ server-side
   `authorized_keys`/permissions/config audit — the client did its
   job.
