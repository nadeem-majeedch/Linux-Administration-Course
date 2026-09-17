# Module 22 Quiz — Answer Key

> Reasoning graded; commands on "would it work if typed".

## Section A — keys & authentication

**A1.** The **public** key goes to `authorized_keys`; the private
key never leaves your machine. Security holds because possession of
the public half lets you *verify* challenges but not *answer* them —
only the private key can sign, and it never transmits.

**A2.** `-t`: algorithm (ed25519 — modern, fast, compact). `-C`:
comment for human identification. `-f`: output path. `lab_vm` (no
suffix) is the private key; `lab_vm.pub` the public.

**A3.** 644 = group/other-readable — any account or process on the
machine could read your identity. sshd treats that as a compromised
key and refuses it. It's M12/M17's permission model enforced by a
protocol: the file's *mode* is part of the key's security.

**A4.** Passphrase: encrypts the private key **at rest** — a stolen
file without the passphrase is useless. Agent: holds decrypted keys
in memory for the session — the passphrase is typed once per
session, not per connection.

**A5.** The tool handles: (1) creating `~/.ssh` with mode 700 if
missing; (2) `authorized_keys` mode 600; (3) de-duplication and
correct ownership. The bare pipe routinely creates the dir with the
umask default (often 755) — which sshd then ignores.

**A6.** `~/.ssh/known_hosts`; first entry follows **TOFU** (trust on
first use). A changed key must be verified **out-of-band** (console,
admin, the rebuild you just did) *before* `ssh-keygen -R` +
re-accept.

**A7.** Causes: (1) the key file was deleted/moved/renamed locally,
(2) its permissions changed, (3) the agent lost it. Distinguisher:
`ls -l ~/.ssh && ssh-add -l` — file present with 600? agent holds
it? (If both fine, it's server-side — check `authorized_keys`.)

## Section B — config

**B8.** `IdentityFile` — client. `PasswordAuthentication` — server.
`HostName` — client. `PermitRootLogin` — server.

**B9.**
```sshconfig
Host gpu01
    HostName 10.0.0.51
    User ds
    IdentityFile ~/.ssh/lab_vm
    ProxyJump jump
```

**B10.** It stops the client from offering *every* agent-loaded key
in turn — servers count repeated offers as brute-force-ish and
some `MaxAuthTries` failures lock you out; with many keys loaded,
`IdentitiesOnly yes` makes per-host key choice deterministic.

**B11.** The **effective, merged** configuration for that alias
(after Host-block precedence and wildcards). One command diagnoses
"wrong port/user/key" config bugs — it prints what the client will
actually do.

**B12.** `prohibit-password`: root may log in **only with a key**,
never a password. The course still prefers `no`: with keys deployed
for every real user, root needs no direct SSH at all — log in as
yourself, `sudo` for privilege (audit trail per M14), and the
most-targeted account name becomes unreachable.

## Section C — execution, copying, tunnels

**C13.** Single quotes: the *remote* shell expands `$USER` → the
remote user. Double quotes: your shell expands **first** → your
local `$USER` is sent. Default to single quotes for remote
commands.

**C14.** The remote command failed with status 3 (its own code,
transported faithfully) — the SSH channel returns the remote exit
status, so automation over ssh inherits strict-mode behavior:
`set -e` scripts stop on remote failures instead of sailing on.

**C15.** scp: one-shot, small, simple (no resume/delta). rsync:
repeated/large/sync-like transfers (delta transfer, `-P` resume,
`-n` dry-run, `--delete` mirroring).

**C16.** First: contents of `~/exp` → into `~/exp/` on the remote
(trees align). Second: the *directory* `~/exp` itself → `~/exp/exp`
on the remote (nesting surprise). The slash is the whole meaning.

**C17.** `-L`: local forwarding. First `8888`: the port opened on
**your** machine. `localhost:8888`: the destination — resolved
**from the remote side**, i.e. the *remote* loopback where Jupyter
listens. `-N`: no remote shell — tunnel only.

**C18.** (1) The service stays loopback-bound — unreachable to
attackers, unchanged security posture; the tunnel adds SSH's
authentication/encryption instead of the app's. (2) No firewall
holes, no server-wide exposure decisions, and the access is
per-user revocable (kill the tunnel) rather than a standing
configuration change.

## Section D — tmux & safety

**D19.** nohup: detaches a *process* from the closing terminal —
output kept, interaction gone. tmux: detaches *terminals* from the
connection — full sessions, scrollback, reattach. Rule: **tmux for
work you rejoin; nohup for fire-and-forget.**

**D20.** Detaches — the session (and its processes) keep running
server-side. From another machine: `ssh vm; tmux attach -t <name>`
(or `tmux ls` first if the name is forgotten).

**D21.** Two sessions **before** changing sshd auth settings: one
to apply/test, one *already-authenticated* as the escape hatch if
the new config locks you out (plus the VM console as the final
backstop). The rule exists because a typo in that file can end
SSH access entirely.

**D22.** Any four: private keys never leave your machine / never
enter repos; `600` private, `700` `~/.ssh`; passphrase per key;
separate keys per context (lab ≠ personal ≠ work); a key is an
identity — revoke by removing the `authorized_keys` line.

## Bonus (Q23) — model answer

1. `ssh gpu01` (via jump — config did the plumbing) — *reachability
   + authentication checked before committing hours*.
2. `tmux new -s train` — *disconnect-protection; the session will
   outlive the SSH connection*.
3. `python3 train.py 2>&1 | tee logs/train_$(date +%F).log` —
   *output survives even a VM crash; the run is auditable*.
4. `Ctrl-b d` then `exit` — *detach deliberately; verify it detached
   before leaving* (a quick `tmux ls` confirms the session lives).

(The rsync of results *after* — not before — is the M23 lesson; the
morning checklist's point is: nothing irreversible happens outside
tmux.)

## Score guide

| Score | Meaning |
|---|---|
| 20–23 | Ready for Mini-Project D |
| 15–19 | Re-read flagged sections; redo the matching clinic patient |
| < 15 | Repeat lessons 1–3 — key workflow is the foundation of everything remote |
