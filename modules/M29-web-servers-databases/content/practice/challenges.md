# Module 29 Challenges — Web Servers, Databases & Deployment

> Eight challenges on your own VM. Loopback/NAT only; config
> changes via backup → test → reload; evidence in `lab-log.md`.

## C1 — The second site (virtual-host fluency)

Add `catalog.test` as a *second* server block with its own root
and access log — both sites live simultaneously on :80. Prove
Host-header routing with three curls (`dashboard.test`,
`catalog.test`, an unknown name → default). Then delete cleanly
(symlink + file + hosts line) and show the default answering
again.

## C2 — The reverse-proxy variants

For a toy backend (`http.server` echoing its `path`), create TWO
locations: `/a/` with `proxy_pass http://127.0.0.1:8000;` (no
slash) and `/b/` with the trailing slash. curl `/a/test` and
`/b/test`; document the two paths the backend received. Then the
one-line rule for choosing between them, written into your
nginx comment.

## C3 — The access-log analyst

Generate 100 requests (a loop mixing good paths, 404s, and one
502 by stopping the app mid-run), then produce, pipeline-only: (a)
status census, (b) top five requested paths, (c) the timestamp of
the first and last 5xx. Then one sentence each: what an on-call
engineer would conclude from each output. (M08 + M24, over
production-shaped data.)

## C4 — The database migration drill

New table `regions(id, name, manager)`, populated by hand; then
`ALTER` the sales table to add a `region_id` column and fill it
from a mapping. Write the two `psql` commands that *verify*
referential sanity after the change (counts per region both
before/after). This is schema evolution, rehearsed small.

## C5 — The scheduled backup

Wire [M19](../../../M19-scheduling-cron-timers/content/README.md):
a user cron line (or timer — state which and why) running
`pg_dump -Fc` nightly into `~/lab29/backups/` with a timestamped
name and a log line; retention via the M24 rotator (keep 7).
Prove one run, then simulate the retention decision with five
fake dumps. The weekly restore test: restore the *latest* dump to
scratch, count-verify, log the RTO.

## C6 — The health probe, monitored

Turn Lesson 4's five-sample probe into `probe.sh` (curl status +
latency; exit 1 on non-200 or latency > 1s), schedule it every 5
minutes, and give it memory: a `health.log` of timestamped
results. Induce a failure (stop the app for one cycle) and show
the log's gap + FAIL line. The M24 absence alarm gets its
production data source.

## C7 — The TLS demo, end to end

Create the self-signed cert (Lesson 4 §4), add a `listen 443
ssl` server block, open 443 in ufw, and verify: `curl -k`
succeeds, plain `curl` shows the certificate complaint, and
`openssl s_client -connect localhost:443 -brief` prints the
negotiated TLS version. Then the honesty paragraph: what `-k`
skipped, and what certbot would add on a real-DNS machine.

## C8 — The stack restart matrix

Measure cold-start of the full stack: `systemctl stop` postgres +
nginx, `--user stop` the app, then time each startup in dependency
order and the *first successful* three-hop curl after each. Fill a
matrix (service → start time → health-confirmed). One paragraph:
which order the runbook mandates and what breaks if inverted.

## Stretch — C9, the architecture memo

A teammate proposes "skip nginx, expose uvicorn on :80 directly
with --proxy-headers". Write the one-page memo: what is lost
(static offload, TLS termination point, buffering, one-door
auditability), what the risk profile becomes, and the diagram of
the recommended path — using only concepts from this module.
The deliverable is the *argument*, in the course's vocabulary.
