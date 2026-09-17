# Lesson 4 — Secrets, venvs, and the Environment in the DS Workflow

> Module 15 · Unit 3 · Difficulty: Intermediate
> Reading time: ~25 min · Lab: [Lab 2](../labs/lab-02-path-clinic.md) (Part C)
> Up next: [practice/quiz.md](../practice/quiz.md)

---

## 1. Environment variables: configuration, or secrets?

Two honest answers:

- **As configuration:** the environment is the *correct* twelve-factor
  place for deployment settings — the same image (M28), different
  `DATABASE_URL` per environment, no rebuild.
- **As secrets:** the environment is *storage, not protection*. Any
  process running as your user can read your environment
  (`/proc/<pid>/environ` of your processes, same UID); child
  processes inherit everything; crash reporters and debug logs print
  it. Treat env vars as **a delivery mechanism**, never as a vault.

The course's rules for secrets in the environment (M25 cron, M28
Compose, M29 CI all restate them):

1. **Never in code** (M26: secrets never in Git — not even "temporarily").
2. **Never in dotfiles** — `.bashrc` is read by everything you run;
   `~/.profile` nearly as wide. Use a restricted-permission file,
   sourced *deliberately*:

```bash
# ~/.config/lab-credentials  (chmod 600) — sourced explicitly, not from bashrc
export DATASET_API_TOKEN="…"
```

```console
$ chmod 600 ~/.config/lab-credentials
$ set -a; source ~/.config/lab-credentials; set +a   # -a: export everything sourced
```

3. **Scope-minimized:** one-shot form for one command —
   `DATASET_API_TOKEN=$(cat ~/.config/token) ./sync_data.sh`.
4. **Assume logs see it:** never `env` or `printenv` into a log,
   ticket, or screenshot; M24's log hygiene rule starts here.

## 2. The venv, revealed as environment surgery

M27 teaches venvs operationally; here is what activation *actually
does* — the diff:

```console
$ python3 -m venv ~/venvs/lab && env | sort > /tmp/env-before
$ source ~/venvs/lab/bin/activate && env | sort > /tmp/env-after
$ diff /tmp/env-before /tmp/env-after
```

You'll see, essentially:

```
> VIRTUAL_ENV=/home/ds/venvs/lab
< PATH=/usr/local/bin:/usr/bin:/bin:…
> PATH=/home/ds/venvs/lab/bin:/usr/local/bin:/usr/bin:/bin:…
```

That's the entire trick: **`VIRTUAL_ENV` set + `PATH` prepended.**
The venv's `bin/` now wins every lookup (Lesson 2's first-match
rule), so `python`, `pip`, `jupyter` are the venv's. `deactivate`
restores the saved originals — no magic, just bag-editing.

Two consequences you can now *derive* rather than memorize:

- A **subshell** inherits the activated environment; a **new terminal
  tab** does not — activation is per-shell, like all environment.
- **cron/scripts** must activate explicitly in-script
  (`source ~/venvs/lab/bin/activate`) because nothing else reads
  bashrc (Lesson 3's third row).

## 3. The explicitness hierarchy (use the top that works)

For getting the right interpreter, most to least robust:

1. **Absolute path:** `~/venvs/lab/bin/python script.py` — immune to
   PATH, activation, and mood. Best for crons and services.
2. **Shebang into the venv:** `#!/home/ds/venvs/lab/bin/python` —
   same immunity, convenient for executables.
3. **Explicit activation inside the script** — readable, still
   correct in cron if the path is absolute.
4. **"I activated it earlier in this shell"** — fine for interactive
   exploration, never for automation. (M25's cron checklist bans
   this with prejudice.)

## 4. Debugging the environment: the general method

The three-step pattern that solves *every* env-var bug in this
course — and most in real work:

1. **Which process is asking?** (`echo $$` in the shell vs the PID of
   the failing job — M18's process tree.)
2. **What does *that process* actually see?** For running processes:
   `tr '\0' '\n' < /proc/<PID>/environ` — the ground truth, not
   your shell's opinion.
3. **Where should the value be injected?** Caller one-shot, dotfile
   (which one? Lesson 3's matrix), service unit `Environment=` (M20),
   cron's own lines (M25), Compose `environment:` (M28) — one owner,
   stated in the runbook (M29-ext A).

That `/proc/<PID>/environ` read in step 2 is the single most
under-used diagnostic in beginner Linux — from this module on, "what
does the environment look like *in there*?" is one command away.

## 5. DS connection

The entire "works on my machine" class of DS failures reduces to
this module: the notebook kernel's env (Launched from the desktop?
from SSH? under systemd?) ≠ your terminal's env. M27's
`sys.executable`/`sys.prefix` diagnostics, M25's cron env table, and
M28's `docker run -e` are all applications of Lesson 2–4. When you
review a teammate's pipeline, the question "where does each
variable's value enter the process?" is now yours to ask — and to
answer with `/proc/*/environ` evidence.

---

**Key takeaways**

- Env vars: right place for *config*, wrong place to *store* secrets
  — restricted files + explicit sourcing + one-shot injection.
- venv activation = `VIRTUAL_ENV` + PATH prepend; deactivate
  restores; per-shell, like everything environmental.
- Debug method: identify the process → read its `/proc/PID/environ`
  → choose the correct injection point.

**Check yourself:** a cron job logs `ModuleNotFoundError`. Name the
diagnosis command that reads the *job's* real environment, and the
two injection fixes ranked by the §3 hierarchy.

**Next:** [practice/quiz.md](../practice/quiz.md)
