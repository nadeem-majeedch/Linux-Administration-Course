# Module 24 Quiz — Logs, journald & Monitoring

> 22 questions. Answer first, then check [quiz-answers.md](quiz-answers.md).
> Scope: lessons 1–4. The evidence-first rules count as quiz material.

## Section A — journald (Q1–6)

**Q1.** Why must you never `grep pattern /var/log/journal/*`? What two
things does `journalctl` give you that raw grep cannot?

**Q2.** What is the difference between the journal's volatile and
persistent storage — which directories, and what happens at reboot in
each mode?

**Q3.** Write the journalctl command that shows everything unit
`train.service` said at error severity or worse, during the *previous*
boot.

**Q4.** In the priority table, what number and keyword denote
"warning", and what does the range syntax `-p warning..` (trailing
dots) mean?

**Q5.** You run `journalctl --user -u sync.service` and see nothing,
but the service is running. Name the first two things to check.

**Q6.** What does `-o json-pretty` change about the output, and why
would a pipeline prefer it over the default short format?

## Section B — classic logs & rotation (Q7–12)

**Q7.** Which `/var/log` file answers "who used sudo yesterday, and
what command did they run?" — and which answers "what was upgraded
yesterday?"

**Q8.** What kind of storage is `dmesg` reading, and what happens to
old entries?

**Q9.** Given `rotate 7 / daily / compress` in a logrotate config,
state how many days of history the file keeps and what happens to the
oldest entries.

**Q10.** You must search last Tuesday's messages, but the active file
only covers today. Which files do you search, and with which tool(s)?

**Q11.** Name two properties of the "greppable log contract" and the
reason each earns its place on one line.

**Q12.** What does `systemd-cat -t myjob` do for a script's output —
and which journalctl flag then filters to just that script's lines?

## Section C — monitoring (Q13–18)

**Q13.** In `free -h` output, explain the difference between the
`free` and `available` columns, and why a low `free` is usually healthy.

**Q14.** Load average is 6.2 on a machine with `nproc` = 4. What
single additional observation distinguishes "saturated but flowing"
from "queue growing"?

**Q15.** In `vmstat` output, which columns signal memory pressure even
when `free` memory still looks okay, and which column captures "CPU
idle because waiting on storage"?

**Q16.** In `iostat -x` output, name the two columns that most
directly indicate a *device-level* bottleneck, and what each means.

**Q17.** What is `sar`'s unique capability compared to every other
tool in this module — and what must be true on the machine for it to
have data?

**Q18.** A teammate reports "disk full". Which two commands, in order,
localize the problem from filesystem to directory?

## Section D — methodology & safety (Q19–22)

**Q19.** Name the six steps of the incident method in order, one
phrase each.

**Q20.** Why does the method insist on *binary tests* (like `df -h`)
before narrative theories?

**Q21.** State the 3-2-1 rule, and name the lab feature that
demonstrated why the *archive* copy is not replaceable by a
`--delete` mirror.

**Q22.** A fix "worked" — the service starts now. What two things
must still happen before the incident is closed, per the method?

## Bonus (Q23) — DS reality check

A GPU-server teammate says: "The box is slow, CPU is at 90%." Draft
the first three commands you'd run and the one question you'd ask
them, before any verdict.
