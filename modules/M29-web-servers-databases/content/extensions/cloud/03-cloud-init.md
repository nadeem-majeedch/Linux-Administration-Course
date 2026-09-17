# Lesson 3 — cloud-init: The First-Boot Contract

> Extension B · Cloud Linux · Difficulty: Advanced
> Reading time: ~30 min · Lab: [Local cloud-init provisioning](lab-01-local-cloud-init.md)
> Prerequisites: Extension A's provisioning script (this is its declarative cousin)

---

## 1. The first-boot problem, solved twice

Extension A provisioned servers by *running a script on them
afterwards* — which requires the server to already exist and be
SSH-reachable. Cloud instances solve it differently: the provider
hands the instance a **user-data blob** at create-time, and a first-boot
agent inside the image — **cloud-init** — executes it *before you ever
log in*. The result: an instance that comes up already configured —
users, keys, packages, firewall — from its birth certificate.

This is the same idea as M28's Dockerfile at a different layer: a
declarative recipe the machine applies to itself. And it is *the*
bridge skill of this extension: cloud-init is provider-neutral (every
major cloud feeds it user-data; so can you, locally), text-based
(versionable — M26), and idempotent-by-design (it runs once, and its
modules are state-assertions like Ansible's).

## 2. What user-data looks like

Two styles exist; real deployments mix them.

**The `#cloud-config` YAML style** — declarative modules, reading like
the course's inventory:

```yaml
#cloud-config
hostname: ds-analysis-01

users:
  - name: ds
    groups: [adm, sudo]
    shell: /bin/bash
    sudo: ["ALL=(ALL) NOPASSWD:ALL"]      # lab-level; production scopes this
    ssh_authorized_keys:
      - ssh-ed25519 AAAA… ds@laptop       # M22's key, pre-seeded

package_update: true
packages:                                  # M16, declared
  - git
  - python3-venv
  - ufw

write_files:                               # config as files (M25's backup discipline,
  - path: /home/ds/README.txt              #  baked at birth)
    content: |
      Provisioned by cloud-init — see /var/log/cloud-init-output.log
    owner: ds:ds
    permissions: "0644"

runcmd:                                    # the imperative tail (M11 habits apply)
  - sudo -u ds python3 -m venv /home/ds/venv
  - sudo ufw allow OpenSSH
  - sudo ufw --force enable
```

**The shell-script style** (`#!/bin/bash` user-data) — exactly your
Extension A provisioner, executed at first boot. Useful for small
things; the YAML modules are preferred because each is logged,
checked, and individually skippable if already satisfied.

## 3. The lifecycle: what runs when

cloud-init runs in **four stages** at boot — knowing them turns its
logs from noise into a checklist:

```text
 1 detector   — am I supposed to run? (first boot? datasource present?)
 2 local      — network may not be up yet: early config
 3 network    — the main event: users, packages, write_files, config
 4 final      — runcmd, everything else; services may start
```

Every stage logs; the two files you will actually read:

```console
$ sudo cat /var/log/cloud-init-output.log    # the transcript: every module's output
$ sudo cloud-init status --long              # per-stage verdict: done/errors
$ sudo cloud-init query userdata             # what user-data the instance RECEIVED
```

`cloud-init status --long` is this lesson's `systemctl status` — the
first command, the honest state; the output log is the journal tail.
Failures are **loud and located**: a bad package name fails the
package module in the network stage, visibly, while the instance is
otherwise up — the fail-loudly contract (M24/M27) at provisioning
time.

**The once-per-instance rule:** cloud-init's modules run *per instance
id* — a reboot re-runs nothing (it's not a service); a *re-created*
instance re-runs everything. That's the right semantics: first-boot
configuration, not ongoing management (which stays Ansible's job —
Extension A lesson 4; the boundary is a favorite interview question).

## 4. The datasource abstraction (and how you'll run it locally)

cloud-init doesn't care *who* feeds it user-data — it asks a
**datasource**: the cloud's metadata service (`169.254.169.254` — a
link-local HTTP API every provider implements, M21's localhost
concept at datacenter scale), a CD-ROM label, or — the course's
favorite — **`NoCloud`**: plain files on a seed disk/volume.

That last one is the trick that makes this course's lab possible with
zero cloud: a `user-data` file + `meta-data` file on a local seed ISO,
attached to a QEMU/LXC VM (or, in the container variant, just placed
where cloud-init looks). The VM boots, cloud-init finds the NoCloud
datasource, and applies your contract — the exact cloud workflow,
executed on your laptop:

```console
$ ls seed/                 # the "provider" is two files
meta-data  user-data
$ <hypervisor command> … seed.iso   # create-time attachment = the cloud's user-data field
$ ssh ds@<vm-ip>                     # first login: key was pre-seeded — no password ever existed
```

Security notes that carry to real clouds: user-data can contain
secrets, and (on most providers) *any instance on the account can read
its own and the metadata service* — the M25 §5 rule becomes "secrets
in user-data are readable by the instance and its metadata route;
prefer secret managers or post-boot injection", and the famous
metadata-service SSRF attacks are the reason providers added
token-guarded versions. The habits from M25 are not optional in
clouds; they are the *only* defense.

---

## Key takeaways

- **cloud-init = first-boot configuration from user-data** —
  declarative modules + an imperative tail, provider-neutral via the
  datasource abstraction.
- Read it with `cloud-init status --long` + `cloud-init-output.log`;
  failures are loud, per-module, and located in a stage.
- **Per-instance-id semantics**: reboots don't re-run; re-creations
  do — first-boot config, not fleet management (that's Ansible).
- **NoCloud** turns two files into a "provider" — which is why this
  course can teach the real workflow with zero accounts and zero
  spend.

## Check yourself

1. What problem does user-data solve that Extension A's
   run-after-creation script cannot?
2. A package name in user-data is misspelled. Where does the failure
   appear, in which stage, and is the instance still reachable?
3. Why does rebooting not re-run cloud-init — and what *would* re-run
   it?
4. Why is NoCloud the course's chosen datasource, and what two files
   does it need?
5. Where do secrets belong if not in user-data, per M25's extension to
   clouds?

*Answers:* (1) Configuration *at create-time, before first login* —
no pre-existing SSH reachability or agent required; the machine
applies its own birth certificate. (2) In
`/var/log/cloud-init-output.log` under the package module, network
stage; `cloud-init status --long` shows the error — the instance is
up and reachable (that stage's other modules still applied). (3)
Modules are gated per instance-id: the instance fingerprint is
recorded after first run; a *new* instance (new id) re-runs from its
user-data. (4) It needs no provider, account, or metadata network —
just files on a seed disk — making the real cloud-init code path
runnable locally; `user-data` + `meta-data`. (5) In a secrets
manager / encrypted store fetched post-boot with least-privilege IAM,
or injected by configuration management after the fact — because
user-data (and the metadata service) is readable by the instance and
anything that can make it issue requests.

Next: [Lab — local cloud-init provisioning](lab-01-local-cloud-init.md) —
the workflow, for real, on your laptop.
