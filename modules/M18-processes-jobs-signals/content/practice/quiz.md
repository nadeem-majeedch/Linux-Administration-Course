# Module 18 Quiz — 22 Questions

Answer in `lab-log.md`; key: [quiz-answers.md](quiz-answers.md).

1. **R** Distinguish program, process, and thread (one sentence each).
2. **R** What does PPID tell you, and what happens to orphans?
3. **U** Name the two `ps` incantations this course standardizes on and
   what each is for.
4. **P** Decode this STAT pair: `Rs` on a busy python, `D` on an rsync.
5. **U** Why is `D` state immune to `kill -9`, and what's the real fix?
6. **R** Which top keys sort by memory / CPU, show per-core bars, filter
   by user?
7. **U** `wa` is 30% in top. What is the machine waiting on, and which
   lesson-1 census confirms it?
8. **P** `ps aux` shows %CPU 380. One core, or several? Which column
   proves total compute consumed since start?
9. **U** Why is low `free` in `free -h` usually fine? Which column is the
   honest one?
10. **R** Command to find any PID by name *with* its full command line?
11. **U** What does `pstree -p PID` show that `ps aux` can't — and why
    does that matter before killing a launcher?
12. **R** What does Ctrl-Z actually do to the foreground job (which state,
    which mechanism)?
13. **P** `sleep 300 &` twice; stop only the second. Command?
14. **U** Why do background jobs die when the terminal closes — and name
    the two shell-level fixes.
15. **R** `nohup python3 train.py > t.log 2>&1 &` — explain every token.
16. **U** SIGTERM vs SIGKILL: which is catchable, and what does a trapped
    handler typically buy a training run?
17. **R** Which signal does Ctrl-C send, and to *which* processes exactly?
18. **P** Preview-then-kill: the two commands for every pattern kill. Why
    is `-u $USER` non-negotiable on shared servers?
19. **U** Why can't you kill a zombie, and who can clean it up?
20. **R** Nice range and direction. Which direction may a normal user
    move their own process, and why is that rule least-privilege by
    design?
21. **P** `renice -n -5 -p 6001` as non-root: exact failure, and the two
    sanctioned paths that would make it succeed.
22. **DS** Load 18 on 8 cores, `wa` 2%, one python at 700% CPU, RSS
    climbing 1 GB/min. Which playbook steps fire, in order — and what is
    the likely end state if nobody intervenes?
