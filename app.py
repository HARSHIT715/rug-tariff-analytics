"""Drug Tariff Analytics website: serves the dashboard, a JSON API and a token-protected admin page."""
import hmac
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename

import pipeline
from sample import make_sample

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024
WEB = Path(__file__).parent / "web"
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")
SAMPLE = make_sample()


def live_data():
    return json.loads(pipeline.OUT.read_text()) if pipeline.OUT.exists() else None


def authorised() -> bool:
    return bool(ADMIN_TOKEN) and hmac.compare_digest(request.form.get("token", ""), ADMIN_TOKEN)


def denied():
    msg = "Wrong or missing admin token." if ADMIN_TOKEN else "ADMIN_TOKEN is not set on the server, so admin actions are disabled."
    return jsonify(ok=False, message=msg), 403


@app.after_request
def headers(resp):
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Referrer-Policy"] = "same-origin"
    return resp


@app.get("/")
def index():
    return send_from_directory(WEB, "index.html")


@app.get("/admin")
def admin():
    return send_from_directory(WEB, "admin.html")


@app.get("/healthz")
def healthz():
    return "ok"


@app.get("/api/data")
def api_data():
    live = live_data()
    if live:
        updated = datetime.fromtimestamp(pipeline.OUT.stat().st_mtime, timezone.utc).strftime("%d %b %Y %H:%M UTC")
        return jsonify({**live, "meta": {"source": "live", "updated": updated, "latest": live["months"][-1]}})
    return jsonify({**SAMPLE, "meta": {"source": "sample"}})


@app.get("/api/status")
def api_status():
    live = live_data()
    files = sorted(p.name for p in pipeline.RAW.glob("*")) if pipeline.RAW.exists() else []
    return jsonify(source="live" if live else "sample", months=live["months"] if live else [],
                   products=len((live or SAMPLE)["products"]), files=files, admin_enabled=bool(ADMIN_TOKEN))


@app.post("/admin/upload")
def upload():
    if not authorised():
        return denied()
    f, kind, month = request.files.get("file"), request.form.get("kind"), request.form.get("month", "")
    ext = Path(secure_filename(f.filename or "")).suffix.lower() if f else ""
    if ext not in {".csv", ".xlsx"} or kind not in {"drug_tariff", "concessions"} or not re.fullmatch(r"\d{4}-\d{2}", month):
        return jsonify(ok=False, message="Choose a .csv or .xlsx file, a file type and a month."), 400
    pipeline.RAW.mkdir(parents=True, exist_ok=True)
    dest = pipeline.RAW / f"{kind}_{month}{ext}"
    backup = dest.read_bytes() if dest.exists() else None
    f.save(dest)
    try:
        info = pipeline.run()
    except Exception as e:  # bad headers, empty file, etc.: restore the previous state
        dest.unlink(missing_ok=True)
        if backup is not None:
            dest.write_bytes(backup)
        return jsonify(ok=False, message=f"Could not process that file: {e}"), 422
    return jsonify(ok=True, message=f"{dest.name} saved. {info}")


@app.post("/admin/portfolio")
def portfolio():
    if not authorised():
        return denied()
    terms = [t.strip() for t in request.form.get("terms", "")[:5000].splitlines() if t.strip()]
    pipeline.PORTFOLIO.parent.mkdir(parents=True, exist_ok=True)
    pipeline.PORTFOLIO.write_text("\n".join(terms))
    try:
        note = pipeline.run()
    except FileNotFoundError:
        note = "It will apply once the first tariff file is uploaded."
    except Exception as e:
        return jsonify(ok=False, message=f"Saved, but processing failed: {e}"), 422
    return jsonify(ok=True, message=f"Saved {len(terms)} portfolio entries. {note}")


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
