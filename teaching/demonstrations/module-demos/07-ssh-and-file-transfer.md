# Demo 7 — SSH & File Transfer: Keys, Tunnels, Verified Sync

> **Sessions:** S21–S22 (two natural halves) · **Duration:** ~15 min ·
> **Risk:** low — loopback to the demo VM's own sshd; **lab keys only** ·
> **Objective:** the full remote loop — authenticate by key, forward a
> port, transfer with resume, *verify* with a manifest — as one story.

## Prerequisites

- Demo VM running `sshd` (`sudo systemctl is-active ssh`)
- A **demo keypair** (`~/demo-key`, passphrase-less *for the demo only*
  — say so; students' lab keys are passphrase-protected)
- Your own key in the demo VM's `authorized_keys` (loopback)

## Setup (before class)

```console
$ ssh-keygen -t ed25519 -f ~/demo-key -N "" -C "demo only"
$ ssh-copy-id -i ~/demo-key.pub localhost
$ ssh -i ~/demo-key localhost 'echo authenticated by key'
```

## Procedure — half 1 (S21): keys and tunnels

**Step 1 — watch the key get offered.**

```console
$ ssh -v -i ~/demo-key localhost exit 2>&1 | grep -iE 'offering|accepted'
debug1: Offering public key: /home/dsstudent/demo-key ED25519 ...
debug1: Server accepts key: /home/dsstudent/demo-key ED25519 ...
```

*Narration:* "The *public* part is offered; the server issues a
challenge only the private half can answer. The private key never
crosses the wire — that's the whole security model."

**Step 2 — the tunnel.** Start a web server, reach it through the wall:

```console
$ cd ~/demolab && python3 -m http.server 8000 &>/dev/null &
$ curl -s http://localhost:8000 | head -3      # works locally
$ ssh -L 9999:localhost:8000 -N -f localhost   # forward 9999 → 8000
$ curl -s http://localhost:9999 | head -3      # works *through SSH*
```

*Narration:* "The browser on a laptop does this to reach a Jupyter on a
GPU server — `-L 9999:localhost:8888` is the *actual* weekly workflow of
a data scientist on a remote box."

**Cleanup of this half:** `pkill -f 'http.server 8000'; pkill -f 'ssh -L 9999'`.

## Procedure — half 2 (S22): transfer, resume, verify

**Step 3 — the interrupt-and-resume race.**

```console
$ head -c 200M /dev/urandom > ~/demolab/big.bin
$ rsync -avh --progress --partial ~/demolab/big.bin localhost:~/demolab/
# Ctrl-C after ~5 seconds — narrate the partial file's growth
$ ssh localhost du -h ~/demolab/big.bin        # smaller than 200M
$ rsync -avh --progress --partial ~/demolab/big.bin localhost:~/demolab/
# completes — bytes moved ≪ 200M: it RESUMED
```

*Narration:* "`scp` in the same race restarts at zero — no destination
awareness. rsync's delta check is why week-11-you wins the hotel-Wi-Fi
contest."

**Step 4 — the slash trap, revealed by dry-run.**

```console
$ rsync -avhn ~/demolab localhost:~/demolab/dest/    # would create dest/demolab/
$ rsync -avhn ~/demolab/ localhost:~/demolab/dest/   # contents INTO dest/
```

**Step 5 — verification: the manifest.**

```console
$ (cd ~/demolab && find . -name '*.bin' -exec sha256sum {} +) | sort > local.sha
$ ssh localhost 'cd ~/demolab && find . -name "*.bin" -exec sha256sum {} +' | sort > remote.sha
$ diff local.sha remote.sha && echo "VERIFIED IDENTICAL"
```

*Narration:* "rsync said 'up to date' on size+mtime. The sha256 diff is
a *stronger claim* — content, proven independent of metadata. When the
analysis must be reproducible, the manifest ships with the dataset."

## Expected output

Shapes as shown; hashes/PIDs vary (state it). The `VERIFIED IDENTICAL`
line is the emotional close — let the class read it aloud.

## Questions to ask

1. After step 1: "what would change if the fingerprint changed on a
   *known* host?" (M22's host-key choreography — stop, investigate,
   never ignore)
2. After step 3: "what did scp lack, in one word?" (state)
3. After step 5: "which comparison did rsync use by default, and which
   did we just do?" (size+mtime vs content digest)

## Common errors & recovery

- Port 22 refused on the demo VM → `sudo systemctl enable --now ssh`
  (the M21 rung-1 lesson, live)
- `ssh -L` address already in use → a stale forward from a previous
  run; `pkill -f 'ssh -L 9999'`
- The 200 MB transfer finishes before you can interrupt — bump to
  400M, or throttle `--bwlimit=2m`; rehearse the timing (module lab
  notes have it)

## Recovery

Everything is loopback and disposable; `~/demo-key` removal plus
`authorized_keys` line cleanup ends the demo state:

```console
$ ssh localhost 'sed -i /demo-key/d ~/.ssh/authorized_keys'
```

## Cleanup (census)

```console
$ rm -r ~/demolab && rm ~/demo-key ~/demo-key.pub
$ ssh localhost 'grep -c demo-key ~/.ssh/authorized_keys'   # 0
```

## Optional extension

`rsync --checksum` on the same tree — watch it read every byte; the
cost of the *strongest* claim, made visible in time.
