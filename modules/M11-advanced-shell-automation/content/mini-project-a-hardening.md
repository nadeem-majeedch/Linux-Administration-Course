# Mini-Project A — Hardening (M11 Re-submission)

> Module 11 · Unit 3 · Difficulty: Intermediate
> Deliverable: your M10 toolkit, hardened and re-submitted
> Prerequisites: [M11 lessons](README.md) + [Lab 1](labs/lab-01-harden-dq-toolkit.md)
> ⚠️ Same safety envelope as the original; hardening adds *proof*, not
> powers.

M10's toolkit worked; now it must survive colleagues, cron, and
Ctrl+C. Re-submit all three tools with the M11 property set, graded
by *demonstrated proofs* rather than by reading code.

## Required upgrades (per tool)

For **`dq.sh`** and **`summary.sh`** (and `clean.sh` if submitted):

1. **getopts interface** — `-h`, plus at least one meaningful option
   (e.g. `-t THRESHOLD`, `-o OUTDIR`), env-overridable defaults.
2. **`run()` doorway + `--dry-run`** — every modifying command
   through one function; dry-run narrates the *full plan* including
   which files *would* be touched.
3. **mktemp + trap** — scratch space cleaned on every exit path;
   results promoted atomically (temp beside target, then `mv`).
4. **Idempotent re-run** — second run is a clean no-op-or-refresh,
   proven by a double-run transcript.
5. **Timestamped run-log** — `logs/<tool>.log`, one ISO-8601 line
   per event, exit code recorded on exit (M24 will read these).
6. **Interrupt proof** — one Ctrl+C mid-run per tool: no debris, no
   partial outputs, rc=130 logged.
7. **Quality gate** — `bash -n` + `shellcheck` silent on all tools.

`clean.sh` (if present) additionally requires the dry-run to be
*unambiguous about what would be stripped/removed* — its whole value
is the preview.

## Re-submission layout

```text
~/lab11/project-a-hardened/
├── dq.sh  summary.sh  [clean.sh]  [lib.sh]
├── README.md           ← updated: new options, exit codes, config vars
└── transcript.md       ← per tool: dry-run plan, double-run, interrupt,
                          option error paths, shellcheck silence
```

## Grading (20 pts)

| Item | Pts |
|---|---|
| Property set complete on all tools (1–5) | 8 |
| Interrupt proof per tool (6) | 4 |
| Option/error paths demonstrated (64s and 66s) | 3 |
| README updated honestly (limitations included) | 2 |
| `bash -n` + `shellcheck` silent | 3 |

## Where the scripting thread ends

Unit 3 closes here. The hardened toolkit is the reference artifact
for every scripting moment ahead: cron scheduling (M19) will fire
`summary.sh` unattended — its idempotency and logging are why that's
safe; M24's `health.sh`/`backup.sh` inherit the skeleton; the
capstone's deployment scripts meet the same bar. From Unit 4
(permissions) onward, when a script appears, it arrives pre-hardened.
