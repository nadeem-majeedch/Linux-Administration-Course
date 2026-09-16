# Lesson 6 — Shell & Python/pandas: Complements, Not Competitors

> Module 08 · Unit 2 · Difficulty: Intermediate
> Reading time: ~25 min · No lab (mini-project instead)
> Prerequisites: [Lesson 5](05-ds-pipelines.md)

---

## 1. The honest comparison

The module's closing question: *why not just pandas?* Both sides deserve
their best case:

| Dimension | Shell tools | Python/pandas |
|---|---|---|
| Startup cost | ~1 ms/process | ~1–3 s interpreter + imports |
| Memory | constant (streams!) | dataset fully in RAM |
| Scale ceiling | any size file, any machine with SSH | `read_csv` needs RAM ≥ file size |
| Speed (simple filters) | near-I/O speed | seconds of overhead on trivial asks |
| Joins, regressions, plotting | ✗ (awk joins hurt) | ✓ the whole point |
| Readability of complex logic | poor beyond ~5 stages | excellent |
| Reproducibility of *state* | files in, files out — composable | notebooks hide state |
| Availability | every server, no install | needs an environment (M27) |

**The synthesis this course teaches:**

> Shell for *first contact and logistics* — inspect, filter, reduce,
> move, monitor. pandas for *analysis* — joins, statistics, modeling.
> The handoff is a **file or a stream**, and it's cheap.

---

## 2. The division of labor, concretely

**Shell owns:**

- **Recon** (Lesson 1's checklist): `head`, `wc`, `file` before any load
- **Reduction**: 40-GB log → 40-MB relevant slice *before* Python exists
- **Logistics**: find datasets, count rows, split files, checksum, move
  artifacts between machines (M23)
- **Monitoring**: `tail -f training.log | grep --color -E "epoch|error"`
  while the notebook runs
- **Glue**: cron runs `pipeline.sh` which calls Python at the right step

**pandas owns:**

- Anything with *relationships*: merges, groupby-with-multiple-agg,
  pivots
- Statistics beyond mean/max: quantiles, rolling windows, regressions
- Cleaning that needs *row context* (fillna strategies, type inference)
- Anything someone else must read later

**The litmus test:** if the answer is "filter and count," shell first.
If it's "compare distributions across joined tables," pandas. If
unsure: shell recon is 30 seconds; start there.

---

## 3. Handoff patterns (the actual integration)

**Pattern 1 — shell narrows, Python analyzes:**

```console
$ grep " ERROR " server.log > errors-only.log        # 107 lines (~18%)
$ python3 -c "
import pandas as pd
df = pd.read_csv('errors-only.log', sep=' ', header=None,
                 names=['ts','lvl','svc','ip','path','rest'])
print(df['svc'].value_counts())
"
auth-service      22
api-gateway       21
worker-queue      20
...
```

One-liner Python via `-c` — a full value_counts without leaving the
terminal, reading *what grep pre-selected*.

**Pattern 2 — Python produces, shell monitors:**

```console
$ python3 train.py > train.log 2>&1 &
$ tail -f train.log | grep --color -E "epoch=[0-9]+"
```

**Pattern 3 — the pipeline *includes* Python as a stage:**

```console
$ awk -F',' 'NR>1 {print $3}' transactions.csv | sort -u | \
    python3 -c "import sys, pandas as pd; print(pd.Series([l.strip() for l in sys.stdin]).describe())"
count       4
unique      4
...
```

`sys.stdin` makes any Python script a pipeline citizen. This is the
deep idea: **both ecosystems speak *streams*** — the shell's model from
Lesson 1 is the same one pandas' `read_*`/`to_*` functions implement.

**Pattern 4 — CSV as the contract:**

```console
$ awk -F',' 'NR>1 {r[$3]+=$5} END {for (k in r) print k","r[k]}' transactions.csv > region-revenue.csv
$ python3 -c "import pandas as pd; print(pd.read_csv('region-revenue.csv', names=['region','revenue']))"
```

Shell emits valid CSV (`print k","r[k]` — quote any field that may
contain a comma), pandas ingests it. Simple, inspectable, debuggable —
vs a pickled binary blob nobody can audit with `head`.

---

## 4. Performance reality (numbers, not folklore)

From [Lesson 5's workflows](), the awk group-by-sum over 1,061 rows took
imperceptible time — and would over 10 M rows too (streaming). `pd.read_csv`
on 10 M rows: several seconds + ~1 GB RAM. Neither is *wrong*; they cost
different currencies:

- Shell: cheap per-run, zero memory, but logic scales badly with
  complexity (the 8-stage pipeline nobody can read)
- pandas: expensive startup/memory, but complex logic stays linear in
  code length

**Course heuristic:** for a one-off question on a known file — shell.
For anything a colleague will run *after you* — Python, called *by*
shell. M10's scripting course turns that boundary into actual `#!/bin/
bash` files that do recon in shell and delegate analysis to `.py`
helpers — the architecture of every real data pipeline you'll inherit.

### DS framing — why this matters for your first job

Real data engineering is mostly *moving and narrowing* — and that layer
is shell-native everywhere: CI logs, Airflow/SnakeMake tasks, Spark
launchers, S3 sync wrappers. A data scientist who can compose
`find|grep|awk` pipelines debugs production systems that a pure-notebook
colleagate can only restart. (Typo preserved from a real sprint
retrospective; the point stands.)

---

## 5. What shell will *never* do (accept it)

- Joins beyond trivial (`join` exists but requires pre-sorted keys and
  hurts)
- Statistical rigor (quantiles/CIs — awk approximation ≠ inference)
- Visualization (feed a CSV to Python/R, or `gnuplot` if you must)
- Type systems (everything is text; "3" and "3.0" and "3," differ only
  by your conventions)
- Long readable logic — past ~5 stages, port to pandas

The mini-project walks this boundary deliberately: your `dq.sh` will hit
the ceiling where a Python helper is *correct*, and the report should
say so.

---

## Exercises (lab-log.md)

1. Take Workflow C's region-revenue pipeline (Lesson 5 §4) and extend
   it: shell extracts, Python one-liner computes per-region revenue
   *percentiles*... explain why that's the wrong tool choice for n=4
   regions (and what shell stat you'd use instead: sort -n | tail).
2. Convert Lesson 5's Workflow D sensor spike-detection into Pattern 3
   (shell awk → python -c for a z-score on the extracted readings).
3. Write the 5-bullet "division of labor" for YOUR thesis project's
   pipeline (guessing is fine — the exercise is the boundary-drawing).
4. Time three approaches to counting 404s in access.log: `grep -c`,
   `awk`, `python3 -c` (use `time`). Report all three; explain the
   ordering you see in terms of §1's table.
5. (Stretch) Build Pattern 1 on students.csv: shell cleans u008/u009
   (sed/tr from Lesson 4), Python reads the *cleaned* file and reports
   mean GPA by program. Two stages, one line each.

## Check yourself before the mini-project

- [ ] I can state, per task, which side of the boundary it belongs on.
- [ ] I've used `python3 -c` as a pipeline stage (sys.stdin or a file).
- [ ] I know why CSV is the safest interchange format between the two.
- [ ] I can defend "shell recon before pandas load" with the §1 table.

## Further reading (official sources)

- pandas documentation — IO tools (the other side of the handshake):
  https://pandas.pydata.org/docs/user_guide/io.html
- *Data Science at the Command Line* (2nd ed.): https://datascienceatthecommandline.com/
- PEP 8 §**scripts** — writing Python that behaves in pipelines
  (stdin/stdout discipline): https://peps.python.org/pep-0008/
