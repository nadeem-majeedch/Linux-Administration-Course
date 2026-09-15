# Lab 1 — Log Wrangling with Redirection

> Lesson 1 · Time: ~45 min · Risk: zero — everything lives in `~/scratch/m09`

## Goal

Handle a realistic app log with pure redirection: separate errors from noise,
build an append-only archive, and archive *both* result and evidence streams —
the exact workflow M24's incident analysis will assume you own.

## Part 1 — Generate the corpus (5 min)

```console
$ mkdir -p ~/scratch/m09 && cd ~/scratch/m09
$ for u in alice bob carol; do
>   echo "$(date +%T) INFO  login  user=$u"
> done > sessions.log
$ echo "$(date +%T) ERROR db     timeout after 30s" >> sessions.log
$ echo "$(date +%T) WARN  cache  miss ratio 0.42" >> sessions.log
$ echo "$(date +%T) INFO  logout user=alice" >> sessions.log
$ echo "$(date +%T) ERROR api    500 on /orders" >> sessions.log
$ cat sessions.log
```

(First taste of a `for` loop — M10's subject; today it's a typing-saving
suggestion. `>` on the first block *created* the file; `>>` grew it.)

## Part 2 — The three streams, handled (10 min)

```console
$ ls /root > roots.txt 2> roots.err        # prediction FIRST: which file gets content?
$ cat roots.txt roots.err
$ ls sessions.log /nope > both.txt 2>&1    # merge: what lands in both.txt, in what order?
$ ls sessions.log /nope > ok.txt 2> /dev/null   # silence the noise deliberately
```

Log each command with its outcome and one line on *why* the streams split the
way they did. Confirm `echo $?` reports failure even when stderr is silenced.

## Part 3 — Append-only archive (10 min)

```console
$ grep ERROR sessions.log > errors-now.txt
$ date >> archive.log; cat errors-now.txt >> archive.log; wc -l >> archive.log
$ cat archive.log
```

Run the second line **twice**, one minute apart — the file grows both times
(vs. `>` which would truncate). This append-only shape is how job logs, backups'
manifests, and audit trails work (M11, M19, M24 all assume it).

## Part 4 — tee: live view + archive (10 min)

```console
$ grep -c INFO sessions.log | tee count.txt
$ grep ERROR sessions.log | tee -a archive.log | wc -l
```

Second command: three stages — select errors, *append them to the archive*,
count them. Log what `tee` passed along vs what it stored. Then the M24
preview: `grep -v INFO sessions.log | tee problems.txt | wc -l` — is `wc -l`'s
number equal to `cat problems.txt | wc -l`? Why must it be?

## Part 5 — The header/body split (10 min)

```console
$ printf 'id,amount\n1,100\n2,250\n3,90\n' > amounts.csv
$ head -1 amounts.csv > header.csv
$ tail -n +2 amounts.csv > body.csv
$ cat header body.csv > rejoined.csv
$ diff amounts.csv rejoined.csv && echo IDENTICAL
```

Log the diff's silence (success convention!) and what `&&` did with it. Then
break the rejoin on purpose (`cat body.csv header > wrong.csv`) — diff again;
the ordering is *data semantics*, not cosmetics.

## Wrap-up checklist

- [ ] All five parts logged with before/after file states
- [ ] `2>&1` ordering explained in your own words
- [ ] Archive grew across two runs (append-only demonstrated)
- [ ] Header/body split round-trips to IDENTICAL
- [ ] Zero files touched outside `~/scratch/m09`
