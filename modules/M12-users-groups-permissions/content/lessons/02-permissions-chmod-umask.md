# Lesson 2 — Permissions: chmod, Numeric & Symbolic, umask

> Module 12 · Unit 4 · Difficulty: Intermediate
> Reading time: ~35 min · Lab: [Lab 2 — Permission surgery](../labs/lab-02-permission-surgery.md)
> Up next: [M13 Lesson 1 — Ownership & the shared-directory pattern](../../../M13-ownership-shared-access/content/lessons/01-ownership-chown-shared-dirs.md)

---

## 1. The model: three audiences, three verbs

Every file and directory carries an owner, a group, and a mode — the mode answers
"who may do what" for **three audiences**:

| Audience | Meaning |
|---|---|
| **u** (user) | the file's owner |
| **g** (group) | members of the file's group |
| **o** (other) | everyone else |

...with three verbs, which mean different things on files vs directories:

| Verb | On a **file** | On a **directory** |
|---|---|---|
| **r** read | open/read contents | list the names (`ls`) |
| **w** write | modify contents | create/delete entries *inside* |
| **x** execute | run as a program | **enter/traverse** (`cd`, reach children) |

The directory row is the lesson's most valuable line. `w` on a directory lets
you *rename and delete entries in it* — **even files you don't own** — because
those are directory-table edits. And `x` without `r` is a real (weird) thing:
you can pass through and touch files whose names you already know, but not list.

```console
$ ls -l /etc/hostname
-rw-r--r-- 1 root root 14 Aug 30 10:22 /etc/hostname
```

`-` = file; `rw-` owner; `r--` group; `r--` others: root may edit it, you may
only read. The leading character is the type (`-` file, `d` directory, `l`
symlink — M07).

## 2. chmod symbolic: statements about letters

```console
$ chmod u+x script.sh          # add execute for owner
$ chmod go-w notes.txt         # remove write for group and others
$ chmod o=r data.csv           # set others to exactly read
$ chmod a+r README.md          # all: add read
```

Who: `u g o a` · Action: `+ - =` · What: `r w x`. Comma-combine freely:

```console
$ chmod u=rwx,g=rx,o= ~/projects/eds-01/data/raw    # owner full, group enter, others nothing
```

`=` is *set exactly* (unset everything else) — the difference between tuning and
stamping. Symbolic mode is the *human* language: use it when you mean a
statement about one audience.

## 3. chmod numeric: three bits, one octal digit

Each audience's `rwx` is a 3-bit number, read as octal:

| Octal | Bits | Meaning |
|---|---|---|
| 7 | 111 | rwx |
| 6 | 110 | rw- |
| 5 | 101 | r-x |
| 4 | 100 | r-- |
| 0 | 000 | none |

**chmod NNN** sets all three audiences at once — owner, group, other:

```console
$ chmod 600 secrets.env          # rw- --- ---  : only I may read/write
$ chmod 644 report.csv           # rw- r-- r--  : I edit, world reads
$ chmod 700 ~/projects/eds-01    # rwx ------  : my directory, my business
$ chmod 755 deploy.sh            # rwx r-x r-x : I write, world runs
```

Reading 755 aloud: "7 = owner full; 5 = group read+enter; 5 = others same."
Fluency in both directions (symbolic ↔ numeric) is the skill; you'll *think* in
numeric for common shapes (600, 644, 700, 755) and *speak* symbolic for surgical
changes. Recursion for trees: `chmod -R g-rx ~/archive` — with the usual
care: `-R` plus a wrong path is a self-inflicted audit (M07 Lesson 1's rules,
plus snapshots).

## 4. Which audience won? The check order

The kernel checks **exactly one** audience — first match wins, no summing:

1. If you **are** the owner → owner bits apply. Group bits *never consulted*.
2. Else if you're **in the file's group** → group bits.
3. Else → other bits.

The classic stall: you're in the file's group, but the group bits are `---`,
while *other* is `r--`. You still get **nothing** — being in the group doesn't
fall through to other. This bites every student exactly once; remember it in
M13's shared-directory debugging.

## 5. umask: the permissions *new* files get

`chmod` edits existing files; `umask` shapes *newborn* ones. It's a subtraction
mask from 666 (files) / 777 (dirs):

```console
$ umask
0002
$ touch newfile.txt && mkdir newdir && ls -l newfile.txt && ls -ld newdir
-rw-rw-r-- ... newfile.txt          # 666 - 002
drwxrwxr-x ... newdir               # 777 - 002
```

Ubuntu's default `0002` (with the executable bit never granted by files
anyway) gives: files 664, dirs 775 — group-collaborative. A `umask 0077`
workstation gives 600/700 — private by default. Security-sensitive services
(M27's `.env` files) often *want* `umask 077` at creation time. `umask` is a
shell/session property (M15 makes it persistent); scripts can set it
temporarily: `(umask 077; touch secret.env)` — parentheses spawn a subshell so
the session's mask survives.

## 6. Diagnosing permissions: the workflow (Lab 2 rehearses it)

When access fails, don't guess — walk the ladder:

1. **Exact error?** `Permission denied` = mode/ownership; `No such file` =
   spelling/path (M06). Different diseases.
2. **`ls -ld` the *directory* AND `ls -l` the file** — missing `x` on a parent
   directory masquerades as a file problem.
3. **`id`** — who are you, in which groups?
4. **Match audience:** are you owner? in the group? Apply the check-order rule.
5. **Fix minimally:** the *narrowest* change that grants the need (a group
   bit, not `o+rw`; M13's least-privilege argument in full).

## 7. DS framing: the three modes of data life

| Shape | Numeric | Where you'll use it |
|---|---|---|
| `600` private files | secrets: `.env`, API keys (M27/M25) | "only me, ever" |
| `644`/`664` datasets | readable data, group-writable results | shared lab storage (M13) |
| `700`/`750` project dirs | my sandbox / team sandbox | `~/projects`, group project roots |
| `755` scripts/binaries | runnable by all, writable by owner | course scripts, `~/bin` |

The professional habit: **choose the mode from the access contract**, not from
`chmod 777 and pray` — 777 is never the answer; it's the confession that the
group design (M13) wasn't done.

## Exercises (lab-log.md)

1. Symbolic ↔ numeric: write both forms for (a) owner rw, group r, other none;
   (b) owner full, group none, other read. Verify each with `ls -l`.
2. Directory-x drill: `mkdir ~/scratch/nolist && touch ~/scratch/nolist/x.txt
   && chmod 111 ~/scratch/nolist` — can you `cd` in? `ls` it? `cat
   ~/scratch/nolist/x.txt`? Explain each result with the table in §1.
3. The stall: create `f`, `chgrp` it to a group you're in (M13 formalizes
   `chgrp`; in the VM you may `sudo chgrp`), set `chmod 604 f` — can you still
   read it? Why not, per §4?
4. umask experiments: `umask 077; touch t1; mkdir d1` → modes? Then restore.
   Compute the expected values *before* looking.
5. `chmod 777` autopsy: in your VM, `chmod 777` a scratch file, then answer:
   who can now read, modify, *delete* it (remember directory-w), and why is
   this mode a confession rather than a solution?
6. A teammate's script needs to run (`x`) but not be readable (`r`) — possible?
   Try `chmod 711 script.sh` with a real script. When would this trick matter?
7. Diagnose (paper): "`cat data/raw/x.csv` → Permission denied; `ls -l
   data/raw/x.csv` works; user owns the file with 644." Where does the fault
   actually live? (Hint: §6 step 2.)

## Check yourself before M13

- rwx on files vs directories: I can state all six meanings cold.
- Symbolic and numeric chmod: fluent both directions; common shapes memorized.
- The check-order rule — including the group-stall — I can recite and apply.
- umask: I can compute resulting modes for any mask.

## Further reading (official sources)

- Ubuntu Server docs: file permissions —
  <https://documentation.ubuntu.com/server/how-to/security/users/>
- `man chmod`, `man 2 umask`, `man 5 chmod` won't exist — `man chmod` covers all
- Next module: ownership *moves*, special bits, and ACLs complete the model

Next: [M13 Lesson 1 — Ownership & shared directories](../../../M13-ownership-shared-access/content/lessons/01-ownership-chown-shared-dirs.md)
