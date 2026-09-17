# Lab 1 — Harden `dq.sh`: From Script to Tool

> Module 11 · Unit 3 · Difficulty: Intermediate
> Time: ~50 min · Environment: your own VM, `~/lab11/`
> Prerequisites: [Mini-Project A's](../../../M10-bash-scripting/content/mini-project-a-dataset-qc-toolkit.md)
> `dq.sh` (or [M10 Lab 2's](../../../M10-bash-scripting/content/labs/lab-02-build-dq-toolkit.md)),
> [Lessons 1–3](../README.md)
> ⚠️ Reads datasets, writes only `~/lab11/reports/`. The hardening
> adds *safety*, never new powers.

Your dq.sh works. Now it grows up: real options, a dry-run, a log
file, trap-based cleanup, and proof it dies gracefully. Five
upgrades, each tested before the next.

## Setup

```console
$ mkdir -p ~/lab11/{reports,tmp} && cd ~/lab11
$ cp ~/M10-path/dq.sh .            # your working script from M10
$ cp ~/datasets/sales_2026.csv .
$ shellcheck dq.sh && bash -n dq.sh   # confirm the starting point is clean
```

## Upgrade 1 — getopts interface (10 min)

Add per [Lesson 3 §4](../lessons/03-dry-run-idempotency-options.md):

- `-h` — usage, exit 0
- `-o OUTDIR` — report directory (default `./reports`, env-overridable
  `DQ_OUTDIR`)
- `-n` — dry-run (Upgrade 2)
- `-v` — verbose logging

Test the four option paths: `-h`, unknown option, `-o` missing its
argument, and a normal run. All the old argument guards still apply
*after* `shift $((OPTIND - 1))`.

## Upgrade 2 — the run() doorway and dry-run (10 min)

Every *modifying* command (writing the report, mkdir) goes through
`run()`; with `-n`, it narrates instead of acting. Non-modifying
commands (reading the CSV, validating) run normally in dry-run —
a preview that validates is a preview.

```console
$ ./dq.sh -n sales_2026.csv
[dry-run] mkdir -p ./reports
[dry-run] mv -- ./reports/dq_2026-09-15_2104.txt ./reports/dq_sales_2026.csv.txt
2 actions planned
$ ls reports/        # empty — proof
```

## Upgrade 3 — timestamped log + trap cleanup (15 min)

Per [Lesson 2](../lessons/02-signals-temp-cleanup.md): a `mktemp`
scratch file for building the report, cleaned by `trap cleanup EXIT`;
on success, an atomic `mv` of the finished report into place. Add a
timestamped run-log line per step (M24's contract previewed:
ISO-8601, level, one event per line) to `logs/dq.log` via an
append-only `log()` — and *append the exit code on exit* in the
cleanup handler.

```bash
cleanup() {
    rc=$?
    [[ -n "${tmp:-}" && -f "$tmp" ]] && rm -f "$tmp"
    printf '%s INFO  run ended rc=%d\n' "$(date -Iseconds)" "$rc" >> "$LOGFILE"
    exit "$rc"
}
trap cleanup EXIT
```

## Upgrade 4 — the interrupt drill (10 min)

The lab's centerpiece — prove graceful death *both* ways:

1. **Interrupt:** add a temporary `sleep 5` before the promote, run
   in the foreground, Ctrl+C during it. Verify: no report written, no
   temp debris (`ls` scratch), and `logs/dq.log` ends with
   `rc=130` (128+SIGINT — the shell's honest confession).
2. **Error:** run against a corrupt CSV (empty file). Verify: old
   reports untouched, rc=66 (or your code), logged.

Record both traces. A cleanup you haven't killed is a cleanup you
haven't tested.

## Upgrade 5 — idempotent re-run (5 min)

Run the real (non-dry) pass twice. Second run must succeed with
`run()` narrating the overwrite-guard — the atomic `mv` replaces, or
the exists-guard skips, *by design, not by luck*. Show both runs'
logs.

## The bar

| Requirement | Proof in transcript |
|---|---|
| getopts: 4 paths tested | outputs + exit codes |
| dry-run: plan narrated, nothing done | `[dry-run]` lines + empty reports/ |
| trap: interrupt + error paths | rc=130 and rc=66 lines in dq.log, no debris |
| atomic promote | temp name ≠ final name; mv in trace |
| idempotent double-run | two clean rc=0 logs |
| `bash -n` + `shellcheck` | last clean outputs |

## Done when

- [ ] All upgrades tested in order, transcripts in `lab-log.md`
- [ ] The interrupt drill demonstrated (rc=130 in the log)
- [ ] shellcheck zero findings on the hardened script
- [ ] One paragraph: which upgrade changed *how safe* the script is,
      and which merely changed *how convenient* it is
