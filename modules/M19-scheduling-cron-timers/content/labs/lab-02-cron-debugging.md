# Lab 2 — "Works in My Terminal": Diagnosing cron Failures

> Module 19 · Unit 5 · Difficulty: Advanced
> Time: ~45 min · Environment: your own VM, `~/lab19/`
> Prerequisites: [Lab 1](lab-01-schedule-the-pipeline.md), [Lesson 2](../lessons/02-cron-environment-logging.md)
> ⚠️ You will deliberately break a *copy* of the script, never your
> hardened original. All diagnoses use evidence (mail spool, `env
> -i`, env diff) — no guessing, and every fix verified by a real
> cron firing.

The module's signature skill, rehearsed as a clinic: a scheduled
job fails invisibly; you find it from evidence and fix it at the
script. Three patients, each a different environment betrayal.

## Setup — the fragile script (5 min)

Copy `dq.sh` to a deliberately environment-dependent version:

```console
$ cp ~/lab19/dq.sh ~/lab19/fragile.sh
$ sed -i 's#^PATH=.*#PATH=$HOME/.local/bin:$PATH#; s#^\(readonly SCRIPT_DIR=.*\)#readonly SCRIPT_DIR="."\1#' ~/lab19/fragile.sh
```

(If the seds don't match your script's lines, hand-edit to the same
effect: a PATH that only exists in *your* shell, and a relative
`SCRIPT_DIR`.) Verify it still works interactively from
`~/lab19/` — that's the trap: **`./fragile.sh sales.csv` works
fine.** That's what "works in my terminal" looks like.

## Patient 1 — the PATH betrayal (15 min)

Schedule it, with full logging so the failure is *recorded*, not
silent:

```console
$ crontab -l > ~/lab19/crontab.backup
$ crontab -e
# */2 * * * * cd /home/ds/lab19 && ./fragile.sh sales.csv >> /home/ds/lab19/logs/fragile.log 2>&1
```

Wait two minutes, read `fragile.log`. Expected: `python3: command
not found` or similar — the [PATH poverty](../lessons/02-cron-environment-logging.md)
verbatim. (If your script needs no non-/bin tools, the *evidence*
is `echo $PATH` output in the log — record that instead.)

**Diagnose formally:** add a one-minute env-dump job
(`* * * * * env | sort >> /home/ds/lab19/logs/cronenv.log`), diff
against your interactive `env | sort` — the missing variable is
named by the machine, not by guessing.

**Fix at the script** (Lesson 2's rule — carry your own
environment): restore the explicit `PATH=` line. Verify the fix
with a real firing — not with your terminal.

## Patient 2 — the working-directory betrayal (10 min)

Second break, different failure:

```console
$ sed -i 's#^readonly SCRIPT_DIR=.*#readonly SCRIPT_DIR=""#' ~/lab19/fragile.sh
# and remove any cd from the crontab line:
# */2 * * * * /home/ds/lab19/fragile.sh sales.csv >> ... 2>&1
```

cron runs from `$HOME`; the script's relative paths now resolve
wrong. Expected in the log: `sales.csv: No such file` or a silent
wrong-directory read (worse — check for it: a run that "succeeds"
on the wrong file is the nastiest variant).

**Diagnose:** the log's error names the path it *tried* — from
that path, deduce the cwd cron used. **Fix:** `SCRIPT_DIR`
derivation (Lesson 2 §3's `BASH_SOURCE` idiom) so cwd is
irrelevant. Verify by firing.

## Patient 3 — the silent failure (10 min)

Third break — remove the redirect from the crontab line:

```text
# */2 * * * * /home/ds/lab19/fragile.sh sales.csv
```

(And reintroduce any failure you like — break the PATH again.) Now
the job fails into the **mail spool**, not your log:

```console
$ tail -15 /var/mail/$USER 2>/dev/null
```

Read cron's confession: subject line (the job), the output, the
error. This is where *unlogged* scheduled failures live — the
patient teaches why Layer 1 redirect (or Layer 2 internal logging)
is non-negotiable. **Fix:** restore the redirect; clean the test
line out of your crontab entirely (`crontab -e`, verified by
`crontab -l`).

## Wrap-up — the diagnosis ladder

`lab-log.md` closes with the ladder as *your* procedure (five
steps, in order), plus one sentence per patient naming the
environment difference that killed it. The ladder, assembled from
this lab:

1. Read the job's log (Layer 1/2).
2. Read the mail spool (`/var/mail/$USER`) — the unlogged failure's
   record.
3. Reproduce with `env -i /bin/sh -c '...'` — cron's poverty,
   without waiting for cron.
4. Diff environments (`env | sort`, cron dump vs interactive).
5. Fix **at the script** (PATH, absolute paths, no prompts) — the
   crontab is a schedule, not a patch.

## Done when

- [ ] All three patients: symptom log line quoted, diagnosis
      command shown, fix verified by a real firing
- [ ] The env-diff artifact saved (cron env vs interactive env)
- [ ] Final crontab state transcribed (`crontab -l`) — no test
      lines left running
- [ ] The diagnosis ladder written in your own words
