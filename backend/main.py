from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

# Разрешить CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или ["https://dodadigital.kz"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailData(BaseModel):
    name: str
    email: str
    message: str

@app.post("/send-email")
def send_email(data: EmailData):
    sender_email = "office@dodadigital.kz"  # Отправитель
    receiver_email = "office@dodadigital.kz"  # Получатель
    subject = "Новое сообщение с сайта"
    
    body = f"""
    Имя: {data.name}
    Email: {data.email}
    Сообщение:
    {data.message}
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.zoho.com", 465) as server:
            server.login("office@dodadigital.kz", "ПАРОЛЬ_ОТ_ПОЧТЫ")
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}
