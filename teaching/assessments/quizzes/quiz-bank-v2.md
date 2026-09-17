# Quiz Bank v2 — MCQ, Command Interpretation & Output Reading

> 40 items · 4 sections · closed book. Answer all, then your instructor
> holds the key. Items are tagged with the module they assess.
> Every distractor encodes a documented misconception — if an option
> "sounds right," ask which wrong model it's selling.

## Section A — Multiple choice (Q1–15)

**A1.** *(M03)* A user-space program dereferences a bad pointer. What
happens?
a) The kernel crashes and the machine reboots
b) That process is killed; the system continues
c) The nearest service restarts automatically
d) The program is paused until a debugger attaches

**A2.** *(M02)* `cat /etc/os-release` shows `ID=fedora`. Which package
manager does this system use?
a) apt  b) pacman  c) dnf  d) zypper

**A3.** *(M06)* You are in `/var/log/apt`. Which command reads
`/var/log/apt/history.log`?
a) `cat history.log`  b) `cat ../history.log`  c) `cat ~/history.log`
d) `cat /history.log`

**A4.** *(M08)* Given sorted input, which pipeline counts *distinct*
error messages, most frequent first?
a) `uniq -c file | sort -rn`
b) `sort file | uniq -c | sort -rn`
c) `uniq -c file | sort -n`
d) `sort file | sort | uniq -c`

**A5.** *(M09)* After `grep ERROR app.log > result.txt 2> /dev/null`,
what is in `result.txt`?
a) matching lines and errors  b) matching lines only
c) errors only  d) nothing — errors overwrite it

**A6.** *(M10)* In `for f in *.csv; do wc -l "$f"; done`, the quotes
around `"$f"` exist to:
a) make the loop faster  b) survive filenames containing spaces
c) make the output verbose  d) prevent infinite loops

**A7.** *(M12)* Mode `rw-r-----` on a file; you are in the file's group
but not its owner. You can:
a) read and write  b) read only  c) write only  d) nothing

**A8.** *(M12)* `umask 027` is set. A newly created *directory* gets:
a) 750  b) 640  c) 777  d) 727

**A9.** *(M17)* `df -h` shows a filesystem 95% full; `du -sh /data`
totals far less. The most likely explanation:
a) the disk is lying  b) a deleted-but-open file holds the space
c) du skips hidden files by design  d) df counts in binary, du in decimal

**A10.** *(M18)* A process must release its temp resources on shutdown.
Which sequence is professional?
a) `kill -9` immediately  b) `kill -TERM`, wait, then `kill -9` if
needed  c) `kill -HUP`, then `kill -9`  d) close the terminal

**A11.** *(M20)* `systemctl enable foo` reports success, but `foo` is
not running. Because:
a) the unit file is invalid  b) enable wires the boot graph; start
runs it now  c) foo needs root  d) enable only checks syntax

**A12.** *(M21)* `curl http://127.0.0.1:8888` answers *Connection
refused*. The most direct conclusion:
a) the network is down  b) DNS is broken  c) nothing is listening on
8888 locally  d) the firewall dropped it silently

**A13.** *(M22)* The fingerprint of a known host changes on connect.
The professional response:
a) reconnect with `-o StrictHostKeyChecking=no`
b) delete `known_hosts` and move on
c) stop, verify the change out-of-band, then update or investigate
d) switch to password auth

**A14.** *(M27)* `ModuleNotFoundError: No module named 'pandas'` inside
an activated venv that has pandas installed. First suspect:
a) pandas is broken upstream  b) the *kernel/interpreter* running the
code is not that venv  c) pip needs root  d) the import path is too long

**A15.** *(M28)* A container writes user uploads to `/uploads` (a
mounted volume). The container is deleted. The uploads:
a) are gone with the container  b) survive — they live in the volume
on the host  c) move to the registry  d) survive until the image is
pulled again

## Section B — Command interpretation (Q16–27)

Explain precisely what each command does — including what it does
*not* do.

**B16.** `apt list --upgradable`
**B17.** `sudo apt install --dry-run nginx`
**B18.** `chmod 1770 /srv/project`
**B19.** `find . -name '*.log' -mtime +30 -delete`
**B20.** `rsync -avhn --delete clean/ vm:~/data/clean/`
**B21.** `kill -TERM $(pgrep -f training.py)`
**B22.** `journalctl -u webapp -p err --since -1h --no-pager`
**B23.** `ssh -L 9999:localhost:8888 vm -N`
**B24.** `systemctl --user enable --now health.timer`
**B25.** `rsync -a src dst/` (vs `rsync -a src/ dst/`)
**B26.** `docker run -v /data -p 8888:8888 img`
**B27.** `awk -F, '$3 > 100 {print $1}' sales.csv`

## Section C — Output reading (Q28–35)

**C28.** *(M06)*
```
$ pwd
/home/dsstudent
$ cd ../dsstudent/../root 2>&1
```
What happened, and why?

**C29.** *(M12)*
```
$ ls -ld /srv/datasets
drwxrws--- 2 root research 4096 Sep 17 09:14 /srv/datasets
```
Name the two special facts this mode encodes and their effect on new
files.

**C30.** *(M17)*
```
$ df -h /mnt/vol | tail -1
/dev/loop0p1   97M   60M   37M  62% /mnt/vol
```
What kind of device is `/dev/loop0p1`, and how do you know?

**C31.** *(M18)*
```
$ ps -o pid,ppid,stat,cmd -p 4321
  PID  PPID STAT CMD
 4321     1 D    /usr/bin/backup-worker
```
The process ignores `kill -9`. What does `D` explain?

**C32.** *(M20)*
```
● health.service - Health check
     Active: activating (auto-restart) (Result: exit-code)
```
What is happening, and which two commands form the next diagnosis?

**C33.** *(M21)*
```
$ ss -tlnp | grep 8888
(no output)
```
Your Jupyter is "unreachable." What does this prove, and what does it
rule out?

**C34.** *(M24)*
```
Sep 17 02:14:03 lab healthbot[5123]: Traceback (most recent call last):
Sep 17 02:14:03 lab healthbot[5123]: ModuleNotFoundError: pyyaml
```
Give the journalctl invocation that produces *only* this unit's errors
from the last hour.

**C35.** *(M29)*
```
2026/09/17 03:02:11 [error] 812#812: *9 connect() failed (111: Connection refused) while connecting to upstream
```
Which service is answering, which is failing, and what is the next
check?

## Section D — Short scenario (Q36–40)

**D36.** *(M13)* Five researchers share write access to `/srv/datasets`;
an intern must read everything but never delete. Design the mode(s) and
group(s); justify each digit.

**D37.** *(M19)* A cron backup job runs `~/bin/backup.sh` nightly and
"fails silently" (no evidence either way). Diagnose from first
principles and state the logging fix.

**D38.** *(M23)* A nightly `rsync --delete` mirror wiped a folder that
a teammate "had just moved." Which two course rules were skipped, and
what mechanism would have protected the folder even with `--delete`?

**D39.** *(M24)* After a weekend, a server is slow. Your first three
*read-only* commands, in order, and what each rules out.

**D40.** *(M28/M31)* Your capstone API container must survive reboots,
restart on failure, and log where journald can read it. Sketch the
two-line design (what runs it, where logs go).

---
*Instructor key: `keys-instructor/quiz-bank-v2-key.md` (held by your
instructor — not linked from student navigation).*
