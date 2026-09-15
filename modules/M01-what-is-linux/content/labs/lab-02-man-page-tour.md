# Lab 2 — Man Page Tour

> Lesson 6 · Time: ~45 min · Risk level: zero (read-only)
> Environment: any Ubuntu system

## Goal

Turn documentation from a last resort into your first reflex. After this lab you
can open, navigate, search, and *use* a man page — including choosing the right
section, discovering unknown commands with `man -k`, and matching the right help
system (`man` vs `help` vs `--help`) to the question.

## Before you start

- [ ] Terminal open; you remember `q` quits the pager (you'll need it constantly)
- [ ] `lab-log.md` ready — every task asks for *the command you used* plus one line learned

## Part 1 — Navigation circuit (10 min)

Open `man man` (the manual about the manual) and complete this circuit:

1. Scroll one screen forward (**Space**) and back (**b**).
2. Jump to the end (**G**) and the beginning (**g**).
3. Search for the word `section` with `/section`; hop hits with **n**.
4. Quit with **q**. Total time spent lost: aim for under 30 seconds — this
   navigation pattern is muscle memory, not knowledge.

Repeat the circuit once with `man ls`. Speed is the point.

## Part 2 — Read for a purpose (15 min)

Answer each with the *page and section you found it in*, quoted briefly:

1. `man ls` — what exactly does `-h` do? Quote the line.
2. `man ls` — find the option that lists entries *separated by commas*. (Search
   `/comma`.)
3. `man date` — in the SYNOPSIS, what does the `[+FORMAT]` notation tell you?
4. `man date` — find the format controls for a 4-digit year and a zero-padded
   month. Write the command that prints `2026-09-15`-style output and verify it.
5. `man uname` — what does `-a` show that `-r` does not? (Two fields minimum.)
6. `man free` — what is the difference between *free* and *available* columns?
   Quote the relevant DESCRIPTION sentence. (This closes the question Lesson 4
   left open.)

## Part 3 — Sections and collisions (10 min)

1. Run `man -k fstab`. How many results? Which *sections* are they in?
2. Open the fstab page that is **not** section 8 (try `man 5 fstab`). What does
   this section document — the command or the *file format*?
3. Run `man printf`, then `man 3 printf`. Which one documents a *command you
   could run in the shell*? Which one is for C programmers?
4. In one sentence in your log: why do man pages have numbered sections?

## Part 4 — Discovery: finding commands you don't know (10 min)

`man -k <word>` searches every short description. Use it like a search engine:

| Task | Suggested search | Record |
|---|---|---|
| Find disk-usage commands | `man -k disk` | Two names + one line each |
| Find memory-information commands | `man -k memory` | One name beyond `free` |
| Find something for calendars | `man -k calendar` | Does `cal` exist? Try it. |
| Find compression tools | `man -k compress` | Two names + when each is used |

Pick one newly discovered command and skim its full page. What does it do that
you could not do before?

## Part 5 — Right help for the right question (10 min)

For each name below, first *predict* the right tool (`type` them to check):
builtin or program? Then use `help NAME` or `man NAME` accordingly.

| Name | Prediction | `type` says | Help that worked |
|---|---|---|---|
| `cd` | | | |
| `ls` | | | |
| `echo` | | | |
| `date` | | | |
| `history` | | | |

Finally: run `ls --help | head -20` and compare with `man ls`'s first screen.
Write one line: when would you reach for `--help` vs `man`?

## Wrap-up checklist

- [ ] Navigation circuit under 30 seconds without notes
- [ ] Six Part-2 answers logged with quotes
- [ ] You can explain man sections 1 vs 5 vs 8 in one sentence each
- [ ] Two *new-to-you* commands discovered via `man -k` and tried
- [ ] One line in your log: "the help system I will use first from now on is …"

## What you can now do

You can teach yourself any command on any server without internet access. That is
the single most career-relevant skill this module delivers — every later lesson
assumes it.
