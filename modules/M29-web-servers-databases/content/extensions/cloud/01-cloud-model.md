# Lesson 1 — The Cloud Model: A Datacenter Behind an API

> Extension B · Cloud Linux · Difficulty: Advanced
> Reading time: ~25 min · Up next: [Instance lifecycle, storage, networking](02-instance-lifecycle-storage-network.md)

---

## 1. What "cloud" actually is (and isn't)

Strip away the marketing and a cloud is a **very large fleet of servers
provisioned through an API**, rented by the second. Everything else
follows from that sentence:

- **Virtualization at scale** — the M04 hypervisor lesson, run by a
  provider: your "machine" is a VM (or container) on their hardware,
  carved from a template.
- **Self-service via API** — the provider exposes *provisioning* (Extension
  A's discipline) as HTTP calls: create instance, attach disk, open
  firewall port. Consoles and CLIs are just clients of that API.
- **Metered payment** — resources bill while they exist, which is why
  the instance *lifecycle* (next lesson) is a first-class concept:
  forgetting to delete a VM is a subscription, not an incident.
- **Elasticity** — the fleet can grow/shrink programmatically. This is
  the actual revolution: capacity as code, not procurement.

What it isn't: a different operating system. **Your instance runs the
same Ubuntu; the same systemd, journald, SSH, ufw, and apt apply.**
Extension A's skills are the operating skills; the cloud adds
*provisioning speed* and *network topology under your control* — which
is why this course taught the Linux first and the cloud second.

## 2. The shared responsibility model

The cloud's most important contract, and the source of most cloud
security failures when misread:

```text
  YOU (the customer)                          THE PROVIDER
─────────────────────────────          ─────────────────────────
 OS configuration & hardening (M25)    Physical security
 Users, SSH keys, sudo policy (M12/22) Hardware & hypervisor
 Packages & patches (M16)              Network *fabric* reliability
 Firewall rules (ufw AND security grp) Host compliance (ISO/SOC…)
 Services & their logs (M20/M24)       Core infrastructure (power, cooling)
 Data & its backups (M24)              Isolation between tenants
```

The rule of thumb: **the provider secures the cloud; you secure what
you put in it.** "It's in the cloud" is not a security posture —
M25's checklist applies verbatim inside an instance, plus the network
edge (next lesson's security groups, which are *yours* to configure).

## 3. The generic cloud map (provider-neutral vocabulary)

Every major provider implements this shape; only names differ:

| Concept | Generic term | AWS calls it | GCP calls it | Azure calls it |
|---|---|---|---|---|
| A virtual machine | **Compute instance** | EC2 | Compute Engine | Virtual Machine |
| A disk | **Block storage volume** | EBS | Persistent Disk | Managed Disk |
| A file/blob store | **Object storage** | S3 | Cloud Storage | Blob Storage |
| Your private network | **Virtual network (VPC)** | VPC | VPC | VNet |
| Edge firewall per instance | **Security group** | Security Group | Firewall rule | NSG |
| First-boot configurator | **user-data / cloud-init** | EC2 user-data | metadata user-data | Custom Data |
| Who-can-do-what | **IAM** | IAM | IAM | Entra/RBAC |

Learn the *left column*. Providers are interchangeable once you speak
it — including the university's own OpenStack cloud and the cheap
European providers (Hetzner/OVH) that many research groups actually
use. This course deliberately teaches the left column and *names* the
right columns only so you can translate.

## 4. The API-driven datacenter: provisioning as code

The conceptual leap from Extension A: when provisioning is an API,
**infrastructure becomes programmatic** — scripts create instances,
tag them, configure their firewall, attach storage, and (crucially)
*delete* them. Two consequences:

- **Reproducibility at infra level** — the manifest isn't just
  configuration (Ansible), it can include the *existence* of the
  machine: this is **Infrastructure as Code** (IaC; Terraform is the
  lingua franca, taught conceptually in Extension C). A lost server
  becomes a re-run.
- **Cost and lifecycle discipline** — resources that can be created by
  script *must* be deletable by script, with the same evidence
  discipline (tags: owner/purpose/expiry). The cloud's failure mode is
  not crashes; it's the untracked resource billing quietly at 3 a.m.
  Your M24 log-line habit becomes a *tagging* habit.

The API also changes *who* can do what: IAM policies decide which
keys may create/destroy what — the M13/M14 least-privilege lesson,
extended to the datacenter. A data-science team's IAM hygiene (one
key per human, scoped, rotated) is the same discipline as one SSH key
per human, scoped, with passphrase.

---

## Key takeaways

- Cloud = **API-provisioned, metered, elastic** virtualization; the OS
  inside is the same Linux you administer.
- **Shared responsibility**: provider owns the fabric; you own
  everything in the instance — M25 travels intact.
- Speak the **generic vocabulary** (instance, volume, object storage,
  VPC, security group, user-data, IAM); provider names are dialects.
- API-driven provisioning makes **IaC and lifecycle discipline**
  mandatory: infrastructure as reviewable, deletable code.

## Check yourself

1. Why does this course claim "the cloud adds provisioning speed and
   network topology, not a new OS"?
2. In the shared-responsibility table, who owns "patching the OS"? Who
   owns "the hypervisor"? What failure does misreading this cause?
3. Translate: an "S3 bucket" and a "security group" — to this course's
   concepts.
4. Why does API-driven provisioning make *deletion* discipline as
   important as creation discipline?

*Answers:* (1) Because the instance runs the same Ubuntu/systemd/SSH
stack all 28 modules taught — what changes is how fast machines appear
and how you wire their networks, both of which are provisioning
concerns. (2) You patch the OS; the provider runs the hypervisor.
Misreading (either direction) leaves OS vulnerabilities unpatched —
the classic cloud breach is an unpatched, exposed instance, not a
provider failure. (3) S3 bucket ≈ object storage: a file server with
an HTTP API (M21's HTTP + auth); security group ≈ the edge firewall —
ufw's rule model enforced before traffic reaches your instance.
(4) Because creation is now cheap and fast, untracked resources
accumulate silently and bill continuously — the evidence/tagging
discipline (owner/purpose/expiry) is what keeps the API fleet
accountable.

Up next: [Instance lifecycle, storage, networking](02-instance-lifecycle-storage-network.md) —
the machinery under the map.
