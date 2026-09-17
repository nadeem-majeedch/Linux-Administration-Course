# Lesson 4 — The Deployment Model and TLS Concepts

> Module 29 · Unit 7 · Difficulty: Advanced
> Reading time: ~25 min · Lab: [Lab 2 — the deployment lab](../labs/lab-02-deployment.md)
> Up next: [Lab 2](../labs/lab-02-deployment.md), then the [M30 capstone](../../../M30-capstone-project/README.md)

---

## 1. "Deployment" defined — the word for the whole last mile

Everything this course built converges here. **Deployment** is the
repeatable act of taking code from "runs on my machine" to "runs as
a service on a machine, reachable, logged, monitored, and
recoverable". Its components — every one already taught — are:

```text
artifact      the app + its venv (M27), versioned (M26)
process       systemd user unit with Restart= (M20)
config        environment file — secrets out of code (M25 Lesson 5)
front door    nginx server block + proxy_pass (this module, Lesson 2)
data          PostgreSQL, migrated and dumped (Lesson 3)
health        an endpoint + curl checks (M24's kit consumes them)
logs          journalctl + nginx logs (M24's method)
rollback      the previous artifact + config backup (M25's discipline)
runbook       the document that makes it all repeatable (Mini-Project D's form)
```

Deployment is not a tool — it's this checklist wearing a name. The
lesson walks the parts that are new in context; Lab 2 assembles
the whole.

## 2. The app as a systemd user unit

A FastAPI/Flask app served by uvicorn — the app server (ASGI/
WSGI vocabulary: uvicorn speaks ASGI for modern async apps; gunicorn
speaks WSGI for classic Flask) — as a **user service** ([M20's
](../../../M20-systemd-services/content/README.md) pattern, no root,
no system exposure):

```ini
# ~/.config/systemd/user/api.service
[Unit]
Description=Sales API (FastAPI/uvicorn)

[Service]
WorkingDirectory=%h/lab29/app
EnvironmentFile=%h/lab29/app/api.env
ExecStart=%h/lab29/app/.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=on-failure
RestartSec=3
MemoryMax=400M

[Install]
WantedBy=default.target
```

New directives, in context: **`EnvironmentFile`** — the secrets/
config layer: `api.env` (mode 600, git-ignored) holds
`DATABASE_URL=postgresql://appuser:...@127.0.0.1/salesdb` — the
[M25](../../../M25-security-firewall/content/README.md) env-pattern,
now carrying the DB credentials into the app with zero literals in
code. **`Restart=on-failure`** — the crash self-heals in 3s: the
difference between a 502 blip and a 502 morning. **`MemoryMax`** —
the M24 cap so *your* app dies before the server does.

Activation and the health endpoint:

```console
$ systemctl --user daemon-reload && systemctl --user enable --now api.service
$ curl -s http://127.0.0.1:8000/health        # direct — the app's own pulse
{"status":"ok"}
```

The **health endpoint** is two lines of app code (`{"status":"ok"}`
plus, ideally, a DB ping) — and it's what makes the deployment
*machine-checkable*: the [M24 health kit](../../../M24-logs-journald-monitoring/content/README.md)
curls it; nginx proxies it; the absence alarm watches its log
line. Every deployed service this course touches has one.

## 3. The zero-downtime habit — reload, don't restart

Updating the app without dropping the front door:

```console
$ systemctl --user restart api.service        # app restarts — nginx stays up
$ curl -s http://localhost/api/health         # through the proxy: brief 502 at worst
```

Because nginx *proxies*, app restarts are invisible to anyone not
mid-request — and nginx's own config changes use `reload` (M20's
distinction, [M25's](../../../M25-security-firewall/content/README.md)
discipline: backup → `nginx -t` → reload → verify). "Zero-downtime"
at scale means rolling instances behind load balancers; at this
scale it means **the front door never restarts when the back end
does** — an architecture habit, not a product.

## 4. TLS/HTTPS — the concepts

**TLS** (Transport Layer Security) wraps the HTTP conversation in
encryption + authentication: the client verifies the server's
identity via a **certificate**, then both sides derive session
keys. HTTPS = HTTP inside TLS, default port 443.

The certificate model in four claims:

1. A **certificate** binds a domain name to a public key, signed by
   a **Certificate Authority (CA)** — the browser's trust in the CA
   chain transfers to the server ("this really is dashboard.example").
2. **Let's Encrypt** issues free, automated certs; **certbot** (the
   Ubuntu package) obtains and renews them — including nginx
   integration. On a VM *without real DNS*, certbot can't run —
   which is why the labs use the next option.
3. **Self-signed certificates** provide the encryption with no CA
   trust — clients must *explicitly accept* the cert (`curl -k`,
   or import it). Right for lab demos; wrong for anything shared.
4. **TLS terminates at nginx** — the proxy holds the certificate;
   traffic from nginx to the loopback app stays plain HTTP because
   it never leaves the machine (M21's bind-scope security paying a
   dividend).

```console
$ sudo openssl req -x509 -nodes -days 30 -newkey rsa:2048 \
    -keyout /etc/ssl/private/dashboard.key \
    -out /etc/ssl/certs/dashboard.crt \
    -subj "/CN=dashboard.test"                 # the self-signed demo cert
$ sudo ufw allow 443/tcp                       # the HTTPS door (M25)
```

…and an nginx `listen 443 ssl;` block pointing at those files (Lab
2's optional extension). `curl -k https://dashboard.test/`
verifies it — `-k` being the honest acknowledgment that *you* are
the trust anchor here. The HSTS/redirect-to-HTTPS and
cipher-suite details are real-server topics; the concepts —
certificates, CAs, termination, self-signed vs CA-signed — are the
transferable core.

## 5. The logs of the stack — three sources, one method

The deployed system generates three log streams; [M24's
](../../../M24-logs-journald-monitoring/content/README.md) method
reads them as one incident:

| Source | Where | What it tells you |
|---|---|---|
| nginx | `/var/log/nginx/{access,error}.log` | every request + status; proxy failures (502) |
| the app | `journalctl --user -u api.service` | tracebacks, query errors, startup |
| PostgreSQL | `journalctl -u postgresql@*` | auth failures, slow queries, restarts |

The composite diagnosis — "the API is down at 09:14" — walks
front-to-back: nginx access log (502s from when?), app journal
(traceback at 09:13 — the DB credential rotated?), Postgres log
(auth failure 09:12). Three greps, one root cause. The health
endpoint + these logs + the M24 six-step method: the deployed
system is as observable as the machine it runs on.

## 6. Try it now (15 minutes)

1. The unit-file walkthrough: read §2's `api.service` and annotate
   each directive with the module/lesson it comes from. (If
   unfamiliar lines remain, that's Lab 2's preview.)
2. Health-check scripting: `for i in {1..5}; do curl -s -o
   /dev/null -w '%{http_code} %{time_total}s\n' http://localhost:8000/health;
   sleep 1; done` — the monitoring probe, five samples, local.
3. TLS vocabulary check: explain to an imaginary teammate why the
   lab uses a self-signed cert and what `curl -k` *means* — then
   why the same cert would be wrong for a real site.
4. The three-log tour on a VM with the stack (or any one service):
   locate each of §5's sources, tail each, and write the one-line
   "what this stream is for".

## 7. Common mistakes

- Secrets in the unit file itself (`Environment=PASSWORD=...`) —
  `systemctl cat` shows it to every user on the machine;
  `EnvironmentFile` (600) is the pattern.
- `WorkingDirectory` forgotten — the app starts, imports fail on
  relative paths (M19's cwd trap, wearing systemd).
- Testing via the app's port instead of through nginx — the
  proxy's headers/routing/TLS are part of the product; verify the
  front door (Lesson 1 §7's rule).
- Self-signed certs shipped to teammates — `-k` is a *personal*
  acknowledgment; shared trust needs a CA (certbot) or importing
  the cert properly.
- Restart when reload suffices — killing the front door to change
  a config that `nginx -t && reload` applies cleanly.

> **Next:** [Lab 2 — the deployment lab](../labs/lab-02-deployment.md):
> assemble nginx → API → Postgres into one verified, documented
> stack — the capstone's rehearsal, end to end.
