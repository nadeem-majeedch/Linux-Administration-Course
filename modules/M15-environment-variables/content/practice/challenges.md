# Challenge Exercises — M15

> All challenges on your own VM. C3 stages controlled breakage with
> named repairs; C4/C5 are evidence-driven — the diagnosis is the
> deliverable.

## C1 — The inheritance map

Produce a diagram of *your machine's* env-var custody: for four
contexts (SSH login, desktop tab, `sudo -s`, `crontab -e`'s eventual
job), trace which startup files run and what each contributes.
Evidence rule: every arrow in your diagram needs the command that
proved it (`shopt -q login_shell`, `/proc/PID/environ` reads, a
profile.d probe). Deliverable: the diagram + a table of which of
`PATH`, `EDITOR`, `PYTHONPATH` each context sets, overrides, or
drops.

## C2 — The PATH surgeon

Build `~/lab15/c2/` with three programs named `tool`:
(A) `echo A` in `dir-a`, (B) `echo B` in `dir-b`, (C) `echo C` in
`dir-c`. Using *only* one-shot PATH prefixes — no exports — produce
all three outcomes (`A`, `B`, `C`) in three commands. Then write the
two-line rule for how a package manager (M16) and a venv (M27) each
use this exact mechanism to control which `tool` (or `python`) wins.

## C3 — The five-stage incident

Staged, with repairs written *before* each stage:

1. **Shadow:** put an impostor `git` on PATH (harmless echo).
   Diagnose with the three-command reflex.
2. **Amputate:** PATH without `$PATH` in a subshell. Recover by
   absolute paths only.
3. **Vanish:** `unset HOME` in a subshell — run `cd` and observe.
   Explain the failure precisely.
4. **Empty-not-unset:** `MYFLAG= ./check.sh` vs `unset MYFLAG;
   ./check.sh` — write `check.sh` so it distinguishes them honestly
   (`${MYFLAG+x}` or `set -u`).
5. **Stale hash:** install-then-shadow sequence where `command -v`
   lies until `hash -r`.

Deliverable: an incident log — for each stage: symptom, diagnosis
command, one-line cause, one-line repair. This is a drill for M25's
cron clinic and M31's server debugging.

## C4 — The cron-inheritance case file

Set up (M25 preview, allowed): `crontab -e` with
`* * * * * env > /tmp/cron-env.txt` — wait a minute, `crontab -r`
after. Diff `/tmp/cron-env.txt` against your shell's `env`. Write
the case file: three concrete things the cron environment lacks,
and for each, the exact injection fix (cron `VAR=` line, absolute
paths, in-script activation) — citing the lesson for each.

## C5 — The secrets audit

Take any script or dotfile of yours (or a provided sample from
M25/M27): audit it with Lesson 4's rules. For each secret-like
string: where does it enter the process? where is it *stored*?
what reads that storage? Propose the migrated design (restricted
file + explicit source, or one-shot) and the verification command
proving the new design leaks less (what would you grep, where?).
Deliverable: before/after excerpts + the audit table.

## C6 — venv forensics (M27 bridge)

In a fresh venv: `pip install requests`, then from *outside* the
venv run `~/venvs/lab/bin/python -c "import requests;
print(requests.__file__)"` and `python3 -c "import requests;
print(requests.__file__)"` (after `pip install requests` for the
system one, or observe the ImportError). Explain both outputs in
Lesson 2's first-match terms — and predict what `sudo` (M14) does
to the environment when you try `sudo ~/venvs/lab/bin/python`.
Verify the prediction. Deliverable: outputs + one paragraph.
