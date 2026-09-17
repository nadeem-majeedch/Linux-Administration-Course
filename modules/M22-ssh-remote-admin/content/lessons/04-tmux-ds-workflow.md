# Lesson 4 — tmux and the Data-Science Remote Workflow

> Module 22 · Unit 6 · Difficulty: Advanced
> Reading time: ~20 min · Lab: [Lab 1](../labs/lab-01-key-workflow.md) ties it together
> Up next: [Mini-Project D — remote compute workstation](../mini-project-d-remote-compute-workstation.md)

---

## 1. The 3 AM problem

You SSH to the GPU server, start training, go home. Your laptop
sleeps → the SSH connection drops → and with it, usually, everything
attached to that session: the shell sends SIGHUP to its jobs
([M18's](../../../M18-processes-jobs-signals/content/README.md) signal
table, arriving in real life), the training dies mid-epoch. `nohup`
(M18) keeps *one* process alive — but no interaction, no reattach,
no watching the loss curve from bed.

**tmux** (terminal multiplexer) solves it properly: it runs a
*server* on the remote machine that owns terminals independently of
any SSH connection. Detach, disconnect, reboot your laptop — the
sessions, their programs, and their scrollback live on the server.
Reconnect tomorrow and `tmux attach` resumes the scene exactly.

```
your laptop                     GPU server (the VM)
┌──────────┐    SSH (droppable)  ┌──────────────────────────┐
│ terminal │◄───────────────────►│ tmux server              │
└──────────┘                     │  ├─ session: train       │
       ▲                         │  │   └─ python train.py  │  ← survives disconnects
       └──── detach / reattach ──│  └─ session: monitor     │
```

## 2. tmux in one table

```console
$ tmux new -s train          # new session named "train"
$ tmux ls                    # list sessions
$ tmux detach                # (or Ctrl-b d) — leave it running
$ tmux attach -t train       # return later — even from another machine
$ tmux kill-session -t train # clean up when done
```

Inside a session, the **prefix** `Ctrl-b` introduces commands:

| Keys | Action |
|---|---|
| `Ctrl-b d` | detach (the session keeps running) |
| `Ctrl-b c` | new *window* (tabs, per project) |
| `Ctrl-b n` / `p` | next / previous window |
| `Ctrl-b ,` | rename window |
| `Ctrl-b %` / `"` | split pane vertically / horizontally |
| `Ctrl-b arrows` | move between panes |
| `Ctrl-b [` | **scrollback mode** (arrows/PgUp; `q` to exit) |
| `Ctrl-b ?` | key list |

Two of these carry disproportionate value: **detach** (the whole
point) and **scrollback** — remote terminals that lost history
every reconnect now keep thousands of lines, greppable in copy mode.
The [M09](../../../M09-pipes-and-redirection/README.md)/M08
habits still apply where it counts: pipe program output to files;
tmux scrollback is for *reading*, not for analysis.

## 3. The durable-session pattern

The workflow that survives every disconnect, rehearsed until boring:

```console
$ ssh vm
$ tmux new -s train
$ python3 train.py 2>&1 | tee logs/train_$(date +%F).log
# ... watch the first epochs ...
Ctrl-b d                                    # detach; exit ssh freely
$ exit                                      # connection closes; training continues

# ...next morning, anywhere:
$ ssh vm
$ tmux attach -t train
#   → same window, same running job, scrollback intact
```

`tee` (M09) keeps the log file growing regardless of tmux — belt and
suspenders: the session survives disconnects; the log survives even
a crashed VM. For unattended *fire-and-forget* runs, `nohup` remains
legitimate (M18); for anything you'll *return to interactively*,
tmux is the tool. The pairing rule: **tmux for work you rejoin;
nohup for work you don't.**

## 4. The full DS remote-workstation loop

Every piece now exists — assembled, this is the daily loop on every
compute server you'll ever use:

```console
# 1. Connect (keys + config alias — Lessons 1–2)
$ ssh vm

# 2. Durable session
$ tmux new -s jupyter

# 3. Start the service loopback-bound (M21's bind discipline)
$ jupyter notebook --no-browser --port=8888
    → paste the tokened URL somewhere safe; note the port

# 4. Detach; the notebook server lives on
Ctrl-b d

# 5. From the laptop: tunnel to it (Lesson 3)
$ ssh -L 8888:localhost:8888 vm -N
    → browser: http://localhost:8888  ← the REMOTE notebook

# 6. Work; datasets flow via rsync when needed
$ rsync -avP ~/datasets/big/ vm:~/data/big/

# 7. Results flow home, delta-compressed
$ rsync -avP vm:~/experiments/run42/ ~/experiments/run42/
```

Steps 5–7 are the module's DS scenarios made concrete: **remote
Jupyter** without exposing a port, **remote datasets** pushed
delta-style, **experiment results** synced home. Transferring
*models* is the same rsync line pointed at a checkpoint file —
with one [M13](../../../M13-ownership-shared-access/content/README.md)
afterthought: a model landing in a shared `models/` directory may
need `ssh vm 'chmod g+r models/run42.pkl'` before teammates can
load it.

Multi-server reality (the lab's `gpu*` + `jump` config from Lesson
2): the loop is identical per host; the config abstracts the
plumbing.

## 5. Try it now (10 minutes)

1. The survival demo: `tmux new -s test`, start
   `bash -c 'while true; do date; sleep 5; done'`, detach, close the
   terminal *entirely*, reopen, `tmux attach -t test` — the clock
   never stopped. That's the whole value proposition, witnessed.
2. Windows and panes: in `test`, `Ctrl-b c` (window 2), split with
   `"`, `Ctrl-b arrows` to move. Run `htop` in one pane, `watch -n2
   date` in another — a two-pane monitoring session.
3. Scrollback: flood a pane (`seq 1 1000`), `Ctrl-b [`, navigate,
   `q`. Now that history exists *after* reconnecting too.
4. Cleanup: `tmux kill-session -t test` — sessions are processes
   (M18: they're yours to manage); leaving dozens of stale sessions
   on a shared server is the remote equivalent of leaving
   `sleep 99999` running.

## 6. Common mistakes

- Confusing tmux with `nohup`: nohup detaches *output* from a
  terminal; tmux detaches *terminal* from a connection. Different
  problems, different tools.
- Working *without* tmux on remote machines out of habit — the
  first dropped-VPN-training-run fixes that permanently; make the
  reflex pre-emptive.
- Session sprawl: `tmux ls` showing `train`, `train2`, `tmp`,
  `work-old` — name sessions by project and kill them when done.
- Losing the tokened Jupyter URL — it's in the scrollback *and*
  should be in the run log (`tee`, §3). Screenshot-free recall is
  a habit, not luck.
- Killing the *SSH* connection expecting the job to stop — it
  doesn't; that's the feature. To actually stop work: detach, then
  kill the process deliberately (M18's ladder, through ssh).

> **Next:** [Mini-Project D — remote compute
> workstation](../mini-project-d-remote-compute-workstation.md)
> packages Lessons 1–4 into a documented, runnable setup — then
> [M23](../../../M23-file-transfer/README.md) goes deep on the file
> transfer leg.
