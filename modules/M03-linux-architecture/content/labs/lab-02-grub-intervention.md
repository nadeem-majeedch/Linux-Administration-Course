# Lab 2 — Interrupt the Boot on Purpose

> Module 03 · Unit 1 · Difficulty: Intermediate · Est. time: 25 min
> Environment: **your own Ubuntu VM** (needs a real GRUB menu). WSL2
> has no bootloader — do the reading-only §1 and skip to §4.
> ⚠️ Everything here is *one-boot-only* and reverts on the next boot.
> You will not edit any file. Worst case: reboot again.

## 1. Watch the menu (5 min)

Reboot the VM; hold **Shift** (BIOS) or tap **Esc** (UEFI) as it
starts. Confirm you can see the GRUB menu, then let it boot normally.

If the menu never shows (timeout = 0), boot once, run
`grep -E 'timeout|hidden' /boot/grub/grub.cfg` to see the setting, and
practice patience: the keystroke must land *during* the window. Do
**not** edit the config to lengthen it — finding the window is the
skill.

## 2. Read the stage directions (5 min)

At the menu, highlight the default entry and press **`e`**. You are
now looking at the one-boot editor. Find the line beginning `linux`:

```
linux /boot/vmlinuz-6.8.0-45-generic root=UUID=xxxx ro quiet splash
```

Record it, then press **Esc** to discard (do **not** Ctrl-x yet).

## 3. The one-boot override (10 min)

Press `e` again and, at the end of the `linux` line, add:

```
systemd.unit=rescue.target
```

Press **Ctrl-x** to boot. You should land in *rescue mode*: a
single-user shell, root prompt, no network target started.

Evidence collection at the rescue prompt:

```console
# runlevel ; systemctl list-units --state=running | head
# cat /proc/cmdline          # your edit is on record
# systemctl get-default      # what WOULD it boot normally?
```

Then: `systemctl reboot` — and note that the machine boots normally
again. **Your edit lived exactly one boot.**

## 4. Interpretation (5 min, WSL2 students start here)

Answer in your log:

1. Which *act* did `systemd.unit=rescue.target` override, and why did
   the change not persist?
2. Why is rescue mode useful for "forgot my password" — and what does
   that imply about **physical access and disk encryption**? (One
   sentence; M15/M25 revisit the trust model.)
3. `systemctl get-default` shows `graphical.target` (or
   `multi-user.target` on servers). In one sentence: what would change
   about Act 4 if you changed the default?

## Deliverable

Log entries: the recorded `linux` line, the rescue-boot `/proc/cmdline`
proving the override, the `list-units` head (what runs in rescue vs
normal), and the three interpretation answers.

## Troubleshooting

- Missed the menu window: GRUB's timeout may be 0; watch for the
  "GNU GRUB" flash and retry — keystrokes during the window always win.
- Rescue boot wants a root password: if your VM uses the sudo-model
  (no root password), use `systemd.unit=emergency.target` instead —
  same idea, still one boot.
- Stuck in rescue after reboot: you edited `/boot/grub/grub.cfg`
  (don't) — or you're looking at a hung job; `systemctl reboot` from
  the rescue prompt, or reset the VM.
