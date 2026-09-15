# Lesson 6 — Getting Help: man, info, --help

> Module 01 · Unit 1 · Difficulty: Beginner
> Reading time: ~25 min · Lab: [Lab 2 — Man page tour](../labs/lab-02-man-page-tour.md)
> Up next: [Lesson 7](07-command-syntax.md)

---

## 1. The skill this course keeps grading

Here is the honest secret of this profession: **nobody remembers all the options.**
Admins with 20 years of experience look things up constantly. The difference between
a beginner and a professional is not memorization — it is that the professional
*knows where the answers live and reads them fluently*.

On a Linux system, the answers live on the machine itself, always available, even
offline, even mid-incident on a server at 3 a.m. This lesson teaches you to open
that documentation — which then makes every later lesson easier.

## 2. man: the manual system

`man` (manual) shows the reference page — the "man page" — of a command:

```console
$ man ls
```

The page opens in a pager called `less` (a read-only viewer). Navigate it:

| Key | Action |
|---|---|
| **Space** / **b** | Next / previous screen |
| **↑ / ↓**, **j / k** | Line-by-line scroll |
| **/word** | Search forward (`n` = next hit, `N` = previous) |
| **g** / **G** | Top / bottom |
| **q** | Quit back to the shell |

A typical man page has these sections (order can vary slightly):

```
LS(1)                                   User Commands                                  LS(1)

NAME        ls - list directory contents
SYNOPSIS    ls [OPTION]... [FILE]...
DESCRIPTION List information about the FILEs...
OPTIONS     -a, --all    do not ignore entries starting with .
            -l           use a long listing format
...
EXAMPLES, AUTHOR, SEE ALSO
```

| Section | What it gives you |
|---|---|
| **NAME** | The one-line summary — what this is |
| **SYNOPSIS** | The command's grammar (decoded in Lesson 7) |
| **DESCRIPTION** | What it does, behavior details |
| **OPTIONS** | Every flag, with semantics |
| **EXAMPLES / SEE ALSO** | Worked cases; related commands |

**Fast paths when you don't want the full page:**

- `man ls` then `/^ *-a` — jump to the `-a` option.
- `man -k copy` — search all short descriptions for "copy" when you don't know the
  command name yet (same as `apropos copy`).
- `man man` — yes, the manual has a manual. Start there when lost.

## 3. Man page sections: why `man printf` lies to you (slightly)

The manuals are organized into **numbered sections**. The ones you should know now:

| Section | Contents | Examples |
|---|---|---|
| 1 | User commands | `ls`, `grep`, `bash` |
| 5 | File formats and conventions | `fstab`, `proc`, `crontab` |
| 7 | Miscellaneous (protocols, ASCII…) | `ascii`, `signal` |
| 8 | Administration commands | `mount`, `useradd` |

Why numbering matters: names collide across sections. Both the shell built-in
`printf` and the C library function `printf` exist. `man printf` shows **section 1**
(the command), `man 3 printf` shows the C function. When a topic seems to be "the
wrong printf", name the section explicitly: `man 5 crontab` (the crontab *file
format*) vs `man 1 crontab` (the command).

## 4. The quicker answers: `--help`, `help`, `info`

**`--help`** — most commands print a compact usage summary and exit:

```console
$ date --help
Usage: date [OPTION]... [+FORMAT]...
  or:  date;
Display the current time in the given FORMAT, or set the system date.
...
```

Rule of thumb: **`--help` for a quick reminder, `man` for understanding.** On shared
servers and minimal containers, some tiny environments ship man pages without `info`,
but nearly everything supports `--help`.

**`help`** — man pages document *programs on disk*; some commands you type are
actually **shell built-ins** that live inside bash itself. For those, use bash's own
`help`:

```console
$ type cd
cd is a shell builtin
$ help cd
cd: cd [-L|[-P [-e]] [-@]] [dir]
    Change the shell working directory.
...
```

`type` tells you *what a name is* — builtin, program, or alias — so you know which
help system to ask. (`which` answers the related question "which file would run?",
e.g. `which ls` → `/usr/bin/ls`.)

**`info`** — the GNU project's own hypertext documentation system, richer than man
for GNU tools (full nodes, menus, cross-references):

```console
$ info coreutils
```

Navigate with arrows, Enter to follow a link, `n`/`p` for next/previous node, `q`
to quit. Honest guidance: man is the daily driver in this course; info matters mainly
for deep GNU manuals (coreutils, bash); `--help` covers quick lookups. Recognize all
three so no documentation on a server is closed to you.

## 5. Reading documentation like a data scientist

Treat man pages exactly like API docs — same skill, different library:

1. **Start at NAME and SYNOPSIS.** One line: what it is; one line: how it's called.
2. **Scan DESCRIPTION for behavior you depend on** — sort order, defaults, edge cases.
   This is where "sort considers `10` smaller than `9`" type surprises are documented
   (it compares lexicographically unless you ask for `-n` — Module 8).
3. **Read the exact option you need, not the whole page.** `/`-search is your friend.
4. **Cross-check SEE ALSO** — the related commands listed there are how pros discover
   the better tool (`ls` → see also `stat`, `find`, `du`).
5. **Version honesty:** man pages describe *your installed version*. A blog may show
   different behavior because their version differs. On disagreement, the local page
   wins for *your* machine — and CONTRIBUTING.md tells you to file an issue if *we*
   got it wrong.

The meta-skill compounds: every later module assumes you can look up its commands'
options rather than memorizing them from the lesson text.

## 6. When there is no man page

```console
$ man sudo      # works: sudo ships a page
$ man lab-log   # No manual entry for lab-log — it's not a command, just a file
```

Not every word has a manual. For anything conceptual (what is a "unit" in systemd?
what is a "mount point"?), your path is: this course's glossary → the module lesson →
the official project docs (linked in each lesson's Further reading) → `man -k` for
discovery. And of course: the course's own [references](../../../../resources/references.md).

## Exercises (lab-log.md)

For each task, record the *command you used* and *one line of what you learned*:

1. Open `man ls`. Use `/`-search to find what `-h` does. Quote its exact wording.
2. Which man section documents the file `/etc/fstab`? (Hint: `man -k fstab`.)
3. `type cd`, `type ls`, `type echo` — which are builtins? Run `help` on one and
   `man` on another; which worked and why?
4. Find and read the SYNOPSIS of `date`. Predict what `date +%Y-%m-%d` prints,
   then verify.
5. `man -k compress` — name two commands that appear and one sentence on when each
   is used (read their NAME lines).
6. In `info coreutils`, find the node about `sort`. One new fact you learned that
   `sort --help` did not show.
7. Your course claim: "the local man page beats a blog post." Argue why in two
   sentences, then give the counter-case (when the blog is right).

## Check yourself before Lesson 7

- I can open, navigate, search, and quit a man page without help.
- I know what sections 1, 5, 8 contain and can fetch a specific section.
- I can distinguish builtin vs program with `type` and choose `help` vs `man`.
- `--help` vs `man` vs `info`: I know which to reach for and when.

## Further reading (official sources)

- man(1) and less(1) man pages (in your VM: `man man`, `man less`)
- Linux man-pages project — <https://www.kernel.org/doc/man-pages/>
- GNU Info documentation — <https://www.gnu.org/software/texinfo/manual/info/>

Next: [Lesson 7 — Command Syntax](07-command-syntax.md)
