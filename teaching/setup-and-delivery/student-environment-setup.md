# Student Environment Setup — Per-Term Verification

> Students follow the repo-root [`SETUP.md`](../../SETUP.md) (three
> supported paths: **A** VirtualBox VM — recommended, **B** WSL2,
> **C** native install — optional). This guide is the *instructor's*
> companion: what to verify in the Week-1 setup session, and how to
> triage the four failures you will actually see.

## Week-1 setup session (first 30 minutes of Lab 1)

Project the success criteria; students verify their own install:

| Check | Command | Passing looks like |
|---|---|---|
| 64-bit Ubuntu LTS | `lsb_release -a` | the course's stated version |
| Kernel visible | `uname -r` | non-empty; print it (M03 hook) |
| User is themselves | `whoami` | their username, **not** `root` |
| sudo works | `sudo -v` | password prompt, then silence |
| Network inside sandbox | `curl -I https://ubuntu.com` | HTTP/2 200 or 301 |
| Text tools present | `grep --version && sed --version` | version lines |
| Git present | `git --version` | ≥ 2.40 |
| Python present | `python3 --version` | ≥ 3.10 |

Everyone who passes all eight writes their VM name + snapshot count on
the attendance sheet; the **first snapshot** (`pristine`) is taken
before anything else happens in Lab 1.

## Triage: the four real failures

1. **"VT-x/AMD-V is not enabled" (VirtualBox)** — BIOS virtualization
   off. Fix is a reboot into firmware settings; have the BIOS-key
   cheat (F2/F10/F12/Del by vendor) on the projector *before* the
   session. This is 80% of setup-day pain.
2. **WSL2: "WSL 2 requires an update to its kernel component"** —
   run `wsl --update` from *Windows PowerShell as admin*; then
   `wsl --shutdown` once. Document the exact two lines on the board;
   students on managed laptops may need IT to run them.
3. **Disk full on host** — students gave the VM 25 GiB but the *host*
   is the constraint. Teach the snapshot discipline now: snapshots
   store diffs, so a week of `rm -rf` practice without cleanup grows
   the host file. `VBoxManage` compact, or delete redundant snapshots.
4. **`sudo: user is not in the sudoers file`** — they created a user
   without admin during install (Path C), or WSL default user wasn't
   set. Fix: from WSL, `ubuntu config --default-user <name>`; from a
   live USB, the official Ubuntu recovery route. **Don't** hand-edit
   sudoers for this — that's the M14 lesson's cautionary tale.

## Accessibility & low-spec provisions

- **No 4 GiB free?** Path B (WSL2) runs comfortably in 2 GiB with the
  default distro — the course's memory guidance is in `SETUP.md` §0.
- **Managed laptop, can't install anything?** Path D in `SETUP.md`
  (lab machines / cloud options) — coordinate *before* Week 1, not
  during it.
- **Screen-reader users:** the course's terminal-first design is an
  advantage, not a barrier — every lesson's content is plain text.
  The one concession worth making proactively: increase VM console
  font size *and* teach `Ctrl+Shift+=` in GNOME Terminal on day one.

## The end-of-week gate

By end of Week 1 every student can, from their own sandbox:

```console
$ whoami && pwd && lsb_release -d && python3 --version
```

…and state aloud which path they're on (A/B/C/D). That sentence is the
prerequisite for everything in Unit 2; students who can't say it get
a 15-minute slot in the first office hours — the setup debt compounds
otherwise.
