from loguru import logger
import os

# Папка для логов
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Общий лог
logger.add(
    os.path.join(LOG_DIR, "app.log"),
    rotation="00:00",        # ротация раз в сутки
    retention="14 days",     # хранить 14 дней
    compression="zip",       # архивировать старые
    level="INFO",
    enqueue=True,            # безопасно для многопоточности
    backtrace=False,
    diagnose=False,
)

# Отдельный лог для webhooks (не обязательно)
logger.add(
    os.path.join(LOG_DIR, "webhook.log"),
    filter=lambda r: r["extra"].get("channel") == "webhook",
    rotation="10 MB",
    retention="14 days",
    level="INFO",
    enqueue=True,
)

# Отдельный лог для имейл-поллера (не обязательно)
logger.add(
    os.path.join(LOG_DIR, "email_poller.log"),
    filter=lambda r: r["extra"].get("channel") == "email_poller",
    rotation="10 MB",
    retention="14 days",
    level="INFO",
    enqueue=True,
)

def get_logger(channel: str = None):
    if channel:
        return logger.bind(channel=channel)
    return logger
