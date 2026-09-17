# Lesson 3 — Dotfiles: Which File, Which Context

> Module 15 · Unit 3 · Difficulty: Intermediate
> Reading time: ~25 min · Lab: [Lab 1](../labs/lab-01-env-safari.md) (Part C)
> Up next: [Lesson 4 — secrets and venvs](04-secrets-and-venvs.md)

---

## 1. The startup matrix (the whole lesson in one table)

Which files bash reads depends on *how the shell started*:

| Shell started as | Reads | Typical trigger |
|---|---|---|
| **login** | `/etc/profile`, then first-found of `~/.bash_profile`, `~/.bash_login`, `~/.profile` | console login, SSH session, `bash -l` |
| **interactive non-login** | `~/.bashrc` (via the login shell's sourcing, below) | new terminal window/tab in a desktop, most terminal emulators |
| **non-interactive** (scripts) | `$BASH_ENV` if set; usually *nothing of yours* | `./script.sh`, cron (M25), CI (M29-ext C) |

Ubuntu's default `~/.profile` ends with a stanza: *if running bash
and `~/.bashrc` exists, source it*. Net effect on stock Ubuntu:

- **SSH/console login:** profile → bashrc (everything loads)
- **new terminal tab:** bashrc only
- **script/cron:** neither

That third row is the answer to the course's most common
"works-in-my-shell" mystery — and the reason M25's cron checklist
starts with "the cron environment is almost empty."

## 2. The decision rule

> **PATH/variables for daily interactive work → `~/.bashrc`.**
> **Things a login must establish (and that `bashrc` alone can't
> guarantee) → `~/.profile`.**
> **Machine-wide, all users → `/etc/profile.d/*.sh` (drop-in, admin
> territory).**

Why not "just edit `.profile` for everything"? Because terminal tabs
(non-login) never re-read it — your change works after SSH but
vanishes in a new tab, which is worse than not working at all.
Why not "just edit `.bashrc`"? Because *scripts* never read it —
that's Lesson 4's explicit-injection rule.

## 3. Reading Ubuntu's stock `~/.bashrc`

Open yours and note the guard at the top:

```bash
case $- in
    *i*) ;;                # interactive: continue
      *) return;;          # non-interactive: stop here
esac
```

**The guard is load-bearing:** everything below runs *only* for
interactive shells. So additions to `~/.bashrc` — aliases, prompt,
`export` of convenience vars — are, by construction, invisible to
scripts and cron. When you *want* a variable in scripts, it must be
exported *by the caller* or set in the script itself (Lesson 4), not
hidden in bashrc.

Also note what's already there: `HISTCONTROL`, `HISTSIZE`,
the colored `ls` alias, and a `~/.bash_aliases` include — Lesson 4 of
M06's aliases live here; M19 builds on this file properly.

## 4. Editing discipline (the M04 snapshot habit, applied to text)

1. **Copy first:** `cp ~/.bashrc ~/.bashrc.bak-$(date +%F)` — one
   command, saves an evening.
2. **Edit, then verify *in the affected contexts*:** a new tab (non-
   login) *and* `bash -lc 'true'` (simulated login). Both must pass.
3. **Syntax-check without executing:** `bash -n ~/.bashrc` catches
   broken syntax before your next login does.
4. **Recovery hatch:** keep a root-owned pristine copy:
   `sudo cp ~/.bashrc /root/bashrc.pristine` — if your dotfiles ever
   lock you out of a sane shell, `sudo nano /root/bashrc.pristine`
   is the way back. (On a VM, there's always the snapshot; on real
   servers, there's only discipline.)

## 5. The `/etc/profile.d/` pattern (admin-grade)

For machine-wide defaults, administrators don't edit `/etc/profile`
directly — they drop a file:

```console
$ sudo tee /etc/profile.d/lab-env.sh >/dev/null <<'EOF'
# Course lab defaults - safe to delete this file
export LAB_HOME="$HOME/labs"
EOF
$ bash -lc 'echo "$LAB_HOME"'     # login shells see it
```

Why this pattern wins on shared machines (M31 preview): drop-ins are
individually removable, reviewable, and survive package upgrades of
`/etc/profile` itself. The same "drop-in directory beats editing the
central file" logic reappears in sudoers (M14), systemd units (M20),
and nginx (M29).

## 6. DS connection

Your dotfiles are the *shell half* of reproducibility. M27's venv
activation in every shell? One bashrc line — or, better, explicit
activation in the script (Lesson 4). M26's Git identity? It lives in
`~/.gitconfig`, not bashrc — a reminder that *each tool owns its
config file*; bashrc is for shell-level truth only. The common bug:
putting tool config in the shell's config, where it silently fails
for every non-interactive context.

---

**Key takeaways**

- Login vs non-login vs non-interactive decides the file; Ubuntu's
  profile-sources-bashrc makes tabs and logins agree.
- Default rule: bashrc for interactive daily truth; profile for
  login-time establishment; `/etc/profile.d/` for machine-wide.
- The bashrc interactivity guard means **scripts never see it** —
  by design; Lesson 4 handles scripts properly.

**Check yourself:** you add `export DATADIR=~/data` to `~/.bashrc`.
Name one context where `$DATADIR` is empty, and the correct place
for each of: (a) your interactive convenience, (b) a cron job that
needs it.

**Next:** [Lesson 4 — secrets and venvs](04-secrets-and-venvs.md)
