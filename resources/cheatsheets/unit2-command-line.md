# Cheatsheet — Unit 2: Command Line

## Navigation & paths

```bash
pwd                      # where am I
cd /etc/apt              # absolute path (starts at /)
cd ../..                 # relative (.. = parent)
cd ~  cd -               # home / previous directory
ls -lah                  # long, all (incl. hidden), human sizes
realpath FILE            # resolve a path fully
```

FHS map: `/etc` config · `/home` users · `/var` variable data+logs · `/tmp` scratch ·
`/usr` programs · `/opt` extra software · `/proc` kernel view · `/dev` devices.

## File operations

```bash
mkdir -p a/b/c           # nested create
cp -r src dst            # copy recursively
mv old new               # move / rename
rm -i FILE               # delete WITH confirmation (habit)
ls *.csv data/??.tsv     # globs: * any, ? one, [abc] set
cat f | less             # read with pager (also: less f)
head -5 f / tail -n 20 f # ends of files; tail -f grows
wc -l f                  # count lines
file f; stat f           # type; detailed metadata
df -h; du -sh DIR        # free space; directory size
```

**`rm` is forever.** No trash can in the shell. `ls` the glob first, quote paths, prefer `-i`.

## Text tools (M08)

```bash
grep -i 'err' f          # search, ignore case     -v invert -n numbers -c count
grep -r 'TODO' DIR/      # recursive; -E extended regex; -w whole word
sed 's/old/new/g' f      # substitute (preview); -i.bak edits with backup
sort -t, -k3 -nr f       # sort by comma-field 3, numeric, reverse; -u unique
cut -d, -f1,4 f          # fields 1 and 4, comma-delimited
tr -s ' ' < f            # squeeze repeated spaces; tr -d '\r' kill CRs
sort f | uniq -c | sort -rn    # THE frequency-table idiom
comm -12 a b             # common lines (sorted inputs); diff a b
```

Regex essentials (ERE): `^ $` anchors · `.` any char · `[0-9]+` digits · `a|b` either.

## Pipes, redirection, awk, find (M09)

```bash
cmd < in > out 2> err    # stdin from file, stdout, stderr
cmd >> log 2>&1          # append, merge errors into output
cmd | tee log | next     # see AND save
awk -F, '{s+=$3} END {print s}' data.csv      # sum column 3 (comma fields)
awk -F, '$3 > 100 {print $1, $3}' data.csv    # filter + project
find DIR -name '*.log' -mtime -7 -size +1M    # name, age, size
find DIR -name '*.tmp' -delete                 # careful: preview first!
find DIR -name '*.csv' | xargs -n1 wc -l       # act on found files
```

Big files: stream them (`grep | awk | sort`) — never open a 5 GB file in an editor.
