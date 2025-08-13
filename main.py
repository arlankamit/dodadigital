import os
import time
import threading
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from logger import get_logger
from whatsapp_utils import send_whatsapp_text
from imap_reader import check_emails_and_reply

load_dotenv()
log = get_logger()
webhook_log = get_logger("webhook")

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "doda_verify")
EMAIL_POLL_INTERVAL_SEC = int(os.getenv("EMAIL_POLL_INTERVAL_SEC", "30"))

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

# ---- WhatsApp Webhook VERIFY (GET) ----
@app.get("/webhook")
async def webhook_verify(request: Request):
    params = dict(request.query_params)
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        webhook_log.info(f"Webhook verified")
        return int(challenge) if challenge and str(challenge).isdigit() else (challenge or "")
    webhook_log.warning(f"Webhook verify failed: {params}")
    return {"error": "Verification failed"}

# ---- WhatsApp Webhook RECEIVE (POST) ----
@app.post("/webhook")
async def webhook_receive(request: Request):
    payload = await request.json()
    webhook_log.info(f"Incoming: {payload}")

    try:
        entry = payload["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        messages = value.get("messages", [])
        if not messages:
            return {"status": "ignored"}

        msg = messages[0]
        from_number = msg.get("from")
        text = (msg.get("text") or {}).get("body")

        if from_number and text:
            reply = f"Привет! Ты написал: {text}"
            send_whatsapp_text(from_number, reply)
    except Exception as e:
        webhook_log.exception(f"Webhook parse error: {e}")

    return {"status": "ok"}  # всегда 200, чтобы Meta не ретраила

# ---- Email poller (background) ----
def email_poll_worker():
    poller_log = get_logger("email_poller")
    poller_log.info(f"[email-poller] started, interval={EMAIL_POLL_INTERVAL_SEC}s")
    while True:
        try:
            check_emails_and_reply()
        except Exception as e:
            poller_log.exception(f"[email-poller] error: {e}")
        time.sleep(EMAIL_POLL_INTERVAL_SEC)

@app.on_event("startup")
def on_startup():
    t = threading.Thread(target=email_poll_worker, daemon=True)
    t.start()
    log.info("Service started")
