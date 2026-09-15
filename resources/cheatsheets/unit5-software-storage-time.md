# Cheatsheet — Unit 5: Packages, Storage, Processes, Scheduling

## apt (M16)

```bash
sudo apt update                  # refresh package lists (always first)
apt search <term>; apt show <pkg>
sudo apt install pkg1 pkg2
sudo apt remove pkg              # keep configs;  purge = remove configs too
sudo apt autoremove              # drop orphaned dependencies
apt list --installed | grep pkg
apt-cache policy pkg             # installed + candidate versions, repos
dpkg -l | grep pkg               # low-level database
```

dnf (RHEL family): `dnf install/search/info` · pacman (Arch): `pacman -S/-Ss/-Q`.

## Storage (M17)

```bash
lsblk -f                # disks, partitions, filesystems, UUIDs
df -h                   # mounted filesystem usage
du -h --max-depth=1 DIR # what eats space
sudo parted /dev/sdb print            # partition table (VM disk only!)
sudo mkfs.ext4 /dev/sdb1              # format (destroys! VM disk only!)
sudo mount /dev/sdb1 /mnt/data        # attach now
findmnt --verify                      # validate fstab before reboot
```

fstab line: `UUID=...  /mnt/data  ext4  defaults,nofail  0  2`
Always snapshot first; never touch the system disk in labs; `nofail` keeps boot alive.

## Processes, jobs, signals (M18)

```bash
ps aux | grep -i python   # snapshot;  pgrep -af name
top / htop                # live view (q quits)
jobs; bg %1; fg %1        # job control;  Ctrl+Z suspend, Ctrl+C interrupt
./job &                   # background;  nohup ./job &  survive logout
kill -TERM PID            # polite stop (default) — try this FIRST
kill -KILL PID            # last resort (cannot be caught)
nice -n 10 ./job          # low priority;  renice 10 -p PID
uptime                    # load average (read vs core count)
free -h; lsof -p PID      # memory; open files of a process
```

## cron & timers (M19)

```
* * * * *  command
│ │ │ │ │
│ │ │ │ └ weekday 0-7 (0=Sun)
│ │ │ └── month 1-12
│ │ └──── day of month 1-31
│ └────── hour 0-23
└──────── minute 0-59
```

```bash
crontab -l                 # LIST before touching (-r deletes ALL — no prompt!)
crontab -e                 # edit your jobs
# 15 2 * * * /home/me/bin/dq.sh >> /home/me/logs/dq.log 2>&1
systemd-analyze calendar "Mon..Fri 09:00"   # validate schedules
systemctl --user list-timers; journalctl --user -u myjob
```

Cron gotchas: minimal PATH, no shell profile, relative paths break — use absolute paths.
