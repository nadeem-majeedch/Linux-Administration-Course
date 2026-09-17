# The Thirteen Scenarios — Your First Week on the ML Server

> M31 · Unit 8 companion · Difficulty: Advanced
> Reading time: ~35 min · Lab: [Data Science Linux Server Administration Lab](../labs/ds-server-lab.md)
> These scenarios are narrated here and *performed* in the lab — read this
> as the story, run the lab as the practice.

---

**The setup.** Monday morning. The department admin emails you:
*"Account created on `ds-server` (our teaching VM — CPU-only, 4 cores,
8 GB, like every lab here). Your username is `student`. The shared
dataset is at `/data/public/sales2019.csv` with a checksum file
alongside. Key is registered. Welcome."*

Everything that follows is the course, in the order life actually
asks for it.

## Scenario 1 — You receive access

Before the first command, the admin's email already told you the
three facts that matter: the **host**, the **auth method** (your
Ed25519 key is registered — M22's `authorized_keys`), and the **data
location**. On a real server you'd also receive the usage policy —
which is lesson 2 §5's etiquette list with the department's specifics.
The M22 pre-flight runs from your machine:

```console
$ ssh -T student@ds-server
Welcome, student. This is a shared resource...
```

The host-key prompt appears once — and you *verify it* with the admin
before typing yes (M22's TOFU discipline). You're in; `whoami`, `id`,
and `quota -s` are the first three commands — identity, groups,
limits. Reading them is scenario 1's whole point: **know who you are
on the box and what your share is, before you touch anything.**

## Scenario 2 — You connect (and stay connected)

```console
$ ssh student@ds-server
$ tmux new -s week1
```

The connection *itself* is trivial; the *habit* is the scenario: from
this moment, all work happens inside tmux (lesson 2 §1) — every
future disconnect costs a reattach, never a job. The second pane
(`Ctrl-b %`) becomes the monitoring station. Name sessions for the
work (`week1`, not `0`), because in a month you'll have six.

## Scenario 3 — You create a project directory

The lesson-1 contract, instantiated:

```console
$ mkdir -p ~/proj/{src,notebooks,scripts} ~/proj-runs
$ cd ~/proj && git init && echo "sales-analysis on ds-server" > README.md
```

Code here (`~/proj`), runs later in `~/proj-runs` (lesson 3 §2) — the
two trees separate versioned text from regenerable work. The
`.gitignore` exists *now* (M26's ordering rule): `runs/`-style output
dirs, `.venv/`, `.ipynb_checkpoints/`, `*.log`.

## Scenario 4 — You create a Python environment

```console
$ python3 -m venv .venv && source .venv/bin/activate
(.venv) $ which python && python --version     # the two-line sanity (M27)
```

No sudo, no `--user`, nothing system-wide (M27 Q6) — on a shared
server this isn't just hygiene, it's *citizenship*: system Python
belongs to the OS and the admin. If the team used conda, this is
where `micromamba` would stand in (lesson 1 §3's translation); the
law is the same either way — **the environment is local to the
project and defined by a file.**

## Scenario 5 — You install dependencies

```console
(.venv) $ python -m pip install pandas==2.2.3 scikit-learn==1.5.2 matplotlib==3.9.2
(.venv) $ pip freeze > requirements.txt
(.venv) $ pip check
```

Pins land in the file (M27 Q3 — the exact versions, transitive
closure included), `pip check` is the resolver's confession, and the
file is committed *now* — the environment becomes reproducible at
this instant, not when you remember to.

## Scenario 6 — You clone a repository

```console
$ git clone ~/repos/team-methods.git ~/proj/methods   # local bare remote (M26 §1)
```

On a real server this is the department GitLab over SSH (M26 lesson
3 §3 — your key, again); in the lab it's a local bare repo playing
the remote. The clone is where you *read before you run*: the
collaborators' `requirements.txt`, their README's run commands, their
`config.yaml` — the M26 habit of reviewing what you're about to
execute on a machine other people share.

## Scenario 7 — You download/prepare a dataset

```console
$ ls -la /data/public/          # the commons: sales2019.csv + SHA256SUMS
$ cd /data/public && sha256sum -c SHA256SUMS   # integrity, verified
$ ln -s /data/public/sales2019.csv ~/proj/data/sales2019.csv
```

You **verify then reference** (lesson 3 §1): the checksum proves
you're on the version everyone else is; the symlink means your code
cites the commons, not a private copy that will drift. Preparation
(split, clean) writes to `~/proj/data/processed/` — derived from raw
by script, never by hand-edits — and *never* writes into `/data`
(read-only; the attempt failing is the guard working).

## Scenario 8 — You launch Jupyter

```console
(.venv) $ cd ~/proj
(.venv) $ python -m ipykernel install --user --name sales-analysis
(.venv) $ jupyter lab                      # binds 127.0.0.1, prints the token URL
```

From your laptop: `ssh -L 9999:127.0.0.1:8888 student@ds-server -N`,
browse `localhost:9999`, select the **sales-analysis** kernel
(M27 Q9 — the kernel *is* the venv). The posture is non-negotiable on
a shared box: loopback bind + tunnel (M27 Q7) — "open it to the LAN"
is the fastest way to become the security incident in Monday's
meeting.

## Scenario 9 — You run an ML experiment

The pre-flight (lesson 2 §2), then the launch — inside tmux, niced,
logged, checkpointed:

```console
(.venv) $ nice -n 10 python src/train.py --config config.yaml \
    2>&1 | tee ~/proj-runs/2026-09-20_lr0.001/logs/train.log
```

The launcher (M31 lesson 3 §2) created the run directory and stamped
`config.yaml` (resolved config + git SHA + dataset checksum). The
model is deliberately modest — logistic regression on the sales data
— because the *course* is teaching the frame, not the leaderboard.
The checkpoint logic (truncate-then-rename per epoch, M27 Q21) means
the job can be killed and resumed — which on a shared server is a
feature of citizenship, not an admission of failure.

## Scenario 10 — You monitor resources

Second tmux pane, the M24-clinic circuit on repeat:

```console
$ htop                 # your nice-10 job: visible, ranked, polite
$ watch -d free -h     # available holds — the pre-flight estimate holds
$ tail -f ~/proj-runs/*/logs/train.log    # epochs ticking, loss falling
```

On a GPU box, `nvidia-smi` takes the second line's place (lesson 1
§4); on this CPU-only teaching VM, the discipline is identical —
**watch the footprint, trust the log, release what you finish.**
Colleagues walking past see a niced, logged, monitored job: the
reputation you're building is this scenario.

## Scenario 11 — You store results

The run completes; its DONE line lands (lesson 3 §3's evidence
bundle):

```console
[2026-09-22T11:04] DONE best_epoch=7 val_mae=212.4 artifacts=model/model.joblib
$ ls -la ~/proj-runs/2026-09-20_lr0.001/
  config.yaml  logs/  metrics.csv  checkpoints/  model/
```

`metrics.csv` holds the epoch rows; `model/model.joblib` carries the
metadata sidecar (git SHA, dataset checksum, config). The three
elements — log line, artifact, config — make the run *citable*
(lesson 3 Q3's list, now all present).

## Scenario 12 — You back up results

The lesson-3 §4 split, executed:

```console
$ cd ~/proj && git add -A && git commit -m "First run: lr sweep prep" && git push origin main
$ tar czf ~/proj-runs-backup-2026-09-22.tar.gz ~/proj-runs/2026-09-20_lr0.001
$ sha256sum ~/proj-runs-backup-2026-09-22.tar.gz > ~/proj-runs-backup.sha256
```

Code is backed up *by the push* (M26's off-site truth); the run
directory — config, metrics, logs, model, *not* checkpoints-beyond-
latest — goes to the tar + checksum, per the M24 §5 rules. The
**restore drill** closes scenario 12: untar into `/scratch`,
checksum-verify, load the model, run the eval — the untested-backup
rule, performed while the week is fresh.

## Scenario 13 — You clean up resources

The scenario everyone skips, stated as policy (lesson 2 §5's last
row):

```console
$ tmux kill-session -t week1              # sessions closed
$ jupyter lab list                        # server: shut down politely (kill the PID)
$ # Jupyter "Running" tab: kernels stopped — the GPU/RAM you were holding, released
$ rm -rf /scratch/$USER/*                 # scratch is ephemeral BY DESIGN — purged
$ df -h /scratch && du -sh ~/proj-runs    # the numbers that prove it
```

Leaving a box as you found it — sessions dead, kernels released,
scratch purged, backups verified — is the last scenario *and* the
reputation's last mile. The admin's next email about the next
researcher will cite you as the example.

---

## The week in one paragraph

Access verified, connection made durable, project and environment
built from pins, dependencies frozen and committed, repository
cloned and *read*, dataset verified and referenced (never copied),
Jupyter reached through a tunnel, experiment launched niced and
logged inside tmux, resources watched, results stored with their
provenance, backups made *and restored*, everything cleaned up. **No
command in this story is new** — that's the course's thesis, closing:
administration is what makes the data science *possible*, and now it's
what makes it *yours*.

Up next: perform it — [the Lab](../labs/ds-server-lab.md).
