# Module 12 — Challenge Problems

Log attempts in `lab-log.md`. Account surgery: **VM only**, throwaway users
only. Everything else is read-only or touches files you create.

## ★ C1 — The passwd census

One pipeline per question over `/etc/passwd` (M08/M09 skills): (a) how many
accounts total, (b) how many have bash as shell, (c) how many nologin, (d)
which UIDs above 1000 exist. Decode each awk/cut you use.

## ★ C2 — Membership audit

For every group your user belongs to: `getent group <name>` — who else is in
it? Write the two-line security note for any group that implies *admin power*
(`sudo`) vs plain membership groups. (No changes — this is an audit.)

## ★ C3 — The mode reverse-engineer

`ls -l /usr/bin/passwd /usr/bin/sudo /tmp` — three *unusual* mode strings
(letters `s`, `s`, `t`). Do not decode them yet (M13 Lesson 2); instead:
record them, hypothesize what the extra letters might mean from the commands'
purposes, and write your guesses. M13 grades them.

## ★ C4 — The umask studio

Prove these three statements experimentally (subshell per experiment):
(a) umask can't *grant* the executable bit to new files, (b) `umask 000`
yields 666/777 (and why that's not 777 for files), (c) a umask of `022` vs
`002` differs exactly in group-writability — the collaboration dial.

## ★★★ C5 — The broken home (VM)

Create `t-fix` with `useradd` *without* `-m`. Log in via `sudo -iu t-fix`
(read-only — you're previewing M14): what's wrong with the session (home?
shell? prompt?). Diagnose from `getent passwd t-fix` and repair with
`usermod -m -d /home/t-fix` (plus `mkdir`/`chown` — M13 teaches `chown`; use
`sudo usermod -m -d` and observe what it moves). Full write-up: symptom →
cause → fix → verification.

## ★★★ C6 — Design defense

A teammate proposes: every researcher gets UID<1000 "so they sort first", all
datasets `chmod 666`, everyone in `sudo`. Write the four-paragraph rebuttal
from this module (identity conventions, least privilege, the 777 confession,
audit trail) — addressed to a technically literate but rushed PI.
