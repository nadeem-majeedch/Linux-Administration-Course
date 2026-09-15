# Challenge Problems — Module 18

After the quiz; record each in `lab-log.md`. Own VM/WSL2, normal user
unless a step says otherwise.

- [ ] **C1 — the census one-liner.** Build a single pipeline: your 5
  processes with the highest RSS, showing pid, rss in MB, etime, and the
  first 60 chars of the command. (Hint: `ps -u $USER -o ... --sort=-rss`
  + `head` + `cut -c1-60`.)
- [ ] **C2 — three states, three proofs.** Deliberately create one `S`,
  one `T`, and one `Z` process of yours; capture `ps` lines as evidence;
  then eliminate each with the *correct* mechanism (CONT/resume, wait via
  parent exit, etc.) and note why kill is not that mechanism.
- [ ] **C3 — the misattributed kill.** Write a scenario + demonstration
  where `pkill -f python3` would kill something the user didn't intend
  (e.g., their own VS Code python extension host), and the scoped,
  verified alternative that wouldn't.
- [ ] **C4 — load without CPU.** Produce sustained `wa` > 10% on your VM
  (large file copy between disks or `dd` to a slow target — *into
  ~/scratch, never a device*). Capture top header + `iostat -x` +
  D-state census; explain the mismatch in three sentences.
- [ ] **C5 — the OOM post-mortem, from fiction to fact.** Read the OOM
  report format in Lesson 3 §5; then trigger a *tiny, controlled* OOM in
  a VM snapshot (python allocating until death — set swap small first)
  and extract the kernel's actual report lines. Identify the victim, the
  culprit, and the anon-rss figure from the log.
- [ ] **C6 — job-control survival drill.** Start `python3 -m
  http.server`; suspend it, background it, renice it +15, disown it,
  close the terminal, re-verify from a new terminal, then clean it up by
  PID. Every step with its command and output snippet.
- [ ] **C7 — priority arithmetic.** On your N-core VM: run N nice-0
  burners, then one nice-19. Using top, estimate the burner's effective
  share; compare with the −20…+19 scale's *intent*. Write the 3-sentence
  conclusion about what nice does and doesn't promise.
- [ ] **C8 — the runbook card.** Distill this module into one page:
  "Something's wrong with my job" → the 10 commands, in order, with the
  question each answers. Test the card by walking a partner (or your own
  past incident) through it.

C5 note: if you can't snapshot, *skip it* — a shared machine is never the
place; the C4 demonstration covers the observation skills instead.
