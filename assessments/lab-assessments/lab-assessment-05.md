# LA-5 — Remote Workstation Drill (30 min)

> Assesses: M22 + M31 labs · 10 points · evidence transcript
> required. Environment: student's own VM acts as the "remote ML
> server"; laptop (or second shell) is the client. Instructor
> spot-checks the *client-side* config at the end.

## Tasks

**T1 (3).** Establish key-only SSH from client to the VM: Ed25519
key (new or existing), `authorized_keys` installed with correct
permissions, and a `~/.ssh/config` alias `mlsrv` so that
`ssh mlsrv uptime` works **without any password prompt**. Prove with
the command and its output.

**T2 (3).** Over that session: create `~/mlsrv-demo/` on the VM,
place a small `train.py` (stdout prints one line every 2 seconds ×
10), and launch it with `nohup` **disconnected from the terminal**
— prove it survives your logout by reconnecting and showing the
process + its log growing.

**T3 (2).** From the client, open an SSH tunnel and show a browser
or `curl` reaching a service on the VM through `localhost`
(`python3 -m http.server 9999` on the VM is the standard stand-in).
Proof: the `curl` output *from the client side*.

**T4 (2).** Sync a directory from client to VM with `rsync`,
*modify one file locally*, re-run the sync, and show from rsync's
output that only the changed file was transferred.

## Rubric

| Points | Requirement |
|---|---|
| 1 | T1 key type Ed25519 (or correctly justified RSA) |
| 1 | T1 server-side perms `~/.ssh` 700 / `authorized_keys` 600 shown |
| 1 | T1 `ssh mlsrv uptime` output with no prompt visible |
| 1 | T2 job launched with `nohup … &` (or `tmux`/`setsid`) and *proven* alive after reconnect (`ps` + growing log) |
| 1 | T2 log file path stated and shown growing |
| 1 | T3 tunnel form correct (`-L 9999:localhost:9999`) and client-side curl proof |
| 1 | T4 rsync `-av` style output naming the one transferred file on re-run |
| 1 | T4 target/paths correct (no `//` traps, trailing-slash semantics respected) |
| 1 | Transcript shows *both* sides (client commands and VM proof) |
| 1 | No password ever typed after T1 completes (visible in transcript) |

## Common failures

- Password used "just this once" mid-drill — that resets T1 to 0;
  the whole objective is key-only operation.
- T2 job killed by session end because it was backgrounded with `&`
  alone (no `nohup`/`tmux`) — the reconnect proof catches it.
- T4 syncing with `-n` still active and declaring victory — dry-run
  output is *not* a transfer.
