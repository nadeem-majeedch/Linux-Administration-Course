# Unit 6 Teaching Guide — Services, Network & Security (M20–M25)

> Sessions S19–S24 · companions: [speaker notes](../../speaker-notes/unit-06-services-network-security-notes.md) · [deck](../../lecture-slides/unit-06-services-network-security-slides.md)

## M20 systemd, Services & Boot (S19)

**Objectives.** Unit-file reading; lifecycle verbs; enable-vs-start as
two graphs; status output as evidence; user units as the practice
ground.

**Difficult concepts.** The boot graph vs runtime state distinction
(the drawn symlink is the anchor). Crash-loop reading:
`activating (auto-restart)` before the journal names the cause.

**Common mistakes.** Editing unit files without `daemon-reload`;
`enable` without `start` (and the reverse confusion); reading `status`
as "fine" because the line says loaded.

**Demo plan.** Break a *user* unit's ExecStart → status → journal →
one-line fix → `daemon-reload` → start. The full loop in under 4
minutes.

**Assessment hook.** M20 quiz (unit failure triage); LA-4's service
forensics builds directly on this lab.

**Extension.** ★★★: M20 challenges (write a unit with restart policy
and hardening directives at reading level).

**Troubleshooting (in class).** User-unit quirks require loginctl
enable-linger for some checks — the module lab stages it; if linger is
refused on lab machines, fall back to the module's plain user-unit path.

## M21 Networking Fundamentals (S20)

**Objectives.** Layer vocabulary (MAC/IP/ports/DNS); `ss` reading; the
six-rung diagnosis ladder as *ordered discipline*.

**Difficult concepts.** Refused vs timeout (rung 4 vs rung 3 hinge);
loopback as a *real* network interface (it has its own rules).

**Common mistakes.** Debugging DNS before checking listeners; `ping`
as the universal verdict; ignoring the ladder's order (tool soup).

**Demo plan.** The Jupyter-not-reachable walk: rung by rung to "no
listener — it's not the network."

**Assessment hook.** M21 quiz (layer-by-layer diagnosis); the ladder
reappears in the final exam's network section.

**Extension.** ★★★: M21 challenges (tracepath path analysis).

**Troubleshooting.** All labs loopback; if NAT networking breaks in the
room, *most* of this session survives (loopback doesn't care) — plan B
is built in.

## M22 SSH & Remote Administration (S21)

**Objectives.** Key lifecycle end-to-end; ssh_config aliases; host-key
trust (TOFU + change choreography); tunnels; tmux durability.

**Difficult concepts.** Private-key *identity* semantics (what the key
proves); host-key change as an *event to investigate*; tunnel direction
(local forward semantics).

**Common mistakes.** 600/700 permission failures on `.ssh` (the famous
message); agent confusion (keys vs agent forwarding); leaving
PasswordAuthentication reasoning fuzzy.

**Demo plan.** Host-key-changed choreography (planned, safe, restored);
tunnel to a localhost web app with the path drawn.

**Activity.** "Why did SSH refuse?" evidence round (5 cases).

**Assessment hook.** M22 quiz; LA-5's client-side spot-check; M23
depends on this lab's working keys.

**Extension.** ★★★: ProxyJump chains from M22 challenges.

**Troubleshooting.** Loopback-only policy keeps this safe; if a student
points at external hosts, stop it in the moment — the module's safety
contract is the citation.

## M23 File Transfer (S22)

**Objectives.** Tool selection by workload; rsync semantics (slash,
compare modes, resume); the `--delete` gate; sha256 verification.

**Difficult concepts.** Slash semantics (contents vs container);
size+mtime vs `--checksum` vs manifest (three levels of claim strength).

**Common mistakes.** The slash trap (`rsync -a src dst/` nesting);
`--delete` unrehearsed; trusting "up to date" as *proof* (it isn't).

**Demo plan.** The interrupt-and-resume race (scp restarts vs rsync
resumes at 200 MB); dry-run reveal of the slash difference.

**Assessment hook.** M23 quiz (tool selection, rsync semantics); A3
and the capstone's transfer pipeline.

**Extension.** ★★★: the reproducibility-pack challenge (M23 practice).

**Troubleshooting.** The interrupt demo needs the timing rehearsed —
too fast and the contrast is invisible; the module lab's timing notes
are calibrated.

## M24 Logs, journald & Monitoring (S23–S24, two sessions)

**Objectives.** journalctl as *interface* (queries, not greps); classic
/var/log coexistence; rotation; vital-signs reading; the 8-step method
introduced.

**Difficult concepts.** Persistent vs volatile journal (and why a
rebooted machine loses evidence without persistence); available-vs-free
memory; si/so as the dying-server signal.

**Common mistakes.** Grepping journal directories; `--since` syntax
guesswork; panic-reading `used` memory; skipping baseline before
anomaly.

**Demo plan.** Forensics on a staged failure: journal query → quoted
evidence → cause. Memory-hog + `free -h`/`vmstat` live.

**Activity.** Build-the-query round; next-step-in-the-method round.

**Assessment hook.** M24 quiz; LA-4 (service & log forensics) is the
graded artifact; the method is the practical exam's skeleton.

**Extension.** ★★★: the monitoring-circuit challenge (M24 labs).

**Troubleshooting.** Staged bloated journals need the infra checklist
run before S23; if persistence isn't enabled on lab images, the
rotation lesson changes — check first.

## M25 Security & Firewall (S24)

**Objectives.** Threat model for a lab server; UFW default-deny with
justified allows; SSH hardening at apply-level (with rollback); the
hardening checklist as the capstone artifact.

**Difficult concepts.** Default-deny *rationale* (can't enumerate what
you forgot); the second-session habit as professional insurance;
hardening as *evidenced* practice, not claimed.

**Common mistakes.** ufw enable before allow 22 (the self-lockout);
"temporary" holes; secrets in repo-adjacent env files with wrong modes.

**Demo plan.** Two-terminal ufw drill; checklist walk with evidence
placeholders.

**Assessment hook.** M25 quiz; the checklist *is* capstone area 5's
evidence skeleton; practical exam's firewall task.

**Extension.** ★★★: fail2ban concept reading + one staged brute-force
log analysis (M25 challenges).

---

## Unit-level notes

- **Six sessions, zero slack** — the cut list per session is in the
  speaker notes; the two-terminal ufw habit and the 8-step method never
  cut.
- **Staging dependencies:** bloated journal (S23), crash-loop unit
  (S19/S23), second-session insurance is *policy* from S24 on.
- **The capstone map:** show rubric areas 4–6 after S24 — students
  should see that a third of their capstone was just taught.
