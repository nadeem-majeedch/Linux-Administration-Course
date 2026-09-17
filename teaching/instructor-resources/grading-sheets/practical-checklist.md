# Practical Examination — Invigilation Checklist

> 🔒 INSTRUCTOR-ONLY. Companion to
> [`assessments/practical/practical-exam.md`](../../../assessments/practical/practical-exam.md)
> (staging: [`practical-key.md`](../../../assessments/practical/practical-key.md)).
> Designed to be used **hands-free during the sitting**: print one per
> student, tick in the column, write the state you observed — not the
> commands you saw (students own the keystrokes; you own the states).

**Student:** ________________ **Station/Snapshot:** ________ **Start:** ____ **Finish:** ____
**Transcript (`script practical.log`) collected:** [ ]

## Before the sitting (once per room)

- [ ] Snapshot restored per station; staging verified on ONE spare
      station (each of the 6 faults present, services otherwise green)
- [ ] Clock visible; 90 min announced; 10-min warning planned
- [ ] Open-notes rule stated: *own module notes only*, no internet
- [ ] `script practical.log` requirement announced — no transcript,
      no mark for Part evidence

## Part I — Service rescue (25 pts)

| # | End state to verify | Pts | ✓ | Observed state |
|---|---|---|---|---|
| 1.1 | Unit diagnosed from **its own logs** (journalctl line quoted in transcript) | 8 | | |
| 1.2 | Root cause named (config/exec/dependency), not symptom-masked | 7 | | |
| 1.3 | Unit **active** at finish; `systemctl is-active` exit 0 | 7 | | |
| 1.4 | No collateral change (other units untouched — compare to snapshot) | 3 | | |

## Part II — Identity & permissions (25 pts)

| # | End state | Pts | ✓ | Observed |
|---|---|---|---|---|
| 2.1 | User/group created with correct names & membership | 6 | | |
| 2.2 | Ownership/permissions on the tree exactly as specified (`ls -l` matches) | 8 | | |
| 2.3 | SGID set where required; new files inherit group (one creation demonstrated) | 6 | | |
| 2.4 | Access tested **as the created user** (`sudo -u` / `su -`), not assumed | 5 | | |

## Part III — Disk & data (25 pts)

| # | End state | Pts | ✓ | Observed |
|---|---|---|---|---|
| 3.1 | Filler identified and located (du/lsof evidence in transcript) | 8 | | |
| 3.2 | Space reclaimed **without data loss** (protected tree intact, checksums pass) | 8 | | |
| 3.3 | `df` shows the target threshold reached | 6 | | |
| 3.4 | No destructive command used outside its guarded context | 3 | | |

## Part IV — Network & workflow (25 pts)

| # | End state | Pts | ✓ | Observed |
|---|---|---|---|---|
| 4.1 | Listener confirmed (`ss -ltnp`) and bound to the intended address | 7 | | |
| 4.2 | Connectivity proof captured (curl/nc output with expected response) | 7 | | |
| 4.3 | Firewall adjusted *minimally* (single rule, rationale in notes) | 6 | | |
| 4.4 | Workflow command reproducible from transcript alone | 5 | | |

## After the sitting

- [ ] Transcript file collected and named `student-login.log`
- [ ] Zero-score items circled (pass rule: ≥ 70 AND no zero-score item)
- [ ] Second-mark needed? [ ] ≥ 85  [ ] any zero  [ ] integrity doubt
- [ ] Snapshot reverted / station reset for next candidate
- [ ] Sheet filed with transcript (this is the evidence pair)

**Invigilator:** ______________ **Total:** ____/100
