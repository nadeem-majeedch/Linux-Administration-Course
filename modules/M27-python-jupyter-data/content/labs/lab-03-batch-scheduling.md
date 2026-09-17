# Lab 3 — Batch Scheduling the Course-Way

> Module 27 · Unit 7 · Difficulty: Intermediate
> Time: ~45 min · Environment: your own VM
> Prerequisites: [Lesson 3](../lessons/03-background-workloads.md), [M19](../../../M19-scheduling-cron-timers/README.md)
> ⚠️ Everything under `~/projects/sales-analysis/`; no system
> paths. Scheduled jobs *log* — silently-failing automation is
> the bug we refuse to ship.

The capstone pattern: turn Lab 1's dataset into a nightly
automated pipeline — venv-Python, cron-scheduled, logged,
idempotent, and *verified to have run*.

## Part A — the script (15 min)

`~/projects/sales-analysis/scripts/nightly_summary.sh`:

```bash
#!/usr/bin/env bash
# Nightly regional summary. Idempotent: same inputs → same output.
set -euo pipefail

PROJECT="/home/ds/projects/sales-analysis"
PY="$PROJECT/.venv/bin/python"          # no activation needed (Lesson 1 §4)
STAMP="$(date +%Y-%m-%d)"
OUT="$PROJECT/outputs/summary-$STAMP.txt"

mkdir -p "$PROJECT/outputs"
# truncate-then-replace: safe re-run, no append drift
: > "$OUT.tmp"
"$PY" - "$PROJECT/data/raw/sales.csv" "$OUT.tmp" <<'EOF'
import sys
import pandas as pd
df = pd.read_csv(sys.argv[1])
summary = df.groupby("region")["revenue"].agg(["sum", "mean", "count"])
summary.to_csv(sys.argv[2], sep="\t")
EOF

mv "$OUT.tmp" "$OUT"                    # atomic rename (M11 §2)
echo "[$(date -Is)] wrote $OUT" >> "$PROJECT/outputs/nightly.log"
```

Verify by hand first — **twice** (idempotency check: second run
replaces, not duplicates):

```console
$ chmod +x scripts/nightly_summary.sh
$ scripts/nightly_summary.sh && cat outputs/summary-*.txt
$ scripts/nightly_summary.sh && wc -l outputs/summary-*.txt   # same count
$ tail -2 outputs/nightly.log
```

## Part B — schedule it (10 min)

```console
$ crontab -e
# 02:15 daily — the non-minute-0 slot that survives the batch (M19 §2)
15 2 * * *  /home/ds/projects/sales-analysis/scripts/nightly_summary.sh >> /home/ds/projects/sales-analysis/outputs/cron.log 2>&1
$ crontab -l                     # read-back proof it was saved
```

## Part C — simulate the cron environment (15 min)

Don't wait for 02:15 — *prove* it works under cron's sparse
environment by running the exact command cron will run, but
stripped of your interactive niceties (M19 Lab 2's technique):

```console
$ env -i HOME="$HOME" LOGNAME="$USER" SHELL=/bin/sh PATH=/usr/bin:/bin \
    /home/ds/projects/sales-analysis/scripts/nightly_summary.sh && \
    ls -la outputs/ && tail -2 outputs/cron.log 2>/dev/null; \
    tail -1 outputs/nightly.log
```

The `env -i` wrapper is the rehearsal: if the script works here,
it works under cron — because it made **no** assumption about
PATH, aliases, or an activated venv (the three things that kill
scheduled jobs — M19 §1). Fix-forward rule: any failure here is a
script bug to harden, not a cron mystery.

**Forward trigger:** set a temporary
`* * * * *` line for one minute, watch
`outputs/nightly.log` grow, then remove it. The log line
`[2026-…] wrote outputs/summary-…` appearing *without you
running anything* is the loop closed.

## Part D — failure drill (5 min)

Point `DATA` at a missing file (rename the CSV), run once by
hand, observe: nonzero exit, `set -e` stops the pipeline, no
half-written summary (the `.tmp` never promoted), and the cron
log would carry the traceback. **Restore** the filename. This is
the fail-loudly contract: you *want* the scheduled job to make
noise when its data vanishes — silence is the real outage
(M24 §4's incident discipline).

## Done when

- [ ] Script runs clean twice with identical output (idempotency)
- [ ] Crontab entry saved with read-back proof; redirect discipline
      visible (`>> … 2>&1`)
- [ ] Part C `env -i` rehearsal passed **or** the failure it exposed
      was fixed and re-passed
- [ ] Part D: the missing-data run failed loudly, no partial output,
      data restored
- [ ] One paragraph: what the `log line + summary file` pair proves
      about last night — and what it can't (hence monitoring,
      M24)
