# Midterm Examination — Answer Key & Grading Guide

> For instructors. Student paper: [midterm.md](midterm.md).
> Accept any wording that demonstrates the mechanism; the bracketed
> [keywords] are what must appear.

## Section A (30 pts — 3 each)

**A1.** Cannot deliver: [systemd services] and [sudo/root
administration of a real system] (also acceptable: real filesystem
permissions on a Linux kernel, ufw). Partial: [packaging — apt exists
but system layout/snap behavior differs]. Mechanism: Git Bash is a
userspace port, not a Linux kernel — no init system, no system
packages.

**A2.** `mkdir -p` [succeeds silently if the target already exists]
(idempotent), bare `mkdir` [exits non-zero] — in a re-run script the
bare form aborts the whole run for a harmless condition.

**A3.** Unset `$DIR` expands to empty, so the command degrades to
`rm -rf` with no target *or*, with multiple args, to [deleting the
wrong remaining args]; if `$DIR` is empty-and-first, classic variants
delete from `/`. Fix: [`rm -rf "$DIR"` quoting alone doesn't save
you — the loud-fail guard is `$DIR` in a `: "${DIR:?}"` check or
`set -u`]. Two characters that fail loudly: `":?"`
(`: "${DIR:?unset}"`) — accept `set -u` as equivalent intent.

**A4.** `ls -l` size = [logical bytes of file content]; `du` =
[allocated disk blocks] (space the filesystem reserved). 1-byte file
occupies a 4 KiB block.

**A5.** `mv` within one filesystem is a [rename] (instant); across
filesystems it must [copy + delete] — the USB stick is a different
filesystem, so the hang is the copy of `big.csv`.

**A6.** `important_notes.csv` [matches `*.csv`] and is deleted with
no confirmation. Safer form: [`rm -i` / `rm -I` interactive prompt],
or the lab habit: run `ls *.csv` first, then arrow-up and replace
`ls` with `rm` only after reading the expansion.

**A7.** 077 strips [group and other: r, w, x all] → files `600`,
directories `700`. Trade-off: [maximum personal privacy] at the cost
of [breaking every shared-directory workflow] — nothing you create
is group-readable regardless of directory SGID.

**A8.** 777 grants [write to every user] — teammates can *replace*
the script, and any service account can too. Minimal: [`755`] with
the precondition that [the teammate has read+execute via owner/group/
other — typically group membership] — never "other".

**A9.** Distinguisher: [`ls -li` — hard link shares the inode
number]; or link count `2` in `ls -l`. Divergence: [appending to one
changes both if via inode… no — the operation that makes contents
differ is **replacing** one with a new file (`echo > f2` truncates
the shared inode? no—)] — **accept only**: editing one file through
*its own new copy* (`cp f2 f2.new && mv f2.new f2`) breaks the link
[replaces the directory entry with a new inode]. Grading note: the
clean expected answer is `rm f2 && echo x > f2` — after
re-creation, `f1` and `f2` differ. Any student path that creates a
new inode behind one name is correct.

**A10.** [Non-root services] (postgres, nginx, jupyterhub) run as
their own users and rely on mode bits to protect their data
directories from *each other*; root's omniscience doesn't help the
service that must not read its neighbor. Also acceptable: least-
privilege limits blast radius when a non-root account is compromised.

## Section B (30 pts — 5 each)

**B1.**
```
a2.csv
b.csv
```
Mechanism: [glob expands in lexical order]; `a.txt` doesn't match.

**B2.** (inode numbers symbolic)
```
123 -rw-r--r-- 2 user user 2 … f1
123 -rw-r--r-- 2 user user 2 … f2
456 lrwxrwxrwx 1 user user 2 … f3 -> f1
```
Mechanism: [hard links share an inode (count 2); symlink is its own
inode (count 1, type l)].

**B3.** `out` = `one`, `err` empty → prints `one`. Then `cat
missing` writes to `err2`; `echo $?` prints `1`; `cat err2` prints
`cat: missing: No such file or directory`. Mechanism: [stderr
redirected per-command; exit status of the failed command persists
in `$?`].

**B4.**
```
value is $name
value is data
value is DATA
```
Mechanism: [single quotes suppress expansion; double quotes allow
it; `$( )` runs command substitution inside double quotes].

**B5.**
```
1
/home/user
```
Mechanism: [failed `cd` returns 1 and does not change directory];
`pwd` therefore shows the original location.

**B6.**
```
lvl1/f
lvl1/lvl2/f
```
then `1`. Mechanism: [`-maxdepth 1` excludes the nested copy;
`find` output is depth-first lexical here but `sort` makes it
deterministic].

## Section C (40 pts) — reference solution

**C1.** `for`-free solution:
```console
$ mkdir -p ~/midterm/{raw,scripts,reports}
$ cd ~/midterm/raw
$ for n in 01 02 03 04 05; do echo "sensor,ok" > sensor_$n.csv; done
$ cp sensor_[135].csv ../reports/
$ ls -l ../reports/   # must show exactly 01, 03, 05
```
Character-class `[135]` matches a *single* position — that's why
`sensor_0[135].csv` is the robust form; accept `sensor_0[135].csv`
or the glob `sensor_0*.[13]`-style only if it demonstrably selects
01/03/05.

**C2.**
```bash
#!/usr/bin/env bash
# clean.sh — count .csv files in a directory
set -u
if [ $# -ne 1 ]; then
    echo "usage: $0 <directory>" >&2
    exit 2
fi
printf '%s\n' "$(find "$1" -maxdepth 1 -name '*.csv' | wc -l)"
```
Must show `./scripts/clean.sh ~/midterm/raw` → `5`, missing-arg run
→ usage on stderr, `$?` = 2.

**C3.**
```console
$ sudo groupadd midteam
$ sudo usermod -aG midteam "$USER"   # re-login or newgrp
$ sudo chgrp midteam ~/midterm/reports
$ sudo chmod 2775 ~/midterm/reports
$ touch ~/midterm/reports/proof.txt
$ ls -l ~/midterm/reports/proof.txt  # group midteam
```
Proof line must show `midteam` as group of `proof.txt` — that is the
SGID inheritance evidence, not the mode of the directory.

**C4.** Cause: the file carries the [sticky/immutable-style
protection — in the lab this is the `undeletable` directory
permission trap: the *directory* lacks write for the user OR the file
has `+i`]; on the exam VM it is staged as `sudo chattr +i`. Expected
chain: `ls -l` (modes look fine) → `lsattr` shows `i` → `sudo chattr
-i` → `rm` succeeds → post-proof listing. Full credit requires
naming `lsattr`/`chattr` — students learned the diagnosis pattern in
M07/M08 labs (diagnose before fix).

## Common failure patterns to watch

- C-section transcripts with `history` cleaned or commands typed
  after the fact — grade 0 for that part (integrity rule on the
  paper).
- A9: students who claim appending to a hard link "forks" the file —
  mechanism error, cap at 1/3.
- B2: accepting `f3` with link count 2 — that's the whole question.
