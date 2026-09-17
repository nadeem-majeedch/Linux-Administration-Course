# Module 22 Labs — SSH & Remote Administration

> Two labs. The "remote" machine is always **your own VM** (addressed
> via localhost / the `vm` alias), or your own host from inside the
> VM. No external hosts, no shared servers, no real credentials —
> lab keys only, kept out of any repo.

| # | Lab | Focus | Time |
|---|-----|-------|------|
| 1 | [lab-01-key-workflow.md](lab-01-key-workflow.md) | The full key workflow: generate → deploy → agent → ssh-config → passwordless verified; fingerprints & first-contact decisions | ~50 min |
| 2 | [lab-02-diagnosis-clinic.md](lab-02-diagnosis-clinic.md) | Five broken-SSH patients — permissions, agent, known_hosts, config resolution, tunnel — symptoms only | ~50 min |

Standing rules (recap):

- `~/.ssh` stays `700`; private keys `600`; `chmod 644` only happens
  as a *deliberate* break, immediately repaired.
- sshd_config is **read and analyzed, never edited** in this module
  (M25 applies hardening).
- `ssh -G`, `ssh -v`, `ls -l ~/.ssh`, `ssh-add -l` are the evidence
  tools; every clinic diagnosis cites one.
- All transcripts to `lab-log.md`, fingerprints and error messages
  verbatim.
