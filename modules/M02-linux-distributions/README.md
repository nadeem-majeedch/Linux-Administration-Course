# M02 — Linux Distributions

> Unit 1 · Foundations of Linux · Difficulty: Beginner
> Prerequisites: [M01](../M01-what-is-linux/README.md)
> Est. time: ~4 h (lessons ~90 min, labs ~60 min, practice ~90 min)

**Status: content complete.**

## Learning objectives

By the end of this module you can:

1. **Explain** the kernel-vs-distribution distinction and name the four
   components a distribution adds beyond the kernel.
2. **Differentiate** the major distro families (Debian, Red Hat, Arch,
   SUSE, Alpine, Arch-derived) by package manager, libc, and release
   model — and say why the differences matter operationally.
3. **Identify** any machine's distribution, version, family, and
   architecture from on-disk evidence (`/etc/os-release`, `uname`,
   `command -v`), without trusting hostnames.
4. **Reason** about release models (point vs rolling; LTS support
   windows) as *operational risk* for shared servers and reproducible
   pipelines.
5. **Verify** a downloaded artifact's integrity (SHA-256) and
   authenticity (GPG signature over a manifest), and explain what each
   step does and does not prove.

## What's inside

| Path | Contents |
|------|----------|
| [content/README.md](content/README.md) | Module guide + objectives + prerequisite links |
| [content/lessons/](content/lessons/) | 3 lessons: what a distribution is · identify your distro · checksums & signatures |
| [content/labs/](content/labs/) | 2 labs: identification circuit · verify a download |
| [content/practice/](content/practice/) | Quiz (+ key) · challenge exercises C1–C5 |
| [content/practice/challenges.md](content/practice/challenges.md) | Symptom → cause → fix challenges (C4–C5) |

## Definition of done

- [ ] Both labs completed with recorded evidence
- [ ] Quiz score ≥ 16/20; challenges C1–C3 attempted
- [ ] You can state any machine's identity in one sentence — and say
      which command proved each clause

## Module links

- Roadmap: [COURSE-ROADMAP.md](../../COURSE-ROADMAP.md#unit-1--foundations-of-linux-m01m04)
- Next: [M03](../M03-linux-architecture/README.md) · Cheatsheets:
  [resources/cheatsheets/](../../resources/cheatsheets/)
