# Module 05 Practice — Aliases & History (10 Questions)

Answer in `lab-log.md`; key below.

1. **R** Which keys recall and interactively search history?
2. **R** `!513` does what? `!!`? `!grep`?
3. **P** What does `!!:p` do differently from `!!` — and why do we drill it?
4. **R** When does bash write history to `~/.bash_history`?
5. **U** Two terminals are open; why doesn't terminal B see terminal A's
   newest commands? What forces it?
6. **R** Define an alias `lht` for "long, human, newest-first listing".
7. **P** `alias ll='ls -lh'` then `ll *.csv` — does the glob expand? Where in
   the expansion order does the alias sit?
8. **U** Why don't aliases work inside scripts — and what does that break for
   the `alias rm='rm -i'` safety idea?
9. **R** How do you list all aliases? Remove one?
10. **DS** Your top-5-customers pipeline (M09) is typed daily. Walk the
    four-step compounding loop (type → recall → alias → function) naming
    what changes at each step.

---

## Answer key

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
