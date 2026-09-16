# Module 08 — Text Processing Toolkit · Content Index

> **Status:** Content complete — 6 lessons, 3 labs + mini-project,
> command reference, quiz + key, 8 challenges, troubleshooting guide,
> 6 generated datasets.
> Module contract: [../README.md](../README.md) · Difficulty: Intermediate.

**The module's thesis:** shell text tools do real data work — *before*
you reach for Python. They are not a pandas replacement; they are the
fast, observable first pass (`file → grep → cut → sort → uniq → awk →
output`) that tells you whether your 40-GB CSV even deserves the RAM.

## Lessons

| # | File | Topic |
|---|------|-------|
| 1 | [01-viewing-counting.md](lessons/01-viewing-counting.md) | cat/less/head/tail/wc, text streams, stdin/stdout recap |
| 2 | [02-finding-files-and-text.md](lessons/02-finding-files-and-text.md) | find (+ -exec), locate, grep families, regex fundamentals |
| 3 | [03-columns-sort-uniq.md](lessons/03-columns-sort-uniq.md) | cut, paste, sort, uniq, tr — the column toolkit |
| 4 | [04-sed-awk-xargs.md](lessons/04-sed-awk-xargs.md) | sed substitution, awk field processing, xargs, command substitution |
| 5 | [05-ds-pipelines.md](lessons/05-ds-pipelines.md) | the canonical DS pipeline, applied to logs/CSVs/sensors; data-quality patterns |
| 6 | [06-shell-and-pandas.md](lessons/06-shell-and-pandas.md) | when shell, when Python/pandas; handoff patterns; performance reality |

## Labs & Project

| # | File | Task |
|---|------|------|
| 1 | [lab-01-data-quality-recon.md](labs/lab-01-data-quality-recon.md) | Read-only recon of all six datasets |
| 2 | [lab-02-log-forensics.md](labs/lab-02-log-forensics.md) | access.log + server.log incident analysis |
| 3 | [lab-03-column-clinic.md](labs/lab-03-column-clinic.md) | transactions + students + sensor column work |
| ★ | [mini-project-data-quality-toolkit.md](labs/mini-project-data-quality-toolkit.md) | Build `dq.sh` — a data-quality CLI for any CSV/log (graded deliverable) |

## Reference & Practice

- [Command reference](command-reference.md) — every tool on one page, with the *when*
- [Quiz](practice/quiz.md) (22 Q) · [Answer key](practice/quiz-answers.md)
- [Challenges](practice/challenges.md) (C1–C8)
- [Troubleshooting](troubleshooting.md) — 10 symptom→cause→fix patterns
- [Datasets](data/README.md) — schemas, provenance, *declared* dirt, regeneration

## Cross-references

- [M09 pipes](../../M09-pipes-and-redirection/content/lessons/01-stdin-stdout-stderr-redirection.md) —
  the stream mechanics this module assumes.
- [M10 bash scripting](../../M10-bash-scripting/README.md) — turns this
  module's one-liners into reusable tools.
- [M27 Python/Jupyter](../../M27-python-jupyter-data/README.md) — where
  pandas deepens everything here.
