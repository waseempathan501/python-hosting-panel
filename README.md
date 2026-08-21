# Waseem Visuals — File Hosting

Flask-based personal hosting site: profile page + a dashboard that hosts
HTML/CSS/JS files, raw pasted HTML code, images, audio, video, and any
other file — each gets an instant live link.

## Deploy on Railway
1. Push this folder to a GitHub repo (or use Railway's "Deploy from local").
2. On Railway: **New Project → Deploy from GitHub repo**.
3. Railway auto-detects `requirements.txt` + `Procfile` — no extra config needed.
4. Once deployed, open the generated `*.up.railway.app` URL.

## Important note about uploaded files
Railway's default filesystem is **ephemeral** — every time you redeploy
(push new code), the `uploads/` folder and `files_db.json` are wiped and
start empty again. Files you upload will stay live and working between
normal restarts, but not across redeploys.

To make uploads permanent, add a **Railway Volume**:
- Project → your service → **Settings → Volumes → New Volume**
- Mount path: `/app/uploads`
- Redeploy — after this, `uploads/` survives redeploys.

## Run locally
```
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000
