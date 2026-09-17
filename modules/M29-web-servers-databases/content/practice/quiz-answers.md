# Module 29 Quiz — Answer Key

> Reasoning graded; commands on "would it work if typed".

## Section A — HTTP & the request path

**A1.** GET (read, no side effects), POST (send data, may change
state), PUT/DELETE (replace/remove — recognition). GET must be
safe/idempotent: no state changes — crawlers and prefetchers fire
GETs constantly.

**A2.** 2xx success; 3xx redirect; 4xx *client* error (bad
request); 5xx *server* error (server side failed). The fork: 4xx
→ inspect the request (path, auth, headers); 5xx → inspect the
stack (app, proxy, DB). It halves the search space before any
command is run.

**A3.** The proxy is *alive and answering* — the backend is not.
Commands: `systemctl --user status api.service`,
`journalctl --user -u api.service --no-pager | tail`,
`ss -tlnp | grep 8000`.

**A4.** Client → (DNS/hosts) → TCP :80 → nginx (server block) →
location: static-from-disk or `proxy_pass` → app
(127.0.0.1:8000, user unit) → PostgreSQL (127.0.0.1:5432) → back
up the chain. Only **nginx** is network-facing; app and DB bind
loopback.

**A5.** `curl -s -o /dev/null -w '%{http_code} %{time_total}s\n'
URL` — machine-readable status + latency; scriptable into health
checks and monitoring probes (M24's kit consumes exactly this).

## Section B — nginx

**B6.** `available` holds every site's config; `enabled` holds
symlinks to the active ones (nginx reads only enabled).
`sudo ln -s /etc/nginx/sites-available/x /etc/nginx/sites-enabled/`
(and `rm` the symlink to disable).

**B7.** The **`Host` header** matched against `server_name`
(port must match too). No match → the **default server** (first
block on that port, or `default_server`-marked) answers — the
"wrong site answered me" explanation.

**B8.** `nginx -t` parses the config without applying it; a syntax
error caught there costs two seconds, while one *not* caught +
`restart` takes the whole front door down (all sites).

**B9.** `reload`: re-read config, existing connections and
workers finish gracefully — no dropped requests. `restart`: full
stop+start — all connections severed. Reload for config; restart
only when the binary itself changed.

**B10.** Without trailing slash on `proxy_pass`: the app receives
`/api/health` (original URI forwarded). With
`proxy_pass http://127.0.0.1:8000/`: the location prefix is
stripped — the app receives `/health`. Both valid; the app's
routes must match the choice.

**B11.** `error.log` names it (permission denied, with path).
Suspects: the file needs `644` and every directory on the path
needs the execute bit (`755`) for `www-data` — `namei -l` walks
the chain (M13's tool).

## Section C — PostgreSQL

**C12.** One *cluster* (instance) hosts many *databases* (each
with schemas/tables). Ubuntu's package creates cluster `main` on
install, listening on 5432.

**C13.** Local admin auth is **peer**: OS user ↔ DB role mapped by
name, so admin access goes through the `postgres` OS account —
`sudo -u postgres psql`. It avoids network auth for
administration entirely.

**C14.** Principle: **least privilege** (M25 Lesson 1) — the app
role gets only its database's rights. Consequence: a compromised
app process can damage only `salesdb`, not the cluster, its
roles, or other databases.

**C15.** `\copy` — client-side: reads files the *client* can
access (your paths, no superuser needed). Server-side `COPY` runs
as the postgres process (server paths, superuser) — `\copy` is
the safe default for lab and app use.

**C16.**
```console
$ pg_dump -U appuser -Fc salesdb > salesdb-$(date +%F).dump
$ createdb -U appuser salesdb_scratch
$ pg_restore -U appuser -d salesdb_scratch salesdb-*.dump
```
Verification: row counts match the source (`SELECT count(*)` both
sides) *before* promotion — restore to scratch, never over live.

**C17.** *Who may connect from where, and how* (host/user/db →
auth method). The classic message: `no pg_hba.conf entry for
host ...` — an auth-policy finding, not a network fault.

## Section D — deployment & TLS

**D18.** `EnvironmentFile`: config/secrets injected at start —
out of code and out of `systemctl cat`'s sight (600 file).
`Restart=on-failure`: crash self-heals — a blip, not an outage.
`MemoryMax`: the runaway app dies alone (M24's cap), not the
server.

**D19.** Mechanisms: (1) `systemctl cat` would display an
in-unit `Environment=` to any local user; the 600 env file is
readable only by the service's user. (2) Git never sees it
(git-ignored). Principle: secrets live at the narrowest readable
scope, injected, never committed.

**D20.** App restart: the app's connections drop for its restart
window; nginx stays up and answers (502 for in-flight, then
healthy) — `Restart=`'s window is ~seconds. nginx reload: config
reread, no connection loss. The front door is the shared doorway
for every site — restarting it for a backend change converts one
app's update into every site's outage.

**D21.** Certificate: a domain↔public-key binding, signed. CA: a
trusted issuer whose signature browsers already trust.
Self-signed: you sign your own — encryption yes, third-party
trust no; appropriate for labs/localhost demos where the client
explicitly accepts it (`curl -k`), never for shared services.

**D22.** Plain HTTP over **loopback** — same machine, never
touching a network interface. Acceptable because the exposure of
loopback traffic is local by construction (M21 bind scope); TLS's
job (protecting the wire) is already complete at the nginx
boundary.

## Bonus (Q23) — model answer

1. `curl -s -o /dev/null -w '%{http_code}\n' http://dashboard.test/api/health`
   — reproduce: confirm 502 (and `curl http://127.0.0.1:8000/health`
   directly: is the app alive at all?).
2. `systemctl --user status api.service` — dead? restarting-loop?
3. `journalctl --user -u api.service --no-pager | tail -20` — the
   traceback (DB auth? import error? port taken?).
4. `ss -tlnp | grep -E ':8000|:5432'` — is anything listening
   where it should be?
5. `sudo tail /var/log/nginx/error.log` — nginx's view: connect()
   refused vs timeout (app dead vs hanging).
6. Fix per evidence → restart app (or DB) → re-run step 1 →
   postmortem with prevention (health alarm would have paged at
   09:14:01, not 09:40).

## Score guide

| Score | Meaning |
|---|---|
| 20–23 | Deployment-ready — the capstone stack awaits |
| 15–19 | Re-read flagged lessons; redo the matching lab phase |
| < 15 | Repeat lessons 2–3; the proxy and DB are load-bearing |
