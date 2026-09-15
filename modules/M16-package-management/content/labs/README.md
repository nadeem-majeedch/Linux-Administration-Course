# Module 16 Labs — Package Management

> Three labs. Lab 1 is entirely read-only (zero changes to your system).
> Labs 2–3 make small, previewed, reversible changes on your own
> VM/WSL2. No destructive operations anywhere; removals target only
> packages the lab itself installed.

| # | Lab | Focus | Time |
|---|-----|-------|------|
| 1 | [lab-01-package-explorer.md](lab-01-package-explorer.md) | Read-only: dpkg queries, apt search/show/policy, dependency reading | ~30 min |
| 2 | [lab-02-safe-lifecycle.md](lab-02-safe-lifecycle.md) | Full install→verify→remove cycle, done the safe way | ~40 min |
| 3 | [lab-03-repo-audit.md](lab-03-repo-audit.md) | Audit sources, PPA test-drive in a VM, dry-run security upgrades | ~40 min |

Standing safety rules (recap):

- `apt show` before every install; read the NEW/REMOVED summary line.
- Install/removal experiments use small, well-known packages only.
- PPA tests live in a disposable VM; nothing on shared machines.
- Record evidence in `lab-log.md`.
