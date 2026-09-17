# Module 26 Labs — Git and Development Workflows

> Unit 7 · Difficulty: Intermediate
> Three labs. All run **inside your own VM**; the "remote" is a local bare
> repository, so nothing here touches external hosting or real credentials.

| # | Lab | Focus | Est. time |
|---|-----|-------|-----------|
| 1 | [lab-01-version-your-work.md](lab-01-version-your-work.md) | init → commit → branch → merge on a real project; build a genuine history | ~45 min |
| 2 | [lab-02-break-repair-clinic.md](lab-02-break-repair-clinic.md) | Remotes (push/pull), then five deliberate failures with recovery | ~60 min |
| 3 | [lab-03-end-to-end-ds-workflow.md](lab-03-end-to-end-ds-workflow.md) | **Capstone walk:** SSH → Git → venv → data → Jupyter → analysis → output → Git | ~75 min |

General rules for all three:

- Every command typed, not pasted — muscle memory is the deliverable.
- `git status` before and after anything that surprises you.
- Destructive recoveries (`reset --hard`, `restore`) happen only inside
  these practice repos; that's what makes them safe to practice.
- Evidence in `lab-log.md`: command + key output lines, per the course
  convention ([M24](../../../M24-logs-journald-monitoring/README.md) onward).

Prerequisites: [Lesson 1](../lessons/01-git-model-core-loop.md) for Lab 1;
Lesson 3 for Lab 2; all three lessons + [M27](../../../M27-python-jupyter-data/README.md)
for Lab 3.
