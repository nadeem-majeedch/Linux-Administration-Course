# Data Science Linux Server Administration Lab

> M31 capstone lab · Unit 8 companion · Time: ~3 hours (can split across two sittings)
> Environment: **your own VM, CPU-only** — the "ML server" is a second user
> account playing the shared machine; no GPUs, no cloud, no spend
> Prerequisites: lessons 1–3 and the [13 scenarios](../lessons/04-scenario-walkthrough.md)
> ⚠️ Everything under your two accounts on your VM. Cleanup is a graded
> phase, not an afterthought.

## The setup — a two-actor stage (10 min)

Your VM plays the shared server; a **second user account** (`colleague`)
plays everyone else. If you haven't made one (M12):

```console
$ sudo useradd -m -s /bin/bash colleague && sudo passwd colleague
$ sudo groupadd lab && sudo usermod -aG lab $USER && sudo usermod -aG lab colleague
$ sudo mkdir -p /data/public /scratch && sudo chgrp -R lab /data /scratch
$ sudo chmod 2770 /data /scratch        # SGID commons (M13)
```

Stage the "department dataset" as the admin would:

```console
$ printf 'region,revenue,units\nnorth,1200,15\nsouth,850,11\nnorth,300,4\neast,410,6\n' | \
    sudo tee /data/public/sales2019.csv > /dev/null
$ sudo sha256sum /data/public/sales2019.csv | sudo tee /data/public/SHA256SUMS
$ sudo chmod 0640 /data/public/*        # read-only for the lab group (the guard)
```

You are now `student` (your account); `colleague` exists for the
shared-permission proofs in Phase 4. Keep `lab-log.md` open — **every
phase ends with evidence, and the evidence chain is the grade.**

---

## Phase 1 — Access & connection (Scenarios 1–2)

```console
$ ssh student@localhost                  # the "server" is your VM; keys already yours
$ whoami && id && df -h /data /scratch   # identity, groups, limits — scenario 1
$ tmux new -s ds-lab                     # scenario 2: everything from inside tmux
```

**Evidence:** the `id` output (you're in `lab` — that's the
permissions story later), and `tmux ls` after a deliberate
detach/reattach.

## Phase 2 — Project, environment, dependencies (Scenarios 3–5)

```console
$ mkdir -p ~/proj/{src,notebooks,scripts,data/processed} ~/proj-runs && cd ~/proj
$ git init && git config user.name "Lab Student"     # (M26 config already set? keep it)
$ printf '.venv/\nruns/\n__pycache__/\n.ipynb_checkpoints/\n*.log\n' > .gitignore
$ python3 -m venv .venv && source .venv/bin/activate
(.venv) $ python -m pip install pandas==2.2.3 scikit-learn==1.5.2
(.venv) $ pip freeze > requirements.txt && pip check && wc -l requirements.txt
```

**Evidence:** `which python` inside the venv, the freeze line-count,
and `pip check`'s silence. *Conda aside (lesson 1 §3):* write, in the
log, the `environment.yml` equivalent of your two pins — name, deps,
pip section — to prove you can translate.

## Phase 3 — Code, dataset, experiment (Scenarios 6–9)

The method, as a collaborator would provide it — write it to
`~/proj/src/train.py` (a deliberately modest CPU workload: logistic
regression with a sweep, checkpointing per epoch):

```python
"""Run-aware trainer: stamps its run dir, logs, checkpoints, ends with DONE."""
import argparse, json, hashlib, time, os
from datetime import datetime
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

p = argparse.ArgumentParser()
p.add_argument("--config", required=True)
args = p.parse_args()
cfg = json.load(open(args.config))

run = os.path.join(os.path.expanduser("~/proj-runs"), cfg["run_name"])
os.makedirs(os.path.join(run, "checkpoints"), exist_ok=True)
os.makedirs(os.path.join(run, "model"), exist_ok=True)

df = pd.read_csv(cfg["data_path"])          # references the commons via config
X = pd.get_dummies(df[["region"]])
y = df["units"]
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=cfg["seed"])

metrics = open(os.path.join(run, "metrics.csv"), "a")
metrics.write("epoch,lr,val_mae\n")
model = None
for epoch, lr in enumerate(cfg["lrs"], 1):
    model = LogisticRegression(C=1.0 / lr, max_iter=200)
    model.fit(Xtr, ytr)
    mae = mean_absolute_error(yte, model.predict(Xte))
    metrics.write(f"{epoch},{lr},{mae:.4f}\n"); metrics.flush()
    tmp = os.path.join(run, "checkpoints", "last.joblib.tmp")
    joblib.dump({"model": model, "epoch": epoch, "lr": lr}, tmp)
    os.rename(tmp, os.path.join(run, "checkpoints", "last.joblib"))   # atomic (M27 Q21)
    print(f"[{datetime.now().isoformat(timespec='seconds')}] epoch={epoch} lr={lr} val_mae={mae:.4f}", flush=True)
    time.sleep(1)                            # so htop/watch have something to watch

joblib.dump({"model": model, "config": cfg}, os.path.join(run, "model", "model.joblib"))
print(f"[{datetime.now().isoformat(timespec='seconds')}] DONE best_epoch={epoch} artifacts=model/model.joblib", flush=True)
```

Scenario 6 — the repo (local bare remote as the GitLab):

```console
$ git init --bare ~/repos/ds-lab.git
$ git remote add origin ~/repos/ds-lab.git
$ printf 'region,revenue\nnorth,1200\nsouth,850\n' > data/processed/preview.csv
$ git add -A && git commit -m "Run-aware trainer + pinned env" && git push -u origin main
```

Scenario 7 — the dataset, *verified and referenced*:

```console
$ cd /data/public && sha256sum -c SHA256SUMS && cd ~/proj
$ ln -s /data/public/sales2019.csv data/sales2019.csv
$ cat > config.yaml <<EOF
run_name: 2026-09-20_lr0.001
data_path: /data/public/sales2019.csv
lrs: [0.01, 0.1, 1.0]
seed: 42
EOF
```

Scenarios 8–9 — Jupyter (tunneled, kernel registered) and the
launch, per lesson 2 §2's pre-flight:

```console
(.venv) $ python -m ipykernel install --user --name ds-lab
(.venv) $ jupyter lab                     # verify bind: ss -tlnp | grep 8888 → 127.0.0.1
# tunnel from your "laptop" terminal: ssh -L 9999:127.0.0.1:8888 student@localhost -N
(.venv) $ nice -n 10 python src/train.py --config config.yaml \
    2>&1 | tee ~/proj-runs/2026-09-20_lr0.001/logs/train.log
```

(The launcher's run-dir stamping is abbreviated here — config carries
the run name — but the *log + DONE line + metrics* contract is
enforced by `train.py` exactly as lesson 3 §3 demands.)

## Phase 4 — Shared-server proofs (colleague exists for a reason)

Three permission facts, witnessed — `sudo -iu colleague` for the
second actor:

```console
$ echo x > /data/public/probe.txt            # FAILS: read-only commons (guard working)
$ sudo -iu colleague -- head -1 /data/public/sales2019.csv    # colleague CAN read
$ sudo -iu colleague -- ls ~/proj             # colleague CANNOT — $HOME is yours alone
```

**Evidence:** the three transcripts — your failed write (the
permission *system* enforcing the contract), colleague's successful
read (the commons works), colleague's failed `ls` (privacy works).

## Phase 5 — Monitor, store, verify (Scenarios 10–11)

Split tmux (`Ctrl-b %`); run the monitoring circuit in the right pane
while the sweep runs in the left:

```console
$ htop                       # the nice-10 job, ranked below your interactive shell
$ watch -d free -h           # available: the pre-flight's promise, held
$ tail -f ~/proj-runs/*/logs/train.log
```

Then the artifact chain:

```console
$ ls -la ~/proj-runs/2026-09-20_lr0.001/{logs,checkpoints,model}
$ cat ~/proj-runs/*/metrics.csv              # the epoch rows — the quantitative heartbeat
```

**Evidence:** the DONE line, `metrics.csv` contents, and one htop
frame showing your job *nicely* below others.

## Phase 6 — Back up, restore-drill, clean up (Scenarios 12–13)

```console
$ git add -A && git commit -m "First sweep complete" && git push   # code: the push IS the backup
$ tar czf ~/runs-backup.tar.gz -C ~ proj-runs/2026-09-20_lr0.001 --exclude='checkpoints'
$ sha256sum ~/runs-backup.tar.gz | tee ~/runs-backup.sha256
$ mkdir -p /scratch/$USER/restore-test && tar xzf ~/runs-backup.tar.gz -C /scratch/$USER/restore-test
$ sha256sum ~/runs-backup.tar.gz && diff <(sha256sum ~/runs-backup.tar.gz | cut -d' ' -f1) \
    <(cut -d' ' -f1 ~/runs-backup.sha256) && echo RESTORE-VERIFIED
$ python -c "import joblib; m=joblib.load('/scratch/$USER/restore-test/proj-runs/2026-09-20_lr0.001/model/model.joblib'); print('model loads:', type(m['model']).__name__)"
```

The **untested-restore rule, performed**: checksum verified *and* the
model actually loaded from the restored tree — a backup that can't do
both is a rumor.

Cleanup (scenario 13, the graded one):

```console
$ tmux ls && tmux kill-session -t ds-lab
$ ss -tlnp | grep 8888            # find the jupyter PID; kill $(…) politely; re-run: gone
$ rm -rf /scratch/$USER/restore-test
$ du -sh ~/proj-runs && df -h /data /scratch    # the box as you found it
```

## Done when (the evidence chain, phase by phase)

- [ ] P1: `id` (lab membership) + detach/reattach proof
- [ ] P2: venv `which python`, freeze + `pip check`, the
      `environment.yml` translation paragraph
- [ ] P3: pushed commit (bare remote), checksum-verified dataset,
      symlink (not copy), tunnel + kernel evidence, niced launch
- [ ] P4: the three permission transcripts (guard works, commons
      works, privacy works)
- [ ] P5: DONE line, `metrics.csv`, monitoring frame
- [ ] P6: push, backup + checksum, **restore-verified + model-loads**,
      cleanup census (`tmux ls`, `ss`, `df`) clean
- [ ] One paragraph: the reproducibility chain for *your* run — six
      links, each naming its artifact (lesson 3 §5)

**Feed-forward:** this working setup — repo, pinned env, run-tree
convention, backup habit — is the [capstone's](../../../M30-capstone-project/README.md)
starting kit; the lab's evidence chain is the capstone's grading
standard in miniature.
