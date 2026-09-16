# Module 21 — Networking Fundamentals · Content Index

> **Status:** Content complete — 5 lessons, 2 labs, quiz + key, 8
> challenges, troubleshooting guide.
> Module contract: [../README.md](../README.md) · Difficulty: Advanced.

> 🟡 **Module safety contract:** all labs and challenges run against
> **localhost** or your own VM. No scanning, probing, or traffic
> generation against external systems, university networks, or any host
> you don't own — that's policy at every employer, and it's policy here.
> (Passive observation of your *own* machine's connections is fine.)

## Lessons

| # | File | Topic |
|---|------|-------|
| 1 | [01-networking-fundamentals.md](lessons/01-networking-fundamentals.md) | IP/MAC/interfaces/subnets/gateways/routing; the layered model that organizes every diagnosis |
| 2 | [02-ip-and-routing.md](lessons/02-ip-and-routing.md) | the `ip` toolkit: addr/link/route, reading your machine's config, the DNS/DHCP roles |
| 3 | [03-dns-resolution.md](lessons/03-dns-resolution.md) | resolution chain, /etc/hosts, systemd-resolved, dig/host/resolvectl, DNS diagnosis |
| 4 | [04-ports-tcp-udp-sockets.md](lessons/04-ports-tcp-udp-sockets.md) | TCP vs UDP, ports, sockets, loopback, ss, the three-way handshake, connection states |
| 5 | [05-http-tools-diagnosis.md](lessons/05-http-tools-diagnosis.md) | curl/wget, nc, tcpdump intro, the **layered diagnosis playbook**, DS network scenarios |

## Labs

| # | File | Task |
|---|------|------|
| 1 | [lab-01-local-network-lab.md](labs/lab-01-local-network-lab.md) | Map your own machine: interfaces, routes, resolution, sockets — then the four-command health check |
| 2 | [lab-02-diagnosis-clinic.md](labs/lab-02-diagnosis-clinic.md) | Three local break-and-fix incidents (DNS, port, route) using the layered playbook |

## Practice & Support

- [Quiz](practice/quiz.md) (22 Q) · [Answer key](practice/quiz-answers.md)
- [Challenges](practice/challenges.md) (C1–C8)
- [Troubleshooting](troubleshooting.md) — 10 symptom→cause→fix patterns

## Cross-references

- [M20 systemd](../../M20-systemd-services/content/README.md) —
  ssh/nginx are services with listening sockets; NetworkManager/systemd-
  networkd are units too.
- [M22 SSH](../../M22-ssh-remote-admin/README.md) — everything here is
  the foundation SSH builds on.
- [M25 firewall](../../M25-security-firewall/README.md) — firewalls
  filter exactly the ports/sockets this module teaches.
- [M29 web/db servers](../../M29-web-servers-databases/README.md) —
  where listening sockets become applications.
