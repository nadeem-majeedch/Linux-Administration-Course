# M09 — Pipes, Redirection & Filters: content guide

> The stream model — the idea that made Unix win. Everything after
> this module assumes you can wire programs together.

**Lessons**

| # | Lesson | You will be able to |
|---|--------|---------------------|
| 1 | [01-stdin-stdout-stderr-redirection.md](lessons/01-stdin-stdout-stderr-redirection.md) | Redirect the three streams precisely, including `2>&1`, `tee`, and the `/dev/null` idiom |
| 2 | [02-pipes-chaining-substitution.md](lessons/02-pipes-chaining-substitution.md) | Build multi-stage pipelines, chain with `&&`/`||`/`;`, and use command substitution |

**Labs** — [labs/README.md](labs/README.md): log wrangling ·
pipeline workshop.

**Practice** — [practice/quiz.md](practice/quiz.md) (+ key),
[challenges.md](practice/challenges.md) (6 challenges).

## Learning objectives

By the end of this module you can:

1. **Explain** the stream model: every process opens stdin (0),
   stdout (1), stderr (2); redirection rewires the *file
   descriptors*, not the program.
2. **Redirect** precisely: `>`, `>>`, `<`, `2>`, `2>&1`, `&>`,
   `tee` for tees-in-the-stream, `/dev/null` as the discard device —
   and predict where every byte goes in a compound redirection.
3. **Compose** pipelines that process data larger than RAM: the
   stages stream, memory stays constant, and intermediate files
   never exist.
4. **Chain** commands with `;`, `&&`, `||` — and state the exit-
   status semantics each one tests.
5. **Substitute** command output into command lines
   (`$(...)`), including the nesting and quoting rules.
6. **Debug** pipelines stage-by-stage (run each segment, inspect
   counts) — the method every later module's one-liners assume.

## Command-line skills

`>` `>>` `<` `2>` `2>&1` `&>` · `|` · `tee` (`-a`) · `/dev/null` ·
`&&` `||` `;` · `$(...)` · `xargs` (bridge to M08 §4) · pipeline
inspection habits (`wc -l` between stages, `head`/`tail` probes).

## Prerequisite map

M08's filters (`grep`, `sort`, `cut`, `awk`, `sed`) are the *cars*;
this module is the *track*. Downstream: M10/M11 scripts are
pipelines with memory; M24's log analysis and M08's DS pipelines
are this module's daily form; M21's `curl | jq`-style inspection and
M29's log pipelines are the same skill aimed at services.
