# Lesson 1 — The Transfer Toolbox: scp, sftp, and when rsync waits

> Module 23 · Unit 6 · Difficulty: Intermediate
> Reading time: ~25 min · Lab: [Lab 1, Parts A–B](../labs/lab-01-dataset-sync-circuit.md)
> Up next: [Lesson 2 — rsync fundamentals](02-rsync-fundamentals.md)

---

## 1. Three tools, three jobs

[M22](../../../M22-ssh-remote-admin/content/lessons/03-remote-execution-tunnels.md)
showed that `scp` is just an SSH connection carrying bytes. Keep that
model — it explains every flag and every failure. The toolbox has
three shelves:

| Tool | Shape of the job | Why this tool |
|---|---|---|
| **`scp`** | one-off copy of a file or tree | Zero ceremony: `scp file vm:~/`. No state, no comparison — it copies, period. |
| **`sftp`** | interactive browsing and ad-hoc moves | A shell-like session: look around, get/put several files, no new connection each time. |
| **`rsync`** | synchronization, bulk or repeated | Compares source and destination and moves **only the difference** — and can resume a broken transfer. |

The DS workload pattern: `scp` for "grab that one CSV", `sftp` for
"let me see what's actually in `/data/incoming`", `rsync` for "keep
my experiment folder synced to the server all week."

## 2. scp — precise and stateless

```console
$ scp local.csv vm:~/data/                # push: local → remote
$ scp vm:~/results/run1.csv ./            # pull: remote → local
$ scp -r ~/exp vm:~/                      # recursive: whole directory
$ scp -P 2222 local.csv vm:~/             # capital P: port (NOT ssh's -p!)
$ scp -C big.csv vm:~/                    # compress in flight (text only helps)
$ scp -3 a.csv b.csv                      # via your laptop (legacy; rare)
```

Two classic mistakes, both permanent:

- **`-p` vs `-P`.** `scp -p` preserves *timestamps/modes*; the port
  flag is capital `-P`. Wrong case = wrong meaning (ssh uses `-p`
  for port; scp diverges — historical accident, memorize it).
- **Overwriting.** `scp` silently replaces an existing destination
  file. There is no "are you sure". If the destination name matters,
  check first (`ssh vm 'ls -l ~/data/local.csv'`) or use `rsync
  --dry-run`, which reports what would change.

## 3. sftp — the interactive session

```console
$ sftp vm
sftp> pwd                 # remote working directory
sftp> lpwd                # *l*ocal working directory — the l-prefix rule
sftp> ls, lls, cd, lcd    # every command has a local twin
sftp> get run1.csv        # remote → local
sftp> put cleaned.csv     # local → remote
sftp> get -r raw/         # recursive get
sftp> bye
```

`sftp` is the right tool when you'd otherwise type five `scp`
commands in a row, or when you need to *look* before you transfer.
Batch mode exists for scripts (`sftp -b batchfile`), but a scripted
`rsync` is almost always the better automation answer.

## 4. Where rsync fits — and why it waits

If you copy a 5 GB directory twice with `scp`, it moves 10 GB. With
`rsync`, the second run moves only what changed — often megabytes.
rsync also transfers *only complete, correct* files (it writes to a
hidden temp name and renames on success), and it can **resume** an
interrupted transfer instead of starting a 5 GB file over.

That capability comes with a price: rsync *compares and mutates the
destination to match the source* — including deletions, if you ask
for it (`--delete`, Lesson 2). So the toolbox rule is:

> **Quick one-off copy you can afford to repeat → `scp`.
> Anything repeated, resumable, or deletable → `rsync`, with
> `--dry-run` first.**

## 5. Permissions land with the bytes

Files arrive with the identity of the *account that received them*
(`dsstudent` on your VM), not the sender. If your laptop user is
`nadeem`, the VM file is owned by `dsstudent` — usually exactly what
you want. But group-project setups (M13) care about the *group* of
new files: on shared trees, an rsync that preserves remote ownership
(`-o -g`, root-only) is a specialist operation; plain `-a` from your
own account keeps things simple and is what this course uses.

## 6. DS connection

Dataset work is transfer work: pull the raw feed onto the VM, push
cleaned outputs to shared storage, sync experiment folders to a GPU
box. Choosing `scp` where `rsync` belongs wastes hours (re-uploading
5 GB instead of 50 MB of deltas); choosing naked `--delete` where
care belongs can erase a semester. The toolbox decision is a
*professional judgment call* this course assesses.

## Self-check

- Which flag moves a *directory* with scp? Which sets the port?
- When is `sftp` better than two `scp` invocations?
- What does rsync know that scp doesn't — and what danger does that
  knowledge enable?

Up next: [Lesson 2 — rsync fundamentals](02-rsync-fundamentals.md).
