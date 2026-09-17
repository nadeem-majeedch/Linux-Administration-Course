# Lab 1 — nginx Static Site + PostgreSQL from CSV to Backup

> Module 29 · Unit 7 · Difficulty: Advanced
> Time: ~60 min · Environment: your own VM
> Prerequisites: [Lessons 1–3](../README.md)
> ⚠️ Loopback/NAT only; lab DB password only; restore goes to a
> *scratch* database, never over the original.

Two halves: the front door (nginx, static) and the vault
(PostgreSQL, data). Verified separately in this lab; composed in
[Lab 2](lab-02-deployment.md).

## Part A — nginx: server block + static dashboard (25 min)

**A1. Install & baseline** (Lesson 2 §1): install, status, the
default page via curl. Record the four-command transcript.

**A2. Your site:** create `~/lab29/www/index.html` — a minimal
dashboard shell:

```html
<!DOCTYPE html><html><head><title>Sales Dashboard</title></head>
<body><h1>Sales Dashboard</h1><p id="status">static shell — API lands in Lab 2</p>
</body></html>
```

**A3. The server block** (Lesson 2 §2):
`/etc/nginx/sites-available/dashboard` with `server_name
dashboard.test`, `root /home/ds/lab29/www` — plus the `/etc/hosts`
line, the symlink, **`nginx -t`**, reload, and the two verification
curls (by name; with a wrong Host header → default server).

**A4. The 403 experiment** (Lesson 2 §3): `chmod 700 ~/lab29/www`,
curl (403), read `error.log`'s last line, `namei -l` the path, fix
(755/644), re-curl. The permissions clinic, web edition — logged
with the error.log line quoted.

**A5. Log census:** ten requests (mix in two 404s), then the
status-census pipeline (`awk '{print $9}' access.log | sort | uniq
-c`) on *your* block's access log.

## Part B — PostgreSQL: role, data, query, backup (30 min)

**B1. Install & posture:** install, status, `ss -tlnp | grep 5432`
(loopback confirmed — record it), log location identified.

**B2. Role & database** (Lesson 3 §2):

```console
$ sudo -u postgres psql
postgres=# CREATE ROLE appuser WITH LOGIN PASSWORD 'lab-only-CHANGE-ME';
postgres=# CREATE DATABASE salesdb OWNER appuser;
postgres=# \c salesdb
salesdb=# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO appuser;
```

**B3. Table + CSV load** (§4): create the `sales` table (date,
region, amount), `\copy` from a course dataset (M08's
`sales_2026.csv` — or any CSV with a header), verify with `SELECT
count(*)` and `\d sales`. Record the row count — it's the restore
verification number later.

**B4. The analytics query:** the GROUP BY regional summary (§3),
plus the pipe-to-shell census (`-Atc` into `sort | uniq -c`). Two
outputs into the log.

**B5. Backup & verified restore** (§6):

```console
$ mkdir -p ~/lab29/backups
$ pg_dump -U appuser -Fc salesdb > ~/lab29/backups/salesdb-$(date +%F).dump
$ createdb -U appuser salesdb_scratch
$ pg_restore -U appuser -d salesdb_scratch ~/lab29/backups/salesdb-*.dump
$ psql -U appuser -d salesdb_scratch -c "SELECT count(*) FROM sales;"
```

The scratch count must equal B3's. **Time the restore** — your
first database RTO. Then drop the scratch database (it was a
rehearsal, not a copy).

## Part C — the wiring preview (5 min)

One paragraph in `lab-log.md`: which pieces of today's work will
Lab 2 reuse (the server block gains a `/api/` location; `appuser`
gains an env-file password; the dashboard page gains a JS fetch to
`/api/`)? The composition map, written before it exists.

## Done when

- [ ] A2–A5 transcripts complete (including the 403/error.log
      evidence)
- [ ] B2–B5 complete; loopback binding recorded; scratch-restore
      count matches; **RTO timed**
- [ ] `nginx -t` appears before every reload (count them)
- [ ] The Part C composition paragraph written
