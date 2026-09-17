# Extension B Practice — Cloud Linux

## Quiz (10 questions)

Answer first; key at the bottom.

1. Complete the sentence: "A cloud is a very large ______ provisioned
   through an ______, rented by the ______."
2. Shared responsibility: classify — OS patching, hypervisor, security
   groups, physical security. Who owns each?
3. State the billing difference between RUNNING, STOPPED, and
   TERMINATED — and the trap in the third.
4. Block vs object storage: which one does a Postgres data directory
   need, and why?
5. Translate to course concepts: (a) security group, (b) VPC, (c)
   instance family, (d) object storage.
6. Your security group allows 22 from your office IP; ufw on the
   instance allows all. Can you SSH in? What if both are reversed?
7. What does cloud-init's user-data solve that Extension A's
   run-after-boot script cannot?
8. Name cloud-init's four stages and the two files you read to debug it.
9. Why does rebooting not re-run cloud-init? What *would* re-run it?
10. What is the NoCloud datasource, and why is it this course's chosen
    vehicle?

### Key (sketch answers)

1. …fleet of servers… through an API… rented by the second.
2. You: OS patching, security groups (your rules), in-instance
   everything. Provider: hypervisor, physical security. (Security
   groups sit at *your* edge — their *implementation* is the
   provider's, their *rules* are yours.)
3. RUNNING bills compute+disks; STOPPED bills disks only; TERMINATED
   bills nothing *but may leave volumes/snapshots billing quietly* —
   the trap is untracked attached resources.
4. Block: Postgres needs POSIX semantics — partial writes, fsync,
   random I/O — which object storage deliberately lacks.
5. (a) ufw at the network edge (default-deny rule set before your
   kernel), (b) M21's private address plan made declarative, (c) the
   vCPU/RAM shape choice (and for DS, the GPU ladder), (d) an HTTP API
   of named blobs — auth-gated file server, the artifact/backup home.
6. SG allows + ufw allows → in. Both "reversed" (SG denies, ufw
   allows) → **out**: the edge drops before the kernel ever sees the
   packet — the layer people forget when "it stopped working."
7. Configuration *at create-time, before first login* — no
   pre-existing SSH reachability or agent required.
8. detector → local → network → final; debug via
   `cloud-init status --long` and `/var/log/cloud-init-output.log`.
9. Modules are gated per instance-id (recorded after first run); a
   *new* instance (new id) re-runs from its user-data.
10. A datasource from plain files (user-data + meta-data on a seed
    disk/volume labeled `cidata`) — no provider, account, or metadata
    network needed, so the real cloud-init code path runs locally with
    zero spend.

## Challenges

**C1 — Console translator.** Open the documentation of any one
provider (or the university OpenStack docs) *read-only*; produce a
two-column table mapping ten console terms to the generic/course
concepts. No account creation — docs only. Deliverable: the table +
any term that *didn't* translate (they exist; name them).

**C2 — The cost model.** Write `estimate.sh`: given a shape (vCPU,
RAM, GB block storage) and hours-per-day, print a monthly cost range
using published on-demand prices for any two providers (paste the
prices as constants, cite them). Add the "forgot to terminate for a
year" line for a 1-volume instance. Deliverable: the script + one
paragraph on which lifecycle discipline the number justifies.

**C3 — Security group diff.** Two YAML security-group declarations:
one allows 22 from `0.0.0.0/0` and 8888 from anywhere; the other
allows 22 from a named office range and 8888 from nowhere. For each,
write the M25-style risk sentence, then the tunnel-based alternative
for the 8888 need (M22/M27 posture). Deliverable: the diff + sentences.

**C4 — user-data review.** A teammate's user-data contains: an inline
API key, `apt upgrade -y` at first boot, a public SSH key, and a
`curl | bash` installer. Review it as you would M25 §5: one risk
sentence per line, the reorder you'd propose, and what you'd fetch
post-boot via a secret manager instead.

---
*Back to: [Extension B index](README.md) · [M29 extensions](../README.md)*
