import os
import requests


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_message(text: str) -> bool:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        print("[telegram] Message sent successfully.")
        return True
    except Exception as e:
        print(f"[telegram] Failed to send message: {e}")
        return False


def send_error_alert(error: str) -> None:
    msg = f"⚠️ *Stock Agent Error*\n\n`{error[:300]}`"
    send_message(msg)
