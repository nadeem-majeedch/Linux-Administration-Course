# Lab 2 — The Deployment Lab: nginx → API → PostgreSQL

> Module 29 · Unit 7 · Difficulty: Advanced
> Time: ~75 min · Environment: your own VM
> Prerequisites: [Lab 1](lab-01-nginx-postgres.md) (nginx block,
> `salesdb` + `appuser` live)
> ⚠️ Loopback/NAT only. The DB password lives in an `api.env` (600,
> git-ignored) — never in code, never in the unit file. Config
> changes: backup → test → reload → verify, always.

The course's assembled artifact: a data product deployed as
services — static front, API middle, database beneath — verified
hop by hop and documented in a runbook. This is the capstone's
rehearsal.

## The app — provided, minimal (10 min)

`~/lab29/app/main.py` — a FastAPI app that queries the database:

```python
import os
from fastapi import FastAPI
import psycopg2

app = FastAPI()

def db():
    return psycopg2.connect(os.environ["DATABASE_URL"])

@app.get("/health")
def health():
    try:
        db().close(); return {"status": "ok", "db": "up"}
    except Exception as e:
        return {"status": "degraded", "db": str(e)[:80]}

@app.get("/api/sales/summary")
def summary():
    with db() as conn, conn.cursor() as cur:
        cur.execute("SELECT region, SUM(amount) AS total FROM sales GROUP BY region ORDER BY total DESC")
        return [{"region": r[0], "total": float(r[1])} for r in cur.fetchall()]
```

```console
$ python3 -m venv ~/lab29/app/.venv && ~/lab29/app/.venv/bin/pip install fastapi uvicorn psycopg2-binary
```

(The venv: [M27](../../../M27-python-jupyter-data/README.md)'s
pattern. The DB URL: *not in this file* — `os.environ` reads what
the unit injects.)

## Phase 1 — the app service (20 min)

`api.env` (chmod 600, git-ignored):

```text
DATABASE_URL=postgresql://appuser:lab-only-CHANGE-ME@127.0.0.1:5432/salesdb
```

The unit from [Lesson 4 §2](../lessons/04-deployment-tls.md)
(`EnvironmentFile`, `Restart=on-failure`, `MemoryMax`). Then:

```console
$ systemctl --user daemon-reload && systemctl --user enable --now api.service
$ curl -s http://127.0.0.1:8000/health          # direct: {"status":"ok","db":"up"}
$ curl -s http://127.0.0.1:8000/api/sales/summary | head -c 200
```

Both curls recorded. **The resilience drill:** `kill` the app's
uvicorn process (M18's preview→TERM), watch `systemctl --user
status` show the `Restart=on-failure` resurrection within seconds,
curl health again. Self-healing, witnessed.

## Phase 2 — the proxy (15 min)

Extend Lab 1's server block with the `/api/` location
([Lesson 2 §4](../lessons/02-nginx.md)) — decide and *comment* the
trailing-slash form — then backup → edit → `nginx -t` → reload:

```console
$ curl -s http://dashboard.test/api/sales/summary     # through the front door
$ curl -s http://dashboard.test/                      # static still works
$ curl -s -o /dev/null -w '%{http_code}\n' http://dashboard.test/api/health
```

**The 502 drill:** `systemctl --user stop api.service` → curl →
502 (quote the access-log line and the error-log line) → start →
200. The signature failure of proxied stacks, induced and read.

## Phase 3 — the database connection chain (10 min)

Prove the full path in one request, then decompose it:

```console
$ curl -s http://dashboard.test/api/sales/summary | python3 -m json.tool | head -12
$ sudo -u postgres psql salesdb -c "SELECT * FROM pg_stat_activity WHERE usename='appuser';"
```

The `pg_stat_activity` row: the app's connection, visible from the
database side — the request path (Lesson 1 §4) closed as evidence.
Then the negative test: stop postgres (`systemctl stop
postgresql`), curl (degraded health / 502), read the *app's*
journal traceback, start postgres, recover. Every hop's failure
mode has now been seen.

## Phase 4 — the runbook (15 min)

`~/lab29/runbook.md` — Mini-Project D's form, for this stack.
Required sections, each with the *actual commands*:

1. **Start/stop the stack** — postgres (system), api (user),
   nginx (system); the order matters and is stated.
2. **Health check** — the three curls (static, `/api/health`
   through proxy, direct app) with expected outputs.
3. **Read the logs** — the three §5 sources and which question
   each answers.
4. **Restore the DB** — the Lab 1 B5 procedure, scratch-first,
   count-verified.
5. **Rollback config** — the nginx backup-restore path and the
   `env` rotation (password change = rotate env + restart app).
6. **Limits** — self-signed TLS absent-or-demo, no real DNS, lab
   password posture (M25's honesty section).

## Done when

- [ ] All phases' curl transcripts in `lab-log.md`
- [ ] Resilience drill (restart) + 502 drill + DB-failure drill
      evidenced
- [ ] `api.env` verified: 600, git-ignored, not in unit file
      (`systemctl --user cat api | grep -c PASSWORD` = 0)
- [ ] `runbook.md`: six sections, commands not intentions
- [ ] Final `ss -tlnp`: every listening service justified in one
      line (the M25 audit reflex, on the finished stack)
