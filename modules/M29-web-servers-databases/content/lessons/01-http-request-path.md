# Lesson 1 — HTTP, Ports and the Request Path

> Module 29 · Unit 7 · Difficulty: Advanced
> Reading time: ~25 min · Lab: [Lab 1 — nginx & Postgres](../labs/lab-01-nginx-postgres.md)
> Up next: [Lesson 2 — nginx](02-nginx.md)

---

## 1. What a web server actually is

Strip the mystique: a **web server** is a program that listens on a
TCP port ([M21](../../../M21-networking-fundamentals/content/README.md)),
speaks the **HTTP** protocol, and answers requests — usually with a
file from disk or a response computed by another program. "Deploying
a data product" — a dashboard, a model API, a data portal — means
running such a program on a Linux machine you administer and
understanding every hop between a browser and it. This module builds
that entire stack on your VM: nginx in front, a Python API behind,
PostgreSQL under it all.

## 2. HTTP in one page — the conversation

HTTP is a request/response protocol over TCP. A browser asks; the
server answers; the connection closes (or is reused). The request:

```http
GET /dashboard/index.html HTTP/1.1
Host: localhost
User-Agent: curl/8.5.0
Accept: */*
```

Method + path + version, then headers. The response:

```http
HTTP/1.1 200 OK
Server: nginx/1.24.0
Content-Type: text/html
Content-Length: 512

<!DOCTYPE html>...
```

Status + headers + body. The vocabulary worth owning:

**Methods** — the verbs. For DS work you need exactly four:

| Method | Meaning | DS use |
|---|---|---|
| `GET` | read, no side effects | fetch the dashboard, query the API |
| `POST` | send data, may have side effects | submit a prediction, upload a payload |
| `PUT`/`DELETE` | replace/remove | (REST APIs — recognize them) |

**Status codes** — the classes carry the diagnosis:

| Class | Meaning | The one you'll meet |
|---|---|---|
| 2xx | success | `200 OK`, `204 No Content` |
| 3xx | redirect | `301`, `304` (cached) |
| 4xx | **client** error | `404` not found, `403` forbidden, `401` unauthenticated |
| 5xx | **server** error | `500` app crash, `502` proxy lost the app, `504` timeout |

The 4xx/5xx split is the first diagnostic fork of every web
incident: 4xx = *the request is wrong* (bad path, bad auth); 5xx =
*the server side failed* (app down, proxy broken). [M22's
tunnel + this module's stack] generate both classes in the lab
precisely so you learn to read them.

**Headers** — metadata: `Content-Type` (what the body is —
`text/html`, `application/json`), `Location` (redirects),
`Authorization` (tokens), `Server`. The DS-critical pair:
`Content-Type: application/json` for APIs, `Cache-Control` for
whether the browser is showing you stale data.

## 3. Ports, localhost, and the verification tool

Recap with purpose — from
[M21](../../../M21-networking-fundamentals/content/README.md):

- Web defaults: **80/TCP** (HTTP), **443/TCP** (HTTPS); dev services
  pick high ports (8000, 8888).
- **localhost** = the loopback conversation: server and client on
  the same machine, no network involved. Every service in this
  module binds loopback or the VM's NAT interface — never exposed.
- **`curl` is the verification instrument** for every hop:

```console
$ curl -i http://localhost:8000/            # -i: include response headers
$ curl -s http://localhost:8000/api/health  # -s: silent; body only
$ curl -sI http://localhost:8000/           # -I: HEAD request — headers only
$ curl -sv http://localhost:8000/ 2>&1 | grep -E 'Connected|HTTP/1'   # -v: the transcript
$ curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' http://localhost:8000/api/
200 0.012s                                   # status + latency in one line
```

The last form is the health-check idiom — status code and latency,
machine-readable, scriptable into the M24 health kit. Add `-X POST
-H "Content-Type: application/json" -d '{"x":1}'` for POSTing JSON
to your API, and `curl` covers the whole lab.

## 4. The request path — the map of this module

Every web interaction in this module traverses the same chain, and
every lesson owns a hop:

```text
browser / curl
   │  DNS or /etc/hosts (a name → an IP)
   ▼
TCP connection to host:port          ← M21: ports, sockets, bind scope
   ▼
nginx :80 (the front door)
   │  server block picks the site     ← Lesson 2
   │  location /      → static files from disk
   │  location /api/  → reverse proxy
   ▼                    proxy_pass http://127.0.0.1:8000
FastAPI app :8000 (loopback only!)   ← Lessons 2 & 4 (systemd unit)
   │  queries the database
   ▼
PostgreSQL :5432 (loopback only!)    ← Lesson 3
```

Three structural ideas to name now:

- **Static vs dynamic** — files served straight from disk (fast,
  nginx's core job) vs responses computed on request (the app's
  job). The dashboard page is static; `/api/predict` is dynamic.
- **Reverse proxy** — nginx accepting requests *on behalf of* the
  app: the app binds loopback only (unreachable directly), nginx
  is the sole public door. One port, TLS termination, static-file
  offloading, buffering — and the reason your app can stay
  privileged-minimal.
- **Loopback everywhere** — only nginx faces even the VM's
  network; the app and DB are reachable *through* it (or via your
  [M22 tunnel](../../../M22-ssh-remote-admin/content/README.md)).
  Defense-in-depth from [M25](../../../M25-security-firewall/content/README.md)
  Lesson 1, as architecture.

Trace a request aloud — DNS, TCP, server block, location, proxy,
app, DB, and back — and you have this module's table of contents.

## 5. The lab stack preview

What Lab 1–2 assembles, in full:

```text
nginx :80 ──── /          → static dashboard (HTML/CSS from /var/www or ~)
        └──── /api/       → FastAPI on 127.0.0.1:8000 (user systemd unit)
                                └── PostgreSQL on 127.0.0.1:5432
                                        └── table loaded from sales CSV
```

Everything with: a service per component (`systemctl`/`--user`),
a log per component (nginx logs, journalctl, Postgres logs), a
health check per hop (curl), and a runbook (the lab's deliverable).
This is the "small but complete" deployment — the same shape as
every real one you'll inherit, minus the scale.

## 6. Try it now (10 minutes)

1. The four-verb curl drill against any running service you have
   (M22's lab server, a tunnel): `-i`, `-s`, `-sI`, and the
   status+latency one-liner — read each header aloud.
2. Status-code safari: `curl -s -o /dev/null -w '%{http_code}\n'`
   against `/` (200), a nonsense path (404), and — if a proxy is
   running — with its backend dead (502). Three codes, three
   stories.
3. Draw the request path for *your* M22 tunnel setup (browser →
   SSH → Jupyter): which hops exist, which are encrypted, which
   binds loopback? The vocabulary transfers whole.
4. `ss -tlnp` on the VM — note every listening line; by module's
   end, nginx (80) and Postgres (5432) join this list, and you'll
   audit them with the M25 rubric.

## 7. Common mistakes

- Reading `404` as "server broken" — 4xx means the *request* is
  wrong (path, host header); check what you typed before blaming
  the stack.
- Forgetting the `Host` header matters — nginx's server blocks
  are selected by it; `curl http://127.0.0.1/` and
  `curl http://mysite.test/` can hit *different sites* on the same
  server (Lesson 2's whole point).
- Testing the app directly and thinking you tested the stack —
  always verify through the front door (`curl localhost/`) so
  nginx's hop is included.
- assuming latency is the DB — measure per hop (`-w '%{time_total}'`
  against app direct vs through proxy) before verdicts (M24's
  evidence rule).

> **Up next:** [Lesson 2 — nginx](02-nginx.md): installing the front
> door, server blocks, static files, and the reverse proxy — with
> the config-test-reload discipline.
