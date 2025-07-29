import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.yourserver.com"  # например, smtp.yandex.kz
SMTP_PORT = 587
SMTP_USER = "noreply@dodadigital.kz"
SMTP_PASSWORD = "your_password"

TO_EMAIL = "office@dodadigital.kz"

def send_email(subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = TO_EMAIL

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, TO_EMAIL, msg.as_string())
        return True
    except Exception as e:
        print(f"Email send error: {e}")
        return False
