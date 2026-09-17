# Module 11 Labs — Advanced Shell & Automation

> Two labs under `~/lab11/`. Lab 1 upgrades M10's toolkit; Lab 2 is
> the **final scripting challenge** for Unit 3. Every modifying
> script must demonstrate: dry-run, idempotent re-run, trap cleanup
> on Ctrl+C, and shellcheck silence.

| # | Lab | Focus | Time |
|---|-----|-------|------|
| 1 | [lab-01-harden-dq-toolkit.md](lab-01-harden-dq-toolkit.md) | Harden M10's `dq.sh`: options, dry-run, trap cleanup, timestamped logs, interrupt test | ~50 min |
| 2 | [lab-02-final-scripting-challenge.md](lab-02-final-scripting-challenge.md) | **Final challenge**: `organize.sh` — a guarded, idempotent, self-testing dataset organizer | ~60 min |

Standing rules (recap):

- Every modifying command passes through the `run()` doorway.
- Temp files: `mktemp`, cleaned by `trap ... EXIT`, same filesystem
  as their target.
- Interruption drills are part of the deliverable, not an option.
- Transcripts in `lab-log.md`: dry-run plans, double-run proofs,
  interrupt traces, shellcheck's last clean output.
