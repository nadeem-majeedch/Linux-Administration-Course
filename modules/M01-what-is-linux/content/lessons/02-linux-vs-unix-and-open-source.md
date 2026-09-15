# Lesson 2 — Linux vs Unix & Open Source

> Module 01 · Unit 1 · Difficulty: Beginner
> Reading time: ~20 min · Lab: none · Up next: [Lesson 3](03-distributions-and-ubuntu.md)

---

## 1. Unix: the ancestor

**Unix** is an operating system developed at Bell Labs in 1969 by Ken Thompson and
Dennis Ritchie. Its design was revolutionary and durable — so durable that almost
every major OS today is either a Unix descendant or borrows its ideas.

Unix's founding ideas (you will live inside all of them this course):

| Idea | What it means | Where you'll feel it |
|---|---|---|
| **Everything is a file** | Devices, processes, and sockets appear as files you can read | M03 (`/proc`), M07, M09 |
| **Small tools, combined** | Many simple programs that do one thing well, joined by pipes | M08–M09 |
| **Plain text as interface** | Configs and outputs are text; text is universal | M07–M08, M24 |
| **Multi-user from birth** | Several people share one machine with separated rights | M12–M14 |
| **Hierarchical filesystem** | One tree of directories starting at `/` | M06 |

Unix spread to universities (the source code was shared for study), mutated into
dozens of variants — **BSD**, **Solaris**, **AIX**, **HP-UX** — and its concepts
became a standard: **POSIX**, the Portable Operating System Interface, which defines
what "Unix-like" behavior means.

## 2. So what is the difference between Linux and Unix?

**Unix is a family of operating systems with shared design and a shared lineage;
Linux is a *re-implementation* of that design, written from scratch, with no Unix
source code in it.**

Think of it this way:

- Unix is the original blueprint and the OS family built from it.
- Linux is a house built to the same blueprint, by different people, starting from
  zero — and given away for free.

| | Unix (original family) | Linux |
|---|---|---|
| Born | 1969, Bell Labs | 1991, Linus Torvalds |
| Source code | Proprietary per vendor (except BSD branch) | Open from day one |
| Cost | Historically: expensive hardware + licenses | Free to obtain and run |
| Runs on | Vendor's own machines | Anything: watch → supercomputer |
| Standardized by | POSIX and certification ("UNIX" trademark) | Follows POSIX in practice |
| Examples | Solaris, AIX, HP-UX, macOS* | Ubuntu, Debian, Fedora, RHEL |

\* macOS deserves a footnote: its core (Darwin) descends from BSD Unix, so macOS
*is* a certified UNIX. That is why a Mac's Terminal already feels Unix-ish — you can
practice many course commands on it — but the course's Ubuntu environment remains the
reference, because macOS differs in packaging (`brew` vs `apt`), boot system, and
directory layout.

**What this means for you practically:**

1. Skills transfer. Command-line habits learned on Ubuntu work on every Unix-like
   system: RHEL servers, macOS, BSD firewalls, WSL2.
2. The vocabulary transfers. "Everything is a file", pipes, man pages, permissions —
   all Unix ideas Linux inherited.
3. Certification doesn't matter to you; behavior does. Linux is "Unix-like" —
   POSIX-conformant in practice — and that is why your skills are portable.

## 3. Software with visible source: open source

To understand Linux's explosion, you need one distinction: **source code** vs
**binary**.

- **Source code** = the human-readable instructions (like `.py` files for Python).
- **Binary** = the compiled program your CPU runs (like an `.exe`).

Proprietary software ships you binaries only — you can use it, not study it. **Open
source software** ships the source too, under a **license** that grants everyone
certain rights.

## 4. The four freedoms (and the licenses that encode them)

The Free Software Foundation defines freedom in software as:

1. **Freedom to run** the program, for any purpose.
2. **Freedom to study** the source code.
3. **Freedom to modify** it.
4. **Freedom to redistribute** copies, modified or not.

Licenses turn these ideas into law. The two big families:

| License family | Core rule | Examples | Practical consequence |
|---|---|---|---|
| **Copyleft** | If you distribute the software, you must distribute your source changes under the same license | GPLv2 (Linux kernel), GPLv3, AGPL | Improvements stay free |
| **Permissive** | Almost no conditions: use, modify, embed in proprietary products | MIT, BSD, Apache 2.0 | Maximum adoption; this course's own LICENSE is MIT |

Both are "open source" and "free software". The split is philosophical (must future
versions stay free?), not practical for you today: either way you can read, run, and
learn from the code.

> **Terminology, settled:** "free software" (FSF, emphasizes freedom), "open source"
> (OSI, emphasizes the development model), "FOSS/FLOSS" (both together). In this
> course we say *open source* and mean all of it.

## 5. Why open source matters *to you* (not just to philosophy)

This is the section to remember. Open source is why data science looks the way it does:

1. **Reproducibility.** You can pin exact versions of every tool (`pip freeze`,
   apt version pinning in M16, Docker images in M28) because everything is inspectable
   and rebuildable. Try pinning a closed binary that phones home.
2. **No licensing ceiling.** A 500-node GPU cluster costs hardware, not 500 licenses.
   Universities and startups run on this.
3. **You can read the code.** Does `sort` order 10.0 after 9.0? Read its manual, or
   its source; ask upstream. With enough skill, you can even fix a bug in your OS.
4. **The ecosystem you use is open source.** Python, pandas, NumPy, scikit-learn,
   PyTorch, Jupyter, R, PostgreSQL — all of it. Linux is simply the foundation layer
   of the same phenomenon.
5. **Your contributions are possible.** From this course's own CONTRIBUTING.md to
   kernel patches, the ladder from user to contributor is open.

## 6. Free vs open: the one-sentence versions

- **Free software:** your freedom to run, study, modify, share is the point.
- **Open source:** the development model (visible source, collaboration) is the point.
- **Freeware** (not the same!): zero price, closed source. Beware the classic exam trap:
  free ≠ open source ≠ freeware.

## Exercises (lab-log.md)

1. Name three Unix design ideas you will personally meet later in this course and
   the module where each appears.
2. In two sentences: why is Linux "Unix-like" rather than "Unix"? Why does the
   distinction not change your day-to-day skills?
3. Your MacBook friend says "I don't need this course, macOS is Unix." Give one
   true part of their claim, one caveat, and the course's counter-argument.
4. Explain copyleft vs permissive licenses to a classmate using one sentence each
   and one example of what you could (and couldn't) do with code under each.
5. Pick a tool you already use (pandas, VS Code, Excel). Which are open source?
   For one open-source pick, name one concrete benefit you get *as a student* from
   its source being available.
6. Why does open source make *reproducibility* easier? Answer in exactly three
   sentences a DS manager would accept.

## Check yourself before Lesson 3

- I can define Unix and place Linux in its family tree.
- I can state what POSIX is and why it makes my skills portable.
- I can explain the four freedoms and name two licenses from each family.
- I can give three practical (non-ideological) reasons open source matters in data science.

## Further reading (official sources)

- gnu.org: philosophy of free software — <https://www.gnu.org/philosophy/free-sw.en.html>
- Open Source Initiative — <https://opensource.org/licenses>
- The Open Group (UNIX trademark/standards) — <https://www.unix.org/what_is_unix.html>
- Linux Kernel Organization — <https://www.kernel.org/>

Next: [Lesson 3 — Distributions & Ubuntu](03-distributions-and-ubuntu.md)
