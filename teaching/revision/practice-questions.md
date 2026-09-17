# Practice Questions — Unit by Unit

> Answer on paper or aloud first. Each question has a **hint**
> (indented, grey) — read it only after a genuine attempt. Full
> solutions are not provided here; verify by *doing* in your VM, which
> is the point.

## Units 1–2 (M01–M07)

1. A colleague's Ubuntu server has an unfamiliar package manager. How
   do you identify the distro family before recommending an install
   command?
   > *Hint:* what do `/etc/os-release` and the presence of `apt`/`dnf`
   tell you — and which do you trust more?
2. `mkdir -p a/b/c` then `rmdir a` — what happens and why?
   > *Hint:* rmdir refuses non-empty; which flag or which order
   changes the outcome, and why is that refusal a *feature*?
3. Predict: `echo "data" > f.txt; ln f.txt h.txt; rm f.txt; cat h.txt`
   > *Hint:* hard link = second name for the same inode. Which count
   in `ls -l` proves it?
4. Why does `grep error *.log 2>/dev/null | wc -l` silently ignore
   unreadable files — and is that safe?
   > *Hint:* stderr is discarded, not counted. What would you lose?
5. Write the glob that matches `report-2026-01.csv` but not
   `report-2026-01.csv.bak`.
   > *Hint:* the shell matches the *whole* string; end your pattern
   deliberately.

## Units 3–4 (M08–M13)

6. `./run.sh` exits 1 with no output. Name three distinct causes and
   one diagnostic step each.
   > *Hint:* shebang wrong? `set -e` fired mid-pipe? script not
   executable? — one probe per cause.
7. What does `trap 'rm -rf "$TMP"' EXIT` guarantee that a trailing
   `rm` line does not?
   > *Hint:* how many ways can a script stop early?
8. A file shows `-rw-rw----  1 ana research 4096 …` and Ben (in
   research) edits it successfully. Elena (not in research) gets
   Permission denied. Explain both outcomes with the mode bits.
   > *Hint:* which tertile applies to Ben, which to Elena, and what
   does `-` in position 1 rule out?
9. Your team dir has SGID but new files are still private. What two
   settings besides SGID must be right?
   > *Hint:* the *creator's* umask, and the directory's group-w bit.
10. Why is `sudo vim file` a common footgun compared with
    `sudoedit file`?
    > *Hint:* what does the editor run as, and what can $PATH abuse
    do with it?

## Units 5–6 (M15–M25, M32)

11. `apt install` says "Unable to locate package". Give two causes and
    the diagnostic for each.
    > *Hint:* stale index vs missing repo vs typo — one command each.
12. `/` is at 95%. `du -x -d1 /` reports far less than `df` does. Name
    the classic suspect and its one-liner.
    > *Hint:* what holds space after its file is deleted?
13. A cron job emails you: "command not found: python3". Why now?
    > *Hint:* what does cron's PATH contain, and what's the two-line
    fix (absolute shebang + PATH line)?
14. Your unit runs fine manually, fails at boot. What single line in
    `systemctl cat` explains most such cases?
    > *Hint:* which directive gates network-dependent units?
15. `curl http://localhost:8000` works from the VM; the host browser
    can't connect. Give the three-point diagnosis in order.
    > *Hint:* bound address (ss) → firewall (ufw) → forwarding
    (VM/WSL port forward). Which is most common in this course's labs?
16. What does `journalctl -u api --since "1 hour ago" -p err` give you
    that opening /var/log/syslog does not?
    > *Hint:* unit filtering, priority filtering, structured fields,
    boot scoping — name two.

## Unit 7 (M26–M29, M31)

17. `pip install -r requirements.txt` succeeds; the notebook still
    can't import pandas. Give the two most likely causes and their
    one-line probes.
    > *Hint:* which python does Jupyter's kernel use? Which python
    did pip target?
18. Why must experiment outputs live in a volume/bind mount rather
    than the container's writable layer?
    > *Hint:* what happens to the writable layer at `docker rm`?
19. Your analysis is reproducible on your machine only. List the three
    artifacts that would make it reproducible on any Linux box.
    > *Hint:* pinned deps, checksummed data, versioned code — plus
    what *records how they meet*?
20. `docker run` fails: "port is already allocated". Find the holder
    and decide the fix without killing anything blindly.
    > *Hint:* `docker ps` first, then `ss -ltnp` — who owns 8000?
