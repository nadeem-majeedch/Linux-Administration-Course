# Unit 1 Lecture Slides — Foundations of Linux (M01–M04)

> **Delivery:** Sessions 1–4 (Weeks 1–2) · ~90 min each · For teaching
> notes, see [../speaker-notes/unit-01-foundations-notes.md](../speaker-notes/unit-01-foundations-notes.md)
> Slide format: content → delivery notes → demo suggestion → student question.

---

# Slide 1 — Title

## Slide Content
**Linux Administration: Zero to Hero**
Unit 1 — Foundations (M01–M04)
BS Data Science · From zero experience to your own Ubuntu server

## Instructor Delivery Notes
Housekeeping first (5 min): VM requirements on the board, SETUP.md link
on screen. Promise of the unit: *by week 3 you will be fluent at a
terminal you built yourself.*

## Visual or Demonstration Suggestion
Photo of a datacenter rack beside a laptop — "both run the same OS family."

## Student Question
"Name one thing you do on a computer that you think touches an operating system directly."

---

# Slide 2 — Course context: why a DS degree needs Linux

## Slide Content
- Jupyter servers, GPU clusters, cloud VMs: **Linux**
- Python environments, permissions, datasets at scale: **Linux**
- Every tool in your DS stack runs *on* it — the OS is not optional knowledge
- Course promise: you leave administering your own server, capstone-proven

## Instructor Delivery Notes
Anchor in their world: show a real job posting for a data scientist
mentioning Linux/SQL/Python. The stack diagram comes in Slide 4 — resist
explaining it yet.

## Visual or Demonstration Suggestion
Screenshot of a real `htop` on an ML server — "someone here is the admin."

## Student Question
"Who has used SSH or seen a terminal? What were you doing?"

---

# Slide 3 — What is an operating system?

## Slide Content
- The layer between **hardware** (CPU, RAM, disks) and **applications**
- Three jobs: share hardware fairly, protect programs from each other,
  provide useful abstractions (files! processes! network!)
- Kernel = the core of the OS, always resident; everything else is programs

## Instructor Delivery Notes
Analogy that lands: the OS is the *building manager* — allocates rooms
(memory), enforces who-enter-which-door (permissions), fixes plumbing
(drivers). Don't define "distribution" yet; Slide 5 does it.

## Visual or Demonstration Suggestion
Layer diagram: hardware → kernel → system libraries → applications.

## Student Question
"Your Python script writes a CSV. Who actually touches the disk?"

---

# Slide 4 — Where "Linux" sits: the full stack

## Slide Content
```
applications (python, git, jupyter)
system libraries (glibc)
system utilities (bash, coreutils)
Linux KERNEL  ← the thing called "Linux"
hardware
```
- "Linux" strictly = kernel; "a Linux system" = kernel + GNU + utilities + apps

## Instructor Delivery Notes
This is the precision slide. GNU/Linux naming fight: 30 seconds of
history, then move on — the *useful* takeaway is that a distro bundles
kernel + userland.

## Visual or Demonstration Suggestion
Same layer diagram, annotated with commands they'll meet: `ls` (utilities), `bash` (shell), `python` (app).

## Student Question
"Is Android a Linux system? Argue both sides in 30 seconds."

---

# Slide 5 — Distributions: Linux with a package manager

## Slide Content
- A distro = kernel + userland + **package manager** + release policy + support
- Families: **Debian** (→ Ubuntu) · **Red Hat** (→ Fedora/RHEL) · **Arch** (rolling)
- Our tool: **Ubuntu LTS** — 24.04: 5 years of security updates, huge documentation trail
- Same kernel lineage; different packaging and release rhythm

## Instructor Delivery Notes
Show the family tree, then immediately make it practical: "the exam asks
you to *identify* a distro from evidence — `cat /etc/os-release`."
Distribution-awareness over distro-war opinions.

## Visual or Demonstration Suggestion
`cat /etc/os-release` output projected; circle `ID=ubuntu`, `VERSION_CODENAME`.

## Student Question
"Your server says `dnf: command not found`. Which family is it from?"

---

# Slide 6 — Knowledge check + activity

## Slide Content
1. What is the difference between the *kernel* and a *distribution*?
2. Why does this course pin Ubuntu **LTS**?
3. Task: in pairs, draw the stack and place `bash`, `python`, `glibc`, the kernel.

## Instructor Delivery Notes
Circulate during the pair task — the libc position is the discriminating
answer. Debrief with the Slide 4 diagram.

## Visual or Demonstration Suggestion
Timer on screen; 4 minutes for the pair task.

## Student Question
(see task 3 — the drawing *is* the check)

---

# Slide 7 — Linux architecture: the four-act boot

## Slide Content
```
FIRMWARE (UEFI) → BOOTLOADER (GRUB) → KERNEL + initramfs → systemd → login
   self-test        picks the kernel      drives the disk    services start
```
- Why you care: "server won't boot" decomposes into these acts

## Instructor Delivery Notes
Keep it to 12 minutes — depth arrives in M20. The gift here is
*vocabulary* for failure: "stuck in GRUB" vs "stuck at services."

## Visual or Demonstration Suggestion
Boot the instructor VM with the projector on; name each act as it happens.

## Student Question
"Where in the four acts would a *full disk* first cause trouble?"

---

# Slide 8 — Kernel space vs user space

## Slide Content
- User programs ask the kernel via **syscalls** — the only door to hardware
- Crash in user space → one program dies; crash in kernel space → whole system
- That asymmetry is *why the boundary is a security boundary*
- `ls /proc`, `ls /sys` — windows into the kernel's own bookkeeping

## Instructor Delivery Notes
The Python-writes-a-CSV story: Python → libc `write()` → syscall →
kernel → disk. Make them say the chain back. This is the unit's most
exam-dense idea.

## Visual or Demonstration Suggestion
`cat /proc/cpuinfo | head` live — "reading kernel bookkeeping as files."

## Student Question
"Why can't your Python code just write bytes to the disk itself?"

---

# Slide 9 — CLI vs GUI: why the terminal wins here

## Slide Content
- GUI: discoverable, slow to automate, one machine at a time
- CLI: scriptable, composable, works over a 56 KB link to a GPU server, *recordable*
- Reproducibility: commands are text → they can live in Git → they can be re-run exactly

## Instructor Delivery Notes
Their future: the GPU server they'll use in year 3 has no desktop. The
terminal is not nostalgia; it's the interface of remote compute.

## Visual or Demonstration Suggestion
Same task twice: rename 200 files by GUI vs `for f in *.jpeg; do mv ...` — time both.

## Student Question
"Name a task you do repeatedly that you'd like to automate."

---

# Slide 10 — Knowledge check + activity

## Slide Content
1. A kernel panic kills the machine; a crashed `python` doesn't. Why?
2. Pairs: trace "Jupyter serves you a notebook" through the stack.
3. Task: `ls /proc` — find three files whose names suggest their purpose.

## Instructor Delivery Notes
The Jupyter trace is the synthesis task for the session — accept any
chain that crosses the syscall boundary explicitly.

## Visual or Demonstration Suggestion
Solutions drawn live from student answers.

## Student Question
(see task 2)

---

# Slide 11 — VMs: your safe laboratory

## Slide Content
- A VM = a complete computer **emulated inside your computer**
- Snapshots: freeze the machine; restore = the mistake never happened
- This is what makes safe administration practice possible — break things *here*
- Course rule: risky operations happen in the VM or loopback, never on the host

## Instructor Delivery Notes
Sell the snapshot as a superpower: it converts fear into experiments.
Show the VirtualBox snapshot UI on the projector.

## Visual or Demonstration Suggestion
Take a snapshot; rename `/etc/hostname` content (harmless chaos); restore; diff.

## Student Question
"What would you try first if mistakes were free?"

---

# Slide 12 — Installing Ubuntu: the guided tour

## Slide Content
- ISO → VM optical drive → boot → installer
- Sizing for this course: 2 vCPU · 4 GB RAM · 25 GB disk · user `dsstudent`
- **We never partition the host** — the installer sees the *virtual* disk only
- First login: updates (`sudo apt update` — full lesson in M16)

## Instructor Delivery Notes
This session is 60% hands-on. Instructor installs alongside, projector on
the partition screen, saying out loud: "the installer thinks this *is*
the disk — that's the safety."

## Visual or Demonstration Suggestion
Live install, paused on the "Erase disk" screen for the misconception talk —
*erase which disk? The virtual one.*

## Student Question
"Why is 'Erase disk and install Ubuntu' safe today of all days?"

---

# Slide 13 — First login & the desktop brief

## Slide Content
- Terminal app: your new home (Ctrl+Alt+T)
- `whoami`, `hostname`, `pwd` — three identity commands
- Update now: `sudo apt update && sudo apt upgrade` (what is sudo? next unit deep-dive)
- Take snapshot #1: **clean baseline**

## Instructor Delivery Notes
Slow typing everyone: `sudo` password invisibility freaks beginners —
name it before they type. The baseline snapshot is homework-complete
criteria.

## Visual or Demonstration Suggestion
Password typing with no echo — show it, explain it, normalize it.

## Student Question
"Which of today's three commands answers 'which machine am I on'?"

---

# Slide 14 — Common mistakes (Unit 1)

## Slide Content
- Confusing *distribution* with *kernel* ("install more kernels to be faster")
- Giving the VM 1 GB RAM — then blaming Linux for being slow
- Taking no snapshot before experimenting
- Typing passwords into random "terminal-like" web windows (phishing shape)

## Instructor Delivery Notes
Each mistake = one recovery story from real cohorts. The snapshot one
costs the most time — harp it now, save hours in week 6.

## Visual or Demonstration Suggestion
Before/after screenshots of a 1 GB vs 4 GB VM booting.

## Student Question
"Which of these have you already done?" (honest hands normalize recovery)

---

# Slide 15 — Practical demonstration: the machine reports itself

## Slide Content
```console
$ uname -a                # kernel identity
$ cat /etc/os-release     # distribution identity
$ hostnamectl             # hostname, OS, kernel in one view
$ uptime                  # how long since boot
```
Expected: kernel version string with `x86_64`, `ID=ubuntu`, `VERSION_CODENAME=noble`.

## Instructor Delivery Notes
Have students run each and *read* the output aloud — this is their first
evidence-reading drill. Outputs vary by install; that variance is itself
the lesson (evidence over memorization).

## Visual or Demonstration Suggestion
Split screen: instructor output vs student output; find the differences.

## Student Question
"Which command would prove *which Ubuntu release* a server runs?"

---

# Slide 16 — Data Science connection

## Slide Content
- The stack you just built is a **single-node version of an ML server**
- Same kernel, same package manager, same terminal — the GPU server just has more of everything
- Course thread: every unit ends with "how this looks on the lab server"

## Instructor Delivery Notes
Show a real university-cluster login banner if available; otherwise the
M31 module's server anatomy diagram — that's their week 15 destination.

## Visual or Demonstration Suggestion
Roadmap graphic: Unit 1 → ... → Unit 8 capstone, with "you are here."

## Student Question
"What's one thing this VM can't do that a real ML server can?"

---

# Slide 17 — Unit summary

## Slide Content
- OS = hardware manager; Linux kernel = the core; distro = kernel + userland + package policy
- Four-act boot; syscall boundary; user vs kernel space
- VMs + snapshots = safe practice
- Ubuntu LTS installed, snapshotted, updated — your laboratory exists

## Instructor Delivery Notes
One-line bridging to Unit 2: "You own a machine. Next you learn to
*speak* to it — 30 words at a time."

## Visual or Demonstration Suggestion
The stack diagram, now fully labeled by the class.

## Student Question
"Whisper to your neighbor: what's the difference between sudo and a snapshot?" (both matter, different layers)

---

# Slide 18 — Exit ticket & homework

## Slide Content
**Exit ticket (write before leaving):**
1. One thing that's clearer now
2. One thing still fuzzy
3. `hostnamectl` says *what three things* about your machine?

**HW:** M02 + M03 quizzes; snapshot verification screenshot; read M05 lesson 1

## Instructor Delivery Notes
Collect fuzzies — they seed the Session 5 warm-up. Verify snapshots
before Week 3; a student without one will hit the wall in M06 labs.

## Visual or Demonstration Suggestion
QR/link to the exit form.

## Student Question
(exit ticket *is* the question)

---

## Deck references
- Module sources: [M01](../../modules/M01-what-is-linux/README.md) · [M02](../../modules/M02-linux-distributions/README.md) · [M03](../../modules/M03-linux-architecture/README.md) · [M04](../../modules/M04-installing-linux-vms/README.md)
- Labs: M04 lab 1–2 · Next deck: [Unit 2 — Command Line Fluency](unit-02-command-line-slides.md)
