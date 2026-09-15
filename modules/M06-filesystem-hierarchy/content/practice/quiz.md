# Module 06 Quiz — 20 Questions

Answer in `lab-log.md` before checking the [answer key](quiz-answers.md).

1. **R** What does `pwd` print, and why do professionals run it reflexively?
2. **P** You are in `/home/dsstudent/projects`. What does `cd ../data` do?
3. **R** Name three `ls` flags you will use daily and what each does.
4. **U** What is the difference in output between `ls /tmp` and `ls -ld /tmp`?
5. **P** `ls -lht` — what order do files appear in, and in what unit are sizes?
6. **R** What are `.` and `..`?
7. **R** Why do config files like `.bashrc` start with a dot, and how do you
   list them?
8. **U** Absolute vs relative path: define each in one line and give the deciding
   rule for scripts.
9. **P** From `/usr/share/doc`, write the *relative* path to `/usr/share`.
10. **R** What does `~` expand to? What does `~ben` expand to?
11. **U** Why is `~` safe in `cd` and `ls` but not guaranteed in every program's
    config files?
12. **P** After `cd /etc/ssh`, what does `cd ../..` resolve to?
13. **R** Name the FHS directory whose contract is: system-wide text configuration.
14. **R** Which directories are virtual (kernel-generated, no disk behind them)?
15. **U** What happens to `/tmp` at reboot, and what does that imply for dataset
    scratch files?
16. **U** Why does Ubuntu's `/bin` pointing to `usr/bin` not break old commands
    and documentation?
17. **R** What does `mkdir -p` do that `mkdir` does not — and what happens when
    the target already exists?
18. **P** `touch README.md` where the file exists: what changes, what doesn't?
19. **U** Explain brace expansion in `mkdir -p p/{a,b}/c` — how many directories
    result, and which?
20. **DS** Name two rules of the course's dataset-project layout and the reason
    each exists.
