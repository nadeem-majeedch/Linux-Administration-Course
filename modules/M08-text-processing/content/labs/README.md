# Module 08 Labs — Text Processing

> Three labs against the [module datasets](../data/README.md), then the
> graded mini-project. Labs 1 is read-only; Lab 3 works on **copies**
> (sed -i discipline); the mini-project writes only to `~/lab08/`.

| # | Lab | Focus | Time |
|---|-----|-------|------|
| 1 | [lab-01-data-quality-recon.md](lab-01-data-quality-recon.md) | Read-only recon: schema, scale, health of all 6 datasets | ~40 min |
| 2 | [lab-02-log-forensics.md](lab-02-log-forensics.md) | access.log + server.log incident analysis pipelines | ~45 min |
| 3 | [lab-03-column-clinic.md](lab-03-column-clinic.md) | transactions/students/sensor column work + sed/tr/awk cleaning | ~45 min |
| ★ | [mini-project-data-quality-toolkit.md](mini-project-data-quality-toolkit.md) | `dq.sh` — reusable data-quality CLI (deliverable + rubric) | ~2 h |

Standing rules (recap):

- Datasets live in `content/data/`; generate with
  `python3 data/generate_data.py` if absent — never edit generated files.
- Lab 3 copies first (`cp file file.work`); no in-place edits on originals.
- Every pipeline goes in `lab-log.md` **with its output** — pipelines
  without evidence are guesses.
- All work as your normal user; nothing here needs sudo.
