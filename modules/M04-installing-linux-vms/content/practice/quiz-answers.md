# Module 04 Quiz — Answer Key

## Section A

**Q1.** 4 GiB is what the *labs* need (Jupyter + Postgres + Docker
coexist; M24 needs headroom to observe swapping). On an 8 GiB host
that forces **serial work**: one VM at a time, host apps closed — the
constraint is scheduling, not impossibility. Half credit for "it
fits" without the constraint.

**Q2.** Works: M05–M12 command-line modules — real kernel, real
tools. Partial: M20/M24 (systemd works *after* `wsl.conf`
enablement); M22 (SSH to *localhost* or a second imported distro —
no second machine). Fails: M03 Lab 2 — no bootloader exists; also any
lab needing a true network boundary (two hosts) without extra
tooling. The reason: WSL2 shares one kernel with a synthetic
platform — no firmware/GRUB act, one namespace-fence around
everything.

**Q3.** Resource: ~1 GiB RAM + disk reclaimed for datasets. Pedagogy:
the course's entire skill set is terminal-and-configuration; a GUI
invites point-and-click habits, and *servers are where DS actually
runs* (M31) — honest rehearsal.

**Q4.** NAT: VM can reach out; nothing inbound by default — no
accidental exposure of sshd/Jupyter to the LAN/Internet. M22
deliberately adds host-only/port-forwarding, *with* a firewall
conversation (M25).

**Q5.** Isolation (host files/credentials unreachable), reset
(snapshots), fidelity (real kernel/systemd/root). A web terminal
gives fidelity-lite of the *shell* only; no reset for kernel/boot
breakage, and isolation is someone else's sandbox policy.

## Section B

**Q6.** A tampered ISO whose tamperer also publishes a matching
checksum manifest — integrity to *their* bytes. The signature over
the manifest (`SHA256SUMS.gpg`, verified against Ubuntu's official
key) closes it: they can't forge the publisher's signature.

**Q7.** Investigate (read, don't install yet): the manifest covers the
*release set*; missing lines mean you fetched only some files — which
is fine if *your* ISO's line is `OK`. The danger case is your ISO
line missing or `FAILED`. Judgment: `OK` on the target file = the
verification you needed.

**Q8.** Proven: the signature is mathematically from the private key
matching that public key. Not proven: that the key *is* Ubuntu's.
Next step: compare the key's fingerprint against ubuntu.com's
published fingerprint, then locally certify (`--lsign-key`). The
warning is the web-of-trust gap, not a failure.

**Q9.** The ISO is the root of trust for everything the system
becomes: every package, key, and default arrives via it. Verifying
after install proves nothing retroactively — you'd be auditing a
crime scene by the culprit's notes.

## Section C

**Q10.** On a VM, "the disk" is a virtual 25 GiB file — expendable,
host-safe. On a dual-boot host, the installer sees *real* disks
including Windows'. Re-confirm at: (1) the disk-selection screen
(identity/size must match the virtual disk), (2) the confirmation
screen naming the device node it will erase.

**Q11.** Convenience: no retrofit chore. M22-relevant: SSH-enabled-
at-birth means the *first* remote session can be to a server whose
origin you fully know (you saw every install choice) — a cleaner
security story than "and then I installed sshd from somewhere."

**Q12.** The sudo model (M14): root is a *role you assume* with
auditable logging, not an account you inhabit daily. Installers
following it give you least-privilege from minute one; a set root
password invites `su`-as-lifestyle, unlogged.

**Q13.** The file grows on demand: 6.2 GiB = actually written so far.
Inside the VM, `df -h` reports the *filesystem's* view — up to 25 GiB
capacity, current usage ~5–6 GiB. The gap between host file size and
VM usage is thin provisioning; M08 makes you fluent in both views.

## Section D

**Q14.** The hypervisor forks the disk's state: existing bytes stay
put, new writes go to a small delta file. No 25 GiB is copied —
instant because only *future* changes are captured.

**Q15.** Host/hypervisor loss: snapshots live inside the same host
file(s) — disk failure, theft, ransomware on the host destroy VM and
snapshots together. Only a copy on *different* storage (M26) survives.

**Q16.** Milestone naming + cadence: a current `working-<date>`
snapshot kept fresh (old one deleted), taken *after* each unit's
completion — so reverts land you at "last good unit," not "week
ago." `pre-<module>` snapshots bound the blast radius of dangerous
labs.

**Q17.** Each snapshot adds a delta layer; reads/writes traverse the
chain. End-state: coalesce/delete — keep one current `working-…`,
delete superseded milestones (VirtualBox "delete snapshot" merges).

**Q18.** It must contain: exact steps, in order, testable by a
tired stranger — which snapshot to revert to, what to re-run, and how
to verify success (the evidence pair). Depends on: the snapshot
inventory (naming discipline) and the recorded day-one evidence
(lab log/`lab-environment.md`) that defines "working."
