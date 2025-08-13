import os
import imapclient
import pyzmail36
import re
from .email_utils import send_email_reply
from .logger import get_logger

log = get_logger("email_poller")

IMAP_HOST = os.environ.get("IMAP_HOST", "imap.zoho.com")
IMAP_PORT = int(os.environ.get("IMAP_PORT", "993"))
IMAP_USER = os.environ.get("IMAP_USER", os.environ.get("EMAIL_HOST_USER"))
IMAP_PASS = os.environ.get("IMAP_PASS", os.environ.get("EMAIL_HOST_PASSWORD"))

_seen = set()  # дедупликация в рамках процесса

def _strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)

def check_emails_and_reply(limit: int = 20):
    """
    Проверяет UNSEEN письма и отвечает отправителю. Возвращает краткий статус.
    """
    if not all([IMAP_HOST, IMAP_PORT, IMAP_USER, IMAP_PASS]):
        log.error("IMAP env vars missing")
        return {"status": "IMAP env missing"}

    replied = 0
    try:
        with imapclient.IMAPClient(IMAP_HOST, port=IMAP_PORT, ssl=True) as client:
            client.login(IMAP_USER, IMAP_PASS)
            client.select_folder("INBOX")

            uids = client.search(["UNSEEN"])
            uids = uids[-limit:]

            for uid in uids:
                if uid in _seen:
                    continue

                raw = client.fetch([uid], ["RFC822"])[uid][b"RFC822"]
                msg = pyzmail36.PyzMessage.factory(raw)

                subject = msg.get_subject() or ""
                from_name, from_email = (msg.get_addresses("from") or [(None, None)])[0]

                text = ""
                if msg.text_part:
                    text = msg.text_part.get_payload().decode(msg.text_part.charset or "utf-8", errors="ignore")
                elif msg.html_part:
                    html = msg.html_part.get_payload().decode(msg.html_part.charset or "utf-8", errors="ignore")
                    text = _strip_tags(html)

                reply_subject = f"Re: {subject}" if subject else "Re: Ваше обращение"
                reply_body = (
                    f"Здравствуйте{', ' + from_name if from_name else ''}!\n\n"
                    "Спасибо за ваше письмо. Мы получили его со следующим содержанием:\n"
                    "----------------------------------------\n"
                    f"{text[:2000]}\n"
                    "----------------------------------------\n\n"
                    "Это автоответ. Специалист свяжется с вами при необходимости."
                )
                if from_email:
                    send_email_reply(from_email, reply_subject, reply_body)
                    log.info(f"Email reply sent to={from_email} subj={reply_subject}")
                    replied += 1

                _seen.add(uid)

        return {"status": f"✅ Ответов отправлено: {replied}"}
    except Exception as e:
        log.exception(f"IMAP poll exception: {e}")
        return {"status": "error", "error": str(e)}
