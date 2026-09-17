#!/usr/bin/env bash
# build-site.sh — generate the MkDocs sources (site-src/) from repository content.
#
# WHAT: copies the course's markdown into site-src/ under stable, student-facing
#       paths and writes the few generated landing pages. No content is edited —
#       files are copied byte-for-byte, so repository-relative links keep working
#       because the directory structure is preserved 1:1.
#
# WHY README-as-index: MkDocs natively maps a directory's README.md to that
# directory's index page, so modules get clean URLs (…/M10-bash-scripting/)
# and every file is published byte-for-byte — nothing is generated or
# rewritten. Links between pages therefore resolve exactly as they do on
# GitHub. (An earlier design generated an index.md beside each README; it
# collided with this native mapping and was removed.)
#
# OUTPUT (site-src/, consumed by mkdocs.yml):
#   modules/M*/**  projects/**  assessments/**  datasets/**  resources/**
#   cheatsheets/**  labs/**
#   README.md  SETUP.md  COURSE-ROADMAP.md  CONTRIBUTING.md  WEBSITE.md
#   site.md
#
# RUN: bash scripts/build-site.sh   (from the repository root)
set -euo pipefail
cd "$(dirname "$0")/.."

DST="site-src"

echo ">> cleaning $DST"
rm -rf "$DST"
mkdir -p "$DST"

echo ">> copying course content (byte-for-byte)"
# 1:1 trees — every relative link inside these keeps working. MkDocs maps
# each directory's README.md to the directory index (clean URLs, no rewriting).
cp -r modules projects assessments datasets resources cheatsheets labs accreditation "$DST/"

echo ">> root pages"
# Copied under their ORIGINAL names: module pages link up to them via relative
# paths like ../../CONTRIBUTING.md, which must keep resolving. README.md at
# the docs root becomes the site homepage (MkDocs native README-as-index).
cp README.md SETUP.md COURSE-ROADMAP.md CONTRIBUTING.md "$DST/"
cp QA-REPORT.md FINAL-AUDIT.md "$DST/" 2>/dev/null || true
# WEBSITE.md is also copied so the site.md link resolves on the site.
cp WEBSITE.md "$DST/WEBSITE.md"

echo ">> generated landing pages"
cat > "$DST/site.md" <<'EOF'
# About This Website

This site is **generated from the course repository** — the Markdown you are
reading lives in the [GitHub repository](https://github.com/nadeem-majeedch/Linux-Administration-Course)
and is published automatically by GitHub Actions on every push to `main`.

## How it is built

| Aspect | Choice |
|---|---|
| Generator | [MkDocs](https://www.mkdocs.org/) — plain Markdown in, static site out |
| Theme | [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) |
| Source of truth | The repository files themselves (copied verbatim at build time) |
| Deployment | GitHub Actions → GitHub Pages (`.github/workflows/publish.yml`) |
| Build guarantee | The build runs in **strict mode**: a broken internal link fails publication |

Nothing is converted or rewritten: every lesson, lab, quiz, and cheatsheet is
the same file you see in the repository, which is why relative links between
pages work both on GitHub and on this site.

## For maintainers

- Site configuration: [`mkdocs.yml`](https://github.com/nadeem-majeedch/Linux-Administration-Course/blob/main/mkdocs.yml)
- Source generator: [`scripts/build-site.sh`](https://github.com/nadeem-majeedch/Linux-Administration-Course/blob/main/scripts/build-site.sh)
- Publication workflow: [`.github/workflows/publish.yml`](https://github.com/nadeem-majeedch/Linux-Administration-Course/blob/main/.github/workflows/publish.yml)
- Local preview and rationale: [WEBSITE.md](WEBSITE.md) in the repository.
EOF

# (labs/ and cheatsheets/ ship their own README.md, which MkDocs serves as
# the directory index — no generated landing pages needed.)

echo ">> done: $(find "$DST" -name '*.md' | wc -l) markdown files in $DST"
