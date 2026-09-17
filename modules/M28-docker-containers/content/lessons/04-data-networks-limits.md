# Lesson 4 — Data, Networks, and Limits

> Module 28 · Unit 7 · Difficulty: Intermediate → Advanced
> Reading time: ~35 min · Lab: [Lab 2](../labs/lab-02-build-persist-debug.md) (volumes), [Lab 3](../labs/lab-03-jupyter-compose.md) (networks)
> Up next: [Lesson 5 — Compose, security, mistakes](05-compose-security-mistakes.md)

---

## 1. The writable layer is a lie you shouldn't believe

Lesson 1 §3: each container gets a thin writable layer on top of the
image. It *works* — until the container is removed, and with it every
byte written there. Demo it once (Lab 2 makes you) and the rule is
permanent:

> **Anything that must survive the container lives outside it.**

Docker's answer is volumes and bind mounts — two ways to punch a hole in
the container's filesystem and aim it at real storage.

## 2. Named volumes vs bind mounts

| | **Named volume** | **Bind mount** |
|---|---|---|
| Syntax | `-v pgdata:/var/lib/postgresql/data` | `-v /home/ds/lab/data:/data` |
| Managed by | Docker (location, lifecycle) | You (an exact host directory) |
| Good for | databases, state the *container stack* owns | datasets, configs, code under active edit |
| Populates from image? | yes, first use copies image content in | no — host wins, empty means empty |
| Portability | survives host reinstalls (Docker area) | tied to host paths |
| Team-safe? | yes — opaque to callers | only if the path is yours |

The DS mapping is natural: **databases and app state → named volumes;
your datasets, notebooks, and scripts → bind mounts.** A training run
that reads `~/projects/ds-capstone/data/` and writes `…/outputs/` binds
both directories; the container stays disposable, the data stays yours.
That's the "data volumes" pattern of every serious ML rig.

```console
$ docker volume create labdata
$ docker volume ls
$ docker volume inspect labdata        # Mountpoint: /var/lib/docker/volumes/...
$ docker run --rm -v labdata:/data alpine:3.20 sh -c 'echo hi > /data/x.txt'
$ docker run --rm -v labdata:/data alpine:3.20 cat /data/x.txt   # hi — survived
```

Two containers sharing one volume share a directory — the clean way to
move a model from a training container to a serving container without
`docker cp` gymnastics.

> ⚠️ **Removal = deletion.** `docker volume rm labdata` deletes the data.
> Not "unmounts", deletes. The course rule is M24's backup rule in
> Docker clothing: *list it* (`docker volume ls`), *name it exactly*,
> and never `volume prune` on a machine whose volumes you didn't create.

**SELinux/AppArmor aside (one line):** on hosts with labeled security,
bind mounts may need `:z`/`:Z` flags; plain Ubuntu VMs in this course
don't, but recognize the symptom (`Permission denied` on a bind-mounted,
world-writable dir) before reaching for `chmod 777` — the wrong medicine
(M25's lesson).

## 3. Container networking: the bridge you're standing on

Default setup: each container attaches to a private **bridge** network
(`docker0` on the host) with its own IP — the network namespace from
Lesson 1. Consequences, each of which is a debugging session saved:

- **Outbound just works** (SNAT via the host): containers can `pip
  install`, `git clone`, reach APIs.
- **Inbound requires publication** (`-p`, Lesson 2 §4) — that's why the
  curl to `127.0.0.1:8080` worked only *with* `-p`.
- **Container-to-container on a user-defined network** uses **service
  names as DNS**. This is the big one:

```console
$ docker network create labnet
$ docker run -d --name db --network labnet -e POSTGRES_PASSWORD=labpass postgres:16.4
$ docker run --rm --network labnet postgres:16.4 psql -h db -U postgres -c 'select 1;'
```

`-h db` resolved because **Docker runs an embedded DNS for user-defined
networks**: the name `db` is an A record. No IPs, no `/etc/hosts`
editing — names are the API between containers. (The default bridge has
no such DNS; user-defined networks are the everyday choice.)

`localhost` inside a container is the *container's* loopback — not the
host's, not a sibling's. "My app can't reach the database" is very often
`localhost` used where a network name (or published port) belonged.

## 4. Environment variables and configuration

`-e KEY=value` injects runtime configuration — the 12-factor habit, and
the container-native form of M25 §5's secrets rules:

```console
$ docker run --rm -e GREETING="hello ds" -e REPLICAS=4 alpine:3.20 env | grep -E 'GREETING|REPLICAS'
```

Conventions that matter:

- **Config via env, secrets via files.** Env vars leak casually —
  `docker inspect` shows them to anyone with docker access, they land in
  logs and `env` dumps. For API keys, mounts of secret files or Docker
  secrets (Compose) are the taught pattern; `-e API_KEY=…` is for lab
  trivials.
- Images provide *defaults* (`ENV` in the Dockerfile); `-e` overrides per
  run. Config = deployment-specific; image = environment — don't bake
  credentials into images (Lesson 5's mistake #1).

## 5. Resource limits: cgroups as a courtesy to colleagues

Untampered, a container can starve the host exactly like any process
(M18's runaway `train.py`). cgroups make the leash explicit:

| Flag | Limits | Typical use |
|---|---|---|
| `--cpus=2` | ~2 CPU cores' worth of time | leave headroom on shared boxes |
| `--memory=2g --memory-swap=2g` | 2 GB RAM, no swap overflow | contain OOM blast radius |
| `--pids-limit=100` | process count | fork-bomb brakes |

```console
$ docker run --rm --cpus=1 --memory=512m python:3.12-slim python3 -c "
import time, sys
start = time.time()
rows = []
try:
    while True:
        rows.append('x' * 10_000_000)
except MemoryError:
    print('capped at', len(rows), 'chunks')
"
```

The `--memory-swap=2g` detail is the practical one: set memory **equal**
to memory-swap and the container cannot borrow swap — it OOMs (exits
137) instead of grinding the host's disk. On shared university servers,
limits aren't optional hygiene; they're how you get invited back. `docker
stats` (Lesson 2) shows the live numbers; `docker inspect` shows the
ceilings.

---

## Key takeaways

- The writable layer dies with the container; **named volumes for state,
  bind mounts for your datasets and code**.
- Volume removal is deletion — list, name exactly, prune never-by-accident.
- User-defined networks give containers **DNS by service name**; inbound
  needs `-p`; `localhost` inside a container is the container's own.
- Config flows in via `-e` (secrets via mounted files, not env); cgroup
  flags (`--cpus`, `--memory`) are the shared-server courtesy.

## Check yourself

1. A Postgres container stored its data with no volume; after `rm` +
   re-run the tables are gone. Where did the rows live, and what one
   flag keeps them?
2. Why does `-v /home/ds/project:/app` make live-editing Python code
   possible without rebuilds — and what does that imply about testing
   *image* changes the same way?
3. Your API container reaches the database by `-h db`. What resolved
   that name, and would it work on the default bridge?
4. A container exits 137 under load. Decode the exit, name the flag
   that likely caused it, and the design choice that prevents it.

*Answers:* (1) in the container's writable layer, destroyed by `rm`;
`-v pgdata:/var/lib/postgresql/data` (first run populates from the
image, then persists). (2) the bind mount maps host files live into the
container's view — edits appear instantly; but the *image* (deps, base)
changes only via rebuild, so image-level changes still need
`docker build`. (3) Docker's embedded DNS on the user-defined network
`labnet`; the default bridge has no DNS — IP or `--link` legacy, so no.
(4) 137 = 128+9 (SIGKILL), typically the cgroup OOM killer firing;
`--memory` (and equal `--memory-swap`) caused the kill; chunking/
streaming the workload or raising the limit deliberately prevents it.

Up next: [Lesson 5 — Compose, security, and mistakes](05-compose-security-mistakes.md) —
stacks, hardening, and the ten ways it all goes wrong.
