# Lab 2 — Break & Fix: Three Service Failures, Diagnosed

> Module 20 · Unit 6 · Difficulty: Advanced
> Time: ~45 min · Environment: your own VM, **user units only**
> Prerequisites: [Lab 1](lab-01-service-circuit.md) (you have hello.service)
>
> This lab breaks things *on purpose* — your own user unit, three ways —
> so the diagnostic reflexes (status → journal → hypothesis → fix →
> verify) become yours. Every incident gets the five-part writeup:
> **symptom → diagnosis → fix → verification → prevention.**

## Setup

From Lab 1 you should have `hello.service` running:

```console
$ systemctl --user is-active hello.service     # expect active
$ cp ~/.config/systemd/user/hello.service ~/hello.service.bak   # the undo button
```

## Incident 1 — the typo'd ExecStart (the classic)

**Break it:**

```console
$ sed -i 's|ExecStart=%h/bin/hello-loop.sh|ExecStart=%h/bin/hello-loop.shX|' \
    ~/.config/systemd/user/hello.service
$ systemctl --user restart hello.service 2>&1
```

**Diagnose (resist guessing — read):**

```console
$ systemctl --user status hello.service     # Active: failed (exit-code=203)
$ journalctl --user -u hello.service -n 8 --no-pager
```

203/EXEC: the binary literally doesn't exist at that path. **Record**
the status + journal lines that *say* so.

**Fix + verify:**

```console
$ sed -i 's|hello-loop.shX|hello-loop.sh|' ~/.config/systemd/user/hello.service
$ systemctl --user daemon-reload            # <- the step everyone forgets
$ systemctl --user restart hello.service
$ systemctl --user is-active hello.service  # active again
```

**Prevention (write it):** which command would have caught this before
the restart? (Hint: `systemd-analyze --user verify
~/.config/systemd/user/hello.service` — run it and paste its verdict.)

## Incident 2 — the restart loop (a foreground lie)

**Break it:** make the script background itself (the anti-pattern from
Lesson 3 §2):

```console
$ sed -i 's|^while true; do|nohup bash -c '"'"'while true; do|' ~/bin/hello-loop.sh
$ echo 'done'"'"' & | cat >> /dev/null   # (skip this line — do the next block instead)
```

Simpler, deterministic breakage — replace the script with one that
double-forks and exits:

```console
$ cat > ~/bin/hello-loop.sh <<'EOF'
#!/bin/bash
# anti-pattern: daemonizes itself — systemd sees "main process exited"
nohup bash -c 'while true; do echo hi; sleep 5; done' >/dev/null 2>&1 &
exit 0
EOF
$ systemctl --user restart hello.service; sleep 10
$ systemctl --user status hello.service     # watch it: activating → activating…
$ journalctl --user -u hello.service -n 12 --no-pager   # "Scheduled restart job"
```

**Diagnose:** systemd starts it, the parent exits 0, with
`Type=simple` + `Restart=on-failure` the manager keeps re-launching —
the log shows the restart scheduling loop. **Record** two consecutive
"Started/Scheduled restart" pairs.

**Fix:** restore the foreground script (Lab 1's original) or set
`Type=forking` (and know why that's the wrong tool here — one
sentence):

```console
$ cp ~/hello.service.bak ~/.config/systemd/user/hello.service
$ cp /dev/null /tmp/x   # (no-op) — restore the script from your Station-3 heredoc:
$ cat > ~/bin/hello-loop.sh <<'EOF'
#!/bin/bash
while true; do echo "$(date +%T) hello from systemd"; sleep 5; done
EOF
$ systemctl --user daemon-reload && systemctl --user restart hello.service
$ sleep 12 && systemctl --user status hello.service   # active, no restart churn
```

**Prevention:** the Type= decision tree in one line: *foreground
script → simple; self-daemonizing → fix the script (preferred) or
Type=forking.*

## Incident 3 — the invisible edit (daemon-reload miss)

**Break it — but this time *edit correctly but forget the reload*:**

```console
$ sed -i 's/^Restart=on-failure/Restart=on-failure\nRestartSec=1/' \
    ~/.config/systemd/user/hello.service
$ systemctl --user restart hello.service        # no daemon-reload!
$ systemctl --user show hello.service -p RestartUSec   # what's actually loaded?
```

The `show` output still says `5s` — your edit isn't live. **Record**
the loaded value vs the file's value (they disagree).

**Fix:**

```console
$ systemctl --user daemon-reload
$ systemctl --user show hello.service -p RestartUSec   # now 1s
$ sed -i 's/^RestartSec=1/RestartSec=5/' ~/.config/systemd/user/hello.service
$ systemctl --user daemon-reload && systemctl --user restart hello.service
```

**Prevention:** `daemon-reload` after every unit-file change — or use
`systemctl edit`, which reloads for you. Write the one-line rule.

## Wrap-up — the incident retrospective

All three incidents in one table: symptom → the single log line that
gave it away → the fix → the one-command prevention. Then the
meta-question: which of the three would you have *guessed* wrong
without the journal, and what does that say about where you look first?

## Done when

- [ ] All three incidents have the five-part writeup
- [ ] Incident 1 includes the `systemd-analyze verify` prevention check
- [ ] Incident 2 includes two restart-loop log pairs
- [ ] Incident 3 includes the loaded-vs-file disagreement evidence
- [ ] `hello.service` healthy at the end (`is-active` = active)
