# Unit 7 Speaker Notes — The Data Science Stack (M26–M29)

> Companion to [../lecture-slides/unit-07-data-science-stack-slides.md](../lecture-slides/unit-07-data-science-stack-slides.md).

## Sessions 25–28 overview

**Teaching purpose.** Install the profession on the machine. The
pedagogical spine: *every DS tool is administered with verbs students
already own* — services, permissions, tunnels, logs, mounts. By week's
end the "integrated loop" slide should feel like a summary of the whole
course, not a new diagram.

**Opening question (S25).** "What does Git actually store when you
commit?" Expect "the files" — the pointer/snapshot correction is the
session's load-bearing idea; everything about branching follows from it.

## Per-slide guidance

- *S2 (Git model):* draw commits as nodes, branches as sticky labels.
  Move the label live on the drawing. The "branch copies my project"
  fear dies here or haunts them for years — spend the time.
- *S3 (SSH remotes):* connect explicitly to M22: "the key you made in
  week 11 is your GitHub credential now." Identity config: two minutes,
  but commit-authorship fails without it and the error confuses.
- *S4 (venv):* the `which python3` in/out demo is the unit's best
  thirty seconds. The M15 PATH mystery resolves *visibly* — ask a
  student to narrate the mechanism before you confirm.
- *S5 (Jupyter):* full reframe as a supervised service: start it,
  `ss` proves the listener, tunnel reaches it, journal/logs hold its
  words. nbconvert mention earns its keep with the "nobody watches
  notebooks at 2 a.m." line — batch is the adult form.
- *S7 (containers):* kernel-sharing explains startup speed — demo by
  timing `docker run hello-world` vs a VM boot. The volume-permission
  gotcha gets named now (M13 knowledge) because every cohort hits it.
- *S8 (serving):* 502-from-nginx-logs demo: the reverse proxy is
  *upstream-dead*, and the log says so in one line. This is the
  practical exam's evidence-reading habit in new clothes.

## Misconceptions (unit-wide)

1. "Git stores whole project copies" — pointer graphs; deltas and
   objects, cheaply.
2. "venv is optional hygiene" — it's the isolation boundary; system
   python breakage is a *reinstall* event.
3. "Jupyter is a GUI app" — it's a server: ports, PIDs, logs, kernels.
4. "Containers are tiny VMs" — different mechanism (namespaces/cgroups
   conceptually), different guarantees; kernel is *shared*.
5. "A dump file is a backup" — the rumor backup; restore-test or it
   doesn't exist.

## Expected responses & probes

- S2 trick question ("what got copied?"): correct answers mention
  pointers/labels; probe further: "where do the *files* live?" — the
  object store answer completes the model.
- S4 three-suspects question: wrong-env, wrong-kernel, not-installed-in-
  *this*-venv — students who produce all three are venv-fluent; those
  who produce one are pip-fluent only. Route the latter to the M27
  troubleshooting page.
- S9 Q2 (502 log first): expect "nginx error.log" — accept; sharpen to
  *which line shape* (upstream connect/refuse) and what it implies.

## Demo choreography & error table

| Session | Demo | Failure beat | Recovery |
|---|---|---|---|
| S25 | merge conflict (tiny) | conflict markers | edit, add, commit |
| S26 | bare `pip install` into system | permission error / externally-managed | venv, redo |
| S26 | tunnel | page unreachable before tunnel, works after | — (the contrast) |
| S27 | volume + wrong ownership | app can't write /data | chown/group fix (M13 verbs) |
| S28 | 502 | upstream dead | read log, start upstream, retry |

## Classroom activities

- S26: "three suspects" drill on printed stack traces (pairs, 5 min).
- S27: docker run flag-ordering exercise — broken commands to repair.
- S28: request-lifecycle tracing: one request, name every hop and log
  it would touch.

## Timing & cuts

S26 and S28 are dense; the cuttable slice is nbconvert (S26) and the
reverse-proxy theory (S28, labs carry it). Never cut: which-python3
demo, tunnel demo, 502 log demo — they're the transfer moments.

## Transition

"You can run the whole stack. Unit 8: run it *as a server* — and defend
the work." (M31/M32, revision, then the exams.)
