import os
import shutil
import datetime as dt
import requests
from dotenv import load_dotenv
from logger import get_logger

log = get_logger()

# Загружаем .env из папки backend
load_dotenv()

APP_ID = os.getenv("META_APP_ID")              # App ID
APP_SECRET = os.getenv("META_APP_SECRET")      # App Secret
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")  # Текущий токен

if not all([APP_ID, APP_SECRET, ACCESS_TOKEN]):
    log.error("❌ В .env отсутствуют META_APP_ID, META_APP_SECRET или WHATSAPP_ACCESS_TOKEN")
    raise SystemExit(1)

url = "https://graph.facebook.com/v21.0/oauth_access_token"
# Исправленный путь: /oauth/access_token
url = "https://graph.facebook.com/v21.0/oauth/access_token"
params = {
    "grant_type": "fb_exchange_token",
    "client_id": APP_ID,
    "client_secret": APP_SECRET,
    "fb_exchange_token": ACCESS_TOKEN
}

log.info("🔄 Обновляем токен...")
resp = requests.get(url, params=params, timeout=30)
data = resp.json()

if "access_token" not in data:
    log.error(f"❌ Ошибка при получении токена: {data}")
    raise SystemExit(1)

new_token = data["access_token"]
expires_in = data.get("expires_in", 0)  # в секундах
days_left = expires_in // 86400

# Бэкап .env
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copyfile(env_path, env_path + f".bak_{ts}")

# Перезапись .env
with open(env_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(env_path, "w", encoding="utf-8") as f:
    found = False
    for line in lines:
        if line.startswith("WHATSAPP_ACCESS_TOKEN="):
            f.write(f"WHATSAPP_ACCESS_TOKEN={new_token}\n")
            found = True
        else:
            f.write(line)
    if not found:
        f.write(f"WHATSAPP_ACCESS_TOKEN={new_token}\n")

log.info(f"✅ Новый токен сохранён в .env, действует ~{days_left} дней")
