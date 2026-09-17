# Lesson 2 — nginx: Server Blocks, Static Files and the Reverse Proxy

> Module 29 · Unit 7 · Difficulty: Advanced
> Reading time: ~25 min · Lab: [Lab 1](../labs/lab-01-nginx-postgres.md)
> Up next: [Lesson 3 — PostgreSQL](03-postgresql.md)

---

## 1. Install and layout — where everything lives

```console
$ sudo apt install nginx                      # the M16 five-beat workflow
$ systemctl status nginx                      # active, enabled — an M20 service
$ ss -tlnp | grep nginx                       # LISTEN 0.0.0.0:80 — the front door exists
$ curl -sI http://localhost/ | head -3        # HTTP/1.1 200 OK, Server: nginx/...
```

Default page served — the install is verified end to end in four
commands. The file layout (Ubuntu's convention) is the map for
everything else:

| Path | Contents |
|---|---|
| `/etc/nginx/nginx.conf` | main config — includes the two dirs below |
| `/etc/nginx/sites-available/` | your **server blocks**, one file per site |
| `/etc/nginx/sites-enabled/` | symlinks to enabled sites (`nginx` reads *only* these) |
| `/var/www/html/` | default static root |
| `/var/log/nginx/access.log` | every request, one line each |
| `/var/log/nginx/error.log` | nginx's own complaints |

The `available`/`enabled` split (same pattern as sshd drop-ins and
sudoers.d): write in `available`, enable with
`sudo ln -s ../sites-available/mysite /etc/nginx/sites-enabled/`,
disable by removing the symlink — config as switchable units.
The logs are [M24](../../../M24-logs-journald-monitoring/content/README.md)
text files: `tail -f`-able, greppable, pipe-able.

## 2. Server blocks — virtual hosts

One nginx, many websites. Each **server block** declares which
requests it answers — matched by port **and** the `Host` header
(the `server_name`):

```nginx
# /etc/nginx/sites-available/dashboard
server {
    listen 80;
    server_name dashboard.test;      # the name this site answers to

    root /home/ds/lab29/www;         # where files come from
    index index.html;

    access_log /var/log/nginx/dashboard.access.log;
}
```

Enable and test — with the discipline that never varies:

```console
$ echo "127.0.0.1 dashboard.test" | sudo tee -a /etc/hosts    # lab DNS (M21 §DNS)
$ sudo ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled/
$ sudo nginx -t                 # THE syntax gate — before any reload, always
$ sudo systemctl reload nginx   # re-read config; existing connections survive (M20)
$ curl -s http://dashboard.test/          # Host header now selects your block
```

Two nginx behaviors to internalize: **`nginx -t` before every
reload** (M25's config discipline — a broken config + restart
takes the front door down), and **first-match defaulting** — with
no matching `server_name`, nginx answers with the *default server*
(the first block listening on that port, or one marked
`default_server`). "Why is my request hitting the wrong site?" is
almost always the Host header not matching any `server_name` —
check with `curl -H "Host: dashboard.test" http://localhost/`.

## 3. Static files — the core job

`root` + `index` serve files by mapping the URI onto disk:
`GET /assets/style.css` → `/home/ds/lab29/www/assets/style.css`.
Permissions matter (M12/M13 in a new costume): nginx runs as
`www-data`, so the static tree must be readable *by www-data* —
`chmod 755` directories, `644` files, and `namei -l` (M13's
clinic tool) when a mysterious 403 appears.

```console
$ curl -sI http://dashboard.test/ | grep -E 'HTTP|Content-Type'
HTTP/1.1 200 OK
Content-Type: text/html
```

A 403 here is a *permissions* finding, not a web bug — and the
access log says so (`"GET / HTTP/1.1" 403`), while error.log names
the exact permission denied.

## 4. Location blocks — routing within a site

`location` blocks route paths to different handlers:

```nginx
server {
    listen 80;
    server_name dashboard.test;
    root /home/ds/lab29/www;

    location /api/ {                      # everything under /api/ → the app
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {                   # long-cache the assets
        expires 7d;
    }
}
```

Prefix matching (`location /api/`) sends that subtree to
`proxy_pass`; everything else falls through to static. The
trailing-slash semantics bite here too (M23's rule wearing
nginx): `proxy_pass http://127.0.0.1:8000` forwards the *original*
URI; `proxy_pass http://127.0.0.1:8000/` strips the location
prefix first — the difference between `/api/health` and `/health`
reaching your app. Lab 2 exercises both; pick deliberately and
comment it.

## 5. The reverse proxy — nginx in front of your app

That `proxy_pass` block *is* the reverse proxy: nginx accepts
public requests and forwards them to the app, which binds
**127.0.0.1:8000 only** — invisible except through nginx. What the
proxy buys:

- **One door** — TLS (Lesson 4), headers, and rate limits live in
  one place, not per-app.
- **Static offload** — nginx serves assets fast; the app process
  only handles dynamic work.
- **Buffering & resilience** — slow clients queue at nginx, not in
  the app; a brief app restart shows `502` instead of connection
  errors (and with `proxy_next_upstream`/retries, sometimes
  transparently).
- **The 502 signature** — when the app is down, nginx answers
  `502 Bad Gateway`: the *proxy is fine, the backend isn't*. The
  diagnosis order that follows: `systemctl --user status <app>` →
  `journalctl --user -u <app>` → is it listening?
  (`ss -tlnp | grep 8000`) — the M24 ladder, frontend-to-back.

The app side needs headers preserved (`proxy_set_header`) so it
sees the real Host and client IP; for WebSockets (Jupyter —
[M22's](../../../M22-ssh-remote-admin/content/README.md) tunnel
topic) two more lines (`Upgrade`/`Connection`) exist, named here
for recognition.

## 6. Logs — the stack's black box flight recorders

```console
$ sudo tail -3 /var/log/nginx/access.log
127.0.0.1 - - [15/Sep/2026:21:04:11 +0000] "GET /api/health HTTP/1.1" 200 15 "-" "curl/8.5.0"
```

The **combined log format**: client, timestamp, request line,
**status**, bytes, referrer, user-agent. The status column is your
fleet-wide error census: `awk '{print $9}' access.log | sort |
uniq -c` (M08/M24) — one pipeline, the API's health history.
error.log carries nginx's *own* view: permission denials, upstream
connection failures (the 502s), config warnings. Between the two
logs, "the site is down" becomes a timestamped, attributable
incident — M24's method with a professional data source.

## 7. nginx vs Apache — the comparison the interview asks

Both are excellent; the honest comparison at concept level:

| | **nginx** | **Apache (httpd)** |
|---|---|---|
| Model | event-driven, async — few processes, many connections | process/thread per request (mpm_event mitigates) |
| Config layout | `sites-available/enabled`, server blocks | `vhosts`, `mods-enabled`, `.htaccess` per-directory overrides |
| Strengths | static files, reverse proxy, high concurrency, low memory | ubiquity, `.htaccess` flexibility, decades of modules |
| Config dialect | its own concise DSL | XML-flavored directives, per-dir |

For this course's use — reverse proxy in front of app services —
nginx is the natural fit (and the DS-stack default: JupyterHub,
Grafana, every container stack proxies through it). Ubuntu ships
both (`apt install apache2` works identically); recognize Apache's
layout for the machines that have it, configure nginx fluently.

## 8. Try it now (15 minutes)

1. Install, verify, and *locate*: the four §1 commands, then
   `ls sites-enabled/` — who's answering on :80 right now?
2. Build the dashboard block (§2) with a one-line HTML file;
   `nginx -t` → reload → curl by name → curl with a *wrong* Host
   header and watch the default server answer. The Host-header
   mechanism, witnessed.
3. The 403 experiment: `chmod 700` the www directory, curl again
   (403), read `error.log`'s last line, fix permissions, re-curl.
   M13's clinic, in web form.
4. Log census: fire ten requests (mixed 200s and one 404), run the
   §6 status-census pipeline — your first access-log analysis,
   two minutes flat.

## 9. Common mistakes

- Skipping `nginx -t` — a config typo + `restart` = the whole
  front door down (and `sites-enabled/default` answered before you
  knew there was a default).
- Editing `nginx.conf` directly for a site change — use
  `sites-available` + symlink; the main file is the *includes*,
  not the sites.
- Forgetting `www-data` needs the path — every directory from `/`
  down needs execute for the traversal (namei -l diagnoses).
- The `proxy_pass` trailing slash — silently rewrites the path;
  test with `curl -v` through the proxy, not just direct.
- Debugging the app when access.log says 4xx — read the status
  class first (Lesson 1 §2); it halves the search space.

> **Up next:** [Lesson 3 — PostgreSQL](03-postgresql.md): the
> database under the stack — roles, databases, psql, CSV loading,
> and the backup command you'll schedule in M19 terms.
