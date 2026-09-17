# Module 03 Troubleshooting — Architecture-Level Symptoms

> Six patterns where the *architecture* is the diagnosis. Each:
> symptom → layer location → evidence → fix class → prevention.
> Commands are read-only unless stated; fixes live in their owner
> modules (linked).

## 1. "command not found" for something you just installed

**Layer:** shell + `$PATH` (Lesson 4's actor 1–2).
**Evidence:** `type -a <cmd>`; `echo $PATH | tr ':' '\n'`.
**Cause classes:** installed to a non-PATH dir (e.g. `~/.local/bin`,
venv scripts) · PATH not refreshed in *this* shell · alias shadowing.
**Fix:** adjust PATH in the right dotfile (M15) or call by path —
don't `sudo ln -s` into `/usr/local/bin` reflexively.
**Prevention:** after any tool install, `type -a` it before scripting.

## 2. `error while loading shared libraries: libX.so.N: cannot open shared object file`

**Layer:** dynamic loader (actor 4).
**Evidence:** `ldd $(command -v <prog>) | grep 'not found'`;
`ldconfig -p | grep libX`.
**Causes:** library genuinely absent (install it — M16) · present in
a non-standard dir the loader doesn't scan · wrong soname version.
**Fix class:** install the proper package; `LD_LIBRARY_PATH` only as
a *diagnosis*, never a lifestyle (it shadows system libs per-process).
**Prevention:** prefer distro packages over hand-copied `.so` files.

## 3. Process stuck in `D` state, unkillable

**Layer:** kernel-side wait (Lesson 2).
**Evidence:** `ps -o pid,stat,wchan:32,cmd -p <PID>`; `journalctl -k -g <dev>`.
**Cause classes:** storage not answering (network mount dead, disk
error, lost iSCSI). **Fix class:** fix the underlying I/O (unmount,
restore the export) — the process frees when the syscall returns.
**Prevention:** soft-mount/time out network filesystems; monitor
`wa` (M24).

## 4. Boots to a target other than yours (or hangs at boot jobs)

**Layer:** Act 4 — init.
**Evidence:** `journalctl -b -p err`; `systemctl --failed`;
`systemctl get-default`.
**Causes:** default.target changed, a unit wedged, fsck pending.
**Fix class:** unit repair (M20); one-boot GRUB override
([Lab 2](labs/lab-02-grub-intervention.md)) to reach rescue.
**Prevention:** after any unit change, `systemctl reboot` *in the VM*
and check `journalctl -b -p err` — the boot is the test.

## 5. "Wrong Python" runs (env confusion, pre-M27 preview)

**Layer:** shell PATH + symlink chains (actors 1–2 + Lesson 4 §2).
**Evidence:** `type -a python3`; `readlink -f $(command -v python3)`;
`python3 -c 'import sys; print(sys.executable, sys.prefix)'`.
**Cause:** multiple interpreters, PATH order, venv not activated.
**Fix:** M27's venv discipline — but now you can *explain* it: the
shell resolves, the loader maps; both leave evidence.
**Prevention:** always `sys.executable` in diagnostics, never trust
the prompt.

## 6. The (deleted) library haunting

**Layer:** shared libraries (Lesson 4 §3).
**Symptom:** an updated service still reports the old version.
**Evidence:** `ls -l /proc/<pid>/exe` — note the ` (deleted)` suffix;
`systemctl show -p MainPID <unit>`.
**Cause:** process started before the package update; old inode held
open. **Fix class:** restart the unit (M20). **Prevention:** after
`apt upgrade`, review `needrestart`-class output — anything holding
old libs that faces the network deserves a restart.

---

**The M03 habit:** before reaching for fixes, spend one command
locating the *layer*. Every pattern above costs one evidence command
to localize — and the localization tells you which module's playbook
to open.
