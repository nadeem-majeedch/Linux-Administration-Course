# Module 22 Quiz — SSH & Remote Administration

> 22 questions. Answer first, then check [quiz-answers.md](quiz-answers.md).
> Scope: lessons 1–4. Safety-rule questions count as quiz material.

## Section A — keys & authentication (Q1–7)

**Q1.** In the key pair, which half goes to `authorized_keys` and
which never leaves your machine — and what makes the exchange secure
despite the public half being public?

**Q2.** `ssh-keygen -t ed25519 -C "lab22" -f ~/.ssh/lab_vm`: what do
`-t`, `-C`, and `-f` each do, and which file is the private key?

**Q3.** Why does ssh refuse a private key with mode 644 — and what
does that have to do with M12/M17?

**Q4.** What problem does the passphrase solve, and what problem
does ssh-agent solve? (One sentence each.)

**Q5.** `ssh-copy-id` vs `cat pub | ssh ... 'cat >> authorized_keys'`:
name the three details the tool handles that the hand-rolled pipe
often gets wrong.

**Q6.** Which file records server host keys, what trust model does
its first-entry follow, and what must you do before accepting a
*changed* key?

**Q7.** Your key stopped working on every server at once. Name the
two most likely causes and the one command distinguishing them.

## Section B — config (Q8–12)

**Q8.** For each directive — client or server side?
`IdentityFile`, `PasswordAuthentication`, `HostName`, `PermitRootLogin`.

**Q9.** Write the `Host` block: alias `gpu01`, real host
`10.0.0.51`, user `ds`, key `~/.ssh/lab_vm`, reached *via* alias
`jump`.

**Q10.** What does `IdentitiesOnly yes` prevent, and when does it
matter in practice?

**Q11.** `ssh -G vm` — what does it print, and which class of bug
does it diagnose in one command?

**Q12.** In sshd_config, what does `PermitRootLogin prohibit-password`
allow and disallow — and why is `no` still the course recommendation
once keys are deployed?

## Section C — execution, copying, tunnels (Q13–18)

**Q13.** Explain the difference in expansion:
`ssh vm 'echo $USER'` vs `ssh vm "echo $USER"`.

**Q14.** `ssh vm 'some-command'; echo $?` returned 3. What does that
tell you, and why does it matter for automation?

**Q15.** When is scp the right tool vs rsync? Two criteria for each
side.

**Q16.** The trailing-slash rule: what's the difference between
`rsync -a ~/exp/ vm:~/exp/` and `rsync -a ~/exp vm:~/`?

**Q17.** `ssh -L 8888:localhost:8888 vm -N` — what does each part
do (`-L`, the two 8888s and `localhost`, `-N`), and which machine's
loopback does the middle `localhost` refer to?

**Q18.** Why is tunneling preferred over "just make Jupyter listen
on 0.0.0.0"? Two reasons.

## Section D — tmux & safety (Q19–22)

**Q19.** tmux vs nohup: one sentence each on which problem each
solves, and the course pairing rule.

**Q20.** What does `Ctrl-b d` do, what keeps running, and how do
you get back from a *different* machine?

**Q21.** The two-terminal rule before applying
`PasswordAuthentication no` — state it, and explain what each
terminal is for.

**Q22.** List four of the five key-hygiene rules from Lesson 1 §7.

## Bonus (Q23) — the GPU-server morning

You're about to run a 6-hour training on `gpu01` (reached via a
jump host). List the four commands you type before walking away —
in order — and what each protects against.
