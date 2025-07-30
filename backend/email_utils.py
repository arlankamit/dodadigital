import os
import smtplib
from email.mime.text import MIMEText

# 🎯 Безопасно: конфигурация из переменных окружения
SMTP_SERVER = os.environ.get("EMAIL_HOST", "smtp.zoho.com")
SMTP_PORT = int(os.environ.get("EMAIL_PORT", "465"))
SMTP_USER = os.environ.get("EMAIL_HOST_USER")
SMTP_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_RECEIVER = os.environ.get("EMAIL_RECEIVER", SMTP_USER)

def send_email(name: str, email: str, message: str, phone: str) -> dict:
    subject = "Новое сообщение с сайта dodadigital.kz"
    body = f"""
Имя: {name}
Email: {email}
Телефон: {phone}

Сообщение:
{message}
"""


    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, EMAIL_RECEIVER, msg.as_string())
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}
