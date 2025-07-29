from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from email_utils import send_email  # импорт

app = FastAPI()

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
def handle_email(data: EmailData):
    return send_email(data.name, data.email, data.message)
