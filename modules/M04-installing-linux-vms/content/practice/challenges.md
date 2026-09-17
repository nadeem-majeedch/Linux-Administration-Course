# Challenge Exercises — M04

> All challenges run on your own host/VM. C3/C4 involve no risk —
> the risk is *skipping* them and meeting the skill first during a
> real incident.

## C1 — The sizing argument

Your team gets one physical server (16 cores, 64 GiB, 2 TiB) to turn
into a shared lab: **five student VMs** for this course. Write the
allocation table (vCPU/RAM/disk per VM), justify each number against
the course's actual workloads (M24's load clinic, M28's containers,
M31's training run), and state the two resource-contention failures
you'd expect if you overcommitted — with the instrument that would
reveal each (name the module).

## C2 — Verification under imperfection

The `SHA256SUMS` server is unreachable, but you have: the ISO, a
`SHA256SUMS` from a campus mirror, and Ubuntu's signing key fetched
from ubuntu.com. Design the verification: which parts still prove
integrity? authenticity? Write the exact command sequence and the
honest limitations of what you can claim afterward. (This is the
"mirror is down, defense is due" scenario.)

## C3 — The revert rehearsal

Deliberately, on your own VM: (1) snapshot `pre-c3`; (2) break
something *cosmetic but persistent* — e.g. replace `~/.bashrc`'s
prompt with something garish and `sudo apt install cowsay`; (3) from
**inside** the VM, without reverting yet, document exactly what state
you'd lose beyond the cosmetic bits (any pending lab logs? apt
lists?). (4) Revert, verify with the evidence pair. Then write the
two-sentence rule for *when* reverting beats repairing.

## C4 — Dual-boot interrogator (paper exercise)

A friend asks you to dual-boot Ubuntu onto their Windows laptop.
Produce the interrogation checklist: every question you'd ask and
every check you'd run *before* touching the installer (BitLocker?
UEFI vs legacy? free space? backups?), plus the two installer screens
where mistakes are unrecoverable, and the safer alternative you'd
recommend instead. Cite the lesson that shaped each item.

## C5 — Environment-as-document

Exchange `lab-environment.md` with a classmate (shared drive, not
Git yet — M26 comes). Each of you: attempt to reconstruct the other's
VM state *from the document alone* — list their snapshots, state
their reset procedure back to them, and identify one ambiguity that
would block an actual reset. Fix your own document accordingly.
The graded artifact: your *revised* `lab-environment.md` + the
ambiguity you found in theirs.
