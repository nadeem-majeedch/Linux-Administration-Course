# CLO × Module Mapping Matrix

> Companion to [CLO-ASSESSMENT-ALIGNMENT.md](CLO-ASSESSMENT-ALIGNMENT.md)
> (which defines the proposed CLOs and maps them to assessments).
> This grid answers the reviewer's question in the other direction:
> *where in the course is each CLO developed?*
>
> Cell codes: **●** primary home (objectives explicitly target it) ·
> **○** reinforcing practice (content supports it, objectives don't
> lead with it). Derivation: module objectives read from
> [COURSE-ROADMAP.md](../COURSE-ROADMAP.md) and module READMEs; no
> module content was modified to fit this grid.

| Module | CLO-1 CLI/text | CLO-2 Scripting | CLO-3 Identity/permissions | CLO-4 Pkg/storage/services/sched | CLO-5 Network/SSH/transfer | CLO-6 Logs/monitoring/method | CLO-7 DS stack |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| M01 What is Linux? | ○ | | | | | | |
| M02 Distributions | ○ | | | ○ | | | |
| M03 Architecture | ○ | | | ○ | | ○ | |
| M04 Installing Ubuntu / VMs | | | | ○ | | | ○ |
| M05 Terminal & Shell | ● | ○ | | | | | |
| M06 Filesystem Hierarchy | ● | | | | | | |
| M07 Files & Directories | ● | | ○ | | | | |
| M08 Text Processing Toolkit | ● | ○ | | | | | ○ |
| M09 Pipes & Redirection | ● | ○ | | | | | ○ |
| M10 Bash Scripting | ○ | ● | | | | | ○ |
| M11 Advanced Shell & Automation | ○ | ● | | ○ | | | ○ |
| M12 Users, Groups & Permissions | | | ● | | | | |
| M13 Ownership & Shared Access | | | ● | | | | |
| M14 Sudo & the Root Principle | | | ● | | | | |
| M15 Environment Variables | ○ | ○ | | | | | ○ |
| M16 Package Management | | | | ● | | | ○ |
| M17 Storage & Filesystems | | | | ● | | | |
| M18 Processes, Jobs & Signals | | ○ | | ○ | | ● | |
| M19 Scheduling: cron & timers | | ● | | ● | | | ○ |
| M20 systemd, Services & Boot | | | | ● | | ○ | |
| M21 Networking Fundamentals | | | | | ● | ○ | |
| M22 SSH & Remote Administration | | | | | ● | ○ | ○ |
| M23 File Transfer (SCP/SFTP/rsync) | | | ○ | | ● | | ○ |
| M24 Logs, journald & Monitoring | | | | | | ● | |
| M25 Security & Firewall | | | ○ | | ● | ○ | |
| M26 Git & Development Workflows | | | | | | | ● |
| M27 Python, Jupyter & Data | ○ | | | | | | ● |
| M28 Docker & Containers | | | | | | | ● |
| M29 Web Servers, Databases & Deployment | | | | ● | ○ | | ● |
| M30 Capstone | ○ | ● | ● | ● | ● | ● | ● |
| M31 DS Server (companion) | | ○ | | ○ | ● | ● | ● |
| M32 Performance & Troubleshooting Clinic (companion) | | | | | | ● | ○ |

**Reading notes**

- **Every CLO has at least two primary homes plus capstone
  demonstration** — no CLO is a single-module orphan:
  CLO-1 (M05–M09), CLO-2 (M10–M11), CLO-3 (M12–M14), CLO-4
  (M16–M20), CLO-5 (M21–M23, M25), CLO-6 (M18, M24, M32), CLO-7
  (M26–M29).
- **Sequential reinforcement is real, not decorative:** scripting
  appears in five modules before the capstone demands it; the
  evidence-first method (CLO-6) starts in M03's layer attribution
  and matures through M24/M32.
- **The companion row (M31/M32)** mirrors the repository's actual
  structure: both are content-complete companions to the capstone
  unit, not part of the 30-module teaching spine.

*Assessment mapping per CLO (which instrument measures what) lives
in [CLO-ASSESSMENT-ALIGNMENT.md](CLO-ASSESSMENT-ALIGNMENT.md) §2–4.*
