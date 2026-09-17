# Module 23 Quiz — Performance & Troubleshooting Method

> 22 questions. Answer first, then check [quiz-answers.md](quiz-answers.md).
> Scope: the eight-step methodology, the twelve drill cards, the
> Performance Clinic signatures. Method counts: "what command" earns
> half credit; "what command, *why now*, and what it rules out" earns
> full.

## Section A — the methodology (Q1–6)

**Q1.** List the eight steps in order. Which single reordering most
often turns a solvable incident into an unsolvable one?

**Q2.** What three facts must the step-1 problem sentence contain, and
why does each one change the investigation?

**Q3.** Why is "snapshot before you touch anything" a *rule* and not a
preference? Name two kinds of evidence that die on a casual restart.

**Q4.** State the three properties of a good hypothesis, and rank
these two by testability: "the venv lost pandas" vs "the system is
misconfigured somehow".

**Q5.** What is the blast-radius sentence, and why must it precede a
mutating test rather than follow an incident?

**Q6.** Verification of "Jupyter unreachable from the office" — why is
`systemctl status` green insufficient, and what does complete
verification look like?

## Section B — performance signatures (Q7–12)

**Q7.** Load 7.0 on 4 cores; `top`: `us` 14%, `wa` 42%, `id` 40%. Two
sentences: what's the resource, and which two numbers say so?

**Q8.** Distinguish swap *size* from swap *activity*, and give the
`vmstat` columns for the one that constitutes the symptom.

**Q9.** A process is at PID 1 inside its namespace and died with exit
137. Which mechanism killed it, and which command finds the verdict?

**Q10.** `await` 3 ms, `%util` 99, `aqu-sz` 1.1 vs `await` 90 ms,
`%util` 60, `aqu-sz` 6. Which disk is *busy* and which is *sick*?
Justify with the queue depth.

**Q11.** `free -h` shows `free` 250M, `available` 5.0G. One sentence
on why this is healthy, naming the mechanism.

**Q12.** TX `dropped` climbs during a large transfer while `errors`
stays zero. What is the mechanism, and who owns the fix?

## Section C — the cards (Q13–18)

**Q13.** Server-slow ticket. You've got `uptime`, `vmstat`, `top`,
`free`, `iostat` available. In what order do you run them, and which
*single* column most often redirects the diagnosis away from CPU?

**Q14.** Disk "full": `df` says 98%, `du` accounts for 45% of the
device. Name the mechanism, the evidence command, and why `rm` of the
file did nothing.

**Q15.** In card 9's decision tree, why does `namei -l` beat `ls -l`
for "Permission denied" on a deep path?

**Q16.** Card 11: `pip install` fails with "externally-managed
environment". What is the *system* doing correctly, and what is the
course's fix (two words)?

**Q17.** Card 7: `dig` answers correctly but `getent hosts` disagrees.
Which layer wins for applications, and what file did you now think to
read?

**Q18.** Card 12's duplicate-server trap: two jupyter processes in
`ps`, one listener in `ss`. What happened, and why does the *new*
server's failure look silent?

## Section D — synthesis (Q19–22)

**Q19.** The Drill Book's incident 1 planted two faults. Explain why
fixing the first and stopping there is the *method failure*, not just
an incomplete fix.

**Q20.** You inherit a ticket: "cron job never ran." Write your first
three commands in order, and what each rules out.

**Q21.** Why does the methodology call prevention *part of the
incident* (step 8) rather than a nice-to-have afterward? Give one
concrete canary for card 2's incident class.

**Q22.** A colleague's postmortem reads: "Fixed it — restarted the
service. Working now." Rewrite it in the step-8 template's spirit
(three sentences: mechanism, evidence, prevention).

Check answers: [quiz-answers.md](quiz-answers.md) ·
Practice more: [challenges.md](challenges.md)
