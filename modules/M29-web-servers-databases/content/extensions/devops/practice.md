# Extension C Practice — DevOps on Linux

## Quiz (10 questions)

Answer first; key at the bottom.

1. What wall does DevOps remove, and what is the loop that replaces it?
2. "If it isn't in the repo, it doesn't exist" — name three artifact
   classes this covers beyond source code.
3. Why does "commit early, commit small" become an operational
   property in DevOps?
4. CI vs CD (delivery vs deployment): state the difference and where
   the human sits on the risk dial.
5. Why can a fresh runner per job not suffer drift — and what replaces
   the long-lived server's "state"?
6. In a workflow, what do `needs:` and `runs-on:` each control?
7. Why tag built images with the commit SHA instead of `latest`?
8. Where do pipeline secrets live and how are they exposed to steps?
   What happens when one appears in a log?
9. Place Terraform, Ansible, Compose, and Git on the four IaC layers.
10. In the one-VM blue-green pattern, name the three non-negotiable
    post-bind steps.

### Key (sketch answers)

1. The dev/ops handoff wall; the write→commit→pipeline→deploy→operate
   loop with feedback as commits.
2. Environment contracts (requirements.txt), pipeline definitions
   (workflows), infrastructure manifests (IaC), runbooks, config
   templates — anything the running system depends on.
3. The commit is the unit of deploy *and rollback*: small commits make
   reverts surgical and failures bisectable.
4. CI: every push is built+verified automatically. Delivery: artifact
   packaged/ready, human triggers deploy. Deployment: the trigger is
   automatic — the dial is how much human gate sits before production.
5. Ephemeral runners share no state between runs; the *manifest*
   (pinned deps, image) is the state — reproducibility as
   architecture.
6. `needs:` = job dependency/gating order; `runs-on:` = the runner
   environment (which ephemeral machine class executes the job).
7. The SHA anchors the artifact to the exact code that built it —
   traceability and rollback anchoring; `latest` is the mutable-tag
   sin at deploy scale.
8. In the platform's secret store; injected as environment
   variables/files at runtime and masked in logs. If one reaches a
   log: it's burned — rotate/revoke first, then fix the leak.
9. Machines = Terraform; insides = Ansible; runtime = Compose;
   everything = Git.
10. Smoke-test through the public path; flip (proxy/port); keep the
    old unit stopped-but-present for the rollback window.

## Challenges

**C1 — Workflow archaeology.** Take this lab's `ci.yaml` and annotate
every line with its course source (module + lesson). Any line you
can't source is a signal you're copying syntax you don't understand —
research it, then annotate. Deliverable: the annotated file.

**C2 — The drift-proof experiment, quantified.** Extend the lab's
Part C: pollute the *runner's* base image instead of the host (build a
tiny broken image with a stale pandas), point `act` at it with `-P`,
and show the workflow *still* passes (or fails differently). Then
digest-pin the base image and show stability. Deliverable: the three
runs + one paragraph.

**C3 — Secrets audit of a workflow.** A teammate's workflow contains
`run: curl -H "Authorization: token $MY_TOKEN" …` with
`env: MY_TOKEN: ghp_xxxx` *in the file*, plus a debug step
`run: env | sort` for "visibility". Identify every leak, state the
fix per leak (secret store injection, log masking, removal of the
debug step), and write the two-sentence PR review you'd leave.
Deliverable: the review.

**C4 — Terraform reading exam.** Write (on paper, no providers) a
~25-line Terraform manifest for Extension B's lab shape: one VM
(specify shape), one block volume (persist: true), one security group
(22 from office, nothing else), all tagged owner/purpose/expiry.
Annotate each stanza with its Extension B vocabulary. Then write what
`plan` would print on the first run vs a run after changing the shape
line. Deliverable: the manifest + the two hypothetical plans.

---
*Back to: [Extension C index](README.md) · [M29 extensions](../README.md)*
