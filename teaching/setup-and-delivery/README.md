# Setup & Delivery — Instructor Guides

> Environment preparation and per-term delivery logistics for anyone
> teaching this course. Student-facing setup lives in the repo root:
> [`SETUP.md`](../../SETUP.md) — the guides here build on it, they
> don't replace it.

| Guide | Use it |
|---|---|
| [instructor-environment-setup.md](instructor-environment-setup.md) | One-time: instructor machine, staging VMs, the docs venv, demo accounts |
| [student-environment-setup.md](student-environment-setup.md) | Per-term: what to verify in Week 1's setup session; the standard lab image |
| [lab-infrastructure.md](lab-infrastructure.md) | Room setup, snapshot strategy, shared-dataset staging, exam station prep |
| [delivery-checklist.md](delivery-checklist.md) | The week-by-week operational checklist: before/during/after each session |
| [fresh-environment-verification-checklist.md](fresh-environment-verification-checklist.md) | One consolidated pre-term pass: every environment check the course assumes, with pass/fail fields (not executed by its authors — it is the instrument for *your* fresh-VM day) |

## The one rule that shapes all four guides

Everything in this course is designed to run **inside a student-owned
sandbox** (VM / WSL2 / containers). Nothing in the lab path requires a
real shared server, root on a host, or paid cloud. The infrastructure
guides exist to make that sandbox *boring to set up and trivial to
reset* — because a course that teaches break-and-repair needs
snapshots, not courage.
