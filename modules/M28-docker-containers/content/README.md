# Module 28 — Docker and Containers

> Unit 7 · The Data Science Stack · Difficulty: Intermediate → Advanced
> Time: ~8 hours total · Environment: your own VM with Docker Engine installed (Lab 0)
> Prerequisites: [M16](../../M16-package-management/README.md) (packages), [M20](../../M20-systemd-services/README.md) (services), [M27](../../M27-python-jupyter-data/README.md) (Python environments), [M26](../../M26-git-dev-workflows/README.md) recommended

Containers are how modern data science ships: a training job that runs on
your laptop runs identically on the university GPU server, on a cloud
worker, and on a colleague's machine — because the *environment itself*
became an artifact. This module takes you from "containers share the host
kernel — so what?" to building, persisting, networking, and composing
containers, with every Data Science example pinned to reproducibility.

**The one-sentence frame:** a container is an isolated *process* (M18's
namespaces and cgroups, productized); an image is its immutable blueprint;
Docker is the tooling that builds, runs, and ships both.

## What you'll be able to do

- Explain containers vs VMs precisely: what's shared, what's isolated, and why it matters
- Run, inspect, stop, and remove containers with the full `docker` core vocabulary
- Read and write Dockerfiles; build images; exploit layer caching deliberately
- Persist data with named volumes and bind mounts — and prove which survives what
- Map ports, pass environment variables, and connect containers on a network
- Orchestrate a multi-service stack (API + database) with Docker Compose
- Apply container security basics and avoid the classic footguns

## Files in this module

| Path | Contents |
|---|---|
| [lessons/01-container-fundamentals.md](lessons/01-container-fundamentals.md) | VMs vs containers, the shared kernel, images, layers, registries, architecture |
| [lessons/02-docker-cli-lifecycle.md](lessons/02-docker-cli-lifecycle.md) | The core CLI: run/ps/logs/exec/stop/rm; the container lifecycle; fore/background |
| [lessons/03-dockerfiles-and-builds.md](lessons/03-dockerfiles-and-builds.md) | Dockerfile instructions, layer caching, tagging, image hygiene, multi-stage awareness |
| [lessons/04-data-networks-limits.md](lessons/04-data-networks-limits.md) | Volumes vs bind mounts, container networking, ports, env vars, resource limits |
| [lessons/05-compose-security-mistakes.md](lessons/05-compose-security-mistakes.md) | Docker Compose for multi-service stacks; container security; the ten classic mistakes |
| [labs/README.md](labs/README.md) | Lab 0 (install) + three hands-on labs |
| [practice/quiz.md](practice/quiz.md) → [quiz-answers.md](practice/quiz-answers.md) | 22 questions, reasoning-graded key |
| [practice/challenges.md](practice/challenges.md) | Eight challenges, C1 (drills) → C8 (design) |
| [troubleshooting.md](troubleshooting.md) | Ten real-world container failure patterns |

## The safety contract (same as every module)

- **No arbitrary host data is ever touched.** Every mount in this module
  binds a directory *you created for the lab*; every volume is named and
  listed before removal; nothing teaches `docker system prune` without
  stating exactly what it deletes — and every destructive command is
  practiced on lab-created objects only.
- Containers run from official images (`python`, `postgres`) on the Docker
  Hub *official* namespaces, pinned to version tags — never `latest` in this
  course.
- Ports publish on `127.0.0.1` by default in labs; the M25 loopback posture
  carries over.
- The `sudo docker` vs `docker` group discussion is taught as the
  least-privilege lesson it is (M13/M14 echo) — including what the `docker`
  group implicitly grants.

## Suggested path

1. **Lab 0** — install Docker Engine in your VM (official repo, sudo, once)
2. Lessons 1–2, then **Lab 1** (first containers: run, inspect, clean)
3. Lesson 3, then **Lab 2** (build the M27 environment into an image; volumes)
4. Lessons 4–5, then **Lab 3** (Jupyter container; Compose API + Postgres)
5. Quiz; challenges C1–C4 minimum; troubleshooting read-through

Up next in Unit 7: [M29 — Web Servers, Databases & Deployment](../../M29-web-servers-databases/README.md) —
where the Compose stack of Lab 3 meets nginx and TLS.
