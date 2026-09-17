# Viva Practice Bank — Student Edition

> General practice questions in the style of the graded viva
> (`assessments/viva-questions.md` is the full instructor bank; this
> student set is a fair sample of its *style*, not its content).
> Practice **aloud, 60–90 seconds per answer** — the graded format is
> evidence-first: claim → mechanism → how you'd verify.

## Format reminder

Two pillars: defend a claim from *your own* system, then justify a
trade-off against its alternative. Every answer can be drilled with
"why?" twice.

## Pillar 1 — Evidence answers ("how do you know?")

1. "You say your script is idempotent. How would you demonstrate that
   to me in 30 seconds?"
2. "Your backup strategy — walk me through how you *proved* a restore
   works, not that an archive exists."
3. "You claim the service failed because of a config error, not a
   dependency. What journal line said so?"
4. "Show me the evidence that only your user can write to the shared
   directory — not that everyone can't."
5. "Your Jupyter server is bound correctly. What single command
   output convinced you?"
6. "You fixed a full disk. Prove the data is intact afterwards."
7. "Which command output told you the container was using too much
   memory — and what did it show?"
8. "You say the transfer completed. What did you check besides exit
   code 0?"

## Pillar 2 — Trade-off answers ("why this and not that?")

9. "Why rsync rather than scp for your weekly dataset sync — and
   when would scp be the *right* answer?"
10. "Why did you put the team on SGID + umask rather than ACLs? Name
    what ACLs would have bought you."
11. "Why a systemd timer over cron for your cleanup job — and what
    does cron still do better?"
12. "Why did you pin versions in requirements.txt despite the
    maintenance cost?"
13. "Why run the notebook server as a normal user with a venv rather
    than system-wide pip?"
14. "Why did you keep the firewall default-deny when it complicated
    your own lab? What did it protect against concretely?"
15. "Why Docker for the API and not a venv + systemd unit? Be honest
    about what Docker made harder."
16. "Why tar.gz for the archive rather than rsync to a mirror? What
    failure mode does each cover that the other doesn't?"

## Drill technique

For each answer above, a grader will follow with "why?" twice. Prepare
the **second layer**: not just *what* you did, but the mechanism
underneath, and the *cost* you accepted.

Example to depth-3:

- "rsync, because it transfers deltas."
  - *Why deltas?* size+mtime comparison skips unchanged blocks →
    weekly syncs move megabytes, not gigabytes.
  - *Why does that matter here?* the lab uplink is slow and metered;
    full copies would make the schedule miss.
  - *Cost accepted?* mtime-based comparison can miss same-size edits;
    I mitigate with `--checksum` for critical manifests.
