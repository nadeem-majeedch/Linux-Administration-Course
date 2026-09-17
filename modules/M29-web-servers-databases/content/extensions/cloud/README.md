# Extension B — Cloud Linux (Provider-Neutral)

> M29 extensions · Difficulty: Advanced · Time: ~4 hours
> Environment: your own VM; cloud-init exercised **locally** (no cloud accounts)
> Prerequisites: Extension A (server lifecycle), M21, M22, M25

The university GPU server is *someone else's* fleet; cloud computing is
the model where you — the data scientist — provision your own slice of
a datacenter through an API. This extension teaches the **generic cloud
model**: the concepts every provider implements (AWS, GCP, Azure,
OpenStack, university OpenStack/Hetzner/OVH clouds alike), so that the
skills transfer rather than lock in.

**Provider neutrality is a hard rule of this course**: no accounts are
created, no provider CLIs are installed, no credentials exist. Cloud
concepts are exercised *locally* — most importantly **cloud-init**,
which runs happily inside a QEMU/LXC VM or even a container with its
`nocloud` datasource. The lab provisions a real VM from a real
`user-data` file, exactly as a cloud would, on your laptop.

## Files

| # | File | Topic |
|---|------|-------|
| 1 | [01-cloud-model.md](01-cloud-model.md) | The generic cloud: VMs/instances, regions, shared responsibility, the API-driven datacenter |
| 2 | [02-instance-lifecycle-storage-network.md](02-instance-lifecycle-storage-network.md) | Instance lifecycle & states, block vs object storage, VPC/security-groups models, monitoring hooks |
| 3 | [03-cloud-init.md](03-cloud-init.md) | First-boot configuration: user-data, the nocloud datasource, reading real cloud-init logs |
| 4 | [lab-01-local-cloud-init.md](lab-01-local-cloud-init.md) | **Local lab:** provision a VM (or container) from a user-data file — the cloud workflow, zero cloud |
| — | [practice.md](practice.md) | 10 questions + key, 4 challenges |

## The transfer thesis

By the end you should be able to read *any* provider's console or docs
and map every term to something you already own:

| Cloud term | You already know it as |
|---|---|
| Instance / droplet / compute engine | Your M04 VirtualBox VM |
| Security group / firewall rules | ufw (M25), at the network edge |
| Block storage volume | M17's virtual disk (`disk.img`) |
| Object storage (S3-class) | A file server with an HTTP API (M21) |
| SSH key pair registered at create-time | M22's `authorized_keys`, pre-seeded |
| Instance metadata & user-data | This extension's cloud-init |
| Provider CLI/Terraform | Extension A's provisioning script, against an API |

Start: [Lesson 1 — the cloud model](01-cloud-model.md)
