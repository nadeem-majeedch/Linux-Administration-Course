# Lab 2 — The PATH Clinic

> Module 15 · Unit 3 · Difficulty: Intermediate · Est. time: 45 min
> Environment: your own VM. All breakage is staged inside
> `~/lab15/` with named repairs. **Never type Lesson 2's PATH
> amputation into a root shell or a login shell you can't reopen** —
> here it lives in throwaway subshells.

## Part A — The impostor (10 min)

Stage a shadowing binary:

```console
$ mkdir -p ~/lab15/shadow && cd ~/lab15/shadow
$ printf '#!/bin/bash\necho "IMPOSTOR python (harmless demo)"\n' > python3
$ chmod +x python3
$ PATH="$PWD:$PATH" type -a python3
$ PATH="$PWD:$PATH" command -v python3
$ PATH="$PWD:$PATH" python3        # impostor wins — first match
$ python3 --version                # your normal shell: real one
```

Record: `type -a` output in both orders, and the winner's identity.
Then answer: what *minimal* evidence distinguishes "impostor on PATH"
from "broken real python"? (You just performed it.)

## Part B — Amputation and the field amputation kit (10 min)

The accident, in a throwaway subshell (safe by construction):

```console
$ bash    # subshell — break this one only
$ export PATH=/opt/nowhere/bin      # forgot $PATH: amputation
$ ls                                # command not found
$ /bin/ls /                         # absolute paths still work
$ echo "$PATH"                      # document the damage
$ exit
```

Now write, in your own words tested in *another* throwaway subshell,
the two-step recovery: (1) full-path shell or exit, (2) the *correct*
export syntax re-adding with `$PATH`. Verify both. Record the wrong
line, its symptom, and the corrected line side by side.

## Part C — The venv reveal (15 min)

```console
$ python3 -m venv ~/lab15/venv
$ env | sort > /tmp/before.env
$ source ~/lab15/venv/bin/activate
$ env | sort > /tmp/after.env
$ diff /tmp/before.env /tmp/after.env
$ type -a python | head -3          # who wins now?
$ command -v pip && pip --version   # venv pip?
$ deactivate
$ type -a python | head -3          # restored?
```

Record the exact diff lines and the `type -a` before/after. Then the
explicitness test from Lesson 4:

```console
$ ~/lab15/venv/bin/python --version    # absolute: no activation needed
```

Answer: for a cron job, which form do you ship and why (one
sentence)?

## Part D — The honest emptiness check (10 min)

```console
$ unset MYFLAG
$ echo "${MYFLAG:-}" | wc -c        # 1: just the newline — unset AND empty look alike
$ test -z "${MYFLAG:-}" && echo "unset or empty"   # the honest check
$ MYFLAG= ; test -z "${MYFLAG:-}" && echo "still unset-or-empty"
$ bash -c 'set -u; echo "$MYFLAG"' 2>&1 | tail -1  # what does bash say?
```

Record all four. One sentence: why does M19's `set -u` turn this
ambiguity into an error, and why is that a *feature* for scripts?

## Deliverable

`path-clinic.md`: Part A's type -a evidence, Part B's wrong/right
pair, Part C's diff + verdict, Part D's outputs — closing with the
three-command diagnosis reflex from Lesson 2 stated in your own
words.

## Troubleshooting

- `python3 -m venv` fails with ensurepip — `sudo apt install
  python3-venv` (M16/M27 territory; note it).
- `type -a` shows the impostor *after* `deactivate` — a stale hash:
  `hash -r` (Lesson 2 §4), then re-check.
- Part B panic reflex — `exit` (or `/bin/bash`) always restores;
  that's why the clinic runs in subshells.
