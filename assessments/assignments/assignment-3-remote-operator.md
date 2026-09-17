# Assignment 3 — The Remote Operator

> Covers M20–M25, M27–M28 (services, SSH, security, logs, Python
> envs, Git, Docker) · 5% of course grade · due end of week 15 ·
> individual work. Environment: your own Ubuntu VM as the "server";
> your laptop as the operator seat.

## The story

You are the operator of a tiny ML service. Everything you do from
now on happens **over SSH** — the VM console is off-limits for this
assignment and using it is the first thing the transcript will
reveal.

## Deliverables

### 1. Key-only access, hardened (20%)

- Dedicated Ed25519 key for this assignment; `ssh_config` alias
  `a3srv`.
- Server: password authentication refused *for your user only* —
  via a drop-in (`/etc/ssh/sshd_config.d/`), with the
  before/after evidence and **a documented rollback command** (a
  hardening step without a rollback path loses the points).
- Prove: a failed password attempt is impossible from the client
  (`ssh -o PubkeyAuthentication=no a3srv` must be refused), and
  `sshd -T | grep -E 'passwordauthentication|pubkeyauthentication'`
  output attached.

### 2. The service, as a unit (25%)

- `model-api.service` (user unit): serves a tiny Flask/FastAPI
  `GET /health` returning `{"status":"ok"}` from a venv you built.
- Restart on failure, starts at login (default target), logs to the
  journal — prove each property with the corresponding command.
- Inject one failure (delete the venv's flask), capture the
  crash-loop in `journalctl`, then repair and show recovery. The
  incident section (before/after + decisive journal line) goes in
  `evidence/incident.md`.

### 3. Container twin (20%)

- Same app packaged in a container (Dockerfile submitted) bound to
  a VM port ≥ 10000, data/config via a read-only bind mount where
  applicable.
- Prove: `docker logs` shows requests, `curl` from your *laptop*
  through a published port reaches it, and a resource limit (`--memory`)
  is set and visible via `docker inspect`.

### 4. Defense sheet (25%)

`DEFENSE.md` — the viva-facing page, one paragraph per answer, each
grounded in a command you actually ran (quote it):

1. Why key-only beats long passwords here (mechanism, not slogans).
2. What your unit's `Restart=` choice trades away — describe a
   failure where it makes things worse.
3. Where each secret in this assignment lives, and the command
   proving none are in the repo or the journal.
4. Your three-line "service down" runbook for *this* service —
   commands, not prose.
5. One thing containers make *worse* for debugging, with the
   counter-technique you'd use.

### 5. Git hygiene (10%)

- All work committed in a course repo with meaningful history
  (≥ 6 commits showing real increments, not one blob).
- `git log --stat` excerpt attached proving no secret ever entered
  history; theDEFENSE/venv/.env classes are `.gitignore`d from the
  first commit.

## Submission

Repo URL + `a3.log` (client-side transcript) + server-side
`journalctl` excerpt file. Both sides required — an operator works
in two places.

## Grading (100 pts → 5%)

| Area | Pts | Hard rules |
|---|---|---|
| Key-only + hardening | 15 | rollback documented; `sshd -T` proof attached |
| Unit correctness | 10 | all three properties proven, not claimed |
| Incident section | 15 | decisive journal line quoted; recovery shown |
| Container twin | 15 | laptop-side curl proof; limits visible in inspect |
| Defense sheet | 30 | 6 pts per answer; unquoted claims cap at 3 pts each |
| Git hygiene | 10 | incremental history; secrets absent from day one |
| Transcripts (both sides) | 5 | complete sessions |

**Penalties:** password auth disabled system-wide instead of
per-user −10; secrets in any commit −15 plus mandatory history
remediation before resubmission; VM console use after Task 1 is
confirmed −20.
