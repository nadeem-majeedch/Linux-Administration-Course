# Mini-Project D — Remote Compute Workstation (M22)

> Module: M22 — SSH and Remote Administration · Unit 6 · Difficulty: Advanced
> Prerequisites: M20, M21, M22 in progress; your VM is the "remote" machine

## Brief

Set up and document a complete remote workstation workflow — the daily pattern on
university GPU servers — using your VM as the remote host and your physical machine
as the client. By the end, everything you do on the VM happens *over SSH*.

## Deliverables

1. **Working SSH setup, evidenced:**
   - Ed25519 key pair, passphrase-protected, agent-backed (show `ssh-add -l` output)
   - `~/.ssh/config` with two aliases: `dslab` (direct) and `dslab-tunnel`
     (same host plus the local forward from item 2)
   - passwordless login demonstrated in a terminal transcript
2. **A working tunnel:** local port forward from the client to a service on the VM
   (the `hello.service` user unit from M20, or the Jupyter instance from M27) —
   screenshot/transcript of the service reached via `localhost` on the client.
3. **tmux workflow transcript:** start a long job inside tmux over SSH, detach,
   close the SSH session entirely, reconnect, reattach, show the job kept running.
4. **`runbook.md`** — the operator document (this is graded heavily):
   - connect (with and without the alias)
   - check a service's health and read its logs
   - deploy a file (scp) and restart the service
   - recover: agent not loaded, wrong key permissions, host-key warning explained
     (what it means, what to check, what to *never* do blindly)
   - cleanup: how to revoke a key properly

## Constraints

- All against your own VM. Password authentication is left enabled on the VM in this
  project (M25 changes that); the runbook notes where hardening will land.
- No keys in the repo. The runbook must reference key *fingerprints*, never key
  material, and `.gitignore` must cover `*.pem`, `id_*`, `.env` (already in the
  course root `.gitignore`).
- `shellcheck` clean for any helper scripts you add.

## Rubric

| Criterion | Weight |
|---|---|
| Working key-based SSH + config aliases (evidence) | 25% |
| Tunnel demonstrated end to end | 15% |
| tmux persistence demonstrated | 15% |
| Runbook quality: could a classmate operate your VM from it alone? | 35% |
| Hygiene: no secrets, correct .gitignore, clean history | 10% |

## Stretch goals

- Add a second host entry using `ProxyJump` through a third machine (another VM).
- Add `ServerAliveInterval` and explain what problem it solves.
- Script the "morning routine": one command that connects, checks the service, and
  opens tmux (or starts it).
