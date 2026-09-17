# Quiz Bank v2 — Answer Key & Grading Guide

> **INSTRUCTOR ONLY.** Student paper: [../quiz-bank-v2.md](../quiz-bank-v2.md)
> (not linked from student navigation; see [distribution policy](../../../instructor-resources/INSTRUCTOR-ONLY.md)).
>
> Grading guide: MCQ auto-scorable. Interpretation/output items graded
> on mechanism — a correct answer with wrong vocabulary loses a point,
> not the item. Every distractor note names the misconception it
> encodes ([bank](../../../instructor-manual/common-misconceptions.md)).

## Section A — MCQ (1 pt each)

| # | Key | The mechanism | Distractor encodes |
|---|---|---|---|
| A1 | **b** | isolation asymmetry: user-space faults are contained | (a) "kernel crash = app crash" |
| A2 | **c** | Fedora = Red Hat family → dnf | family blindness (apt reflex) |
| A3 | **a** | relative from cwd — you're already in the named dir | `../` overuse; `~` = home confusion |
| A4 | **b** | uniq collapses *adjacent* equals → sort first; -rn for "most first" | (a/d) uniq-without-sort; (d) double-sort noise |
| A5 | **b** | stdout → file; `2>` discards stderr; redirect ≠ filter | (a) merging streams by instinct |
| A6 | **b** | quoting survives word splitting on spaces | "quotes = verbosity" |
| A7 | **b** | the *matching triplet* is the source of truth (group: r--) | owner-triplet misread |
| A8 | **a** | dir base 777 − 027 = 750 | file-base arithmetic (640) |
| A9 | **b** | deleted-but-open: fd held, space freed at exit | "df lies"/units-confusion myths |
| A10 | **b** | TERM allows cleanup; KILL is last resort | force-first culture |
| A11 | **b** | enable = boot-graph symlink; start = runtime | enable≡start |
| A12 | **c** | refused = reached host, no listener (rung 4 result) | ping-first network panic |
| A13 | **c** | TOFU bookkeeping: verify out-of-band, then update | `-o Strict...=no` normalization |
| A14 | **b** | wrong interpreter/kernel — the env isn't the one you think | "pip broke" externalizing |
| A15 | **b** | volumes outlive containers by design | container≡data conflation |

## Section B — Interpretation (2 pts each: what it does + what it doesn't)

- **B16.** Lists packages with newer catalogue versions *only*; installs nothing (and is stale until `apt update`).
- **B17.** Full dependency simulation of the nginx install; zero system change — the rehearsal reflex.
- **B18.** Directory: 1=sticky (deletion restricted to file owners), 770 = owner+group rwx, other none — team-writable, self-protecting.
- **B19.** Deletes log files under cwd older than 30 days, recursively. *Does not* prompt, *does not* descend into other filesystems unless mounted under `.`, and `.` placement makes scope everything below — dangerous if cwd is wrong (name the census reflex).
- **B20.** **Dry-run** mirror: reports (including deletions) without touching anything. `--delete` would make source authoritative; the `n` is the gate. Trailing slash: contents of `clean/` into `data/clean/`.
- **B21.** Sends SIGTERM (polite, trap-friendly) to the PID(s) matching `training.py`. Risks: pattern can match unintended processes (two-python3s lesson); TERM may be ignored → escalate after waiting.
- **B22.** Only the `webapp` unit's entries, priority ≤ err (err/crit/alert/emerg), from the last hour, no pager. It reads the *journal index* — not raw files.
- **B23.** Opens a *local* forward: connects your 9999 → through SSH → to `localhost:8888` *from the server's side*. `-N` = no shell. The use case: remote Jupyter reachable at local 9999.
- **B24.** `enable --now`: wires the user timer into the boot (default target) graph *and* starts it immediately — two graphs, one command.
- **B25.** Copies the directory itself → `dst/src/`. The slash-less source is the classic nesting trap; with trailing slash, contents merge into `dst/`.
- **B26.** Creates an *anonymous* volume at `/data` in the container and publishes host 8888→container 8888. *Does not* bind your host `~/data` — that needs `-v ~/data:/data`; anonymous volumes vanish with `rm` unless reattached.
- **B27.** For comma-separated lines, prints field 1 where field 3 numerically exceeds 100. `-F,` sets the splitter; `$3+0`-style care needed if field 3 may be non-numeric (header lines!).

## Section C — Output reading (2 pts each)

- **C28.** Permission failure: `/root` is not traversable by `dsstudent` (x missing for other). The path never resolved; `2>&1` merged stderr into stdout so we *see* the error. (Mechanism: directory-x.)
- **C29.** `s` in the group triplet = **SGID on the directory** (new files inherit group `research`); `770` = no access for others. New files: owned by creator, group research, modes per that umask.
- **C30.** A **loopback** device — a file mounted as a block device. Tells: the `/dev/loop0p1` naming and (from the lab context) a 97 MB "disk" — a size no real disk ships with.
- **C31.** `D` = uninterruptible sleep — waiting on I/O in the kernel; signals (even SIGKILL) are *not delivered* until the syscall returns. Diagnosis: what I/O is it stuck on (storage path), not more signals.
- **C32.** Crash-loop: exits with an error and `Restart=` policy keeps retrying. Next: `journalctl --user -u health -n 20` (cause), `systemctl --user cat health` (config). Fix-verify with `is-active`.
- **C33.** No listener on 8888: the app isn't running/bound — a *process* problem, not network (rungs 1–3 moot; refused would mean rung 4). Rules out firewall/DNS entirely.
- **C34.** `journalctl -u healthbot -p err --since -1h --no-pager` (accept `--since "1 hour ago"`). Unit filter + priority + window = the evidence query.
- **C35.** nginx (the logger) answered; the *upstream* (app on the proxied port) refused the connection. Next check: is the upstream process up/listening (`ss -tlnp` on the upstream port, `systemctl status` on the app).

## Section D — Scenario (3 pts each: design + justification + trade-off named)

- **D36.** Group `research` owns `/srv/datasets` `2770` (or 2775 if read-for-others is required — but intern is *in* the group read-write unless separated): intern gets a *read* path — either `o=rx` (public read) or — cleaner — an ACL/group `interns:r-x`; sticky (`1770`) if deletion self-protection matters. Full credit: explicit mode digits + who-gets-what + the sticky/SGID trade-off named.
- **D37.** Cron's minimal environment: relative `~` path resolves wrong or PATH lacks a command; zero logging hides the truth. Diagnosis: run the exact command *as cron would* (`set -e; cd /; $SHELL -c '...'`), check `cron`'s mail absence. Fix: absolute paths + `>> log 2>&1` (or systemd timer, journald-logged).
- **D38.** Skipped: (1) the read `--dry-run` before the deleting sync, (2) the source-authority decision (who is master). Protection mechanism: `--backup --backup-dir` (removals archived, not destroyed) — or immutable snapshots on the server side (M19 policy). Only the mechanism *plus* the two rules is full credit.
- **D39.** Any defensible read-only triad, e.g.: `uptime`/`vmstat 1` (load vs saturation), `free -h` (memory pressure/swap), `df -h` (disk full) — order matters less than *read-only + what each rules out* stated. Full credit names the ruling-out ("swap-in nonzero → memory, not CPU").
- **D40.** Runs as a **systemd user unit** (or system unit) with `Restart=on-failure` + `WantedBy=default.target` (boot survival); logs to stdout/stderr so **journald** collects them (`journalctl -u api`). Two lines of design + the logging contract = full credit.

## Difficulty distribution (as shipped)

Easy recall-in-context: A1–A5, B16, C30 (≈30%) · Intermediate
mechanism: A6–A12, B17–B25, C28–C33 (≈50%) · Transfer/design: A13–A15,
B26–B27, C34–C35, D36–D40 (≈20%).

## Evidence notes (for disputed answers)

- A9/C30-style items: settle by reproducing on the spot (`lsof +L1`,
  `losetup -l`) — the demo *is* the authority
- B25: settle with the module's dry-run demo (slash experiment)
- D38: the capstone rubric's backup non-negotiable is the policy source
