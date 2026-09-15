# Module 06 — Challenge Problems

Log attempts (commands + outcomes) in `lab-log.md`. All safe: creation and
reading only.

## ★ C1 — Blindfold navigation

With the screen cleared (`Ctrl+L`), reach these five targets using **Tab only**,
no full typing: `/usr/share/doc/grep`, `/var/log`, `/etc/apt`, your home, and
`/proc`. Record keystroke counts. Under 15 keystrokes each means fluency.

## ★ C2 — The path decoder

For each line, state the final directory *without running* (then verify):

```
a) /etc/../etc/../var
b) ~/projects/../projects/eds-01
c) /usr/bin/../lib
d) ~/data/raw/../../archive
```

## ★★ C3 — FHS comparison: VM vs lab server

If a lab server (or a classmate's machine) is reachable over SSH (or compare
against WSL2): `ls /` both machines. Identify three layout differences and
research (official docs) which package or feature explains one of them.

## ★★ C4 — Dataset layout review

You're handed a colleague's project:

```
~/stuff/final/FINAL2/data copies/newest/sales.csv
```

Rewrite it into the course convention (Lesson 4), listing the exact `mkdir -p`
brace-expansion command that builds the skeleton and where `sales.csv` lands.
One paragraph: what risks did the old layout create?

## ★★ C5 — The reboot survivor list

Predict, then verify with the map (don't actually reboot): for each —
`/tmp/mine.csv`, `~/data/raw/sales.csv`, `/var/log/syslog`, `/etc/hostname`,
`/run/user/1000/notes` — does it survive reboot? Who owns it? Could another
user read it? (Last column is a preview of M12; "probably not" is acceptable
with reasoning.)

## ★★★ C6 — The /proc interview

In `/proc`, find your shell's PID directory (`echo $$` gives the PID). Inside
it: `cat cmdline`, `head -5 status`. Three lines in your log: what process is
this, how much memory does `status` claim, and why is this "everything is a
file" rather than magic?
