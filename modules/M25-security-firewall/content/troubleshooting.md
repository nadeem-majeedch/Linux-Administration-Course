# Module 25 Troubleshooting — Hardening Symptoms → Causes → Fixes

> Ten patterns — mostly *self-inflicted by hardening*, which is the
> honest majority. Each: **symptom → cause → diagnosis → fix →
> prevention**. The M24 incident method structures every case;
> evidence before verdicts.

## 1. "I locked myself out of my own server"

**Cause:** firewall enabled without an SSH allow, or sshd
auth-change applied without the two-terminal rule.
**Diagnosis:** from the VM console (the escape hatch): `sudo ufw
status verbose; sudo sshd -G $USER | grep -iE 'password|root'`.
**Fix:** whichever layer locked it — `sudo ufw disable` and/or
restore the drop-in `.bak` + reload. Re-verify from SSH.
**Prevention:** the choreography order (allow before enable;
verify before closing); the console is named in the rollback plan
*before* it's needed.

## 2. "SSH suddenly asks for a password again"

**Cause (post-hardening):** your drop-in lost precedence to a later
file (`50-cloud-init.conf`); group membership expired from
`AllowGroups` (never re-logged-in); key file permissions drifted.
**Diagnosis:** `sudo sshd -G $USER | grep -iE
'passwordauthentication|allowgroups'`; `groups`; `ls -l ~/.ssh`.
**Fix:** rename the drop-in to `99-`, re-login for group refresh,
re-`chmod 600`.
**Prevention:** `sshd -G` after every sshd change; the
verification trio after every reload.

## 3. "sshd won't start after my config edit"

**Cause:** syntax/directive error in a drop-in — `sshd -t` was
skipped.
**Diagnosis:** `sudo sshd -t` (it names the file and line);
`journalctl -u ssh -b --no-pager | tail`.
**Fix:** correct or remove the offending drop-in; `sshd -t` until
clean; `reload`.
**Prevention:** `sshd -t` before *every* reload — it costs two
seconds and this incident.

## 4. "ufw blocks a service I allowed"

**Cause hierarchy:** rule targets the wrong port/protocol; service
bound to an interface the rule doesn't cover (or loopback-only —
then the *service*, not the firewall, is the problem); a deny rule
earlier in the list wins; the traffic is IPv6 and the rule is
v4-only (ufw handles dual-stack for simple rules, not for scoped
ones).
**Diagnosis:** `sudo ufw status verbose`; M21's ladder from the
client (`nc -zv`, `curl -v` — refused vs timeout); on the server,
`ss -tlnp` to re-check the bind.
**Fix:** correct the rule (`delete` + re-add, or `insert 1` for
precedence) or fix the bind.
**Prevention:** rules verified by *connection test*, not by their
presence in the list.

## 5. "Rate-limited by my own ufw limit rule"

**Cause:** `ufw limit OpenSSH` throttles per-IP connection rate —
your own test loop (or a hung multiplexer) trips it.
**Diagnosis:** pattern in timing (works, then 30s of refusal);
`sudo dmesg | tail` shows ufw LIMIT blocks.
**Fix:** wait it out (30s window) or remove the limit while
testing.
**Prevention:** testing loops on real servers use the
non-limited path or pacing — and knowing your own rules' side
effects (C4's rehearsal).

## 6. "unattended-upgrades is enabled but security patches pile up"

**Cause:** the timer never fired (machine off/asleep), the
`20auto-upgrades` file lacks the `1` values, or
`/var/run/reboot-required` has been true for weeks (patched kernel
not *running*).
**Diagnosis:** `systemctl status apt-daily-upgrade.timer; cat
/etc/apt/apt.conf.d/20auto-upgrades; cat /var/run/reboot-required
2>/dev/null`.
**Fix:** enable the timer config properly; reboot during the next
window.
**Prevention:** the weekly check (C6's report) — patch status is a
*metric*, reviewed, not assumed.

## 7. "A file I git-ignored is still 'tracked'"

**Cause:** tracked before ignored — `.gitignore` only affects
untracked files. (Lesson 5 §3's third rule, biting exactly as
taught.)
**Diagnosis:** `git check-ignore -v .env && git ls-files | grep
.env` — ignored *and* tracked simultaneously.
**Fix:** `git rm --cached .env` (keep the file), commit — and the
history caveat from Lesson 5 §5: if a real secret, revocation
first.
**Prevention:** ignore *before* creation; `git status` as the
habit that catches it in seconds.

## 8. "AppArmor/SELinux broke my app" (the MAC chafe)

**Cause:** the program does something its profile doesn't allow —
often legitimate-but-unusual paths.
**Diagnosis:** AppArmor: `sudo journalctl -g DENIED --since
"1 hour ago" | grep <program>`; SELinux: `sudo ausearch -m avc
-today`.
**Fix:** adjust the policy (add the path/permission) or fix the
app's assumption — *not* setenforce 0 / complain mode as the
end state (that's a debugging tool, not a fix).
**Prevention:** know the mode you're in (`aa-status`, `getenforce`)
and the log that names denials before you need it.

## 9. "I found a credential committed months ago"

**Cause:** the leak is old; the clock on it is *still running* —
tokens don't expire because the commit aged.
**Diagnosis:** Lesson 5 §5: assume use — check the provider's
access logs; `git log -p` to establish exposure window.
**Fix:** revoke/rotate first; then purge current state; history
rewrite as a coordinated event.
**Prevention:** the Lab 2 audit as a periodic sweep, and the
env-pattern making new leaks structurally impossible.

## 10. "The hardening checklist never gets finished"

**Cause:** it's treated as an event (a lab) instead of a routine
(quarterly), or every item demands perfection so none get done.
**Diagnosis:** the checklist itself — X/Y with dates. No dates =
not a routine.
**Fix:** timebox a quarterly hour; verified-or-explicitly-accepted
per item (the checklist's own scoring rule); automate what's
automatable (C6's patch report; Lab 1's verification trio as a
script).
**Prevention:** attach the checklist run to something scheduled
(M19 timers for the check *emails*; the human does the reading).

## When to escalate

| Evidence | Escalate to |
|---|---|
| Any sign of real compromise (unexpected persistence, auth.log anomalies) | IT security — immediately, with your transcripts; do not investigate alone |
| Lockout on a *shared* machine | Co-admin with console access — and your rollback plan |
| MAC denials on a production app | App owner + security — policy change is a review |
| Credential leak on company infrastructure | Security team *before* self-help — they coordinate rotation |

> The module's ethics contract cuts both ways: you defend your
> systems; anything beyond that — attribution, counter-attack,
> investigation of others — belongs to professionals. Escalating
> early with evidence *is* the competent move.
