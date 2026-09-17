# Module 29 Quiz — Web Servers, Databases & Deployment

> 22 questions. Answer first, then check [quiz-answers.md](quiz-answers.md).
> Scope: lessons 1–4.

## Section A — HTTP & the request path (Q1–5)

**Q1.** Write the four HTTP methods a DS person needs, with the
side-effect rule for GET.

**Q2.** Status-code classes: what does each of 2xx/3xx/4xx/5xx
mean, and what is the *first diagnostic fork* the 4xx/5xx split
gives you?

**Q3.** `502 Bad Gateway` — what does it say about the proxy vs
the app, and what are the first three commands you run?

**Q4.** Name the hops of the module's request path, in order,
noting which hop is the only network-facing one.

**Q5.** The curl one-liner for "status code + latency", and why
that pair is the health-check idiom.

## Section B — nginx (Q6–11)

**Q6.** Explain `sites-available` vs `sites-enabled` — and the
command that connects them.

**Q7.** What selects a server block when several listen on :80 —
and what happens when nothing matches?

**Q8.** Why `nginx -t` before every reload? State the failure it
prevents.

**Q9.** `reload` vs `restart` for nginx — what does each do to
live connections?

**Q10.** In `location /api/ { proxy_pass http://127.0.0.1:8000; }`
— what URI does the app receive for a request to `/api/health`?
What changes with a trailing slash on `proxy_pass`?

**Q11.** A 403 from a static site: which log names the cause, and
which two permission bits are the usual suspects?

## Section C — PostgreSQL (Q12–17)

**Q12.** Cluster vs database: state the relationship, and what
Ubuntu creates on install.

**Q13.** Why does administration go through `sudo -u postgres psql`
— and what is peer authentication?

**Q14.** Why should your app connect as `appuser`, not `postgres`?
(A principle and a consequence.)

**Q15.** `\copy` vs `COPY`: which does the course use and why?

**Q16.** `pg_dump -Fc` then restore: write the three commands
(dump, scratch target, restore) and the verification that must
follow.

**Q17.** `pg_hba.conf` — what does it control, and which classic
error message points at it?

## Section D — deployment & TLS (Q18–22)

**Q18.** In the `api.service` unit: what do `EnvironmentFile`,
`Restart=on-failure`, and `MemoryMax` each buy the deployment?

**Q19.** Why does the DB password live in `api.env` (600) rather
than the unit file or the code? (Two mechanisms, one principle.)

**Q20.** The app restart vs nginx reload: what does each disturb,
and why is the front door never restarted for an app change?

**Q21.** Certificate, CA, self-signed: define each in one line,
and state when a self-signed cert is appropriate.

**Q22.** TLS terminates at nginx — what travels from nginx to the
loopback app, and why is that acceptable?

## Bonus (Q23) — the morning incident

09:14: `curl dashboard.test/api/health` returns 502. You have the
three log sources. Draft the six-step (M24) diagnosis as commands,
in order, with what each would tell you.
