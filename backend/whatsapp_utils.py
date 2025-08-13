import os
import requests
from .logger import get_logger

log = get_logger("webhook")

WHATSAPP_TOKEN = os.environ.get("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.environ.get("WHATSAPP_PHONE_NUMBER_ID")

def send_whatsapp_text(to: str, text: str):
    """
    Отправляет текстовое сообщение адресату 'to' в рамках 24-часового окна.
    Не инициирует чат первым.
    """
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        log.error("WHATSAPP env vars are missing (token/phone id)")
        return {"error": "missing_env"}

    url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        j = r.json()
        if r.status_code >= 400:
            log.error(f"WA send error {r.status_code}: {j}")
        else:
            log.info(f"WA sent to={to} resp={j}")
        return j
    except Exception as e:
        log.exception(f"WA send exception: {e}")
        return {"error": str(e)}
