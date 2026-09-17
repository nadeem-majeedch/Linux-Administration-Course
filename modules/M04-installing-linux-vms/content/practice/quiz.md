# Module 04 Quiz — Installation & VMs

> 18 questions. Answer first, then check
> [quiz-answers.md](quiz-answers.md). Scope: lessons 1–4.
> These test *reasoning under constraints*, not recall of menu names.

## Section A — Environment choices (Q1–5)

**Q1.** Your laptop has 8 GiB RAM total. Why does the course still
specify 4 GiB for the VM — and what operational constraint does that
impose on how you work through the course?

**Q2.** A classmate plans to do all labs on WSL2 "because it's
faster." Give one module where that plan *works*, one where it
*partially* works (and what they substitute), and one where it fails
outright — with the architectural reason for each verdict.

**Q3.** Why does the course install **Server** rather than Desktop in
the VM? Give the resource argument and the pedagogical argument.

**Q4.** NAT vs bridged networking for the lab VM: which is the safer
default, what does the safer option *prevent*, and which module
deliberately revisits the choice?

**Q5.** A web-based "Linux terminal" claims to replace your VM. Name
the three properties from Lesson 1 that it cannot provide, and what
each property buys the course.

## Section B — Verification (Q6–9)

**Q6.** You verified the ISO's SHA-256 but not the signature. What
attack remains open, and what single additional artifact closes it?

**Q7.** `sha256sum -c SHA256SUMS` prints `OK` for the ISO and several
`No such file or directory` lines for other files in the manifest.
Install or investigate? Justify.

**Q8.** `gpg --verify` says *Good signature* but warns the key is not
certified. In plain words: what is proven, what is not, and what is
the honest next step?

**Q9.** Why must verification happen **before** the install, not
after? State it in terms of the ISO's role in the system's trust.

## Section C — Provisioning decisions (Q10–13)

**Q10.** The installer offers "Use entire disk." On a VM this is
usually safe; on a dual-boot host it is the most dangerous screen in
the course. Explain the difference in what "the disk" means, and
name the two screens where you must re-confirm what you're erasing.

**Q11.** Why does the course install OpenSSH server *during*
installation rather than after? Give both the convenience reason and
the M22-relevant reason.

**Q12.** Why does the installer create a **normal user** rather than
asking you to set a root password? (M14 formalizes this; answer from
today's lesson plus M01's security instincts.)

**Q13.** Your VM's disk is 25 GiB but "dynamically allocated." You
check the host folder: the file is 6.2 GiB. Reconcile, and predict
what M08's `df -h` will show *inside* the VM.

## Section D — Snapshots & reset (Q14–18)

**Q14.** Explain what happens on disk when you take a snapshot —
why it is near-instant despite a 25 GiB disk.

**Q15.** Why is a snapshot not a backup? Give the failure scenario
that defeats snapshots completely.

**Q16.** You reverted to `clean-install` and lost a week of lab work
along with the disaster you meant to fix. What *policy* (naming,
timing) from Lesson 4 would have prevented this?

**Q17.** Why do long-lived snapshot chains slow the VM's disk I/O,
and what is the recommended end-state for a chain?

**Q18.** `lab-environment.md` contains a "reset procedure" line. What
must that line contain to be worth anything at 2 a.m., and which two
artifacts does it depend on?
