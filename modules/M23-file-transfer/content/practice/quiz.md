# Module 23 Quiz — File Transfer & Synchronization

> 20 questions. Answer first, then check [quiz-answers.md](quiz-answers.md).
> Scope: lessons 1–3. Scenario-based throughout — every answer
> requires reasoning the cheatsheet can't supply.

## Section A — Tool selection (Q1–5)

**Q1.** A teammate's 5 GB file transfer over flaky hotel Wi-Fi died
at 92% four times using `scp`. Name the exact rsync flag(s) that
turn the fifth attempt into a resumable one, and explain what scp
fundamentally lacks — in terms of *file state*, not feature lists.

**Q2.** You must move a directory containing 40,000 small files to a
new server once. Why is `tar` + single-file transfer usually faster
than `rsync -r`, even though rsync is "the sync tool"? What property
of the transfer is the bottleneck?

**Q3.** Your dataset is a 2 GB `.gz` file. A colleague suggests
`rsync -azh`. Give two reasons this specific combination wastes
resources, and the corrected command.

**Q4.** When is `sftp` genuinely better than two or three sequential
`scp` invocations? Give one concrete scenario from your own lab.

**Q5.** A labmate runs `rsync -a src dst/` expecting to merge files
into `dst/`. Diagram (text) where the files actually land, and the
one-character fix.

## Section B — Flags & semantics (Q6–12)

**Q6.** Expand the six things `-a` implies (the `rlptgoD` set), and
name which two of those can only be fully preserved by root on the
*destination* — and why a normal-user sync still works fine for
course purposes.

**Q7.** `scp -P 2222` vs `scp -p` — one sentence each. What
single-character typo would silently preserve timestamps when you
meant to specify a port?

**Q8.** After `touch sensor.csv`, rsync re-transfers the whole file
even though the content is byte-identical. What comparison pair
triggered this, and which `--check`-style option avoids it at the
cost of reading every byte?

**Q9.** Why does `--delete` combined with `--exclude` create an
ambiguity, and which additional flag makes the semantics explicit?
What is the safer belt-and-braces alternative to outright deletion
taught in this module?

**Q10.** You push with `--delete`. Your teammate pulls with
`--delete`. Same flag, opposite dangers — state each direction's
risk in one sentence.

**Q11.** `--append-verify` on a log file being actively written:
what corruption mechanism makes this unsafe, and what is the
correct choice for live files?

**Q12.** Which rsync line in your log lets you detect "the source
tree is being churned nightly by builds"? Quote the metric and give
the threshold intuition.

## Section C — Verification & provenance (Q13–16)

**Q13.** rsync reports "up to date" but your sha256 manifest diff
shows one differing file. Walk through exactly how this is possible
(both comparison models), and which command would have caught it.

**Q14.** Why keep `local.sha256` in the project directory after the
transfer? Answer in terms of *reproducibility*, naming what later
question the file answers.

**Q15.** The manifest verify step failed with a diff line ending in
`< feed_cleaned.csv`. Which side has the extra/changed file, and
what does the `<` direction mean in `diff` output?

**Q16.** A verified sync ran at 14:00. At 16:00 the server-side
copy is edited. At 17:00 a teammate re-runs the sync *pull* into
their laptop copy. What does the laptop end up with, and what
one-word policy (from M19) prevents this class of confusion?

## Section D — Safety & automation (Q17–20)

**Q17.** List, in order, the three gates the course's
`sync-results.sh` passes before any byte moves. For each, name the
failure it prevents.

**Q18.** An unattended cron rsync with no SSH key: what two
different failure modes can occur, and which one is *dangerous*
rather than merely annoying? Why does `BatchMode=yes` eliminate the
dangerous mode?

**Q19.** A teammate proposes `--delete` in the nightly cron with no
dry-run. Write the two-line policy statement you'd add to the team
README, using this module's rules.

**Q20.** Your sync log shows `sent 12.35M bytes ... speedup is
2.98`. Explain the number as if to a statistician: what is the
denominator, and what ideal value does 1.0 represent?

---
*Answer key (instructor use): [quiz-answers.md](quiz-answers.md)*
