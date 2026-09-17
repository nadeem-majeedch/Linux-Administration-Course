# Demo 2 — The Permission Matrix: Decoding & Breaking

> **Session:** S11 · **Duration:** ~12 min · **Risk:** low (VM, scratch
> dir) · **Objective:** make the rwx triplets *decodable at a glance*
> and expose the directory-`x` wall with a planned failure.

## Prerequisites

- Your demo VM (or a student volunteer's, shared on projector)
- Clean scratch directory

## Setup

```console
$ mkdir -p ~/demolab/matrix && cd ~/demolab/matrix
$ echo secret > vault.txt && echo notes > notes.txt
$ chmod 640 vault.txt && chmod 644 notes.txt
$ ls -l
```

Expected: `-rw-r-----` on vault, `-rw-r--r--` on notes.

## Procedure

**Step 1 — decode in chorus.** Project `ls -l`; the class reads each
triplet aloud: owner/group/other. "Decode `640` without looking:
4+2, 4, nothing."

**Step 2 — the switch.**

```console
$ chmod u+x,g+x vault.txt    # whoops — executable data file?
$ ls -l vault.txt
-rwxr-x--- 1 dsstudent dsstudent 7 Sep 17 10:12 vault.txt
```

*Narration:* "Legal, meaningless, and a classic exam trap: `+x` on a
data file is *permission* granted, not transformation. Run it and see."

```console
$ ./vault.txt
./vault.txt: Permission denied      # or exec-format garbage
```

(The exact message varies by shell/kernel — read it aloud either way.)
Revert: `chmod 640 vault.txt`.

**Step 3 — the directory-x wall (planned failure).**

```console
$ mkdir locked && echo x > locked/file.txt
$ chmod 664 locked          # r + w, NO x — the classic mistake
$ ls locked
ls: cannot access 'locked/file.txt': Permission denied
$ cat locked/file.txt
cat: locked/file.txt: Permission denied
$ cd locked
bash: cd: locked: Permission denied
```

*Narration:* "`r` let me *list the names* — but every attempt to reach
the contents needs `x`. Read without traverse: a phone book with the
pages glued shut."

**Step 4 — repair with understanding.**

```console
$ chmod 755 locked && cat locked/file.txt
x
```

**Step 5 — umask live.**

```console
$ umask 027
$ touch newfile && mkdir newdir && ls -ld newfile newdir
-rw-r----- ... newfile        # 666 & ~027 = 640
drwxr-x--- ... newdir         # 777 & ~027 = 750
$ umask 022                   # restore the session default
```

*(The subshell caveat from the M12 quiz — `(umask 077; touch x)` — is
worth 30 seconds: a subshell's umask dies with it.)*

## Questions to ask

1. Before step 3's failure: "predict exactly which operations fail."
2. "Why do files start at 666 and directories at 777 in the umask
   base?" (execute is a security decision, never default)
3. "You need teammates to *see* filenames but not open them — which
   mode?"

## Common errors & recovery

- `chmod 640` typo'd as `0640` — fine; octal either way
- Demo run as wrong user → Permission denied *on the chmod*: diagnose
  ownership first (a real-world lesson in itself)
- The `./vault.txt` behavior differs across kernels (ENOEXEC message vs
  shell fallback) — both readings are correct; evidence over scripts

## Cleanup (census)

```console
$ ls ~/demolab/matrix
$ rm -r ~/demolab/matrix && ls ~/demolab 2>&1
```

## Optional extension

`stat vault.txt` — show the same permissions in a different notation
(octal `640` visible); connect the two notations via the tool.
