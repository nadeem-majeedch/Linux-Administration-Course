# 5 — Processes

> Learn it: [M18 — Processes, Jobs & Signals](../modules/M18-processes-jobs-signals/content/README.md) ·
> Lookup, not understanding.

## Looking

| Command | Purpose | Important options | Example |
|---|---|---|---|
| `ps` | snapshot of processes | `aux` all+detail · `-ef` full format · `-u USER` mine | `ps aux --sort=-%mem \| head` |
| `top` | live view | `P` CPU sort · `M` memory · `k` kill · `q` quit | `top` |
| `htop` | better live view | F6 sort · F9 kill · `/` filter | `htop -u ana` |
| `pgrep` | find PIDs | `-a` show cmdline · `-f` match full cmdline · `-u USER` | `pgrep -af train.py` |
| `pstree -p PID` | process tree | `-p` show PIDs | see a launcher's children |
| `uptime` | load averages | — | decode vs core count |

⚠️ The identify-first rule: **`pgrep -af PATTERN` before every
`pkill -f PATTERN`** — matching by full command line can catch
innocent bystanders (`pkill -f train.py` matches `tail -f
train.log`).

## Killing / signaling

| Signal | Name | Meaning |
|---|---|---|
| 15 | SIGTERM | polite: "finish and exit" — **default of `kill`** |
| 2 | SIGINT | your `Ctrl+C` |
| 1 | SIGHUP | "terminal gone"/reload convention |
| 9 | SIGKILL | cannot be caught; last resort only |

```console
$ kill PID                 # SIGTERM
$ kill -TERM PID           # explicit
$ kill -9 PID              # ⚠️ SIGKILL — only after TERM failed
$ pkill -u $USER -f NAME   # scoped by user+pattern
$ killall NAME             # by exact name ⚠️
```
Order of escalation: TERM → wait → TERM again → `kill -9`, and only
on processes you own.

## Jobs (in one shell)

| Command | Purpose |
|---|---|
| `CMD &` | start in background |
| `Ctrl+Z` | suspend current job |
| `jobs` | list shell's jobs |
| `bg %N` / `fg %N` | resume in background/foreground |
| `nohup CMD &` | survive logout; output → `nohup.out` |
| `disown %N` | detach an already-running job |

## Survival beyond the terminal

| Tool | Use | Notes |
|---|---|---|
| `tmux` / `screen` | persistent session | `tmux new -s work`, detach `Ctrl+b d`, resume `tmux attach -t work` |
| `systemd` user unit | real service management | survives logout with `loginctl enable-linger` (M20) |

## Priority

```console
$ nice -n 10 make train        # start kind (higher n = lower priority)
$ renice -n 5 -p PID           # ⚠️ lowering nice of a running proc needs root
$ ionice -c3 -p PID            # idle-class disk access
```
Only root may *increase* priority (lower the nice value).

## Reading top's summary rows

| Field | Means |
|---|---|
| `us sy ni id wa st` | user / kernel / niced / idle / **waiting on I/O** / stolen time — high `wa` = disk-bound, not CPU-bound |
| load avg | runnable + uninterruptible tasks — divide by cores; sustained > cores needs a look |
| `%MEM` / VIRT vs RES | RES is the honest footprint; VIRT includes mappings you may never touch |
