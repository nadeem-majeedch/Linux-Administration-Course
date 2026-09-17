# Module 29 Troubleshooting — Stack Symptoms → Causes → Fixes

> Ten patterns for the deployed stack, ordered by encounter
> frequency. Each: **symptom → cause → diagnosis → fix →
> prevention**. The M24 method opens every case; the request path
> (Lesson 1 §4) orders the evidence.

## 1. 502 Bad Gateway through the proxy

**Cause:** nginx is fine; the *backend* is unreachable — app
crashed, not started, wrong port, or bound to a different address.
**Diagnosis:** `systemctl --user status api.service`;
`journalctl --user -u api.service --no-pager | tail`;
`ss -tlnp | grep 8000`; nginx `error.log` shows
`connect() failed`.
**Fix:** restart/rebind the app; correct the `proxy_pass` target.
**Prevention:** `Restart=on-failure` + the health probe (C6) —
502s page *you* within minutes, not the users first.

## 2. Static files 403 (or 404) through nginx

**Cause:** 403 = permissions on the path (`www-data` can't
traverse/read); 404 = wrong `root`, or the file's not where the
URI maps.
**Diagnosis:** `error.log` (the exact denied path); `namei -l
/home/ds/lab29/www/index.html` (bit-by-bit); compare `root` vs the
URI.
**Fix:** 755 dirs / 644 files; correct the root.
**Prevention:** after moving docroots, one curl + one `namei -l`
before declaring done.

## 3. "Wrong site answered" (default server strike)

**Cause:** the request's `Host` header matched no `server_name`,
so the default server (first block on the port) answered.
**Diagnosis:** `curl -H "Host: dashboard.test" http://localhost/`
— works? Then routing is name-based; check DNS/hosts and the
`server_name` spelling.
**Fix:** add/correct `server_name`; add the hosts entry (lab);
mark the intended catch-all `default_server` deliberately.
**Prevention:** every server block's `server_name` tested at
creation (Lab 1 A3's two-curl check).

## 4. App starts, then dies in a restart loop

**Cause:** crash-on-boot — DB credential refused, import error
(venv/cwd), port already taken, missing env var.
**Diagnosis:** `journalctl --user -u api.service -b --no-pager |
tail -30` (the traceback is verbatim); `systemctl --user show api
-p ExecStart` (what's actually being run).
**Fix:** per evidence — env var, path, port (the M10/M19 rules
recast).
**Prevention:** `env -i` gate + a manual `ExecStart`-line run
*before* enabling; `Restart=` hides nothing from the journal.

## 5. "relation does not exist" / permission denied in the app

**Cause:** the app role lacks rights on the table/schema, the
table is in another database, or the connection went to the wrong
db (default `postgres`?).
**Diagnosis:** as the app role: `psql -U appuser -d salesdb -c
'\dt'` (does the app even *see* the table?); `\dn+`, `\dp` for
privileges.
**Fix:** `GRANT` (on tables *and* sequences) or fix the connection
string's database.
**Prevention:** post-migration GRANTs are part of the migration
script (C4's drill), not memory.

## 6. "Too many clients" / connection refused from the app

**Cause:** leaked connections (no close/context manager), or
`max_connections` shared with every other tenant of the cluster;
connection-refused variant = postgres stopped or bound away.
**Diagnosis:** `SELECT count(*) FROM pg_stat_activity;` + by user;
`ss -tlnp | grep 5432`; app-side: are connections returned to a
pool?
**Fix:** close/`with`-manage connections; restart the app to
drain; raise limits only with a reason written down.
**Prevention:** the `with db() as conn:` pattern (Lab 2's app
does this); the health endpoint's db ping catches it early.

## 7. Config change took the site down (nginx dead)

**Cause:** syntax error + `restart` (the exact sequence
[M25](../../M25-security-firewall/content/lessons/03-ssh-hardening-applied.md) §3 bans).
**Diagnosis:** `sudo nginx -t` (names file and line);
`systemctl status nginx`; `journalctl -u nginx`.
**Fix:** correct or restore the backup (`sites-available/*.bak`),
`nginx -t`, `reload`.
**Prevention:** the five beats — backup, edit, **test**, reload,
verify — no exceptions, including "tiny" edits.

## 8. CSV load fails or loads garbage

**Cause:** wrong `FORMAT`/`HEADER` options, delimiter mismatch
(`;` vs `,`), encoding, or columns mismatched to the table.
**Diagnosis:** read the psql error (line number!); `head -2
file.csv`; compare to `\d tablename`.
**Fix:** correct the `WITH (...)` options; create matching columns
(or stage into a text table first).
**Prevention:** `\copy` a 3-row sample before the full file; count
check after (`SELECT count(*)` vs `wc -l`).

## 9. Restore overwrote/won't restore

**Cause:** restored into the *live* database (the unforgivable
variant), or `pg_restore` errors from role/ownership mismatches.
**Diagnosis:** the restore transcript (errors are per-object and
named); for the live-overwrite: the M24 postmortem, honestly, and
the state of the dump file (which is why it existed).
**Fix:** re-restore to a **scratch** database; `--no-owner`
when roles differ between source and target.
**Prevention:** the runbook's restore section names the scratch
target *before* any incident; dumps verified by test-restore
schedule (M24's rule).

## 10. The whole stack is "slow" (no error at all)

**Cause:** anything — DB query without index, app doing N+1
queries, nginx fine, upstream latency — which is why "slow" needs
per-hop evidence.
**Diagnosis:** the latency ladder: `curl -w` at each hop (static
through nginx → direct app → app's query timing); `EXPLAIN ANALYZE`
the slow SQL; `pg_stat_activity` for long queries; M24's vmstat for
the machine itself.
**Fix:** index the query, batch the queries, cache the static —
*per the hop that measured slow*.
**Prevention:** the per-hop probe in the health kit makes "slow"
have a *location* within one incident, not a week of vibes.

## When to escalate

| Evidence | Escalate to |
|---|---|
| Data loss or corruption (restore went wrong) | Data owner + your postmortem, immediately — before any fix attempt |
| Suspected breach (unknown connections in `pg_stat_activity`, foreign log lines) | IT security (M25's escalation table) |
| Cluster-level Postgres issues (WAL, replication) | DBA/admin — beyond lab scope |
| Repeat 502s with clean app logs | Infra owner — the request path beyond your VM |

> The stack gives you *three* log streams and a health endpoint —
> more evidence per incident than anything earlier in the course.
> The skill is walking the path front-to-back, in order, before
> theorizing.
