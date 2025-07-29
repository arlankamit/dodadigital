import smtplib
from email.mime.text import MIMEText

# Конфигурация (лучше вынести в .env позже)
SMTP_SERVER = "smtp.zoho.com"
SMTP_PORT = 465
SMTP_USER = "office@dodadigital.kz"
SMTP_PASSWORD = "ПАРОЛЬ_ОТ_ПОЧТЫ"  # Замени на ENV для безопасности

def send_email(name: str, email: str, message: str) -> dict:
    subject = "Новое сообщение с сайта dodadigital.kz"
    body = f"""
    Имя: {name}
    Email: {email}

    Сообщение:
    {message}
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = SMTP_USER

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, SMTP_USER, msg.as_string())
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}
