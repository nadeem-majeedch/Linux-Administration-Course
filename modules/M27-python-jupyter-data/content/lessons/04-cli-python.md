# Lesson 4 — Command-Line Python: One-liners, -m Idioms and Pipelines

> Module 27 · Unit 7 · Difficulty: Intermediate
> Reading time: ~20 min
> Up next: [Lab 1 — environments](../labs/lab-01-environments.md)

---

## 1. Python as a pipeline citizen

[M08](../../../M08-text-processing/content/README.md) gave you
grep/cut/awk pipelines; [M10](../../../M10-bash-scripting/content/README.md)
made them scripts; this lesson puts **Python itself** in the
pipeline — the interpreter invoked from the shell, doing the
structured-data work text tools find awkward (real CSV parsing,
JSON surgery, timestamps), then handing its output to the next
stage like any filter. The DS payoff: `python -c` handles the
quoted-CSV and nested-JSON cases where awk bends, without leaving
the terminal.

## 2. `python -c` — the one-liner

```console
$ python3 -c "print(sum(1 for _ in open('data.csv')))"     # line count, Python-style
1201
$ cat sales.csv | python3 -c "import sys, csv; rows=list(csv.reader(sys.stdin)); print(len(rows[0]), 'columns')"
5 columns
```

The contract: `-c "code"` runs the string; **`sys.stdin` is the
pipeline input**, `print` is the output — Python as a filter.
Quoting rule ([M19's](../../../M19-scheduling-cron-timers/content/README.md)
environment lesson echoing): double quotes outside for the shell,
single quotes inside for Python strings — and the idiom is
one-expression long; anything longer graduates to a script (§5).

The everyday one-liners worth reflexes:

```console
$ python3 -m json.tool response.json | head -20          # pretty-print/validate JSON (an API curl's best friend)
$ python3 -c "import json,sys; d=json.load(open('c')); print(sorted(d, key=d.get)[-3:])"  # top-3 keys
$ python3 -c "from datetime import date; print(date.today().isoformat())"   # 2026-09-15
$ python3 -c "print(f'{1234567:,}')"                      # 1,234,567 — formatting on tap
```

## 3. `-m` — run the module, not the file

`python -m <module>` executes a module as a script — the form
that fixes half of Python's CLI mysteries:

```console
$ python3 -m pip install pandas       # pip *bound to this interpreter* (Lesson 1 §3)
$ python3 -m venv .venv               # the canonical venv creation
$ python3 -m json.tool f.json         # json as a CLI tool
$ python3 -m http.server 8000 --bind 127.0.0.1    # instant file server (M21/M22 labs)
$ python3 -m timeit "'-'.join(str(n) for n in range(100))"   # micro-benchmark
```

Why `-m` beats `python path/to/module.py`: it resolves the module
*from sys.path with your environment* — the venv-correct, cwd-safe
invocation. `python -m pip` is the course habit for exactly this
reason; `python -m http.server --bind 127.0.0.1` is the lab
server from three modules, now explained.

## 4. Structured data through the pipe

Where Python earns its pipeline seat — the cases M08 flagged as
awk-hostile:

```console
# real CSV: quoted commas survive (awk's nemesis)
$ python3 -c "
import csv, sys
for row in csv.reader(sys.stdin):
    print(row[0], row[3])
" < sales.csv | sort | uniq -c | sort -rn | head

# nested JSON from an API, flattened
$ curl -s http://127.0.0.1:8000/api/sales/summary | python3 -c "
import json, sys
for row in json.load(sys.stdin):
    print(f\"{row['region']},{row['total']:.2f}\")
"

# timestamp arithmetic across a log
$ grep INFO server.log | python3 -c "
import sys
from datetime import datetime
ts = [datetime.fromisoformat(l.split()[0]) for l in sys.stdin]
print('span:', ts[-1] - ts[0])
"
```

Each is a *filter* — stdin to stdout, composable, exit-code-honest
(§5) — and each is one `import` away from the full standard
library. The design rule stays M10's: text tools for text-shaped
problems; Python for structure; **the pipeline stays the
pipeline** — Python in it, not instead of it.

## 5. Scripts with shebangs — the graduation

The one-liner that grew:

```python
#!/usr/bin/env python3
"""csv_stats.py — column statistics for a CSV. Usage: csv_stats.py FILE [COLUMN]"""
import csv, sys

def main():
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} FILE [COLUMN]", file=sys.stderr)
        return 64
    try:
        with open(sys.argv[1], newline="") as f:
            rows = list(csv.DictReader(f))
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 66

    col = sys.argv[2] if len(sys.argv) > 2 else next(iter(rows[0]))
    values = [float(r[col]) for r in rows]
    print(f"n={len(values)} min={min(values):.2f} max={max(values):.2f} "
          f"mean={sum(values)/len(values):.2f}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

```console
$ chmod +x csv_stats.py && ./csv_stats.py sales.csv amount
n=1200 min=12.50 max=987.00 mean=243.17
$ ./csv_stats.py; echo $?                       # → 64 (usage) — the M10 contract
```

Every course discipline lands: shebang, docstring-as-usage,
argument guard with 64/66, stderr for errors, `sys.exit(code)` for
the caller. In an activated venv, `#!/usr/bin/env python3` resolves
to *the venv's* interpreter (PATH, again) — so the script inherits
the project's pandas without saying so. That's the bridge to
[M11's](../../../M11-advanced-shell-automation/content/README.md)
automations and [M19's](../../../M19-scheduling-cron-timers/content/README.md)
scheduled jobs: a Python script that is a first-class Unix
command.

## 6. Try it now (20 minutes)

1. The filter trio: run §4's three pipelines against your own
   data/API — each through `sort | uniq -c` or `python -m
   json.tool` for a second stage.
2. `-m` tour: `python3 -m json.tool` on a config; `python3 -m
   http.server 8000 --bind 127.0.0.1` + curl + Ctrl-C; `python3 -m
   timeit` on two string-building idioms.
3. Graduate `csv_stats.py`: chmod, run on two columns, then the
   exit-code paths (no args → 64; missing file → 66) with `echo $?`.
4. The stdin/stdout witness: `python3 -c "import sys;
   sys.stdout.write('out\n'); sys.stderr.write('err\n')" 2>/dev/null`
   — then swap the redirect. The two streams, separated exactly as
   M10's logging contract demanded.

## 7. Common mistakes

- Unbounded input: `open('data.csv').read()` on a 10 GB file —
  stream (`for line in f`, `chunksize=`) or die by memory (M24's
  OOM incident, self-inflicted edition).
- Quoting collisions: nested same-quote strings in `-c` — switch
  outer/inner quotes or graduate to a script.
- `python` vs `python3` — on Ubuntu, `python` may not exist (or
  may be something else); say `python3` (or the venv's python)
  explicitly.
- Swallowing stdin: a `-c` filter that opens files by name *and*
  ignores `sys.stdin` — pick the contract (filter or file-tool)
  and honor it.
- One-liners growing past a screen — the script with shebang,
  guards, and exit codes is the maintenance form; `-c` is for
  expression-sized work.

> **Next:** [Lab 1 — environments](../labs/lab-01-environments.md):
> build, freeze, recreate, verify — the reproducibility contract,
> enforced hands-on.
