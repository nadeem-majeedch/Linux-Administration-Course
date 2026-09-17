# Lab 2 — The WSL2 Track

> Module 04 · Unit 1 · Difficulty: Beginner · Est. time: 30 min
> Environment: Windows 10/11 with WSL2 available (SETUP.md covers
> install). This lab makes WSL2 *honest* about what it is — and gets
> it to feature parity with the VM track for the modules ahead.

## 1. Check what you have

In PowerShell:

```powershell
wsl.exe --status
wsl.exe --list --verbose
```

Record: WSL version, your distro name, and whether it's **VERSION 2**
(generally is, on updated Windows). Ubuntu LTS from the Store is the
course distro; `wsl --install -d Ubuntu-24.04` if absent.

## 2. Enable systemd (the course requirement)

Many modules (M20, M24, M29) need a real init. In the WSL shell:

```console
$ sudo tee /etc/wsl.conf >/dev/null <<'EOF'
[boot]
systemd=true
EOF
```

Then in **PowerShell**: `wsl.exe --shutdown`, wait 8 s, reopen. Verify:

```console
$ cat /proc/1/comm        # systemd — not "init" or "sh"
$ systemctl is-system-running
```

Record both. If `is-system-running` says `degraded`, that's real
diagnostic material — `systemctl --failed` and read (M03's habit).

## 3. The parity circuit

Run and record, exactly as a VM student would:

```console
$ sudo -v && whoami
$ ip -brief address           # note eth0's odd address space — WSL NAT
$ df -h /
$ hostnamectl
$ uname -r                    # a Microsoft-built kernel — note the suffix
```

## 4. The honest-differences table

Write, from evidence not memory:

| Capability | VM | WSL2 | Source of difference |
|---|---|---|---|
| systemd / units | yes | after §2 | init is boot-time; WSL boots differently |
| M03 Lab 2 (GRUB) | yes | n/a | no bootloader |
| Windows↔Linux files | via share | seamless (`/mnt/c`) | 9P filesystem — note `stat` oddities on `/mnt/c` |
| Second "machine" for M22 | clone VM | second distro (`wsl --import`) or localhost-only | one kernel shared |
| M17 loopback disks | yes | losetup works | same kernel |
| Port forwarding | NAT config | localhost auto-forwards to Windows | WSL networking model |

## 5. Deliverable

`wsl2-environment.md`: §1 status, §2 evidence, §3 circuit outputs,
§4 table completed with your observed values, and a closing
paragraph: **which three course labs would you substitute, and with
what?** (You may consult the labs' "WSL2" notes, but the reasoning
must be yours.)

Finally, add one §4 row of your own: **what stands in for the VM
snapshot on your track, and what can it actually restore?** (Honest
answers include "nothing full-machine — I can only reconstruct files";
WSL2 has no checkpoint equivalent, so your real reset button is
documented commands, e.g. re-running this lab.)

## Troubleshooting

- `systemctl` says "System has not been booted with systemd" — §2
  wasn't applied or `wsl --shutdown` didn't happen; redo and check
  `/proc/1/comm`.
- Slow `/mnt/c` access — expected (9P); keep course work in `~/`,
  which lives in the Linux filesystem.
- Time drift — enable `hwtime` sync per SETUP.md; NTP confusion
  breaks TLS later (M29) and cron (M25) in confusing ways.
