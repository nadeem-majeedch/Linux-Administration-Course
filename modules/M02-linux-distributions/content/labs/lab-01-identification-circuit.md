# Lab 1 — The Identification Circuit

> Module 02 · Unit 1 · Difficulty: Beginner · Est. time: 30 min
> Environment: your own Linux (VM recommended) — plus optionally two
> throwaway containers if you have Docker from M28.
> ⚠️ All commands are read-only. Nothing here changes your system.

## Objective

By the end you can determine *what distribution a machine actually
runs* from evidence on the machine itself — the first question of
every incident, install, and compatibility discussion.

## Part A — Your own machine (10 min)

Run the circuit, writing down each answer before the next command:

```console
$ cat /etc/os-release | head -4
$ uname -m && uname -r
$ uptime -p
```

1. **Identity:** what distro + version? Which field told you the
   *family*?
2. **Kernel:** what series is running, and is it different from what
   the distro release implies?
3. **Uptime:** how long has this machine been up — i.e., how long
   since its last reboot/kernel change?

Write one **speakable sentence**: *"This machine is …"*

## Part B — The family interview (10 min)

Using only files on disk (no web):

```console
$ command -v apt dnf pacman apk zypper 2>/dev/null
$ ldd --version | head -1
$ ls /etc/ | grep -iE 'release|debian|redhat|arch' 
```

- Which package manager(s) exist? Which would you *use*?
- Which libc? (glibc vs musl changes what prebuilt binaries run.)
- Do any family-marker files (`/etc/debian_version`, `/etc/redhat-release`)
  exist?

## Part C — Optional: the container zoo (10 min, needs Docker)

Compare two official-library bases, pinned like you were taught
(`debian:12.11`, `alpine:3.20` — or any two pinned tags of official
images):

```console
$ docker run --rm debian:12.11  sh -c 'cat /etc/os-release | head -2; command -v apt apk; uname -m'
$ docker run --rm alpine:3.20   sh -c 'cat /etc/os-release | head -2; command -v apt apk; uname -m'
```

Record the differences that would *matter*: package manager, libc
(see `ldd` inside — does alpine even have glibc?), default shell.

## Deliverable

A short `identity-report.md`: the Part A sentence, the Part B table,
and (if done) Part C's table. Close with: **why two commands, not
one** (what does `os-release` know that `uname` doesn't, and
vice-versa?).

## Troubleshooting

- `cat: /etc/os-release: No such file or directory` — old or
  minimal system: try `cat /etc/*release* /etc/issue` and note that
  support for the standardized file is itself a compatibility fact.
- `command -v` prints nothing for a manager — that manager isn't
  installed; that *is* evidence, record it as "absent".
