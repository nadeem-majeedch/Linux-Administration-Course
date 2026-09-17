# 7 — Text Processing

> Learn it: [M08 — Text Processing](../modules/M08-text-processing/content/README.md) ·
> [M09 — Pipes & Redirection](../modules/M09-pipes-and-redirection/content/README.md) ·
> Lookup, not understanding.

## Viewing

| Command | Purpose | Key options | Example |
|---|---|---|---|
| `cat` | dump small files | `-n` number lines | `cat config.txt` |
| `less` | page through big ones | `/pat` search · `q` quit · `F` follow | `less +F app.log` |
| `head -n K` | first K lines | `-n` count | `head -5 data.csv` |
| `tail -n K` | last K lines | `-f` follow · `-F` follow+rotate-safe | `tail -f /var/log/syslog` |
| `wc` | count | `-l` lines · `-w` words · `-c` bytes | `wc -l data.csv` |

## Redirection & pipes

| Form | Effect |
|---|---|
| `CMD > FILE` | stdout → file (overwrite ⚠️) |
| `CMD >> FILE` | stdout → file (append) |
| `CMD 2> FILE` | stderr → file |
| `CMD > out 2> err` | both, separately |
| `CMD &> FILE` | both, one file |
| `CMD 2> /dev/null` | discard stderr |
| `A \| B` | A's stdout → B's stdin |
| `A \| tee FILE \| B` | branch: keep a copy while piping |
| `$(CMD)` | command substitution |

## grep — select lines

| Option | Effect | Example |
|---|---|---|
| (basic) | fixed-ish patterns | `grep error app.log` |
| `-i` | case-insensitive | `grep -i fail app.log` |
| `-v` | invert match | `grep -v '^#' conf` |
| `-n` | line numbers | `grep -n TODO src/*.py` |
| `-r` | recursive | `grep -r psycopg2 project/` |
| `-E` | extended regex | `grep -E '^(GET\|POST)' access.log` |
| `-c` | count only | `grep -c ERROR app.log` |
| `-l` | filenames only | `grep -l secret *.env` |
| `-w` | whole word | `grep -w OK results.txt` |
| `-A/-B/-C N` | context after/before/both | `grep -C 2 panic dmesg.txt` |

Regex crib: `^` start · `$` end · `.` any char · `[abc]` class ·
`*` 0+ · `+` 1+ (with `-E`) · `\|` alternation (with `-E`) ·
`\<word\>` word boundary.

## cut / paste / tr — fields & characters

| Command | Effect | Example |
|---|---|---|
| `cut -d, -f2` | 2nd comma-field | `cut -d, -f1 names.csv` |
| `cut -c1-8` | char columns | first 8 chars of timestamps |
| `paste A B` | interleave files side-by-side | `paste names.txt scores.txt` |
| `tr SET SET2` | translate/delete chars | `tr a-z A-Z` · `tr -d '\r'` (Windows CR) · `tr ' ' '\t'` |

## sort / uniq — ordering & counting

| Option | Effect |
|---|---|
| `-n` | numeric sort (the forgotten classic) |
| `-r` | reverse |
| `-h` | human sizes (`2K`, `1M`) |
| `-k N` | sort by field N (`-k2,2nr` common) |
| `-u` | unique (implies uniq) |
| `-t X` | field separator |

```console
$ sort -t, -k2 -rn scores.csv | head      # top by 2nd field, numeric
$ sort names.txt | uniq -c | sort -rn     # frequency table
```
`uniq` only collapses **adjacent** duplicates — it almost always
follows `sort`.

## sed — stream edit

| Form | Effect | Example |
|---|---|---|
| `s/old/new/` | substitute first per line | `sed 's/foo/bar/' f` |
| `s/old/new/g` | all per line | `sed 's/,/;/g' f` |
| `-n 'Np'` | print line N only | `sed -n '5p' f` |
| `-n '/pat/p'` | grep-ish | `sed -n '/ERROR/p' app.log` |
| `Nd` | delete line N | `sed '1d' f` (drop header) |
| `-i` | **edit file in place** | ⚠️ test without `-i` first; `-i.bak` keeps a backup |

## awk — columns with logic

```bash
awk -F, '{print $1, $3}' data.csv              # fields 1 and 3 (comma-separated)
awk -F, 'NR>1 {s+=$2} END {print s}' data.csv  # sum column 2, skip header
awk '$3 >= 400 {c++} END {print c+0}' access.log
awk -F, '{print $2}' | sort | uniq -c | sort -rn   # frequency of col 2
```
Patterns: `NR` line number · `NF` fields on this line · `BEGIN{}` /
`END{}` blocks · `-F` sets the separator.

## xargs — build commands from input

| Form | Effect |
|---|---|
| `… \| xargs CMD` | append input as arguments |
| `… \| xargs -n1 CMD` | one item per invocation |
| `… \| xargs -I{} CMD {}` | place item explicitly |
| `… \| xargs -P4 CMD` | 4 parallel workers |
| `… \| xargs -r CMD` | skip run if input empty (GNU) |

```console
$ find . -name '*.log' -print0 | xargs -0 gzip     # the safe null-separated form
$ cat urls.txt | xargs -n1 -P4 curl -sO
```

## find + processing

```console
$ find data -name '*.csv' -mtime -7          # changed this week
$ find . -type f -printf '%s %p\n' | sort -rn | head    # ten biggest
```

## The reference pipeline

```console
$ tail -n +2 sales.csv | cut -d, -f2 | sort | uniq -c | sort -rn | head -5
  (skip header)   (pick column)   (group)  (count)    (rank)     (top 5)
```
Shell text tools *complement* pandas: use them to triage gigabytes
before loading anything, and to script the boring 90%.
