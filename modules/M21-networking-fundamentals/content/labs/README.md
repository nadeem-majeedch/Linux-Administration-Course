# Module 21 Labs — Networking

> Two labs, entirely **localhost / own-VM**. The module safety
> contract applies with full force: no scanning or probing of external
> systems, university networks, or hosts you don't own. All break-fix
> happens to services *you* started on *your* machine.

| # | Lab | Focus | Time |
|---|-----|-------|------|
| 1 | [lab-01-local-network-lab.md](lab-01-local-network-lab.md) | Map your own machine: interfaces, routes, resolvers, sockets; the health check | ~45 min |
| 2 | [lab-02-diagnosis-clinic.md](labs/lab-02-diagnosis-clinic.md) | Three local incidents (DNS, port, route) — diagnose with the layered playbook | ~50 min |

Standing rules (recap):

- Servers you start bind to `127.0.0.1` explicitly.
- `tcpdump` captures loopback (`-i lo`) only.
- Every diagnosis uses the six-rung ladder — evidence before verdicts.
- `lab-log.md` holds transcripts; the labs grade the evidence.
