# Cheatsheet — Unit 7: Git, Python, Docker, Serving

## Git (M26)

```bash
git init / git clone URL
git status; git log --oneline --graph
git add -p; git commit -m "why: what this changes"
git switch -c feature-x; git switch main
git merge feature-x               # resolve conflicts, then commit
git remote -v; git push; git pull --rebase
git restore FILE                  # discard worktree changes
git reflog                        # your safety net
```

Never commit: datasets (bulk), `.venv/`, logs, artifacts, secrets — write `.gitignore` first.

## Python environments (M27)

```bash
python3 -m venv .venv             # create (in project dir)
source .venv/bin/activate         # activate (prompt shows (.venv))
pip install -r requirements.txt   # pinned deps
pip freeze > requirements.txt     # pin AFTER a working install
python train.py > logs/train.log 2>&1 &   # background + log
deactivate                        # leave the venv
```

Run Jupyter on a server, reach it locally:

```bash
jupyter lab --no-browser --port 8888    # ON the server
ssh -L 8888:localhost:8888 dslab        # FROM your laptop, then browse
```

GPU awareness: `nvidia-smi` (GPU status), `CUDA_VISIBLE_DEVICES=0` (pick GPU).

## Docker (M28)

```bash
docker run -d --name app -p 8000:8000 -v data:/data image
docker ps -a; docker logs -f app; docker exec -it app bash
docker build -t myproj:latest .
docker compose up -d / down / logs -f
docker system df                  # disk usage (prune = cleanup, read flags first!)
docker cp app:/app/model.joblib . # get artifacts out
```

Volume = data survives container removal. Bind mount `-v "$PWD:/src"` = live files.

## Serving stack (M29)

```bash
sudo systemctl reload nginx       # after config edit; test first:
sudo nginx -t
sudo -u postgres psql -d mydb     # DB shell;  \copy sales FROM 'file.csv' CSV HEADER;
pg_dump mydb > backup.sql         # DB backup; psql mydb < backup.sql restores
curl localhost/api/health         # verify every hop
```
