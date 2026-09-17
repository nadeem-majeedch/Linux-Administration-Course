# Mini-Project A — Dataset QC Toolkit

> Module 10 · Unit 3 · Difficulty: Intermediate
> Deliverables: `dq.sh` · `summary.sh` · optional `clean.sh` ·
> `README.md` · all shellcheck-clean
> Prerequisites: both [M10 labs](labs/README.md); M08 datasets; M09
> pipelines
> ⚠️ Safety envelope: tools operate only on files given as arguments;
> `clean.sh` (if attempted) moves to a `trash/` subdirectory — it
> never deletes. Every tool: strict mode, guards, stderr logs, data
> on stdout.

You are the data engineer for a small team. Every week a folder of
CSVs arrives — and every week someone (you) eyeballs row counts,
hunts duplicates, and squints at columns. Build the toolkit that
does the eyeballing.

## Deliverable 1 — `dq.sh` (the validator)

**Usage:** `dq.sh FILE [FILE...]` — accepts *multiple* files (arrays
+ `"$@"` from Lesson 4).

Per file, report: row count (excl. header), duplicate-ID count,
empty-cell count, and a verdict `OK` / `WARN` / `FAIL` with
thresholds as `readonly` variables at the top (documented). Any FAIL
→ the *script* exits non-zero (67) after reporting on all files.

Contract: exit 64 wrong usage · 66 missing/unreadable input · 67 any
file failed QC · 0 all clean. All four paths demonstrated in the
transcript.

## Deliverable 2 — `summary.sh` (the reporter)

**Usage:** `summary.sh DIR` — for every CSV in DIR, one line to
stdout (and *only* that line shape, so output is pipeable):

```text
rows  dupes  empties  file
1201  3      14       sales_2026.csv
```

Then a final totals line. Errors and progress to stderr. Reuse `dq.sh`'s
QC logic *by importing it* — `source ./lib.sh` if you extract a
shared library (recommended), or by calling `dq.sh` per file. State
which approach you chose in the README and why.

## Deliverable 3 — `clean.sh` (optional, the hardening exercise)

**Usage:** `clean.sh FILE` — strips empty rows and trims whitespace
via M08 tools, writing `FILE.clean` **without touching the original**
(backup-before-modify; atomic-ish write to temp + mv is M11's — for
now, write a `.clean` sibling). Refuse to "clean" a file you can't
read, and refuse an output name that already exists.

## Deliverable 4 — `README.md` (the rung-5 difference)

Half a page: purpose of each tool, usage lines, exit-code table, QC
thresholds and *why they're what they are*, one "limitations" section
(comma-in-quoted-fields, encoding — the honest C4 assumption), and
one "how I tested" section pointing at the transcript.

## Grading (20 pts)

| Item | Pts |
|---|---|
| `dq.sh`: multi-file, verdicts, exit-code contract demonstrated | 6 |
| `summary.sh`: pipeable stdout, totals, reuse approach justified | 5 |
| `clean.sh` (optional): safe sibling-write, refusals | 2 |
| README: contract + thresholds + limitations + testing | 4 |
| All scripts: strict mode, `bash -n`, `shellcheck` zero findings | 3 |

## Submission layout

```text
~/lab10/project-a/
├── dq.sh
├── summary.sh
├── clean.sh          (optional)
├── lib.sh            (if shared logic extracted)
├── README.md
└── transcript.md     (all failure paths, a full clean run, shellcheck silence)
```

## Where this leads

M11 hardens this exact toolkit — `--dry-run`, trap-based temp
cleanup, idempotency, `getopts` options — and Mini-Project E (M24)
adds health checking. The QC thresholds you choose here become the
`health.sh` philosophy there: **verdicts with documented thresholds,
not vibes.**
