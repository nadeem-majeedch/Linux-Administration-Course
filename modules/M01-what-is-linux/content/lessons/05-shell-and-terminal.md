# Lesson 5 — The Shell & The Terminal

> Module 01 · Unit 1 · Difficulty: Beginner
> Reading time: ~20 min · Up next: [Lesson 6](06-getting-help.md)

---

## 1. Three words people mix up: console, terminal, shell

These terms are used interchangeably in casual talk, but they name different things.
Getting them straight now prevents confusion all course:

| Term | What it is | Analogy |
|---|---|---|
| **Console** | Historically: the physical keyboard+screen wired to the machine; today: the virtual log-in screens (Ctrl+Alt+F3 on a desktop Ubuntu) | The machine's own built-in keyboard/monitor |
| **Terminal (emulator)** | The *window* on your desktop that displays a text session: GNOME Terminal, Konsole, Windows Terminal, iTerm | The cup |
| **Shell** | The *program* running inside that window: reads your lines, runs commands, prints results. The default on Ubuntu is **bash** (Bourne Again Shell) | The coffee |

So: you type in a **terminal** (window), the **shell** (bash) inside it interprets
what you typed, and asks the kernel to do it. The shell is a user-space program —
replaceable! Others exist (`zsh`, `fish`, `ksh`); bash is the course standard and
the default almost everywhere you will work.

A little history that explains the name: real hardware terminals (like the VT100)
were screens+keyboards connected to a central computer by a cable. Your GNOME
Terminal *emulates* that device in software — hence "terminal emulator".

## 2. CLI vs GUI: when each wins

A **GUI** (graphical user interface) presents files and apps as icons, windows,
menus. A **CLI** (command-line interface) presents them as text commands and text
output.

| | GUI | CLI |
|---|---|---|
| Learning curve | Minutes | Weeks (but compounds) |
| Discoverability | Excellent (visible options) | Requires documentation (→ Lesson 6) |
| Repeatability | Poor: you click 200 times, then explain *how* to a colleague | Perfect: the command line *is* the recipe |
| Speed, one action | Often faster | Often slower |
| Speed, 10,000 actions | Impossible by hand | Trivial: loop over it (M10) |
| Remote over slow link | Heavy | Excellent — text only |
| Automation / scheduling | Not really | Its native habitat (M19) |

The honest answer is *both have jobs*: you will still use a browser and a file
manager. The CLI wins exactly where professional work lives — **repeating,
combining, automating, and doing it on machines you only reach over the network**.

> **Data Science connection:** your daily tools already agree. Jupyter, pandas, and
> ML libraries are driven by *code you type*, not menus. The shell is the same idea
> one layer down: typed commands, composable, automatable. GUI data tools exist —
> and every serious pipeline outgrows them, because pipelines must re-run tomorrow
> without a human clicking.

## 3. Reading the prompt

After login you see something like:

```
dsstudent@ubuntu-ds-lab:~$
```

Read it as four fields:

| Field | Meaning |
|---|---|
| `dsstudent` | Your **username** |
| `@ubuntu-ds-lab` | The machine's **hostname** |
| `:` | Separator |
| `~` | Your **current directory**: `~` is shorthand for your home directory (`/home/dsstudent`) |
| `$` | "The shell is ready, and I am a **normal user**." A root shell would end in `#` instead — if you ever see `#`, you are holding admin power; double-check every line |

When you change directory, the `~` becomes the path, e.g. `~/projects`. The prompt
is a *status display*: glance at it before every command.

> **Course habit #1:** always read the full prompt before pressing Enter. Most
> beginner catastrophes (from M07 on) start with running a command in the wrong
> place or as the wrong user. The prompt told you; the habit is learning to look.

## 4. Your first keystrokes

Open a terminal (Lab 4 shows exactly how) and try these — all harmless:

**Does it echo text back?**

```console
$ echo "hello, Linux"
hello, Linux
```

`echo` prints its arguments to the screen. It looks trivial; it is actually the
shell's "print statement" and you will use it in every script from M10 on.

**What time does the machine think it is?**

```console
$ date
Tue Sep 15 20:42:07 UTC 2026
```

Servers keep time in UTC; logs (M24) are timestamped with this clock.

**Who am I on this machine?**

```console
$ whoami
dsstudent
```

Trivial at home; essential on shared servers, where "wait, which account am I?"
precedes many mistakes (M14).

**The shell remembers:**

- **Tab completion.** Type `ech` then press **Tab** → the shell completes `echo`.
  Type `date --` then **Tab Tab** (double-tap) → it lists the options. Tab is the
  single biggest fluency accelerator; use it from today on *every* command and path.
- **History.** Press **↑**/**↓** to walk through previous commands; the `history`
  command lists them; **Ctrl+R** starts a reverse search — type a fragment like
  `free` and it recalls the last command containing it.

**Three control keys to learn before anything else:**

| Keys | Effect |
|---|---|
| **Ctrl+C** | Interrupt the *running* command (also: how you get your prompt back) |
| **Ctrl+D** | End of input: closes the shell/session (or use `exit`) |
| **Ctrl+L** | Clear the screen (or run `clear`) |

A safe experiment: run `ping -c 4 localhost` (pings your own machine 4 times,
harmless), then stop a long one with Ctrl+C: `ping localhost` runs forever —
**Ctrl+C** — the shell prints `^C` and gives you the prompt back. You have just
used a *signal* (Module 18's topic, met early as a survival skill).

## 5. The shell is a programming language (preview)

Everything you type is interpreted by a real language with variables, loops, and
conditions. You will program it properly in Modules 10–11. For now, one glimpse —
the shell can reuse a result inline:

```console
$ echo "Today is $(date +%A)"
Today is Tuesday
```

`$(…)` runs the inner command first and pastes its output into the outer one.
Don't memorize the syntax yet; notice the *possibility*: commands can build commands.
That composition is the CLI's superpower.

## 6. Command blocks in this course

Typographic conventions used everywhere in this repo:

```console
$ command --options arguments     # $ = normal user prompt (not typed by you)
```

- The `$` (or `#` for root) **is not part of what you type.**
- `#` at line end starts a comment in shell (and in this course's code blocks).
- Lines **without** a `$` inside a `console` block are *output*.
- In `bash`/`python` blocks, the same rules apply per language.

## Exercises (lab-log.md)

1. In your own words: what is the difference between the terminal and the shell?
   Which one is bash?
2. Decode this prompt: `nadia@hpc-login-3:/data/nadia$` — username, hostname,
   current directory. What is `#` at the end telling you instead?
3. Run `echo "hello, Linux"`, `date`, and `whoami`. Paste the outputs into your
   lab log, with one comment line per command saying what it does.
4. Practice Ctrl+R: recall the `free -h` command from Lesson 4 (or run it once
   first). Which keys recalled it?
5. Try Tab completion: type `his` + Tab. What did it complete to? Then `history`
   and count your commands so far.
6. Start `ping localhost`, stop it with Ctrl+C, and write down exactly what the
   shell printed. Which control key "gets the prompt back"?
7. Argue the case *for* the CLI to a GUI-only colleague using the table in §2 —
   but also give one honest case where the GUI wins.

## Check yourself before Lesson 6

- I can explain terminal vs shell vs console and say which is bash.
- I can read every field of my prompt, including `$` vs `#`.
- I use Tab and history reflexively; I know what Ctrl+C, Ctrl+D, Ctrl+L do.
- I can predict: "echo $(whoami)" prints what?

## Further reading (official sources)

- GNU Bash manual — <https://www.gnu.org/software/bash/manual/>
- GNOME Terminal help (in your VM: `man gnome-terminal`)
- Ubuntu desktop usage docs — <https://help.ubuntu.com/stable/ubuntu-help/>

Next: [Lesson 6 — Getting Help](06-getting-help.md)
