import os
import imapclient
import pyzmail36
from email_utils import send_email
from whatsapp_utils import send_whatsapp_message

EMAIL = os.environ.get("EMAIL_HOST_USER")
PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
IMAP_SERVER = "imap.zoho.com"
IMAP_PORT = 993

def check_emails_and_reply():
    try:
        with imapclient.IMAPClient(IMAP_SERVER, port=IMAP_PORT, ssl=True) as client:
            client.login(EMAIL, PASSWORD)
            client.select_folder("INBOX")

            messages = client.search(["UNSEEN"])
            for uid in messages:
                raw_message = client.fetch([uid], ["BODY[]", "FLAGS"])[uid][b"BODY[]"]
                message = pyzmail36.PyzMessage.factory(raw_message)

                subject = message.get_subject()
                from_name, from_email = message.get_addresses("from")[0]
                text = message.text_part.get_payload().decode(message.text_part.charset) if message.text_part else ""

                reply_text = f"Здравствуйте, {from_name or from_email},\nСпасибо за обращение. Мы получили ваше сообщение:\n{text}"
                send_email(from_name or from_email, from_email, reply_text, "N/A")
                send_whatsapp_message(reply_text)

        return {"status": "✅ Ответы отправлены"}
    except Exception as e:
        return {"error": str(e)}
