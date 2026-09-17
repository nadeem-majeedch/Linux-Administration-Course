# Lesson 3 — PostgreSQL: Roles, Databases, psql and Backups

> Module 29 · Unit 7 · Difficulty: Advanced
> Reading time: ~25 min · Lab: [Lab 1](../labs/lab-01-nginx-postgres.md)
> Up next: [Lesson 4 — deployment & TLS](04-deployment-tls.md)

---

## 1. Install and the cluster model

```console
$ sudo apt install postgresql            # M16's workflow; ~100MB with client tools
$ systemctl status postgresql            # active — another M20 service
$ ss -tlnp | grep 5432                   # LISTEN 127.0.0.1:5432 — loopback only, by default
```

Two architecture facts shape everything after:

- **A cluster, not a database** — one PostgreSQL *instance*
  (cluster) hosts many **databases**, each with schemas of tables.
  Ubuntu's package creates one cluster (`main`) on install.
- **The `postgres` superuser** — administration happens *as the
  postgres OS account*, via `sudo -u postgres psql`. This is
  peer-authentication: local OS users map to DB roles by name —
  which is why the root→postgres dance exists and why it's the
  sanctioned admin path.

## 2. Roles and databases — the authN/authZ split, again

PostgreSQL's [M25](../../../M25-security-firewall/content/README.md)
Lesson 1 vocabulary, in native dialect: **roles** are identities
(login roles = users; group roles = groups — the M12 model
exactly); **databases** hold the data; **privileges** (GRANT) are
the authorization.

```console
$ sudo -u postgres psql
postgres=# CREATE ROLE appuser WITH LOGIN PASSWORD 'CHANGE-ME-lab-only';
postgres=# CREATE DATABASE salesdb OWNER appuser;
postgres=# \c salesdb                       -- connect to it
salesdb=# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO appuser;
salesdb=# \du                               -- list roles (the /commands are psql's)
```

Course rules, learned the M25 way: **a per-app role with minimal
rights** — the API gets `appuser`, not the `postgres` superuser;
**the password is lab-only** (rotated or deleted with the lab) and
travels via env file, never into code ([M25 Lesson
5](../../../M25-security-firewall/content/README.md)); **the role owns
its database** so its privileges are self-contained. The
`localhost`-only binding (verify with `ss`) is the network half —
the database is unreachable except from the machine itself, same
posture as the app behind nginx.

## 3. psql essentials — the command-line client

`psql` is the admin knife; the backslash commands are its
superpower:

| Command | Does |
|---|---|
| `\l` | list databases |
| `\c db` | connect to a database |
| `\dt` | list tables |
| `\d table` | describe a table (columns, types, keys) |
| `\du` | list roles |
| `\x` | expanded display (wide rows become readable) |
| `\q` | quit |
| `\?` | the full command list |
| `\copy ...` | file I/O — §4 |

SQL itself — the DS essentials:

```sql
SELECT * FROM sales LIMIT 5;                     -- peek (always LIMIT first)
SELECT region, SUM(amount) AS total
FROM sales GROUP BY region ORDER BY total DESC;  -- the analytics workhorse
SELECT * FROM sales WHERE amount > 1000 AND region = 'EU';
INSERT INTO sales VALUES ('2026-09-15', 'EU', 250.00);
```

Non-interactive SQL — the automation form (M19's scripts):

```console
$ psql -d salesdb -c "SELECT count(*) FROM sales;"
$ psql -d salesdb -Atc "SELECT region FROM sales GROUP BY region;"   # -A unaligned, -t tuples-only → pipe-clean output
```

That last flag pair (`-At`) makes psql a *Unix citizen* — CSV-ish
output into [M08](../../../M08-text-processing/content/README.md)
pipelines: database → cut/sort/uniq, the full course loop.

## 4. Loading data — \copy, the CSV door

```sql
-- inside psql, connected to salesdb with a table made:
CREATE TABLE sales (date DATE, region TEXT, amount NUMERIC);
\copy sales FROM '/home/ds/lab29/sales.csv' WITH (FORMAT csv, HEADER true);
SELECT count(*) FROM sales;
```

`\copy` (client-side; server-side `COPY` needs superuser and
server-readable paths — `\copy` is the right default) streams a
CSV into a table. This is the "load the dataset into Postgres"
moment of the whole course — a real CSV from the M08 datasets into
a real relational store, then queried with GROUP BY in half a
second. Column types matter (`DATE` parses, `NUMERIC` sums) — the
`\d sales` description is the honesty check after every load.

## 5. Logs, connections and configuration

- **Logs** — Ubuntu's Postgres logs via the journal/syslog:
  `journalctl -u postgresql@16-main` (or `sudo tail
  /var/log/postgresql/postgresql-16-main.log`). Failed logins,
  slow-query hints, startup/shutdown — M24's reading skills
  apply verbatim.
- **Connections** — `ss -tlnp | grep 5432` (bind scope); who's
  connected: `SELECT * FROM pg_stat_activity;` — the
  who-did-what-now table (M18's `ps` for the database).
- **Configuration** — `/etc/postgresql/16/main/` holds
  `postgresql.conf` (bind address, memory, logging) and
  `pg_hba.conf` (host-based auth: *who may connect from where,
  how*). Reading level only — but `pg_hba.conf` is the answer to
  "why can't my app connect?" (the auth rules file), and changes
  require `sudo systemctl reload postgresql`.

## 6. Backups — pg_dump, the one-command insurance

[M24 Lesson 5](../../../M24-logs-journald-monitoring/content/README.md)'s
principles, database-shaped. `pg_dump` produces a *consistent*
snapshot of one database, even while it's running:

```console
$ pg_dump -U appuser -Fc salesdb > ~/lab29/backups/salesdb-$(date +%F).dump
$ ls -lh ~/lab29/backups/                      # the backup exists — verify, don't assume
```

`-Fc` = custom format (compressed, restorable-selective); plain
SQL is the alternative (`pg_dump salesdb > file.sql` — readable,
grep-able, portable across versions). The restore:

```console
$ createdb -U appuser salesdb_restore          # fresh target (never over the original!)
$ pg_restore -U appuser -d salesdb_restore ~/lab29/backups/salesdb-2026-09-15.dump
$ psql -U appuser -d salesdb_restore -c "SELECT count(*) FROM sales;"
```

The M24 doctrine verbatim: restore **to a fresh database**, verify
the row count against the source, *then* promote — never restore
over live data. And the scheduling note that ties the course
together: this dump command is a one-line [M19](../../../M19-scheduling-cron-timers/content/README.md)
cron entry with a log line — the nightly database backup is a
ten-minute build once every prerequisite exists. (Whole-cluster
copies exist — `pg_dumpall`, filesystem snapshots — named for
recognition; per-database dumps are the DS workhorse.)

## 7. PostgreSQL vs MySQL/MariaDB — the comparison at concept level

| | **PostgreSQL** | **MySQL / MariaDB** |
|---|---|---|
| Lineage | object-relational, standards-first | MySQL lineage; MariaDB = community fork (post-Oracle) |
| SQL character | strict, feature-rich (CTEs, window fns, JSONB, arrays) | pragmatic; MariaDB tracks MySQL compat |
| Analytics lean | strong (window functions, EXPLAIN depth) | fine for simpler reads |
| Admin shape | roles/databases, `pg_hba.conf`, `pg_dump` | users@host grants, `my.cnf`, `mysqldump` |
| Client | `psql` | `mysql`/`mariadb` |
| Ubuntu package | `postgresql` | `mariadb-server` (default in Ubuntu repos) |

Translation table: `psql -c` ≈ `mysql -e`; `\l` ≈ `SHOW
DATABASES`; `\du` ≈ `SELECT user FROM mysql.user`; `pg_dump` ≈
`mysqldump`. The concepts — service, roles, grants, dump/restore,
loopback binding — transfer whole; only the dialect changes.
Ubuntu ships MariaDB as its MySQL variant; course labs use
PostgreSQL (the DS/analytics default), with MySQL/MariaDB
recognized at this level.

## 8. Try it now (20 minutes)

1. Install and posture: the three §1 commands — confirm 5432 is
   loopback-only *before* anything else (M25's audit reflex).
2. Role + db + table: create `appuser` and `salesdb` (§2), make a
   two-column table, `\copy` a small CSV (§4), `SELECT` with
   GROUP BY — the whole loop inside `psql`.
3. The census pipeline: `psql -d salesdb -Atc "SELECT region,
   amount FROM sales;" | sort | uniq -c | sort -rn | head` —
   database into M08 tools, no Python in sight.
4. Dump → drop (the *test* db, never the original) → restore →
   count-verify: the full M24 discipline, rehearsed on data you
   control. Time it; that's your first database RTO.

## 9. Common mistakes

- Connecting as the `postgres` superuser from your app — the
  least-privilege breach at the heart of the stack; apps get
  `appuser`.
- Restoring over the live database — scratch target first, always
  (M24 §7).
- `\copy` paths relative to *where you started psql* — use
  absolute paths; the error ("No such file") means what it says.
- Forgetting the password in the connection env (M25's env-file
  pattern) — `psql` prompting interactively is fine for admins,
  fatal for scheduled jobs (M19's no-prompts rule).
- Blaming the network when `pg_hba.conf` is the answer — "no
  pg_hba.conf entry for host" is an auth-config finding, and
  `[ss]`-level verification of the bind address rules the rest out.

> **Up next:** [Lesson 4 — deployment & TLS](04-deployment-tls.md):
> the app as a systemd unit, config via environment, health
> checks — and HTTPS concepts with a self-signed demo.
