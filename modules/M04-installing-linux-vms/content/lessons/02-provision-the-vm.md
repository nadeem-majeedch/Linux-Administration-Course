# Lesson 2 — Provision the VM

> Module 04 · Unit 1 · Difficulty: Beginner
> Reading time: ~25 min · Lab: [Lab 1](../labs/lab-01-provision-the-vm.md)
> Up next: [Lesson 3 — verify and first boot](03-verify-and-first-boot.md)

---

## 1. The provisioning sequence

Four steps, in this order — each one catches the previous step's
mistakes:

1. **Download** the ISO from an official Ubuntu source (never a
   mirror you can't name).
2. **Verify** it (M02's Lab 2: SHA-256 from the published
   `SHA256SUMS`, signature if offered).
3. **Provision** the VM: sizing decisions first, then attach the ISO.
4. **Install** through the server installer, then snapshot.

The order is the lesson: verification *before* an hour-long install,
sizing *before* the installer asks, snapshot *before* you explore.

## 2. Sizing decisions (and why)

| Resource | Course setting | Why |
|---|---|---|
| vCPU | 2 | enough for labs; M24's load clinic wants *multiple* cores to make load averages honest |
| RAM | 4 GiB | Jupyter + Postgres + Docker coexist comfortably; M24's OOM demos need headroom to *observe* swapping before death |
| Disk | 25 GiB | Ubuntu Server ~5 GiB; datasets, containers and M17's loopback disks fit with room to fill *some* of it safely |
| Network | NAT (default) | VM reaches out; nothing on your LAN reaches in — the safe default until M22 teaches explicit forwarding |

**Disk honesty:** the 25 GiB is usually *dynamically allocated* — the
file grows as you use it. It will not consume 25 GiB on day one, and
M08's `df`/`du` will make you fluent in telling allocated vs used.

## 3. The installer, annotated

Ubuntu Server's Subiquity installer asks, in order — with the course
answers and the *reason*:

| Prompt | Course answer | Why it matters later |
|---|---|---|
| Keyboard/language | yours | wrong layout poisons every password you type |
| Install type | Use entire disk (the **VM's** disk) | M17 will teach what partitions *are* — today the VM's virtual disk is expendable; the installer only erases the VM, never your host |
| Profile setup | your name, `ds` as username, strong password | this is the **normal user** the whole course assumes — you are *never* root by default (M14) |
| SSH server | ✅ **install OpenSSH server** | M22 begins here; retro-fitting is easy but why not now |
| Featured snaps | none | course uses apt; M16 covers snap separately |

**Username habit:** pick something you'd be willing to type in an
SSH command thousands of times. Short, lowercase, no spaces.

## 4. First boot checklist

After install + reboot (and ISO unmount):

```console
login as your user, then:
$ sudo -v && whoami                    # password works; sudo warms (M14)
$ ip -brief address                    # note the NIC name + address (M21)
$ systemctl --no-pager --failed        # fresh boot should be clean (M03)
$ df -h /                              # note real usage (M08 revisits)
```

A clean boot shows **no failed units**. If something is already
failed on day one, that's your first troubleshooting exercise —
`journalctl -b -p err` and read (M03 §2).

## 5. The snapshot (the module's real deliverable)

In VirtualBox: **Machine → Take Snapshot** → name it
`clean-install-<date>`. virt-manager: snapshot per domain. Hyper-V:
checkpoint.

**What a snapshot is:** the VM's disk state, frozen — return here any
time, even months from now, even after a catastrophic lab.

**What it is not:** a backup (Lesson 4's whole point — snapshots live
*inside* the same host as the VM; lose the host, lose both) and not
a substitute for M26's discipline. It is the *reset button*, and the
reset button is the reason every later module can say "you may break
this freely".

Take **two** before moving on: `clean-install` (pristine) and
`post-M04` (after Lab 1's checks). The difference between them is
your first evidence of "what setup did I actually do?"

---

**Key takeaways**

- Verify before installing; size before the installer asks; snapshot
  before exploring.
- The installer creates a *normal user* — the course never assumes
  root (M14's whole thesis starts here).
- SSH server installed at day one saves M22's retrofit.

**Check yourself:** why does NAT (rather than bridged) networking
make the first weeks safer? What module will change that, and how?

**Next:** [Lesson 3 — verify and first boot](03-verify-and-first-boot.md)
