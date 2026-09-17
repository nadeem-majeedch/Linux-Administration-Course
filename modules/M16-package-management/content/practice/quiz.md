# Module 16 Quiz — 20 Questions

Answer in `lab-log.md`; key: [quiz-answers.md](quiz-answers.md).

1. **R** Name the three layers (repository/apt/dpkg) and one job of each.
2. **R** What does `dpkg -S` do, and what's the apt-world equivalent of
   "which repo offers this package"?
3. **P** Decode `ii` in `dpkg -l` output — and name the status prefix
   meaning "removed but config remains."
4. **U** Why does `sudo dpkg -i foo.deb` fail for anything with
   dependencies, and what's the correct one-command fix?
5. **R** `apt update` vs `apt upgrade` — one sentence each, then: which
   error symptom means you skipped the first?
6. **P** `remove` vs `purge` vs `autoremove` — one sentence each, and
   which never touches `/home` data (all three? explain).
7. **U** In the check-first workflow, what does the summary line's
   "The following packages will be REMOVED" signal, and what's the
   required response?
8. **R** Before installing a library on a **production** server, your
   team rule is: preview every change to the package set first. Name
   the apt mode that resolves and reports without touching the
   system — and the one line of its output you must read before
   saying yes.
9. **U** Name the four Ubuntu components and their support character.
10. **DS** Why can `universe` matter for a data science VM specifically?
11. **R** What does apt verify before trusting a repository's index —
    and against what?
12. **U** Decode `W: GPG error ... NO_PUBKEY ABCD1234`: what happened,
    what it prevents, and what the *legitimate* fix path is?
13. **DS** Give the two strongest arguments against installing a
    cutting-edge ML library from a random PPA — one operational, one
    security.
14. **R** Which suite in sources.list exists *solely* for security
    patches, and what tool automates installing it?
15. **P** Write the translation table entries: `dpkg -S`, `apt install`,
    `apt autoremove` → their dnf equivalents.
16. **U** Why is `/usr/local` the default prefix for source builds, per
    FHS — and what conflict does this prevent?
17. **P** In the configure/make/install loop, which step needs root in
    the *default* flow, and how does `--prefix=$HOME/.local` remove that?
18. **DS** State the course's apt/pip/conda division in one sentence,
    then explain what PEP 668 ("externally managed") protects on Ubuntu
    24.04.
19. **DS** `pip install psycopg2` fails with "pg_config not found."
    Which kind of apt package is missing, and which Lesson-1 skill finds
    its name?
20. **R** Why is `apt install --dry-run` (and `--no-install-recommends`)
    the data scientist's two favorite apt flags? One sentence each.
