#!/usr/bin/env python3
"""Dataset generator for M08 — Text Processing Toolkit.

Writes all six course datasets with deliberate, *declared* dirt so text
tools have something real to chew on. Deterministic: every dataset is
byte-identical on every machine (fixed seeds). Re-run any time:

    python3 modules/M08-text-processing/content/data/generate_data.py

Output directory: modules/M08-text-processing/content/data/
"""
import random
import shutil
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).parent
random.seed(42)

# ---------------------------------------------------------------- users.csv
USERS = [
    ("u001", "Amara Okafor", "amara.okafor@uni.edu", "CS", 3),
    ("u002", "Boris Ivanov", "boris.i@uni.edu", "DS", 2),
    ("u003", "Chen Wei", "chen.wei@uni.edu", "DS", 4),
    ("u004", "Dara Keo", "dara.keo@uni.edu", "MATH", 1),
    ("u005", "Elif Yilmaz", "elif.y@uni.edu", "PHYS", 3),
    ("u006", "Farid Nasser", "farid.n@uni.edu", "DS", 2),
    ("u007", "Grace Mensah", "grace.m@uni.edu", "CS", 4),
    ("u008", "Hana Sato", "hana.sato@uni.edu", "DS", 1),
    ("u009", "Igor Petrov", "igor.p@uni.edu", "STAT", 3),
    ("u010", "Juana Ortiz", "juana.o@uni.edu", "DS", 2),
]

SERVICES = ["api-gateway", "auth-service", "data-loader", "report-engine",
            "ml-inference", "worker-queue"]
LEVELS = ["INFO"] * 12 + ["WARN"] * 4 + ["ERROR"] * 3      # ~18% problems
IPS = [f"10.0.{a}.{b}" for a in range(1, 5) for b in range(1, 12)]
PATHS = ["/api/v1/datasets", "/api/v1/queries", "/api/v1/models/run",
         "/api/v1/reports/daily", "/api/v1/auth/login", "/health",
         "/api/v1/datasets/upload", "/static/app.js"]


def write(path: Path, text: str) -> None:
    # Force LF line endings: these files model Linux text on all platforms.
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print(f"wrote {path.relative_to(HERE)} ({len(text.splitlines())} lines)")


# ------------------------------------------------------- sales transactions
def gen_transactions() -> None:
    regions = ["emea", "apac", "amer", "latam"]
    lines = ["transaction_id,date,region,product,amount"]
    tx = 1000
    for day in range(1, 92):                      # 2019-01-01 .. 2019-03-31
        d = datetime(2019, 1, 1) + timedelta(days=day - 1)
        for _ in range(random.randint(8, 15)):
            tx += random.randint(1, 7)
            amt = round(random.expovariate(1 / 240) + 5, 2)
            lines.append(f"TX{tx},{d:%Y-%m-%d},{random.choice(regions)},"
                         f"{random.choice(['widget','gadget','doohickey','thingamajig'])},{amt}")
    # deliberate dirt (declared in README): 4 duplicated rows, 1 negative
    dupes = [l for l in lines[1:] if l.startswith(("TX100", "TX150", "TX180", "TX200"))][:4]
    lines = lines[:1] + lines[1:] + dupes
    lines.insert(57, "TX240,2019-02-26,emea,widget,-42.50")
    write(HERE / "transactions.csv", "\n".join(lines) + "\n")


# ------------------------------------------------------------ server logs
def gen_server_log() -> None:
    start = datetime(2026, 3, 10, 0, 0, 0)
    lines = []
    for i in range(600):
        t = start + timedelta(seconds=i * 144 + random.randint(0, 60))
        lvl = random.choice(LEVELS)
        svc = random.choice(SERVICES)
        msgs = {"INFO": f"request processed in {random.randint(2, 400)}ms",
                "WARN": f"slow query took {random.randint(1500, 9000)}ms",
                "ERROR": f"connection refused after {random.randint(3, 5)} retries"}
        lines.append(f"{t:%Y-%m-%d %H:%M:%S} {lvl} {svc} {random.choice(IPS)} "
                     f"{random.choice(PATHS)} {msgs[lvl]}")
    write(HERE / "server.log", "\n".join(lines) + "\n")


# ------------------------------------------------------------ access logs
def gen_access_log() -> None:
    codes = [200] * 20 + [301] * 3 + [404] * 4 + [500] * 2
    sizes = lambda: random.choice([212, 1024, 4096, 15320, 88, 64210])
    lines = []
    start = datetime(2026, 3, 10, 0, 0, 0)
    for i in range(500):
        t = start + timedelta(seconds=i * 173 + random.randint(0, 90))
        ip = random.choice(IPS)
        path = random.choice(PATHS)
        code = random.choice(codes)
        lines.append(f'{ip} - - [{t:%d/%b/%Y:%H:%M:%S} +0000] "GET {path} HTTP/1.1" '
                     f'{code} {sizes()} "-" "CourseBot/1.0"')
    write(HERE / "access.log", "\n".join(lines) + "\n")


# --------------------------------------------------------------- students
def gen_students() -> None:
    headers = "student_id,name,email,program,year,gpa,credits"
    rows = [headers]
    for sid, name, email, prog, year in USERS:
        gpa = round(random.uniform(2.2, 4.0), 2)
        # deliberate dirt (declared): u006 has a trailing-space name, u008
        # a malformed email, u009 gpa written with a comma decimal
        if sid == "u006":
            name += " "
        if sid == "u008":
            email = "hana.sato AT uni.edu"
        if sid == "u009":
            gpa_s = f"{gpa:.2f}".replace(".", ",")
            rows.append('{},{},{},{},{},"{}",{}'.format(sid, name, email, prog, year, gpa_s, year * 30))
            continue
        rows.append(f"{sid},{name},{email},{prog},{year},{gpa:.2f},{year * 30}")
    write(HERE / "students.csv", "\n".join(rows) + "\n")


# ---------------------------------------------------------------- sensor
def gen_sensor() -> None:
    """TSV telemetry: 3 sensors, 1 Hz, ~30 min, with a gap and 2 spikes."""
    lines = ["timestamp\tsensor_id\ttemp_c\thumidity_pct"]
    base = datetime(2026, 3, 10, 12, 0, 0)
    temps = {"s1": 21.0, "s2": 19.5, "s3": 23.2}
    t = 0
    for i in range(1800):
        t += 1
        s2_offline = 700 <= t <= 730         # declared gap: ONLY s2 drops
        for sid in ("s1", "s2", "s3"):
            if sid == "s2" and s2_offline and random.random() < 0.95:
                continue
            drift = random.uniform(-0.15, 0.15)
            temp = round(temps[sid] + i * 0.002 + drift, 1)
            if sid == "s3" and t in (1200, 1201):   # declared spikes
                temp = round(temp + 40, 1)
            hum = round(45 + random.uniform(-3, 3), 1)
            stamp = (base + timedelta(seconds=t)).strftime("%Y-%m-%dT%H:%M:%S")
            lines.append(f"{stamp}\t{sid}\t{temp}\t{hum}")
    write(HERE / "sensor-telemetry.tsv", "\n".join(lines) + "\n")


# ----------------------------------------------------------- experiment log
def gen_experiment() -> None:
    lines = ["# experiment run: exp-2026-03-10-a  (declared dirt: 2 reruns, 1 FAIL)"]
    for i in range(40):
        stamp = (datetime(2026, 3, 10, 9, 0) + timedelta(minutes=i * 7)).strftime("%H:%M:%S")
        acc = round(0.7 + i * 0.004 + random.uniform(-0.01, 0.01), 4)
        status = "FAIL" if i == 23 else "OK"
        lines.append(f"epoch={i:02d} time={stamp} accuracy={acc:.4f} "
                     f"loss={round(1.3 - i * 0.02 + random.uniform(-0.02, 0.02), 4):.4f} "
                     f"lr=0.001 status={status}")
    write(HERE / "experiment.log", "\n".join(lines) + "\n")


# --------------------------------------------------------------- readme
README = """# M08 Datasets — schema, provenance & deliberate dirt

All files are generated by `generate_data.py` (fixed seed 42 → byte-identical
everywhere). Regenerate: `python3 generate_data.py`. License: course-internal
synthetic data (MIT per repo LICENSE).

| File | Format | Rows | Deliberate quirks (declared, never silent) |
|---|---|---|---|
| `transactions.csv` | CSV | ~1,030 | 4 duplicated rows; 1 negative amount (TX240) |
| `server.log` | space-separated log | 600 | mixed levels; ~18% WARN/ERROR |
| `access.log` | Apache combined | 500 | 404/500 responses; varied sizes |
| `students.csv` | CSV | 10 | u006 trailing-space name; u008 ` AT ` email; u009 comma-decimal GPA |
| `sensor-telemetry.tsv` | TSV | ~5,350 | 30-second outage for s2; two +40 °C spikes on s3 |
| `experiment.log` | key=value log | 40 | one FAIL epoch; 2 reruns of epoch 5-6 |

Use `sha256sum *` after regenerating to confirm integrity against your copy.
"""


def main() -> None:
    # idempotent: clean previous run
    for f in HERE.glob("*"):
        if f.is_file() and f.name != Path(__file__).name and f.name != "README.md":
            f.unlink()
    gen_transactions()
    gen_server_log()
    gen_access_log()
    gen_students()
    gen_sensor()
    gen_experiment()
    write(HERE / "README.md", README)
    print("\nAll datasets generated. sha256sums:")
    for f in sorted(HERE.glob("*.csv")) + sorted(HERE.glob("*.log")) + sorted(HERE.glob("*.tsv")):
        import hashlib
        print(f"  {hashlib.sha256(f.read_bytes()).hexdigest()[:16]}  {f.name}")


if __name__ == "__main__":
    main()
