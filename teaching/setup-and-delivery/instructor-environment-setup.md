# Instructor Environment Setup — One-Time

> Everything an instructor needs *on their own machine* to teach,
> demonstrate, stage exams, and build the course website. Estimated
> setup: half a day once, minutes per term after.

## 1. Your teaching machine

- **Host OS:** any of Windows 10/11, macOS, Linux. VirtualBox (free)
  or Hyper-V/VMware for VMs; WSL2 if you demonstrate on Windows.
- **One "instructor" VM:** Ubuntu LTS (same version the course
  specifies — see `SETUP.md` Path A for the exact spec: 2 CPUs,
  4 GiB RAM, 25 GiB disk). This is your *demo* machine; keep a
  **pristine snapshot** labelled `CLEAN` before anything else.
- **Terminal with copy-paste:** VirtualBox Guest Additions (or
  `open-vm-tools`) installed — half your live demos depend on pasting
  command blocks cleanly.

## 2. Demo accounts (for the M10–M13 unit)

The identity/permissions demos need *second users*. Create them once
inside the instructor VM — never on your host:

```bash
# Inside the instructor VM only:
sudo adduser demo1 --gecos "" --disabled-password
sudo adduser demo2 --gecos "" --disabled-password
sudo usermod -aG sudo demo1   # only if a demo needs a second sudoer
```

Snapshot after this point: label `CLEAN+USERS`. All permission demos
now run as `demo1`/`demo2` via `su - demo1` — no host risk, one
snapshot-restore to reset.

## 3. Exam staging VM

- A **second** VM, server-flavored Ubuntu (no desktop) — this is the
  snapshot base for the [practical exam](../../assessments/practical/practical-key.md)
  and LA sessions.
- Follow `assessments/practical/practical-key.md` **Part 0 staging
  script** on this VM, then snapshot as `EXAM-FAULTS-IN`.
- Verify staging once per term: run the exam yourself against a fresh
  clone; every fault must be present and solvable in 90 minutes.

## 4. Course website build (docs venv)

The MkDocs build is Python-isolated so it never touches system
packages:

```bash
python3 -m venv .docs-venv
.docs-venv/bin/pip install -r requirements-docs.txt   # pinned versions
.docs-venv/bin/python -m mkdocs build --strict         # the CI gate
.docs-venv/bin/python -m mkdocs serve                  # live preview :8000
```

The same pipeline runs in CI (`.github/workflows/publish.yml`); if the
strict build passes locally, it passes in Actions.

## 5. Per-term refresh (minutes)

1. [ ] `git pull` the course repo
2. [ ] `.docs-venv/bin/pip install -r requirements-docs.txt` (pinned
      versions drift rarely; check the changelog if pins move)
3. [ ] Strict build green locally
4. [ ] Restore `CLEAN+USERS` snapshot on the demo VM; recreate the
      week's demo artifacts (scripts/`git init`/datasets) during the
      first demo, *on screen* — the setup is part of the pedagogy
5. [ ] Exam VM: verify `EXAM-FAULTS-IN` snapshot still boots and the
      six faults are present (10 min)

## 6. Safety posture for instructors

The demos in [`demonstrations/`](../demonstrations/demo-index.md) are
chosen so that **nothing touches your host OS**; the most destructive
command anywhere is a guarded `rm` inside a created scratch dir in the
VM. Keep it that way: if you improvise a demo, run it in the VM, and
snapshot before improvising. The [`safety card`](../../resources/cheatsheets/safety-card.md)
students follow is the same card you teach by.
