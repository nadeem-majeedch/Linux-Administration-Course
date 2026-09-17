# Lab 2 — Build, Persist, Debug: The Environment Becomes an Image

> Module 28 · Unit 7 · Difficulty: Intermediate → Advanced
> Time: ~60 min · Environment: your VM, Docker installed
> Prerequisites: [Lesson 3](../lessons/03-dockerfiles-and-builds.md), [Lesson 4](../lessons/04-data-networks-limits.md); M27's Lab 1 `requirements.txt`
> ⚠️ Volumes created here are named `lab2-*`; bind mounts point only at
> `~/projects/ds-capstone/` from M26/M27. Removals are by exact name.

The module's core transaction: take M27's pinned environment
(`requirements.txt`) and M26's analysis project, and bake them into an
image — then prove volumes persist, writable layers die, and `exec` is
for looking, not fixing.

## Part A — the image (20 min)

```console
$ cd ~/projects/ds-capstone            # from M26 Lab 3 (analysis.py, requirements.txt)
$ printf '.venv/\ndata/\noutputs/\n.git/\n.ipynb_checkpoints/\n' > .dockerignore
```

Create `Dockerfile` (Lesson 3 §5's, trimmed to this project):

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# deps first: the cache-heavy layer (changes only when requirements change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# code last
COPY analysis.py .

RUN useradd --create-home appuser
USER appuser

CMD ["python", "analysis.py"]
```

M26 Lab 3's `analysis.py` reads `data/raw/sales.csv` — for the image run
below we'll pass the path via bind mount, so first confirm the script's
assumption, then build and watch the cache work:

```console
$ docker build -t ds-capstone:1.0 .
$ docker build -t ds-capstone:1.0 .     # again — everything CACHED, seconds
$ touch analysis.py && docker build -t ds-capstone:1.0 .
$ docker images ds-capstone             # one image, same layers reused
```

The second build is the cache lesson; the third (after `touch`) shows
only the COPY-and-later layers re-running while `pip install` rides the
cache — Lesson 3 §3 witnessed in your own timings. Log the three
build-time tails.

## Part B — run it with your data (10 min)

The image contains code and environment; the data stays *yours* — bind
mounted (Lesson 4 §2's division of labor):

```console
$ docker run --rm -v "$HOME/projects/ds-capstone/data:/app/data:ro" \
    -v "$HOME/projects/ds-capstone/outputs:/app/outputs" ds-capstone:1.0
$ ls -la ~/projects/ds-capstone/outputs/    # the result landed on the HOST
```

`:ro` on the data mount is the point: the container can *read* your raw
data and *cannot* write it — M27's read-only raw discipline, enforced by
mount flags. The write mount for `outputs/` is the pipeline's whole
output contract.

## Part C — writable layer vs volume: the experiment (15 min)

Three rounds, one truth:

```console
# Round 1 — writes die with the container (writable layer)
$ docker run --name lab2-throwaway ds-capstone:1.0 sh -c 'echo ephemeral > /app/note.txt'
$ docker rm lab2-throwaway                # layer gone, note gone

# Round 2 — writes survive in a named volume
$ docker volume create lab2-notes
$ docker run --rm -v lab2-notes:/notes alpine:3.20 sh -c 'echo survives > /notes/x.txt'
$ docker run --rm -v lab2-notes:/notes alpine:3.20 cat /notes/x.txt   # survives

# Round 3 — the same volume, different container: sharing by mount
$ docker run --rm -v lab2-notes:/data alpine:3.20 cat /data/x.txt     # still survives
```

Cleanup, by exact name:

```console
$ docker volume rm lab2-notes             # this DELETES the data — it's lab scratch, say so
```

## Part D — exec: the debugging visit (10 min)

```console
$ docker run -d --name lab2-serve -v "$HOME/projects/ds-capstone/data:/app/data:ro" \
    ds-capstone:1.0 python3 -c "import time,sys; [print('alive', flush=True) or time.sleep(5) for _ in iter(int,1)]"
$ docker exec -it lab2-serve bash           # inside: who am I? what's here?
appuser@…:/app$ whoami && id                # appuser — USER took effect
appuser@…:/app$ python3 -c "import pandas; print(pandas.__version__)"
appuser@…:/app$ pip list | head             # the pinned env, inside the image
appuser@…:/app$ touch /tmp/seen-by-exec && ls /tmp/seen-by-exec
appuser@…:/app$ exit
$ docker restart lab2-serve && docker exec lab2-serve ls /tmp/seen-by-exec   # GONE — writable layer
$ docker logs --tail 2 lab2-serve
$ docker rm -f lab2-serve
```

`exec`'d changes live in the writable layer and die at restart — Lesson 2
§3's caveat, demonstrated. The env you *meant* to fix belongs in the
Dockerfile (image) or the config (volume/env) — never in a container
you'll throw away.

## Done when

- [ ] Three build timings logged, showing cache hit then partial
      invalidation
- [ ] Part B: output file visible on the **host**; `:ro` noted
- [ ] Part C: ephemeral-vs-volume transcript; volume removed by name
- [ ] Part D: `whoami` = appuser; the exec-write that didn't survive
      restart, with one line on where the durable fix belongs

Next: [Lab 3 — Jupyter & Compose](lab-03-jupyter-compose.md) — the full
stack.
