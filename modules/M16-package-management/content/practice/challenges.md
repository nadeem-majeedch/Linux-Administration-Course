# Challenge Problems — Module 16

After the quiz; record in `lab-log.md`. Disposable VM/WSL2 only for
anything state-changing.

- [ ] **C1 — the file detective.** Find which package owns `/bin/df`,
  `/etc/hosts` (careful — this one's interesting!), and `/usr/share/man/
  man1/grep.1.gz`. One of these isn't owned by a *normal* package —
  explain which and why (dpkg-conffile vs generated file).
- [ ] **C2 — the version pin.** `apt install pkg=VERSION` pins a version.
  Simulate (`--dry-run`) installing a *specific older version* of a
  package on your VM. What does apt say? Explain why pinning old
  versions long-term is a security anti-pattern.
- [ ] **C3 — the hold audit.** `apt-mark showhold` on your VM. If empty:
  hold one package (`sudo apt-mark hold tree`), attempt a dry-run
  upgrade, observe, then `unhold`. Write the 3-sentence "what are holds
  for and why are they dangerous left on security packages" summary.
- [ ] **C4 — dependency archeology.** `apt show libreoffice-core | grep
  Depends | tr ',' '\n' | wc -l` — count the deps. Now find the
  *smallest* installed package by dependency count you can
  (`apt show tree`, `jq`, `sl`). Two paragraphs: what makes a package's
  dependency surface big vs small, and the DS-relevant lesson about
  library design.
- [ ] **C5 — the mirror speed run.** Identify your current mirror
  (`grep -r deb /etc/apt/sources.list | head -1`), then time
  `sudo apt update` against archive.ubuntu.com vs a regional mirror
  (edit sources in the disposable VM only). Report both timings and
  whether the mirror choice was worth it — then revert if changed.
- [ ] **C6 — the broken repo simulation.** Add a sources line pointing
  at a nonexistent URL (`/etc/apt/sources.list.d/broken.sources`),
  `apt update`, capture the error, then remove the file and verify
  clean. Decode each error line — what *kind* of failure was it (network
  vs signature vs metadata)?
- [ ] **C7 — RPM field trip.** On the translation table in Lesson 3 §2,
  add three rows we didn't list (e.g., "which package owns this file",
  "repo file location", "changelog of a package"). Verify your answers
  with any dnf documentation — cite the man page or docs URL you used.
- [ ] **C8 — the toolchain decision memo.** Your project needs:
  python 3.12 (system has 3.12), pandas 2.3, psycopg2, CUDA toolkit 12.4,
  and git. For each: apt or pip/conda or either — with one justification
  sentence. Format as a memo your future sysadmin-self would approve.

C6 in the wild: dead third-party repos are the #1 cause of
"`apt update` is scary red" on student machines; rehearsing the diagnosis
in a VM makes the real event boring.
