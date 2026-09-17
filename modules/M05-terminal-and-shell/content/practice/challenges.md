# Module 05 Challenges — Terminal & Shell

> Attempt before peeking; these exercise *judgment*, not recall.
> All are safe: worst case, `exit` the shell and open a new one.
> Difficulty: ★ beginner → ★★★ stretching.

## 1. The `type` census (★)

Run `type -a` on a dozen commands you've met so far and classify each
as **alias / builtin / file**. Find at least one of each category on
your system. Deliverable: a two-column list with one surprise
explained — *why* is that command the category it is? (Hint from
[Lesson 5](../lessons/05-aliases-and-history.md): `ls` is rarely just
`ls`.)

## 2. Explain the exit codes (★)

Run each pair and explain the difference in exit codes:

```console
$ man ls            # then quit with q
$ man nonexistentpage
```

Deliverable: which succeeded, what `$?` said, and *why a man page
that "opened and closed" can still count as success*. When would a
script care?

## 3. Man-page archaeology (★★)

Using only `man bash` (search with `/`), find and cite the section
that explains each of these, quoting one line from each:

- what `$?` holds
- what `!!` expands to
- the difference between `~` and `$HOME`

Deliverable: the three quotes plus the man section numbers you found
them in. This is the *skill* the course wants: answering questions
from the primary documentation, not a search engine.

## 4. Design two aliases, defend one (★★)

Create two aliases you would genuinely use daily (one safety alias,
one convenience). Then **delete the convenience one** and justify in
one paragraph: what did the alias save, and what did it cost you in
transparency? (There is no right answer; the defense is graded —
echoes the alias-lifetime rules in [Lesson 5](../lessons/05-aliases-and-history.md).)

## 5. The un-helpable command (★★★)

Find a command installed on your system whose `--help` output is
longer than one screen *and* whose man page is longer than 500 lines
(`man command | wc -l`). Then answer: for a beginner, when is
`--help` better, and when is `man`? Deliverable: your rule of thumb
in three sentences, with the command as the worked example.
