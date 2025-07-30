import threading
import time
from src.signal_engine import scan_and_send_signals
from telegram_listener import run_bot

def start_signal_engine():
    print("🚀 Starting CryptoChamps signal engine (simple polling version)...")
    while True:
        scan_and_send_signals()
        time.sleep(1200)  # Scan every 20 minutes

def start_listener():
    print("✅ Telegram bot listener running (polling)...")
    run_bot()

if __name__ == "__main__":
    threading.Thread(target=start_listener, daemon=True).start()
    start_signal_engine()
