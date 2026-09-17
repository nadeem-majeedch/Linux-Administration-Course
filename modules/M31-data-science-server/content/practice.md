# M31 Practice — The Data Science Server

## Quiz (22 questions)

Answer first, then check the key below. Method and *why* count: a
command without its reason earns half.

### Section A — the server frame (Q1–6)

**Q1.** State the three contract changes a shared ML server imposes
versus your workstation VM.

**Q2.** The directory contract: where do code, shared datasets,
derived data, and big intermediates each live — and why does `/scratch`
exist as a *separate* filesystem role?

**Q3.** `/data/public/sales2019.csv` is group-owned `lab`, mode 0640,
directory 2750. Explain what each element guarantees, and who can
write there.

**Q4.** Why is `pip install --user` worse than a project venv on a
shared server, when both avoid sudo?

**Q5.** A teammate's `environment.yml` lists `pytorch`, `cudatoolkit=12.1`,
and a `pip:` section. Translate the file's *shape* to your venv+pip
world, and name the dependency you could *not* carry over.

**Q6.** In the GPU stack (framework → toolkit → driver → hardware),
which layers can you, a non-root researcher, control — and which
mismatch causes the classic "CUDA version insufficient" failure?

### Section B — running work (Q7–12)

**Q7.** SSH drops 40 minutes into training. For each tool — bare SSH
command, `nohup … &`, tmux, systemd user unit — is the job alive, and
is its output recoverable?

**Q8.** Why pair tmux with `| tee logfile` rather than trusting
either alone?

**Q9.** List the four pre-flight items before launching a long job,
and the one extra item on a GPU box.

**Q10.** What does `nice -n 10` change — and what does it *not*
change — about your job's effect on colleagues?

**Q11.** Jupyter's server vs kernels: which one holds RAM/GPU while a
notebook sits idle, and what is the etiquette fix?

**Q12.** `nvidia-smi` shows a GPU at 3% utilization but 22 GB/24 GB
memory used. Diagnose in one sentence, name the instrument that
confirms it, and the fix.

### Section C — data & reproducibility (Q13–18)

**Q13.** Why reference the shared dataset (symlink/absolute path)
rather than copying it into `$HOME`? Two costs of copying.

**Q14.** What role does `SHA256SUMS` play in the `/data` contract,
and when do you run it?

**Q15.** Name the five things a trustworthy run directory contains
beyond the model file — and say which one *you* must write by hand
(versus the launcher writing it).

**Q16.** The three-element evidence bundle for "this run happened" —
and the one line that distinguishes *finished* from *merely wrote
output*.

**Q17.** Which content classes get backed up on the DS server, and
which deliberately don't? One line of why per class.

**Q18.** The reproducibility chain's six links — name each and its
artifact.

### Section D — synthesis (Q19–22)

**Q19.** Scenario 13 (cleanup) is graded like the others. Argue the
case: why is cleanup an *administrative* deliverable rather than
common courtesy?

**Q20.** A colleague's notebook has held a GPU kernel idle for two
days (3% util, 20 GiB held). Compose the two-sentence message you'd
actually send — polite, specific, with the instrument's numbers.

**Q21.** Your run's `metrics.csv` shows val_mae flat from epoch 5 to
12. What does that suggest about the *next* launch — and which
scenario's mechanics make the re-launch cheap?

**Q22.** The capstone grades "reliable and reproducible beats
impressive and mysterious." Map that sentence onto this module: which
lesson owns *reliable*, which owns *reproducible*, and what single
lab artifact demonstrates both?

### Key (sketch answers — your wording may be better)

1. Guest not owner (user-space only); the box outlives your login
   (survival + backup contracts); everything you do is visible
   (etiquette as policy).
2. Code → `$HOME` (backed up, quota'd); shared datasets → `/data`
   (protected commons); derived data → per-project `processed/`
   (regenerable); intermediates → `/scratch` (fast, ephemeral,
   purge-eligible) — separating *lifetime and audience* of each data
   class so backup/quota/purge policies can differ per role.
3. `lab` group membership grants read; SGID on the directory keeps
   new files group-`lab`; 0640 = group-read, no group/other write →
   nobody but admins (or the `data` owner) writes; the commons is
   read-only *to researchers by construction*.
4. `--user` installs into a shared-per-user site-packages — version
   conflicts leak across *all* your projects (and into any tool that
   reads user site), while a venv is project-scoped and disposable;
   on a multi-project server, `--user` recreates the system-Python
   crosstalk problem one level down.
5. `name:` → project dir; conda deps → apt/system packages or conda-
   only recognition; the `pip:` section → `requirements.txt` verbatim.
   `cudatoolkit` cannot carry over — it's a conda-channel native
   package (the reason conda exists); venv+pip would need a wheel
   that bundles its own CUDA runtime instead.
6. You control the *framework* and the *toolkit/runtime* (per-
   environment); the *driver* is host-level (admins). Mismatch:
   toolkit newer than the driver's ABI — fix environment-side
   (older toolkit/wheel), never by touching the driver.
7. bare SSH: dead, output lost. nohup: alive, output in the
   redirect file. tmux: alive, interactive state *and* (with tee)
   the log. user unit: alive, supervised (restart on failure),
   journald captures output.
8. tmux alone: output lives in scrollback (history lost on kill);
   tee alone: disk evidence but no interactive view; together: live
   pane *and* durable log — M24's evidence contract applied to your
   own job.
9. Estimate footprint (peak RSS via scaled run / `time -v`); nice
   the launch; unconditional logging (`tee`, absolute paths);
   checkpoint design (resume-able). GPU extra: check `nvidia-smi`
   free memory and pin `CUDA_VISIBLE_DEVICES` per the box's
   convention.
10. Changes: scheduling priority under contention (colleagues'
    interactive work keeps latency). Not changed: memory footprint,
    I/O volume, runtime — nice is ranking, not a resource cap.
11. The *kernel* (a separate process per notebook) holds its
    allocations — including the GPU caching-allocator pool — while
    idle. Fix: shut kernels down from the Running tab when a run
    ends.
12. Idle kernel/process holding the caching allocator's pool —
    allocated but unused. Confirm: `nvidia-smi`'s process list (the
    PID and its MiB). Fix: exit that process (shut the kernel down);
    memory returns on process exit.
13. Quota debt (`$HOME` is quota'd and backed up) and divergence risk
    (copies silently differ; the checksummed commons guarantees one
    version).
14. It's the immutability *proof* of the commons: run it at download
    and any time you suspect drift — `sha256sum -c` passing means
    you're on the version everyone cites.
15. Stamped `config.yaml` (resolved config + code SHA + data
    checksum), `logs/` (the tee'd transcript), `metrics.csv` (epoch
    rows), `checkpoints/` (resume states), `model/` + metadata
    sidecar. The launcher writes all but the *config values
    themselves* — the knobs you chose are the hand-written part.
16. The log line (job's voice), the output artifact (metrics/
    checkpoint/model), the resource trace (monitoring snapshot) —
    and the `DONE best_epoch=…` line is the finished marker: a run
    without it didn't complete, whatever the files suggest.
17. Code → the git *push* (off-site by definition); run configs/
    metrics/logs → backed up (small, irreplaceable context); model
    artifacts → backed up (weeks of compute); checkpoints → latest
    only (resumability, not history); `/scratch` → never (ephemeral
    by design).
18. Code = git SHA; environment = `requirements.txt` pins (or image
    SHA); data = dataset checksum; config = stamped `config.yaml`;
    run = the run directory; proof = fresh clone + fresh env re-run
    reaching the same numbers.
19. Because leftover state *is* an administrative condition: idle
    kernels hold resources others need, un-purged scratch becomes
    next month's disk-full incident (M32-clinic card 2), and the
    cleanup census is the same evidence discipline as every other
    scenario — the box's health is part of the work.
20. "Hi — `nvidia-smi` shows your PID 5432 holding 20 GiB on GPU 0 at
    3% utilization since Sunday; I need the memory for tonight's
    sweep. Could you shut the notebook's kernel down, or should I?
    (Nothing is lost — it'll re-allocate on your next run.)"
21. Flat validation suggests the learning-rate range is wrong (or the
    model's capacity is) — the next launch changes *config*, and
    scenario 9's mechanics make that cheap: new run directory, same
    code, stamped config, resumable pattern — a config change is a
    one-file edit plus one command.
22. *Reliable* is lesson 2 (tmux/tee survival, pre-flight, nice,
    monitoring, checkpoints — the job behaves); *reproducible* is
    lesson 3 (the six-link chain, stamped configs, checksums). The
    lab artifact that demonstrates both: the **run directory with its
    DONE line, stamped config, metrics, and the restore-verified
    backup** — evidence that it ran reliably *and* can be re-run.

## Challenges (C1–C6)

**C1 — The conda translation.** Take any public `environment.yml`
(find one in a GitHub repo you use); produce the venv+pip
`requirements.txt` equivalent, the list of conda-only deps you *can't*
translate, and — for one of those — the pip wheel that bundles the
native lib instead. Deliverable: both files + the three-line
commentary.

**C2 — The etiquette monitor.** Script `etiquette.sh`: runs
`nvidia-smi --query-compute-apps=pid,used_memory` (or, CPU-only, a
`ps --sort=-rss | head`), flags any process using more than a fair
share (arg-threshold), and prints a ready-to-send note per offender.
Test against your own deliberately-greedy `mem_grow` (M24-clinic).
Deliverable: script + the note it produced about *you*.

**C3 — Run-tree archaeology.** Two run directories from Phase 3's
sweep, no README, no config — just `metrics.csv`. Reconstruct which
run was better *and which config produced it* from artifacts alone;
then add the one file to each directory that would have made the
archaeology trivial. Deliverable: the verdict + the file.

**C4 — The kill-and-resume drill.** Kill the Phase-3 training
mid-sweep (`kill`, not `kill -9`), then resume from the checkpoint
into a *new* run directory (per lesson 3's config discipline).
Deliverable: both run dirs' logs + one paragraph on what resume
*cost* you (the honest answer: nothing, if the checkpoint pattern is
right — prove it).

**C5 — The shared-server incident.** Your colleague (the `colleague`
account) fills `/scratch` to 95% with an abandoned 3 GB file while
your training runs. Walk the M32-clinic disk-full card *from the
user side*: diagnose (`df`, `du` on the shared FS), escalate to the
"admin" (you, sudo — but write the ticket you'd send a real one),
and state what the *policy* fix is (purge daemon? quotas?). No
deleting colleague's files — the fix is a conversation and a policy,
not `rm`.

**C6 — The reproducibility audit.** Trade lab logs with a classmate.
Using *only their log*, rebuild their run: clone their repo ref,
recreate their env from their freeze, verify their dataset checksum,
re-run their config, compare `metrics.csv`. Score them: which of the
six chain links were actually present? Deliverable: their scorecard
+ the one missing link that broke your rebuild (someone's will).

---
*Back to: [module index](README.md) · [M31 README](../README.md) ·
[M30 Capstone](../../M30-capstone-project/README.md)*
