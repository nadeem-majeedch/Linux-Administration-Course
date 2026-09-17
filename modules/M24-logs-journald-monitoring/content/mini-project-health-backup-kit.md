# Mini-Project E — Server Health & Backup Kit

> Module 24 · Unit 6 · Difficulty: Advanced
> Deliverables: `health.sh` · `backup.sh` (with restore mode) · one
> incident report
> Prerequisites: all four M24 labs; M18 (signals), M20 (user units),
> M23 (rsync), M08 (text pipelines)
> ⚠️ Safety envelope: everything operates on user data and user-scope
> units only; `backup.sh`'s restore mode writes **only** to a target
> directory it is explicitly given, and refuses to run otherwise.

You are the administrator of your own DS workstation now. Build the
kit you'll wish you had the first time a training job dies at 3 AM:
one command that tells you the machine's story, one command that
makes your data survivable, and one postmortem proving you can
diagnose from evidence.

## Deliverable 1 — `health.sh`

**Usage:** `./health.sh` prints a one-page report; `./health.sh
--watch` reprints every 30 s (via `watch`, no loops).

Required sections, in order — the 60-second check from
[Lesson 3 §8](lessons/03-monitoring-toolkit.md), now scripted:

1. **Header** — hostname, date (ISO-8601), uptime, load vs `nproc`
   with a plain-language verdict (`OK` / `BUSY` / `SATURATED`).
2. **Memory** — `free -h` one-liner + verdict on *available* (not
   free) and swap use.
3. **Disk** — `df -h` for `$HOME`'s filesystem + `/tmp`; flag any
   filesystem ≥ 80% (`OK`/`WATCH`/`FULL`).
4. **Errors since boot** — `journalctl -b -p err.. --no-pager |
   tail -5`, count total.
5. **My services** — for each unit in a list you define (default:
   the M24 lab units, e.g. `sync.service train.service`):
   `systemctl --user is-active` line.
6. **My journal (1h)** — `journalctl --user --since "-1 hour" -p
   warning.. --no-pager | tail -10`.

Requirements: bash strict mode (`set -euo pipefail`), functions per
section, exit code `0` if no section verdicts worse than `WATCH`,
`1` otherwise — so the script is *composable* (cron-able, chained).
Comment the verdict *thresholds* at the top; they're policy, and
policy wants documentation.

## Deliverable 2 — `backup.sh`

**Usage:**

```console
$ ./backup.sh archive                    # tar.gz + sha256, into $BACKUP_DIR
$ ./backup.sh mirror <dest-dir>          # rsync -av --delete
$ ./backup.sh restore <archive> <dest>   # tar -xzf into an EXPLICIT dest
```

Required behavior:

- `archive`: timestamped filename (`precious-2026-09-15T2114.tar.gz`
  style), followed immediately by `sha256sum` written beside it, and
  a `tar -tzf` listing count printed ("41 files archived"). Source
  dir configurable at the top (`SRC="${SRC:-$HOME/lab24/precious}"`).
- `mirror`: refuse to run if `<dest-dir>` is missing or empty-ish
  unsafe — specifically, **abort** if the destination does not exist
  (no `mkdir` surprises) and print what `--delete` will do first
  (`rsync -avn` — the dry run — narrated before the real one).
- `restore`: **refuse** if `<dest>` exists and is non-empty; refuse
  if it equals `/` or `$HOME`; require it be given explicitly. After
  extracting: print file count + a `diff -r` suggestion line.
- Every mode logs one ISO-8601, key=value line per action (the
  Lesson 2 §6 contract) to stderr: `2026-09-15T21:14:02+00:00 INFO
  mode=archive files=41 sha=abcd1234…`
- `set -euo pipefail`; no interactive prompts; no absolute path
  assumptions beyond the configurable source.

## Deliverable 3 — the incident report

Pick **one** incident from [Lab 1](labs/lab-01-log-forensics.md) (or
a real one from your own machine this week) and write the five-line
postmortem — then a **sixth line: the kit's role**. Which command of
your kit would have *detected* it earlier, or prevented it outright?
(E.g., OOM death → health.sh memory section verdict; moved script →
health.sh "my services" section going red.)

One page maximum. Evidence quotes over narration.

## Grading (suggested rubric, 20 pts)

| Item | Pts |
|---|---|
| `health.sh` sections complete, verdicts correct, exit-code contract | 6 |
| `backup.sh` archive + mirror correct; dry-run and refusal guards implemented | 6 |
| `restore` mode verified in lab-log: extract → diff -r → "IDENTICAL" | 4 |
| Incident report: evidence-quoted, six lines, kit linkage | 4 |

## Submission

Repo-style layout in `~/lab24/kit/`:

```text
kit/
├── health.sh
├── backup.sh
├── kit.conf              # SRC, BACKUP_DIR, SERVICES list
├── incident-report.md
└── lab-log.md            # transcripts: health run, archive, mirror,
                          # dry-run, refusal cases, full test-restore
```

Transcripts must include at least one *working* restore and one
*refused* bad invocation for each guard (nonexistent dest; restore
into non-empty dir; restore into `$HOME`) — the guards are graded by
watching them fire.
