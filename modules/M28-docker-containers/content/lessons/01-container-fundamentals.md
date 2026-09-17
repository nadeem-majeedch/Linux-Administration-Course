# Lesson 1 — Container Fundamentals: VMs, Kernels, Images, Registries

> Module 28 · Unit 7 · Difficulty: Intermediate → Advanced
> Reading time: ~30 min · Lab: [Lab 0 — install](../labs/lab-00-install.md), [Lab 1](../labs/lab-01-first-containers.md)
> Up next: [Lesson 2 — the Docker CLI and container lifecycle](02-docker-cli-lifecycle.md)

---

## 1. The problem containers solve (and why a DS student cares)

In [M27](../../../M27-python-jupyter-data/README.md) you built a pinned
environment and proved it replicable: `requirements.txt`, freeze, recreate
as a second user. That contract works *within one machine and one libc*.
It quietly assumes a lot: the same base OS, the same system libraries, the
same Python build, the same CUDA driver layout. The moment your analysis
must run on the professor's GPU server, a journal reviewer's machine, or a
cloud worker, "pip pinned" stops being the whole story.

Containers close the gap by packaging **code + runtime + system
dependencies** into one immutable artifact — the *image* — and running it
in an isolated process. The unit of reproducibility stops being a text
file and becomes a bit-for-bit blueprint: `docker run` on any Linux host
with the same image executes against the same environment, down to the
system libraries. This is why "works on my machine" became a solvable
problem, and why every modern ML platform (training clusters, cloud
notebooks, job schedulers) ships workloads as containers.

## 2. Virtualization vs containers: what each isolates

You've run an Ubuntu VM all course ([M04](../../../M04-installing-linux-vms/README.md)),
so you already own one half of the comparison:

```text
  VM approach                    Container approach
┌─────────┬─────────┐         ┌─────────┬─────────┐
│  App A  │  App B  │         │  App A  │  App B  │
├─────────┼─────────┤         ├─────────┼─────────┤
│ libs+   │ libs+   │         │ bins/   │ bins/   │
│ bins A  │ bins B  │         │ libs A  │ libs B  │
├─────────┴─────────┤         ├─────────┴─────────┤
│  Guest OS (full!) │         │  (no guest OS)    │
├───────────────────┤         ├───────────────────┤
│  Hypervisor       │         │ Container engine  │
├───────────────────┤         │  (Docker)         │
│  Host OS          │         ├───────────────────┤
├───────────────────┤         │  Host OS          │
│  Hardware         │         ├───────────────────┤
└───────────────────┘         │  Hardware         │
                              └───────────────────┘
```

- A **VM** virtualizes *hardware*: each guest runs a complete OS on a
  hypervisor (VirtualBox, KVM). Strong isolation, total generality — and a
  full OS's RAM, disk, and boot time per instance.
- A **container** virtualizes at the *OS level*: every container is just a
  regular process on the **host kernel**, with the kernel enforcing
  isolation. No guest OS, so containers start in milliseconds, consume
  little beyond their workload, and pack far more densely.

The precise claim to remember: **containers share the host kernel and
isolate the view of the system; VMs isolate everything including the
kernel.** Consequences worth knowing:

| Property | VM | Container |
|---|---|---|
| Boot time | tens of seconds | milliseconds |
| Overhead per instance | GBs (guest OS) | MBs (bins/libs only) |
| Kernel | its own, per guest | host's, shared |
| Can run Windows guest on Linux host? | yes | no (containers are OS-native) |
| Isolation strength | hardware boundary | kernel-enforced boundary (strong, weaker than VM) |

That last row is the honest caveat: because all containers share one
kernel, a kernel vulnerability is common surface to all of them — one of
several reasons container security (Lesson 5) exists as a discipline.

## 3. How isolation actually works (concepts from your own toolchain)

Two Linux kernel features — which you have *already used indirectly* — do
the work:

- **Namespaces** give a process a private *view*: its own PID space (PID 1
  inside the container isn't the host's PID 1), its own network stack (its
  own `eth0` and ports — M21's `ss` inside a container shows a different
  world), its own mounts, its own hostname, users.
- **Control groups (cgroups)** cap and account *resources*: this container
  gets 2 CPUs and 2 GB of memory, no more (M18's `nice` was the gentle
  cousin; cgroups are the enforcement mechanism).

A container, then, is **not a little machine** — it's an ordinary host
process wearing namespaces as blinders and cgroups as a leash. When you
`docker run ubuntu ps aux`, you see the container's private PID view; the
host's `ps aux` (M18) sees the same process at its real host PID. That
two-views-one-process fact explains most container debugging you'll ever
do.

A third piece rounds it out: **union filesystems** stack read-only image
layers with one writable layer per container — which is exactly why
(Lesson 2) writing inside a container then deleting the container deletes
the writes.

## 4. Images, layers, and the registry model

An **image** is an immutable template: a stack of **layers**, each layer
the file-system diff produced by one build step. Two properties do all the
work:

1. **Layers are shared.** Ten images built `FROM python:3.12-slim` share
   that base's layers on disk — one copy, not ten. `docker images`
   shows logical sizes; `docker system df` shows how much is truly
   duplicated.
2. **Layers are content-addressed.** A layer's identity is a hash of its
   contents. Rebuilding with an unchanged step *reuses* the cached layer
   byte-for-byte (the engine of build speed in Lesson 3), and identical
   content anywhere is stored once.

A **registry** (Docker Hub by default, or a private one — the university
may run GitLab's) stores images and serves them on `docker pull`/`push`.
The naming grammar tells you everything:

```text
python:3.12-slim
└──┬──┘ └───┬───┘
 image  tag      ← docker.io/library/python implied (official namespace)
gitlab.example.com:5050/team/project:1.4.2
└──────────────┬──────────────────────┘ └──┬──┘ └┬──┘
     registry (with port)             path   tag
```

**Tags are mutable labels; digests are immutable.** `python:3.12` can be
re-pushed and change under you; `python@sha256:…` is pinned forever. The
course rule — **pin version tags, never `latest`** — is the registry-level
echo of M27's `requirements.txt` pins, and digest-pinning is the
publish-a-reproducibility-artifact upgrade. One habit from M16 carries
verbatim: you only ever *pull* here; pushing to a registry is not required
in this course (build locally, run locally).

## 5. Docker's architecture: client, daemon, runtime

Three moving parts, and knowing which is which turns errors into
directions:

- **The CLI (`docker`)** — a client. It doesn't run containers; it talks
  to…
- **The daemon (`dockerd`)** — the engine that builds images, manages
  containers/volumes/networks. The `Cannot connect to the Docker daemon`
  error means *client can't reach daemon* — service not running, or (the
  classic) your user lacks permission to its socket (Lab 0 §C).
- **The runtime (containerd/runc)** — the lowest layer: given a prepared
  spec, runc actually forks the process with namespaces and cgroups set.

On your Ubuntu VM all three are native Linux processes. (Docker Desktop on
macOS/Windows hides a Linux VM underneath — which is itself the
VM-vs-container lesson, embodied.)

## 6. Vocabulary check

| Term | One line |
|---|---|
| Image | Immutable, layered template for containers |
| Container | A process running from an image, isolated by namespaces/cgroups |
| Layer | Content-addressed FS diff; shared between images |
| Tag | Mutable label on an image (`:3.12-slim`); digest = immutable pin |
| Registry | Server storing/serving images (Docker Hub, GitLab registry) |
| Volume | Docker-managed persistent storage (Lesson 4) |
| Dockerfile | Recipe that builds an image |
| Compose | Declarative multi-container orchestration (Lesson 5) |

---

## Key takeaways

- Containers are **isolated host processes** (namespaces = view, cgroups =
  resources) — not VMs; no guest OS, near-instant start, shared kernel.
- Images are **immutable layer stacks**; layers are shared and
  content-addressed, which is why pulls, builds, and disk usage behave as
  they do.
- **Pin version tags** (digests when publishing) — mutable tags are the
  registry-world equivalent of unpinned `requirements.txt`.
- CLI → daemon → runtime: permission errors are daemon-socket problems,
  not container problems.

## Check yourself

1. Why can a container start in milliseconds while a VM takes a minute?
2. Inside a container, `ps aux` shows PID 1 as your app. On the host, the
   same process is PID 5432. Which kernel feature produces each number?
3. Your teammate's `pip`-pinned project runs on their laptop but fails on
   the cluster with a missing system library. Which gap does an image
   close that `requirements.txt` cannot?
4. What is the difference between `python:3.12` and
   `python@sha256:abc…`, and which does this course pin by default?

*Answers:* (1) no guest OS to boot — the process just forks against the
host kernel with namespaces applied. (2) the PID namespace produces the
container-private view; the host sees the real PID — same process, two
namespaces' worth of labeling. (3) system-level dependencies (libc
versions, native libraries, OS packages) that pip never managed; the
image includes the whole user-space stack. (4) tag = mutable pointer,
digest = immutable content pin; the course pins version tags in labs and
treats digests as the publishing-grade upgrade.

Up next: [Lesson 2 — the Docker CLI and container lifecycle](02-docker-cli-lifecycle.md) —
vocabulary as commands.
