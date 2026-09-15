# Lab 3 — The Repository Audit: Trust, PPAs & Security Debt

> Module 16 · Unit 5 · Difficulty: Intermediate
> Environment: your own **disposable VM** (snapshot if you can) · Time: ~40 min
> Prerequisites: [Lesson 2](../lessons/02-repositories-security-ppas.md)
> The audit is read-only; the PPA test-drive is done add→verify→**remove**
> on the disposable VM only.

## Part A — audit your sources (read-only)

```console
$ grep -rEh "^(deb|URIs|Suites|Components)" /etc/apt/sources.list /etc/apt/sources.list.d/ 2>/dev/null | sort -u
$ ls /etc/apt/sources.list.d/                      # drop-ins: who else lives here?
$ apt policy | head -20                            # every source + priority
```

**Record:** your complete source inventory. For each: official Ubuntu
archive, third-party vendor, or PPA? Are `noble-security` and
`noble-updates` present (on WSL2 images they sometimes aren't — note it
if so)? Any source with a `signed-by=` keyring — where does that key
come from?

## Part B — the trust check

```console
$ ls /etc/apt/keyrings/ 2>/dev/null
$ sudo apt update 2>&1 | grep -iE "signed|gpg|warn|err" | head
```

A clean run prints no GPG warnings. **Record:** any warning lines and
their meaning (Lesson 2 §2). A warning is apt's trust system speaking —
decode it, don't silence it.

## Part C — the PPA test-drive (disposable VM)

We add the most famous PPA in the DS world, *verify* what it changes,
and remove it — the full hygiene loop:

```console
$ sudo add-apt-repository -y ppa:deadsnakes/ppa    # adds source + key
$ ls /etc/apt/sources.list.d/                      # the drop-in file appeared
$ cat /etc/apt/sources.list.d/deadsnakes-*.sources 2>/dev/null || cat /etc/apt/sources.list.d/deadsnakes-*.list
$ apt policy python3.11                            # which source now offers it?
$ sudo apt update && apt policy python3.11         # compare priority of sources
```

**Record:** before/after for `apt policy python3.11`. Which *suite* would
win if you installed (PPA priority 500 vs archive 500 — tie broken how?
Look at the version numbers `apt policy` shows). Then the removal:

```console
$ sudo add-apt-repository -y --remove ppa:deadsnakes/ppa
$ ls /etc/apt/sources.list.d/ | grep -i deadsnakes || echo "source gone"
$ apt policy python3.11                            # back to archives only
```

**Record:** one paragraph: what the PPA gave, what it cost (support
story, update story), and the exact two commands that undo an
`add-apt-repository`.

## Part D — the security debt dry-run

```console
$ apt list --upgradable 2>/dev/null | tail -n +2 | wc -l
$ apt-get --dry-run upgrade 2>/dev/null | grep -cE "^Inst "   # same number? why not?
$ apt list --upgradable 2>/dev/null | grep -iE "openssl|libssl|curl|python3.1" | head
$ apt-get changelog openssl 2>/dev/null | head -12            # read one fix
```

**Record:** pending count; whether it includes security-sensitive
libraries; for one package, the changelog's headline (CVE id or summary).
Then *decide*: on this personal VM, run the upgrade (safe, previewed) or
log it as follow-up homework — either way, record the decision.

## Part E — the audit report (deliverable)

Half a page, structured like a real review:

1. **Sources:** N official, N third-party, N PPAs; anomalies.
2. **Trust:** keys verified / warnings found / verdict.
3. **Security:** pending count, notable items, action taken.
4. **Recommendation:** the one change you'd make to this machine's
   software sourcing (e.g., "add noble-security; it's missing").

## Done when

- [ ] Source inventory + trust check recorded
- [ ] PPA added, its effect *measured* via apt policy, and removed
- [ ] Security debt counted, one changelog read, decision recorded
- [ ] Audit report written
- [ ] (If snapshotted) VM restored to pre-lab state
