# Module 01 — What Is Linux? (Foundations of Linux)

> Unit 1 · Foundations of Linux
> Difficulty: Beginner · Prerequisites: none
> Environment: read-along now, hands-on from Lesson 8 (Setup) onward

## What this module is

The zero-to-one module. You arrive knowing only how to use a computer with icons;
you leave able to *talk about* Linux correctly, *run* your first commands, *find
answers* in the system's own documentation, and *operate* a real Ubuntu environment
you set up yourself.

No prior Linux experience is assumed. If you can install an app and type in a box,
you can do every lab in this module.

## Lessons (8)

| # | Lesson | Covers | Lab |
|---|---|---|---|
| 1 | [What Is Linux?](lessons/01-what-is-linux.md) | Operating systems, the kernel, GNU/Linux naming, where Linux runs | — |
| 2 | [Linux vs Unix & Open Source](lessons/02-linux-vs-unix-and-open-source.md) | Unix lineage, licenses, free software vs open source, why it matters for you | — |
| 3 | [Distributions & Ubuntu](lessons/03-distributions-and-ubuntu.md) | Distros, families, release models, why the course uses Ubuntu LTS | — |
| 4 | [Linux Architecture](lessons/04-linux-architecture.md) | Layers, kernel space vs user space, "everything is a file", the shell's place | [Lab 1](labs/lab-01-identify-your-system.md) |
| 5 | [The Shell & The Terminal](lessons/05-shell-and-terminal.md) | Terminal vs shell vs console, CLI vs GUI, why data scientists live in the CLI | — |
| 6 | [Getting Help: man, info, --help](lessons/06-getting-help.md) | Man pages, sections, info, `--help`, the survival skill | [Lab 2](labs/lab-02-man-page-tour.md) |
| 7 | [Command Syntax: Options & Arguments](lessons/07-command-syntax.md) | The grammar of commands: prompts, options, arguments, safe first commands | [Lab 3](labs/lab-03-first-commands.md) |
| 8 | [Setup: VMs, WSL2 & Ubuntu](lessons/08-setup-vms-wsl2-ubuntu.md) | Installing Linux, virtual machines, WSL2, Ubuntu setup, first login | [Lab 4](labs/lab-04-ubuntu-setup.md) |

**Suggested order:** Lessons 1–3 (concepts) → Lesson 8 (set up your machine) →
Lessons 4–7 (architecture, terminal, help, syntax). Many students prefer installing
Ubuntu early so every later lesson happens on a real system; the module works either
way.

## What you will be able to do

- Explain what an operating system is and what the Linux kernel does
- Correctly use the terms kernel, distribution, shell, terminal, GUI, CLI
- Name the major distribution families and say which one you use and why
- Explain user space vs kernel space and why the separation protects you
- Set up Ubuntu LTS in a VM (or WSL2) and take a snapshot
- Log in, open a terminal, and run your first commands safely
- Look up any command's manual and read it
- Predict what a command line will do by reading its options and arguments

## Definitions of done

- [ ] All 8 lessons read; each lesson's exercises attempted
- [ ] Labs 1–4 completed; results recorded in your `lab-log.md`
- [ ] Quiz (30 questions) passed: [practice/quiz.md](practice/quiz.md) — 80% minimum
- [ ] At least 3 challenge exercises from [practice/challenges.md](practice/challenges.md) attempted
- [ ] Your environment exists, is snapshotted, and is recorded in `lab-log.md`

## Data Science connection

Every Jupyter server, GPU cluster node, Docker container, and cloud instance you will
ever use in your career runs Linux. This module gives you the vocabulary those systems
speak — kernel, distribution, shell, daemon, user space — and a working environment
where the rest of the course happens. By Lesson 8 you already have the machine that
later modules will turn into your personal data-science workstation.

## Full specification

The complete module contract (objectives, skills, roadmap placement) is in the
[module root README](../README.md) and [COURSE-ROADMAP.md](../../../COURSE-ROADMAP.md).

## Troubleshooting

Anything in the labs misbehaving? Start with the
[module troubleshooting guide](troubleshooting.md) — it covers the ten most common
failure points at this stage, from "VT-x disabled" to "sudo doesn't work".
