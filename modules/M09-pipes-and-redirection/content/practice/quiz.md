# Module 09 Quiz — 20 Questions

Answer in `lab-log.md` before the [answer key](quiz-answers.md).

1. **R** Name the three standard streams, their descriptor numbers, and defaults.
2. **U** Why do stdout and stderr exist as separate streams?
3. **P** `cmd > f.txt` where f.txt exists — outcome? And with `>>`?
4. **P** `ls /nope > out.txt` — what appears on screen, what lands in the file?
5. **R** What does `2>` capture? What does `2>&1` literally mean?
6. **U** Why must `2>&1` come *after* `> file` in `cmd > file 2>&1`?
7. **R** What is `/dev/null` for, and which stream usually goes there?
8. **P** `sort list.txt > list.txt` — what's in list.txt afterwards, and why?
9. **R** What does `tee` do that `>` cannot?
10. **P** `grep x f | tee -a a.log | wc -l` — describe all three stages' effects.
11. **U** Why must `sort` precede `uniq -c`?
12. **P** `printf '9\n10\n2\n' | sort | head -1` — output? With `sort -n`?
13. **R** The counting idiom for "top 5 values of a column" — write it.
14. **U** `cut -d, -f3` fails on a quoted field containing a comma. What class
    of question is the pipeline still valid for?
15. **R** `&&` vs `;` vs `||` — one line each.
16. **P** `mkdir -p a && cp x a/ && echo OK` with an unwritable parent —
    does OK print? Which operator decided?
17. **R** What does `$(date +%F)` do, and what's the legacy equivalent?
18. **P** `cp f "f-$(date +%s).txt"` — why can this never collide?
19. **U** Aliases: why don't they work inside scripts, and why is
    `alias rm='rm -i'` not a safety strategy?
20. **DS** Give the one-pipeline answer to: "which API endpoint appears most
    often in access.log?" and name the tool that would replace the last
    stage if you needed *sums* per endpoint (M08 foreshadow).
