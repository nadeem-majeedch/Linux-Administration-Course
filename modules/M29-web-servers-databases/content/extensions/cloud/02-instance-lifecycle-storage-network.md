# Lesson 2 — Instance Lifecycle, Storage, and Networking

> Extension B · Cloud Linux · Difficulty: Advanced
> Reading time: ~30 min · Up next: [cloud-init](03-cloud-init.md)

---

## 1. The instance lifecycle (states, and what they bill)

A cloud instance is a VM with a *state machine* — and unlike your M04
VM, the states have price tags:

```text
  API: create                API: start
    ┌─────────┐  stop    ┌─────────┐
    │ PENDING │ ───────► │ RUNNING │ ──► (in use: this is where you work)
    └─────────┘          └────┬────┘
         ▲        start       │ stop / terminate
         │    ┌──────────┐    │
         └─── │ STOPPED  │ ◄──┘   ┌───────────┐
              └──────────┘        │ TERMINATED│ (gone; disk per its policy)
                    reboot = stop+start in place
```

The billing subtleties worth knowing before they cost money:

- **RUNNING** bills compute. **STOPPED** usually bills *only the
  attached disks* — cheap storage, no CPU. **TERMINATED** bills
  nothing but may leave volumes/snapshots behind (the quiet-billing
  trap from lesson 1).
- **stop vs terminate** is M18's SIGTERM-vs-SIGKILL at machine scale:
  stop is recoverable (start again, disk persists); terminate is
  destructive *by design* — and its safety is the **persistent disk**
  policy (below).
- **Reboot from inside** (`sudo reboot`) vs from the API: inside is
  the OS you know; the API one is for "the SSH session is dead" —
  both end at the same running kernel.

Metadata every instance carries: its type (vCPU/RAM shape — the
"instance family" ladder from 1 vCPU to GPU monsters), its tags
(owner/purpose/expiry — lesson 1's discipline), and its **user-data**
(next lesson's topic).

## 2. Storage: block vs object (the two DS realities)

Cloud storage splits into two families, and data science uses both
*differently*:

**Block storage (the disk)** — a volume attached to one instance,
appearing as `/dev/vdb`-class device: literally M17's `disk.img`, made
someone else's problem to persist.

- Lifecycle options: **delete-with-instance** (scratch/temp — the safe
  default for throwaway compute) vs **persist** (datasets, databases —
  survives terminate). Choosing deliberately *is* the discipline: the
  scratch default prevents quiet billing; the persist flag protects
  the data. Snapshots = point-in-time copies (M24's backup model,
  provider-implemented — and the same **untested-restore rule**
  applies to them).
- Performance classes (throughput/IOPS tiers) map to M24 Clinic
  lesson 3's instruments: the same `iostat await` tells you when the
  tier is wrong.

**Object storage (S3-class)** — not a disk at all: an HTTP API to
named blobs, unlimited capacity, accessed with `GET/PUT` over HTTPS
(M21's HTTP with authentication). The DS workhorse for datasets,
model artifacts, and backup targets (M24's "off-site copy" made
concrete).

- It is *not* POSIX: no partial writes, no directories (prefixes
  instead), list-and-fetch semantics. Tools (`s3cmd`/`rclone`/`mc`
  class) put a file-ish face on it; the model underneath matters when
  a 40 GB single blob "upload" is the wrong shape (chunk it).
- Access control is IAM + per-bucket policy — the secrets lesson
  (M25 §5) applies: *keys never in the repo*, and public buckets are
  how datasets leak.

| | Block volume | Object storage |
|---|---|---|
| Appears as | `/dev/...` filesystem | HTTP API of blobs |
| Attached to | one instance | reachable from anywhere (auth-gated) |
| Best for | OS, databases, live scratch | datasets, artifacts, backups |
| M-source | M17 disks | M21 HTTP + auth |
|_billing_ | per GB-month (while attached!) | per GB-month + requests |

## 3. Networking: VPC, security groups, and the edge

The cloud re-implements your M21/M25 networking as configurable
objects:

```text
            internet
               │
        ┌──────┴──────┐
        │  VPC 10.0.0.0/16   (your private address space — M21 §2)
        │  ┌───────────────────────────┐
        │  │ public subnet 10.0.1.0/24 │ ← instances with internet egress
        │  │  ┌──────────────┐         │
        │  │  │ ds-analysis  │◄── security group: 22 from <office IP> only
        │  │  └──────────────┘         │
        │  └───────────────────────────┘
        │  ┌───────────────────────────┐
        │  │ private subnet 10.0.2.0/24│ ← databases: no direct internet, ever
        │  └───────────────────────────┘
        └─────────────────────────────
```

- **VPC/subnets** — your private address plan (M21's subnetting,
  made declarative): public-facing work in public subnets, data work
  in private ones.
- **Security groups** — a *stateful* edge firewall per instance,
  evaluated **before** traffic reaches your kernel: M25's ufw model
  moved outward. The twin rule carries: ufw *and* the security group
  both allow, or nothing flows — and when "it just stopped working"
  after a redeploy, *this* is the layer people forgot (the
  M32-clinic connectivity card, one rung earlier than usual).
  Course posture, cloud edition: 22 from known ranges only, app ports
  via tunnel/bastion — never 0.0.0.0/0 "temporarily".
- **SSH at fleet scale** — the M22 patterns professionalized: key
  pairs registered *at create-time* (no passwords ever existed), and
  for private subnets a **bastion/jump host** — M22's `ProxyJump`
  chapter becoming architecture.

## 4. Monitoring from the outside

The provider meters the *hypervisor view*: CPU utilization, network
in/out, disk ops — visible as time series in their console/API (the
M24 sar concept, host-implemented). Two honest notes for a DS admin:

- Hypervisor metrics answer "is the *machine* healthy"; they do not
  answer "is *pandas* healthy". Your in-instance kit (M24's health.sh,
  journal skills) still owns the application truth — the two layers
  complement: provider says CPU pinned at 100%, your `pidstat` says
  which process and since when.
- The M32-clinic lesson holds verbatim: provider graphs are evidence
  for the resource conversation; your instruments remain the verdict.

---

## Key takeaways

- Instance states have **price tags**: RUNNING bills compute, STOPPED
  bills disks, TERMINATED can leave volumes behind — lifecycle
  discipline is cost discipline.
- **Block = disk** (M17, delete-with-instance vs persist is a
  deliberate choice); **object = HTTP blobs** (M21 + auth, the DS
  artifact home) — different tools, both already understood.
- VPCs and security groups are M21/M25 declarative: plan addresses,
  default-deny at the edge, and remember *both* firewalls when
  debugging reachability.
- Provider metrics = hypervisor truth; your M24 kit = application
  truth; the DS admin reads both layers.

## Check yourself

1. A teammate "deletes" an instance to save money. Where can costs
   quietly continue, and which two lifecycle concepts govern that?
2. Why is object storage the natural home for model artifacts — and
   why is it *not* the natural home for a Postgres data directory?
3. Your app worked yesterday; today the browser can't reach it. The
   instance runs, ufw allows the port, `ss` shows the listener. Which
   cloud-layer object do you inspect next, and what changed most
   likely?
4. What does the bastion pattern solve that public-subnet-only cannot?

*Answers:* (1) Attached block volumes and snapshots bill regardless of
instance state; the concepts are disk *persistence policy* and the
tag-for-expiry discipline — delete the volumes or accept the storage
bill knowingly. (2) Artifacts are write-once/read-many blobs fetched
over HTTP — object storage's exact shape (and it needs no attached
instance); Postgres needs POSIX semantics (partial writes, fsync,
random I/O) that object storage deliberately lacks — that's a block
volume's job. (3) The **security group** — the edge layer people
forget exists (especially after a redeploy recreates the instance
with a default group); `ss` proves the kernel sees nothing because
the *edge* is dropping, not the app. (4) It keeps sensitive instances
in private subnets with no internet path at all, while admin access
happens through one hardened, audited jump host — smallest possible
exposed surface, every session logged in one place.

Up next: [cloud-init](03-cloud-init.md) — configuring the machine at
first boot.
