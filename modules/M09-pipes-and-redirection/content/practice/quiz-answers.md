# Module 09 Quiz — Answer Key

1. stdin (0, keyboard), stdout (1, screen), stderr (2, screen).
2. Results vs diagnostics: capture/store/consume each independently — e.g.,
   pipe results onward while errors still reach the human.
3. `>` truncates to empty then writes; `>>` appends.
4. The error line appears on screen (stderr unredirected); out.txt is created
   (empty).
5. stderr; "send fd 2 to wherever fd 1 currently points."
6. Because redirections apply left-to-right: after `> file`, fd 1 points at
   the file — so `2>&1` then sends stderr there too. Reversed, fd 1 still
   points at the screen when `2>&1` runs.
7. A discard device — write = gone. Typically stderr (deliberate silencing),
   sometimes stdout in quiet scripts.
8. Empty. `>` truncates the target *before* `sort` reads it (same file on
   both ends of the pipe-less redirection).
9. Copies stdout to a file *and* passes it through (screen/next stage).
10. grep selects ERROR lines; `tee -a` appends them to a.log *and* forwards;
    `wc -l` counts what arrived.
11. `uniq` only collapses *adjacent* equal lines; sort gathers duplicates.
12. `10` (lexicographic: '1' < '2' < '9'); with `sort -n`: `2`.
13. `cut -d, -fN file | sort | uniq -c | sort -rn | head -5`
14. Approximate/aggregate questions on well-behaved rows — quick profiling,
    not exact columnar correctness (that needs a real CSV parser / M08 tools).
15. `;` always; `&&` only on success (exit 0); `||` only on failure (≠0).
16. No. The first `&&` gate fails (mkdir/cp chain breaks), so `echo OK` never
    runs — `&&`'s short-circuit decided.
17. Substitutes the command's output (current date, e.g. 2026-09-15); legacy:
    backticks `` `date +%F` ``.
18. `%s` = seconds since epoch — monotonically increasing, no reuse within a
    machine's lifetime.
19. Aliases are interactive-shell conveniences expanded at typing time; scripts
    run non-interactive shells that don't load them — so safety-via-alias
    vanishes exactly where automation runs. Habit + flags, not dotfiles.
20. `cut -d' ' -f7 access.log | sort | uniq -c | sort -rn | head -1`
    (endpoint = 7th space-field in combined log format). For *sums*:
    awk (M08).
