# Module 10 Troubleshooting — Script Symptoms → Causes → Fixes

> Ten patterns, ordered by how often they bite. Each: **symptom →
> cause → diagnosis → fix → prevention**. The meta-tool for all of
> them is the Lesson 5 ladder: read verbatim → `bash -n` → `bash -x`
> → `shellcheck`.

## 1. `command not found` — for your variable's name

**Cause:** spaces around `=` (`count = 5`) — bash runs `count` as a
command. **Diagnosis:** the error names the *left side* of your
intended assignment. **Fix:** `count=5`. **Prevention:** none needed
— this one burns once. (But `bash -n` confirms the rest of the file
parses.)

## 2. `No such file or directory` for a file that visibly exists

**Cause:** word splitting on an unquoted variable — the path with
spaces became several arguments. **Diagnosis:** `bash -x` shows the
post-expansion command: `+ cp my report.csv backup/`. **Fix:** quote
every expansion: `cp "$f" backup/`. **Prevention:** shellcheck
SC2086; the course rule "quote every use".

## 3. Script runs fine alone, but `VAR` is empty inside `$(...)` or a pipe

**Cause:** command substitution runs in a subshell — variables set
*inside* it don't escape. **Diagnosis:** `bash -x` shows the
assignment working... within the subshell only. **Fix:** capture
output with `var=$(cmd)` *at the top level*; use functions/exit
codes to return status, not side-effect assignments. **Prevention:**
treat `$( )` as read-only capture; never set-and-rely inside it.

## 4. "It works when I paste the commands, fails as a script"

**Cause:** usually one of: missing shebang (a different shell ran
it), missing `chmod +x` (ran via `sh script.sh` — again a different
shell), relative paths (the working directory differs), or PATH
(works interactively because of shell functions/aliases that scripts
don't inherit — M15's distinction). **Diagnosis:** run `bash -x
script.sh`; compare the failing line's expanded form. **Fix:**
shebang + `chmod +x`; `cd "$(dirname "$0")"` or absolute paths;
full paths for crontab-bound scripts. **Prevention:** the Lesson 5
rung-5 skeleton; test from a different cwd.

## 5. `[: missing ]'` / `unexpected EOF while looking for matching`

**Cause:** unbalanced quotes or brackets — often a quote *inside* a
variable's value colliding with test syntax, or a missing `fi`/`done`
far from the reported line. **Diagnosis:** `bash -n` — note the
error's line is where bash *gave up*, not necessarily where the
mistake is; scan upward. **Fix:** balance; prefer `[[ ]]` for bash
scripts (no bracket-splitting games). **Prevention:** `bash -n`
before running; an editor with bracket matching.

## 6. Loop runs once on the literal `*.csv`

**Cause:** empty glob — no matches, and without `nullglob` bash
keeps the pattern as text. **Diagnosis:** `bash -x` shows `for f in
'*.csv'`. **Fix:** `shopt -s nullglob` at the top, or the in-loop
guard `[[ -e "$f" ]] || exit 66` (which *also* documents "this
script needs input"). **Prevention:** every glob-loop in course
scripts carries the guard — it doubles as the missing-input error.

## 7. The script succeeds — and did the wrong thing

**Cause:** an unchecked early command failed; later steps operated on
stale/missing state. Classic under `set -e`-less scripts.
**Diagnosis:** add strict mode, re-run: the *first* lie is exposed.
Check exit codes of everything that matters (or let `-e` do it).
**Fix:** `set -euo pipefail` + explicit guards for the paths where
failure is *expected and handled*. **Prevention:** strict mode is
the course default; the `cmd || fail "message"` pattern for
deliberate handling.

## 8. `line N: unexpected argument` from a command that "should take" those args

**Cause:** unquoted variables *inside* a command's arguments, or a
glob matching more than expected — the command received a different
argument count than intended. **Diagnosis:** `bash -x`, count the
arguments in the `+` line. **Fix:** quote; if a filename legitimately
starts with `-`, separate options: `cp -- "$src" "$dst"`.
**Prevention:** SC2086; `--` habit for user-supplied names.

## 9. Cron/CI runs it differently than you do

**Cause:** the script relied on *interactive context*: aliases
(don't exist in scripts), a relative path (different cwd), a
non-interactive PATH, or a command that prompted for input (no tty →
hang). **Diagnosis:** run it under `env -i bash script.sh` — a
minimum environment — or read M19's cron notes. **Fix:** absolute
paths; avoid interactive reads when automated; set PATH explicitly
if needed. **Prevention:** the "works from any cwd, any
environment" bar of rung-5 scripts; M11's dry-run mode.

## 10. A script that prompts... and hangs the pipeline

**Cause:** `read -p` in a script that later ran inside a pipeline or
scheduler — nothing supplies stdin, so it waits forever.
**Diagnosis:** the hang *is* the diagnosis; check for `read`,
interactive confirmations. **Fix:** arguments/flags instead of
prompts; a `--yes` flag where confirmation is genuinely required;
`read -t 30` timeouts where unavoidable. **Prevention:** course
rule from Lesson 3 — arguments for anything automated, `read` only
for genuinely interactive tools.

## When to escalate (to a human or a tool)

| Situation | Escalate to |
|---|---|
| Fix works but you can't explain *why* | TA — an unexplained fix is a future bug |
| shellcheck finding you can't resolve | The code's wiki page → TA; don't disable without an argument |
| Script will run against shared/production data | Reviewer first — dry-run (M11) + guards demonstrated |
| Same bug class three times in your own code | Personal checklist item — write the rule down |

> Escalating with the transcript (`bash -x` output + shellcheck
> findings) is the M24 incident-report habit, years early.
