# Lab 0 — Install Docker Engine in Your VM

> Module 28 · Unit 7 · Difficulty: Intermediate → Advanced
> Time: ~30 min · Environment: your Ubuntu VM (sudo required — a lab, not a habit)
> Prerequisites: [Lesson 1](../lessons/01-container-fundamentals.md); M14/M16 for the sudo discipline
> ⚠️ This is the one place in the module sudo is needed, and it's the
> *installation* — the M16 package-management procedure with a new repo.

## Part A — the official-repo install (15 min)

Ubuntu's own `docker.io` package works, but Docker's official repo gets
fresher Engine releases. The full procedure from
[docs.docker.com](https://docs.docker.com/engine/install/ubuntu/) —
uncompressed here so you *see* each step's purpose:

```console
# 1. Remove old/conflicting packages (a fresh VM may report none — fine)
$ sudo apt-get remove docker docker-engine docker.io containerd runc

# 2. Prerequisites: apt over HTTPS with keyrings
$ sudo apt-get update
$ sudo apt-get install -y ca-certificates curl gnupg

# 3. Docker's official GPG key (trust anchor for the repo)
$ sudo install -m 0755 -d /etc/apt/keyrings
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
$ sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 4. Add the repo (notice: signed-by the key above)
$ echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Install the engine
$ sudo apt-get update
$ sudo apt-get install -y docker-ce docker-ce-cli containerd.io \
      docker-buildx-plugin docker-compose-plugin
```

Steps 2–4 are pure M16 vocabulary — keyring, signed repo, refresh — now
for a third-party repo instead of Ubuntu's own.

## Part B — verify the engine (5 min)

```console
$ sudo systemctl enable --now docker      # M20 vocabulary: enable + start now
$ sudo systemctl status docker            # active (running)
$ sudo docker run --rm hello-world
```

`hello-world` pulling and printing its explanation proves the whole
chain: client → daemon → registry pull → runc run. `sudo docker run
--rm hello-world` again is instant — layers cached, Lesson 1 §4 witnessed
on your own disk.

## Part C — the `docker` group question (10 min)

Every `sudo docker` is a lesson in itself. By default the daemon's
socket (`/var/run/docker.sock`) is `root:docker` — so the Ubuntu
instructions offer:

```console
$ sudo usermod -aG docker $USER   # then log out/in (or newgrp docker)
$ docker run --rm hello-world     # no sudo — works
$ id | tr ',' '\n' | grep docker  # membership, for your lab-log
```

**Do it in your VM, and understand what you did.** The `docker` group is
*effectively root on the host*: anyone in it can talk to the daemon, and
the daemon can mount `/` into a container (M13's least-privilege echo —
this is Lesson 5 §2's daemon-boundary discussion, made physical). On a
single-student VM, group membership is the pragmatic choice; on a shared
server it's a decision to document, not default. Rootless mode exists
(`dockerd-rootless-setuptool.sh`, or Podman daemonless) — awareness is
the requirement, not installation.

## Done when

- [ ] `docker --version` and `docker compose version` both print
- [ ] `hello-world` ran twice (second time from cache) — log both
- [ ] `systemctl status docker` shows active; `is-enabled` shows enabled
- [ ] `docker` works without sudo, and one written line answers: *what
      did joining the `docker` group really grant me?*

Next: [Lab 1 — first containers](lab-01-first-containers.md).
