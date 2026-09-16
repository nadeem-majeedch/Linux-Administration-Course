# Challenge Problems — Module 08

After the quiz; all against [../data/](../data/README.md) (regenerate if
you've mangled copies). Every answer: pipeline + output + one-sentence
explanation in `lab-log.md`.

- [ ] **C1 — the anomaly sweep.** In transactions.csv, find rows whose
  amount is an outlier by *order of magnitude*: mean ± threshold logic
  in awk (two-pass: mean first, then filter > 5× mean). Report count
  and the top 3. Would `sort -t, -k5 -n | tail` have found the same?
  When do the two approaches diverge?
- [ ] **C2 — the sessionizer.** access.log: group requests into
  "sessions" per IP with >60s gaps = new session. awk with a
  last-seen-per-IP array. Report: sessions per IP, top 3 by session
  count. (Hard — but it's the canonical awk state machine.)
- [ ] **C3 — the diff engine.** students.csv exists in two eras:
  original (README-documented dirt) vs your Lab 3 `.work`. Produce a
  change report: which lines changed, summarized as `id: field before →
  after` using diff + sed/awk on the diff output.
- [ ] **C4 — the one-liner loglevel plot.** server.log: render the
  hourly ERROR histogram as text bars (`uniq -c` counts → awk printf
  with `int($1/5)` `#`s). 24 rows, sorted by hour, zero-hours included
  via seq | paste if you dare.
- [ ] **C5 — the regex golf.** Write the *shortest* ERE that matches
  exactly the four product names in transactions.csv but none of the
  regions. Verify both directions (grep -c against each column's
  universe). Then the same for sensor IDs s1–s3 vs timestamps.
- [ ] **C6 — the pipeline race.** Same question, three implementations:
  count requests per endpoint (access.log). (a) grep|cut|sort|uniq,
  (b) awk single pass, (c) your best. `time` all three ×10 runs;
  report means and explain the ranking in terms of process count.
- [ ] **C7 — the format converter.** students.csv → a fixed-width
  .txt report (columns 12/24/6/4 chars, right-aligned GPA) using only
  awk printf. Then reverse-engineer: parse your own fixed-width back to
  CSV with cut -c ranges. Two pipelines, lossless round-trip.
- [ ] **C8 — the mystery file.** Have a partner (or generate: shuffle
  transactions.csv, corrupt 3 rows — wrong field count, a swapped
  delimiter, a duplicated line) hand you an unknown CSV. Run your
  mini-project `dq.sh` (or the Lesson 5 §7 checklist if unfinished) and
  write the diagnosis. Time-box: 10 minutes — analysts don't get all
  day.

C2 is the "interview question" of this module: stateful awk under
pressure. C6 is the performance intuition Lesson 6 argues in prose.
