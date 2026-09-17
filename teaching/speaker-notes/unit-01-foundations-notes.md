# Unit 1 Speaker Notes — Foundations (M01–M04)

> Companion to [../lecture-slides/unit-01-foundations-slides.md](../lecture-slides/unit-01-foundations-slides.md).
> Notes expand the deck; they don't repeat it. Total across 4 sessions:
> ~6 h contact.

## Session 1 (Slides 1–6)

**Teaching purpose.** Establish identity and safety before content: by
the end students know *what they're going to become* (someone who
administers their own machine), and that mistakes are the method.

**Opening question.** "Who owns the computer you're sitting at?" — every
hand rises. Follow-up: "Who can *administer* it — add a user, see every
process?" — hands fall. That gap is the course.

**Per-slide guidance.**

- *S3 (OS definition):* the building-manager analogy is the anchor;
  return to it every time a concept appears (permissions = door keys,
  processes = residents, memory = rooms).
- *S4 (stack):* the GNU/Linux naming aside must stay under 60 seconds.
  The durable takeaway: "distro = kernel + everything around it."
- *S5 (distros):* write `cat /etc/os-release` on the board and leave it
  there — it returns in the exam.
- *S6 (activity):* expect ~30% of pairs to place glibc inside the kernel.
  That error is gold — it sets up Slide 8.

**Terminology to insist on.** *kernel*, *distribution*, *user space*,
*shell* (preview only). Discourage "Linux system" vagueness.

**Beginner misconceptions (unit-wide, observed every cohort).**

1. "Linux is an application you install like Word."
2. "Ubuntu = Linux" (and therefore Red Hat ≠ Linux).
3. "The terminal is an app like any other — maybe optional."
4. "Root is just a stronger password."

**Expected student responses.** S1 question: browsers/games (fine —
bridge to "and *who lets* the browser write files?"). S5 dnf question:
silence is normal; answer it yourself via the package-manager idea.

**Live demo instructions.** Boot the instructor VM before class starts
(failure of *this* demo is catastrophic for tone). `uname -a` — read the
string out loud, piece by piece, no hand-waving.

**Possible command errors during demo.** None by design; if you mistype,
*use it* — narrate the recovery. Modeling recovery is the hidden lesson.

**Classroom activity.** Card sort (paper, not on a slide — prepare 8
cards: Android, Ubuntu, macOS, VirtualBox, bash, apt, Jupyter, ext4);
teams place them on the stack drawing they make in Slide 6's task.
Debrief targets Android (defensible *both* ways — make someone argue
each). If printing wasn't possible, run it as a shout-out sort against
the Slide 4 diagram.

**Time allocation.** 20/45/15/10 as deck states. If running long, cut
the card sort, never Slide 4.

**Transition.** "Next session you boot your own machine into the same
stack you just drew."

**Exit questions (S1 formative, per plan).** Three-question exit poll:
what's the kernel? what's a distro? what runs on servers? Collect
tickets; the "fuzzy" answers feed Session 5's warm-up.

---

## Session 2 (Slides 7–10)

**Teaching purpose.** Give the machine *anatomy*: boot acts and the
syscall boundary — the two ideas that make later diagnostics rational.

**Opening question.** "You press power. Name everything that happens
before you see a login screen." Take 4 guesses, order them into the
four acts on the board.

**Per-slide guidance.**

- *S7 (boot):* timebox 12 min. The exam wants *vocabulary*, not GRUB
  internals.
- *S8 (syscall boundary):* the Python-writes-CSV chain is the unit's
  densest idea. Have 3 students restate the chain; incorrect restatements
  are the lesson.
- *S9 (CLI):* the timed GUI-vs-CLI file-rename race is worth its 5
  minutes — the margin is the argument.

**Questions to ask (and expected responses).**
"Why is a kernel crash fatal but a Python crash not?" — expect "the
kernel is more important" (true but imprecise); sharpen to *isolation
asymmetry*: user-space crashes are contained by design.

**Live demo.** `ls /proc` — pick `/proc/cpuinfo`, `/proc/uptime`. Sell
"the kernel's diary, exposed as files."

**Troubleshooting the demo.** If a student's VM froze (1 GB RAM cohort),
don't fix quietly — diagnose aloud; it's the day's concept made flesh.

**Transition.** "You know what the machine *is*. Next two sessions: you
build one and learn to trust it."

---

## Sessions 3–4 (Slides 11–18)

**Teaching purpose.** Everyone leaves with a working, snapshotted,
updated VM — and the *belief* that mistakes are recoverable.

**Opening question (S3).** "What does the installer mean by 'Erase
disk'?" Get the wrong answer ("my laptop's disk!") into the air, then
dismantle it with the virtualization slide.

**Demo choreography (S4 snapshot demo).**
1. Snapshot named `clean-install-<date>` (do it live, slowly — the
   exact name students took in M04 lab 1).
2. Introduce harmless chaos *inside the VM*: `sudo hostnamectl
   set-hostname lab-broken` then relogin.
3. Restore snapshot; `hostnamectl` back to original. Narrate: "the
   mistake never happened."
4. Ask: "What does this make possible in this course?" (expected:
   "we can try dangerous things" — confirm and constrain: *in the VM
   only; the host never sees any of this*).

**Possible errors & fixes.**

| Error | Fix |
|---|---|
| VT-x/AMD-V disabled in BIOS (VM won't start 64-bit) | BIOS enable guide is in SETUP.md troubleshooting; loaner USB VM otherwise |
| Install hangs at 30% ("copying files") | almost always insufficient host RAM w/ browser open; close, resume |
| Student forgot password on first login | fastest path: reinstall (20 min, low stakes — it *is* week 2) |

**Classroom activity.** The restore race (pairs) — first pair to
recover the renamed hostname wins. It converts snapshot knowledge into
reflex.

**Time allocation & pacing.** S3 is hands-on heavy: resist lecturing
past 15 min. S4: if the demo runs long, the four-act recap slide can be
assigned reading.

**Summary & exit.** "You now own a machine you can't permanently break."
Exit: the three `hostnamectl` facts. Bridge: "Week 3 — the *words*."

---

## Unit-level instructor checklist

- [ ] Two spare ISOs on USB (install ISO corruption happens weekly)
- [ ] Verify projector displays VM text at 1024×768 (console font legibility)
- [ ] Read [instructor-manual/module-teaching-guides/unit-01-foundations.md](../instructor-manual/module-teaching-guides/unit-01-foundations.md) before S3
- [ ] Exit tickets collected both sessions; fuzzies addressed by next session
