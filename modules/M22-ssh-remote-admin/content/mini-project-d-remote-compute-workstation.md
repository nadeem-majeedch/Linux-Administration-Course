# Mini-Project D — Remote Compute Workstation

> Module 22 · Unit 6 · Difficulty: Advanced
> Deliverables: working setup + `runbook.md` + `setup-proof.md`
> Prerequisites: both [M22 labs](labs/README.md); M20 (user services);
> M21 (the ladder); M18 (process discipline)
> ⚠️ Scope: your own VM as the "remote" machine; host as the client.
> Lab keys only. sshd_config is read (C9-style review), not modified —
> hardening is applied in M25, and the runbook notes where.

By the end, *everything* you do on the VM happens over SSH, by
alias, with keys — and the whole setup is documented well enough
that a teammate could reproduce it from your runbook alone. This is
the daily pattern on university GPU servers, rehearsed until it's
boring.

## Part 1 — the setup (working, evidenced)

1. **Keys:** the `lab_vm` pair from Lab 1 (or a fresh pair if you
   prefer), agent-loaded, `IdentitiesOnly`, passwordless verified
   from a cold terminal.
2. **Config:** `~/.ssh/config` with `vm` alias *and* a second alias
   (`vm-alt`) using a second key to a second user (C3's pattern) —
   demonstrating multi-key discipline.
3. **The service:** a user unit (M20) running a loopback-bound
   "compute" service — `python3 -m http.server 8888 --bind
   127.0.0.1` behind `systemctl --user enable --now compute.service`
   (the unit file from M20's lab, port changed). It must survive
   reboot (`loginctl enable-linger` if you want the M20 depth —
   optional, note it).
4. **The tunnel pattern:** a documented one-liner
   (`ssh -L 8888:localhost:8888 vm -N`) plus its curl verification.

## Part 2 — the tmux loop (working, evidenced)

Demonstrate the full cycle from [Lesson 4](lessons/04-tmux-ds-workflow.md):

- `tmux new -s compute` → start a long-ish job (`bash -c 'for i in
  $(seq 1 60); do date; sleep 5; done' | tee compute.log`) → detach
  → close the SSH connection *entirely* → reopen → attach → job
  still running, scrollback intact.
- The disconnect test: kill the SSH connection *mid-job* (not
  gracefully — `pkill -f "ssh.*vm"` from the host), then reattach:
  the job never noticed. Screenshot-equivalent: the log's timestamps
  prove continuity.

## Part 3 — `runbook.md` (the graded document)

A one-page operations runbook a teammate could follow cold. Required
sections:

1. **Connect** — exact commands (alias-based), what healthy looks
   like (the "connected as" line), what failure looks like (which
   troubleshooting entry applies).
2. **Work** — the tmux loop, the service start/stop, the tunnel.
3. **Transfer** — the two rsync lines (push datasets, pull results)
   with the `-n`-first rule stated.
4. **Recover** — the three failure plays from
   [troubleshooting.md](troubleshooting.md) you actually rehearsed:
   password-prompt (permissions check), host-key-changed (verify →
   `-R` → re-accept), tunnel-dead (check service, not tunnel).
5. **Limits** — what this setup does NOT do (no sshd hardening yet —
   M25; no jump host in the lab — the config block exists but points
   at localhost; keys are lab keys, not identities).

## Part 4 — `setup-proof.md` (the evidence file)

Transcripts, each with the command and its output: `ssh -G vm` for
both aliases; `ssh-add -l`; the passwordless connect; `systemctl
--user status compute.service`; the tunnel + curl; the disconnect
test's log timestamps; the recover play you performed (pick one,
rehearse it for real).

## Grading (20 pts)

| Item | Pts |
|---|---|
| Setup: keys, config ×2 aliases, service, tunnel — all evidenced | 6 |
| tmux loop incl. the hostile-disconnect test | 4 |
| Runbook: five sections, teammate-cold-start plausible | 6 |
| Evidence file: complete, verbatim outputs | 3 |
| `shellcheck`-clean *if* any scripts were written for the setup (e.g. a `tunnel-up` helper) | 1 |

## Where this leads

M23 deepens the transfer leg (SFTP, rsync mastery); M25 applies the
sshd hardening your runbook's "Limits" section promised; M27's
Python/Jupyter module assumes this workstation exists; and the
capstone's deployment chapter is this runbook with real stakes.
The habit it leaves you with: **remote work is documented work** —
if it isn't in the runbook, it didn't happen.
