# Lab 3 — The Priority Clinic: Keep Jupyter Responsive Under Load

> Module 18 · Unit 5 · Difficulty: Intermediate
> Environment: your own VM/WSL2, normal user · Time: ~35 min
> Prerequisites: [Lesson 3](../lessons/03-priority-and-resources.md)
> Safety: burners are nice 19; the only sudo is one optional, marked check.

**Scenario:** you're in a Jupyter session exploring a dataset while a
batch preprocessing job runs. Done badly, the batch makes the notebook
unusable. Done well, both coexist. This lab builds the "done well."

## Part A — the actors

```console
$ mkdir -p ~/lab18 && cd ~/lab18
# "Jupyter": an interactive loop that must stay snappy
$ cat > jupyter_sim.sh <<'EOF'
#!/bin/bash
while true; do
  s=$(date +%s%N); :; e=$(date +%s%N)
  echo $(( (e - s) / 1000000 )) >> latency.log
  sleep 0.5
done
EOF
$ chmod +x jupyter_sim.sh && ./jupyter_sim.sh & echo "jupyter PID: $!"
# "batch": a CPU burner
$ nice -n 19 bash -c 'while :; do :; done' & echo "batch PID: $!"
```

## Part B — baseline, then contention

```console
$ sleep 10; tail -5 latency.log        # baseline: ~0 ms with an idle box
$ for i in 1 2 3; do nice -n 19 bash -c 'while :; do :; done' & done
$ sleep 20
$ uptime                                # load now ~= core count
$ awk '{s+=$1; if ($1>m) m=$1} END {print "mean", s/NR, "ms; max", m, "ms"}' latency.log
```

**Record:** mean/max latency before vs during four nice-19 burners. With
burners *nicely* at +19, your interactive loop should barely notice —
that's the entire point of nice. If your VM has 1–2 cores and you *do*
see latency, note it: contention math depends on core count, and your
write-up should say so.

## Part C — what if batch *hadn't* been nice?

```console
$ pgrep -af "while :; do :; done" | head     # preview the burners' PIDs
$ sudo renice -n 0 -p PID1 PID2 PID3         # OPTIONAL (sudo, your VM):
                                             # make them equals
$ sleep 20
$ awk '{s+=$1} END {print "mean now:", s/NR, "ms"}' latency.log
```

Now the interactive loop *does* suffer — equal priority, equal share.
Restore kindness without sudo being needed:

```console
$ renice -n 19 -p PID1 PID2 PID3              # lowering back is always allowed
$ pkill -u $USER -f "while :; do :; done"     # preview with pgrep -af first!
```

**Record:** the three latency means (baseline / nice-19 load / nice-0
load). Three numbers, one conclusion about niceness on shared machines.

## Part D — the memory side

```console
$ python3 - <<'EOF' &
a = []
while True:
    a.extend([0] * 10_000_000)   # ~80 MB per append, forever
    time.sleep(1)
EOF
$ top -p $(pgrep -f "a.extend")     # M-sort; watch RSS climb
```

Let it reach ~1 GB, then TERM it (PID from pgrep; TERM is plenty — *why
doesn't this need KILL?*). **Record:** the RSS at kill time and one
sentence on what would have happened on a shared server without a limit
(→ M20's systemd limits; → OOM, Lesson 3 §5).

## Part E — the clinic report (deliverable)

Write the incident-style summary of this lab using the Lesson-3 playbook
format: load numbers, latency table, renice interventions with PIDs,
memory observation, and the mitigations you'd propose for a real 24-core
server running three batch jobs and eight notebooks. Half a page maximum —
brevity is part of the exercise.

## Done when

- [ ] Three latency means recorded (baseline / +19 load / 0 load)
- [ ] The sudo renice step done (or explicitly skipped with reasoning)
- [ ] Memory experiment: RSS captured, job terminated by TERM
- [ ] Clinic report written to playbook format
- [ ] All burners and the memory eater confirmed dead (`pgrep` census clean)
