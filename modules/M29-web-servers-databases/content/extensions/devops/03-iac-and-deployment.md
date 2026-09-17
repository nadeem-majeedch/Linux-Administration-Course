# Lesson 3 — IaC, Terraform, and Deployment Patterns

> Extension C · DevOps on Linux · Difficulty: Advanced
> Reading time: ~30 min · Lab: continues in [Local CI](lab-01-local-ci.md)
> Teaching mode: Terraform **conceptually** — reading exercises only; no providers,
> no accounts, no state files that matter.

---

## 1. Configuration management vs infrastructure as code

Extension A introduced declarative configuration (Ansible): *the
insides of machines*. **Infrastructure as Code (IaC)** moves up a
layer: *the machines themselves, their networks, and their storage* —
the cloud objects from Extension B — declared as versioned text.

```text
  Layer            Tool family          Declares
─────────────────────────────────────────────────────────
  machines exist   IaC (Terraform)      "two VMs, this shape, this VPC,
                                         these security groups, this disk"
  machine insides  config mgmt          "these users, packages, units,
                   (Ansible)             this firewall policy"
  application      Docker/Compose       "this runtime, these mounts,
                   (M28)                 these ports"
  code             Git (M26)            "this is the change"
```

The layering is the lesson: each level consumes the one below and is
consumed by the one above. Terraform creates the instance; Ansible
configures it; Docker runs the app; Git versions all four
declarations. Teams that blur the layers (creating VMs in Ansible,
configuring inside Terraform) fight their tools; teams that keep them
review every change at the right altitude.

## 2. Terraform: the declarative object graph, conceptually

Terraform (HashiCorp; open source engine, many providers) reads
`.tf` files describing *desired infrastructure* and reconciles reality
toward them through provider plugins (AWS, GCP, Azure, OpenStack,
Proxmox, even Docker — providers are plugins against APIs, which is
why the skill transfers).

The workflow is its whole philosophy — three commands, in order:

```console
$ terraform plan      # compute the DIFF between reality and the manifest
$ terraform apply     # apply exactly that diff (after a human reads it)
$ terraform destroy   # remove everything the manifest created (tag-scoped)
```

**`plan` is the feature.** Every change — a new instance, a resized
disk, an opened port — arrives as a readable diff (`+ create`, `~
update in-place`, `- destroy`) *before* it happens. The M11
dry-run discipline and the M32-clinic blast-radius sentence, made into
a product: infrastructure changes become reviewable text, and the
"who opened that port?" archaeology becomes `git log` on the `.tf`
file.

Two concepts make it honest:

- **State** — Terraform records what it created in a state file, the
  bridge between manifest and reality. It is *sensitive* (contains
  attributes of everything, sometimes secrets) and *load-bearing*
  (lose it and Terraform forgets what it made) — hence state
  backends with locking, and the course rule: state files never live
  in the repo (M25 §5, again).
- **Plan/apply/destroy symmetry** — the same manifest that creates
  also destroys (cleanly, scoped by the manifest). Extension B's
  lifecycle discipline (lesson 2: cost, tagging, expiry) becomes
  mechanical: untracked resources are exactly the ones *outside* the
  manifest, and their existence is itself a finding.

Reading exercise (in the lab): a ~20-line Terraform manifest for two
VMs + a security group; map each stanza to Extension B's vocabulary —
and notice that you can read it *because* you speak the generic cloud
model.

## 3. Containers in the pipeline: the artifact that closes the gap

M28's lesson was "the image is the environment as an object." In the
DevOps loop that object becomes **the deploy artifact** — the thing
built once by CI, promoted through environments, and run identically
everywhere:

```text
  CI:  test code → docker build -t app:sha256-… → (push to registry)
  CD:  pull app:sha256-… → run beside old → health check → flip → keep old for rollback
```

The pinning rules from M28 carry verbatim and gain teeth: base images
digest-pinned (lesson 1 §4), built images tagged by *commit SHA*
(lesson 2 §3), and the registry (M28's "pulls only" rule) becoming the
one push destination when a real one exists — with the same
least-privilege IAM as every other API.

Why containers *fit* pipelines specifically: the runner can't drift
your app's environment (it doesn't have one — the image is), parity
between test and prod is structural (same image, different env vars —
lesson 1 §3), and rollback is image-tag rotation: run the previous
tag. The M27 venv discipline, promoted to the deployment unit.

## 4. Deployment patterns, honestly scaled

The patterns, from the course's toolbox upward — all achievable on
one VM with user units:

| Pattern | Mechanism | Course source | When it's enough |
|---|---|---|---|
| **In-place restart** | stop → update → start | M20/M29 | solo tools, tolerable downtime |
| **Reload vs restart** | config reload (no drop) vs process restart | M29 (nginx) | config-only changes |
| **Blue-green** | run new beside old, verify, flip, keep old | M28 compose ports / M20 units | anything user-facing |
| **Canary** | route 10% to new, watch, promote | M29 proxy + M24 monitoring | when "mostly right" is wrong |

The course's version of blue-green on one VM: the new service binds a
second port, the pipeline smoke-tests it, nginx's `proxy_pass` flips
(M29's one-line config change + reload), and the old unit stays
stopped-but-present for one working day — rollback as a
`systemctl --user start`, not an archaeology. The verify step (health
endpoint through the *public* path) is the M32-clinic discipline, and
the keep-the-old window is the runbook's rollback section (Extension A
lesson 3) made real.

Monitoring closes the loop (lesson 1 §4): the deploy that follows a
canary or blue-green *watches* the health series before deleting the
old — M24's evidence habit as a deployment gate.

---

## Key takeaways

- IaC declares the *machines* (Terraform), CM their *insides*
  (Ansible), Compose the *runtime* (M28), Git the *everything* —
  keep the layers clean.
- Terraform's workflow — **plan → apply → destroy** — makes
  infrastructure changes reviewable diffs; its state file is
  sensitive, load-bearing, and never in the repo.
- The container image is the **deploy artifact**: built once from a
  digest-pinned base, tagged by SHA, promoted, and rolled back by tag
  rotation.
- Deployment patterns scale from restart to blue-green on one VM; the
  constants are the **smoke-test gate** and the **kept-old rollback
  window**.

## Check yourself

1. State the four IaC-adjacent layers and one tool per layer. What
   fails when a team blurs two layers?
2. Why is `terraform plan` the feature rather than `apply` — and what
   course discipline is it the product of?
3. Why must the state file never live in the repo? Name both reasons.
4. In the one-VM blue-green pattern, what are the three non-negotiable
   steps after the new service binds?
5. How does rollback work in an image-based deployment, and why is it
   *safer* than "git revert + rebuild" in the moment?

*Answers:* (1) Machines (Terraform), insides (Ansible), runtime
(Compose), code (Git); blurring (e.g., creating VMs in Ansible)
produces half-tracked state — objects exist that the declarative tool
can't see or reconcile. (2) Because it renders the *diff before the
change* — reviewable, arguable, abortable; it's the M11 dry-run +
M32-clinic blast-radius sentence, productized. (3) Sensitivity (it can
contain secrets/attributes) and load-bearingness (it's the
reality-bridge; loss or tampering desynchronizes manifest and world).
(4) Smoke-test through the *public* path (health endpoint); flip the
proxy; keep the old unit stopped-but-present for the rollback window.
(5) Re-point to the previous image tag (or start the kept old unit) —
safer because it's a *known-good artifact already running in prod
before*, not a rebuild that re-enters all the CI risk with production
down.

Next: [Lab — local CI](lab-01-local-ci.md) — the robot, on your laptop.
