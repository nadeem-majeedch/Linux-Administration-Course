# Lesson 2 — Signals, Temp Files and Graceful Death

> Module 11 · Unit 3 · Difficulty: Intermediate
> Reading time: ~25 min · Lab: [Lab 1 — harden dq.sh](../labs/lab-01-harden-dq-toolkit.md)
> Up next: [Lesson 3 — dry-run, idempotency & options](03-dry-run-idempotency-options.md)

---

## 1. The script that dies badly — and why it matters

A data-cleaning script crashes halfway (Ctrl+C, a full disk, an
error): it leaves a half-written output file that *looks* valid, and
a temp directory nobody will ever remove. Next run: "output already
exists?" confusion; next month: `~/tmp` full of `out.csv.tmp2`,
`out.csv.tmp3`. Automation scripts must assume they **will be
interrupted** — and arrange their affairs accordingly. Three tools
make death graceful: **trap** (run cleanup on the way out),
**mktemp** (temp files that don't collide), and the **write-temp-
then-rename** pattern (output is either fully old or fully new).

## 2. Signals in one paragraph (M18 goes deep)

When you press Ctrl+C, the kernel delivers **SIGINT** to the running
process; `kill PID` sends **SIGTERM** ("please finish"); a script
can *catch* these and run a handler before exiting. Bash exposes
this via `trap 'commands' SIGNAL`. The course uses three now —
`EXIT` (runs on *every* exit path: success, error, interrupt),
`INT`, `TERM` — and defers the full grammar (HUP, process groups,
the kill ladder) to
[M18](../../../M18-processes-jobs-signals/content/README.md).

## 3. trap — the cleanup contract

```bash
#!/usr/bin/env bash
set -euo pipefail

tmpdir=$(mktemp -d)
cleanup() {
    [[ -d "$tmpdir" ]] && rm -rf "$tmpdir"
    echo "cleaned up." >&2
}
trap cleanup EXIT                      # runs on ANY exit — success or not

echo "working with $tmpdir" >&2
echo "data" > "$tmpdir/work.txt"
# ... process; on success we promote results out of tmpdir ...
cp "$tmpdir/work.txt" result.txt
```

Run it, kill it with Ctrl+C mid-sleep, make it fail — `cleanup` runs
*every time*. That is the contract: **whatever happens, no debris.**

Details that keep the contract honest:

- Define `tmpdir` *before* the trap — the handler references it.
- Guard inside the handler (`[[ -d ]] &&`): cleanup must be
  re-runnable (it can fire twice — e.g. an INT handler that also
  lets EXIT fire).
- Want to *know* why you exited? Stash the status first:

```bash
cleanup() {
    rc=$?
    rm -rf "$tmpdir"
    (( rc != 0 )) && echo "exited early (rc=$rc); no results written" >&2
    exit "$rc"
}
trap cleanup EXIT
```

- `trap '' INT` *ignores* Ctrl+C (lockfiles' cousin); `trap - INT`
  resets to default. Rarely needed — knowing they exist is enough.

## 4. mktemp — temp files that can't collide

`out.tmp.$RANDOM` works until two runs land in the same millisecond
or an attacker predicts the name on a shared machine. `mktemp`
creates a **freshly-created, name-collision-free** path:

```bash
tmpfile=$(mktemp)                     # /tmp/tmp.XXXXXXXXXX
tmpdir=$(mktemp -d)                   # a whole directory
work=$(mktemp --tmpdir="$HOME/lab11" out.XXXXXX)   # name hint + location
```

Rules that make it safe: the file **already exists** when you get
its name (no create-race), the name is unpredictable (shared-machine
safe), and — with the trap above — it *always* gets removed. On
servers, prefer `--tmpdir` to keep bulk work off a full `/tmp`
(M24's disk-full incident).

## 5. Write-temp-then-rename — the atomic-ish write

The half-written output file is the worst debris: it *looks* like a
result. The fix relies on one filesystem fact —
**`mv` within the same filesystem replaces the destination
instantly**, either-fully-or-not:

```bash
#!/usr/bin/env bash
# safe-update.sh — refresh summary.txt without ever leaving a half file
set -euo pipefail

target="$HOME/lab11/summary.txt"
tmp=$(mktemp --tmpdir="$(dirname "$target")")     # SAME filesystem — required!

generate_summary > "$tmp"                          # any failure aborts before mv
mv -f "$tmp" "$target"                             # instant swap: old or new, never mixed
echo "updated $target" >&2
```

The **same-filesystem requirement** is the whole trick (M17's
groundwork): `/tmp` and `$HOME` may be different filesystems, where
`mv` silently degrades to copy+delete — the exact gap we're closing.
Hence `mktemp --tmpdir="$(dirname "$target")"`: temp lives beside
the target. Two footnotes: `generate_summary > "$tmp"` under
`set -e`-with-pipefail aborts *before* any mv — failures can't reach
the rename; and "atomic-ish" is honest — a power cut can still cost
the file, but *no reader ever sees a mixture*.

## 6. Interrupt drills — trust but verify

The pattern isn't real until you've killed it:

```console
$ bash -x safe-update.sh &        # start it
$ kill -INT %1                    # or Ctrl+C in its own terminal
$ ls -la ~/lab11/                 # summary.txt unchanged; NO tmp debris
$ ls /tmp | grep tmp. | wc -l     # your mktemp leftovers: 0
```

And the failure-direction test: point `generate_summary` at a
missing input, run, confirm — old `summary.txt` intact, rc non-zero,
no debris. **Both directions is the bar** (Lab 1 grades exactly
this: interrupt and error).

## 7. Putting it together — the interruptible pattern

```bash
#!/usr/bin/env bash
# harden-demo.sh — the full shape: strict, temp, trap, atomic promote
set -euo pipefail

readonly OUT="${1:?usage: harden-demo.sh OUTFILE}"
tmp=$(mktemp --tmpdir="$(dirname "$0")")

cleanup() {
    rm -rf "$tmp"
    echo "[clean] temp removed" >&2
}
trap cleanup EXIT

for i in 1 2 3; do
    printf 'row %d\n' "$i" >> "$tmp"
    sleep 2                       # the window to Ctrl+C
done

mv -f "$tmp" "$OUT"               # promote only on full success
echo "[ok] wrote $OUT" >&2
```

This is the skeleton Lab 1 grafts onto `dq.sh`, and the same shape
M19's scheduled scripts and M28's containerized ones will wear.

## 8. Try it now (15 minutes)

1. Build `harden-demo.sh`; run to completion. Then run again and
   Ctrl+C during the sleep: verify no debris, no output file. That's
   the *graceful death* demo — record both runs.
2. Break the same-filesystem rule: point `--tmpdir` at `/tmp` while
   OUT is on your home filesystem. Does anything break today? (No —
   but explain in one sentence why the rule exists anyway: the
   guarantee, not the test, is the point.)
3. Stash-the-status variant (§3): make the script fail, and confirm
   the handler prints `rc=...` and the exit code survives to the
   caller (`echo $?`).
4. mktemp naming: `ls` five `mktemp` results — see the random part;
   that's the collision-freedom.

## 9. Common mistakes

- `trap cleanup EXIT` defined before `tmpdir` exists — the handler
  fires and references emptiness (with `set -u`: a loud crash *inside
  your cleanup*, which is somehow worse).
- Cleanup without the re-run guard — a trap that fires twice and
  rm-rf's a path that has, by then, become something else.
- mktemp's name used without its result: `mktemp` then writing to
  `out.tmp` — you created a file to ignore it.
- Cross-filesystem mv — the atomicity silently evaporates. Temp
  beside the target, always.
- Testing only the success path. The drills in §6 *are* the lab;
  untested cleanup is unproven cleanup.

> **Up next:** [Lesson 3 — dry-run, idempotency &
> options](03-dry-run-idempotency-options.md): the patterns that make
> scripts *safe to hand to other people and to cron*.
