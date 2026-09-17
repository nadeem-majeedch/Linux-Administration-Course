# Module 28 Quiz — Answer Key

> Grading guide: Sections A–C are factual; D accepts any wording that
> shows the *judgment*. Command answers graded on "would it work if
> typed", not exact form.

## Section A — fundamentals

**Q1.** Shares: the host **kernel** (one kernel for all containers).
Does not share: process view, network stack, mounts, hostname, users
(namespaces); and resource ceilings are enforced per-container
(cgroups). Namespaces draw the *view* boundary; cgroups draw the
*resource* boundary.

**Q2.** Each VM carries a full guest OS — its own kernel, init, and user
land — costing GBs and boot time. Containers are isolated *processes*
with no guest OS: their overhead is bins/libs plus the process itself,
so three stack comfortably in a fraction of the RAM.

**Q3.** The PID namespace gives the container a private process table in
which its main process is numbered 1 (it's the "init" of that view).
The host sees the same task at its real host PID. One process, two
namespace-relative labels.

**Q4.** Disk holds the layer stack once — both images share the base's
layers; only their divergent upper layers are distinct. `docker images`
reports logical per-image sizes that overlap; `docker system df` reports
the true totals (shared/reclaimable), which is why the images list
overstates real usage.

**Q5.** A tag (`:3.12-slim`) is a mutable pointer — upstream can re-push
it. A digest (`@sha256:…`) pins immutable content. The course pins
version tags by default (readable, still specific) and names digest
pinning the upgrade when publishing artifacts to others.

**Q6.** (1) daemon running? — `systemctl status docker`; (2) permission?
— plain `docker` vs `sudo docker` (socket group membership; Lab 0 §C);
(3) context/environment? — `DOCKER_HOST` pointing somewhere odd, or
Docker Desktop vs native mismatch.

## Section B — CLI & lifecycle

**Q7.** `--rm` auto-removes the container on exit — no stopped corpse,
no reclaimable writable layer. You *don't* want it when you need the
post-mortem: logs of a crashed job, `inspect` of the exit state, or
restarting the same container (`docker start`).

**Q8.** `stop` sends **SIGTERM**, waits a grace period (default 10 s,
`-t` to change), then **SIGKILL**; `kill` sends SIGKILL immediately.
Images whose entrypoint traps/forwards SIGTERM and exits promptly make
`stop` fast — one reason proper init handling is part of image quality.

**Q9.** `exec` processes and their writes live in the container's
writable layer, which `docker rm` destroys. The durable fix belongs in
the Dockerfile (a new layer/image build), in the pinned
`requirements.txt`, or in mounted config — not in a disposable runtime.

**Q10.** 137 = 128 + 9 → the process was killed by **SIGKILL** — in this
scenario the kernel's cgroup OOM killer enforcing the container's
`--memory` limit. (`docker inspect .State.OOMKipped` confirms.)

**Q11.** It publishes the port **only on the host's loopback
interface** — reachable from the host itself, unreachable from the LAN.
That's M25's loopback-only posture (and M27's Jupyter binding),
container edition.

**Q12.** The image's default command has no TTY-attached work to do, so
the main process exits and the container exits with it — the lifecycle
rule. `-it` (allocate TTY + keep stdin open), typically with `bash`/`sh`
as the command, gives the interactive session.

## Section C — images, data, networks

**Q13.** Good because layers after the *first invalidated* one are what
re-run: source edits (most frequent) sit *above* the pip layer, so the
expensive install stays cached. Move the COPY above pip and every code
edit invalidates the COPY *and every later layer* — full re-install each
edit. Cache hit = all inputs of a step unchanged; one miss invalidates
everything after it.

**Q14.** Layers are additive. Same-RUN removal happens *within* the one
layer, so the lists never enter the image. A separate later RUN adds a
whiteout on top — the files still occupy the earlier layer's bytes, and
`docker history` proves it.

**Q15.** The rows live in the container's writable layer
(`/var/lib/postgresql/data` as written by the container), which dies at
`docker rm` — a week of data for one removal. Fix:
`-v pgdata:/var/lib/postgresql/data` (named volume; first run populates
from the image, subsequent runs persist regardless of container
lifecycle).

**Q16.** (a) Named volume — opaque, Docker-managed, portable, survives
host churn; the DB owns its state's location. (b) Bind mount — the
dataset is *yours* (versioned, shared with M26 tooling), and live reads
from the host path are the whole point; `:ro` for raw. (c) Bind mount
(or `env_file`/mounted secret) — per-deployment config differs by host
and must be editable/reviewable; baking it in would rebuild images per
environment.

**Q17.** Docker's **embedded DNS** on user-defined networks: service
names get A records, so `db` resolves inside `api`. The default bridge
provides no name resolution (legacy container links only) — IP addresses
or nothing there.

**Q18.** Boundary 1: the network **namespace** — `0.0.0.0` inside the
container only spans the container's own interfaces; it has no route to
"the LAN" except through publication. Boundary 2: the **published
port's interface binding** — `-p 127.0.0.1:8899:8888` confines host
reachability to the host itself. Both text and flag required for full
credit.

## Section D — compose, security, synthesis

**Q19.** `depends_on` orders *container start*, not application
readiness — the DB process exists while Postgres still rejects
connections. Fix: `healthcheck` on the dependency (a real probe —
`pg_isready`) + `condition: service_healthy` on the dependent, so Compose
waits for *working*, not merely *running*.

**Q20.** Leaks: (1) image layers — `docker history`/`docker save`
extract it; (2) runtime inspection — `docker inspect`, `docker exec …
env` for anyone with Docker access; (3) registry pushes — the credential
ships with every pull; (4) logs/CI output — build args and command lines
get recorded. Alternative: mount secret *files* (tight permissions,
git-ignored) or use proper secrets management; env vars only for
non-sensitive config.

**Q21.** Survives `down`: images, bind-mounted host files, named
volumes — **and** only if `-v` is absent. Removed by plain `down`:
containers and the project network. Removed only by `down -v`: named
volumes (their data dies with them). So: images ✓, bind mounts ✓,
volumes ✓/✗ (plain vs `-v`), containers ✗/✗, network ✗/✗.

**Q22.** "`prune --volumes` bulk-deletes every unused volume on the
host — including teammates' stopped-project data and anything not
attached *right now*; volume deletion is data deletion with no undo.
The safe alternative is targeted `docker rm`/`rmi`/`volume rm` by exact
name for objects we created. Run `docker system df` first (and `docker
volume ls`) so we're deleting a known list, never a category."

Check understanding in practice: [challenges.md](challenges.md) ·
Symptoms: [../troubleshooting.md](../troubleshooting.md)
