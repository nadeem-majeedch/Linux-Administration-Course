# Website & Publication (MkDocs + GitHub Pages)

This repository publishes its course content as a static website via
**MkDocs** with the **Material for MkDocs** theme, built and deployed by
[`.github/workflows/publish.yml`](https://github.com/nadeem-majeedch/Linux-Administration-Course/blob/main/.github/workflows/publish.yml) on every
push to `main`.

## Why MkDocs (and not something heavier)

| Criterion | Why MkDocs wins for this course |
|---|---|
| Content stays plain Markdown | The repository is the source of truth. Files are **copied verbatim** into the site — nothing is converted, so GitHub, editors, and the website all render the same files. |
| Minimal footprint | One YAML config (`mkdocs.yml`), one pinned `requirements-docs.txt`. No Node toolchain, no framework lock-in, no external services. |
| University-friendly | Built-in full-text search, mobile-responsive layout, accessible navigation, per-page edit links — zero custom JavaScript to maintain. |
| Relative links survive | MkDocs reads the same relative links already used across the repo; `strict` + `validation` settings make any broken link a **build failure**, so it can never be published. |
| Reproducible CI | `pip install` of two pinned packages; build fails loudly on warnings (`mkdocs build --strict`). |

A university course needs a site that a teaching assistant can maintain after
the original authors leave. MkDocs is that: two files of configuration and a
shell script, all reviewable in a normal pull request.

## How the site is generated

`scripts/build-site.sh` prepares the docs tree (`site-src/`, gitignored):

1. Copies the content trees **byte-for-byte**: `modules/`, `projects/`,
   `assessments/`, `datasets/`, `resources/`, `cheatsheets/`, `labs/`.
   Because the directory layout is preserved exactly, every existing
   repository-relative link keeps working on the website.
2. For every directory with a `README.md`, writes a sibling `index.md` that
   *includes* the README (`--8<--` snippet). MkDocs serves `directory/` from
   `directory/index.md`, so nav URLs are clean (`…/M10-bash-scripting/`) while
   relative links written *from* the README resolve identically.
3. Copies root pages (`README.md → index.md`, plus `SETUP.md`,
   `COURSE-ROADMAP.md`, `CONTRIBUTING.md`, `WEBSITE.md` under their original
   names, because module pages link up to them relatively).
4. Writes the few generated landing pages (About This Website, Progressive
   Labs index, Cheatsheets index).

`mkdocs build --strict` then renders the site into `site/` (gitignored).

## Local preview (students & maintainers)

From the repository root:

```bash
python -m venv .docs-venv
source .docs-venv/bin/activate        # Windows: .docs-venv\Scripts\activate
pip install -r requirements-docs.txt
bash scripts/build-site.sh
mkdocs serve
```

Then open the printed URL (default `http://127.0.0.1:8000/`) in a browser.
`mkdocs serve` live-reloads on save. To produce the final static site:

```bash
mkdocs build --strict --clean     # output in site/ — open site/index.html
```

Nothing in these steps needs administrator rights, and nothing writes outside
the repository directory (`.docs-venv/`, `site-src/`, `site/` are gitignored).

## How GitHub Pages deployment works

1. A push to `main` (or a manual *Run workflow* on the Actions tab) triggers
   `.github/workflows/publish.yml`.
2. **Build job** — checks out the repo, installs the pinned toolchain, runs
   `scripts/build-site.sh`, then `mkdocs build --strict --clean`. Any broken
   internal link or missing nav entry fails the job with the offending file
   named in the log. The rendered `site/` is uploaded as a Pages artifact.
3. **Deploy job** — `actions/deploy-pages` publishes the artifact.
4. The site appears at
   `https://nadeem-majeedch.github.io/Linux-Administration-Course/`.

**One-time repository setting:** Settings → Pages → *Build and deployment* →
Source: **GitHub Actions**. Until then the deploy step fails with an
explanatory message.

Security posture of the workflow:

- Top-level `permissions: contents: read` — jobs inherit no write access.
- Only the deploy job elevates, to exactly `pages: write` + `id-token: write`
  (OIDC; no long-lived PAT is involved anywhere).
- No credentials persist past checkout (`persist-credentials: false`).
- All actions are the official `actions/*` images, pinned to current major
  versions (checkout v7, setup-python v7, configure-pages v6,
  upload-pages-artifact v5, deploy-pages v5).
- `concurrency` cancels superseded deployments instead of queuing them.

## Conventions for contributors

- Write content with normal repository-relative links; the build validates
  them. Do not link with `localhost` URLs, absolute GitHub URLs, or `file://`.
- New top-level pages must be copied in `scripts/build-site.sh` and added to
  `nav` in `mkdocs.yml` — the strict build fails if one is missing.
- New module directories are picked up automatically by the copy step, but add
  their entry to `nav` so students can navigate to them.
- The nav order mirrors the curriculum units in `COURSE-ROADMAP.md`; keep them
  in sync.
