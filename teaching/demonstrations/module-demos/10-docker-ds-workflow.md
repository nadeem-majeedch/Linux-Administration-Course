# Demo 10 — Docker & the DS Workflow: Containerized Jupyter

> **Session:** S27 · **Duration:** ~12 min · **Risk:** low (VM +
> Docker; loopback ports) · **Objective:** containers as *the
> reproducibility machine* — one image, pinned environment, data in a
> volume, port published — and the M21/M22 verbs supervising it.

## Prerequisites

- Demo VM with Docker working (`docker info` succeeds)
- A small dataset file for the volume (`~/demolab/data/sales.csv`)

## Setup

```console
$ mkdir -p ~/demolab/data && echo "ts,sensor,value" > ~/demolab/data/sales.csv
$ docker pull jupyter/base-notebook:latest        # before class — it's ~300 MB
```

## Procedure

**Step 1 — VM vs container, felt in the bones.**

```console
$ time docker run --rm jupyter/base-notebook:latest echo "hi from a container"
```

*Narration:* "Milliseconds — no BIOS, no boot, no guest kernel. A
container is *your* kernel hosting an isolated process. A VM boots a
whole computer; a container starts a process with walls."

**Step 2 — run the notebook server with a port and a volume.**

```console
$ docker run -d --name demo-jupyter \
    -p 8888:8888 \
    -v "$HOME/demolab/data:/home/jovyan/data:rw" \
    jupyter/base-notebook:latest
$ docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
$ docker logs demo-jupyter 2>&1 | grep -o 'http://127.0.0.1:8888/[^?]*token=[a-f0-9]*' | head -1
```

*Narration:* three flags, three old friends — `-p` publishes a *port*
(M21's doors), `-v` mounts a *volume* (M17's mounts, M13's permission
questions), `docker logs` is `journalctl` for containers (M24's
evidence habit). Every verb is one you own.

**Step 3 — the data really is shared.**

```console
$ ls ~/demolab/data                     # host view
$ docker exec demo-jupyter ls /home/jovyan/data   # container view — same bytes
$ echo "new row" >> ~/demolab/data/sales.csv
$ docker exec demo-jupyter tail -1 /home/jovyan/data/sales.csv
```

**Step 4 — destroy the container; the data survives.**

```console
$ docker rm -f demo-jupyter
$ ls ~/demolab/data                     # still here — the volume held it
```

*Narration:* "Containers are disposable by design; *data* lives in
volumes. Delete the container, keep the dataset — that division is why
the capstone's pipeline can be rebuilt nightly without touching the
data."

**Step 5 — the reproducibility punchline.**

*Narration over the still-running slides:* "Pinned base image + pinned
pip requirements + data in a volume = your exact environment on any
Linux box in one command. That is what 'reproducible' means
operationally — and it's the capstone's Docker track."

## Expected output

Container IDs/hashes vary; the shapes (port mapping in `docker ps`,
token in logs, volume parity) are stable. Token output varies — say so.

## Questions to ask

1. After step 1: "why is there no boot?" (shared kernel — no guest OS)
2. After step 4: "where would you put the *model checkpoints* if they
   must survive rebuilds?" (another volume — decide, don't guess)
3. "The notebook says connection refused from your host browser — which
   M21 rung, and which flag?" (listener/publish: `-p`)

## Common errors & recovery

- Port 8888 already bound (last session's Jupyter) → `ss -tlnp | grep
  8888`, kill the stale process or map `-p 8890:8888`
- Permission denied inside `/home/jovyan/data` (host uid vs container
  uid mismatch) — the classic volume gotcha; fix with a group/chown on
  the host (M13 verbs), and narrate that this is *the* known Docker
  sharp edge
- Docker daemon dead on the room image → `sudo systemctl start docker`;
  if the room can't run Docker at all, the [module lab's](../../../modules/M28-docker-containers/content/labs/README.md)
  non-Docker fallback path applies

## Recovery

`docker rm -f demo-jupyter` recovers from any container-state mess; the
volume data is host-side and untouched by any container failure.

## Cleanup (census)

```console
$ docker rm -f demo-jupyter 2>/dev/null
$ docker rmi jupyter/base-notebook:latest     # reclaim ~300 MB (say why)
$ rm -r ~/demolab                              # after the census
$ docker ps -a | wc -l                         # 1 = header only
```

## Optional extension

Write the 5-line Dockerfile that pins `pandas==<version>` into the
image, rebuild, and diff `pip freeze` inside the two containers — the
layer cache makes the rebuild instant, which *is* the caching lesson.
