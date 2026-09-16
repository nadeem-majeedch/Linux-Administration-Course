# M08 Command Reference — the Toolkit on One Page

Organized by pipeline stage. Every entry: *what* (syntax), *why* (the
question it answers), *watch out* (the trap). Examples use the module
datasets in [data/](data/README.md).

## View & Count

| Command | Syntax | Use it when | Watch out |
|---|---|---|---|
| `cat` | `cat f1 f2 > out` | concatenating streams/files | useless use: `cat f \| grep x` — grep takes files |
| `less` | `less +F server.log` | reading big files; live follow | `/pat` then `n`; `q` quits, `F` re-follows |
| `head` | `head -3 f` / `head -c 500 f` | schema peek (`-1`), sampling | header-aware: `tail -n +2` for body |
| `tail` | `tail -f app.log` / `tail -n +2` | live logs; header stripping | `-f` forever until Ctrl-C |
| `wc` | `wc -l f` | scale check before loading | `< f` drops the filename; `-l` alone for clarity |

## Find

| Command | Syntax | Use it when | Watch out |
|---|---|---|---|
| `find` | `find . -name "*.csv" -size +10k` | files by name/size/age | QUOTE globs; `-exec ... {} +` to act |
| `find -exec` | `find . -name "*.log" -exec wc -l {} +` | batch action on hits | `+` = batch (fast), `\;` = one-by-one |
| `locate` | `locate -i report` | instant whole-disk name search | index freshness (`sudo updatedb`) |

## Filter & Match

| Command | Syntax | Use it when | Watch out |
|---|---|---|---|
| `grep` | `grep -c ERROR server.log` | line filtering, counting | use `-E` for modern regex |
| `grep -v` | `grep -v INFO f` | exclude | remember it also excludes lines *containing* INFO |
| `grep -o` | `grep -oE "[0-9]+ms" f` | token extraction | feeds `sort \| uniq -c` for censuses |
| `grep -r` | `grep -rl ERROR --include="*.log" .` | search trees | `-l` = filenames only |
| context | `grep -C2 404 access.log` | debugging around a hit | -A/-B/-C: after/before/both |

**Regex pocket card (ERE):** `^start` · `end$` · `.` any · `[abc]` set ·
`[0-9]{2,4}` count · `a|b` union · `col?` optional · `\.` literal dot.
Regexes match *lines*, not grammars — no HTML/JSON parsing.

## Columns & Categories

| Command | Syntax | Use it when | Watch out |
|---|---|---|---|
| `cut` | `cut -d, -f2,4 f` | fixed single-char delimiters | quoted fields break it; no last-field — use awk |
| `cut -c` | `cut -c1-10 f` | fixed-width columns | counts *characters* incl. delimiter |
| `sort` | `sort -t, -k5 -nr f` | ordering, numeric, by key | `-n` or `10 < 9`!; `-u` dedupes |
| `uniq` | `... \| sort \| uniq -c \| sort -rn` | censuses | **adjacent lines only** — sort first, always |
| `uniq -d` | `sort \| uniq -d` | find dupes | duplicates = adjacent pairs |
| `paste` | `paste -d, f1 f2` | merge streams side-by-side | process substitution: `paste <(a) <(b)` |
| `tr` | `tr '\t' ','` / `tr -s ' '` / `tr -d ' '` | charset translation, squeeze, delete | whole classes only; no fields |

## Transform & Program

| Command | Syntax | Use it when | Watch out |
|---|---|---|---|
| `sed 's/a/b/'` | `sed 's/ AT /@/' f` | text substitution per line | first match/line — add `g` for all |
| `sed -n '2,5p'` | `sed -n '2,8p' f` | extract line ranges | `-n` + `p` pairs only |
| `sed -i` | `sed -i.bak 's/x/y/' f` | **in-place rewrite** | rehearse without `-i` first; `-i.bak` for backups |
| `awk '{print $2}'` | `awk '{print $2}'` | fields, conditions, math | `$1`-based; `$NF` last; `$0` whole |
| `awk -F,` | `awk -F',' '$6>3.5 {print $2}'` | conditional columns | default FS is whitespace — set `-F` for CSV |
| awk arrays | `{c[$3]++} END {for (k in c) print c[k], k}` | group-by counts/sums | no sort — pipe to `sort -rn` |
| awk aggregates | `{s+=$5; n++} END {print s/n}` | means/sums/min-max | `NR>1` to skip headers |
| `xargs` | `... \| xargs -r -d '\n' wc -l` | streams → arguments | `-r` on empty input; `-I{}` per-line |
| `$( )` | `echo "$(grep -c E f) errors"` | embed output in commands | always over backticks; nests cleanly |

## The Three Idioms (tattoo-worthy)

```console
# 1. The census
cut -d, -f3 f.csv | sort | uniq -c | sort -rn | head -N

# 2. Header/body split
head -1 f.csv          # schema
tail -n +2 f.csv       # body only

# 3. Group-by sum
awk -F, 'NR>1 {s[$3]+=$5} END {for (k in s) print k, s[k]}' f.csv | sort -k2 -rn
```

## The Canonical Pipeline

```text
file → grep → cut → sort → uniq → awk → output
(narrow) (columns) (group) (aggregate) (compute) (capture)
```
