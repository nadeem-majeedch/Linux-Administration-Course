# Drill Book — Incident 1: The Vanished Service

> Setup time: 5 min · Solve time: ~25 min
> Cards: [6 — Service failed](../scenarios/06-service-failed.md) + [10 — Python env failure](../scenarios/10-python-env-failure.md)
> Everything here lives in your user-scope units (M20) and your own venv.

## Setup (run this, then close it — no peeking while solving)

```bash
#!/usr/bin/env bash
# setup-incident-1.sh — breaks ONLY your own user unit + your own venv
set -euo pipefail
mkdir -p ~/drill1 && cd ~/drill1

# a tiny analysis service (M20 user-unit pattern)
python3 -m venv .venv
./.venv/bin/python -m pip install -q pandas==2.2.3 flask==3.0.3
cat > app.py <<'EOF'
from flask import Flask
import pandas as pd
app = Flask(__name__)
@app.route("/health")
def health(): return {"ok": True}
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5055)
EOF
cat > myapi.service <<'EOF'
[Unit]
Description=Drill-1 analysis API
[Service]
ExecStart=%h/drill1/.venv/bin/python %h/drill1/app.py
Restart=on-failure
[Install]
WantedBy=default.target
EOF
mkdir -p ~/.config/systemd/user
cp myapi.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now myapi.service
sleep 2 && systemctl --user is-active myapi.service

# THE BREAK — two faults, one incident:
rm -rf .venv/lib/python3*/site-packages/pandas        # fault A: dep vanishes
sed -i 's|/drill1/.venv/bin/python|/usr/bin/python3|' \
    ~/.config/systemd/user/myapi.service              # fault B: ExecStart re-pointed
systemctl --user daemon-reload
systemctl --user restart myapi.service || true
echo "Incident 1 staged. Service state:"
systemctl --user is-active myapi.service || echo "(failed)"
```

## The symptom (all you get)

```console
$ systemctl --user status myapi.service
● myapi.service - Drill-1 analysis API
     Active: failed (Result: exit-code) …
```

The endpoint `curl http://127.0.0.1:5055/health` refuses. **Your
incident brief:** "The analysis API is down; it was fine yesterday."

## Solving notes (for the grader in you)

- Expect **two** faults. The first hypothesis the journal suggests will
  be *true but insufficient* — fixing only fault A still fails. That's
  the lesson: the second hypothesis comes from evidence *after* the
  first fix, and step 7 (verify) is what exposes the residue.
- Exit-code decoding (card 6) discriminates the fault classes: one is
  a 203-class ExecStart problem, one an app-level import failure.
- Safe tests: `systemctl --user cat` (read the unit as-installed),
  `/usr/bin/python3 -c "import pandas"` (the re-pointed interpreter's
  world), `journalctl --user -u myapi -n 20` — all read-only, all
  evidence.
- The undo: restore the ExecStart line (sed back or rewrite the unit
  verbatim) + recreate the venv *from the pin discipline* (the setup
  shows the two packages; your `requirements.txt` should say so —
  that's the prevention sentence).

**Done when:** the health endpoint returns 200 *through the service*
(not by hand-running the app), the journal is quoted at each stage,
and the eight-step block names both root causes with their
preventations ("absolute venv path in ExecStart", "pinned requirements
recreate").

Next: [Incident 2 — the full disk that isn't](lab-02-the-full-disk-that-isnt.md)
