# Lab — Provision a VM from user-data (NoCloud, zero cloud)

> Extension B · Cloud Linux · Time: ~60 min · Environment: your own machine
> ⚠️ No cloud accounts, no provider CLIs, no credentials. The "provider"
> is a two-file seed. All networking is host-local (NAT/loopback).
> Two tracks: **QEMU** (real VM, needs ~15 GB disk) or **LXC** (lighter).
> If neither is available on your machine, the **container fallback**
> still runs cloud-init's NoCloud path.

## Part A — write the birth certificate (15 min)

`~/cloud-lab/seed/user-data` — the contract from lesson 3, tuned to boot
fast (small package set):

```yaml
#cloud-config
hostname: ds-cloud-01

users:
  - name: ds
    shell: /bin/bash
    sudo: ["ALL=(ALL) NOPASSWD:ALL"]
    lock_passwd: true                     # no password — key-only, M22 posture
    ssh_authorized_keys:
      - <paste the content of ~/.ssh/id_ed25519.pub>

package_update: true
packages: [git, python3-venv, tree]

write_files:
  - path: /etc/motd.d/provisioned         # evidence of the contract, at login
    content: |
      ds-cloud-01 — provisioned by cloud-init (NoCloud seed)
      manifest: see /var/lib/cloud/instance/user-data.txt
    permissions: "0644"

runcmd:
  - echo "[$(date -Is)] runcmd: node ready" >> /var/log/node-bootstrap.log
```

`~/cloud-lab/seed/meta-data` — the instance identity (NoCloud requires it):

```yaml
instance-id: ds-cloud-001
local-hostname: ds-cloud-01
```

Change `instance-id` → cloud-init re-runs; keep it → it won't (lesson
3's semantics — you'll *prove* this in Part D).

## Part B — build the seed and boot (20 min)

**QEMU track** (the most cloud-like — cloud images are qcow2, M17's
format awareness):

```console
$ cd ~/cloud-lab
$ genisoimage -output seed.iso -volid cidata -joliet -rock seed/user-data seed/meta-data
$ # download a cloud image once (Ubuntu 24.04 cloud image, ~600 MB):
$ qemu-img create -f qcow2 disk.qcow2 15G
$ qemu-system-x86_64 -m 2048 -smp 2 \
    -drive file=disk.qcow2,format=qcow2 \
    -drive file=seed.iso,format=raw,readonly=on \
    -netdev user,id=n0,hostfwd=tcp:127.0.0.1:2222-:22 \
    -device virtio-net-pci,netdev=n0 -nographic
```

Read that command as the cloud API made visible: the disk image *is*
the provider's template, `seed.iso` *is* the user-data field (volume
label `cidata` = the NoCloud trigger), and `hostfwd 127.0.0.1:2222`
*is* the security group rule — one port, loopback-bound (M25 posture,
edge edition).

**LXC track** (lighter — cloud-init runs inside a stock Ubuntu
container if the lxc templates include it):

```console
$ lxc launch ubuntu:24.04 ds-cloud-01 -c cloud-init.user-data="$(cat seed/user-data)"
```

**Container fallback** (no hypervisor available): a Docker container
from an image with cloud-init installed, seed mounted, verifying the
*datasource* mechanics even though boot is emulated — the lab notes
which parts are faithful (modules, logs, semantics) and which are
simulated (no real boot).

## Part C — log in and read the evidence (15 min)

```console
$ ssh -p 2222 ds@127.0.0.1              # key pre-seeded: no password ever existed
$ cloud-init status --long              # per-stage verdicts — lesson 3's first command
$ sudo cat /var/log/cloud-init-output.log | tail -25   # the transcript: modules & output
$ cat /etc/motd.d/provisioned           # the contract's evidence, at login
$ ls /var/lib/cloud/instance/           # what the instance RECEIVED (incl. user-data copy)
$ id && git --version                   # user exists, packages landed
```

Then the deliberate-failure drill — the fail-loudly contract at
provisioning time: add a misspelled package (`packagez: [zzz-not-real]`
→ correct the key) with a **new instance-id**, re-boot, and find the
failure: which stage, which module, what does `status --long` say, is
the instance still reachable? Restore, re-run clean.

## Part D — the instance-id semantics, proven (10 min)

```console
$ sudo reboot                            # (or stop/start via your hypervisor)
# after boot:
$ ls /var/lib/cloud/instances/           # same id — cloud-init did NOT re-run
$ sudo rm /etc/motd.d/provisioned        # break something user-data created
$ sudo reboot                            # …and it stays broken: first-boot only
```

Then change `instance-id: ds-cloud-002`, attach the same seed to a
*fresh* disk — and watch everything re-apply. Write the two-sentence
rule in your journal (lesson 3 Q3's answer, now witnessed).

## Done when

- [ ] Seed built (`genisoimage`/LXC flag) and instance booted with
      key-only login — no password at any point
- [ ] `cloud-init status --long` + output log quoted in `lab-log.md`
- [ ] Deliberate module failure located (stage, module, verdict) and
      recovered
- [ ] Part D's two reboots witnessed the per-instance-id rule
- [ ] One paragraph: map every element of your setup (image, seed,
      hostfwd) to its cloud-console equivalent (template, user-data,
      security group)

**Stretch:** add a `write_files` + `runcmd` pair that deploys your
Extension A `health.sh` as a systemd timer on first boot — the
Extensions A+B seam: provisioned monitoring on a provisioned node.
