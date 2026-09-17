# Module 02 Quiz — Linux Distributions

> 16 questions. Answer first, then check [quiz-answers.md](quiz-answers.md).
> Understanding over lookup: several questions have no single command
> as an answer — the reasoning *is* the answer.

## Section A — what a distribution is (Q1–5)

**Q1.** Distinguish "Linux" from "a Linux distribution" in two
sentences a non-technical friend could follow.

**Q2.** Name the three ingredients that cluster distros into families.
Which one changes your daily typing most?

**Q3.** Your teammate says "we should use Arch on the shared server
because it always has the newest packages." Give the *server-side*
argument against rolling releases that isn't "new = scary."

**Q4.** Why do so many DS container images build on Debian/Ubuntu
bases rather than whichever distro the author likes?

**Q5.** Ubuntu LTS releases every two years with five years of
support. What administrative behavior does that promise enable that a
rolling release cannot?

## Section B — identification (Q6–11)

**Q6.** You're on an unknown machine. Give the four-command circuit
and what each command contributes to the identity.

**Q7.** `/etc/os-release` says `ID_LIKE="rhel fedora"`. What do you
now know, what can you *predict*, and what one command confirms it?

**Q8.** `uname -r` reports `6.8.0-45-generic`. Your colleague writes
"we're on distro 6.8". Untangle the confusion.

**Q9.** Why source `/etc/os-release` in a script rather than parsing
`PRETTY_NAME` with grep?

**Q10.** A server runs Ubuntu 20.04 in 2026. State the question that
matters, the source that answers it, and the administrative
consequence if the answer is bad.

**Q11.** Why do hostnames make terrible identity sources? (The course
cited a real failure mode.)

## Section C — checksums & signatures (Q12–16)

**Q12.** Integrity vs authenticity: one sentence each, and which tool
answers which.

**Q13.** An attacker replaces a download *and* its published SHA256
list. Why does the checksum still match — and which verification step
saves you?

**Q14.** Why is SHA-256 preferred over MD5 for downloads, while MD5
remains "fine" for detecting bitrot in your own backups?

**Q15.** GPG prints "Good signature from …" *and* "not certified with
a trusted signature." What happened cryptographically, what remains
undone, and what do you do about it?

**Q16.** Name two places later in this course where the
integrity-plus-authenticity pattern reappears, with the tool for each.

Check answers: [quiz-answers.md](quiz-answers.md) ·
Practice more: [challenges.md](challenges.md)
