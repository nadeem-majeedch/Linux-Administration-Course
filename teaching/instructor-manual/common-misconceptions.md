# Common Misconceptions — The Bank

> Consolidated from all eight units' speaker notes, ordered by course
> week. Each entry: the wrong model → why it's sticky → the
> disconfirming demo → the correct mechanism to install. Use this as a
> pre-week refresher and during grading to name what you're seeing.

## Unit 1 (Weeks 1–2)

| Misconception | Why sticky | Disconfirming demo | Correct model |
|---|---|---|---|
| "Linux is an app you install" | desktop metaphor | show kernel panic vs app crash asymmetry | kernel = resource manager below apps |
| "Ubuntu = Linux" | first distro met | `dnf` on Ubuntu fails; same kernel, different userland | distro = kernel + packaging + policy |
| "The VM's 'Erase disk' erases my laptop" | installer text is scary | partition screen *inside* the VM with host disk visible in host OS | virtualization = the disk is a file |
| "Root is a stronger password" | sudo prompt looks like login | `sudo -l` shows *policy*, not power level | root is uid 0, a role; sudo is delegated policy |
| "1 GB RAM VM is fine" | small sounds efficient | compare boot+browser times 1 vs 4 GB | the VM competes with host for real RAM |

## Unit 2 (Weeks 3–4)

| Misconception | Why sticky | Demo | Model |
|---|---|---|---|
| "Home = root of disk" | `~` feels central | `ls /` beside `ls ~` | `/` is the tree; `~` is one branch |
| "`cd` in one terminal affects the other" | windows feel connected | `pwd` both after one `cd` | each shell is a separate process with its own cwd |
| "`uniq` removes duplicates" | the name says so | run `uniq` on unsorted data — doubled lines remain | uniq collapses *adjacent* equals |
| "`>` writes when the command finishes" | causal intuition | `ls > full-file` — file truncates instantly | redirection opens/truncates before exec |
| "grep and find are related" | both 'search' | grep a directory without -r vs find by name | find = files by metadata; grep = lines by content |

## Unit 3 (Week 5)

| Misconception | Why sticky | Demo | Model |
|---|---|---|---|
| "Scripts are a different language" | file vs prompt | paste a working one-liner into a file; run | same shell grammar, saved |
| "`set -e` makes it safe" | one-liner hope | `false || echo ok` exits 0 | set -e has documented exemptions |
| "shellcheck is pedantic" | warnings feel noisy | the classic `$VAR` split bug it catches | linter = reviewer who never sleeps |
| "chmod +x makes programs" | mental shortcut | `chmod +x notes.txt` then run — exec format error | x = *permission*, not transformation |

## Unit 4 (Week 6)

| Misconception | Why sticky | Demo | Model |
|---|---|---|---|
| "`chmod 777` fixes sharing" | it makes errors vanish | teammate deletes teammate's file; accountability gone | shared *groups* + SGID/sticky preserve order |
| "r on a directory means enter" | file intuition | `chmod 664 dir` — list names, cannot open | x = traverse; r = list names |
| "sudo is a bigger password" | prompt similarity | `sudo -l`, scoped drop-ins | policy engine + audit trail |
| "environment is global" | "the" PATH | `sudo` and `cron` see different env | env is inherited per-process |

## Unit 5 (Weeks 8–9)

| Misconception | Why sticky | Demo | Model |
|---|---|---|---|
| "`apt update` installs" | naming intuition | update then `apt list --upgradable` — nothing changed | update = catalogue refresh |
| "formatting is always catastrophic" | real-world trauma | mkfs on a *loopback* disk | the object defines the risk |
| "`kill -9` is professional" | force = control | trap script: TERM cleans, KILL skips | signal ladder: TERM → wait → KILL |
| "cron emails me failures" | docs say so | unlogged cron job fails silently | explicit logging is the contract |
| "load = CPU%" | both sound busy | load 4.0 on 32 cores = quiet | load = runnable+uninterruptible ÷ cores |

## Unit 6 (Weeks 10–12)

| Misconception | Why sticky | Demo | Model |
|---|---|---|---|
| "enable = run now" | verb confusion | enable without start — status inactive | enable = boot graph; start = runtime |
| "ping failing = network down" | ping = internet in pop culture | refused vs timeout distinction | ping is one rung, not the verdict |
| "keys are safe because they're on disk" | possession = security | stolen-laptop scenario; passphrase + 600 + agent | controls: mode, passphrase, never-copy |
| "`journalctl` is grep with steps" | old habits | grep binary journal dir vs `journalctl -u` | structured, indexed, boot-scoped |
| "used memory high = crisis" | task-manager instinct | `free -h`: used 7.2G, available 5.9G | cache is used-but-reclaimable; watch available |
| "firewall = allow my port" | positive framing | default-deny demo with justification | deny by default; allow *with reasons* |

## Unit 7 (Weeks 13–14)

| Misconception | Why sticky | Demo | Model |
|---|---|---|---|
| "Git copies the project on branch" | file-manager metaphor | commit graph: labels move, objects shared | branches are pointers |
| "pip into system python is fine" | works until it doesn't | apt python-package conflict story | system python belongs to apt |
| "Jupyter is a GUI app" | the browser lies | `ss -tlnp | grep 8888` shows the *server* | Jupyter = web server + kernels |
| "containers are small VMs" | marketing language | `docker run` in ms vs VM boot | shared kernel, isolated processes |
| "the dump file is my backup" | task completed feeling | restore it — into *what*, verified how? | backup = restorable, tested copy |

## Unit 8 (Weeks 15–16)

| Misconception | Why sticky | Demo | Model |
|---|---|---|---|
| "build is the project" | visible progress bias | phase weights: Operate 30% | administration is the graded skill |
| "snapshots replace backups" | snapshot feels safe | same-disk failure scenario | 3-2-1: different device, tested restore |
| "re-reading = revision" | familiarity ≠ recall | mock practical under clock | triage + evidence drills |

## Using the bank

- **Before each unit:** read the rows; plan which two you'll elicit
  deliberately (predict-phase bait).
- **During grading:** name the misconception in feedback — "this is the
  'uniq needs sort' model" teaches faster than a corrected command.
- **Contributing:** new rows come from anonymized transcript patterns;
  add them to the unit's speaker notes *and* here.
