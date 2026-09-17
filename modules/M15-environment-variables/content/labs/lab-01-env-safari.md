# Lab 1 — The Environment Safari

> Module 15 · Unit 3 · Difficulty: Beginner → Intermediate · Est. time: 40 min
> Environment: your own VM. All commands are read-only except Part D's
> guarded drop-in (removal included). Nothing here can break your shell
> beyond the current session.

## Part A — Inheritance, proven (10 min)

```console
$ env | sort > /tmp/parent.env
$ bash -c 'env | sort' > /tmp/child.env
$ diff /tmp/parent.env /tmp/child.env | head
```

1. What differs? (Hint: `_`, maybe `SHLVL`.)
2. The one-way rule, demonstrated: child tries to `export` upward —
   show that the parent never sees it.
3. The one-shot form: `GREETING=hi bash -c 'echo $GREETING'` — then
   confirm `echo "$GREETING"` in the parent is empty.

Record: three lines of evidence for "copy, downward only."

## Part B — The two contexts (10 min)

From your desktop terminal (or `bash` inside WSL) vs an SSH session
to your own VM (`ssh ds@localhost` — M22 light):

```console
$ echo "$0 $-"          # this shell: name + flags (i = interactive, l = login?)
$ shopt -q login_shell && echo LOGIN || echo NOT-LOGIN
$ cat /proc/$$/environ | tr '\0' '\n' | grep -c .
```

Record the login/not-login verdict for each context, and the
environment entry counts. Explain the count difference in Lesson 3's
matrix terms.

## Part C — Dotfile routing, verified (10 min)

Temporarily (you'll revert in Part C cleanup) add a marker to each
file — **back them up first**:

```console
$ cp ~/.bashrc ~/.bashrc.lab-bak && cp ~/.profile ~/.profile.lab-bak
$ echo 'echo ">> bashrc ran"'    >> ~/.bashrc
$ echo 'echo ">> profile ran"'   >> ~/.profile
```

Now open a **new terminal tab** (or `bash`): which marker(s) print?
Run `bash -lc 'true'`: which print(s)? Run `bash -c 'true'`: which?

**Cleanup (do not skip):**

```console
$ cp ~/.bashrc.lab-bak ~/.bashrc && cp ~/.profile.lab-bak ~/.profile
$ bash -n ~/.bashrc && bash -n ~/.profile && echo syntax-ok
```

Record the routing table you *observed* and compare with Lesson 3's.

## Part D — The admin drop-in (optional, 10 min, sudo)

```console
$ sudo tee /etc/profile.d/zz-lab-probe.sh >/dev/null <<'EOF'
export LAB_PROBE=active
EOF
$ bash -lc 'echo "$LAB_PROBE"'; bash -c 'echo "[$LAB_PROBE]"'
$ sudo rm /etc/profile.d/zz-lab-probe.sh    # cleanup
```

Record which contexts saw it. Why does `/etc/profile.d/` reach
non-login *interactive* shells on Ubuntu? (Trace the chain:
`/etc/profile` → `~/.profile` → `~/.bashrc` — which link carries it?)

## Deliverable

`env-safari.md`: Parts A–D evidence, the observed routing table, and
one paragraph: **why "it works in my shell" is not evidence** — what
*would* be?

## Troubleshooting

- Both markers fire in a plain `bash` — check whether Ubuntu's
  `.profile` sourced `.bashrc` (it does); that *is* the lesson.
- `diff` shows more than a line or two — you may have env-modifying
  prompts (e.g. conda); note them: they're real-world noise.
- Part D: `bash -c` saw it too? Only if something exported it *from
  the login parent* — that's inheritance, and exactly the point.
