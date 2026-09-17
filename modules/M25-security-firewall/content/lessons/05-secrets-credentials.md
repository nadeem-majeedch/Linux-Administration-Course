# Lesson 5 — Secrets and Credentials

> Module 25 · Unit 6 · Difficulty: Advanced
> Reading time: ~25 min · Lab: [Lab 2 — the secrets audit](../labs/lab-02-secrets-audit.md)
> Up next: [Lesson 6 — monitoring layers](06-monitoring-layers.md)

---

## 1. The leak that ends careers happens in a git push

The most common way a DS person loses control of a credential isn't
exotic: it's `git commit -m "quick fix"` carrying an API token in a
notebook. Automated scanners watch public repos *for exactly this*,
and industry experience is that leaked keys get picked up and used
within minutes. This lesson is the defense: what counts as a
secret, where secrets live, and the hygiene that makes the leak
*structurally impossible* rather than merely avoided.

## 2. What is a secret — the inventory

Anything that grants access and must not be readable by others:

| Class | Examples | Leak surface |
|---|---|---|
| **Credentials** | passwords, SSH private keys, API tokens, OAuth secrets | repos, dotfiles, shell history |
| **Connection strings** | `postgres://user:pass@host/db` | notebooks, config files |
| **Personal data** | API keys tied to *your* accounts (data vendors, cloud) | everything above |
| **Infrastructure facts** | internal hostnames, IPs, team structures | notebooks pushed to public |

The DS reality: your working folder is *full* of the first three —
data-vendor keys, database URLs, cloud credentials for compute
bids, SSH keys for the cluster. The exposure isn't hypothetical;
it's the default unless you build the habits below.

## 3. Where secrets live — the hierarchy of hygiene

**Best: a secrets manager or agent.** Real teams use vault systems
(HashiCorp-style) or cloud secret stores; for individuals,
password managers (which hold more than passwords) and the
ssh-agent (M22) already cover identity. Course posture: know these
exist, use a password manager for your own credentials, and never
reinvent one in a script.

**Good: environment variables, injected — not stored in the repo.**

```bash
# ~/.bashrc or a sourced, git-ignored file — never in the repo
export KAGGLE_API_TOKEN="..."     # ← your shell has it
```

```python
import os                          # your code reads it — no literal in sight
token = os.environ["KAGGLE_API_TOKEN"]
```

The pattern: *code* references `os.environ[...]`; the *value*
arrives from outside the repo (sourced file, CI secret, scheduler
env). [M15's](../../../M15-environment-variables/README.md) env-var
mechanics, now carrying their security payload. The failure mode to
respect: env vars leak into logs and error traces (`echo $TOKEN`,
tracebacks printing locals) — treat env vars as *better*, not
bulletproof.

**Acceptable with discipline: a `.env` file — git-ignored,
mode-restricted.**

```bash
# .env  (in .gitignore! chmod 600!)
KAGGLE_API_TOKEN=...
DB_URL=postgres://ds:***@10.0.2.15/dsdb
```

```python
# python-dotenv reads it at runtime — but only locally
from dotenv import load_dotenv; load_dotenv()
```

The three-part discipline, all three required: **in
`.gitignore` before the file exists** (M26 will formalize
gitignore semantics — a file tracked *once* is in history
forever), **`chmod 600`** (M12's model — it's a credentials file),
and **a tracked `.env.example`** with empty values so teammates
know the shape.

**Never: literals in code, notebooks, or shell history.** Every
`api_key = "sk-..."` line is a leak awaiting `git push`. And note
the notebook hazard: Jupyter cells *cache outputs* — a token
echoed to stdout once persists in the `.ipynb` even after the cell
is edited. "I deleted it" is not "it's gone."

## 4. SSH keys are secrets too — the recap with teeth

[M22's](../../../M22-ssh-remote-admin/content/README.md) hygiene rules
were about function; here they're about classification:

- Private keys = credentials, `600`, never leave the machine, never
  enter any repo. (Course `.gitignore` has excluded `*.pem`, `*.key`
  since [M04](../../../M04-installing-linux-vms/README.md) — now you know
  exactly which lesson that was serving.)
- A key without a passphrase is a password lying on disk — a
  compromise of the file *is* a compromise of every server its
  public half sits on.
- Revocation is the upside of keys: removing one line from
  `authorized_keys` kills a leaked key everywhere — passwords can't
  be revoked per-device. This asymmetry is why M22 required keys
  from day one.

## 5. When a secret leaks — the response playbook

Because it will happen (to you or a teammate), the playbook:

1. **Revoke first, investigate second** — rotate the token/key at
   the provider; disable the SSH key (`authorized_keys` line out).
   Speed beats forensics; a revoked secret is a *contained* leak.
2. **Remove from history properly** — deleting the file in a new
   commit does *not* scrub history; the credential remains at the
   old commit. Tools exist for history rewrites (BFG, git-filter-repo
   — [M26](../../../M26-git-dev-workflows/README.md) territory), but
   revocation makes the rewrite non-urgent; do it calmly, after.
3. **Assume use** — check the provider's access logs for the token;
   look for unfamiliar logins (M24's auth.log habits, applied to
   whatever the secret unlocks).
4. **Write the postmortem** — M24's five lines: how it leaked, why
   it could, what hygiene change prevents the class. The prevention
   line is the one that compounds.

Lab 2 rehearses steps 1–2 on a seeded (fake) repo — the muscle
memory without the 3 AM adrenaline.

## 6. Secrets in team settings — the shared-server extension

On shared GPU servers the surface grows:

- **Shared identities are attribution poison** — M25 Lesson 1's
  rule: every action in auth.log should name a person; shared API
  accounts make breaches unattributable and revocation all-or-
  nothing.
- **Your env is readable by root** (and by anything you run with
  elevated rights) — don't paste secrets into terminals on machines
  you don't control; shell history and `/proc/*/environ` are
  readable upstream.
- **Notebooks are shared state** — the team checkpoint folder
  containing your `.env`-reading notebook has, effectively, your
  token. The hygiene scale: env-injected > .env-600 > hardcoded,
  and teammates inherit whichever you chose.

## 7. Try it now (15 minutes)

1. Self-audit: `grep -rInE '(api[_-]?key|token|secret|password)["'"'"']?\s*[:=]'
   ~/projects --include="*.py" --include="*.ipynb" | grep -v environ | head`
   — read every hit; classify real secret / placeholder / false
   positive. (Lab 2 formalizes this.)
2. History check: `history | grep -iE 'token|key|password'` —
   anything in your shell history that shouldn't be? (`history -c`
   and a habit change if so.)
3. `.env` rehearsal: create one in a scratch repo with a fake
   value, gitignore it, `git status` — prove the file is invisible
   to git *before* it ever exists in reality.
4. Classification drill: for your current project, list every
   secret it touches and where each lives today. One column: "fine
   now", one: "fix this week".

## 8. Common mistakes

- Adding the `.env` to `.gitignore` *after* it was committed —
  tracking is forever; the ignore only affects the future.
- "Temporary" tokens in notebooks — permanence is whatever git
  decides, not what you intended.
- Committing `.env.example` *with real-looking values* — the
  example that isn't fake enough becomes the leak.
- Rotating by editing the stored secret only — rotate *at the
  provider*, then update the stored copy; the old value remains
  valid otherwise.
- Believing private repos are safe — access spreads (teammates,
  CI systems, future public-ification); hygiene must not depend on
  the repo staying private.

> **Up next:** [Lesson 6 — monitoring
> layers](06-monitoring-layers.md): auditd, AppArmor vs SELinux,
> fail2ban, and malware-as-a-backup-problem.
