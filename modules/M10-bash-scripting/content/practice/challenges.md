# Module 10 Challenges — Bash Scripting

> Eight challenges, all under `~/lab10/`, all shellcheck-clean by the
> course bar. Each delivers a *tool*, not an exercise answer — write
> them as rung-5 reusable scripts (Lesson 5 §4): header, strict mode,
> usage, log/fail, main.

## C1 — The extensible converter

`convert_csv.sh IN OUT`: validates both arguments (exit 64 on wrong
count, 66 on missing input, 2 on existing output — *refuse to
overwrite*), converts `,` to tab (M08 tools), logs each step to
stderr, exits 0 with the row count printed to stdout. Stretch: accept
either argument order by inspecting extensions.

## C2 — The dedupe reporter

`dupes.sh FILE COLUMN`: reports how many duplicate values appear in
the given CSV column number (cut/sort/uniq from M08), printing the
top five with counts. Guard: COLUMN must be a positive integer —
write the *test* for that (`[[ "$col" =~ ^[0-9]+$ ]]`), and exit 64
on failure. Edge: a file with a single data row (there can be no
duplicates — make the tool *say* that, not just print 0).

## C3 — The batch renamer with a safety net

`rename_ext.sh DIR OLD NEW`: renames `*.OLD` to `*.NEW` in DIR using
the `${f%.OLD}` idiom. Safety net: refuse if DIR lacks any OLD files
(exit 66, name the glob); refuse if any target already exists (exit
2, list the collisions *before* renaming anything — check all first,
act second). Dry-run thinking starts here; M11 formalizes it.

## C4 — The column profiler

`profile.sh FILE`: for a CSV, print one line per column: index, header
name, empty-cell count, distinct-value count. All M08 tools — the
function form (`profile_column()`) and a loop over `1..num_cols` make
it 25 lines. The interesting bug you'll meet: columns whose *data*
contains commas — document the tool's assumption (simple CSVs, no
quoting) in the header comment. Knowing what your tool *doesn't* do
is rung-5 documentation.

## C5 — The env-aware bootstrapper

`newproj.sh NAME`: creates `~/projects/NAME/` with subdirs
(`data/`, `src/`, `results/`), a `.gitignore` stub (M26 preview:
`results/`, `*.log`, `__pycache__/`), and a `README.md` containing
the project name and today's date. Refuse if the directory exists
(exit 2); print the tree at the end. This is the
"environment setup" automation — write it so running it twice is
harmless *by refusal*, and say so in the header.

## C6 — The log summarizer

`logsum.sh LOGFILE`: for an M08-style server log (timestamp level
message), print: total lines, count per level (INFO/WARN/ERROR —
case-insensitive), first and last timestamp, and the five most
frequent message *kinds* (strip numbers/timestamps with sed, then
sort|uniq -c|sort -nr). Guard: non-existent and empty files, and a
file with zero ERROR lines (the summary should still print — zeros
are data).

## C7 — The health mini-check

`quickcheck.sh`: three lines of verdicts — disk (`df -h` on $HOME ≥
80% → WARN), memory (`free -h`, available < 20% of total → WARN),
load (`uptime` vs `nproc` → WARN if 1-min load > cores). Exit 0 if
no warnings, 1 otherwise — and *test that contract* by faking a
warning (hint: the thresholds are just variables at the top; that's
why they're variables). This is Mini-Project E's `health.sh` in
embryo — M24 will grow it.

## C8 — The self-testing script

Take C1 and add `--selftest`: runs the tool against a temp CSV it
creates itself (mktemp is M11's, but `scratch/` under the script's
dir is fine for now), asserts the output line count and exit codes
for: good input, missing input, existing output — printing PASS/FAIL
per assertion and exiting non-zero if any failed. You've written a
test suite for your own tool; the header comment should explain the
contract ("given X, expect Y") — the roadmap's
tests-as-expectations idea, made executable.

## Stretch — C9, the pipeline consolidator

`runall.sh`: runs C1→C2→C6 in sequence on a dataset, stopping at the
first failure (`set -e` does this naturally — verify it), logging
each stage's exit code, and producing one summary line per stage to
stdout. The lesson to write up: what did `&&`-chaining *not* give you
that the script does? (Answer to discover: per-stage logging,
distinct codes, a single place to add stage 4.)
