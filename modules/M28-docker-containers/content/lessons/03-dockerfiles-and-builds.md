# Lesson 3 — Dockerfiles, Builds, and Layer Caching

> Module 28 · Unit 7 · Difficulty: Intermediate → Advanced
> Reading time: ~35 min · Lab: [Lab 2](../labs/lab-02-build-persist-debug.md)
> Up next: [Lesson 4 — data, networks, and limits](04-data-networks-limits.md)

---

## 1. The Dockerfile is the environment, written down

Everything M27 packed into `requirements.txt` plus the OS around it —
base system, system libraries, Python itself — becomes a text file.
A **Dockerfile** is a sequence of instructions; each instruction produces
one **layer** in the image built from it.

```dockerfile
# A minimal, honest Python analysis image
FROM python:3.12-slim          # 1. the base layer stack you inherit

WORKDIR /app                   # 2. set the working dir (created if missing)

COPY requirements.txt .        # 3. copy ONLY the dependency manifest first
RUN pip install --no-cache-dir -r requirements.txt

COPY analysis.py .             # 4. then your code — which changes most often
CMD ["python", "analysis.py"]  # 5. the default command
```

Build and run it:

```console
$ docker build -t sales-analysis:1.0 .
$ docker run --rm sales-analysis:1.0
```

`-t name:tag` names the result (tag defaults to `latest` — which is why
this course writes explicit tags). The trailing `.` is the **build
context**: the directory whose contents the builder may COPY — one reason
`.dockerignore` exists (§5).

## 2. The instruction set you actually need

| Instruction | Does | Notes |
|---|---|---|
| `FROM` | base image to inherit | official, version-pinned bases only |
| `WORKDIR /app` | set/CREATE working dir | prefer over `RUN cd` (persists for all later steps) |
| `COPY src dst` | copy files from context into layer | what you *name* is what ships |
| `ADD src dst` | COPY + tar-extract + URL fetch | prefer COPY; fewer surprises |
| `RUN` | execute a command **at build time** | install deps; each RUN = one layer |
| `ENV K=V` | environment variable baked into image | config defaults, PATH fixes |
| `ARG` | build-time-only variable | `--build-arg`; not present at run time |
| `EXPOSE 8000` | documentation: the port the app listens on | no publishing (that's `-p`/compose) |
| `USER 1000` | run as non-root from here on | security default; Lesson 5 |
| `CMD` | default command, **overridable** at `run` | one per image (last wins) |
| `ENTRYPOINT` | fixed executable, CMD becomes args | CLI-tool images; less common in DS work |

The `CMD`-override mechanic ties to Lesson 2: `docker run sales-analysis:1.0 python3 repl.py`
replaces CMD wholesale. And the `RUN`-vs-`CMD` distinction is the
build/run boundary: **RUN happens once, on the builder, into the image;
CMD happens every run, inside the container.**

## 3. Layer caching: the engine of build speed

Every instruction's layer is cached; a step re-executes only if *its
inputs changed* — the instruction itself, the files it copies, or any
**earlier** layer. The cache is therefore an argument for ordering:

```text
COPY requirements.txt .      ← changes only when deps change   (rare)
RUN pip install -r ...       ← invalidated only by the line above
COPY analysis.py .           ← changes every edit             (frequent)
```

Edit `analysis.py` ten times: the expensive `pip install` layer survives
ten rebuilds (~seconds, from cache), only the cheap COPY re-runs. Put the
`COPY analysis.py .` *before* the pip install and every code edit pays
the full install again — the classic Dockerfile mistake, and the
roadmap's "ordering puzzle": **copy the thing that changes least, first.**

Two cache-hygiene corollaries:

- **One `apt`/`pip` layer, then clean in the same layer.** Removing files
  in a *later* layer hides them but doesn't shrink the image — the files
  live on in the earlier layer. `rm -rf /var/lib/apt/lists/*` must ride
  in the *same* RUN that downloaded them.
- **`.dockerignore`** (like `.gitignore`, at the context root) keeps
  `.venv/`, `data/`, `.git`, outputs out of the context — smaller
  uploads, and it prevents `COPY . .` from shipping junk that
  invalidates caches. The M26/M27 ignore-categories carry over.

## 4. Image hygiene: size and reproducibility

DS images grow fast; the two big levers:

- **Slim bases.** `python:3.12-slim` (Debian, minimal) vs the full
  `python:3.12` (~1 GB of extras). `alpine` variants are smaller still but
  use musl libc — native wheels (`pandas`, `numpy`) can break or
  rebuild-from-source; for DS, `slim` is the pragmatic default.
- **`--no-cache-dir`** on pip and no apt-lists left behind (above).

**Multi-stage builds** (concept, awareness): a *builder* stage compiles
with the heavy toolchain, and a final `FROM` copies only the artifacts
into a slim base — build tools never ship. For pure-wheel DS workloads
you rarely need it; for anything compiling native extensions it halves
image size. Recognize the pattern; write it when a build output must
outlive its build tools.

**Reproducibility, layered:** base pinned by tag (Lesson 1 §4) + `pip
install -r requirements.txt` with exact pins (M27) + your code copied
last = an image that reconstructs the environment *including the OS*.
Digest-pin the base and the image becomes publish-grade. This is the
"reproducible ML environment" in its strongest form: not a lockfile, a
blueprint.

## 5. A DS-grade image, annotated

```dockerfile
FROM python:3.12-slim

# OS deps some wheels need (slim lacks them); clean in the SAME layer
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# deps first: the cache-heavy layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# code last: changes most
COPY analysis.py .

# run as a real user, not root (Lesson 5)
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000
CMD ["python", "analysis.py"]
```

Everything in it maps to a lesson in this course: pinned base (M27), one
layer per download + clean (this lesson), non-root USER (M13's
least-privilege), documented port (M21), default command (M20's
service-thinking).

---

## Key takeaways

- Each Dockerfile instruction is a **layer**; the image is the stack.
- Order by **change frequency**: deps before code, or every edit re-pays
  the install.
- Clean inside the same layer that dirtied it; `.dockerignore` before
  `COPY . .` exists at all.
- Pin the base, pin the requirements, run as non-root — the image is the
  strongest reproducibility artifact this course produces.

## Check yourself

1. Your build re-runs `pip install` on every code edit. Which lines are
   in the wrong order, and why exactly does the cache miss?
2. Why does `RUN pip install X && rm -rf ~/.cache` shrink the image while
   `RUN pip install X` then `RUN rm -rf ~/.cache` does not?
3. What does `EXPOSE 8000` actually do, and what publishes a port?
4. `latest` was just re-pushed upstream. Who notices first — you or your
   CI — and why is that question itself the problem?

*Answers:* (1) the `COPY analysis.py .` sits above the pip layer; code
edits invalidate that COPY, and every *following* layer (the install)
misses with it. Deps first, code last. (2) layers are additive — the
second RUN's "removal" only adds a whiteout on top; the cached download
still occupies the earlier layer. Same-layer commands share one layer.
(3) it's metadata — documentation for humans and `-P`; publication is
`-p`/`ports:` at run time. (4) whoever pulls next — and the point is
that "next pull changes your environment silently" means mutable tags
were the wrong pin from day one.

Up next: [Lesson 4 — data, networks, and limits](04-data-networks-limits.md) —
making containers honest about state.
