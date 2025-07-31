import threading
import time
import os
from src.signal_engine import scan_and_send_signals
from telegram_listener import run_bot

if not os.getenv("TELEGRAM_BOT_TOKEN"):
    raise RuntimeError("🚨 TELEGRAM_BOT_TOKEN missing — set it on Railway!")
    
def start_listener():
    print("✅ Telegram bot listener running...")
    run_bot()

if __name__ == "__main__":
    print("🚀 CryptoChampsBot_v4 starting...")

    listener_thread = threading.Thread(target=start_listener)
    listener_thread.start()

    print("📡 Starting signal engine...")
    while True:
        scan_and_send_signals()
        time.sleep(1800)  # Scan every 30 minutes
