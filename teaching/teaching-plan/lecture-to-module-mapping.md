# Lecture ↔ Module Mapping

> The cross-reference that keeps the 16-week plan honest against the
> 32-module curriculum. Both directions are given so a substitute
> instructor can answer "what do I teach Thursday?" *and* "where does
> M17 live?" instantly.

## Direction 1 — every module's teaching slot

| Module | Session(s) | Week | Notes |
|---|---|---|---|
| M01 What is Linux? | 1 | 1 | conceptual, no VM needed |
| M02 Distributions | 2 | 1 | short; pairs with M01 |
| M03 Architecture | 2 | 1 | layered-cake model |
| M04 Installing Ubuntu / VMs | 3–4 | 2 | hands-on install; snapshot discipline |
| M05 Terminal & Shell | 5 | 3 | first real command fluency |
| M06 Filesystem Hierarchy | 5 | 3 | |
| M07 Files & Directories | 6 | 3 | |
| M08 Text Processing Toolkit | 7–8 | 4 | two sessions: core tools; grep/sed/awk |
| M09 Pipes & Redirection | 8 | 4 | |
| M10 Bash Scripting | 9–10 | 5 | two sessions: core; functions/debugging |
| M11 Advanced Automation | 10 | 5 | |
| M12 Users, Groups & Permissions | 11 | 6 | |
| M13 Ownership & Shared Access | 11 | 6 | mini-project B territory |
| M14 Sudo & the Root Principle | 12 | 6 | |
| M15 Environment Variables | 12 | 6 | folded into the M14 session's second half |
| **Midterm consolidation** | 13 | 7 | review + practice circuit (M01–M13) |
| **Midterm examination** | 14 | 7 | in-repo paper, 2 h + live terminal |
| M16 Package Management | 15 | 8 | |
| M17 Storage & Filesystems | 15–16 | 8 | loopback disks |
| M18 Processes, Jobs & Signals | 17 | 9 | |
| M19 Scheduling (cron/timers) | 18 | 9 | + M15 env-in-cron recap |
| M20 systemd & Services | 19 | 10 | |
| M21 Networking Fundamentals | 20 | 10 | |
| M22 SSH & Remote Administration | 21 | 11 | |
| M23 File Transfer (scp/sftp/rsync) | 22 | 11 | builds on M22 key workflow |
| M24 Logs, journald & Monitoring | 23–24 | 12 | incl. performance clinic streams |
| M25 Security & Firewall | 24 | 12 | hardening checklist |
| M26 Git & Dev Workflows | 25 | 13 | |
| M27 Python, Jupyter & Data | 26 | 13 | venv/Jupyter on Linux |
| M28 Docker & Containers | 27 | 14 | |
| M29 Web Servers, DBs & Deployment | 28 | 14 | nginx + PostgreSQL basics |
| M31 DS Server (companion) | 29 | 15 | the "day on an ML server" narrative |
| M32 Performance Clinic (companion) | 29 | 15 | 8-step method + drill book |
| **Final revision** | 30 | 15 | revision room + practical-exam prep |
| **Practical examination** | 31 | 16 | staged-server circuit, 90 min |
| **Final exam / capstone defense** | 32 | 16 | final paper window; capstone vivas |

## Direction 2 — every session's content

| Session | Week | Content | Deck section |
|---|---|---|---|
| 1 | 1 | Course intro + M01 | U1 §1–2 |
| 2 | 1 | M02 + M03 | U1 §3–4 |
| 3 | 2 | M04 install lab (part 1) | U1 §5 |
| 4 | 2 | M04 snapshots + M04→M05 bridge | U1 §5–6 |
| 5 | 3 | M05 + M06 | U2 §1–2 |
| 6 | 3 | M07 | U2 §3 |
| 7 | 4 | M08 core tools | U2 §4 |
| 8 | 4 | M08 grep/sed/awk + M09 | U2 §5 |
| 9 | 5 | M10 core scripting | U3 §1 |
| 10 | 5 | M10 cont. + M11 | U3 §2–3 |
| 11 | 6 | M12 + M13 | U4 §1 |
| 12 | 6 | M14 + M15 | U4 §2–3 |
| 13 | 7 | Midterm consolidation | — |
| 14 | 7 | **Midterm** | — |
| 15 | 8 | M16 + M17 part 1 | U5 §1–2 |
| 16 | 8 | M17 part 2 (loopback lab) | U5 §2 |
| 17 | 9 | M18 | U5 §3 |
| 18 | 9 | M19 | U5 §4 |
| 19 | 10 | M20 | U6 §1 |
| 20 | 10 | M21 | U6 §2 |
| 21 | 11 | M22 | U6 §3 |
| 22 | 11 | M23 | U6 §4 |
| 23 | 12 | M24 lessons 1–3 | U6 §5 |
| 24 | 12 | M24 monitoring + M25 | U6 §6 |
| 25 | 13 | M26 | U7 §1 |
| 26 | 13 | M27 | U7 §2 |
| 27 | 14 | M28 | U7 §3 |
| 28 | 14 | M29 | U7 §4 |
| 29 | 15 | M31 + M32 | U8 §2 |
| 30 | 15 | Final revision | U8 §3 |
| 31 | 16 | **Practical exam** | — |
| 32 | 16 | **Final + capstone defense** | — |

## Compression policy (honest statement)

- Modules compressed to a **half-session** (M02, M03, M06, M09, M11, M13,
  M15): each is either conceptual, short, or a natural appendage to its
  neighbor. Their *labs* are full homework labs — compression applies to
  contact time, not practice volume.
- Modules with **two full sessions** (M08, M10, M24) carry the heaviest
  DS-critical skill load (text pipelines, scripting, observability).
- Nothing from the 30-module spine is dropped. The two-semester variant
  simply gives every module one session (15 weeks × 2 = 30 slots + intro
  + exam weeks), removing all compression.
