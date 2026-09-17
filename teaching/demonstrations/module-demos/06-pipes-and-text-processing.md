# Demo 6 — Pipes & Redirection: Where the Bytes Go

> **Session:** S8 · **Duration:** ~12 min (two natural halves) ·
> **Risk:** low (sacrificial files in `~/demolab`) · **Objective:** the
> redirection x-y table as *lived experience* — including the
> truncate-before-exec surprise that makes `>` forever dangerous.

## Prerequisites

- Demo VM terminal projected
- A course log file on hand (or generate the sample below)

## Setup

```console
$ mkdir -p ~/demolab && cd ~/demolab
$ cat > app.log <<'EOF'
2026-09-17T09:00:01 INFO  boot complete
2026-09-17T09:00:04 ERROR disk latency high
2026-09-17T09:01:22 INFO  cache warm
2026-09-17T09:02:40 ERROR disk latency high
2026-09-17T09:03:10 WARN  retry 1
2026-09-17T09:04:05 ERROR disk latency high
EOF
$ echo "precious data" > f.txt
```

## Procedure — half 1: building the pipeline

**Step 1 — one stage at a time, predicting each shape.**

```console
$ grep ERROR app.log                  # 3 lines
$ grep ERROR app.log | cut -d' ' -f1  # 3 timestamps
$ grep ERROR app.log | cut -d' ' -f4  # 3 identical messages
```

*Narration after the third:* "Same message three times — who wants a
count? What must happen before `uniq -c` can help?" (sort — elicit it,
don't say it.)

```console
$ grep ERROR app.log | cut -d' ' -f4 | sort | uniq -c
      3 disk latency high
```

**Step 2 — the x-y table, built interactively.** For each row, students
predict, then you run:

| Command | Where do the bytes go? |
|---|---|
| `wc -l app.log` | stdout, with the *filename* |
| `wc -l < app.log` | stdin — count only, no name |
| `grep ERROR app.log > out.txt` | file (stdout); stderr still *prints* |
| `grep EROR app.log 2> err.txt` | error → file; stdout empty |
| `grep ERROR app.log >> out.txt` | file, appended |

**Step 3 — the truncation trap (planned failure).**

```console
$ wc -c f.txt
13
$ grep ERROR app.log > f.txt      # f.txt had "precious data"...
$ cat f.txt                        # ...and now it's grep output
2026-09-17T09:00:04 ERROR disk latency high
...
```

*Narration:* "The shell opened `f.txt` for writing — *truncating it* —
**before** grep ran. The redirect isn't part of grep; it's the shell's
work, done first. `>` is overwrite-shaped, always."

## Procedure — half 2: stderr separation

```console
$ ls exists.txt nope.txt > out.txt 2> err.txt
$ cat out.txt err.txt
```

*Narration:* "Two streams, two files — a pipeline can't sort truth from
noise if both share a spout. `2>&1` merges them; order matters:
`cmd > f 2>&1`, not `cmd 2>&1 > f`."

## Expected output

Exactly as above for the heredoc sample; counts differ with your own
log file (say so).

## Questions to ask

1. After the truncation: "when *would* you want truncation?" (fresh
   reports, log rotation — it's a feature with sharp edges)
2. "Why does `wc -l < f` lose the filename?" (stdin has no name — the
   tool prints what it knows)
3. "You want one file with output AND errors, errors *interleaved*
   naturally — which redirection?"

## Common errors & recovery

- `grep ERROR` case-sensitivity surprises (no matches) — `grep -i` or
  note the exactness lesson
- Heredoc EOF not at line start (nested in a script) — the terminal
  waits; Ctrl-C and retype with `EOF` alone on the line
- Students' own `>>` vs `>` confusion mid-lab — back to the table row

## Recovery

All artifacts are disposable demo files; cleanup below. The lesson's
*point* is that some mistakes aren't recoverable — that's why the
sacrificial `f.txt` says "precious data" on purpose.

## Cleanup (census)

```console
$ ls ~/demolab
$ rm -r ~/demolab && ls ~/demolab 2>&1
```

## Optional extension

`tee out.txt` in the middle of the pipeline — watch the data flow
*through* to the screen while landing in the file; the tee verb returns
in every transfer/backup script later in the course.
