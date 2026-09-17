# M27 — Python, Jupyter and Data Workloads

> Unit 7 · The Data Science Stack
> Difficulty: Intermediate · Prerequisites: M16, M15, M10, M19

**Status: content complete.** Four lessons, three labs, an 8-challenge
practice set, and a ten-pattern troubleshooting index — all inside your own
VM, all loopback-only, all evidence-first.

## What this module covers

Python venvs and pinned requirements; Jupyter headless over SSH tunnels; background training runs with logs; GPU tooling awareness.

**Start here:** [content/README.md](content/README.md) — the module index with the recommended path.

| Piece | What you get |
|---|---|
| [Lesson 1](content/lessons/01-python-on-linux.md) | Python on Linux: interpreters, `python3 -m pip`, venv anatomy, PATH interplay, pinned requirements |
| [Lesson 2](content/lessons/02-jupyter-on-linux.md) | Jupyter headless: config, kernels-as-venvs, tunnels, nbconvert |
| [Lesson 3](content/lessons/03-background-workloads.md) | Long-running work: nohup/tmux/systemd, resource caps, GPU vocabulary |
| [Lesson 4](content/lessons/04-cli-python.md) | Python on the command line: one-liners, `-m` idioms, shell pipelines |
| Labs 1–3 | Build-freeze-recreate environments · remote Jupyter with tunnels · cron-scheduled batch with env rehearsal |
| [Practice](content/practice/quiz.md) | 22-question quiz + key, challenges C1–C8 |
| [Troubleshooting](content/troubleshooting.md) | 10 symptom→cause→fix patterns |

The full specification — learning objectives, concepts, command-line skills,laboratory, exercises, mini-project, and the Data Science connection — lives in
[COURSE-ROADMAP.md](../../COURSE-ROADMAP.md), Unit 7.

## Before you start

- [ ] Prerequisites complete: M16, M15, M10 (M19 for Lab 3)
- [ ] Lab environment working ([SETUP.md](../../SETUP.md))
- [ ] `lab-log.md` exists in your home directory

## Definition of done

- [ ] All three labs completed; evidence recorded in `lab-log.md`
- [ ] Environment freeze/recreate (Lab 1) proven as a second user
- [ ] Remote Jupyter reached via tunnel only (Lab 2) — LAN curl fails
- [ ] Nightly batch scheduled with `env -i` rehearsal passed (Lab 3)
- [ ] Quiz attempted before checking the key; ≥2 challenges done

## Module links

- Roadmap: [COURSE-ROADMAP.md](../../COURSE-ROADMAP.md#unit-7--the-data-science-stack-m26m29)
- Cheatsheets: [resources/cheatsheets/](../../resources/cheatsheets/)
- Fixes and questions: open an issue per [CONTRIBUTING.md](../../CONTRIBUTING.md)
