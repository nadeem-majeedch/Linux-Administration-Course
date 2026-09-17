# Module 05 Practice — Aliases & History: Answer Key

> **Instructor material.** Student paper: [quiz-aliases-history.md](quiz-aliases-history.md).
> Answers preserved verbatim from the original combined file (2026-09 split
> per audit Finding C — content unchanged, location changed).

1. ↑/↓ walk; Ctrl+R interactive search (n to cycle, Enter to run).
2. Runs history entry #513; runs the previous command; runs the most recent
   command starting with `grep`.
3. `:p` *prints* the expansion without executing — the preview latch that
   keeps history expansion safe while the reflex trains.
4. On session exit (append), or immediately via `history -a`.
5. Each session keeps history in memory and appends on exit; `history -a` in
   the active session forces the append.
6. `alias lht='ls -lht'`
7. Yes — alias expands first, then the line's globbing runs normally. Alias
   is step one of expansion.
8. Scripts run non-interactive shells: no alias expansion. So the "-i guard"
   silently vanishes on servers/scripts — safety can't live in dotfiles.
9. `alias` (list); `unalias NAME` (remove one).
10. Type it carefully once → days of Ctrl+R recall → `alias topcust='tail
    -n +2 sales.csv | cut -d, -f2 | sort | uniq -c | sort -rn | head -5'` →
    when it needs a filename argument/variants, promote to an M10 function
    (`topcust FILE`, column parameter). Each step cuts keystrokes and error
    surface.
