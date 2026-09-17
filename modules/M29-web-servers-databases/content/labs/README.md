# Module 29 Labs — Web Servers, Databases & Deployment

> Two labs on your own VM. Every service binds loopback or the NAT
> interface; every config change follows backup → test → reload →
> verify; every hop is proven with curl, not assumed.

| # | Lab | Focus | Time |
|---|-----|-------|------|
| 1 | [lab-01-nginx-postgres.md](lab-01-nginx-postgres.md) | nginx server block + static site; PostgreSQL role/db/CSV load/query; `pg_dump` + verified restore | ~60 min |
| 2 | [lab-02-deployment.md](lab-02-deployment.md) | The deployment lab: FastAPI as a user unit behind nginx, Postgres underneath, every hop curl-verified, runbook written | ~75 min |

Standing rules (recap):

- `nginx -t` before every reload; config backups before edits
  (M25's five beats).
- Services: nginx as system unit (it's the front door), the app as
  a *user* unit with `EnvironmentFile` (M25's secrets pattern).
- The database role is per-app, least-privilege, lab-password only.
- Evidence to `lab-log.md`: curl transcripts, journal lines, log
  excerpts — the runbook grades on these.
