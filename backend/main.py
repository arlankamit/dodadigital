from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from email_utils import send_email

app = FastAPI()

# Разрешаем доступ с твоего фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dodadigital.kz"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/send-email")
def send_email_route(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    subject = f"Новое сообщение от {name} ({email})"
    full_message = f"От: {name} <{email}>\n\n{message}"

    success = send_email(subject, full_message)
    return {"success": success}
