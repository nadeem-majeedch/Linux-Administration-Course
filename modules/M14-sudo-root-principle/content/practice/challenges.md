# Challenge Problems — Module 14

Do these after the quiz. Report each in `lab-log.md`; all work in your own
VM/WSL2.

- [ ] **C1 — the pass-argument trap.** Explain why `sudo cat /root/secret >
      copy.txt` fails while `sudo sh -c 'cat /root/secret > copy.txt'`
      works, *then* the deeper trap: `sudo cat /root/secret` alone prints
      the file to your terminal — and `tee` can capture it. Map the three
      patterns onto "which process opens which file".
- [ ] **C2 — drop-in author.** Create `/etc/sudoers.d/ds14-prune`: members
      of group `dsstudents` may run, with no password, exactly
      `/usr/local/bin/prune-old` — a script (which you also write, root-
      owned 755) that deletes `*.tmp` files older than 7 days from
      `/srv/scratch` only. Prove the boundary: `sudo -n /usr/local/bin/prune-old`
      works; `sudo -n rm` does not. *(Safety: test `prune-old` first on a
      fake directory you build for the purpose.)*
- [ ] **C3 — forensic reading.** Run `journalctl _COMM=sudo --no-pager` on
      your VM and pick the busiest day. Write a 5-sentence narrative of
      "what this admin was doing" purely from the log. Note which
      information the log *lacks* (hint: full arguments are not always
      there — where do they live?).
- [ ] **C4 — recovery drill.** On a throwaway VM/snapshot: break sudo
      deliberately by adding `Defaults ignore_dot`… actually, simpler and
      safer: rename `/etc/sudoers` itself is *too* destructive — instead,
      add a drop-in containing a deliberate syntax error via `visudo -f`
      (watch it save you), then bypass visudo with
      `echo 'bogus line' | sudo tee /etc/sudoers.d/broken` and observe
      `sudo visudo -c` and `sudo -l` behavior. Repair. Write down the exact
      recovery path you'd use if this had been the main file (GRUB recovery
      or `wsl -u root`).
- [ ] **C5 — least-privilege rewrite.** Take this real-world bad drop-in and
      rewrite it minimally-permissively; justify each change:
      `%data ALL=(ALL:ALL) NOPASSWD: ALL`
      The team's actual needs: run `systemctl restart airflow-*`, and run
      `/usr/local/bin/backup-restore` (root-owned).
- [ ] **C6 — env forensics.** Write a tiny script `envdump.sh` that runs
      `env | sort > /tmp/env-$$-out` — run it three ways: as you, via
      `sudo envdump.sh`, and via `sudo -E envdump.sh`. Diff the outputs.
      Which variables did `env_reset` strip? Which survived? Name one that
      *should* be stripped always (`AWS_SECRET_ACCESS_KEY`, anyone?) and
      explain the leak path if `env_keep` were misused.
- [ ] **C7 — sudo as another user.** Explore `sudo -u postgres -H bash -c
      'echo $HOME; id'` on your VM (install `postgresql` first, or pick any
      service account). Explain the difference between `sudo -u`,
      `su - user`, and `sudo -iu user`. When is each the right tool? This
      returns in M20 when you inspect services' environments.

C4 in the wild: cloud images occasionally ship sudoers changes that break
on upgrade; the drill makes the recovery reflexive instead of terrifying.
