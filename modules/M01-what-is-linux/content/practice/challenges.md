# Module 01 — Challenge Exercises

Open-ended tasks. ≥3 write-ups in `lab-log.md` are required for the module; each
write-up includes: what you tried, commands used, what surprised you. Difficulty:
★ routine · ★★ stretch · ★★★ research-y. All tasks are **safe** — no destructive
commands are ever needed; the answers live in reading, comparing, and writing.

## ★ C1 — The translator

Write a one-page cheat card (by hand or editor) translating these five questions
into the exact commands that answer them:

1. What distro and version is this machine?
2. Which kernel, which architecture?
3. How much RAM is available right now?
4. How many CPUs, what model?
5. Who am I and in which groups?

Trade cards with a classmate and grade each other's by *running* them.

## ★ C2 — Man page speedrun

Using only man pages (no web): find (a) the `ls` option that sorts by file size,
(b) the `date` format for the week number of the year, (c) what `id -Gn` shows.
Record the exact option strings and quote the man-page lines.

## ★ C3 — Prompt story

Take a screenshot of your prompt (or copy the text). Annotate every field:
username, hostname, path, `$`. Then write the prompt you would *expect* to see
as root on the same machine in the same directory. Explain the difference in one
sentence.

## ★★ C4 — Distro briefing

Pick a distribution you have never used (Fedora, openSUSE, Arch, Mint — not
Ubuntu). From its **official site/docs only**, write 6 lines: family, package
manager, release model, support window, one notable difference from Ubuntu, one
sentence on who should choose it.

## ★★ C5 — The honest VM vs WSL2 review

You installed one of them; research the other enough to write a fair comparison
for your own notes: 2 strengths, 2 weaknesses, and a one-line "pick X if…, pick
Y if…" recommendation for an incoming student with a 16 GB-RAM Windows laptop.

## ★★ C6 — Everything-is-a-file field trip

Read `man 5 proc` (section 5!) for ten minutes, then find and report: which /proc
file would tell you (a) the system's uptime, (b) the kernel's view of memory
without `-h` formatting, (c) your own process's ID-space? Verify two of your
answers with `cat`. (Uptime: `cat /proc/uptime` — compare with `uptime`'s output.)

## ★★ C7 — Exit-code census

Collect exit codes from ten different commands you have run this module
(successes and deliberate failures). Tabulate: command, exit code, your
hypothesis of *why that number*. Any non-0/1 code deserves one man-page lookup
(`man ls` → EXIT STATUS section, if present; `man bash` → Exit Status).

## ★★★ C8 — Source-code safari

Visit the GNU coreutils manual online (linked in Lesson 7's further reading).
Find the documentation page for `echo`. Compare what it documents with `help echo`
in your shell — differences? (e.g., `-e`, `-n` behavior). Write 5 lines on why
"the manual on my machine" and "the manual on the web" can disagree — and which
one wins on *your* server.

## ★★★ C9 — Design the course's dataset identity card

Imagine Module 8 will hand you `sales-2019-q1.csv`. Design the "identity block"
for *datasets* by analogy with Lesson 4's system identity: which 5 facts would you
want to know about any data file before analyzing it (size? line count? encoding?
…)? For each fact, guess whether a command exists (name it if you know one; else
write "TBD — later module"). Keep this list; later modules let you tick it off.

## ★★★ C10 — Teach-back

Write a 10-line explanation of "what is Linux?" aimed at a smart 12-year-old,
using *none* of these words: kernel, distribution, terminal, user space. If you
can't avoid a term without losing accuracy, that's a sign you've found the load-
bearing concepts — list them and why they're hard to replace.
