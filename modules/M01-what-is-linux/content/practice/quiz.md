# Module 01 Quiz — 30 Questions

Answer in your `lab-log.md` *before* opening [quiz-answers.md](quiz-answers.md).
Types: **R** = recall, **U** = understanding, **P** = prediction (what will happen?).

## Section A — What Linux is (Lessons 1–2)

1. **R** In one sentence: what is an operating system?
2. **R** Strictly, what does the word "Linux" name?
3. **U** What did the GNU project contribute to modern Linux systems? Name three
   specific tools from this module's lessons that are GNU software.
4. **R** Who started the Linux kernel, where, and in which decade?
5. **U** Your phone runs Linux. In one sentence, reconcile that with the fact that
   it has no "Linux" logo.
6. **R** Name the two license families (free-software licenses) and one license
   from each.
7. **U** Why is macOS "certified UNIX" while Linux is not — and why doesn't it
   matter for your command-line skills?

## Section B — Distributions & Ubuntu (Lesson 3)

8. **R** List four things a distribution adds around the kernel.
9. **R** Match: .deb/`apt` — ? ; .rpm/`dnf` — ? (name the families)
10. **U** Ubuntu 24.04 is an LTS. What does that mean in months and years, and why
    do servers prefer it?
11. **P** A machine's `/etc/os-release` contains `ID_LIKE=debian`. Will
    `dnf install tree` work on it? What should you type instead?
12. **U** Give one scenario where a rolling release is a *reasonable* choice and
    one where it is a bad one.

## Section C — Architecture (Lesson 4)

13. **R** Name the four jobs of the kernel.
14. **U** What separates user space from kernel space, and what is the mechanism
    called that crosses it?
15. **U** A Python script enters an infinite loop using 100% CPU. Explain why the
    whole machine does not freeze, using the words *user space* and *kernel*.
16. **P** What does `cat /proc/cpuinfo` show — a file stored on disk, or something
    else? How do you know?
17. **R** What is a daemon? Give two examples from the lesson.
18. **P** `free -h` shows *available* 3.0 GiB and *free* 2.1 GiB. Which number
    matters when deciding "can I load a 2.5 GB dataset?" and why roughly?

## Section D — Shell, terminal, CLI (Lesson 5)

19. **R** Distinguish terminal, shell, and console in one line each.
20. **R** What does the `$` at the end of `nadia@hpc-1:/data$` indicate about the
    user — and what would indicate the opposite?
21. **P** You type `echo one two three`. How many arguments does `echo` receive?
    What prints?
22. **P** You type `echo "one two three"`. How many arguments? What prints?
23. **U** Which keys: interrupt a running command, clear the screen, recall the
    previous command, search history interactively?

## Section E — Help & syntax (Lessons 6–7)

24. **R** What do man page sections 1, 5, and 8 contain? One example of each.
25. **P** Which man command shows the *file format* of crontab rather than the
    crontab command?
26. **R** A command is a shell builtin. Which help system answers for it, and how
    do you find out it's a builtin in the first place?
27. **U** Decode: `cp [OPTION]... SOURCE DEST` — how many arguments are required?
    What may repeat?
28. **P** What are the three equivalent ways to get `ls` with long format and
    human-readable sizes? Which one is idiomatic in one-liners?
29. **P** After `whoami --bogus`, what does `echo $?` print roughly — and what
    does the number mean?
30. **U** What does `--` do in a command line, and which class of mistakes does it
    prevent?

---

Total: 30 points (1 per question). Passing: 24. When done, check
[quiz-answers.md](quiz-answers.md) and record your score in `lab-log.md`.
