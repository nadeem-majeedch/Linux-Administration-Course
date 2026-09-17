# Lesson 4 — Configuration Management Concepts (Ansible, Conceptually)

> Extension A · Server Administration · Difficulty: Advanced
> Reading time: ~30 min · Up next: [Extension B — Cloud Linux](../cloud/README.md)
> Teaching mode: **concepts and reading** — no Ansible installation required (the lab's
> provisioning script *is* the imperative ancestor of these manifests)

---

## 1. The problem configuration management solves

Lesson 2's provisioning script solves consistency for *one node shape*
if you run it by hand per node. At fleet scale that becomes: N nodes ×
M policies × manual orchestration = drift with extra steps.
**Configuration management (CM)** is the tooling category that makes
policy *executable and self-enforcing*:

> Declare the desired state; the tool computes and applies the
> difference; re-running converges.

Two design poles exist, and knowing them organizes every tool you'll
meet:

- **Imperative** — scripts that *do steps* (`apt-get install …`).
  Flexible, familiar (your provisioning script), but the end state is
  implicit in the steps.
- **Declarative** — manifests that *describe the end state* ("package
  git is present; user ds exists; service jupyter enabled"). The tool
  figures out the how and — crucially — **detects drift** by comparing
  reality to the declaration.

Your skeleton script already half-way converged: its `|| exists`
guards *simulate* declarativeness. CM tools formalize it.

## 2. The landscape in one paragraph each

- **Ansible** (Red Hat; agentless, Python): SSH-based — the control
  node pushes YAML "playbooks" over the same SSH you mastered in M22.
  No agent to install on targets; the inventory is a text file; tasks
  are declarative modules (`apt`, `user`, `service`, `copy`). The
  course's closest cultural match: it *is* your provisioning script,
  declaratized, running through M22's channel.
- **Puppet / Chef** (agent-based, older school): a resident agent on
  each node pulls its manifest from a master. Powerful at very large
  scale; the agent infrastructure is itself a system to operate.
- **SaltStack**: master/agent with fast messaging; the middle ground.
- **NixOS / declarative OS**: the whole *system* is a declaration — the
  strongest form of the idea; a different lifestyle than incremental
  CM.

Course scope: **Ansible conceptually** (it's the most common in DS
shops), the others as vocabulary. The exam question is never "which
tool" — it's "declarative vs imperative, agent vs agentless, push vs
pull."

## 3. Reading an Ansible playbook (the course, translated)

Inventory first — lesson 2's fleet file, formalized:

```ini
# inventory.ini
[ds_nodes]
ds-analysis-01 ansible_host=10.0.2.15
ds-analysis-02 ansible_host=10.0.2.16

[ds_nodes:vars]
ansible_user=ds
```

And a playbook — read each task against the M-source it encodes:

```yaml
# playbook.yml — "the desired ds-node" (declarative lesson-1 script)
- hosts: ds_nodes
  become: true                      # sudo, M14
  tasks:
    - name: base packages present   # M16
      ansible.builtin.apt:
        name: [git, ufw, python3-venv]
        state: present
        update_cache: true

    - name: ds user exists          # M12
      ansible.builtin.user:
        name: ds
        shell: /bin/bash
        state: present

    - name: SSH key deployed        # M22 — key from the repo, never typed
      ansible.posix.authorized_key:
        user: ds
        key: "{{ lookup('file', 'keys/ds.pub') }}"

    - name: firewall — allow SSH only   # M25
      community.general.ufw:
        rule: allow
        name: OpenSSH

    - name: firewall enabled
      community.general.ufw:
        state: enabled

    - name: jupyter unit deployed   # M20/M29 — unit from the repo
      ansible.builtin.copy:
        src: files/jupyter.service
        dest: /home/ds/.config/systemd/user/
        owner: ds
      become_user: ds

    - name: jupyter enabled         # M20
      ansible.builtin.systemd:
        name: jupyter
        enabled: true
        scope: user
      become: true
      become_user: ds
```

Every lesson of this course appears *as a module*: `apt` (M16), `user`
(M12), `authorized_key` (M22), `ufw` (M25), `copy` + `systemd`
(M20/M29), with `become` as M14's sudo. The run is:

```console
$ ansible-playbook -i inventory.ini playbook.yml --check --diff   # the dry-run (M11's lesson, formalized)
$ ansible-playbook -i inventory.ini playbook.yml                  # apply
$ ansible-playbook -i inventory.ini playbook.yml                  # re-run: nothing changes = converged
```

Note the built-ins mapping to course habits: `--check`/`--diff` is the
dry-run discipline (M11 lesson 3), idempotent re-runs are the
convergence check (lesson 2), and "changed=N" output is the drift
report — generated, not hand-written.

## 4. What CM changes about *thinking*

Three shifts, each of which you've already made once in this course:

1. **From steps to state** — like venvs (M27): you stopped describing
   how to build the environment and pinned *what it should be*. CM
   does that for servers.
2. **From snowflakes to cattle** — any node can be rebuilt from the
   repo; the loss of a server becomes an incident of minutes, not a
   disaster of archaeology.
3. **From memory to review** — policy changes are pull requests
   (M26): diffed, discussed, applied by the tool, logged by the tool.
   The change log in lesson 3's runbook stops being hand-written and
   starts being generated.

**Honest limits (and why the lab still uses a script):** Ansible
assumes SSH-reachable targets and a control node with Python — real
infrastructure this course's labs deliberately avoid installing. The
lab's bash provisioner *is* a legitimate CM for one-to-five boxes; the
playbook above is its roadmap for growth. Concept mastery, tool
later — exactly the course's pattern for Terraform and GitHub Actions
in Extensions B and C.

---

## Key takeaways

- CM = declarative manifests + convergence + drift reporting; the two
  design axes are imperative/declarative and agent/agentless.
- **Ansible**: agentless, SSH-pushed YAML; its modules are this
  course's lessons (apt/user/authorized_key/ufw/systemd) rewritten as
  state.
- `--check --diff` = dry-run discipline; the unchanged re-run =
  convergence proof; "changed=" lines = drift findings.
- The mindset shifts — state-not-steps, cattle-not-snowflakes,
  review-not-memory — are the transferable part; tools are details.

## Check yourself

1. Name the two design axes of CM tools and place Ansible on both.
2. In the playbook, which module encodes M25's firewall policy — and
   why *two* tasks rather than one?
3. What does the second (unchanged) run of a playbook prove, and what
   is that proof called in lesson 2's vocabulary?
4. Why does the course call the lab's bash script "a legitimate CM for
   small fleets" despite teaching Ansible?

*Answers:* (1) Imperative-vs-declarative and agent-vs-agentless (plus
push-vs-pull); Ansible: declarative, agentless, push. (2)
`community.general.ufw` — two tasks because *allowing* (rule state)
and *enabling* (service state) are two independent declarations; each
is separately idempotent and separately checkable. (3) Zero changes on
re-application proves reality already matches the declaration —
convergence; the unchanged output is the consistency evidence.
(4) Because it already has the three CM essentials (idempotent,
logged, self-verifying) without requiring SSH-keyed targets or a
Python control node — the concepts are the curriculum; the tool is an
implementation choice.

Up next: [Extension B — Cloud Linux](../cloud/README.md) — where fleets
actually live.
