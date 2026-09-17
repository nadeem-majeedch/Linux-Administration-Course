# Module 25 Challenges — Security & Hardening

> Eight challenges, defense only, inside your own VM. Evidence in
> `lab-log.md`; the [hardening checklist](../hardening-checklist.md)
> is the rubric's backbone. C1–C3 are design challenges (no
> commands required); C4–C8 are hands-on.

## C1 — Rule design under constraints

Design (on paper) the complete ufw rule set for three hosts, and
justify every line: (a) a personal VM reachable only from your
host; (b) a shared GPU server reachable from campus + VPN, running
SSH, Jupyter (tunneled only — what does that imply?), and a
monitoring agent; (c) a public web server (HTTP/HTTPS + SSH from
admin subnet, with `limit`). For each: which rules are service
profiles vs port rules, and where `ufw limit` earns its place.

## C2 — The spot-the-vulnerability config

You're handed three configs (write them out yourself, then review
them as if a teammate submitted them): (1) an `sshd_config.d/`
drop-in with `PasswordAuthentication no` but *no* `AllowGroups`
and a ` PermitRootLogin yes` line; (2) a `.gitignore` that
contains `*.env` while a `.env` is already tracked; (3) a ufw rule
set where `allow 22` comes *after* `enable` in the setup script.
For each: name every finding, rank by severity, write the corrected
version.

## C3 — The threat-model brief

One page: your own VM as the asset. List its five most valuable
data items (keys? datasets? tokens?), the top four threat vectors
from Lesson 1 §7 as they apply *specifically to your setup*, and
which checklist items mitigate each. End with the two changes
you'd make first if you had one hour. (This is the exercise that
turns a checklist into judgment.)

## C4 — The firewall lab extension

Extend Lab 1: source-scoped SSH (host subnet only), a `limit`-ed
SSH rule, and a demonstration that a *removed* rule actually
blocks (spin a loopback service, allow it, curl OK, delete rule,
curl fails). All with before/after `ufw status numbered` outputs.

## C5 — The audit drill

Full listening-service audit of your VM into an `audit.md`: every
`ss -tulpn` line with the three questions answered; at least one
service *closed* (disable --now) with reasoning; then a re-audit
showing the delta. If your VM is already minimal, the finding is
"surface already minimal" — prove it with the before/after tables.

## C6 — The patch report

Write `patch-report.md`: current upgradable list with security
counts; unattended-upgrades timer state; the reboot-required check;
and a one-paragraph policy statement (what auto-updates, what
waits for a window, and why). Then *schedule* the weekly check as
a cron line (M19 preview — write it, don't install it) that mails
the count.

## C7 — The notebook forensics pass

Take a real (or freshly made) `.ipynb` and audit it as data:
`unzip -p notebook.ipynb | grep -iE 'token|key|secret|password'`
— notebooks are zips; cell *outputs* are searchable text. Find any
leaked-looking output, then write the one-line team rule that
prevents the class. (If clean: document the check itself as the
deliverable.)

## C8 — The rollback fire drill

Timed: break your own SSH hardening (revert the drop-in, reload),
*lose* access deliberately (confirm the password prompt returns),
then recover via the documented rollback path — target under 5
minutes from break to hardened-again. The deliverable is the timed
transcript plus the two sentences you'd add to the runbook having
actually done it once.

## Stretch — C9, the checklist run

Run the full [hardening checklist](../hardening-checklist.md)
against a *second* machine (host WSL? another VM?) — untouched by
this course. Score X/Y, list the top five gaps, fix one, re-score.
You've now used the artifact as it's used in the field: as an
audit instrument on a system you didn't build.
