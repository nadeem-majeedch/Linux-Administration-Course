# Module 23 Labs — File Transfer & Synchronization

> Two labs, both **loopback-only** (`localhost` inside your own VM).
> No real remote hosts, no credentials, nothing outside `~/m23lab*`.

| # | Lab | Focus |
|---|-----|-------|
| 1 | [lab-01-dataset-sync-circuit.md](lab-01-dataset-sync-circuit.md) | scp precision, sftp session, rsync measurement, slash rule, interrupt & resume, sacrificial `--delete` demonstration |
| 2 | [lab-02-transfer-automation.md](lab-02-transfer-automation.md) | Guarded sync script, weekly pull→clean→push→verify loop, manifest verification, failure reading |

Shared rules: start `script m23-labN.log` before touching anything;
answer every **Checkpoint** inline in the transcript; teardown only
paths you created this session, by exact name, after printing them.
