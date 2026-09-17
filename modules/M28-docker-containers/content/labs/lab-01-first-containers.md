# Lab 1 — First Containers: Run, Inspect, Understand, Clean

> Module 28 · Unit 7 · Difficulty: Intermediate → Advanced
> Time: ~45 min · Environment: your VM, Docker installed ([Lab 0](lab-00-install.md))
> Prerequisites: [Lesson 2](../lessons/02-docker-cli-lifecycle.md)
> ⚠️ Every object this lab creates is named `lab1-*` or disposable with
> `--rm`; every removal targets exactly what this lab created.

The core CLI as reflexes. By the end, `run/ps/logs/exec/stop/rm` should
feel like M18's process tools wearing containers — because they are.

## Part A — one-shots and the exit rule (10 min)

```console
$ docker run --rm python:3.12-slim python3 --version    # auto-removed on exit
$ docker run python:3.12-slim python3 -c "print('gone in a second')"
$ docker ps -a                            # the --rm one is NOT here; prove it
$ docker run ubuntu:24.04                 # instant exit — why? (default cmd, no TTY)
$ docker ps -a                            # ...but THIS one left a corpse; find it
```

That pair of corpses-vs-clean-exits is Lesson 2 §1's rule witnessed:
containers exit when their main process exits, and `--rm` decides whether
a body remains. Remove the corpse by the name `ps -a` showed you:

```console
$ docker rm <name-from-ps>                # exactly the one you created
```

## Part B — a long-runner, inspected like a service (15 min)

```console
$ docker run -d --name lab1-web -p 127.0.0.1:8080:80 nginx:1.27-alpine
$ docker ps                               # STATUS "Up …", PORTS mapping
$ curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8080   # 200
$ docker logs lab1-web                    # nginx's access log — your curl is in it
$ docker top lab1-web                     # processes inside, host-side view
$ docker exec lab1-web sh -c 'hostname; ls /usr/share/nginx/html'   # inside, no TTY needed
$ docker inspect -f '{{.NetworkSettings.IPAddress}}' lab1-web       # its bridge IP
```

Two views, one truth: the container's IP exists *on the docker bridge*
(your host reached it via the published port, not that IP). Then the
negative test — the loopback posture (M25 carry-over):

```console
$ ip -brief addr show                     # your VM's LAN IP, e.g. 192.168.x.x
$ curl -s -m 3 -o /dev/null -w '%{http_code}\n' http://<that-ip>:8080 || echo "refused — as intended"
```

Refused, because publication was `127.0.0.1:8080` — Lesson 2 §4's
host-first reading, proven.

## Part C — signals and lifecycle states (10 min)

```console
$ docker stop lab1-web && docker ps -a | grep lab1-web   # Exited (0) — SIGTERM, graceful
$ docker start lab1-web && docker ps | grep lab1-web     # same container, re-run
$ docker logs --tail 3 lab1-web               # logs persist across restart
$ docker restart lab1-web                     # stop+start in one verb
```

Then the SIGTERM-vs-SIGKILL distinction with a container that ignores
SIGTERM (the honest way to see why `kill` exists):

```console
$ docker run -d --name lab1-stubborn alpine:3.20 sh -c \
    'trap "" TERM; sleep 300'                 # TERM trapped = ignored
$ time docker stop -t 3 lab1-stubborn         # waits 3s, then SIGKILL
$ docker inspect -f '{{.State.ExitCode}}' lab1-stubborn    # 137 = 128+9 (M18 echo)
$ docker rm lab1-stubborn
```

Graceful exit 0 vs forced 137: two stop stories in one transcript.

## Part D — cleanup, deliberately (5 min)

```console
$ docker stop lab1-web && docker rm lab1-web
$ docker ps -a                                # lab1-* gone; anything else, note it — leave it
$ docker images                               # python/nginx/alpine layers remain — useful cache
$ docker system df                            # the honest ledger (C[ontainers]=0 for this lab)
```

**Leave the images** — later labs rebuild from them. This is the
targeted-cleanup discipline: remove *your* containers by name, keep the
shared layer cache, and never reach for `system prune` to tidy up
(Lesson 5's mistake #10).

## Done when

- [ ] Part A: `--rm` container absent from `ps -a`, default-cmd corpse
      found and removed by name
- [ ] Part B: 200 on loopback; your curl visible in `docker logs`; LAN
      curl refused and explained in one line
- [ ] Part C: graceful `Exited (0)` vs `137` with the trapped-TERM
      experiment recorded
- [ ] Part D: only lab1-* removed; `docker system df` output saved

Next: [Lab 2 — build, persist, debug](lab-02-build-persist-debug.md) —
M27's environment becomes an image.
