# Module 28 Troubleshooting — Container Symptoms → Causes → Fixes

> Ten patterns, ordered by how often they hit real students. Each:
> **symptom → cause → diagnosis → fix → prevention**. The recurring
> theme: a container is a process (Lesson 1) — diagnose it with process
> instincts (M18) plus the Docker vocabulary.

## 1. `Cannot connect to the Docker daemon`

**Cause:** the CLI can't reach `dockerd` — service stopped, wrong
context, or your user lacks socket permission.

**Diagnosis:** `systemctl status docker` (running?); `docker context
ls` (right context? `DOCKER_HOST` set?); `ls -l
/var/run/docker.sock` (which group owns it — are you in it, `id`)?

**Fix:** `sudo systemctl start docker`; or `newgrp docker`/re-login
after `usermod -aG docker`; or unset the stray `DOCKER_HOST`.

**Prevention:** Lab 0's verify trio (`version`, `run hello-world`,
`systemctl is-enabled`) after any host change.

## 2. Container exits immediately ("my container keeps dying")

**Cause:** the main process ended — most often a foreground-only
misunderstanding: default CMD finished, an entrypoint script failed,
or config/env was missing and the app bailed.

**Diagnosis:** `docker ps -a` (the corpse and its exit code);
`docker logs <name>` (the actual error); `docker inspect -f
'{{.State.ExitCode}} {{.State.Error}}'` (137? 1? 125?).

**Fix:** depends on the corpse — supply missing `-e`/config; run the
real service command (`… server` not `… --help`); use `-d` for
long-runners and `logs -f` to watch. Rule: **the log always knows.**

**Prevention:** image CMD = a long-running command for service images;
`docker run --rm … --help` first to smoke-test the entrypoint.

## 3. `port is already allocated`

**Cause:** another container (or host process) owns the published host
port.

**Diagnosis:** `docker ps` — which container published it? Then M21
vocabulary on the host: `ss -tlnp | grep <port>` — a non-Docker
process may own it.

**Fix:** stop/remove the other container by name; or publish a
different host port (`-p 127.0.0.1:8081:80`); or free the host process
*if it's yours* (M18 signals discipline).

**Prevention:** a small port map for your lab services (documented in
`lab-log.md`) beats improvising port numbers.

## 4. `permission denied` on bind-mounted files

**Cause:** UID mismatch — the container's user (often root, or a fixed
UID like 1000) writes to a host directory owned by *you* (also 1000 —
or not), or the mount was flagged `:ro`.

**Diagnosis:** `docker exec <c> id` (who is the container?); `ls -ld
<hostdir>` (who owns the dir?); check your `docker run` line for `:ro`.

**Fix:** align deliberately — run the container as your UID
(`--user $(id -u):$(id -g)` for tool images that allow it), chown the
lab directory, or remove `:ro` if writes were intended. On SELinux
hosts it's `:z/:Z` — but on these Ubuntu VMs, check ownership first.

**Prevention:** images that `USER 1000` + host dirs owned by 1000
(this course's VM default) agree by construction; decide `:ro` at
mount time, not at crash time.

## 5. Data vanished after re-creating the container

**Cause:** state lived in the writable layer (or an *anonymous* volume
you didn't track) — `docker rm` was the eraser.

**Diagnosis:** `docker inspect -f '{{.Mounts}}' <name>` on the *old*
container if it still exists; your run command — was there a `-v`?
`docker volume ls` for stray anonymous volumes (`docker volume ls -f
dangling=true`).

**Fix:** if the old container exists, `docker cp` the data out; then
re-run *with* the named volume. If it's gone, it's gone — restore from
your backup (M24 Lesson 5's rule: untested backups aren't backups).

**Prevention:** any stateful service gets a **named** volume at first
run; C3's gauntlet exists so this mistake costs you nothing but pride.

## 6. Build fails mid-way after working yesterday

**Cause:** a layer re-ran after upstream invalidation and hit a changed
world — upstream image updated (mutable tag), a package version
vanished from apt/pip, or the network hiccuped.

**Diagnosis:** read the failed step's output *in the build log* (the
failing command is echoed); `docker build --progress=plain` for full
logs; check whether the failing layer is after a `FROM` (tag moved?)
or a `RUN apt/pip` (package drift?).

**Fix:** pin harder (`FROM python:3.12.7-slim`, exact pip pins — the
M27/M28 rule), `apt-get update` inside the same RUN, retry after
confirming the base digest. Fix *the pin*, not just the symptom.

**Prevention:** `latest`/floating tags are the root cause of most
"yesterday it built" mysteries — pins are reproducibility *and*
diagnosability.

## 7. Container has no network / can't resolve names

**Cause:** wrong network (default bridge has no service-name DNS),
`--network none` left over from a debug run, or a firewall/host VPN
interfering with the bridge.

**Diagnosis:** `docker inspect -f '{{.NetworkSettings.Networks}}'
<c>` (which network?); inside: `getent hosts <name>` (DNS working?);
`ip route` inside the container.

**Fix:** `docker network connect <net> <container>` to join the right
user-defined network (hot-pluggable!), or re-run with `--network`.
Host-level: `iptables`/VPN interference is an admin conversation, not
a container flag.

**Prevention:** user-defined networks by default (Compose does this
for you); the default bridge is for strangers.

## 8. Disk full: Docker ate the SSD

**Cause:** months of builds — dangling layers, stopped containers,
build cache, orphaned volumes — the M27 §10 creep, container-sized.

**Diagnosis:** `docker system df` then `docker system df -v` (the item
by-item truth); `docker ps -a` corpses; `docker images -f
dangling=true`.

**Fix (targeted, in order of safety):** remove stopped containers by
name → `docker container prune` (stopped only) → `docker rmi` the
dangling images → `docker builder prune` (build cache — rebuilds get
slower, that's the cost) → volumes only by exact name, never `prune`
on shared hosts.

**Prevention:** `--rm` for one-shots; named cleanup in lab scripts; a
weekly `docker system df` glance (the M27 `du` habit, Docker edition).

## 9. Compose: "cold start race" — API dies before DB is ready

**Cause:** `depends_on` ordered the *start*, not *readiness*; the API
crashed connecting to a Postgres that wasn't accepting connections yet.

**Diagnosis:** `docker compose ps` (states right after `up`);
`docker compose logs db` (pg ready when?) vs `logs api` (crashed
when?); the restart-loop pattern in api's log.

**Fix:** `healthcheck` on db + `depends_on: condition: service_healthy`
(Lesson 5 §1); a retry/backoff in the app's connection code is the
belt to that suspenders.

**Prevention:** every compose dependency that takes time to *become
ready* (databases especially) gets a real healthcheck — "running" is
not "working" (M24's distinction).

## 10. `exec`-fixed config reverts after restart

**Cause:** the fix lives in the writable layer; restart is fine but
`rm`+re-run rebuilds from image + mounted config, which never got the
fix.

**Diagnosis:** compare `docker exec <c> cat /path/to/config` against
the image's version (`docker run --rm --entrypoint cat <img> /path`)
— if they differ, you're container-patching.

**Fix:** move the fix to its honest home: the Dockerfile (baked
config), the mount (host-owned file), or `-e` (per-run config); rebuild
if image-level.

**Prevention:** treat `exec` as a *diagnostic* session by default —
write the durable fix where the next `up` will find it.

## Escalation table

| Layer | Evidence command | Hands off / escalate when |
|---|---|---|
| Daemon | `systemctl status docker`, `docker context ls` | Socket perms on shared hosts → admin |
| Container | `ps -a`, `logs`, `inspect .State.*` | Someone else's container — never stop/kill blind |
| Image/build | `docker build --progress=plain`, `history` | Registry/push issues → not in this course |
| Storage | `system df -v`, `volume ls` | Any volume you didn't create — never prune shared |
| Network | `inspect .NetworkSettings`, `getent hosts` | Host firewall/VPN conflicts → admin |
| Compose | `compose ps`, per-service `logs` | Shared stacks → coordinate before `down` |

Related modules: [M18](../../M18-processes-jobs-signals/content/troubleshooting.md)
(signals/exit codes), [M21](../../M21-networking-fundamentals/content/troubleshooting.md)
(ports/DNS fundamentals), [M24](../../M24-logs-journald-monitoring/content/troubleshooting.md)
(log-driven diagnosis), [M16](../../M16-package-management/content/troubleshooting.md)
(package drift).
