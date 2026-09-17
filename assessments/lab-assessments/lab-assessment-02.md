# LA-2 — Pipeline Fluency (25 min)

> Assesses: M09–M10 labs · 10 points · evidence transcript required.
> Environment: student's own VM. Setup: `curl -o ~/la2.log` the
> cohort sample log (or the instructor distributes `sample.log`).
> Format reference:
>
> ```text
> 2026-03-03T09:14:02Z INFO  upload  user=sam bytes=204800
> 2026-03-03T09:14:03Z ERROR upload  user=lee bytes=0
> 2026-03-03T09:15:10Z INFO  query   user=sam bytes=4096
> ```

## Tasks

Answer each with **one pipeline** (single line, may use `;` between
sub-answers). Save all outputs into `~/la2/answers/` with the given
filenames — the files are the deliverable.

**T1 (2).** `total_lines.txt` — number of lines in the log.

**T2 (2).** `error_users.txt` — usernames that produced ERROR
lines, deduplicated, sorted.

**T3 (2).** `bytes_per_user.txt` — total bytes per user across all
lines, sorted descending. (Parsing `key=value` fields is expected;
awk is the intended tool but any correct pipeline counts.)

**T4 (2).** `last_error.txt` — the *full line* of the most recent
ERROR entry, plus its line number in the file, in the form
`<lineno>: <line>`.

**T5 (2).** `daily_counts.txt` — per-date count of lines
(`2026-03-03 42` style), sorted by date.

## Rubric

| Points | Requirement |
|---|---|
| 1 | T1 output is exactly one number, nothing else |
| 1 | T2 dedup + sort (`sort -u` or `sort | uniq`) — raw list caps at 0.5 |
| 1 | T3 correct totals (instructor has the reference values) |
| 1 | T3 numeric descending sort (`sort -rn` or awk END block) |
| 1 | T4 returns the *line*, not the count (`grep -n` + `tail -1`) |
| 1 | T4 preserves the original line content intact |
| 1 | T5 groups on the date field (first column before `T`) |
| 1 | All five files present with correct names |
| 1 | Every answer is a single pipeline (no intermediate temp files beyond the deliverables) |
| 1 | Transcript shows each pipeline before its output file is checked |

## Common failures

- T3 summing with `paste`/`bc` loops — works but fails the
  single-pipeline rule; cap 0.5.
- T4 using `tac | grep -m1` without restoring order — accept only
  if the *line number* is still correct.
- Manual inspection answers pasted into files — zero for that task;
  the pipeline must be visible in the transcript.
