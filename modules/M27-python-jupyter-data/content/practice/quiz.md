# Module 27 Quiz — Python, Jupyter & Data on Linux

> 22 questions. Answer first, then check [quiz-answers.md](quiz-answers.md).
> Scope: lessons 1–4 plus the environment/tunnel/batch labs. The
> "evidence-first" and "fail-loudly" rules count as quiz material.

## Section A — Python environments (Q1–6)

**Q1.** Why does `python3 -m pip install` beat bare `pip install` in
this course? Name the two failure modes the explicit form avoids.

**Q2.** Your teammate ran `pip install pandas` and the import still
fails in their notebook. Name the three most likely causes, in
diagnosis order.

**Q3.** What exactly does `pip freeze > requirements.txt` capture that
`pip install pandas` does not — and what is the *cost* of that
capture?

**Q4.** Where does `python3 -m venv .venv` put the interpreter, and
what two mechanisms make `import pandas` inside the venv resolve
to the venv's copy and not the system's?

**Q5.** A scheduled script calls
`/home/ds/proj/.venv/bin/python script.py` with **no activation**.
Why does that work, and why is it *more* reliable than activating?

**Q6.** Why does this course install packages into a project-local
`.venv` rather than `pip install --user` or the system Python?
Give one reason from the reproducibility side and one from the
system-integrity side.

## Section B — Jupyter on Linux (Q7–12)

**Q7.** Why must a headless Jupyter server bind `127.0.0.1` rather
than `0.0.0.0:8888` in this course's labs?

**Q8.** What is the difference between the browser URL a tunnel gives
you (`http://127.0.0.1:9999`) and the server's actual listener —
and what does the `-L 9999:127.0.0.1:8888` each half mean?

**Q9.** Your notebook imports pandas fine in one kernel and fails in
another. Explain via kernels-as-venvs.

**Q10.** What does `jupyter nbconvert --to script analysis.ipynb` buy
you in a pipeline context, and what does it lose?

**Q11.** Why is `ps aux | grep jupyter` insufficient as shutdown
procedure, and what's the polite alternative?

**Q12.** Where does Jupyter keep notebooks by default relative to the
command you ran — and how does `root_dir` config change that?

## Section C — processes, scheduling, permissions (Q13–18)

**Q13.** Why does `nohup python big_job.py &` survive logout where
bare `python big_job.py &` may not — and what does nohup actually
change?

**Q14.** A 40-minute training run is eating 95% CPU and the PI asks
for it to be "niced". What command, what does nice actually do,
and when would you use `renice` on a running PID?

**Q15.** Your cron job runs at 02:15 but the 02:15 log line never
appears. List four diagnosis steps in order.

**Q16.** Why is `env -i HOME=$HOME LOGNAME=$USER PATH=/usr/bin:/bin /path/to/script.sh`
the correct rehearsal for a cron job, and what three assumptions
does it strip away?

**Q17.** Your dataset directory must be read-only for the whole
research group but writable by you. Which mode string, and which
special bit would you use on the *directory* to enforce
group-ownership of new files?

**Q18.** `chmod -R a-w data/raw/` breaks the "accidental overwrite"
guard. Why does read-only-by-permission beat read-only-by-
convention, and when does it *not* protect you (what can still
write there)?

## Section D — synthesis (Q19–22)

**Q19.** A colleague says "pip installed it, so Jupyter will see it."
Compose the two-sentence correction — venv scoping, kernel
binding.

**Q20.** Give the three-element evidence bundle for "the nightly job
ran last night" and the one thing it can *not* prove.

**Q21.** A training script writes checkpoints every epoch to
`outputs/`. It dies at epoch 7 of 20 mid-write. Why is the
truncate-then-rename pattern in the nightly script the right
defense, and what does it guarantee about the on-disk state?

**Q22.** Why does this course run every Python lab as a *project
directory* — `data/`, `notebooks/`, `outputs/`, `.venv/`,
`scripts/`, `requirements.txt` — instead of one big shared folder?
Name three distinct benefits tied to Linux administration
concepts.

Check answers: [quiz-answers.md](quiz-answers.md) ·
Practice more: [challenges.md](challenges.md) ·
Symptoms index: [../troubleshooting.md](../troubleshooting.md)
