# Level 2 — Intermediate: The Analyst's Day

> Assumes M08–M13 · ~2 h · your own VM · `script level-2.log` first.
> One working day, three jobs: answer questions from data, automate
> the answer once, then make it safe for a teammate. Today the
> distinction between *using* a pipeline and *owning* it gets drawn.

## Setup (5 min)

```console
$ curl -O https://course-portal.uni.edu/labs/level2-data.tar.gz
$ tar xzf level2-data.tar.gz -C ~ && cd ~/level2
```

Contents: `weblog/` (a week of access logs, ~50k lines,
`IP method path status bytes time` space-separated), `team.csv`
(`username,role,project`), and `README` from "the previous analyst"
(one true sentence, one wrong one — part of the job is checking).

## Job 1 — Answer from evidence (30 min)

Write each answer as **one pipeline into `answers/NN.txt`** — the
file is the deliverable, the pipeline must appear in your
transcript:

1. Top 10 client IPs by request count.
2. Percentage of requests with status ≥ 400 (one decimal).
3. The busiest 15-minute window of the whole week (any correct
   bucketing; state your method in the file header comment).
4. Bytes served per hour, as `HH: total` — midnight-aligned.
5. Which `project` from `team.csv` generated the most traffic —
   requires joining the log IPs to usernames: the mapping file
   `ipmap.csv` (`ip,username`) is provided, and `join` after `sort`
   is the intended tool (awk also fine; no Excel).

## Job 2 — Make it repeatable (30 min)

1. Turn answers 1, 2 and 5 into `daily-report.sh <logfile>`:
   writes all three to stdout, exits non-zero with usage if the
   argument is missing, exits non-zero if the file doesn't exist
   — *distinct error messages for the two cases* (you'll reuse this
   reflex at every level above).
2. Test all three paths: good file, missing arg, missing file.
   Transcript shows all three exit codes.
3. `shellcheck daily-report.sh` — attach the clean output (or your
   fix commits if it wasn't clean first time; honest iterations
   score full, untested perfection scores zero).

## Job 3 — Make it safe for a teammate (40 min)

1. Create group `analysts`; create `/srv/level2` (sudo allowed
   *here only*), group-owned, SGID, group-writable, not
   world-readable.
2. Put `daily-report.sh` and the answers there. Files land
   group-writable without any post-chmod — prove it with a fresh
   file.
3. Play the teammate (second account or `sudo -u <other>`): read
   the report, attempt to delete your script — capture the result.
   Then justify the mode you gave `daily-report.sh` so teammates can
   *run* it but not *edit* it.
4. **Break it on purpose:** corrupt one line of your script
   (introduce `$?`-eating quoting bug), run it, capture the
   failure, fix it *from the error message only*, and write the
   diagnosis into `answers/incident.md` — symptom, evidence,
   cause, fix, prevention.

## Rubric (10 pts)

| Pts | Requirement |
|---|---|
| 3 | Job 1: five answer files, pipelines visible, numbers match instructor reference |
| 1 | Job 1 #5 join done on sorted keys (or correct awk hash) |
| 2 | Job 2: distinct error paths + all exit codes shown |
| 1 | Job 2 shellcheck clean (or honest iteration shown) |
| 1 | Job 3: SGID inheritance proofed with a fresh file |
| 1 | Job 3: teammate run/delete experiment captured |
| 1 | Job 3: break-and-repair with four-part incident note |

## Watch-for

- `sort` without the numeric flag on counts — "top 10" sorted
  lexically is the classic Level-2 scar.
- The wrong sentence in the previous analyst's README: whoever
  trusts it over the log data gets to explain the discrepancy in
  their incident note. Checking claims against evidence starts
  *now*, not at Level 4.
