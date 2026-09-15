# Lesson 1 — Navigating the Filesystem: pwd, ls, cd

> Module 06 · Unit 2 · Difficulty: Beginner
> Reading time: ~30 min · Lab: [Lab 1 — Navigation drills](../labs/lab-01-navigation-drills.md)
> Up next: [Lesson 2 — Paths: absolute, relative, ~](02-paths-absolute-relative-home.md)

---

## 1. The filesystem is one tree

Windows gives you drive letters — `C:\`, `D:\`. Linux gives you **one tree**, rooted
at `/` (pronounced "root"), with every disk, partition, and USB drive *attached into*
that tree somewhere (that's "mounting" — Module 17's topic; for now: one tree, one
root).

```
/                        ← root of everything
├── home/
│   └── dsstudent/       ← YOUR files live here
├── etc/                 ← system configuration
├── var/                 ← variable data: logs, caches
└── usr/                 ← installed software
```

Two consequences worth internalizing now:

1. **There are no drive letters.** A second disk doesn't appear as `D:`; it appears
   as a directory inside the tree.
2. **Everything starts at `/`.** Every path you will ever type is either a route
   *from* `/` (absolute) or a route *from where you stand* (relative) — Lesson 2.

## 2. Where am I? — `pwd`

**Print Working Directory.** The shell is always *somewhere* in the tree; `pwd`
prints that place.

```console
$ pwd
/home/dsstudent
```

**When to use it:** constantly. Most "my script can't find the file" mysteries
(Module 10) and most "oops, wrong place" disasters (Module 7) begin with the shell
being somewhere other than where the user assumed. Professionals `pwd` reflexively
after opening a terminal, after `cd`, before any operation with consequences.

Your prompt already shows the path (`dsstudent@lab:~$`) — but prompts are
configurable and can lie by abbreviation; `pwd` is the ground truth.

## 3. What's here? — `ls`

**List** directory contents.

```console
$ ls
Desktop   Documents   Downloads   Music   Pictures   snap   Videos
```

Bare `ls` shows *non-hidden* names, sorted alphabetically, columns fitted to width.
It has the most useful option set of any command you'll learn this week:

### The working pair: `-l` and `-h`

```console
$ ls -l /etc/hostname
-rw-r--r-- 1 root root 14 Aug 30 10:22 /etc/hostname
```

Read the long line left to right:

| Field | Here | Meaning |
|---|---|---|
| `-rw-r--r--` | type + permissions | `-` = file (`d` = directory); `rw-` owner, `r--` group, `r--` others (Module 12 decodes fully) |
| `1` | link count | how many names point at this data (Lesson: links, M07) |
| `root` | owner | which user owns it |
| `root` | group | which group |
| `14` | size in bytes | — but in what unit? |
| `Aug 30 10:22` | last modified | — |
| name | — | — |

That raw byte size is why `-h` exists:

```console
$ ls -lh ~/Downloads
total 2.4G
-rw-r--r-- 1 dsstudent dsstudent 2.3G Aug 30 14:01 ubuntu-24.04.1-desktop-amd64.iso
-rw-r--r-- 1 dsstudent dsstudent 117M Sep  2 09:44 sensor-dump-2026-09.csv
```

`-h` = *human-readable*: `117M` instead of `122683392`. You will type `ls -lh`
hundreds of times this course; it is the default view for "what's taking space?"

### The pair you'll use on data: `-t` and `-r`

```console
$ ls -lht ~/Downloads      # newest first
$ ls -lhr ~/Downloads      # oldest first
```

`-t` sorts by **modification time**, `-r` **reverses** any sort. "Which dataset did
I touch most recently?" is a daily question once experiments produce files (and
Module 18's long jobs make it diagnostic).

### The one that reveals the invisible: `-a`

```console
$ ls -a ~
.  ..  .bashrc  .profile  .ssh  Desktop  Documents ...
```

Names starting with `.` are **hidden files** — a convention, not encryption: the
`ls` tool simply skips them unless you ask. They hold configuration
(`.bashrc` — Module 15) and credentials (`.ssh` — Module 22). Two entries deserve
attention right now:

- `.` — **this directory itself**
- `..` — **the parent directory**

They are real entries in every directory, and they are the engine of relative paths
(Lesson 2). Related: `ls -A` shows hidden files *without* `.` and `..` — often the
cleaner view.

### The most valuable flag you'll underuse: `-d`

```console
$ ls -ld /tmp
drwxrwxrwt 13 root root 4096 Sep 15 20:11 /tmp
```

Without `-d`, `ls /tmp` lists the *contents* of /tmp. With `-d`, `ls` describes
*the directory itself*. When you want to know "what are the permissions on this
directory?" (Module 12) — `ls -ld`, every time. Beginners burn hours on that
distinction.

**Recap — the five-flag toolkit:** `ls -lha` (everything, long, human sizes) for
orientation; `ls -lht` for recency; `ls -ld DIR` for directories themselves.

## 4. Moving: `cd`

**Change Directory.** The shell's legs.

```console
$ cd /etc          # absolute: from the root, spelled in full
$ pwd
/etc
$ cd ~             # home (see Lesson 2 for ~)
$ cd               # bare cd = home: the shortcut you'll overuse lovingly
$ cd -             # back to the PREVIOUS directory — a toggle between two places
$ pwd
/etc
```

`cd -` is the underrated one: alternate between a dataset and your analysis folder
all day with two keystrokes. It prints where it took you.

**Tab completion changes `cd` from chore to reflex:**

```console
$ cd /usr/sha<Tab>     → cd /usr/share/
$ cd ~/Doc<Tab>        → cd ~/Documents/
```

Type the first letters, press **Tab**; the shell completes. Double-Tab lists
possibilities when several match. Use it for every path from today — it is faster
*and* it prevents typos from creating wrong paths.

## 5. Errors you will see (and what they're telling you)

```console
$ cd /etc/Hostname
bash: cd: /etc/Hostname: No such file or directory
```

Linux paths are **case-sensitive**: `Hostname` ≠ `hostname`. On Windows-trained
fingers this causes daily stumbles; treat exact case as part of the name.

```console
$ cd /root
bash: cd: /root: Permission denied
```

`/root` is the *root user's* home — your user may look at the door but not enter
(permissions: Module 12). The system refused **and told you why**; this message is
normal, not a malfunction.

## 6. Data Science framing: your working set

Datasets, code, results — professionals don't scatter them; they build a convention
on day one. This course's convention (created in Lab 1, argued in Lesson 3):

```
~/
├── data/          # raw + intermediate datasets (replaceable, regenerable)
├── projects/      # code: one folder per project, git-ready (Module 26)
└── archive/       # finished experiments, moved out of the way
```

Navigation fluency exists to serve a layout like this: `cd ~/projects` → work →
`cd -` to compare against `~/data` → `ls -lht` to see what you touched last.
Module 7 turns this skeleton into a working dataset project.

## Exercises (lab-log.md)

1. Run `pwd` in a fresh terminal. Then `cd /usr/share/doc`, `pwd`, `cd`,
   `pwd`. Record all three readings and what `cd` did each time.
2. Use only Tab completion to reach `/usr/share/doc/grep` (no full typing).
   Note how many keystrokes it took versus typing it fully.
3. In your home: `ls -a` — list three hidden entries. Which one will Module 15
   teach you to edit safely (hint: the shell's config)?
4. `ls -lht ~/Downloads` (or any folder you've touched): what is the most
   recently modified file? When was it modified?
5. `ls -ld /tmp /var/tmp` — compare the two lines. What differs in the first
   field and the dates? (One sentence; Modules 12/17 will deepen this.)
6. Predict first: after `cd /etc`, what does bare `cd` do? After `cd /home`,
   what does `cd -` do? Verify both.
7. A classmate's prompt shows `~/projects/eds-m01` but they claim "the terminal
   is broken — my file isn't here." What do you ask them to run first, and why?

## Check yourself before Lesson 2

- I can run `pwd`, `ls -lha`, `ls -lht`, `ls -ld DIR`, `cd PATH`, `cd -` from memory.
- I can read an `ls -l` line: type, permissions, owner, group, size, date, name.
- I know what `.` and `..` mean and that names starting with `.` are hidden.
- I use Tab completion on every path.

## Further reading (official sources)

- `man pwd`, `man ls`, `man cd` (builtin — `help cd`) in your VM
- GNU Coreutils manual — <https://www.gnu.org/software/coreutils/manual/>

Next: [Lesson 2 — Paths: absolute, relative, and ~](02-paths-absolute-relative-home.md)
