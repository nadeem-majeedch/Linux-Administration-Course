# Lab 2 — Log Forensics: Incident Analysis with Pipelines

> Module 08 · Unit 2 · Difficulty: Intermediate
> Time: ~45 min · Read-only against the datasets
> Prerequisites: [Lesson 4](../lessons/04-sed-awk-xargs.md), [Lesson 5](../lessons/05-ds-pipelines.md)

**Scenario:** it's 08:30. The on-call dashboard flagged `api-gateway`
overnight. You have `access.log` (500 requests) and `server.log` (600
events) and forty minutes before standup. Build the answers as
pipelines; every answer needs its command *and* its output in
`lab-log.md`.

## Part A — establish the timeline

```console
$ head -1 server.log | cut -d' ' -f1          # window start
$ tail -1 server.log | cut -d' ' -f1          # window end
$ awk '{print substr($1,1,10)}' server.log | sort | uniq -c   # events per day
```

**Record:** the covered window and events/day. (Forensics rule one:
know your data's *time coverage* before interpreting any rate.)

## Part B — the error profile

```console
$ awk '{print $3}' server.log | sort | uniq -c | sort -rn     # level census
$ grep -c "ERROR" server.log                                  # headline number
$ awk '$3 == "ERROR" {print $4}' server.log | sort | uniq -c | sort -rn   # by service
```

**Record:** total errors, per-service ranking, and the service you'd
page first (one sentence of justification *from the numbers*).

## Part C — temporal pattern (the grafana-in-one-line drill)

```console
$ grep "ERROR" server.log | cut -d' ' -f2 | cut -d: -f1 | sort | uniq -c
$ grep "ERROR" server.log | awk '{print substr($2,1,5)}' | sort | uniq -c | sort -k2 | head -8
```

**Record:** the hourly histogram. Do errors cluster? (Our data: they
accumulate through the day — which services *also* peak then? Cross-ref
Part B's worst service with `grep <svc> | histogram`.)

## Part D — correlate the two logs

`access.log` is the edge view (HTTP), `server.log` the internal view.
Find the same incident in both:

```console
$ awk '$9 == 500 {print $4, $7}' access.log | sort | uniq -c | sort -rn   # 500s by ip+path
$ awk '$9 == 500 {print $7}' access.log | sort | uniq -c | sort -rn       # by endpoint
$ grep "models/run" server.log | grep -c ERROR                            # internal view, same story?
```

**Record:** the top-500 endpoint, whether server.log's ERROR lines
agree in proportion, and one sentence on *why two logs are better than
one* (what can each see that the other can't?).

## Part E — the slow-query investigation

```console
$ grep "slow query" server.log | grep -oE "[0-9]+ms" | sed 's/ms//' | sort -rn | head -5
$ grep "slow query" server.log | grep -oE "[0-9]+ms" | sed 's/ms//' | \
    awk '{s+=$1; n++; if ($1 > m) m = $1} END {printf "n=%d mean=%.0f max=%.0f\n", n, s/n, m}'
$ grep "slow query" server.log | cut -d' ' -f4 | sort | uniq -c | sort -rn | head -3   # who's slow
```

**Record:** n/mean/max latency, the slowest service, and — the analyst
move — whether the *slow* services match the *error* services (Part B).
One sentence: correlation or coincidence?

## Part F — the incident summary (deliverable)

Five bullets, each backed by a pipeline from above:

1. Window + volume
2. Error headline + worst service
3. Temporal pattern
4. Cross-log confirmation (or contradiction)
5. Recommended next probe (be specific: which command would you run
   next, on which file?)

This mirrors real incident reports — numbers first, narrative second,
next-step always.

## Done when

- [ ] Parts A–E recorded with commands AND outputs
- [ ] The five-bullet incident summary written
- [ ] Every claim in the summary traces to a pipeline you ran
