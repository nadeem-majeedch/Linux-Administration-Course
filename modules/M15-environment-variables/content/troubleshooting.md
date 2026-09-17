# Module 15 Troubleshooting — Environment & PATH Symptoms

> Eight patterns. Each: symptom → likely cause → diagnosis → fix →
> prevention. The universal first move is **identify the process**,
> then read *its* environment — never your shell's opinion of it.

## 1. `command not found` — but you just installed it

**Causes:** installed outside PATH (`~/.local/bin`, venv, `/opt/...`)
· new terminal didn't re-source · stale hash cache.
**Diagnosis:** `type -a <cmd>`; `echo "$PATH" | tr ':' '\n'`;
`dpkg -L <pkg> | grep bin/` (M16) to find where it went.
**Fix:** add the right dir to PATH in the right dotfile (Lesson 3
matrix), or call by absolute path; `hash -r` if cache is stale.
**Prevention:** after installing any tool, `type -a` it in a *fresh*
shell before scripting around it.

## 2. Wrong version of a tool runs (the impostor)

**Cause:** earlier PATH entry shadows (conda base, `~/.local/bin`,
pipx, older install).
**Diagnosis:** `type -a <tool>` — the full candidate list, in order;
`<tool> --version` vs the absolute path's `--version`.
**Fix:** reorder PATH entries, remove the impostor, or use absolute
paths in scripts (Lesson 4 hierarchy).
**Prevention:** venv/pipx per project; never install into system
site-packages "just in case".

## 3. "Works in my shell, fails in cron/script/CI"

**Cause:** non-interactive shells read no bashrc; cron's env is
minimal (`PATH=/usr/bin:/bin`, no `HOME` assumptions beyond basics).
**Diagnosis:** replicate the context: `env -i /bin/bash --noprofile
--norc -c 'your script'` — closest local reproduction of "empty
bag"; for cron, the env-dump cron from C4.
**Fix:** explicit injection: cron `VAR=value` lines, absolute
interpreter paths, in-script `source` of venv/profile (M25's
checklist operationalizes this).
**Prevention:** treat every automation as env-free until proven
otherwise — the script states its own requirements.

## 4. `sudo` loses your environment

**Symptom:** `sudo ./script.sh` can't find vars/tools that plain
`./script.sh` saw.
**Cause:** `sudo` resets the environment by policy (`env_reset`,
secure_path — M14).
**Diagnosis:** `sudo env | sort > /tmp/sudo.env` and diff against
your own.
**Fix:** pass deliberately: `sudo VAR=val ./script.sh` or
`sudo -E` (know why *before* using it — it's the wide door), or fix
the script to need nothing from the caller.
**Prevention:** scripts that need privilege state their needs;
audit with the diff above.

## 5. Prompt/aliases vanish in one context only

**Cause:** dotfile routing — change landed in `.profile` but the
context is non-login (or vice versa), or `.bashrc`'s interactivity
guard returned early.
**Diagnosis:** `shopt -q login_shell` in the failing context;
`bash -n ~/.bashrc ~/.profile` for syntax; add temporary echo probes
(then remove).
**Fix:** move the change to the file the context actually reads
(Lesson 3's decision rule).
**Prevention:** after dotfile edits, verify in *all* contexts: new
tab, `bash -lc true`, `bash -c true`.

## 6. `ModuleNotFoundError` in Python (environment, not code)

**Cause:** interpreter mismatch — the running Python isn't the one
that got the `pip install` (wrong venv, notebook kernel vs shell,
cron context).
**Diagnosis:** in the *failing* process:
`python -c "import sys; print(sys.executable, sys.prefix)"`; compare
with the venv you intended; `/proc/PID/environ` for jobs.
**Fix:** explicit interpreter (absolute path/shebang) or correct
activation — Lesson 4's hierarchy.
**Prevention:** `sys.executable` printed in every long job's log
header; one venv per project, named for it.

## 7. Secrets leaked into logs/screenshots

**Cause:** `env`/`printenv` output pasted into tickets; scripts
echoing variables; `.bashrc` holding tokens.
**Diagnosis:** grep the *destinations*: logs, shell history
(`history | grep -i token` — and remember M10's history rules),
dotfiles.
**Fix:** rotate the exposed credential *first*, then migrate
storage (restricted file + explicit source, one-shot injection);
scrub the specific leak site.
**Prevention:** secrets never in dotfiles or history-producing
commands; `set +x`/avoid `-x` near secrets; audit before sharing
any config.

## 8. `bash: syntax error` after a dotfile edit — and now every shell fails

**Cause:** broken syntax in `.bashrc` (unclosed quote, stray
control character from a Windows editor — M06's CRLF note).
**Diagnosis:** `bash -n ~/.bashrc` reports the line; if interactive
login is broken, `bash --noprofile --norc` still opens.
**Fix:** repair or restore the `.bak` you made (Lesson 3 discipline);
fix line endings (`sed -i 's/\r$//' ~/.bashrc`).
**Prevention:** `bash -n` before sourcing; backups before edits;
edit dotfiles with LF endings.
