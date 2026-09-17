# Module 29 — Web Servers, Databases & Deployment · Content Index

> **Status:** Content complete — 4 lessons, 2 labs, quiz + key, 8
> challenges, troubleshooting guide.
> Module contract: [../README.md](../README.md) · Difficulty: Advanced.

> 🟡 **Module safety contract:** everything runs on the student's own
> VM, bound to loopback or the NAT interface. No public exposure, no
> production systems, no real domains (TLS is conceptual + self-signed
> demo only). Services run as user units where possible; every
> config change uses the backup → `nginx -t` → reload → verify
> discipline from [M25](../../M25-security-firewall/content/README.md).

## Lessons

| # | File | Topic |
|---|------|-------|
| 1 | [01-http-request-path.md](lessons/01-http-request-path.md) | HTTP fundamentals (methods, status codes, headers), ports & localhost recap, curl verification, the full request path DNS→proxy→app |
| 2 | [02-nginx.md](lessons/02-nginx.md) | nginx install & layout, server blocks (virtual hosts), locations, static serving, reverse proxy, access/error logs, reload vs restart, nginx vs Apache |
| 3 | [03-postgresql.md](lessons/03-postgresql.md) | install & service, roles/databases/privileges, psql essentials, CSV loading with `\copy`, localhost-only binding, logs, `pg_dump`/restore, MySQL/MariaDB comparison |
| 4 | [04-deployment-tls.md](lessons/04-deployment-tls.md) | the deployment model: app as systemd user unit, env-file config, health endpoints, stack logs; TLS/HTTPS concepts (certificates, self-signed demo, certbot named) |

## Labs

| # | File | Task |
|---|------|------|
| 1 | [lab-01-nginx-postgres.md](labs/lab-01-nginx-postgres.md) | nginx static dashboard + server blocks; PostgreSQL: create role/db, load CSV, query, `pg_dump` + restore |
| 2 | [lab-02-deployment.md](labs/lab-02-deployment.md) | The deployment lab: FastAPI service as a user unit, nginx proxying `/api/` to it, Postgres behind it — every hop verified with curl, runbook written |

## Practice & Support

- [Quiz](practice/quiz.md) (22 Q) · [Answer key](practice/quiz-answers.md)
- [Challenges](practice/challenges.md) (C1–C8)
- [Troubleshooting](troubleshooting.md) — 10 symptom→cause→fix patterns

## Extensions — Server Administration · Cloud Linux · DevOps

Three advanced clinics that scale the core module to fleets, clouds, and
pipelines — provider-neutral, no paid infrastructure, labs fully local:
[extensions/README.md](extensions/README.md).

## Cross-references

- [M20 systemd](../../M20-systemd-services/content/README.md) —
  the app's unit file; reload vs restart semantics.
- [M21 networking](../../M21-networking-fundamentals/content/README.md) —
  ports, sockets, bind scope, curl; the request path starts there.
- [M24 monitoring](../../M24-logs-journald-monitoring/content/README.md) —
  the stack's logs (nginx + app + Postgres) read with those skills.
- [M25 security](../../M25-security-firewall/content/README.md) —
  config-change discipline (backup/test/reload), ufw for the new
  ports, env-file secrets.
- [M27 Python](../../M27-python-jupyter-data/README.md) — the API
  app and its venv; `psycopg2` from Python.
- [M19 scheduling](../../M19-scheduling-cron-timers/content/README.md) —
  the scheduled `pg_dump`.
- [M30 capstone](../../M30-capstone-project/README.md) — this
  module's runbook is the capstone deliverable standard.
