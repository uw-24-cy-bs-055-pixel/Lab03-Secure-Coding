
import hashlib
import os
import hmac
import json
import sqlite3
import requests
from pathlib import Path
from functools import wraps
from flask import Flask, request, session, send_file, render_template
import math
from markupsafe import escape

app = Flask(__name__)
app.secret_key = os.environ["SMARTCAMPUS_SECRET_KEY"]
GATEWAY_TOKEN = os.environ["GATEWAY_TOKEN"]
DB = "fees.db"


def db():
    return sqlite3.connect(DB)


def require_role(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if session.get("role") != role:
                return "Forbidden", 403
            return func(*args, **kwargs)
        return wrapper
    return decorator


@app.route("/invoice")
def invoice():
    sid = request.args.get("student_id")

    if str(session.get("uid")) != str(sid):
        return "Forbidden", 403

    rows = db().execute(
        "SELECT term, amount, status FROM invoices WHERE student_id=?",
        (sid,)
    ).fetchall()

    return str(rows)


@app.route("/pay", methods=["POST"])
def pay():
    receipt = hmac.new(
        app.secret_key.encode(),
        (request.form["student_id"] + request.form["amount"]).encode(),
        hashlib.sha256
    ).hexdigest()

    r = requests.post(
        "https://pay.example.com/charge",
        data={
            "token": GATEWAY_TOKEN,
            "amount": request.form["amount"]
        },
        verify=True,
        timeout=10
    )
    return receipt + r.text



@app.route("/discount")
def discount():
    value = request.args.get("percent", "0").strip()

    if value.lower() == "nan":
        return "Invalid discount", 400

    try:
        percent = float(value)

        if not math.isfinite(percent) or not 0 <= percent <= 100:
            return "Invalid discount", 400

        return str(percent)

    except (ValueError, TypeError):
        return "Invalid discount", 400

@app.route("/import", methods=["POST"])
@require_role("bursar")
def import_batch():
    try:
        data = json.loads(request.data)
        return str(data)
    except (ValueError, TypeError):
        return "Invalid JSON", 400


@app.route("/notice")
def notice():
    name = request.args.get("name", "")
    return render_template("notice.html", name=name)


@app.route("/receipt")
def receipt():
    receipt_dir = Path("receipts").resolve()
    file_path = (
        receipt_dir / request.args.get("file", "")
    ).resolve()

    if not file_path.is_relative_to(receipt_dir) or not file_path.is_file():
        return "Invalid receipt file", 400

    return send_file(file_path)


@app.route("/refund", methods=["POST"])
@require_role("bursar")
def refund():
    connection = db()
    try:
        connection.execute(
            "UPDATE invoices SET status='refunded' WHERE id=?",
            (request.form["id"],)
        )
        connection.commit()
    finally:
        connection.close()

    return "Refunded"


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=False)
