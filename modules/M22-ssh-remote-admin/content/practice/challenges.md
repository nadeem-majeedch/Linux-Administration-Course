# Module 22 Challenges — SSH & Remote Administration

> Eight challenges on your own VM. Lab keys only; no external hosts;
> sshd_config remains read-only until M25. Evidence in `lab-log.md`.

## C1 — The fingerprint registry

Build `~/lab22/hostkeys.md`: for your VM, record the host key
fingerprints of **all** its key types (`for f in /etc/ssh/ssh_host_*_key.pub;
do ssh-keygen -lf $f; done` inside the VM) alongside the
`known_hosts` entries your client holds. Then explain in one line
which algorithm your client *chose* for the connection
(`ssh -v vm 2>&1 | grep -i 'host key'`) and why modern defaults
prefer it.

## C2 — The config translator

Take three real commands and express each as a config block, then
*verify* with `ssh -G` that the block reproduces the command
exactly: (a) `ssh -i ~/.ssh/lab_vm -p 2222 ds@localhost`,
(b) `ssh -L 6006:localhost:6006 vm -N`, (c) `ssh -J jump gpu02`
(jump and gpu02 both defined by you). Deliverable: commands,
blocks, and the matching `-G` output lines.

## C3 — The multi-key juggling act

Create a second key pair (`lab_vm_b`) and deploy it to a *second*
user on the VM (create `labuser` inside the VM — M12's useradd in
anger). Configure two aliases (`vm`, `vm-labuser`), each with
`IdentitiesOnly yes`. Prove with `ssh vm whoami` and
`ssh vm-labuser whoami` that the right key lands on the right
account — and one line on what would happen without
`IdentitiesOnly` (hint: agent + `MaxAuthTries`).

## C4 — The quoting gauntlet

One-line ssh commands (no scripts!) that: (a) print the remote
hostname and *local* username in one line, (b) create a file on the
VM whose *name* contains today's date (expanded remotely), (c) send
a local variable's *value* while expanding everything else
remotely, (d) run a remote pipeline that counts ERROR lines in the
VM's journal **and** greps the result locally to exclude one unit.
Each with the output as evidence — quoting is a contact sport.

## C5 — The tunnel commute

With a loopback "Jupyter" (an `http.server` on the VM, 8888):
establish a tunnel *in a named tmux window* on the host (why
there?), curl through it, then — the twist — kill the SSH
connection and show the tunnel died *with* it (curl fails), while
the VM's server is untouched (`ss` proof). One paragraph: which
process owns which end, and why `-N` tunnels belong in tmux windows
on the client side too.

## C6 — The permissions relay

Push a file via scp into a setgid shared directory on the VM
(M13's `/srv/project/` pattern — create it if needed), then read it
as the *other* user from C3. If it fails, diagnose (namei -l) and
fix with the minimal chmod — *on the VM, over ssh*. Deliverable:
the failing read, the diagnosis, the fix, the passing read.

## C7 — The sync rehearsal

Rehearse Mini-Project D's result-sync: build a fake `experiments/`
tree locally (three runs, one checkpoint file each), rsync to the
VM, add a run + modify one checkpoint locally, rsync again —
capture both transfers' stats lines and compute what fraction of
bytes moved the second time. Then the same with `--dry-run` and
annotate what `-n` reported vs reality. Close with the
`--delete` question: prove on a *scratch* directory that it mirrors
a deletion, and write the one-line warning you'd put in a team wiki.

## C8 — The runbook drill (Mini-Project D prelude)

From a cold VM: connect (alias), tmux, start a loopback service,
detach, tunnel from the host, curl-verify, detach, rsync a file in,
rsync a file out — **timing yourself**, target under 3 minutes —
then kill everything cleanly (tmux session, tunnel, VM service) and
verify the clean state (`tmux ls` empty, no stray ssh, VM service
gone). This is the muscle memory Mini-Project D documents.

## Stretch — C9, the client-side hardening review

Read your `~/.ssh/config` against this module's checklist
(`IdentitiesOnly`, `AddKeysToAgent`, `ServerAliveInterval`, no
`StrictHostKeyChecking` anywhere, named aliases over raw IPs) and
write `lab22-config-review.md`: current state, findings, fixes
applied. Then the same review of the *server* (`sshd -T | grep -iE
'passwordauthentication|permitrootlogin|pubkey'` — read-only) with
a one-paragraph "what I would change in M25 and why".
