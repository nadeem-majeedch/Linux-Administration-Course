# Quiz Bank — format standard + module index

> Every quiz: 8–10 questions, 20 minutes, closed book. Format
> constraint: **every question presents a situation or evidence
> artifact** — a command output, an error, a scenario — and asks for
> diagnosis, prediction, or justification. No "define X". No
> "which flag does Y".
>
> **Where the quizzes live:** the bank is complete as per-module
> practice quizzes at `modules/M*/content/practice/quiz.md` (+
> answer keys) — ~620 questions across M01–M32, audited against the
> anti-memorization rules below. This directory holds the **format
> exemplar** ([quiz-m12.md](quiz-m12.md), key alongside) that new
> quiz authors copy, plus this index.

## Module quiz index (pointers into modules/)

| Module | Quiz (in `modules/<dir>/content/practice/`) | Reasoning tested |
|---|---|---|
| M01 what-is-linux | quiz.md | OS/kernel/distro distinctions applied to statements about real systems |
| M02 linux-distributions | quiz.md | Distro identification from evidence; verification reasoning |
| M03 linux-architecture | quiz.md | Layer attribution: given a symptom, which layer owns it |
| M04 installing-linux-vms | quiz.md | Environment choices and snapshot/restore reasoning |
| M05 terminal-and-shell | quiz-aliases-history.md | Help-system navigation, alias/history semantics |
| M06 filesystem-hierarchy | quiz.md | Path resolution and FHS placement from descriptions |
| M07 files-and-directories | quiz.md | Glob prediction and inode/link consequences |
| M08 text-processing | quiz.md | Pipeline design given data and constraints |
| M09 pipes-and-redirection | quiz.md | Redirection semantics: where does the byte go |
| M10 bash-scripting | quiz.md | Script debugging: given broken script + output, fix and justify |
| M11 advanced-shell-automation | quiz.md | Automation design: idempotency and failure handling |
| M12 users-groups-permissions | quiz.md (+ [exemplar](quiz-m12.md)) | Permission failure diagnosis from error + `ls -l` evidence |
| M13 ownership-shared-access | quiz.md | Shared-access design: SGID/sticky/ACL selection with trade-offs |
| M14 sudo-root-principle | quiz.md | sudo policy reasoning and incident interpretation |
| M15 environment-variables | quiz.md | Environment inheritance diagnosis (cron/script/sudo cases) |
| M16 package-management | quiz.md | apt failure triage and repository trust reasoning |
| M17 storage-and-filesystems | quiz.md | `df`/`du` contradiction resolution, mount reasoning |
| M18 processes-jobs-signals | quiz.md | Signal selection and process-state interpretation |
| M19 scheduling-cron-timers | quiz.md | Cron environment traps and timer design |
| M20 systemd-services | quiz.md | Unit failure triage from `systemctl`/journal evidence |
| M21 networking-fundamentals | quiz.md | Network layer-by-layer diagnosis from tool outputs |
| M22 ssh-remote-admin | quiz.md | SSH failure diagnosis: auth, keys, config, tunnels |
| M23 file-transfer | quiz.md | Transfer tool selection, rsync semantics (`--delete`/slash/verification) reasoning |
| M24 logs-journald-monitoring | quiz.md | Log/journal forensics and monitoring interpretation |
| M25 security-firewall | quiz.md | Firewall logic and hardening trade-offs |
| M26 git-dev-workflows | quiz.md | Git history reasoning: what did this command change |
| M27 python-jupyter-data | quiz.md | Python environment failure diagnosis |
| M28 docker-containers | quiz.md | Container lifecycle, volumes, and build-cache reasoning |
| M29 web-servers-databases | quiz.md | Web/db service diagnosis and reverse-proxy reasoning |
| M30 capstone | — | assessed via [../project-rubric.md](../project-rubric.md) + [../viva-questions.md](../viva-questions.md) |
| M31 data-science-server | — | assessed via [labs/ Level 5](../../labs/level-5-ds-server.md) + capstone |
| M32 performance-troubleshooting (companion) | [quiz](../../modules/M32-linux-performance-troubleshooting/content/practice/quiz.md) | The 8-step method, method-graded |

## Writing standard (for contributors)

Each quiz file: header with scope + time; Sections A/B/C in the
exemplar's shape — evidence interpretation, scenario diagnosis,
design/justify. Answer keys **must** include: the reasoning, the
common wrong answer, and what evidence would settle the question in
real life. See [quiz-m12.md](quiz-m12.md) as the format exemplar.
