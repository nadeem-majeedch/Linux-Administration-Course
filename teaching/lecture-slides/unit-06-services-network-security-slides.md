# Unit 6 Lecture Slides — Services, Network & Security (M20–M25)

> **Delivery:** Sessions 19–24 · Speaker notes:
> [../speaker-notes/unit-06-services-network-security-notes.md](../speaker-notes/unit-06-services-network-security-notes.md)

---

# Slide 1 — Title

## Slide Content
**Unit 6 — Services, Network & Security**
systemd · Networking · SSH · File transfer · Logs & monitoring · Firewall (M20–M25)
*The unit where your machine starts serving — and defending*

## Instructor Delivery Notes
Six sessions; keep the through-line visible: "everything here is about
*trust across a boundary* — services you trust to run, hosts you trust
to talk to, users you trust to log in."

## Visual or Demonstration Suggestion
`systemctl list-units --type=service --state=running | head` — "your machine already runs dozens of servers."

## Student Question
"Which programs are running on your VM *right now* that you didn't start?"

---

# Slide 2 — systemd: units, states, verbs

## Slide Content
- A **unit** = anything systemd manages; services are `.service` files
- Lifecycle verbs: `start · stop · restart · reload · status`
- **enable ≠ start**: `enable` wires the *boot graph* (a symlink in `multi-user.target.wants`); `start` runs it *now*
- `systemctl status` is evidence: state, PID, recent log lines
- User units (`--user`) run without root — this course's practice ground

## Instructor Delivery Notes
enable-vs-start is the unit's first misconception — draw the boot graph.
Read a `status` output like a chart: loaded/active/PID/memory — every
field is a later diagnostic hook.

## Visual or Demonstration Suggestion
Break a user unit's ExecStart path → `status` shows `activating (auto-restart)` → journal shows the exec failure.

## Student Question
"A service is 'enabled' but dead. Is that a contradiction? What state is it in at boot?"

---

# Slide 3 — Networking: the layered address system

## Slide Content
- **MAC**: hardware, local link only · **IP**: routable across networks
- IPv4 `192.168.1.20/24` — the `/24` is the subnet mask in disguise
- Loopback `127.0.0.1` — *this machine only*; the course's safe test bed
- DHCP assigns IPs; DNS turns names into IPs
- Tools: `ip addr` (modern; `ifconfig` is legacy), `ping`, `dig`

## Instructor Delivery Notes
Layer discipline: MAC gets you onto the street, IP routes across towns,
DNS is the phone book. All network *labs* are loopback — say why (safety
and reproducibility), not just that.

## Visual or Demonstration Suggestion
`ip addr show` → find lo, the v4, the v6. `dig example.com +short` — name→IP in one line.

## Student Question
"Your laptop's IP changes between networks. What usually doesn't? Why?"

---

# Slide 4 — Ports & sockets: doors on a host

## Slide Content
- Port = numbered door; socket = an *open* conversation
- `ss -tlnp` — listening doors and their owners (the tool of record)
- Well-known: 22 ssh · 80/443 web · 5432 PostgreSQL · 8888 Jupyter-typical
- "Connection refused" = host reachable, door closed — *diagnostic gold*

## Instructor Delivery Notes
Refused vs timeout distinction is the six-rung ladder's hinge (rung 4
vs rung 3): refused means you *reached* the machine. Read `ss` output
live on their VMs — find sshd's 22.

## Visual or Demonstration Suggestion
Start a Python http.server on 8000; watch `ss -tlnp` grow a line. Stop it; watch it shrink.

## Student Question
"Jupyter 'won't start'. What does `ss -tlnp | grep 8888` tell you instantly?"

---

# Slide 5 — Knowledge check

## Slide Content
1. `enable --now foo` does what two things?
2. `ping 127.0.0.1` works, `ping 8.8.8.8` times out — which rung failed?
3. `ss` shows nothing on 8888 — is Jupyter's problem *network*?

## Instructor Delivery Notes
Q3 is the ladder's first lesson: no listener means the problem is
*before* networking — the app itself. Resist explaining; ask which rung
would have caught it.

## Visual or Demonstration Suggestion
— 

## Student Question
(Q3 is the check)

---

# Slide 6 — SSH: the remote-everything protocol

## Slide Content
- SSH = encrypted, authenticated shell *and* file transfer *and* tunnels
- Keys beat passwords: `ssh-keygen -t ed25519` → public key to the server's `authorized_keys`
- Private key = identity; **never leaves your machine**; passphrase-protect it
- `known_hosts` = the server's fingerprint — TOFU (trust on first use), then *alarm on change*
- `ssh_config` aliases: `Host lab → HostName, User, IdentityFile`

## Instructor Delivery Notes
Key anatomy: what the public key *is* (a lock) vs private (its key).
The host-key-changed choreography is rehearsed in the lab — today,
narrate the fear correctly: changed fingerprint under known conditions =
re-issue, not ignore.

## Visual or Demonstration Suggestion
`ssh -v localhost` grep the auth exchange — watch the key get *offered*.

## Student Question
"Why does the private key get a passphrase if it's already on your disk?"

---

# Slide 7 — File transfer: choosing the tool

## Slide Content
- `scp file vm:~/` — one-shot copy (simple, stateless, restarts from zero)
- `sftp` — interactive session (browse, get/put several)
- `rsync -avh` — the sync engine: compares, moves *differences*, **resumes**
- rsync trailing slash: `src/` = contents · `src` = the directory itself
- `--delete` never without `--dry-run` first — *course policy, graded*

## Instructor Delivery Notes
The interrupt-and-resume demo (5 GB scale-down: 200 MB) is the sell:
kill rsync mid-flight, rerun, watch it skip done work. scp in the same
race restarts — the numbers speak.

## Visual or Demonstration Suggestion
Split: `scp` restart (full re-transfer) vs rsync resume (partial + catch-up) side by side.

## Student Question
"Your sync deleted a folder on the server you meant to keep. What two course rules were skipped?"

---

# Slide 8 — Knowledge check

## Slide Content
1. `-rw-r-----` on your `~/.ssh/authorized_keys` — accepted or refused? Why?
2. `rsync -a src dst/` vs `rsync -a src/ dst/` — where do files land?
3. `speedup is 2.98` — interpret like a statistician.

## Instructor Delivery Notes
Q1 welds Unit 4 onto SSH (M22's lab covers it — that permission failure
message is famous). Q3: total_size ÷ sent — they *can* do this math.

## Visual or Demonstration Suggestion
— 

## Student Question
(Q2 is the check — slash discipline)

---

# Slide 9 — journald & journalctl: the service's memory

## Slide Content
- journald collects *everything*: service stdout/stderr, syslog, kernel
- Structured, indexed — **query, don't grep raw files**
- Verbs: `journalctl -u NAME` · `-f` follow · `--since/-e/-n` · `-p err`
- Logs as evidence: quote lines, timestamp them, then reason
- `/var/log` still exists (apt, auth, kern) — classic world alongside

## Instructor Delivery Notes
The anti-pattern named: `grep` inside `/var/log/journal` finds binary
soup — journalctl's index is the interface. Live query building: from
"service failed" to the exact exec error in three commands.

## Visual or Demonstration Suggestion
`journalctl -u healthbot -n 20 --no-pager` on a crash-looping unit — read the error aloud like a chart.

## Student Question
"Show the last 10 errors *only* — which flags combine?"

---

# Slide 10 — Monitoring: reading vital signs

## Slide Content
- `uptime` load · `free -h` memory (available ≠ free!) · `df -h` space
- `top`/`htop`: %CPU per core, RES memory, load trend
- `vmstat 1`: run queue, swap-in/out (si/so — swapping *is* the emergency)
- The habit: baseline → anomaly → evidence → method (8 steps, M32)

## Instructor Delivery Notes
free's `available` column fixes the top misread ("used is high!
panic") — cache is used-but-reclaimable. si/so nonzero *persistently* =
memory pressure = the server is dying politely.

## Visual or Demonstration Suggestion
Run a memory-hog script; watch `free -h` available drop and si/so wake up.

## Student Question
"used: 7.2G, free: 200M, available: 5.9G. Crisis? Explain."

---

# Slide 11 — Security: the perimeter and the practice

## Slide Content
- Threat model for a lab server: exposed services, weak auth, stale software, secrets in files
- **UFW**: default deny incoming; allow *justified* ports — `ufw allow 22/tcp`, `ufw status verbose`
- SSH hardening: key-only, no root login, (PasswordAuthentication no — with rollback documented)
- Updates = patching known holes; `apt upgrade` is a security act
- Secrets: `600` env files *outside* the repo; never in shell history

## Instructor Delivery Notes
Every rule gets a *why*: default-deny (you can't enumerate what you
forgot), key-only (passwords brute-force, keys don't), 600 env files
(least privilege for files). M25's checklist is the graded artifact —
preview it.

## Visual or Demonstration Suggestion
`ufw status verbose` before/after: deny-all + two justified allows.

## Student Question
"Which port must your allow-list keep open, and what breaks if you forget?"

---

# Slide 12 — Knowledge check

## Slide Content
1. `journalctl -u web -p err --since -1h` — what exactly appears?
2. UFW default-deny is on. SSH still works. Which rule keeps you in?
3. You see si/so constantly nonzero in vmstat. Diagnosis?

## Instructor Delivery Notes
Q2 is the classic self-lockout check — the answer (22/tcp rule) is also
the *practical exam* trap; students who answer this earn their first
staged-server point.

## Visual or Demonstration Suggestion
— 

## Student Question
(Q2 is the check)

---

# Slide 13 — Common mistakes (Unit 6)

## Slide Content
- `systemctl enable` and wondering why nothing ran
- Debugging the network while no listener exists (rung order violated)
- `--delete` without rehearsal — the sync that ate the dataset
- `grep` on journal directories instead of `journalctl`
- ufw allow 22 *after* enabling default-deny — from a different terminal, or not at all

## Instructor Delivery Notes
The ufw self-lockout has a safe rehearsal in M25's lab (with a second
session open *before* enabling) — teach the open-second-session habit
as professional muscle.

## Visual or Demonstration Suggestion
Two-terminal ufw demo: one session proves the rule, the other stays alive as insurance.

## Student Question
"Which mistake is only *partially* recoverable — and why?"

---

# Slide 14 — Data Science connection

## Slide Content
- The GPU server you'll use *is* this unit: SSH in, keys set, rsync datasets, tmux sessions, journald when training crashes
- Jupyter over a tunnel = port-forwarding (M22 lab)
- Data pipelines = scheduled + logged (M19×M24)
- The capstone's serving stack: API as a *user unit* behind nginx — this unit's verbs

## Instructor Delivery Notes
Map slides to capstone areas 4–6 (serving, security, observability) —
this unit is worth ~1/3 of the capstone rubric; say it out loud.

## Visual or Demonstration Suggestion
Capstone architecture diagram with this unit's topics highlighted.

## Student Question
"Which capstone phase scares you most? (It's Operate — this unit is the antidote.)"

---

# Slide 15 — Summary & exit ticket

## Slide Content
**Summary:** systemctl lifecycle + enable≠start · layered net + doors
(ss) + rungs · SSH keys/TOFU/tunnels · transfer with verification ·
journalctl-as-interface · vital signs · default-deny with justification
**Exit ticket:** one-line each: enable vs start; refused vs timeout;
why 600 on key files?
**HW:** M20–M25 quizzes · LA-4/LA-5 prep · A3 progress

## Instructor Delivery Notes
These exit answers are the practical exam's warm-up items — grade the
pattern, reteach weak spots at S29's warm-up.

## Visual or Demonstration Suggestion
—

## Student Question
(exit ticket is the question)

---

## Deck references
- Modules: [M20](../../modules/M20-systemd-services/README.md) · [M21](../../modules/M21-networking-fundamentals/README.md) · [M22](../../modules/M22-ssh-remote-admin/README.md) · [M23](../../modules/M23-file-transfer/README.md) · [M24](../../modules/M24-logs-journald-monitoring/README.md) · [M25](../../modules/M25-security-firewall/README.md)
- Next deck: [Unit 7 — The Data Science Stack](unit-07-data-science-stack-slides.md)
