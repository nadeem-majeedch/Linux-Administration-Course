# Lesson 3 — Beyond apt: Source Builds, RPM Systems & the DS Toolchain

> Module 16 · Unit 5 · Difficulty: Intermediate
> Reading time: ~35 min · Lab: none (walkthrough is optional; Lab 2
> covers the safe lifecycle) · Prerequisites: Lessons 1–2

> 🔒 Safety: the source-build walkthrough compiles a tiny, harmless tool
> *into your home directory* — no sudo anywhere in it, nothing installed
> system-wide, trivially removed with `rm -r`.

---

## 1. Compiling from source — the concept

Some software exists only as source (research code, niche tools, a fix
not yet packaged). Compiling means translating source → binary on *your*
machine — you trade apt's automation for exactness and currency. The
canonical loop (GNU build convention):

```console
$ ./configure      # probe: compiler present? libraries present? write Makefile
$ make             # compile
$ sudo make install  # copy into system paths (the ONLY root step)
```

Why each step exists: `configure` fails *early and loudly* if you're
missing a dependency — its error (`configure: error: ... required`)
names what to apt-install. `make` honors parallelism (`make -j$(nproc)`).
`make install` places files in the **prefix** (default `/usr/local` —
FHS's designated home for *locally built* software, so it never collides
with apt's `/usr`).

### The cost ledger (why the course says: apt first, source rarely)

- ❌ You now own updates: no `apt upgrade` for this software, ever.
- ❌ You own dependency hunting by hand.
- ❌ dpkg doesn't know it exists → `dpkg -S` can't find its files,
  removal is manual, conflicts are invisible until they hurt.
- ✅ You get exact versions, custom flags, and software no repository has.

**The middle path — checkinstall:** `sudo checkinstall` (after make)
instead of `make install` builds a proper .deb from the install step, so
dpkg can track and remove it. Useful when a source build is unavoidable;
still your maintenance burden for updates.

**Prefix hygiene:** `./configure --prefix=$HOME/.local` keeps everything
under your home — the walkthrough below uses exactly this, making the
whole operation sudo-free and self-contained.

### Walkthrough — a real, tiny, disposable build

```console
$ sudo apt install build-essential    # compiler toolchain (the one root step)
$ mkdir -p ~/src && cd ~/src
# hello from GNU — classic first build:
$ curl -LO https://ftp.gnu.org/gnu/hello/hello-2.12.2.tar.gz
$ tar xf hello-2.12.2.tar.gz && cd hello-2.12.2
$ ./configure --prefix=$HOME/.local
$ make -j$(nproc)
$ make install                        # no sudo: prefix is in your home
$ ~/.local/bin/hello
Hello, world!
```

Removal: `rm -r ~/src/hello-2.12.2 ~/.local/bin/hello` — complete, and
your system package database never noticed. That's the *deal* source
builds offer.

### DS framing

You'll meet source builds as **pip building a wheel from source** — same
mechanics (compiler + headers) behind `pip install` errors like
`Unable to find vcvarsall/gcc`. The apt equivalent of "install the dev
headers": `sudo apt install python3-dev build-essential libpq-dev` — the
incantation that un-breaks most source builds, and precisely why Lesson
1's `dpkg -S` skill ("which package owns this header?") pays rent.

---

## 2. DEB vs RPM — the conceptual map

Ubuntu/Debian use `.deb` + `apt`/`dpkg`; Red Hat family (RHEL, Fedora,
CentOS/Rocky/Alma, openSUSE's `.rpm` variant) use `.rpm` + `yum`/`dnf`
/`zypper`. **The concepts are identical; the nouns differ** — learn the
translation table once and you can administer either family on sight:

| Concept | Debian/Ubuntu | RPM family (RHEL/Fedora) |
|---|---|---|
| package file | `.deb` | `.rpm` |
| low-level tool | `dpkg` | `rpm` |
| high-level tool | `apt` | `yum` → modern `dnf` |
| refresh metadata | `apt update` | `dnf makecache` (often automatic) |
| install | `apt install pkg` | `dnf install pkg` |
| search | `apt search`, `apt show` | `dnf search`, `dnf info` |
| what owns this file? | `dpkg -S /path` | `rpm -qf /path` |
| inventory | `dpkg -l` | `rpm -qa`, `dnf list installed` |
| file list of a pkg | `dpkg -L pkg` | `rpm -ql pkg` |
| package info | `dpkg -s pkg` | `rpm -qi pkg` |
| local file install | `apt install ./f.deb` | `dnf install ./f.rpm` |
| repo config | `/etc/apt/sources.list(.d/)` | `/etc/yum.repos.d/*.repo` |
| third-party repos | PPAs | COPR, EPEL |
| security updates | `unattended-upgrades` | `dnf-automatic` |

Concepts that transfer 1:1: signed metadata, dependency resolution,
main/universe ↔ base/EPEL-ish support tiers, "query before install,"
`remove` vs `purge` (RPM: `dnf remove` keeps nothing config-wise by
default — verify per package), autoremove (`dnf autoremove`).

Concepts that *don't* transfer: version-suffix conventions (`1:2.3-4`
epoch:version-release is dpkg's; RPM's is version-release-dist), and
package *names* differ (`libssl3` vs `openssl-libs`). When reading a
tutorial, translate the *operation*, never copy the *command*.

**For this course:** Ubuntu is the practice ground; the table is your
passport. University clusters often run RHEL-family — expect to read
`dnf` in their onboarding docs, and now you will understand every line.

---

## 3. The DS toolchain: who owns what

The recurring architecture question: apt, pip, conda — who installs what?
The durable answer, then the details:

> **apt owns the OS and system libraries; language-level managers
> (pip/conda) own language packages, inside environments. Never let them
> fight over the same files.**

```console
$ sudo apt install python3 python3-venv python3-pip    # interpreter + venv + pip
$ sudo apt install git                                  # version control
$ python3 -m venv ~/venvs/ds                            # your isolated env
$ source ~/venvs/ds/bin/activate
$ pip install jupyterlab pandas scikit-learn            # INSIDE the env
```

**Why the split (each rule earned in production pain):**

- **pip's system-wide `--break-system-packages` era:** newer Ubuntu
  (23.04+/24.04) marks the system python as *externally managed* — pip
  refuses global installs because apt-owned files live there too; a
  pip/upgrade race can break OS tools (apt itself, unattended-upgrades).
  Venvs sidestep the whole question: your env, your files, zero system
  risk. (Full treatment: [M27](../../../M27-python-jupyter-data/README.md).)
- **apt for:** interpreters, compilers, dev headers, system libs
  (`libpq-dev`, `libxml2-dev`), Jupyter *when you want it system-wide and
  apt-managed* (`sudo apt install jupyter`), CUDA/NVIDIA *driver*
  packages.
- **pip/conda for:** every version-sensitive library (pandas, torch,
  numpy) — pinned per project, reproducible, disposable.
- **Git:** one `sudo apt install git` for the OS tool; per-repo config
  (`git config --global user.name`) lives in your home. [M26](../../../M26-git-dev-workflows/README.md)
  owns Git itself.

**Version reality check:** apt's pandas will be a frozen, older, *very
stable* version; pip's is current. Research code needing `pandas>=2.2`
belongs in a venv, full stop. Conversely, build-essential via pip is
impossible — compilers are OS citizens.

### Docker preview (M28)

`apt` inside a container gets one job per layer (`apt install --no-
install-recommends` for slimness, `rm -rf /var/lib/apt/lists/*` in the
same layer) — the check-first habits from Lesson 1 §4 are exactly what
keeps images small and reproducible.

---

## Exercises (lab-log.md)

1. Predict what's missing, then verify: `pip install psycopg2` (in a
   venv) fails with a pg_config error. Which apt package fixes it, and
   how does this connect to `dpkg -S`?
2. Translate to dnf: `apt update && apt install htop`; `dpkg -L htop`;
   `dpkg -S /usr/bin/htop`. Four commands, table §2, no cheating.
3. Why does `./configure --prefix=$HOME/.local` eliminate the sudo step?
   What FHS principle is this leaning on? ([M06](../../../M06-filesystem-hierarchy/content/lessons/03-filesystem-hierarchy-tour.md))
4. Your teammate runs `sudo pip install numpy` system-wide "because venvs
   are fiddly." Write the three-sentence reply citing what breaks on
   modern Ubuntu (externally-managed) and what to do instead.
5. When *is* a source build the right call? Give one concrete DS-flavored
   scenario where apt and pip both lose.
6. Component mapping: for `main / restricted / universe / multiverse`,
   name the RPM-world analog *concept* (not exact name) — one sentence
   each. Where does EPEL sit on this spectrum?

## Check yourself before the labs

- [ ] I can run the configure/make/install loop and explain each step.
- [ ] I know why prefix-in-home = no sudo = trivial removal.
- [ ] I can translate apt↔dnf operations fluently.
- [ ] I can state the apt/pip/conda division and defend it.

## Further reading (official sources)

- GNU build system (configure/make): https://www.gnu.org/software/make/manual/
- `man checkinstall`; `man dnf` (dnf docs: https://docs.pagure.org/dnf/)
- Debian Python packaging policy / PEP 668 (externally-managed):
  https://peps.python.org/pep-0668/
- Ubuntu Server Docs — package management: https://ubuntu.com/server/docs
