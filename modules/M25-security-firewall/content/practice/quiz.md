# Module 25 Quiz — Security & Firewall

> 22 questions. Answer first, then check [quiz-answers.md](quiz-answers.md).
> Scope: lessons 1–6. Concept questions graded on reasoning; the
> two-terminal rule and rollback discipline count as quiz material.

## Section A — principles (Q1–5)

**Q1.** Define least privilege in one sentence, and name the four
instances the course has already taught it (module + mechanism).

**Q2.** Authentication vs authorization: one sentence each, then
classify — `ssh-copy-id`, `setfacl`, `AllowGroups`, `passwd`,
`chmod 640`.

**Q3.** Your Jupyter binds `0.0.0.0:8888` instead of
`127.0.0.1:8888`. In attack-surface terms, what exactly changed?

**Q4.** Name the layers of the defense-in-depth stack the course
taught, in order, and state which single-layer failure each layer
catches.

**Q5.** Why are backups a *security* control rather than an
operations convenience? One sentence, plus the ransomware-era
nuance.

## Section B — firewall (Q6–10)

**Q6.** Default-allow vs default-deny: which fails *open* and which
fails *closed* — and why does the course mandate one of them?

**Q7.** Order these ufw commands correctly and say why the order is
load-bearing: `ufw enable`, `ufw default deny incoming`,
`ufw allow OpenSSH`.

**Q8.** What does `ufw limit OpenSSH` do, and how does it differ
from fail2ban's mechanism?

**Q9.** Write the ufw rule: SSH allowed *only* from `10.0.2.0/24`.

**Q10.** A service binds to `127.0.0.1:5432`. Why does it need no
ufw rule at all — and what does that imply about bind scope as a
control?

## Section C — SSH & services (Q11–15)

**Q11.** State the two-terminal rule precisely, and what each
terminal is for.

**Q12.** The five beats of the config-change procedure — in order,
one verb each — as applied to sshd.

**Q13.** `sshd -t` vs `systemctl reload ssh` vs `systemctl restart
ssh`: what does each do, and why is the middle one the right choice
here?

**Q14.** `ls /etc/ssh/sshd_config.d/` shows `10-hardening.conf`
(yours) and `50-cloud-init.conf` setting
`PasswordAuthentication yes`. Which wins, why, and what's the fix?

**Q15.** In the listening-service audit, what three questions does
each `ss -tlnp` line have to answer — and what are the three
escalation levels for closing an unneeded service?

## Section D — secrets & monitoring (Q16–22)

**Q16.** Rank by hygiene and justify: hardcoded key in a notebook /
key in a tracked `.env` / key in an ignored `600 .env` /
`os.environ` injection.

**Q17.** Why does adding a committed `.env` to `.gitignore` *after
the fact* not fix the leak — and what are the three response steps?

**Q18.** Why is *revocation* step one of the leak playbook, before
any history rewriting?

**Q19.** auditd vs application logs (M24): what does the kernel
level see that programs don't log? One sentence, plus the role of
`-k` tags.

**Q20.** AppArmor vs SELinux: which default ships on Ubuntu vs
RHEL, what's the policy-shape difference, and what does
complain/permissive mode do?

**Q21.** ufw `limit` vs fail2ban vs auditd: classify each as
prevent/detect, and name its layer.

**Q22.** List four "unexpected X" checks from the persistence
inventory that detect compromise on a Linux host.

## Bonus (Q23) — the checklist as judgment

A teammate says their hardened server has: ufw active, key-only
SSH, unattended-upgrades — but their backup is on a mounted drive
on the same machine, reachable by the same SSH key. Use the
hardening checklist's categories to name the gap and the control
that fixes it.
