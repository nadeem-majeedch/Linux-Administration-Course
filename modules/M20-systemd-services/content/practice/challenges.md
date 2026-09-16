# Challenge Problems — Module 20

After the quiz; own VM, user units preferred. Record evidence in
`lab-log.md`.

- [ ] **C1 — the boot map.** `systemd-analyze critical-chain` +
  `blame | head -10` on your VM. Write the three-sentence story of your
  boot: what gated what, which unit you'd tune first, and what you'd
  *not* touch (why).
- [ ] **C2 — socket activation (read + reason).** `systemctl cat
  ssh.socket` if present (newer Ubuntu) — explain in 3 sentences how
  socket activation differs from always-running, and one benefit for
  a rarely-used service.
- [ ] **C3 — the templated unit.** Write `webhook@.service` such that
  `systemctl --user start webhook@9001` serves M08's http.server on
  port 9001 (`ExecStart=/usr/bin/python3 -m http.server %i --directory
  %h/www`). Start two instances (9001, 9002). Templated units are how
  real fleets avoid copy-paste.
- [ ] **C4 — harden hello.** Add to your hello.service: `PrivateTmp=
  yes`, `NoNewPrivileges=yes`, `MemoryHigh=100M` + `MemoryMax=200M`.
  Verify it still runs; then break the memory cap deliberately
  (`hello-hog.sh` allocating 300M) and read what systemd does (man
  systemd.resource-control → OOM behavior). Report the evidence.
- [ ] **C5 — the oneshot + timer preview.** Write `log-archive.service`
  (Type=oneshot: tars lab-log) and peek at an existing timer
  (`systemctl cat fstrim.timer`). Name the two pieces a *timer* needs
  — full timer authoring is M19, this is the shape.
- [ ] **C6 — rescue rehearsal.** In your VM: GRUB-edit to
  `rescue.target`, from the root shell *read-only-inspect* the system
  (mount, systemctl list-units --failed equivalents), then reboot
  normally. Write what rescue gave you that a running system doesn't,
  and why cloud instances need a different door.
- [ ] **C7 — the post-mortem.** `journalctl -b -1` on your VM after a
  deliberate reboot: find the *last three* messages before shutdown
  and the *first five* after boot. Write the boot's biography in five
  lines (shutdown reason → firmware → kernel → units → login).
- [ ] **C8 — migrate a cron job.** Take any M19-style periodic job
  you'd have written as cron (`@daily tar …`) and express it as a
  `.service` + `.timer` pair on paper. Three sentences: what systemd
  adds (dependencies, logging, missed-run policy via Persistent=).

C3 and C4 are the "hire-able" skills: templated units and resource
control are daily bread on real fleets.
