# M23 — File Transfer & Synchronization

> **Unit 6 · Services, Networking & Security** · Difficulty: Intermediate
> [Content index](content/README.md) · [Labs](content/labs/README.md) · [Quiz](content/practice/quiz.md) · [Challenges](content/practice/challenges.md)
> Companion to [M22 — SSH & Remote Administration](../M22-ssh-remote-admin/content/README.md)

## Summary

Moving data between machines — laptops to lab servers, servers to
storage, datasets in and results out — is a daily Data Science
operation with real failure modes: silent overwrites, interrupted
transfers, ambiguous deletions, and unprovable "it got there"
claims. This module teaches the three-tool transfer toolbox (`scp`,
`sftp`, `rsync`), rsync's comparison and deletion semantics, and the
verification habits (dry-run gates, sha256 manifests, transfer
logs) that make transfers auditable rather than assumed.

## Objectives, labs, assessment

Full objectives and the module map live in
[content/README.md](content/README.md). Labs are loopback-only
(inside your own VM); the quiz key is instructor-held
([quiz-answers.md](content/practice/quiz-answers.md)).

## Roadmap entry

See [COURSE-ROADMAP.md](../../COURSE-ROADMAP.md), Unit 6 —
M23 File Transfer & Synchronization (prerequisites: M10, M19, M22).
