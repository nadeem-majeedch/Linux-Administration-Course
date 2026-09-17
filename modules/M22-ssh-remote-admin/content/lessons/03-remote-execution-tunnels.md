# Lesson 3 — Remote Execution, File Copying and Tunnels

> Module 22 · Unit 6 · Difficulty: Advanced
> Reading time: ~25 min · Lab: [Lab 2 — diagnosis clinic](../labs/lab-02-diagnosis-clinic.md)
> Up next: [Lesson 4 — tmux & the DS workflow](04-tmux-ds-workflow.md)

---

## 1. One connection, three jobs

Lesson 1 established the login. This lesson uses the same encrypted
channel for the other two jobs: **command transport** (run anything
remotely, get the output) and **tunneling** (make remote services
appear local). File transfer rides along — `scp` and rsync-over-ssh
are SSH connections carrying bytes; the deep rsync treatment is
[M23's](../../../M23-file-transfer/README.md).

Throughout, `vm` is the ssh-config alias from Lesson 2 — evidence
that the config is doing its job.

## 2. Remote commands — the one-liner interface

Appending a command changes `ssh` from shell to pipe:

```console
$ ssh vm 'uptime'                          # run, print, exit
 21:04:11 up 3 days,  load average: 0.10, 0.15, 0.09
$ ssh vm 'df -h /home | tail -1'           # pipelines run remotely
$ ssh vm 'pgrep -af python3 | wc -l'       # is my training running?
```

Semantics that matter:

- **The remote shell does the work.** Quotes keep *your* shell out;
  `'...'` (single) passes the command intact — variables expand
  *remotely*: `ssh vm 'echo $USER'` prints the remote user. Double
  quotes expand **locally first** — occasionally exactly what you
  want (`ssh vm "echo $HOME/.ssh"` sends your path), usually a bug.
  This is [M10's](../../../M10-bash-scripting/content/README.md) quoting
  lesson wearing a network costume.
- **stdout comes back** — pipeable into local tools:
  `ssh vm 'journalctl -u ssh -b --no-pager' | grep -c Accepted`
  (remote journal, local grep — [M24](../../../M24-logs-journald-monitoring/content/README.md)
  at network scale).
- **Exit codes come back** — `ssh vm 'false'; echo $?` → 1. A remote
  failure is *your* script's failure ([M11's](../../../M11-advanced-shell-automation/content/README.md)
  strict mode keeps working across the wire; so do dry-runs and
  guards).
- **stdin flows too** — `ssh vm 'cat > ~/in.csv' < local.csv` pushes
  a file without scp; `ssh vm 'grep ERROR app.log' | less` streams
  remotely-filtered logs to a local pager.

The admin loop this enables — one command, many machines:

```bash
for host in vm; do          # (lab: one host; real fleets: many)
    echo "== $host =="
    ssh "$host" 'systemctl is-active ssh jupyter 2>&1; free -h | head -2'
done
```

Remote **process management** (M18 across the wire): `ssh vm 'pgrep
-af train.py'`, `ssh vm 'pkill -f train.py'` — with the same
preview→scope→TERM→verify ladder, just executed through ssh.
Remote **service** management likewise needs sudo *on the remote
side* (`ssh vm 'sudo systemctl status nginx'` — the sudo password
prompt travels through the same channel).

## 3. scp — the quick copy

```console
$ scp local.csv vm:~/data/            # push: local → remote
$ scp vm:~/results/run1.csv ./        # pull: remote → local
$ scp -r ~/exp vm:~/                  # recursive (directories)
$ scp vm:~/a.csv vm2:~/b.csv          # remote → remote (rare; think first)
```

Syntax shape: `scp source destination`, where either side may be
`[user@]host:path` — the colon is the marker. Under the hood it's
SSH (your config aliases, keys, agent all apply). Its limits: no
resume, no delta transfer, everything re-copied — fine for a
checkpoint file, wrong for a 40 GB dataset that changes daily.

**Permissions travel with intent** ([M12](../../../M12-users-groups-permissions/README.md)
revisited): a file pushed to a shared group directory lands with
*your* umask defaults — collaborators may not be able to read it
until `ssh vm 'chmod g+w ...'` or the setgid directory (M13) does
its thing. The DS scenario: pushing `model.pkl` to the team's
`/srv/models/` and having a teammate's loader fail on permissions —
the M13 clinic, arriving over ssh.

## 4. rsync over ssh — the smart copy

One flag turns rsync remote (`-e ssh` is implied by a host:path
target):

```console
$ rsync -avP ~/exp/ vm:~/exp/           # -a archive, -v verbose, -P progress+resume
$ rsync -avP --delete ~/exp/ vm:~/exp/  # mirror: deletions propagate (--delete care!)
$ rsync -avn --delete ~/exp/ vm:~/exp/  # -n DRY RUN: always narrate first (M11's pattern)
```

Why it wins for datasets: **delta transfer** (only changed blocks
cross the wire — a re-run after one more epoch sends megabytes, not
gigabytes), **resume** (`-P`), **the trailing-slash rule** (`~/exp/`
= *contents of* exp; `~/exp` = the directory itself — the single
most common rsync surprise; M23 drills it), and `--delete`'s
mirroring power with its matching danger — `rsync -n` before every
mirror is the course rule, inherited straight from
[M11](../../../M11-advanced-shell-automation/content/README.md)'s
dry-run doctrine.

The DS rhythm this enables: `rsync -avP results/ vm:~/results/`
after each experiment — *syncing experiment results* as a habit, not
a rescue.

## 5. Port forwarding — tunnels

Some services shouldn't face the network: Jupyter on the GPU server
listens on its loopback (correctly! — M21's bind-scope lesson). You
still need it in your browser. SSH tunnels carry arbitrary TCP
through the encrypted channel.

### Local forwarding — `-L` (the workhorse)

```console
$ ssh -L 8888:localhost:8888 vm -N
```

Read `-L` left to right: **local** port 8888 now forwards, through
the SSH connection, to `localhost:8888` *as seen from the remote
side*. With `-N` (no shell — just the tunnel), your browser opens
`http://localhost:8888` and is talking to the *remote* Jupyter —
which never had to expose itself to any network. The remote service
stays loopback-bound (its security posture unchanged — M21 §3);
the tunnel borrows SSH's authentication and encryption.

The composite DS pattern:

```console
$ ssh -L 8888:localhost:8888 -L 6006:localhost:6006 vm -N
#         ^ Jupyter                       ^ TensorBoard
```

One command, two services, zero exposed ports. (Also `-J jump` —
tunneled *through* the bastion of Lesson 2, because of course it
composes.)

### Remote forwarding — `-R` (the reverse)

`-R 8080:localhost:3000 vm` publishes a service running on *your*
machine to port 8080 *on the remote side* — the "show my local
dev server to the cluster" move, and the standard trick for
callback URLs on compute nodes that can't reach your laptop.
(On the server side, `GatewayPorts` governs whether the forwarded
port binds beyond loopback — an sshd_config reading-level note.)

**Awareness-only:** dynamic forwarding (`-D`, a SOCKS proxy) and
X11 forwarding (`-X`) exist; the course teaches the two workhorses
and names the rest. Every tunnel is still SSH — same keys, same
`known_hosts`, same exit-code discipline — just carrying more.

## 6. Try it now (15 minutes)

1. One-liners: `ssh vm 'free -h | head -2'`,
   `ssh vm 'whoami && hostname'`, and the quoting contrast —
   `ssh vm 'echo $USER'` vs `ssh vm "echo $USER"`. Which expanded
   where?
2. Pipe across the wire: `ssh vm 'grep -c "" /etc/passwd'` (remote
   line count), then push a file via stdin
   (`ssh vm 'cat > ~/from-local.txt' < some-file`).
3. scp a small file to the VM and rsync a directory twice —
   observe rsync's second run transfer *almost nothing* (delta
   transfer, witnessed).
4. The tunnel: start a loopback-bound server on the VM
   (`python3 -m http.server 8000 --bind 127.0.0.1`), then from the
   *host*: `ssh -L 8000:localhost:8000 vm -N` and
   `curl http://localhost:8000` — the remote service, local URL,
   proof in one line of curl output.

## 7. Common mistakes

- Double quotes around remote commands — local expansion precedes
  transmission; single-quote remote commands by default.
- scp `-r` for the big sync — full copies forever; rsync for
  anything repeated.
- rsync's trailing slash — `~/exp/` vs `~/exp` doubles or nests
  your directory. `-n` before every real run.
- Forwarding to `localhost:PORT` from a *third* host — `-L`'s
  target resolves **from the remote side**; "localhost" there means
  the remote machine.
- Leaving `-N` tunnels cluttering terminals — run them deliberately,
  kill them deliberately (the Ctrl+C is the tunnel's whole lifecycle).

> **Up next:** [Lesson 4 — tmux & the DS
> workflow](04-tmux-ds-workflow.md): sessions that survive
> disconnects — the last piece of the remote-workstation loop.
