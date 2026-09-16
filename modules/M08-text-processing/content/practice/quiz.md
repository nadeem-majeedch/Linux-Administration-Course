# Module 08 Quiz — 22 Questions

Answer in `lab-log.md`; key: [quiz-answers.md](quiz-answers.md).
Datasets referenced are in [../data/](../data/README.md).

1. **R** Why is `cat file | grep x` called "useless use of cat"?
2. **R** Which two commands answer "what is this file" and "how big is
   this file" before any analysis?
3. **P** Show lines 2–6 of a CSV using only tail and head. Order
   matters — why?
4. **U** What does `tail -n +2` do, and why is it the header/body split
   idiom?
5. **R** Name three things less does that cat can't.
6. **P** Command: count ERROR lines in server.log two ways. When do the
   two disagree? (Hint: multiple matches per line.)
7. **U** What does `grep -o` change about grep's output model — and
   which pipeline does it enable?
8. **P** Write an ERE matching u001–u005 student IDs, and another
   matching either WARN or ERROR.
9. **U** Why is `grep -E` preferred over bare `grep` for `a|b`
   patterns? What would bare grep need?
10. **R** What do find's `-mtime -7` and `-size +10k` test?
11. **P** One command: line counts of every .log under the current
    tree. Two syntaxes (find -exec; xargs).
12. **U** Why does `uniq` require sorted input? What's the failure
    mode without it?
13. **P** The census idiom for: transactions per region, ranked. Write
    it in full.
14. **R** `sort -t, -k5 -nr` — decode every flag.
15. **P** Why does `sort -n` matter for amounts? What does plain sort
    do with 9 vs 10?
16. **U** cut's two hard limits (delimiter type, no last field) — and
    which tool covers both?
17. **P** Convert sensor-telemetry.tsv to CSV in one command. When is
    this safe, when not?
18. **R** sed: what does the `g` flag do, and what does `-n` + `p` do
    together?
19. **U** The sed -i discipline: rehearse → apply → prove. Which
    commands embody each step?
20. **P** awk one-liner: mean GPA of DS students only (students.csv).
21. **P** awk group-by-sum: revenue per region (transactions.csv), with
    header skip. Then rank it with a sort.
22. **DS** Your 40-GB CSV needs (a) row count, (b) a filtered 2-GB
    subset, (c) a per-region join with a lookup table. Which tool for
    each, and why — per Lesson 6's division?

## Bonus (ungraded)

23. Why do ISO-8601 timestamps sort correctly as strings — and which
    Lesson 5 query exploited that?
