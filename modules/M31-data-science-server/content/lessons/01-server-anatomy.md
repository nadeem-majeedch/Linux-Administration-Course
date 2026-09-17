# Lesson 1 — Anatomy of a Data Science Server

> M31 · Unit 8 companion · Difficulty: Advanced
> Reading time: ~30 min · Up next: [Running work](02-running-work.md)

---

## 1. Workstation vs shared server: the frame changes, the OS doesn't

Your M04 VM was a workstation: one user, root-adjacent, restartable at
will. The data-science server is the opposite contract: **one machine,
many researchers, long-running jobs, no restarts** — a GPU box the
whole lab shares, a department compute node, a rented VM the team
won't recreate for your experiment. Three consequences organize this
module:

1. **You are a guest, not the owner** — user-space everything (M27's
   no-sudo discipline), quotas and etiquette replace control.
2. **The box outlives your login** — jobs must survive disconnects
   (tmux/nohup, lesson 2), data must survive the project (layout and
   backups, lesson 3).
3. **Everything you do is visible** — `top` shows your pandas to your
   colleagues; the etiquette rules (lesson 2 §5) are what keep you
   invited back.

The consolation: the OS is the same Ubuntu you've administered for 28
modules. The server frame changes *behavior*, not *tooling*.

## 2. The directory contract of a DS server

Shared servers live or die by layout discipline. The near-universal
convention (this course's M06 hierarchy + M13 permissions, grown up):

```text
/              the system (never yours)
├── home/      one directory per researcher — CODE, notebooks, configs
│   ├── you/
│   └── colleague/
├── data/      SHARED datasets — group-owned, read-only for users
│   ├── public/          (read-only mounts, department-licensed sets)
│   └── projects/<proj>/ (project-shared: SGID + group write, M13)
├── scratch/   fast, EPHEMERAL — big intermediates, auto-purged
└── opt/       group-installed shared software (admins manage)
```

The contract's rules, each traceable to a module:

- **Code in `$HOME`, data in `/data`, junk in `/scratch`** — because
  `$HOME` is backed up and quota'd, `/data` is shared-but-protected,
  and `/scratch` is the sacrifice layer (fast disk, no backup, purge
  policy). Putting a 200 GB intermediate in `$HOME` is the classic
  first-week sin: it fills the backup volume (card 2 of the
  M32-clinic) and isn't even the right disk for the job.
- **Permissions encode the workflow** — `/data` read-only via mode
  bits (M27's guard), project directories group-shared with SGID
  (M13's `2770`), `$HOME` yours alone. On a shared box, permissions
  *are* the collaboration policy.
- **Quotas are real** — `quota -s` or the admin's `df` conversation;
  know your limits before the batch job discovers them.

## 3. Environments on a shared server: venv, pip, conda

Everything M27 taught holds — and the shared server adds constraints
and one more tool.

**venv + pip remains the course default** (project-local, disposable,
pin-driven — M27's whole contract), with the shared-server additions:
*never* install into system Python (PEP 668's guard, M27 Q6), and
never pollute `~/.local` broadly (your `pip install --user` becomes
everyone's version conflict question — keep it project-local).

**conda, conceptually** — the DS world's other environment manager,
and you must *read* it even if you default to venv:

| | venv + pip | conda / mamba |
|---|---|---|
| Scopes | Python packages only | Python itself **+ native libs (CUDA, MKL, GDAL)** |
| Manifest | `requirements.txt` (pins) | `environment.yml` (channels + pins) |
| Speed | pip (PyPI wheels) | conda/mamba solver (mamba = fast) |
| Where | everywhere Python is | needs conda/mambaforge installed (no sudo? user-space miniconda works) |
| Course take | **default** — simple, standard, disposable | recognize, read, translate |

The translation is the skill: given `environment.yml`, you can name
its venv equivalent (`name:` → project dir; `dependencies:` pip
section → `requirements.txt`); given a conda-only dependency (a CUDA
runtime), you know why the team uses conda. **micromamba** is the
no-sudo, user-space variant that makes conda viable on servers you
don't own — the M27 "no sudo anywhere" lesson, conda edition.

**The reproducibility law that outranks tool choice** (M27 Q3): the
environment is defined by a *file in the repo* — pins exact, resolver
tamed — and a *fresh environment from that file* is proven to work
(the build-freeze-recreate drill, now on the shared server where it
matters most).

## 4. GPU servers and CUDA — the administrative level

Data-science servers are usually bought *for* the GPU, so you must be
literate in the admin layer even if your own work is CPU-only:

**The stack, top-down** (each layer must match the one below):

```text
  your framework (PyTorch / TensorFlow)
      ▲ needs
  CUDA toolkit (nvcc, runtime)      — versioned (11.8, 12.1, …)
      ▲ needs driver ABI
  NVIDIA driver (nvidia-smi)        — kernel module, host-level
      ▲ manages
  GPU hardware (A100 / RTX / …)
```

The admin-level facts that matter to a *user*:

- **`nvidia-smi` is the `top` of the GPU** — one command, the whole
  picture: driver/CUDA versions (top right), per-GPU utilization and
  memory, and the process list *with PIDs*. On a shared GPU box, this
  is both your monitoring and your etiquette instrument (lesson 2 §5).
- **Driver vs toolkit** — the *driver* is host-level (admins install;
  you can't and shouldn't), the *toolkit/runtime* comes per-environment
  (conda/pip wheels bundle theirs). Mismatch = the classic
  `CUDA version insufficient for driver` failure; the fix is
  environment-side, not driver-side.
- **GPU memory is the scarce resource** — `nvidia-smi`'s MiB column is
  the number colleagues fight over; a job that OOMs the GPU takes down
  neighbors' allocations (the framework's caching allocator holds
  memory *after* your job ends unless the process exits).
- **Containers are how CUDA is distributed** — M28's world: the
  NVIDIA Container Toolkit passes the host driver into the container;
  the container pins the toolkit. The course's Docker lessons are
  precisely the mechanism modern GPU environments ship in.

**CPU-only alternatives (this course's standing rule):** every GPU
concept has a CPU twin — `sklearn`/small `torch` (CPU build) for
workloads, `nvidia-smi` → `htop`+`free` for monitoring, GPU memory
etiquette → RAM etiquette. The lab runs entirely CPU-only; the
concepts transfer up when you meet the real box.

## 5. The etiquette layer (the unwritten made written)

Shared-server survival is a short list, each line already justified by
a module: check `nvidia-smi`/`htop` before launching big; nice the
batch (M18), cap the containers (M28); announce long jobs; don't sit
on GPUs with idle notebooks (exit the kernel); keep `$HOME` lean, use
`/scratch` for intermediates; back up before you purge; and document
what you leave running. Lesson 2 turns the list into mechanics.

---

## Key takeaways

- The shared server changes the **contract** — guest not owner, jobs
  outlive logins, everything visible — not the tooling.
- The **directory contract** (`$HOME` code, `/data` shared+protected,
  `/scratch` ephemeral) is M06+M13 grown up; permissions are the
  collaboration policy.
- **venv+pip default; conda read-and-translate** (native/CUDA deps are
  why it exists; micromamba makes it sudo-free); the environment-file
  law outranks the tool.
- **GPU/CUDA at admin level**: `nvidia-smi` is the instrument, driver
  vs toolkit is the mismatch diagnosis, GPU memory is the contested
  resource, containers are the distribution mechanism — and every
  concept has a CPU-only twin this course uses.

## Check yourself

1. Why does a 200 GB intermediate belong in `/scratch` and not
   `$HOME`? Give two reasons from different modules.
2. A teammate's `environment.yml` pins `cudatoolkit=11.8`. What layer
   of the GPU stack does that pin manage, and what does it *not*
   manage?
3. Your GPU job finished but `nvidia-smi` still shows your memory
   held. Why, and what's the fix?
4. What makes conda attractive on servers despite venv's simplicity —
   and what makes it viable without sudo?

*Answers:* (1) Backup volume: `$HOME` is backed up and a 200 GB
intermediate wrecks the backup target (M24's capacity triage); and
`/scratch` is the fast/ephemeral layer designed for exactly that
lifetime — intermediates that die with the job. (2) The CUDA
*toolkit/runtime* layer — inside the environment; the *driver* is
host-level, owned by admins, and must merely be ABI-compatible with
the toolkit. (3) The framework's caching allocator holds GPU memory
until the process exits — the kernel is still alive in an idle
notebook; exit the kernel/shut the notebook down (etiquette: release
what you're not using). (4) conda manages *native* dependencies
(CUDA, MKL, GDAL) that pip cannot — real ML needs them; micromamba
installs entirely in user space, no sudo required.

Up next: [Running work](02-running-work.md) — tmux, tunnels, and
watching your job behave.
