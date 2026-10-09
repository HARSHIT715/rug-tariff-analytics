# Drug Tariff Analytics

A Flask dashboard for exploring NHS Drug Tariff price trends, category movements and price concessions, with a protected admin area for monthly uploads and Dr. Reddy's portfolio tracking.

**Live dashboard:** https://drug-tariff-analytics.onrender.com

> **Data note:** Until real tariff files are uploaded, the dashboard displays illustrative sample data. Sample figures are not official NHS reimbursement prices.

## Features

- Interactive price trends and market/portfolio comparisons
- Category A, C and M movement indicators
- Price-concession flags and alerts
- Searchable product explorer and CSV export
- Admin-only CSV/XLSX upload workflow
- Header-row detection for files that start with a report title or metadata
- SQLite record of processed tariff rows and dashboard JSON output
- Basic authentication for admin pages plus a separate admin action token
- Automated tests through GitHub Actions

## Project structure

| Path | Purpose |
| --- | --- |
| `app.py` | Flask routes, admin authentication, upload validation and CSV export |
| `pipeline.py` | Reads monthly files, normalizes data, calculates changes and builds dashboard output |
| `sample.py` | Clearly illustrative data for the empty-state dashboard |
| `web/index.html` | Public dashboard |
| `web/admin.html` | Protected admin upload and portfolio page |
| `test_pipeline.py` | Parser and data validation tests |
| `test_app.py` | Flask route, authentication and upload tests |
| `.github/workflows/tests.yml` | Automated test workflow |
| `render.yaml` | Render deployment configuration |

## Admin setup

In the Render service's **Environment** settings, configure these variables:

- `ADMIN_USERNAME` — admin login username
- `ADMIN_PASSWORD` — admin login password
- `ADMIN_TOKEN` — separate token required for upload and portfolio changes

Keep all three values private. Do not commit them to GitHub or put them in screenshots. If a credential is exposed, rotate it in Render.

Open `/admin` on the live site. The browser first asks for the username and password. Then enter the `ADMIN_TOKEN` into the form to upload a file or update the portfolio list.

## Uploading monthly data

1. Download the appropriate official monthly Drug Tariff data file from NHSBSA.
2. In `/admin`, select **Drug Tariff prices** or **Price concessions**, select the month, choose a CSV or XLSX file and submit.
3. Check the response message and the data status before assuming the upload succeeded.
4. Confirm the public dashboard shows live data and the correct latest month.

The parser scans the first 15 rows for a header and supports common variations of product, pack, price and category column names. Some NHSBSA exports use different layouts or category-specific files; those may still require an explicit mapping. Always compare the processed figures with the official source before using them for decisions.

Prices are currently interpreted as pence and converted to pounds. If your source file already expresses prices in pounds, update `PRICE_IN_PENCE` in `pipeline.py` before uploading it.

## Deployment

The project is configured for Render with Gunicorn. The service health check is `/healthz`.

1. Push the project to the connected GitHub repository.
2. Let Render build and deploy the latest commit.
3. Confirm `/healthz` returns `ok`.
4. Visit the public dashboard and check that `/admin` requires login.
5. Upload a small known test file and confirm the dashboard data changes.

## Storage limitation

The default Render free web service does **not** provide a persistent disk. Files in the service's local filesystem may be lost when the service restarts or redeploys, so the current SQLite database, uploaded files and generated dashboard JSON should not be treated as permanent history on the free plan.

For persistent history, configure a Render persistent disk on a plan that supports it and set `DATA_DIR` to the disk's mount path (for example `/var/data`). Ensure the disk is mounted at that path before deploying. Do not enable this configuration unless the service has the disk attached.

## Tests

For development and CI, install the development dependencies:

```bash
pip install -r requirements-dev.txt
pytest -q
```

GitHub Actions runs the test suite on pushes and pull requests.

## Current limitations

- The dashboard visualizes up to 60 products at a time; the underlying SQLite table stores all processed rows.
- Concession matching currently compares normalized product names and may miss wording differences.
- Price comparisons are only as reliable as the source file's columns, units and selected month.
- Persistent data retention requires persistent storage to be configured on the hosting platform.

## Roadmap

- Store uploaded files and processed history on persistent storage
- Add a month-by-month comparison view and downloadable filtered reports
- Improve concession matching and file-specific column mappings
- Add deployment smoke tests and more coverage for real NHSBSA file variants
