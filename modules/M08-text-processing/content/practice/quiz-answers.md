# Answer Key — Module 08 Quiz

Each answer cites the lesson to revisit.

1. grep accepts filenames directly; the pipe adds a process and hides
   the filename from grep's error messages. cat earns its place only
   when *joining* streams. (L1 §2)
2. `file F` (type/encoding health) and `wc -l F` (scale). (L1 §1, §5)
3. `tail -n +2 f | head -5` — strip the header first, then take rows;
   reversed order grabs the header. (L1 §4)
4. Prints from line 2 to EOF (`+N` = starting line); it's the only
   standard tool that addresses "everything after the first line"
   without knowing the end. (L1 §4)
5. Paging/scrolling, in-file search (`/pat`), follow mode (`F`),
   memory-friendly on huge files — vs cat's dump-everything. (L1 §3)
6. `grep -c ERROR server.log` and `grep ERROR server.log | wc -l`.
   They disagree if a *line* contains ERROR twice (-c counts lines,
   wc counts lines output — actually equal here; they diverge with -o:
   `grep -o ERROR | wc -l` counts matches, not lines). (L1 §6, L2 §2)
7. -o prints only the matched *token*, not the whole line — enabling
   `grep -o ... | sort | uniq -c` censuses of tokens (IPs, codes). (L2 §2)
8. `^u00[1-5]` ; `WARN|ERROR` (with -E). (L2 §3)
9. `-E` makes `|`, `?`, `+`, `()` metacharacters; bare grep (BRE)
   needs escapes (`a\|b`) — escape-bugs follow. (L2 §3)
10. Modified within the last 7 days; strictly larger than 10 KiB. (L2 §1)
11. `find . -name "*.log" -exec wc -l {} +` ; `find . -name "*.log" |
    xargs -r wc -l`. (L2 §1, L4 §3)
12. uniq compares *adjacent* lines; unsorted input leaves scattered
    duplicates unmerged — silently. (L3 §2)
13. `cut -d, -f3 transactions.csv | tail -n +2 | sort | uniq -c | sort -rn`
    — wait, column 3 is region? No: region is field 3, but the header
    would be counted too; correct form:
    `tail -n +2 transactions.csv | cut -d, -f3 | sort | uniq -c | sort -rn`. (L3 §2, L5 §4)
14. delimiter=`,`; key=field 5; numeric compare; reverse (descending). (L3 §2)
15. Plain sort is lexicographic: "10" < "9". Amounts need -n or top-N
    reports lie. (L3 §2)
16. Single-character delimiter (quoted fields break it); can't address
    the last field. awk (`-F`, `$NF`). (L3 §7)
17. `tr '\t' ',' < sensor-telemetry.tsv > out.csv`. Safe when no field
    contains a comma (ours doesn't); unsafe with prose fields. (L3 §5)
18. `g` = substitute every occurrence in the line (not just first);
    `-n` suppresses default printing, `p` prints addressed lines —
    together: precise extraction. (L4 §1)
19. Rehearse: run without `-i` (stdout); apply: `sed -i.bak`; prove:
    `diff file file.bak`. (L4 §1)
20. `awk -F, '$3=="DS" {s+=$6; n++} END {print s/n}' students.csv`. (L4 §2)
21. `awk -F, 'NR>1 {r[$3]+=$5} END {for (k in r) print k, r[k]}'
    transactions.csv | sort -k2 -rn`. (L4 §2, L5 §4)
22. (a) `wc -l` — streams, O(1) memory; (b) grep/awk → new file —
    narrows before Python; (c) pandas — real joins are beyond
    reasonable shell. (L6 §1–2)
23. Fixed-width, zero-padded, big-endian fields → lexicographic =
    chronological order; Workflow D's range query used it directly. (L5 §5)
