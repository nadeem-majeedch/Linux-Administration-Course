# Lab 2 — The Diagnosis Clinic: Five SSH Patients

> Module 22 · Unit 6 · Difficulty: Advanced
> Time: ~50 min · Environment: your own VM (Path A setup from
> [Lab 1](lab-01-key-workflow.md) assumed)
> Prerequisites: [Lab 1](lab-01-key-workflow.md) working end-to-end
> ⚠️ Every patient is *your own* setup, broken by a command *this lab
> gives you*, in your own VM. sshd_config is never edited; key files
> are the only things touched, and all breaks are one-line reversible.

Five patients, symptoms only. For each: **reproduce → diagnose with
the evidence tool → fix → verify → one-line prevention.** The
evidence tools are exactly four — `ssh -v` (or `-vvv`),
`ls -l ~/.ssh` (both machines!), `ssh-add -l`, `ssh -G alias` — plus
the server's auth.log when the client runs out of ideas. The
grading rubric: *which evidence revealed it*.

## Setup — the healthy baseline (5 min)

```console
$ ssh vm 'echo baseline-ok'      # must succeed passwordless (Lab 1)
$ ssh-add -l > ~/lab22-agent.txt # snapshot what the agent holds
```

## Patient 1 — "It asks for a password again"

The TA's break:

```console
$ chmod 755 ~/.ssh/lab_vm        # too-open private key
$ ssh vm                          # password prompt — the key was IGNORED
```

**Diagnose:** `ssh -v vm 2>&1 | grep -iE 'permission|identity|offering'`
— find the exact warning line (note it verbatim: ssh *tells* you).
**Fix + verify:** `chmod 600 ~/.ssh/lab_vm`; passwordless again.
**Prevention (one line):** the 600 is enforced *by the protocol
side*, not politeness.

## Patient 2 — "Works on this machine, not that one"

Scenario: the same key on a second machine (simulate: point the
config at a copy with a *different* name the server doesn't know):

```console
$ cp ~/.ssh/lab_vm ~/.ssh/lab_vm_copy
$ sed -i 's#IdentityFile ~/.ssh/lab_vm#IdentityFile ~/.ssh/lab_vm_copy#' ~/.ssh/config
$ ssh vm                          # password prompt again!
```

**Diagnose:** `ssh -v vm 2>&1 | grep -i 'no mutual\|offering\|authentications'`
— the client offers a key the server's `authorized_keys` doesn't
contain. `ssh -G vm | grep identityfile` shows *why* (the config
change). **Fix:** restore the IdentityFile line; keep `lab_vm_copy`
(or `rm` it) — then explain the prevention: *fingerprint on the
server* (`ssh vm 'cut -d" " -f2 ~/.ssh/authorized_keys'` vs
`ssh-keygen -yf ~/.ssh/lab_vm | cut -d" " -f2`) is how you'd have
spotted the mismatch in one command.

## Patient 3 — "REMOTE HOST IDENTIFICATION HAS CHANGED"

```console
$ ssh-keygen -R localhost >/dev/null           # forget the host (legitimate: rebuild)
$ sudo sh -c 'rm -f /etc/ssh/ssh_host_ed25519_key*'   # inside the VM: new identity
$ sudo systemctl restart ssh
$ ssh vm                                        # the scary warning — verbatim into log
```

**Diagnose:** the warning itself + the *reasoning*: who changed, was
it me? (Here: yes.) **Fix:** `ssh-keygen -R localhost`, reconnect,
accept new fingerprint, record it. **Prevention:** out-of-band
fingerprint verification *before* accepting — and the awareness
that on a real server this warning is a STOP sign, not a prompt.

## Patient 4 — "The alias broke"

```console
$ sed -i 's/^    Port 2222/    Port 2223/' ~/.ssh/config   # wrong port (Path A: use Port 1)
$ ssh vm                        # timeout / refused
```

**Diagnose:** `ssh -G vm | grep -E '^port|^hostname'` — the client
shows what it *resolved* (the config bug, plain as day), and
`ssh -vvv vm 2>&1 | grep -i connect` shows the connection attempt.
**Fix:** restore the line. **Prevention:** `ssh -G` is the first
command for any "config feels wrong" — it prints the merged truth.

## Patient 5 — "The tunnel won't come up"

```console
$ python3 -m http.server 8000 --bind 127.0.0.1 &     # VM side: the "Jupyter"
$ exit                                                # back on the host
$ ssh -L 8000:localhost:8000 vm -N &                  # tunnel in background
$ curl -m 3 -sI http://localhost:8000 | head -1       # expected: HTTP/1.0 200
$ ssh vm 'pkill -f http.server'                       # kill the "Jupyter" only
$ curl -m 3 -sI http://localhost:8000 | head -1       # now: empty/refused
```

**Diagnose:** the M21 ladder, tunneled — the *tunnel* is fine
(prove: `ss -tlnp | grep 8000` on the host still shows ssh
listening); the *service behind it* died. `curl -v` names refused
vs timeout. **Fix:** restart the server; verify through the tunnel.
**Prevention:** tunnel or not, "service up" is checked at the
service (`ss` on the remote), not at the tunnel.

## Wrap-up — the evidence table

`lab-log.md` closes with: patient / symptom / the ONE command that
revealed it / fix / prevention line. Then the meta-question: four
of five patients were diagnosed *client-side* — why is auth.log the
last resort, not the first? (Hint: what does the client know that
the server log shows only cryptically?)

## Done when

- [ ] Five writeups with verbatim evidence lines
- [ ] All config/permissions restored (`ls -l ~/.ssh` matches the
      Lab 1 end-state; `ssh vm 'echo ok'` passwordless)
- [ ] No stray processes (`pgrep -af http.server` empty on the VM)
- [ ] The meta-question answered
