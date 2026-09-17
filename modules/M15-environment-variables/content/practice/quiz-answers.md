# Module 15 Quiz — Answer Key

## Section A

**Q1.** Copy-on-inherit (child gets a snapshot; Lesson 1 §3's
`FRUIT=mango bash -c …` proves both halves: child sees mango, parent
never sees the child's change). Per-process truth (two shells report
different values for the same name; the lab's login-vs-tab
comparison shows it).

**Q2.** `printenv` *looked up the name* in the process's environment
and found nothing — honest failure, non-zero exit. `echo "$MYVAR"`
*expanded an unset variable to empty string* before echo ran — the
shell can't tell you whether the variable was ever there. Dangerous:
a script takes the empty string as a real value and proceeds.

**Q3.** Children receive a *copy*; there's no channel upward —
memory ownership, not permissions. Workaround for one command: the
one-shot prefix `VAR=val command` (parent composes the child's bag
at creation).

**Q4.** (a) login-shell files (`/etc/profile`, `profile.d`) added
entries; (b) a prompt/venv-manager tool (conda, starship) mutated
the env. Distinguish: `bash --norc --noprofile -c env | wc -l` vs
plain `bash -c 'env | wc -l'` — if they differ, something in the
*default* rc chain is the mutator.

**Q5.** "Per-process truth" = each process's bag is the only one that
matters to it. DS example: Jupyter kernel process has `PATH` without
the venv while your terminal has it — both are correct *for their
process*; the notebook is not "broken", it was launched from a
different bag.

## Section B

**Q6.** `export X` — mark existing (or set) as exported;
`X=` — set to empty (still exists); `unset X` — remove the name.
`X=` vs unset are conflated by sloppy programs; honest test:
`test -z "${X:-}"` (empty-or-unset) vs `[ -v X ]` (exists) — or
`set -u`-style expansion errors.

**Q7.** Breakage: PATH no longer contains system dirs — even `ls`
is unfindable. Still works: absolute `/bin/ls`, `/usr/bin/sudo`
(and `exec /bin/bash`). Error: missing `:$PATH` — the new entry must
be *added to* the list, not replace it:
`export PATH="/opt/newthing/bin:$PATH"`.

**Q8.** The shell scans entries **left to right** and executes the
first matching executable found; a prepended directory is therefore
consulted before every existing one — ties go to the front.

**Q9.** Attack: a hostile directory containing a fake `ls` (or
`python`) that runs instead of the system binary whenever you're
cd'd there. Muscle memory: `./script.sh` — explicit current-dir
invocation, deliberate every time.

**Q10.** bash's command-location hash. Fix: `hash -r` (or
`hash -d tool`). Lesson 2 §4.

**Q11.** The prefix form *added* `$PWD` to that command's inherited
PATH only; the parent's PATH untouched. Why better here: no shell
state to leak, self-documenting, reproducible in CI logs — the
parent stays clean and the requirement is visible at the call site.

## Section C

**Q12.** Login: `/etc/profile` → first of
`~/.bash_profile`/`~/.bash_login`/`~/.profile` (which sources
bashrc). Non-login interactive: `~/.bashrc` only. Cron: neither
(non-interactive, non-login) — plus a minimal default env.

**Q13.** It harmonizes the two interactive contexts (logins *and*
tabs load the same bashrc). Deleted: terminal tabs lose everything
bashrc-only (aliases, prompt, PATH tweaks) while SSH sessions keep
them — context-dependent behavior, the classic confusion.

**Q14.** Protecting: non-interactive shells (scripts, cron) from
interactive-only code — prompts, output, anything printing to
stdout. Makes impossible: passing *variables* to scripts via bashrc.
Correct mechanisms: caller one-shot/export, script-internal
defaults, service/cron `Environment=`, or profile.d for login-wide.

**Q15.** Create `/etc/profile.d/99-editor.sh` containing
`export EDITOR=vim` (or nano). Why: drop-ins are per-file removable,
survive `/etc/profile` upgrades, and are reviewable individually.
Verify without login-as-other-user: `bash -lc 'echo $EDITOR'`
(simulates the login chain) + `sudo -u other bash -lc 'echo $EDITOR'`
if you truly need their context.

**Q16.** Likely: (a) SSH is a *login* shell reading profile files
that the desktop tab (non-login) doesn't — a variable set only in
`.profile`/`profile.d` explains it; (b) the SSH shell is bash while
the tab runs something else (`echo $0` in both). Confirm:
`shopt -q login_shell` + `echo $0` in both contexts, and grep the
variable's definition site.

## Section D

**Q17.** Worst→best: script body (versioned secret — worst possible:
copies forever), `.bashrc` (read by everything interactive, easy to
leak in shares/screenshots), `/proc/PID/environ` (not storage at
all — it's *visibility*; listed here because students try it), one-
shot prefix (memory only, scoped to one command), `chmod 600` file
sourced deliberately (persistent, permission-scoped, out of
version-control paths — best of these; a real secret manager beats
all).

**Q18.** Diagnostic: it's the ground truth of any running process's
environment — `tr '\0' '\n' </proc/PID/environ` shows what the
failing job *really* got. Threat model: any process of the same user
(and root) can read it — so secrets placed in the environment are
readable by everything you run; scope-minimize and rotate.

**Q19.** Sets `VIRTUAL_ENV=<venv>`, prepends `<venv>/bin` to `PATH`
(saves originals); `pip`/`python`/`jupyter` resolve via first-match
to the venv's copies. `deactivate` restores saved `PATH` (and
`PS1`), unsets `VIRTUAL_ENV`.

**Q20.** (1) Absolute interpreter in the crontab line:
`~/venvs/lab/bin/python /path/job.py` — immune to PATH/activation
entirely; (2) in-script `source /home/ds/venvs/lab/bin/activate`
*before* python — still explicit. "Activate in bashrc" fails because
cron's shell is non-interactive and never reads bashrc (Q12) —
Lesson 3's third row, restated as a bug report.
