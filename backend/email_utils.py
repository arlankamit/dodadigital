import os
import smtplib
from email.mime.text import MIMEText
from logger import get_logger

log = get_logger("email_poller")

SMTP_SERVER = os.environ.get("EMAIL_HOST", "smtp.zoho.com")
SMTP_PORT = int(os.environ.get("EMAIL_PORT", "465"))
SMTP_USER = os.environ.get("EMAIL_HOST_USER")
SMTP_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

EMAIL_RECEIVER = os.environ.get("EMAIL_RECEIVER", SMTP_USER)  # для форм с сайта

def send_email(name: str, email: str, message: str, phone: str) -> dict:
    """
    Сообщение с сайта -> на общий ящик (EMAIL_RECEIVER).
    """
    subject = "Новое сообщение с сайта dodadigital.kz"
    body = f"""Имя: {name}
Email: {email}
Телефон: {phone}

Сообщение:
{message}
"""
    return _smtp_send(EMAIL_RECEIVER, subject, body)

def send_email_reply(to_email: str, subject: str, body: str) -> dict:
    """
    Ответ отправителю входящего письма.
    """
    return _smtp_send(to_email, subject, body)

def _smtp_send(to_email: str, subject: str, body: str) -> dict:
    if not all([SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD]):
        log.error("SMTP env vars missing")
        return {"success": False, "error": "missing_env"}

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, [to_email], msg.as_string())
        log.info(f"Email sent to={to_email} subject={subject}")
        return {"success": True}
    except Exception as e:
        log.exception(f"Email send exception: {e}")
        return {"success": False, "error": str(e)}
