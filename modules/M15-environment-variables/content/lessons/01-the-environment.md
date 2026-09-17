# Lesson 1 — The Environment

> Module 15 · Unit 3 · Difficulty: Beginner → Intermediate
> Reading time: ~20 min · Lab: [Lab 1](../labs/lab-01-env-safari.md)
> Up next: [Lesson 2 — export and PATH](02-export-and-path.md)

---

## 1. What the environment is

Every process carries a small bag of **name=value strings** called
its *environment*. It's configuration that travels with the process —
who it runs as (`USER`, `HOME`), where it looks for programs
(`PATH`), which language it speaks (`LANG`), and whatever else a
parent chose to pass along.

Two properties define everything else in this module:

1. **Inheritance:** a process's environment is a *copy* of its
   parent's (minus what the parent changes). Changes never flow
   *upward* — a child cannot edit its parent's environment.
2. **Per-process truth:** there is no global "the environment" —
   there is only *this shell's*, *that script's*, *that service's*.
   When two windows disagree, both are right.

## 2. Inspecting the bag

```console
$ printenv | sort | head        # the whole bag, sorted
$ printenv HOME USER SHELL LANG # specific names
$ echo "$PATH"                  # expansion at work
$ env | grep -i proxy           # filtered
```

`printenv VAR` (no `$`) vs `echo "$VAR"` — worth internalizing early:
`printenv` takes the *name*; expansion with `$` happens *before* the
command runs. When `$VAR` is unset, `echo` prints emptiness and lies
by looking fine; `printenv` exits non-zero and tells the truth. M19
makes this distinction a habit with `set -u`.

## 3. Inheritance, demonstrated

The one experiment that makes inheritance permanent memory:

```console
$ FRUIT=mango bash -c 'echo "child sees: $FRUIT"'
child sees: mango
$ FRUIT=mango bash -c 'FRUIT=papaya; echo "child changed: $FRUIT"'
child changed: papaya
$ echo "parent still: $FRUIT"
parent still:
```

The child's copy is its own; the parent's bag was never touched.
**Consequence for everything you automate:** if a script or cron job
(M25) needs a variable, *someone must give it to that process* —
"it works in my shell" means "my shell's parents gave *me* one."

## 4. Where the bag comes from at login

Chain of custody on Ubuntu:

```
PAM → (login shell) bash reads: /etc/profile → /etc/profile.d/*.sh
      → ~/.profile (which sources ~/.bashrc if bash)
Every other terminal: bash reads ~/.bashrc only
GUI apps / services: inherit from systemd, not your shell (M20)
cron jobs: inherit almost nothing (M25)
```

That's why `~/.bashrc` is the everyday edit, `~/.profile` the
login-time one — Lesson 3 dissects the pair and the `bash: file not
found` class of bugs that comes from mixing them up.

## 5. Reading the defaults like an admin

A few variables carry most of the weight in this course:

| Variable | Owner concept | Course module that leans on it |
|---|---|---|
| `PATH` | program lookup order | M15 (Lesson 2), M27 (venvs) |
| `HOME` | "your" files | M06, M26 backups |
| `USER`/`LOGNAME` | identity | M14 (sudo changes `USER` — watch it) |
| `PS1` | prompt | M19 |
| `LANG`/`LC_*` | localization, collation order | M07's `sort` behavior |
| `EDITOR` | which editor opens | git commit (M26), crontab -e (M25) |
| `PYTHONPATH` | import search hack | M27 — and why venvs beat it |

**Exercise in reading:** run `env | sort | wc -l` — then explain why
the number differs between your login shell and a fresh
`bash --norc` child.

## 6. DS connection

When your notebook "can't find the data": the *notebook kernel* has a
different environment than the shell that launched Jupyter. Same
skill, different process. M27's venv activation is literally
environment surgery (`PATH` first-entry swap + `VIRTUAL_ENV` set) —
and M25's cron-vs-shell mystery is inheritance taught the hard way.
This module is the microscope for both.

---

**Key takeaways**

- Environment = per-process name=value bag, inherited by copy,
  never edited upward.
- `printenv` vs `echo "$VAR"`: name vs expansion; honest failure vs
  silent emptiness.
- The login chain decides which file carries which change — Lesson 3.

**Check yourself:** in the §3 experiment, why did the *first* command
see `mango` but the parent saw nothing? Where exactly did `mango`
travel?

**Next:** [Lesson 2 — export and PATH](02-export-and-path.md)
