# Module 13 Quiz — 20 Questions

Answer in `lab-log.md`; key: [quiz-answers.md](quiz-answers.md).

1. **R** Which of chown/chgrp require sudo, and why the asymmetry?
2. **U** Why do Alice's new files get group `alice` by default on Ubuntu?
3. **P** Mode `2770` on a directory — decode every component including the `2`.
4. **U** What does setgid change about files created inside a directory — and
   what does it *not* change?
5. **R** Which bit prevents users deleting each other's files in a shared
   writable directory? Where does Ubuntu use it by default?
6. **P** Mode `3770` on `inbox` — as a non-owner group member, which of
   read/write/delete on *someone else's* file work?
7. **U** Why does the naive shared setup "decay" without setgid + default
   ACLs/umask discipline?
8. **R** What does the trailing `+` in `ls -l` output promise?
9. **R** In `getfacl` output, what is the mask — and which entries does it
   throttle?
10. **P** `setfacl -m u:farid:rx DIR` then `chmod g-rx DIR` — what happens to
    farid's effective rights? Which line of `getfacl` shows it?
11. **U** Default ACLs vs access ACLs: which lives on directories, and what
    does it change about *newborns*?
12. **R** What does SUID on an executable do? Name two canonical Ubuntu
    examples.
13. **U** Why is every SUID-root binary a security-relevant artifact, and why
    does the course forbid making your own?
14. **R** `find / -perm -4000` finds what? (`-2000`? `-1000`?)
15. **U** State least privilege in one sentence and give the DS-server example
    of a student's dataset access.
16. **P** `namei -l /srv/lab/d/x.csv` shows `drwx------ alice labteam` on
    `/srv/lab` and team modes below. Who can reach the file, and what
    component stalls everyone else?
17. **DS** Design: staff rw, students r, one external reviewer r on exactly
    one subfolder. Specify groups, setgid, sticky (if any), and the ACL(s).
18. **DS** Model checkpoints dir: trainer writes, serving layer reads, world
    blind — mode + group plan? (M29 will connect the serving layer.)
19. **U** Why "grant access to roles (groups), not individuals"? Two reasons.
20. **DS** Your lab's "permissions keep breaking" tickets dropped to zero
    after one structural change. What was it, mechanically?
