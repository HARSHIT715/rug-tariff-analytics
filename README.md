# 💊 Drug Tariff Analytics Dashboard

### NHS Drug Tariff Price Monitoring for Dr. Reddy's Laboratories

A Flask-based analytics dashboard for monitoring NHS Drug Tariff reimbursement prices, reviewing price movements and concessions, and highlighting changes relevant to a configured Dr. Reddy's product portfolio.

<p align="center">
  <a href="https://drug-tariff-analytics.onrender.com/">
    <img src="https://img.shields.io/badge/LIVE_DEMO-Open_Website-2ea44f?style=for-the-badge" alt="Live Demo">
  </a>
  <img src="https://img.shields.io/badge/Python-Flask-blue?style=for-the-badge&logo=python" alt="Python Flask">
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite" alt="SQLite">
  <img src="https://img.shields.io/badge/Hosting-Render-5A67D8?style=for-the-badge" alt="Render">
</p>

---

## ✨ Key Features

* 📊 **Price Analytics** — Review drug reimbursement prices and price movements.
* 📈 **Trend Monitoring** — Compare changes across monthly tariff datasets.
* 🏷️ **Category Analysis** — Review movements across tariff categories.
* 💷 **Price Concessions** — Process concession information when a suitable file is provided.
* 🔔 **Change Monitoring** — Highlight important price movements shown by the application.
* 🎯 **Portfolio Tracking** — Prioritize products matching the configured portfolio list.
* 📂 **Monthly Uploads** — Upload tariff files through the protected admin page.
* 🔐 **Admin Authentication** — Protect administrative pages with configured credentials.

## 🛠️ Technology Stack

| Technology            | Purpose                               |
| --------------------- | ------------------------------------- |
| Python                | Application logic and data processing |
| Flask                 | Web application and API               |
| SQLite                | Structured data storage               |
| HTML, CSS, JavaScript | Dashboard interface                   |
| Render                | Cloud hosting and deployment          |
| GitHub                | Source control and project hosting    |

## ⚙️ How It Works

1. **Upload:** An authorized administrator uploads a monthly Drug Tariff file.
2. **Process:** The Python pipeline reads and processes the supplied data.
3. **Analyze:** The application calculates price changes and organizes the results.
4. **Store:** Processed information is saved in SQLite and generated JSON data.
5. **Visualize:** The dashboard presents available trends, category movements, concessions, and portfolio-related results.

## 🗂️ Project Structure

| File               | Description                                                        |
| ------------------ | ------------------------------------------------------------------ |
| `app.py`           | Flask server, website routes, JSON API, and protected admin routes |
| `pipeline.py`      | Processes monthly tariff files and generates analytics data        |
| `sample.py`        | Illustrative data displayed before real data is uploaded           |
| `web/index.html`   | Public dashboard interface                                         |
| `web/admin.html`   | Admin upload interface and portfolio editor                        |
| `render.yaml`      | Render deployment blueprint                                        |
| `requirements.txt` | Python dependencies                                                |

## 🌐 Live Website

**[Open Drug Tariff Analytics Dashboard](https://drug-tariff-analytics.onrender.com/)**

The dashboard may display sample data until a valid monthly Drug Tariff file has been uploaded and processed.

## 🚀 Deployment

This project is hosted on Render and connected to GitHub.

For deployment, configure the following:

* **Build command:** `pip install -r requirements.txt`
* **Start command:** `gunicorn app:app --workers 1 --threads 4 --timeout 120`
* **Environment variables:** `ADMIN_USERNAME`, `ADMIN_PASSWORD`, and `ADMIN_TOKEN`

Use strong, unique secrets and configure them in Render's Environment settings. Never commit credentials or tokens to GitHub.

## ⚠️ Limitations

* Drug Tariff file layouts and column headers can vary between releases.
* Concession matching depends on product-name wording and the supplied file structure.
* The dashboard displays up to 60 products, prioritizing configured portfolio products.
* Render's free service may sleep after inactivity.
* Free hosting does not provide persistent disk storage by default. Uploaded files and database contents may be lost after a restart or redeploy unless persistent storage is configured.

## 🗺️ Future Improvements

* [ ] Improve CSV and Excel header detection.
* [ ] Add stronger upload validation and clearer error messages.
* [ ] Expand historical comparisons across monthly datasets.
* [ ] Add downloadable analytics reports.
* [ ] Provide more detailed portfolio-level insights.
* [ ] Configure persistent storage.
* [ ] Expand automated tests.

## 🔒 Security

* Keep `ADMIN_USERNAME`, `ADMIN_PASSWORD`, and `ADMIN_TOKEN` private.
* Store secrets in Render Environment settings, not in source code.
* Never publish credentials in screenshots, issues, or public commits.

---

<p align="center">
  Built with Python and Flask.
</p>
