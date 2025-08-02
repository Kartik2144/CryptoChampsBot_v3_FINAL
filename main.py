import time
from src.signal_engine import scan_and_send_signals
from src.telegram_bot import run_telegram_bot

if __name__ == "__main__":
    print("🚀 CryptoChamps Hybrid Bot started...")
    run_telegram_bot()
    while True:
        scan_and_send_signals()
        time.sleep(3600)  # check every hour
