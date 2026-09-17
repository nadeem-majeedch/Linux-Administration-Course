# Module 03 Quiz — Architecture

> 20 questions. Answer first, then check
> [quiz-answers.md](quiz-answers.md). Scope: lessons 1–4.
> Most questions ask *why*, not *what* — the answers are not on any
> cheatsheet.

## Section A — The layer cake (Q1–5)

**Q1.** Name the seven layers of the Linux stack in order. For each,
name one command you have used this course that *lives* there.

**Q2.** A colleague says: "Python writes my CSV straight to the disk."
Unpack the claim: list every layer boundary that write crosses, and
name the exact kernel subsystem that finally touches the medium.

**Q3.** Why can you replace the entire user space (install a different
distro) without ever touching the kernel — but not vice-versa without
a reboot? Answer in terms of Lesson 1's two truths.

**Q4.** "Everything is a file" — which layers *provide* this illusion,
and which layer *consumes* it? Use `/proc/cpuinfo` and a regular file
in `/home` as your two examples.

**Q5.** CUDA — why is it called a *stack*? Name its four layers in
order, and state which layer the Linux kernel itself belongs to.

## Section B — Kernel space vs user space (Q6–10)

**Q6.** A buggy user program calls `open("/etc/shadow", O_RDONLY)`.
The call fails. Which side *decided* it fails — the program, libc, or
the kernel? Why must it be that side (one sentence on the security
argument)?

**Q7.** Two programs crash: one is a notebook kernel, one is a GPU
driver bug inside the kernel. What does the system look like after
each? Name the evidence tool for each aftermath.

**Q8.** What is a system call, in one sentence? What is `libc`'s role
in one sentence? Why did M02 say Alpine binaries differ — in terms of
this lesson?

**Q9.** `strace -c` shows your one-line Python program made 400
syscalls before printing anything. Explain the traffic: what work
must happen in user space before your code runs?

**Q10.** Your `ps` output shows a process in `D` state for minutes.
Which side of the wall is it waiting on, and why can't you `kill -9`
it? (M18 will formalize signals; reason from today's lesson.)

## Section C — Boot (Q11–15)

**Q11.** Name the four acts of boot. For each, one sentence: what it
hands to the next act.

**Q12.** The initramfs is deleted from `/boot`. The kernel is intact.
Predict Act 3's behavior and explain *why* the initramfs exists at all
(one sentence on drivers, one on root mounting).

**Q13.** Why does editing GRUB's `linux` line change only one boot?
Where does the change *live*, and what mechanism restores the normal
boot next time?

**Q14.** `systemd-analyze` reports: firmware 1.2s, loader 0.4s,
kernel 3.1s, userspace 22s. Which act do you investigate first, and
what one command ranks the suspects?

**Q15.** Why is `journalctl -b -p err` (boot-scoped) the right first
command after a "server rebooted and now X is broken" report, rather
than `journalctl` alone?

## Section D — User-space anatomy (Q16–20)

**Q16.** List the five user-space actors in Lesson 4's keystroke
walkthrough, in order. Which actor's failure produces "command not
found"?

**Q17.** `ldd /usr/bin/ls` lists `libc.so.6`. Explain in two sentences
what "shared" means economically (memory) and what risk it creates
for system updates (M16 will formalize the policy).

**Q18.** You replace `/usr/lib/x86_64-linux-gnu/libfoo.so.1` with a
new build while two daemons using it are running. What do those
daemons run until restarted, and why — one sentence referencing
`/proc/*/maps`?

**Q19.** `file` says a binary is "statically linked." What changes for
the loader and for library updates? When would you *want* this?

**Q20.** Your `python3` resolves through three symlinks to
`python3.12`. You `apt install python3.13`. Without changing PATH,
which Python does bare `python3` run, and why — name the actor that
decides and the mechanism it uses.
