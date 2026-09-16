# Dataset Build Status

Companion to [README.md](README.md). Datasets marked *pending* are generated in the
content phase (per dataset: generator script, README with schema/provenance/quirks,
and checksums). No bulk data is committed directly.

| Dataset | Status | Producer |
|---|---|---|
| `experiment.log` | **delivered** (M08 data; key=value ML training log) | M08 generator |
| `sales-2019-q1.csv` | **delivered as `transactions.csv`** (M08 data) | [M08 generator](../modules/M08-text-processing/content/data/generate_data.py) |
| `server.log` | **delivered** (M08 data, 600 lines) | M08 generator |
| `access.log` | **delivered** (M08 data, 500 lines) | M08 generator |
| `syslog-sample.log` | pending | generator script (M24 will deliver) |
| `students.csv` | **delivered** (M08 data, 10 records w/ declared dirt) | M08 generator |
| `sensor-telemetry.tsv` | **delivered** (M08 data, ~5.3k rows) | M08 generator |

Rules (from CONTRIBUTING.md, "Dataset Contributions"):

1. Generated datasets must be reproducible from their script and license-clean.
2. Every dataset ships its own README: schema, provenance, license, known quirks.
3. Checksums (`sha256sum`) are published in the dataset README and `expected/`.
4. Size guideline: ≤ ~10 MB per dataset; larger data goes through generation scripts
   or external official sources with checksums.
5. Deliberate dirt (duplicates, malformed emails, BOM, gaps) is a feature — but it
   must be declared in the dataset README, never silent.
