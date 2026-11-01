import os
import sqlite3
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-before-deploying")
DB_PATH = os.environ.get("DATABASE_PATH", "enquiries.db")

@app.context_processor
def inject_year():
    from datetime import datetime
    return {"current_year": datetime.now().year}

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS enquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                subject TEXT,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        con.commit()

def send_notification(name, email, phone, subject, message):
    """Send an email if SMTP environment variables have been configured."""
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    recipient = os.environ.get("HOTEL_EMAIL", "tupevaishnavi20@gmail.com")

    if not all([smtp_host, smtp_user, smtp_password, recipient]):
        return False

    msg = EmailMessage()
    msg["Subject"] = f"Royal Crown Hotel enquiry: {subject or 'General enquiry'}"
    msg["From"] = smtp_user
    msg["To"] = recipient
    msg["Reply-To"] = email
    msg.set_content(
        "A new enquiry was submitted on Royal Crown Hotel website.\\n\\n"
        f"Name: {name}\\nEmail: {email}\\nPhone: {phone or 'Not provided'}\\n"
        f"Subject: {subject or 'General enquiry'}\\n\\nMessage:\\n{message}"
    )
    with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
    return True

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/enquiry", methods=["POST"])
def enquiry():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    subject = request.form.get("subject", "General enquiry").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        flash("Please fill in your name, email and message.", "error")
        return redirect(url_for("home") + "#contact")

    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            "INSERT INTO enquiries (name, email, phone, subject, message) VALUES (?, ?, ?, ?, ?)",
            (name, email, phone, subject, message)
        )
        con.commit()

    try:
        sent = send_notification(name, email, phone, subject, message)
    except Exception:
        app.logger.exception("Email notification failed")
        sent = False

    if sent:
        flash("Thank you! Your enquiry was saved and an email notification was sent.", "success")
    else:
        flash("Thank you! Your enquiry was saved. Email notification needs SMTP setup by the website owner.", "success")
    return redirect(url_for("home") + "#contact")

@app.route("/health")
def health():
    return {"status": "ok"}

init_db()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
