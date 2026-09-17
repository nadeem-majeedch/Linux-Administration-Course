# Lesson 2 — The Docker CLI and the Container Lifecycle

> Module 28 · Unit 7 · Difficulty: Intermediate → Advanced
> Reading time: ~30 min · Lab: [Lab 1](../labs/lab-01-first-containers.md)
> Up next: [Lesson 3 — Dockerfiles and builds](03-dockerfiles-and-builds.md)
> Prerequisite: Docker installed and working ([Lab 0](../labs/lab-00-install.md))

---

## 1. `docker run` — one command, many decisions

The workhorse. Every flag answers a design question you'd otherwise face
at 2 a.m.:

```console
$ docker run --rm -it python:3.12-slim python3 --version
Python 3.12.7
```

Read it left to right as a sentence: *create and start* (`run`) a
container from image `python:3.12-slim`, *auto-remove it when it exits*
(`--rm`), *allocate an interactive terminal* (`-it`), and run `python3
--version` **instead of the image's default command**.

| Flag | Question it answers |
|---|---|
| `--name web` | what should this container be called? (else Docker invents `quirky_einstein`) |
| `-d` | run in background ("detached") or foreground? |
| `-it` | do I need a terminal? (interactive shells, one-shot tools) |
| `--rm` | is this disposable? (one-shot jobs: yes — no corpse to clean) |
| `-p 127.0.0.1:8888:8888` | which container port appears on the host, and on which interface? |
| `-v data:/data` | what persists beyond the container? (Lesson 4) |
| `-e JUPYTER_TOKEN=…` | what configuration flows in? (Lesson 4) |

The image's **default command** matters: `docker run ubuntu` starts and
exits instantly (no terminal attached → nothing to do), while
`docker run -it ubuntu bash` gives you a shell. Same image, different
verb. Containers *exit when their main process exits* — that single rule
is the root of half of all beginner confusion ("my container died!"), and
it's not a malfunction: a container *is* a process (Lesson 1 §3).

## 2. The lifecycle, as a state machine

```text
            docker run
   (image) ────────────► created ──► running ──► paused
                                          │  ▲        │unpause
                              stop/kill   │  │start   │
                                          ▼  │        ▼
                                       stopped/exited ──► removed
                                          docker rm
```

- `docker create` + `docker start` is `docker run` split in two (rarely
  needed, but it explains the states).
- **`stop` vs `kill`** is the M18 signals story, exactly: `stop` sends
  SIGTERM, waits (10 s default) for a graceful exit, then SIGKILL;
  `kill` goes straight to SIGKILL. A well-behaved image traps SIGTERM and
  checkpoints — one reason `kill $(cat jupyter.pid)` worked in M27.
- **`restart`** = stop + start (a *re-run* of the same container);
  `--restart` policies (`on-failure`, `unless-stopped`) give daemon-side
  supervision — a nod toward M20's systemd unit thinking, inside Docker.
- **`--rm`** removes on exit; otherwise exited containers *persist* (with
  their logs and writable layer) until `docker rm`. This is a feature:
  autopsies need bodies.

Fore/background is fluid: start detached, then `docker attach` (or `logs
-f`) to re-watch; Ctrl-C in an attached foreground container sends the
signal *into* it — that's why the course detaches long runs and follows
logs instead.

## 3. Inspecting: the read-only vocabulary

```console
$ docker ps                  # running containers (the cockpit)
CONTAINER ID  IMAGE             STATUS         NAMES
3f9c1e2ab77d  python:3.12-slim  Up 30 seconds  gallant_einstein

$ docker ps -a               # + stopped ones (the graveyard — often the interesting part)
$ docker logs gallant_einstein          # its stdout/stderr, whenever it ran
$ docker logs -f --tail 20 gallant_einstein   # follow, last 20 lines first
$ docker top gallant_einstein           # processes inside (host view is `ps aux`!)
$ docker stats                          # live per-container CPU/mem (M24 echo)
$ docker inspect gallant_einstein       # everything: mounts, ports, env, IP (JSON)
$ docker exec -it gallant_einstein bash # shell INTO the running container
```

`exec` deserves emphasis: it runs a **new process inside the running
container's namespaces** — the same isolation rules, a fresh shell. It's
how you debug a container without disturbing its main process. Two honest
caveats: (1) `exec`'d processes vanish with the container — changes made
inside are written to the container's throwaway writable layer, *not* the
image ("fix by exec" is not a fix); (2) if the image is minimal, `bash`
may not exist — `sh` usually does.

**The image-side twins:**

```console
$ docker images                # local images (repo, tag, size, age)
$ docker pull python:3.12-slim # fetch from registry (all layers, deduplicated)
$ docker rmi python:3.12-slim  # remove an image (fails while containers use it)
$ docker system df             # disk usage: images/containers/volumes/cache
```

`docker images` shows *logical* sizes that overlap (shared layers); the
sum overstates real disk use — `docker system df` is the honest ledger.

## 4. Ports and naming, working examples

A container's network is its own (namespace!). To reach a service inside
from the host, publish the port at run time:

```console
$ docker run -d --name notes -p 127.0.0.1:8080:80 nginx:1.27-alpine
$ curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8080   # 200
$ docker ps --format '{{.Names}}: {{.Ports}}'
notes: 127.0.0.1:8080->80/tcp
```

Read the mapping **host-first**: `hostIP:hostPort -> containerPort`.
`-p 8080:80` publishes on *all* interfaces; the lab convention is
`-p 127.0.0.1:8080:80` — the M25 loopback discipline, container edition
(and identical in spirit to M27's Jupyter binding). `-P` (capital)
publishes every *exposed* port to random host ports — convenient for
tests, unreadable for services.

Names are stable handles: scripts should use `--name` (predictable) and
`docker rm -f <name>` (idempotent-ish re-run: remove-if-exists, then
start fresh). The auto-generated names are fine for experiments, useless
for automation.

## 5. The cleanup discipline

Containers and images accumulate — disk creep (M27 §10's pattern, new
mechanism). The deliberate toolkit:

```console
$ docker rm old_container              # remove one stopped container
$ docker rm -f notes                   # remove even if running (SIGKILL first)
$ docker container prune               # remove ALL stopped containers
$ docker rmi $(docker images -f dangling=true -q)   # untagged layer piles
$ docker system df                     # check before/after — evidence first
```

> ⚠️ **Prune discipline.** `docker system prune` removes *everything
> unused*: all stopped containers, dangling images, unused networks — and
> with `--volumes`, **named volumes holding your data**. On a shared
> machine it can delete a teammate's stopped work. The course rule:
> prefer targeted removal (`rm`/`rmi` by name), and if you ever prune,
> run `docker system df` first, list what will go, and never add
> `--volumes` casually. Volume removal is data deletion (Lesson 4).

---

## Key takeaways

- `docker run`'s flags are design decisions; `--rm -it` for one-shots,
  `-d` + `logs -f` for services, `--name` for anything scriptable.
- Containers **exit when their main process exits**; `stop` is SIGTERM-
  then-SIGKILL, `kill` is immediate (M18's signals, productized).
- Inspect with `ps -a`, `logs`, `exec`, `inspect` before ever removing —
  exited containers keep logs and layers for exactly that purpose.
- Publish ports host-first and on loopback for labs; prune rarely,
  targeted always, volumes never-by-accident.

## Check yourself

1. `docker run ubuntu` exits instantly. Give two ways to keep a
   container alive, and explain which you'd use for a *service*.
2. You attached to a container, hit Ctrl-C, and it stopped. What signal
   arrived, and what does that tell you about attach?
3. A teammate "fixed" a config inside a running container with `exec`,
   and the fix vanished after `docker rm` + re-run. Why?
4. What does `-p 127.0.0.1:5432:5432` guarantee that `-p 5432:5432`
   does not?

*Answers:* (1) keep a long-running main process (`-d` + a service
command) or attach a terminal (`-it ... bash`); a *service* wants `-d`
with a proper main process — a bash shell is a debugging aid, not a
service. (2) SIGINT into the container's main process; attach is a live
channel to the process, not a spectator seat. (3) `exec` writes to the
container's writable layer, which `rm` destroys; the durable fix is in
the image (or its config/volume). (4) that the host port is reachable
*only from the host itself* — loopback publication — rather than every
interface on the LAN.

Up next: [Lesson 3 — Dockerfiles and builds](03-dockerfiles-and-builds.md) —
turning M27's environment into an immutable artifact.
