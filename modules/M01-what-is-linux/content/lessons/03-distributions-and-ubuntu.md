# Lesson 3 — Distributions & Ubuntu

> Module 01 · Unit 1 · Difficulty: Beginner
> Reading time: ~20 min · Lab: none · Up next: [Lesson 4](04-linux-architecture.md)

---

## 1. What a distribution actually is

A **Linux distribution** ("distro") is a complete, packaged operating system built
around the Linux kernel. The kernel alone cannot boot a usable computer; a
distribution assembles everything you need and keeps it updated:

| Ingredient | What it is | Example |
|---|---|---|
| **Linux kernel** | The core, patched and configured by the distro | kernel 6.8 |
| **Userland** | Shell, core utilities, libraries (much of it GNU) | GNU coreutils, bash |
| **Installer** | The program that puts the OS on a disk | Ubiquity/Subiquity |
| **Package manager + repositories** | The software catalog and its updater | `apt` + Ubuntu archives |
| **Desktop environment** (optional) | The GUI: panels, file manager, settings | GNOME |
| **Release policy & support** | When versions ship, how long they're fixed | Ubuntu: LTS + interim |
| **Branding & defaults** | Wallpapers, chosen apps, sane defaults | Ubuntu's choices |

That last row is not a joke: a distro's *decisions* — which versions to freeze,
which defaults to pick, how long to patch — are most of its value.

## 2. The family tree

Distributions are families, because anyone with the source can fork a distro and
build their own:

```
                    ┌── Debian ──► Ubuntu ──► Linux Mint, Pop!_OS, Kubuntu…
                    │      │
                    │      └──► Raspberry Pi OS
                    │
   Slackware ───────┤
                    │
                    └── Red Hat Linux ──► Fedora ──► RHEL ──► CentOS Stream,
                                                  │          Rocky, AlmaLinux
                    Arch ──► Manjaro, EndeavourOS  │
                    SUSE ──► openSUSE, SLES        └──► Amazon Linux
                    (independent lines)
```

| Family | Package format | Package manager | Release style | You'll meet it in |
|---|---|---|---|---|
| **Debian** | .deb | `apt` / `dpkg` | Stable, tested slowly | Ubuntu's parent |
| **Ubuntu** | .deb | `apt` | LTS every 2 years + interim every 6 months | **This course** |
| **Fedora / RHEL** | .rpm | `dnf` | Fedora: fast; RHEL: enterprise | Many university clusters |
| **SUSE** | .rpm | `zypper` | Enterprise + rolling option | Some HPC centers |
| **Arch** | pacman packages | `pacman` | Rolling (always latest) | Enthusiast laptops |

**The course's rule of thumb:** learn the *concepts* once — they are family-portable.
Learn the *commands* per family: `apt install tree` on Ubuntu becomes `dnf install tree`
on RHEL-family machines. Module 16 gives you the full translation table; until then,
you can always identify which family a machine belongs to (Lab 1) and behave
accordingly.

## 3. Release models: why "LTS" is written everywhere

Distributions differ most in **when they ship and how long they support**:

- **Standard releases** (Ubuntu interim: every 6 months): newest software, supported
  9 months. Great for trying features; wrong for servers you must maintain for years.
- **LTS — Long Term Support** (Ubuntu: every 2 years, e.g. 24.04): older, hardened
  software versions, **5 years of security updates** (more with support add-ons).
  The default for servers, clouds, and universities.
- **Rolling releases** (Arch, openSUSE Tumbleweed): continuously updated, no versions
  to "upgrade between". Bleeding edge; needs more admin attention.

**Ubuntu LTS is this course's platform** because it is also *the profession's* platform:
cloud providers' default Linux images are LTS-based, GPU cluster nodes are LTS-based,
Docker images you will use in Module 28 build on LTS bases. Working on 24.04 LTS here
means working on what your employer will hand you.

## 4. Ubuntu: what it is, where it fits

**Ubuntu** is a Debian-based distribution published by Canonical, released every six
months, with LTS every two years (4.04, 8.04, … 24.04 — year. month). Its stated goal
has always been "Linux for human beings": sane defaults, big hardware support, a
one-click installer, and a giant community — which also means: when you search an
error message, most answers you find are Ubuntu answers.

Ubuntu editions you will encounter:

| Edition | What it is | Course use |
|---|---|---|
| **Desktop** | GUI included, installer geared to laptops | **Your VM** (friendlier first contact) |
| **Server** | No GUI by default; same package base | What most real servers run; M20+ examples use it |
| **Cloud images** | Prebuilt VM images for AWS/Azure/GCP/OpenStack | The M22+ "remote server" story |

Two Ubuntu-specific extras to recognize now, judge later:

- **Snap packages:** a distro-independent package format (sandboxed, self-updating).
  Useful sometimes, controversial often; `apt` remains the course default.
- **`sudo` by default:** the Ubuntu installer makes your normal user an administrator
  who *borrows* root power per command with `sudo` — no separate root password to
  misuse. Module 14 is devoted to doing this *well*.

## 5. Choosing (and defending) a distro — a DS decision, not a fashion one

Scenario answers you should be able to give after this lesson:

- **Personal learning laptop in a VM:** Ubuntu LTS Desktop — biggest community,
  matches the course.
- **University GPU cluster:** whatever it runs — usually RHEL-family or Ubuntu LTS;
  you adapt with user-space tools (M27), you don't get to reinstall.
- **A production model-serving server:** Ubuntu LTS or RHEL-family — long support
  windows; nobody wants to rebuild production every 9 months.
- **A 20-euro Raspberry Pi on a shelf as a mini data logger:** Raspberry Pi OS
  (Debian family) — same `apt` skills apply.

The skill being tested is not loyalty to a brand; it is *matching release policy,
support window, and package ecosystem to a workload* — the same reasoning you will
apply to pinning Python versions in Module 27.

## Exercises (lab-log.md)

1. List the seven "ingredients" of a distribution and mark which ones you have
   never consciously noticed before.
2. Explain to a classmate why a distribution is more than "Linux + apps". One
   paragraph, use the word *repository*.
3. Your cluster admin says: "We run Rocky Linux, not Ubuntu." Which family and
   package manager is that? Will your `apt install …` reflex work there?
4. Why do servers standardize on LTS releases while enthusiasts often run rolling?
   Two sentences, use the words *support window* and *stability*.
5. Name the Ubuntu edition for: (a) your course VM, (b) a cloud GPU instance,
   (c) a departmental web server.
6. A friend proposes installing Arch "because it's fastest". For a machine whose
   only job is to run a nightly training job unattended, what is the counter-argument?

## Check yourself before Lesson 4

- I can define *distribution* and name its ingredients.
- I can name the three big families and their package managers.
- I can explain LTS vs rolling and say why the course uses Ubuntu 24.04 LTS.
- Given a scenario, I can propose a distro and defend it.

## Further reading (official sources)

- Ubuntu release cycle — <https://ubuntu.com/about/release-cycle>
- Ubuntu Server documentation — <https://documentation.ubuntu.com/server/>
- Debian — <https://www.debian.org/>
- Fedora — <https://fedoraproject.org/>
- DistroWatch (browsing, not authority) — <https://distrowatch.com/>

Next: [Lesson 4 — Linux Architecture](04-linux-architecture.md)
