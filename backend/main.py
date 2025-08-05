from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from email_utils import send_email
from imap_reader import check_emails_and_reply
from whatsapp_utils import send_whatsapp_message

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailData(BaseModel):
    name: str
    email: str
    message: str
    phone: str

@app.get("/")
def root():
    return {"message": "Doda API is running."}

@app.post("/send-email")
def handle_email(data: EmailData):
    return send_email(data.name, data.email, data.message, data.phone)

@app.get("/check-inbox")
def handle_check_inbox():
    return check_emails_and_reply()

@app.post("/send-whatsapp")
def handle_whatsapp(data: EmailData):
    msg = f"Здравствуйте, {data.name}!\nВаше сообщение получено: {data.message}\nНаш специалист скоро свяжется с вами."
    return send_whatsapp_message(msg)
