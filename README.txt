ROYAL CROWN HOTEL — PYTHON + HTML + CSS + SQLITE DATABASE

Included:
- app.py: Python Flask backend
- templates/index.html: responsive hotel website
- static/style.css: royal theme styling
- SQLite database: enquiries are saved to enquiries.db automatically
- requirements.txt: Python dependencies
- render.yaml: deployment blueprint for Render

RUN ON YOUR COMPUTER:
1. Install Python 3.11 or newer.
2. Open a terminal in this folder.
3. Run: pip install -r requirements.txt
4. Run: python app.py
5. Open http://127.0.0.1:5000

EMAIL NOTIFICATIONS:
The enquiry form saves submissions in SQLite. To get each enquiry in tupevaishnavi20@gmail.com,
configure these environment variables in the hosting dashboard:
- HOTEL_EMAIL = tupevaishnavi20@gmail.com
- SMTP_HOST = your email provider's SMTP server
- SMTP_PORT = 587
- SMTP_USER = the sending email account
- SMTP_PASSWORD = an app password or SMTP credential (never put it in public code)

For Gmail SMTP, enable 2-Step Verification on the sending Gmail account and create an App Password.
Use the account you control as SMTP_USER; it may be the same inbox or a separate sender account.
Do not share your normal Gmail password with anyone or upload it to GitHub.

DEPLOYMENT / WHATSAPP LINK:
This ZIP is the website source code, not a live website link yet.
To get a public HTTPS link that opens when shared on WhatsApp:
1. Create a GitHub account at https://github.com and upload these project files into a new repository.
2. Create a Render account at https://render.com and connect the repository.
3. Deploy as a Python web service (the included render.yaml is a starting point).
4. Add SMTP environment variables in Render settings to enable email notifications.
5. Copy the live https://...onrender.com address and send that link on WhatsApp.

IMPORTANT DATABASE NOTE:
SQLite is good for learning/local demos. On some free hosting plans, local files can reset after redeploy/restart.
For reliable production enquiries, attach a persistent disk for the SQLite database or migrate to a managed PostgreSQL database.
Do not advertise room prices or facilities as real until you verify them; the current prices and amenities are sample content.
Hotel photos are loaded from Unsplash and require internet access.
