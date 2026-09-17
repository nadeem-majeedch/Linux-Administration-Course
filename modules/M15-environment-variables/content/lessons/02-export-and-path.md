# Lesson 2 — export, unset, and the Anatomy of PATH

> Module 15 · Unit 3 · Difficulty: Intermediate
> Reading time: ~25 min · Lab: [Lab 2](../labs/lab-02-path-clinic.md)
> Up next: [Lesson 3 — dotfiles](03-dotfiles.md)

---

## 1. The export line: variables vs environment

A shell assignment creates a **shell variable** — visible to the
shell, invisible to children:

```console
$ COLOR=teal
$ bash -c 'echo "child: [$COLOR]"'
child: []
$ export COLOR=teal
$ bash -c 'echo "child: [$COLOR]"'
child: [teal]
```

`export` marks a variable to be **copied into children's
environments**. Equivalents: `export COLOR` (mark the existing one),
or the one-shot form `COLOR=teal somecommand` (environment for *that
command only* — the cleanest tool for one-off overrides, and the
form CI files (M29-ext C) use).

Three precision points:

- `unset COLOR` removes it entirely; `COLOR=` sets it to *empty* —
  different states, and some programs treat them differently.
- `export COLOR=teal bash -c ...` is wrong — `export` doesn't run
  commands; that's what the one-shot prefix form is for.
- Assignments are *not* expanded-when-exported: `export PATH=$PATH:/opt/bin`
  expands *now, in this shell* — the value is frozen at export time.

## 2. PATH: the lookup list, dissected

When you type `python3`, the shell searches `PATH` **left to right**
and runs the first match:

```console
$ echo "$PATH"
/usr/local/bin:/usr/bin:/bin:/usr/games:/home/ds/.local/bin
$ echo "$PATH" | tr ':' '\n' | cat -n     # one entry per line, numbered
```

Read the numbered list as a *priority order*. Two consequences:

- **First match wins** — if two `python3`s exist in listed
  directories, the earlier entry decides. This single sentence
  explains venvs (M27), "wrong gcc", "wrong pip", and half of all
  environment folklore.
- **`.` is not in PATH, by design** — typing `script.sh` fails but
  `./script.sh` works. That's a *security feature*: a malicious
  `ls` in a writable directory cannot shadow the real one. Never add
  `.` to PATH; the muscle memory of `./` is the protection.

## 3. Modifying PATH — the three correct patterns

```console
# Prepend (wins ties) — for toolchains that must shadow:
$ export PATH="$HOME/.local/bin:$PATH"

# Append (loses ties) — for extra convenience dirs:
$ export PATH="$PATH:/opt/tools/bin"

# One-shot — test before committing to a dotfile:
$ PATH="$HOME/opt/bin:$PATH" somecommand --version
```

**Always keep `$PATH` in the value** (unless you *mean* amputation).
The classic accident is `export PATH=/opt/newthing/bin` — now
`ls`, `sudo`, even `bash` may be unfindable, and the fix needs the
full-path knowledge from M06: `/usr/bin/sudo`, `/bin/nano` still work
because you named them absolutely.

**Safety net worth memorizing:** a *new* terminal re-reads dotfiles;
your damage is bounded to the shell where you typed it. Lesson 3's
dotfile rules make even that safer.

## 4. Debugging PATH like a surgeon

The three-command reflex for "wrong program runs":

```console
$ type -a python3            # ALL matches, in PATH order
$ command -v python3         # the winner
$ /usr/bin/python3 --version # bypass PATH entirely — compare behavior
```

`type -a` is the diagnosis: it shows every candidate and the order
the shell will try. When the wrong one wins, the fix is *always* one
of: reorder/remove a PATH entry, remove/rename the impostor, or
invoke the right one explicitly (scripts should do the latter —
Lesson 4).

Also in the kit: `which -a` (similar to `type -a` for files only),
and `hash -r` — bash caches "where I last found `foo`"; after
installing/removing a binary, a stale cache can lie until you clear
it.

## 5. Unset, defaults, and parameter expansion

The shell's expansion toolkit makes env logic one-liners (M19 uses
these constantly):

```console
$ echo "${HOME}"                      # plain
$ echo "${MYFLAG:-default}"           # default if unset OR empty
$ echo "${MYFLAG-default}"            # default only if unset
$ test -z "${MYFLAG:-}" && echo unset # honest emptiness check
```

The `:-` vs `-` distinction is the difference between treating
"empty" as "missing" or not — data pipelines care, and so does every
config script you'll read.

## 6. DS connection

`PATH` is *why* virtual environments work: activation prepends
`~/.venv/bin`, so `python`, `pip`, `jupyter` resolve to the venv's
copies — Lesson 4 shows the actual diff of `env` before/after. And
when M25's cron job can't find `python`, the diagnosis is this
lesson's: cron's PATH is `/usr/bin:/bin` — first match wins, and
your venv never entered the race.

---

**Key takeaways**

- `export` = copy-to-children; one-shot `VAR=x cmd` = cleanest
  override; unset ≠ empty.
- PATH is a priority list; first match wins; `.` excluded on
  purpose.
- Diagnosis reflex: `type -a` → `command -v` → absolute-path
  comparison.

**Check yourself:** `type -a pip` shows `~/.venv/bin/pip` before
`/usr/bin/pip`. Which one runs — and what does that tell you about
the shell you're in?

**Next:** [Lesson 3 — dotfiles](03-dotfiles.md)
