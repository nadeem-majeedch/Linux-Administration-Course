# Module 15 Quiz — Environment Variables & Dotfiles

> 20 questions. Answer first, then check
> [quiz-answers.md](quiz-answers.md). Scope: lessons 1–4.
> Scenario-heavy: every question is a diagnosis you'll actually run.

## Section A — The model (Q1–5)

**Q1.** State the two defining properties of the environment. Which
bash experiment from Lesson 1 proves each?

**Q2.** `printenv MYVAR` exits 1; `echo "$MYVAR"` prints an empty
line. Explain what each command actually did, and why the second is
the dangerous one in scripts.

**Q3.** Why can no process edit its parent's environment? Answer in
terms of *copy* semantics, and name the mechanism scripts use to
work around the limitation for one command.

**Q4.** `env | wc -l` differs between your login shell and a
`bash --norc` child. Give two plausible causes, and the command that
would distinguish them.

**Q5.** Why is the environment called "per-process truth"? Give the
DS workflow example where two processes legitimately disagree about
the same variable name.

## Section B — export & PATH (Q6–11)

**Q6.** Distinguish, with one command each: `export X`, `X=`,
`unset X`. Which two states do some programs conflate, and what is
the honest test?

**Q7.** `export PATH=/opt/newthing/bin` was just typed. Name the
exact breakage, the two recovery commands that still work, and the
syntax error in the original line.

**Q8.** Explain why prepending to PATH "wins ties" — reference the
lookup algorithm precisely.

**Q9.** Why is `.` excluded from PATH by default? Describe the attack
the exclusion prevents, and the muscle memory that replaces it.

**Q10.** You installed a new binary; `command -v tool` still finds
the old one — in the *same* shell. Name the cache responsible and
the one-command fix.

**Q11.** `PATH="$PWD:$PATH" ./build.sh` ran clean; plain
`./build.sh` fails on `tool: command not found`. What did the
prefix form change, what didn't it change, and why is the one-shot
form better than exporting in the parent shell here?

## Section C — Dotfiles & contexts (Q12–16)

**Q12.** Tabulate: interactive login shell, interactive non-login,
cron job — which bash startup files does each read (Ubuntu
defaults)?

**Q13.** Why does Ubuntu's stock `~/.profile` source `~/.bashrc`,
and what breaks if you delete that stanza?

**Q14.** The guard at the top of `~/.bashrc` returns for
non-interactive shells. What is it *protecting*, and what does it
make impossible? Name the correct mechanism for each thing it makes
impossible.

**Q15.** You need a machine-wide `EDITOR` for all users on a shared
server. Which file do you create (not edit), why that pattern, and
how do you verify it without logging in as another user?

**Q16.** A teammate's script works over SSH but not in a desktop
terminal tab. Using the startup matrix, give the two most likely
causes and the commands that confirm each.

## Section D — Secrets & venvs (Q17–20)

**Q17.** Rank these secret-storage locations worst to best, with one
reason each: `.bashrc`, script body, `chmod 600` file sourced
deliberately, one-shot command prefix, `/proc/PID/environ`.

**Q18.** Why is `/proc/PID/environ` both the *diagnostic* and the
*threat model* of this module? (Two sentences: how you use it, who
else can use it.)

**Q19.** State exactly what `source venv/bin/activate` changes
(variables and order), why `pip` then resolves to the venv's, and
what `deactivate` must restore.

**Q20.** A cron job needs `~/venvs/lab/bin/python`. Apply Lesson 4's
explicitness hierarchy: give the two most robust forms and one
sentence on why "activate it in bashrc" fails here.
