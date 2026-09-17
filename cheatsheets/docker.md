# 18 — Docker

> Learn it: [M28 — Docker & Containers](../modules/M28-docker-containers/content/README.md) ·
> Lookup, not understanding.

## The mental model

An **image** is a read-only template (layers, cached); a
**container** is a running (or stopped) instance of one; a
**registry** (Docker Hub et al.) stores images. Containers share
the host's kernel — VMs don't. That's why they start in
milliseconds and why "it works in my container" still needs your
volumes wired correctly.

## Lifecycle — the daily set

| Command | Purpose | Key options / examples |
|---|---|---|
| `docker pull python:3.12-slim` | fetch image | tag = version; `latest` is a moving target — pin |
| `docker images` | local images | — |
| `docker run IMAGE` | create + start | the big one, below |
| `docker ps` | running containers | `-a` includes stopped |
| `docker stop NAME` / `kill` | polite / immediate | `kill` = SIGKILL semantics |
| `docker rm NAME` | remove stopped container | `-f` = stop+remove ⚠️ |
| `docker exec -it NAME bash` | shell **into** a running container | `-i` stdin, `-t` tty |
| `docker logs -f NAME` | stdout/stderr of container | `--tail 50` |
| `docker inspect NAME` | full metadata JSON | `--format '{{.HostConfig.Memory}}'` |
| `docker system df` | disk usage by docker | — |
| `docker system prune` | reclaim (stopped, dangling) | ⚠️ **never with `--volumes` on shared machines** — that deletes data volumes |

## `docker run` — the options that matter

```console
$ docker run -d --name api \
    -p 10080:8000 \
    -v "$PWD/runs:/runs:ro" \
    -e API_KEY_FILE=/run/secrets/key \
    --memory 512m --cpus 1.5 \
    --restart unless-stopped \
    ds-api:1.4
```

| Option | Meaning |
|---|---|
| `-d` | detached (background) |
| `--name` | stop guessing auto-names |
| `-p HOST:CONTAINER` | publish port (host side is what the firewall sees) |
| `-v HOST:CONTAINER[:ro]` | **bind mount** a host dir (`:ro` = read-only) |
| `-v VOLUME:/path` | **named volume** (docker-managed) |
| `-e KEY=val` / `--env-file f` | environment config |
| `--memory` / `--cpus` | resource caps — politeness on shared machines |
| `--restart unless-stopped` | survive daemon restarts & crashes |
| `-it` | interactive + tty (shells) |
| `--rm` | remove on exit (short jobs) |
| `-u USER` | run as non-root user (course standard) |

## Images & builds

```dockerfile
FROM python:3.12-slim                 # pinned base
WORKDIR /app
COPY requirements.txt .               # deps first = layer cache for code edits
RUN python -m pip install -r requirements.txt
COPY . .
USER 1000                             # never ship as root
CMD ["python", "serve.py"]            # exec form, not shell form
```

| Command | Purpose |
|---|---|
| `docker build -t name:tag .` | build (`-f` other Dockerfile) |
| `docker history name:tag` | layer sizes |
| `docker push` / `docker login` | to a registry |

Build order trick: `COPY requirements.txt` before `COPY . .` makes
code edits reuse the installed-deps layer.

## Volumes: bind vs named

| | Bind mount | Named volume |
|---|---|---|
| path | exact host dir | docker-managed area |
| good for | dev source, reading datasets (`:ro`) | DB data, state |
| share with container | live — edits appear instantly | yes |
| backup story | it's just your dir | via volume tooling |

## Compose — multi-container in one file

```yaml
services:
  api:
    build: .
    ports: ["10080:8000"]
    environment: [ "DATABASE_URL=postgres://db:5432/ds" ]
    depends_on: [db]
  db:
    image: postgres:16
    volumes: [ "pgdata:/var/lib/postgresql/data" ]
volumes:
  pgdata:
```

| Command | Purpose |
|---|---|
| `docker compose up -d` | start the stack |
| `docker compose ps` / `logs -f` | state / output |
| `docker compose down` | stop (add `-v` to ⚠️ delete volumes) |

## Failure quick table

| Symptom | Cause → fix |
|---|---|
| `port is already allocated` | host port taken — `ss -tlnp`, change `-p` |
| file changes not visible | forgot `-v` mount, or edited the image's copy |
| `permission denied` on mounted file | uid mismatch — run with `-u` matching host uid |
| container exits instantly | it has no foreground job — check `docker logs`, add `-it sh` to poke |
| disk filling up | `docker system df`, prune images (⚠️ mind volumes) |
| data gone after `down` | it lived in the container layer, not a volume — mount next time |
