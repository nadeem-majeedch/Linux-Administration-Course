# Answer Key — Module 20 Quiz

Each answer cites the lesson to revisit.

1. systemd (systemd, version from `systemctl --version`); starts
   everything at boot in dependency order, supervises/restarts
   services, logs to the journal. (L1 §1)
2. service (daemons), timer (scheduling), mount (filesystems),
   socket (activation), target (groups/states), device (kernel
   devices). (L1 §2)
3. /usr/lib/systemd/system (vendor) < /run/systemd (runtime) <
   /etc/systemd/system (admin — wins). Package updates overwrite /lib.
   (L1 §2)
4. Vendor file at that path; currently *enabled* (a wants-symlink
   exists); the distro's preset default was also enabled. (L1 §4)
5. start = run now; enable = at every boot; `enable --now` = both at
   once. (L1 §4)
6. **active + disabled** — running this boot only. (L1 §4)
7. Creates a symlink from the unit into a target's `.wants/`
   directory (e.g. multi-user.target.wants/). (L1 §4)
8. `systemctl --failed` (or list-units --state=failed). (L2 §1)
9. Dot/color, Loaded, Active, Main PID+CGroup, log tail; the loop
   tell: Active: activating (auto-restart) with repeated "since Ns
   ago". (L2 §2)
10. reload re-reads config without dropping connections (if the daemon
    supports it — ExecReload exists); when you're SSHed *through* ssh,
    restart would cut your own session. (L2 §1)
11. `journalctl -u UNIT -n 20 --no-pager`; `journalctl -u UNIT -f`;
    `journalctl -u UNIT -p err --since yesterday --no-pager`. (L2 §3)
12. The per-user systemd manager (no sudo, own units); lingering keeps
    the user manager alive after logout so services survive; trade:
    your quota is consumed while logged out. (L2 §4)
13. ```ini
    [Service]
    MemoryMax=2G
    CPUQuota=50%
    ```
    (L2 §4)
14. [Unit] metadata/relations (After=), [Service] how to run
    (ExecStart=), [Install] what enable wires (WantedBy=). (L3 §1)
15. simple = systemd considers it started the moment ExecStart forks;
    forking = it daemonizes (parent exits); oneshot = it exits by
    design. Default simple — correct for foreground scripts. (L3 §2)
16. Endless restart churn: main process exits immediately, manager
    re-schedules; journal shows repeated "Started/Scheduled restart
    job" pairs. (L3 §2, Lab 2 incident 2)
17. After any unit-file edit (outside systemctl edit); edits are
    invisible to systemd — you run old definitions while reading new
    ones. (L3 §3, Lab 2 incident 3)
18. e.g. User=/DynamicUser= (run unprivileged), NoNewPrivileges=
    (blocks escalation), ProtectSystem=strict (read-only system
    paths), PrivateTmp= (private /tmp). Met in shipped units'
    [Service] blocks. (L3 §4)
19. `sudo systemctl edit UNIT` → write only changed directives in
    `/etc/systemd/system/UNIT.d/override.conf` → auto-reload →
    restart; undo: `systemctl revert UNIT`. (L3 §5)
20. firmware → bootloader (GRUB) → kernel+initramfs (M17: fstab pass-1
    mounts /) → systemd (M20's whole module) → getty/DM. (L4 §1)
21. Boots straight to rescue.target once — a root shell for repairs;
    safe because edits are one-boot-only (nothing persists). (L4 §2)
22. ```ini
    [Unit]
    Description=Training queue daemon
    [Service]
    ExecStart=%h/bin/queue-daemon
    Restart=on-failure
    RestartSec=5
    MemoryMax=4G
    [Install]
    WantedBy=default.target
    ```
    stdout/stderr → the journal (`journalctl --user -u …`). (L3 §3)
23. blame sums per-unit activation times (parallel!); critical-chain
    walks the dependency path — a slow unit off the chain delays
    nothing. (L4 §1)
