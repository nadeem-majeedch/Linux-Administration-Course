# Lesson 5 — Docker Compose, Container Security, and the Ten Classic Mistakes

> Module 28 · Unit 7 · Difficulty: Intermediate → Advanced
> Reading time: ~35 min · Lab: [Lab 3](../labs/lab-03-jupyter-compose.md)
> Up next: [M29 — Web Servers, Databases & Deployment](../README.md)

---

## 1. The problem with long `docker run` lines

By Lesson 4 a realistic stack needs: an app container (build, env, port,
bind mounts), a Postgres container (volume, password, healthcheck), a
shared network — and someone to start them in order. As a shell script,
that's a 40-line incantation with the usual failure modes. As **Compose**,
it's a declarative file:

```yaml
# compose.yaml — the whole stack, reviewable in one screen
services:
  api:
    build: .                        # Dockerfile in this directory
    ports:
      - "127.0.0.1:8000:8000"       # loopback posture, M25 carry-over
    environment:
      DATABASE_URL: postgres://app:apppass@db:5432/appdb
    volumes:
      - ./outputs:/app/outputs      # bind mount: results land on the host
    depends_on:
      db:
        condition: service_healthy  # wait for real readiness, not just "started"
    cpus: 2
    mem_limit: 2g

  db:
    image: postgres:16.4           # pinned — course rule
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: apppass   # lab-only value; real secrets ≠ compose files
      POSTGRES_DB: appdb
    volumes:
      - pgdata:/var/lib/postgresql/data   # named volume: survives down/up
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d appdb"]
      interval: 5s
      timeout: 3s
      retries: 10

volumes:
  pgdata:                          # declared = managed by this project
```

The verbs (run from the file's directory):

```console
$ docker compose up -d            # build if needed, create network+volumes, start
$ docker compose ps               # this project's containers
$ docker compose logs -f api      # per-service logs
$ docker compose exec api bash    # into a running service
$ docker compose down             # stop + remove containers & network
$ docker compose down -v          # …and the named volumes — DATA LOSS flag
$ docker compose up -d --build    # rebuild after Dockerfile edits
```

What Compose adds over raw `run`: one **project** namespace (directory
name prefixes everything), a **private network with service-name DNS**
automatic, volumes declared and reusable across `down`/`up`, and
`depends_on` + `healthcheck` for honest startup ordering — `pg_isready`
waiting until Postgres *accepts queries*, not merely that the process
exists (the difference between "it started" and "it works", M24's
distinction, containerized).

**Config hygiene:** real deployments keep credentials out of the YAML
(the file gets committed; secrets don't) — `env_file:` referencing a
git-ignored `.env`, or mounted secret files. Lab files here use throwaway
values and say so.

## 2. Container security: the mental model

Containers are *processes on your kernel* (Lesson 1). Their trust
boundary is strong for accidents, weaker against kernel exploits — so the
practice is layered, and every layer is a course echo:

**Supply chain (M16's lesson, registry edition).** Official, pinned bases
only; `latest` is un-reproducible and unauditable. Minimal bases (`slim`)
shrink the attack surface *and* the image. Rebuild periodically so
security fixes arrive with new layers — a pinned image is reproducible,
not eternally secure.

**The daemon boundary (M13/M14's lesson).** The Docker socket
(`/var/run/docker.sock`) is effectively root on the host — anyone who can
talk to it can mount `/` into a container. That's what "being in the
`docker` group" really grants, and the honest least-privilege discussion
happens in Lab 0 §C. Rootless mode and Podman (daemonless) are the
design-level answers; know they exist and why (Lab 0's notes).

**Runtime hardening (what labs actually do):**

- Run as non-root (`USER 1000` in the Dockerfile) — a container escape's
  blast radius drops to a user's.
- Read-only root filesystem (`--read-only`) with explicit writable
  volumes for the few paths that need writes.
- `--cap-drop=ALL` (plus narrowly re-adding what's genuinely needed) —
  most containers need no kernel capabilities.
- `--security-opt=no-new-privileges:true` — no setuid escalation inside.
- Loopback port publication for anything lab-local (M25).

**Secrets (M25 §5 verbatim):** no secrets in Dockerfiles, images, env
command lines, or committed compose files. Env vars are readable via
`docker inspect` by everyone with Docker access; mounted files with
tight permissions are the taught default.

## 3. The ten classic mistakes (each a small story)

1. **Baking secrets into images.** `COPY .env /app/` puts the credential
   in every layer, forever — images are *extractable* (`docker save`,
   `docker history`). Fix: never copy secrets; mount or inject.
2. **`latest` everywhere.** Three machines, three different environments,
   one mystery. Fix: pin version tags (digests when publishing).
3. **State in the writable layer.** "It worked in the container" +
   `docker rm` = data gone. Fix: volumes for anything kept.
4. **`COPY . .` without `.dockerignore`.** Ships `.venv`, `.git`, 5 GB of
   `data/` into the image; breaks caching. Fix: ignore-file first (M26's
   ordering rule, Docker edition).
5. **Deps-after-code layering.** Every source edit re-downloads the
   world. Fix: manifest first, install, code last (Lesson 3 §3).
6. **Root in the container.** Fine in tutorials; on shared hosts it
   widens every blast radius. Fix: `USER`, cap-drop, no-new-privileges.
7. **Publishing `-p 8888:8888` on a shared/LAN host.** Your notebook
   server now has a public front door. Fix: `-p 127.0.0.1:…` (or compose
   ports as in §1).
8. **`depends_on` without healthchecks.** App boots before Postgres
   accepts connections; the stack "randomly" fails on cold start. Fix:
   `condition: service_healthy` + real probes.
9. **Untampered limits on shared machines.** One container eats the box;
   colleagues notice before you do. Fix: `--cpus`/`--memory` as the
   courtesy (Lesson 4 §5).
10. **`prune` with `--volumes`, casually.** The one command in Docker
    that deletes *data* in bulk. Fix: targeted `rm`/`rmi`; `docker
    system df` before any prune; volumes never pruned on shared hosts.

Every one of these is a debugging session you've had in another module,
wearing a container costume — which is the real takeaway: **the
admin instincts from M06–M25 transfer; Docker is the new vocabulary.**

---

## Key takeaways

- Compose turns a stack into a **reviewable file**: project namespace,
  automatic network with service DNS, declared volumes, health-checked
  ordering. `down -v` is the data-loss flag to fear.
- Security layers: pinned/slim supply chain, daemon-socket trust,
  non-root + caps + no-new-privileges at runtime, secrets as files.
- The ten mistakes are old admin sins in new syntax — your earlier
  modules already taught the fixes.

## Check yourself

1. Why does `depends_on` alone not prevent "cold-start connection
   refused", and what two compose keys fix it?
2. A teammate's Dockerfile contains `ENV API_KEY=sk-live-…`. List every
   way that value leaks, then the fix.
3. What does membership in the `docker` group effectively grant, and
   which earlier module's principle does that violate?
4. Your compose stack ran for a month; `docker compose down` then `up`
   — what's still there, and what needed `-v` to disappear?

*Answers:* (1) `depends_on` orders *start*, not *readiness*; add a
`healthcheck` on the dependency and `condition: service_healthy` on the
dependent. (2) leaks: image layers (`docker history`/`save`), anyone
with Docker access (`docker inspect`/`exec env`), registry pushes, CI
logs. Fix: remove from the image entirely; mount secret files at run
time, git-ignored. (3) effective root on the host (socket access →
mount `/` into a container); violates least privilege (M13/M14). (4)
images and any bind-mounted host files persist; named volumes persist
across `down` and only `down -v` removes them — which is why `-v` is a
deliberate, never-default flag.

**Next module:** [M29 — Web Servers, Databases & Deployment](../../../M29-web-servers-databases/README.md) —
nginx, Postgres, and TLS meet the Compose stack you just learned to run.
