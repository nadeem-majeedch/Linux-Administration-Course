# Lab 2 — The Signal Handshake: Trap, Observe, Escalate

> Module 18 · Unit 5 · Difficulty: Intermediate
> Environment: your own VM/WSL2, normal user · Time: ~40 min
> Prerequisites: [Lesson 2](../lessons/02-jobs-and-signals.md)

This lab makes signals *visible*: a script you control logs every signal
it receives, so TERM vs KILL vs INT stops being theory.

## Part A — a script that talks back

```console
$ mkdir -p ~/lab18 && cd ~/lab18
$ cat > signer.sh <<'EOF'
#!/bin/bash
# signer.sh — logs every signal it can catch, until it can't
log() { echo "$(date +%T) got $1" >> signals.log; }
trap 'log SIGTERM;  exit 0' TERM
trap 'log SIGINT;   exit 0' INT
trap 'log SIGHUP;   exit 0' HUP
echo "$(date +%T) started, PID $$" >> signals.log
while true; do sleep 1; done
EOF
$ chmod +x signer.sh
$ ./signer.sh & echo "signer PID: $!"
```

## Part B — the polite request (SIGTERM)

```console
$ kill -TERM $(pgrep -f "bash ./signer.sh")     # PID verified via pgrep
$ sleep 1; cat signals.log
14:02:11 started, PID 7301
14:02:40 got SIGTERM
```

It caught TERM, logged it, and exited cleanly — because it *chose* to
(trap → exit 0). **Record:** this is what every well-behaved program
tries to do. One sentence: why did the script's exit not require KILL?

## Part C — Ctrl-C vs background: the group experiment

```console
$ ./signer.sh &                     # restart it (log appends)
[1] 7330
$ fg                                # bring it forward
^C                                   # Ctrl-C now
14:05:03 got SIGINT                  # in the log: the INT arrived
```

Now prove the *background* exemption: restart, keep it in background, and
press Ctrl-C in that terminal — the shell takes the Ctrl-C (prints a new
prompt) and **the signer keeps running**. Verify with `pgrep -af signer`.
**Record:** why background jobs survive foreground interrupts (process
groups, Lesson 2 §5), and the exact commands you'd use to stop the
background one.

## Part D — escalation, with evidence

A version of signer that *ignores* TERM shows why KILL exists:

```console
$ cp signer.sh stubborn.sh
$ sed -i "s/trap 'log SIGTERM;  exit 0' TERM/trap 'log SIGTERM' TERM/" stubborn.sh
$ ./stubborn.sh & echo "stubborn PID: $!"
$ kill $(pgrep -f stubborn.sh)      # TERM...
$ sleep 2; pgrep -f stubborn.sh     # ...still alive! logged the TERM, ignored it
$ kill -KILL $(pgrep -f stubborn.sh)
$ sleep 1; pgrep -f stubborn.sh || echo "gone — KILL cannot be trapped"
$ cat signals.log | tail -3         # note: got SIGTERM, then nothing — no clean exit
```

**Record (the ladder, in your own words):** what TERM offered, what
stubborn did with the offer, what KILL did anyway — and what a *training
run* loses when KILL is the closer (buffers, checkpoints).

## Part E — SIGHUP and the terminal

```console
$ ./signer.sh &
$ disown %1                          # or: nohup ./signer.sh & instead
$ exit                               # close THIS terminal (open another first!)
```

Reopen a terminal and check `pgrep -f signer.sh`: with `disown`/`nohup`
it survived the hangup. Repeat *without* disown — gone. **Record:** which
signal the closing terminal delivered, and the one-line explanation of
what nohup changed.

## Part F — the audit drill

```console
$ pgrep -a -u $USER | grep -v pgrep | head     # what of yours is still running?
$ pkill -u $USER -f signer                     # scoped cleanup, previewed
$ pgrep -f signer || echo clean
```

Then write the two-sentence justification a sysadmin would accept for each
kill you performed: *what you verified before signaling* and *what signal
you chose and why*.

## Done when

- [ ] signals.log shows TERM, INT, HUP caught (and the ignored TERM from stubborn)
- [ ] The background/Ctrl-C exemption demonstrated and explained
- [ ] The escalation ladder executed with evidence at each rung
- [ ] Terminal-hangup experiment: job with and without nohup/disown
- [ ] Cleanup previewed (pgrep) then executed (scoped pkill); audit
      sentences written
