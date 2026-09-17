# Module 26 Quiz — Git and Development Workflows

> 22 questions. Answer first, then check [quiz-answers.md](quiz-answers.md).
> Scope: lessons 1–3, all three labs. The "commit early, commit small"
> and "never force-push shared history" rules count as quiz material.

## Section A — the model (Q1–6)

**Q1.** Git stores snapshots, not diffs. What does that mean a commit
contains, and what does the *hash* of the previous commit add?

**Q2.** Name the three states. Which command moves a file between each
adjacent pair?

**Q3.** You edited a file, staged it, edited it again, and ran
`git diff`. Which two states is it comparing? What flag compares the
other adjacent pair?

**Q4.** Why is `git log` instant on a machine with no network, and what
*does* require the network in Git?

**Q5.** What physically is a branch? What does `git switch` actually
change?

**Q6.** Why can Git verify that no file in your history was corrupted,
without any backup checksums?

## Section B — branching & merging (Q7–12)

**Q7.** Distinguish a fast-forward merge from a three-way merge. What
does the second parent of a merge commit record?

**Q8.** Both branches edited *different regions* of the same file.
Conflict or clean? What is the exact condition for a conflict?

**Q9.** List the three steps of conflict resolution and the one command
that backs out of a merge entirely.

**Q10.** What is the difference between `git branch -d` and `-D`, and
why is the lowercase default safer?

**Q11.** What does `git rebase` do to the commits it replays, and what
is the course rule about when that's safe?

**Q12.** `git checkout HEAD~2` then `git commit` — what state are you
in and what is at risk? Name the rescue command.

## Section C — remotes, ignore, auth (Q13–18)

**Q13.** What is a bare repository, and why do Git *servers* use them?

**Q14.** Your push is rejected with "fetch first". What happened,
and what are the next commands?

**Q15.** A 2 GB CSV is committed. Why won't adding it to `.gitignore`
now help, and what are your two options (and their costs)?

**Q16.** Which five categories never belong in a data-science repo's
history? For one of them, name what goes in instead.

**Q17.** Why does the same SSH key authenticate both `ssh ds@server`
and `git push` to a repository hosted on that server?

**Q18.** HTTPS+token vs SSH for remotes — when is each the better
choice, and why are tokens the safer pick on borrowed machines?

## Section D — workflow & synthesis (Q19–22)

**Q19.** Write a commit message (subject + body) for: you fixed the
revenue column's dtype because CSV parsing produced strings, which
silently broke the monthly totals. Follow the course convention.

**Q20.** Pull-early, pull-before-push: explain what each habit
prevents.

**Q21.** Your teammate proposes committing trained model binaries to
the repo "for reproducibility". Compose the two-sentence rebuttal that
names what *does* belong in the repo.

**Q22.** In the end-to-end lab, `outputs/` was in `.gitignore` yet
`outputs/summary.csv` got committed. What mechanism allowed it, and
why was that the *right* decision for this artifact while the PNG
stayed out?

Check answers: [quiz-answers.md](quiz-answers.md) ·
Practice more: [challenges.md](challenges.md) ·
Symptoms index: [../troubleshooting.md](../troubleshooting.md)
