# Challenge Exercises — M03

> All challenges run on your own VM; C4 touches a second throwaway
> container. Nothing privileged except where fenced.

## C1 — Boundary census

Pick three commands of increasing "weight": `true`, `ls /`, and
`python3 -c 'pass'`. For each, `strace -c …` and record: total
syscalls, top three by count, and the single most expensive by time.
Then answer: **what is syscall count a function of** — arguments?
binary size? loaded machinery? Test your hypothesis by strace-ing
`ls /usr` vs `ls /usr/share` (same binary, different work).

## C2 — The wall, drawn from evidence

Produce a one-page annotated diagram of *your machine's* stack.
Requirement: every layer boundary must carry a real evidence line
(a command + its output excerpt) that *proves* the boundary exists on
*this* machine — e.g. the firmware station from Lab 1, `/proc/cmdline`
for the kernel handoff, `ldd` for the libc seam, `strace` total for
the syscall wall. Diagrams without evidence score zero; this is the
M03 exam in miniature.

## C3 — Boot forensics (no reboot needed)

Using only `journalctl -b`, `systemd-analyze [blame|critical-chain]`,
and `/proc/cmdline`, reconstruct and write up this boot's four acts
with timestamps: when did the kernel start, when did userspace start,
which three units took longest, and which (if any) failed? Close with
a verdict: was this boot *clean*, by your own definition — and what
would make you change that definition?

## C4 — Same wall, different tenants

Run the same program two ways and compare the user space:

```console
$ strace -c python3 -c 'import sys; print(sys.version)' 2>&1 | tail -3
$ docker run --rm python:3.12-slim sh -c "python3 -c 'import sys; print(sys.version)'"
```

(If Docker isn't set up yet, defer C4 until after M28's Lab 0.)
Questions: which user space did the container run? What stayed the
same across both runs (hint: the kernel — whose?). One-paragraph
answer: **why "a container is user space with a borrowed kernel"**
and what that implies for the *distro identity* commands from M02
inside vs outside the container.

## C5 — The misattributed crash

A teammate reports: "Python segfaulted, it must be a kernel bug."
Design (don't execute) a three-command evidence sequence that would
confirm or refute each of: (a) user-space bug in their code/libraries,
(b) bad shared library loaded, (c) actual kernel-side cause. For
each branch, name the tool *and* what output would settle it. Grade:
does the sequence run in <2 minutes on a production-like box without
installing anything?

## C6 — Symlink archaeology

Without using Python itself, map *every* interpreter on your VM:
find all files named `python3*` in the standard PATH directories,
resolve each with `readlink -f`, and record which one wins for bare
`python3` — then explain, in actors-of-Lesson-4 terms, *why* the
winner wins and what single change would dethrone it (still without
PATH edits). This is the M27 pre-fix mental model.
