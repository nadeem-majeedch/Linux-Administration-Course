# Lab 3 — Jupyter in a Container, and a Compose Stack

> Module 28 · Unit 7 · Difficulty: Intermediate → Advanced
> Time: ~75 min · Environment: your VM, Docker installed
> Prerequisites: [Lessons 4–5](../lessons/05-compose-security-mistakes.md); M27's Jupyter lesson
> ⚠️ Ports on `127.0.0.1` only; the Postgres password here is a lab
> throwaway (`labpass`) and *never* the pattern for real credentials
> (Lesson 5 §2). All volumes named `lab3-*` or declared in compose.

Two plays of the same theme. First: Jupyter — the M27 workflow — running
from an image with your datasets mounted. Second: a full app+database
stack under Compose, with health-checked ordering. Together they're the
"reproducible ML environment" and the "API service" patterns of modern DS.

## Part A — a Jupyter image (15 min)

In `~/projects/ds-capstone/`, `Dockerfile.jupyter`:

```dockerfile
FROM python:3.12-slim

WORKDIR /work
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt jupyterlab==4.3.4 ipykernel

RUN useradd --create-home dsuser && chown -R dsuser /work
USER dsuser

EXPOSE 8888
CMD ["jupyter", "lab", "--ip=127.0.0.1", "--no-browser", "--ServerApp.token=labtoken"]
```

Build and run — note what's mounted and what isn't:

```console
$ docker build -f Dockerfile.jupyter -t ds-jupyter:1.0 .
$ docker run -d --name lab3-jupyter -p 127.0.0.1:8899:8888 \
    -v "$HOME/projects/ds-capstone:/work/project" ds-jupyter:1.0
```

Wait — the CMD binds `--ip=127.0.0.1` *inside the container*, but the
published port needs the service listening on the container's bridge
interface. This is the lesson: **inside** the container, `127.0.0.1` is
the container's own loopback; `-p` forwards the host port to the
*container's* interface. So the container-side bind must be `0.0.0.0`
(wide inside the isolated namespace), while **loopback discipline is
enforced at publication**: `-p 127.0.0.1:8899:8888`. Fix the CMD to
`--ip=0.0.0.0`, rebuild, re-run — and write the one-sentence
justification in your log: the namespace boundary (Lesson 1) is what
keeps `0.0.0.0`-inside safe here, the loopback publish is what keeps it
unreachable from the LAN.

```console
$ curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8899   # 30x — alive
```

Open `http://127.0.0.1:8899` (token `labtoken`), open
`project/notebooks/analysis.ipynb`, run it — same numbers as M26 Lab 3,
now from inside the image. Your datasets came from the bind mount; the
*pandas* that read them came from the image's pinned `requirements.txt`.
That split is the reproducible-ML pattern in one screenshot.

## Part B — the Compose stack: API + Postgres (30 min)

New directory `~/projects/ds-api/` with three files.

`Dockerfile`:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
      libpq5 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir fastapi==0.115.5 uvicorn==0.32.1 \
      psycopg[binary]==3.2.3 pandas==2.2.3
COPY api.py .
RUN useradd --create-home appuser
USER appuser
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

`api.py` — a tiny service that *reads* from the database:

```python
from fastapi import FastAPI
import psycopg, os, pandas as pd

app = FastAPI()
URL = os.environ["DATABASE_URL"]        # config via env, not baked in

@app.get("/regions")
def regions():
    with psycopg.connect(URL) as conn, conn.cursor() as cur:
        cur.execute("SELECT region, SUM(revenue) AS revenue FROM sales GROUP BY 1 ORDER BY 2 DESC")
        return dict(cur.fetchall())

@app.get("/health")
def health():
    return {"ok": True}
```

`compose.yaml` (Lesson 5 §1's, made real — paste, don't paraphrase):

```yaml
services:
  api:
    build: .
    ports: ["127.0.0.1:8000:8000"]
    environment:
      DATABASE_URL: postgres://app:labpass@db:5432/appdb
    depends_on:
      db:
        condition: service_healthy
    cpus: 2
    mem_limit: 2g

  db:
    image: postgres:16.4
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: labpass
      POSTGRES_DB: appdb
    volumes:
      - lab3-pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d appdb"]
      interval: 5s
      timeout: 3s
      retries: 10

volumes:
  lab3-pgdata:
```

Load real data, then start:

```console
$ printf 'region,revenue\nnorth,1200\nsouth,850\nnorth,300\n' > sales.csv
$ docker compose up -d db                # db first; watch the healthcheck settle
$ docker compose ps                      # db: (healthy)
$ docker compose exec db psql -U app -d appdb -c \
    "CREATE TABLE sales (region TEXT, revenue INT);
     COPY sales FROM '/docker-entrypoint-initdb.d/../dev/null';" 2>/dev/null || true
# simplest robust load — pipe the CSV:
$ cat sales.csv | docker compose exec -T db psql -U app -d appdb -c \
    "CREATE TABLE IF NOT EXISTS sales (region TEXT, revenue INT);"
$ python3 - <<'EOF'                      # tiny loader on the HOST (psycopg via venv not needed):
import csv, subprocess
rows = list(csv.DictReader(open('sales.csv')))
sql = "INSERT INTO sales (region, revenue) VALUES " + ",".join(f"('{r['region']}',{r['revenue']})" for r in rows) + ";"
subprocess.run(["docker","compose","exec","-T","db","psql","-U","app","-d","appdb","-c",sql], check=True)
EOF
$ docker compose up -d api && docker compose ps
$ curl -s http://127.0.0.1:8000/health
$ curl -s http://127.0.0.1:8000/regions | python3 -m json.tool
```

The chain to narrate in your log: host curl → published loopback port →
api container → *service-name DNS* (`db`) → Postgres in its container →
data in the **named volume**. Every lesson of this module in one
request.

## Part C — resilience and teardown (20 min)

```console
$ docker compose restart db && sleep 8 && curl -s http://127.0.0.1:8000/regions   # data survives (volume!)
$ docker compose down && docker compose up -d && sleep 10 \
    && curl -s http://127.0.0.1:8000/regions                                       # full stack re-runs
$ docker compose down && docker compose down -v                                    # NOW remove the volume
$ docker compose up -d && curl -s http://127.0.0.1:8000/regions                    # empty table — proven
$ docker compose down -v
```

The last two lines are the whole persistence lesson as a before/after:
volume present → data survives `down`; `-v` → data gone. You created
`lab3-pgdata`; deleting it is the experiment. One sentence in the log:
*which command would be catastrophic on a real server, and what rule
prevents it?*

## Done when

- [ ] Jupyter reached on `127.0.0.1:8899`; analysis ran with image-pinned
      pandas and host-mounted data; the ip-inside-vs-publish sentence
      written
- [ ] `/regions` returns the sums through the full container chain
- [ ] Data survives `restart` and full `down`/`up`; disappears only after
      `down -v` — transcript logged
- [ ] Stack torn down; `docker system df` shows the leftovers you chose
      to keep (images) vs removed (lab containers/volumes)

Next: [practice/quiz.md](../practice/quiz.md) — then
[M29](../../../M29-web-servers-databases/README.md) takes this stack to
nginx and TLS.
