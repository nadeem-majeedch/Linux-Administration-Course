# Assignment 5 — The Network Doctor

> Covers M20–M23 (services, networking, SSH, transfer) · optional
> replacement for A3 (same 5% weight) · individual work · evidence
> transcripts required.
>
> **The premise:** you are on call for a tiny lab of *one machine* —
> your own VM. Five incidents arrive. For each: diagnose with evidence,
> fix minimally, verify the original symptom is gone, and write the
> incident note. Everything is loopback; nothing leaves your VM.

## Learning objectives assessed

- The six-rung network diagnosis ladder, applied *in order*
- systemd unit triage from state + journal evidence
- SSH failure diagnosis (auth, config, key modes)
- Transfer verification habits (dry-run gates, manifests)

## Environment setup (provided in the assignment pack)

Run the pack's `stage-incidents.sh` **inside your own VM** — it creates
five broken states by: breaking a *user* unit; binding a service to the
wrong port; planting an sshd config mismatch *in a sandbox copy* (never
the real sshd); breaking a listening service's bind address; corrupting
a sync target. Each incident is reversible; the pack includes its own
teardown.

*(If your instructor supplied a staged snapshot instead, restore it and
skip this step.)*

## The five incidents (unknown order — evidence decides)

For each incident you may assume only the symptom line a user would
report. You must produce:

1. **Diagnosis** — the commands you ran *in order*, with output quoted
2. **Minimal fix** — the smallest change that restores service
3. **Verification** — the original symptom, re-tested, gone
4. **Incident note** (3–5 lines): symptom → cause → fix → prevention

| Incident | User-reported symptom |
|---|---|
| 1 | "my health-check service keeps dying" |
| 2 | "my web dashboard is unreachable even though the process runs" |
| 3 | "ssh to my own box suddenly demands a password" |
| 4 | "the sync job says up to date but the files are stale" |
| 5 | "the API answers locally but not from the other terminal's curl" |

## Deliverables

1. `a5.log` — the `script` transcript covering all five incidents
   (start it before the first diagnosis; five labeled sections)
2. `incident-notes.md` — the five notes, each with the four elements
   above, evidence *quoted* (not paraphrased)
3. A one-paragraph reflection: which rung/command you reached for too
   early, and what the ladder discipline cost/won you

## Constraints & hard rules

- **Read-only before mutating**: every fix is preceded by evidence in
  the transcript
- **No reload/reboot escapes**: restarting the VM to "fix" an incident
  scores zero for that incident
- sshd work happens **only on the sandbox copy** the pack provides —
  touching the real `sshd_config` is a zero
- Network scope: loopback only; anything reaching beyond your VM is an
  integrity matter
- Each incident's fix is *minimal*: fixing by rebuilding/removing the
  service scores partial — restore the intended behavior

## Rubric (20 pts)

| Area | Pts | Full credit |
|---|---|---|
| Ladder discipline | 5 | diagnoses proceed rung-by-rung; no tool soup; evidence quoted |
| Root-cause accuracy | 5 | all five causes correctly identified |
| Fix minimality & correctness | 4 | smallest effective change; behavior restored |
| Verification | 3 | original symptom re-tested and shown gone, per incident |
| Incident notes | 3 | four elements each; notes a teammate could act on |

## Academic integrity

The pack's breakage is deterministic, but *your* evidence trail is not
copyable without copying its contradictions. Quote your own outputs;
coordinate on *method*, never on transcripts (see the [framework](../README.md#academic-integrity-guidance)).
