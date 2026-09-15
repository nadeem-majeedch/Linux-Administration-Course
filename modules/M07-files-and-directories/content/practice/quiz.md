# Module 07 Quiz — 20 Questions

Answer in `lab-log.md` before the [answer key](quiz-answers.md).

1. **R** What does `cp` require to copy a directory, and what happens to an
   existing DEST without `-i`?
2. **U** Why is `mv` within one filesystem instant even for a 40 GB file?
3. **R** State the three-command ritual before any `rm -r`.
4. **P** `rmdir` on a directory containing one file: what happens?
5. **U** What does `rm` actually remove, in inode terms?
6. **P** `file` on a `.csv` that's really UTF-16 from Windows: what does it
   report, and why is this check before-pandas?
7. **R** Name stat's three timestamps and one use for each.
8. **U** Which timestamp does `ls -lt` sort by, and what does `touch` move?
9. **R** In `ls -l`, what is the second numeric column?
10. **P** `echo *.log` in a dir with `app-2026-09-01.log` and `app-current.log`
    — exact expansion?
11. **U** Why doesn't `*` match `.bashrc`? Is that a bug or a feature?
12. **P** `rm *.xlsx` where no xlsx exists — what does the shell hand `rm`?
13. **U** Single vs double quotes: which allows `$HOME` expansion?
14. **P** `touch "my file.txt"` — one file or two? Then `rm my file.txt` —
    what happens?
15. **R** Two ways to delete a file literally named `-r`.
16. **U** Same inode on two names: what does appending through one name do to
    the other, and what does deleting one name do?
17. **R** Hard link vs symlink: which survives target deletion, which crosses
    filesystems, which can target directories?
18. **P** `ln -sfn runs/2026-09-15 runs/current` run twice — result? Run twice
    *without* `-n` — result?
19. **U** Why does `ls -l` show a symlink's own size (~path length) rather than
    the target's size?
20. **DS** Your 40 GB dataset is needed by three projects. Which link type do
    you choose, and what's the disk consequence of the wrong choice?
