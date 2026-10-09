# Drug Tariff Analytics Website

🌐 **Live Website:** https://drug-tariff-analytics.onrender.com# Drug Tariff Analytics Website

A Flask website that monitors NHS Drug Tariff reimbursement prices for Dr. Reddy's Laboratories: price trends, category movements, concessions and alerts. It shows sample data until you upload real monthly files on the Admin page.

## What is inside

| Path | Role |
|---|---|
| `app.py` | Flask server: the site, the JSON API, and the token-protected admin routes |
| `pipeline.py` | Cleans monthly Drug Tariff files, calculates changes, writes SQLite and the JSON the site reads |
| `sample.py` | Illustrative data shown before any upload |
| `web/index.html` | The dashboard website |
| `web/admin.html` | Upload page and portfolio list |
| `render.yaml` | Render deployment blueprint |

## Deploy on Render

1. Create a GitHub repository and push this folder:
   `git init && git add . && git commit -m "Drug Tariff site" && git branch -M main && git remote add origin <your-repo-url> && git push -u origin main`
2. In Render, choose **New** then **Blueprint**, connect the repository and apply. Render reads `render.yaml` and builds the service.
   (Or choose **New** then **Web Service** and set build command `pip install -r requirements.txt` and start command `gunicorn app:app --workers 1 --threads 4 --timeout 120`.)
3. When the deploy finishes, your site is at `https://<service-name>.onrender.com`.
4. Open the service's **Environment** tab and copy the generated `ADMIN_TOKEN`. You need it on the Admin page.
5. Go to `/admin`, upload each month's Drug Tariff file (and optionally the concessions file), and add your portfolio product names. The dashboard updates straight away.

## Free plan limits

- A free service goes to sleep after 15 minutes without traffic, so the first visit afterwards takes about a minute to wake.
- The free plan has no persistent disk. Uploaded files and the database are lost whenever the service restarts or redeploys, and the site goes back to sample data. To keep data, use a paid plan, add a disk in `render.yaml` and set `DATA_DIR` to its mount path (see the comments in that file).

## Run locally

```
pip install -r requirements.txt
ADMIN_TOKEN=choose-a-token python app.py
```
Open http://localhost:5000. Data is stored in `data/` unless `DATA_DIR` is set.

## Things to check

- Column headers differ between Drug Tariff releases. If an upload is rejected for a missing column, extend the `COLS` lists in `pipeline.py`.
- The Admin page asks for a month because the pipeline reads it from the file name (`drug_tariff_YYYY-MM`).
- Concessions are matched to tariff lines by product name, so wording differences can cause misses.
- The dashboard shows up to 60 products (portfolio first, then biggest movers). The database keeps everything.
- Keep `ADMIN_TOKEN` private. Anyone with it can replace your data.
