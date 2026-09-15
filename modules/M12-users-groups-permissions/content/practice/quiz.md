# Module 12 Quiz — 20 Questions

Answer in `lab-log.md`; key: [quiz-answers.md](quiz-answers.md).

1. **R** Name the seven fields of `/etc/passwd`.
2. **R** What is UID 0? What UID range do human accounts start at on Ubuntu?
3. **U** Why do hashed passwords live in `/etc/shadow` rather than `/etc/passwd`?
4. **R** Primary group vs supplementary groups: what's the mechanical difference
   (think: new files)?
5. **P** `usermod -G students ben` (no `-a`) — what happens to ben's other
   groups?
6. **R** Which commands create an account on Ubuntu, and which is the friendly
   interactive one?
7. **R** What does a `nologin` shell signal about an account?
8. **U** `chmod o=r data.csv` — which audiences' bits could this have
   *removed*, and why?
9. **P** Give the numeric modes: (a) private-only-me, (b) world-readable
   group-writable, (c) I-write world-run.
10. **U** What does `w` (write) on a *directory* allow that the file's own
    mode cannot prevent?
11. **U** Why can `cd` into a directory with mode `--x` work while `ls` fails?
12. **P** You own `f` with mode 604 and you're in its group. Can you read it?
    Which rule says so?
13. **R** What is umask subtracted from for files? For directories?
14. **P** `umask 027` — what mode do new files get? New directories?
15. **U** Why does `(umask 077; touch x)` not change your shell's umask?
16. **DS** A shared CSV must be editable by the lab group but not by the rest
    of the world. Which mode (and which *audience* does the work)?
17. **DS** Why is `chmod 777` on a dataset folder a confession rather than a
    solution?
18. **R** Which commands change: a file's group? a file's owner+group? your
    own password?
19. **U** `who` vs `w` vs `whoami` — one line each.
20. **DS** Design: Jupyter runs as service account `jupyter` (nologin); 12
    students need their own notebooks; datasets are shared read-only for
    students, writable by staff. Sketch the identity+mode plan in five lines.
