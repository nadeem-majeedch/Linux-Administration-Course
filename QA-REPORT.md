# QA Report — Pre-Publication Audit

> **Date:** 2026-09-17 · **Scope:** entire repository (524 markdown files, 32 modules)
> **Method:** every check below was actually executed against the repository —
> link crawler, `bash -n` over extracted code blocks (Git Bash binary), `py_compile`
> over Python blocks, fence counter, CR scanner, secret-pattern scanner, and manual
> triage of every flag. Nothing was claimed without running it.
>
> **Overall status: PASS WITH WARNINGS**

---

## PASS

| # | Audit area | Check executed | Result |
|---|---|---|---|
| 1 | Broken links | Path-resolving crawler over all 1,812 relative markdown links | **0 broken** |
| 2 | Missing files | Crawler + structural survey (every module dir inventoried) | all referenced files exist |
| 3 | Incorrect paths | Same as #1; cross-module links resolved from each file's own directory | 0 failures |
| 4 | Inconsistent naming | Directory survey vs roadmap numbering | 1 stale duplicate found → **fixed** (see below) |
| 5 | Incorrect commands | `bash -n` on 1,090 bash/sh/console blocks; manual triage of all flags | **0 real syntax defects** |
| 6 | Incorrect options | Spot-verification of high-risk claims (fstab fields, chmod bit math, umask tables, cron fields, SSH file modes, restart policies, `apt -s`, `visudo -c`, `journalctl --vacuum-*`) | verified correct |
| 7 | Unsafe commands | Regex sweep for `rm -rf /`, `mkfs` on real devices, `dd of=/dev/sd*` | all hits are loopback/teaching contexts or explicit anti-patterns |
| 8 | Distro-specific as universal | Sweep for apt/dpkg/ufw/systemctl framing | content consistently labels Debian-family vs RPM-family vs universal |
| 9 | Missing prerequisites | Module READMEs state prerequisites; roadmap dependency chain intact | present (M02/M05 leaner — see warnings) |
| 10 | Duplicate lessons | H1 survey across all 524 files | only intentional README↔content/README pairs |
| 11 | Contradictory explanations | Cross-checked recurring claims (permissions, PATH, journald, systemd) between lessons and cheatsheets | no contradictions found |
| 12 | Missing exercises | Quiz/challenge survey per module | all content modules have practice sets |
| 13 | Missing lab instructions | Lab survey: 74 module labs + 5 top-level level files + assessments | all include setup → steps → evidence |
| 14 | Missing expected outcomes | Content READMEs with learning objectives: 30/30 content-bearing modules | present |
| 15 | Incorrect terminology | Terminology spot-checks (e.g., distribution ≠ kernel ≠ machine, service vs daemon, hard link vs symlink) | correct; M02 troubleshooting page teaches the distinctions |
| 16 | Markdown formatting | Fence-balance counter over all files | **0 unbalanced** (one M08 defect found and fixed) |
| 17 | Code blocks | Fence + language-tag survey | consistent `console`/`bash`/`python` conventions |
| 18 | Shell syntax | `bash -n` (see #5) — 99 initial flags triaged to ~95 transcript-output artifacts + 4 intentional broken-teaching blocks | clean |
| 19 | File references | Links + explicit file-path greps | consistent |
| 20 | DS integration | DS-connection sections present across modules; M31 + capstone close the loop | present |
| 21 | Beginner accessibility | M01–M05 assume zero experience; every destructive operation carries warnings | satisfied |
| 22 | Progression | Units 1→8 scaffold: M01 foundations → M31 server + M30 capstone | coherent |
| 23 | Capstone coverage | 18 tasks × module mapping; every module exercised | complete |
| 24 | Assessment coverage | 59 module quizzes + centralized assessments/ (midterm, final, practical, 5 lab assessments, 3 assignments, rubric, viva) | complete |
| — | Secrets scan | AWS key / GitHub token / Slack token / private-key patterns over all files | **0 hits** |
| — | Python syntax | `py_compile` over all python blocks | **0 failures** |
| — | Line endings | CR scanner after normalization | **0 files with CR** |

## WARNINGS (accepted, documented)

1. **M23-file-transfer** remains a scaffolded contract — the one content-empty
   module. Its roadmap entry says so explicitly; all links to it resolve.
2. **M02 and M05** predate the full module template: single lesson-set, shorter
   quizzes, no dedicated labs directory (M05's labs live in M01 by design, and
   are linked). Content is complete; structure differs from M03+ modules.
3. **M30/M31** embed their practice material in `projects/capstone/` and
   `content/practice.md` respectively rather than `practice/quiz.md` — by design,
   documented in their READMEs.
4. Several intentional "broken" examples (fix-the-bugs labs, incident drills)
   fail `bash -n` by design; each is labeled as broken in surrounding prose.

## ERRORS FIXED (this pass)

| Defect | Fix |
|---|---|
| Stale duplicate module dir `M04-installing-ubuntu` (referenced by 4 files) | directory removed; 4 links retargeted to `M04-installing-linux-vms` |
| M30 README still said "Status: scaffolded", pointed nowhere | rewritten: points to `projects/capstone/` pack, real theme, definition of done |
| M08 `01-viewing-counting.md` missing opening fence (odd fence count) | fence restored; file now balanced |
| M10 lessons 03 & 05: Unicode `←` arrows as pseudo-comments inside runnable bash skeletons (copy-paste breaks) | converted to real `#` comments |
| 30 files with CRLF line endings (incl. 227-CR main README) | normalized to LF; repo-wide CR count now 0 |
| M02, M05 missing the per-module troubleshooting page | both written (symptom → cause → diagnosis → fix → prevention) and wired into module indexes |
| M05 missing challenges page | 5 judgment-based challenges written and wired in |
| 3 pure-recall quiz questions (cheatsheet-answerable) in M14/M16/M18 | rewritten as scenario-grounded questions with matching keys |

## REMAINING ISSUES

None blocking publication. The four warnings above are the known deviations;
the single genuine content gap is M23-file-transfer (flagged in the roadmap and
module README as scaffolded).

## Verification commands (rerunnable)

```bash
# links
python - <<'PY'
import os, re, urllib.parse
bad = 0
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ('.git', '.freebuff')]
    for fn in files:
        if not fn.endswith('.md'): continue
        p = os.path.join(root, fn)
        for m in re.finditer(r'\[[^\]]*\]\(([^)\s]+)\)', open(p, encoding='utf-8').read()):
            u = m.group(1)
            if u.startswith(('http', 'mailto:', '#')): continue
            u = urllib.parse.unquote(u.split('#')[0])
            if u and not os.path.exists(os.path.normpath(os.path.join(root, u))):
                bad += 1; print(p, '->', u)
print('broken:', bad)
PY

# code-block syntax (Git Bash on Windows; plain bash elsewhere)
# bash -n over each ```bash/```console block — see QA method notes

# line endings
grep -rlU --include='*.md' -e "$(printf '\r')" .
```
