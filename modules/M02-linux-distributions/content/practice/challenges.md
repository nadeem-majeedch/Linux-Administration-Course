# Challenge Exercises — M02

> C1/C2 can be done on **any** Linux machine (or a container).
> C3/C4 use the network only for *reading documentation*.
> C5 is a design task — no VM required.

## C1 — The four-flavor identification circuit

Run against the container bases you already trust, nothing else
(pulling a new one is optional; **official-library images only**, never
`latest`):

```console
$ docker run --rm debian:12.11            sh -c 'cat /etc/os-release | head -3; command -v apt dnf pacman apk; uname -m'
$ docker run --rm fedora:42               sh -c '…same…'
$ docker run --rm alpine:3.20             sh -c '…same…'
$ docker run --rm archlinux:base-2025.05.01  sh -c '…same…'
```

Deliver a **table**: image · libc hint (`ldd --version | head -1`) ·
package manager · init you'd expect · architecture. Close with a
three-sentence answer: *if you had to run one old vendor binary +
one current Python stack on the same host, which two flavors and
why?*

## C2 — The support-window census

For the three distros in C1 **plus your Ubuntu VM**: find each
project's official release/EOL statement (web search to the
*project's own* pages only) and record: current release number,
release date, standard-support end, extended/LTS end. Then write the
**one operational sentence per row** for a data platform: what you may
and may not do after the end date (hint: M16's repo-freeze rule
interacts with the answer).

## C3 — Family tree cross-examination

From `/etc/os-release` on your VM, answer — *without* a web search
first, then verify against the Ubuntu/Debian official pages:

1. Which Debian release is your Ubuntu version based on, and how did
   the field `ID_LIKE` tell you before you searched?
2. Does that Debian release still receive security updates *today*?
3. Name one consequence for the **base image policy** you'd write for
   your own containers.

## C4 — Distro-detection one-liner contest

Write a **single pipeline** that prints a one-line identity sentence,
e.g. `Debian-family (ubuntu 24.04) on x86_64, kernel 6.8.0-45-generic`
for your VM — and *something sensible* (not a crash) on a
non-Debian container you can `docker run --rm`. Hint: two `command -v`
probes can make the sentence conditional. You have M07's toolkit.
Grade: correctness on ≥2 distro families, and zero output if run as
root with a broken PATH? No — grade: still works if `/etc/os-release`
is missing (what's your fallback, and why is `uname` never enough?).

## C5 — The registry of trust (design, no terminal)

Your DS team builds images weekly. Write a **one-page policy** (your
own words, no template) answering:

1. Which base images are allowed, and *how referenced* (tag policy vs
   digest policy — name the trade-off M02 vs M28 taught).
2. Where checksum verification happens in the workflow, and for which
   artifacts (ISO? base image? dataset? who signs *your* exports?).
3. What the "unsupported base" finding means operationally — the
   action list, in order.
4. One paragraph: the GPG trust argument in plain language a manager
   could follow (why "the checksum matched" is not the security
   control).

Hand in: the policy + one paragraph naming which **module's evidence
habit** each section reuses.
