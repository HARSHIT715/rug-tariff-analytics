💊 Drug Tariff Analytics Dashboard
NHS Drug Tariff Price Monitoring for Dr. Reddy's Laboratories
A Flask-based analytics dashboard for monitoring NHS Drug Tariff reimbursement prices, reviewing price movements and concessions, and highlighting changes relevant to a configured Dr. Reddy's product portfolio.
<p align="center">
  <a href="https://drug-tariff-analytics.onrender.com">
    <img src="https://img.shields.io/badge/🌐_Live_Demo-Open_Website-2ea44f?style=for-the-badge" alt="Live Demo">
  </a>
  <img src="https://img.shields.io/badge/Python-Flask-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Flask">
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Hosting-Render-5A67D8?style=for-the-badge" alt="Render">
</p>
<p align="center">
  <strong>🚀 Live Website:</strong>
  <a href="https://drug-tariff-analytics.onrender.com">drug-tariff-analytics.onrender.com</a>
</p>
---
📸 Dashboard Preview
<!-- Add a real screenshot of your deployed dashboard to the repository at screenshots/dashboard.png, then uncomment the next line. -->
<!-- ![Drug Tariff Analytics Dashboard](screenshots/dashboard.png) -->
To add a preview, create a `screenshots` folder in this repository, upload a screenshot named `dashboard.png`, and uncomment the image line above.
✨ Key Features
📊 Price Analytics — review drug reimbursement prices and price movements.
📈 Trend Monitoring — compare changes across monthly tariff datasets.
🏷️ Category Analysis — review movements across tariff categories.
💷 Price Concessions — process concession information when a suitable file is provided.
🔔 Change Monitoring — highlight important price movements shown by the application.
🎯 Portfolio Tracking — prioritize products matching the configured portfolio list.
📂 Monthly Data Uploads — upload tariff files through the protected admin page.
🔐 Admin Authentication — protect administrative pages with configured credentials.
🗄️ Data Processing — process tariff data using Python and store results for the dashboard.
🛠️ Technology Stack
Technology	Purpose
Python	Application logic and data processing
Flask	Web application and API
SQLite	Structured data storage
HTML, CSS, JavaScript	Dashboard interface
Pandas	Tabular data processing, if used by the pipeline
Render	Cloud hosting and deployment
GitHub	Source control and project hosting
⚙️ How It Works
Upload: An authorized administrator uploads a monthly Drug Tariff file.
Process: The Python pipeline reads and processes the supplied data.
Analyze: The application calculates price changes and organizes the results.
Store: Processed information is saved in SQLite and generated JSON data.
Visualize: The public dashboard presents the available trends, category movements, concessions, and portfolio-related results.
🗂️ Project Structure
Path	Role
`app.py`	Flask server, website routes, JSON API, and protected admin routes
`pipeline.py`	Processes monthly tariff files and generates analytics data
`sample.py`	Illustrative data displayed before real data is uploaded
`web/index.html`	Public dashboard interface
`web/admin.html`	Admin upload interface and portfolio editor
`render.yaml`	Render deployment blueprint
`requirements.txt`	Python dependencies
`README.md`	Project documentation
🌐 Live Demo
Public dashboard: https://drug-tariff-analytics.onrender.com
The public dashboard may show sample data until a valid monthly Drug Tariff file has been uploaded and processed.
The admin panel is available at `/admin` on the deployed site and requires the configured login credentials. Keep admin credentials and tokens private; do not commit them to GitHub.
🚀 Deployment
This project is deployed on Render and linked to its GitHub repository.
For a new deployment:
Push the project to a GitHub repository.
In Render, create a Web Service or deploy the included Blueprint if your `render.yaml` is configured for it.
Set the build command to `pip install -r requirements.txt`.
Set the start command to `gunicorn app:app --workers 1 --threads 4 --timeout 120`, if this matches your deployment configuration.
Configure the environment variables `ADMIN_USERNAME`, `ADMIN_PASSWORD`, and `ADMIN_TOKEN` in Render. Use strong, unique values and never publish them in this README.
Deploy and open the public dashboard URL above.
⚠️ Limitations
Drug Tariff file layouts and column headers can vary between releases. Uploads may require the processing pipeline to be updated for the exact file format.
Concession matching depends on product-name wording and the structure of the supplied concession file.
The dashboard displays up to 60 products, with configured portfolio products prioritized, while the database may retain more processed products.
Render's free web service can sleep after inactivity, so the first visit after a period without traffic may take longer to load.
Free hosting does not provide persistent disk storage by default. Uploaded files and database contents may be lost after a restart or redeploy unless persistent storage is configured and the app's `DATA_DIR` points to it.
🗺️ Future Improvements
[ ] Improve CSV and Excel header detection for different Drug Tariff formats.
[ ] Add stronger validation and clearer upload error messages.
[ ] Expand historical comparisons across monthly datasets.
[ ] Add downloadable analytics reports.
[ ] Provide more detailed portfolio-level insights.
[ ] Configure persistent storage for reliable long-term data retention.
[ ] Expand automated tests for data processing and API routes.
🔒 Security
Keep `ADMIN_USERNAME`, `ADMIN_PASSWORD`, and `ADMIN_TOKEN` private.
Store secrets in Render's Environment settings rather than in source code.
Never paste credentials or tokens into issues, screenshots, or public commits.
---
<p align="center">
  Built with Python, Flask, and a focus on practical drug tariff analytics.
</p>
