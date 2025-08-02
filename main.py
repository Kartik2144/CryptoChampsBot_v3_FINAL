import time
from src.signal_engine import scan_and_send_signals
from src.telegram_bot import run_telegram_bot
import os
import schedule, time, threading
from src.pnl_tracker import get_daily_pnl
from src.telegram_bot import bot

if not os.getenv("YOUR_TELEGRAM_BOT_TOKEN"):
    raise RuntimeError("🚨 YOUR_TELEGRAM_BOT_TOKEN missing — set it on Railway!")
    
if __name__ == "__main__":
    print("🚀 CryptoChamps Hybrid Bot started...")
    run_telegram_bot()
    while True:
        scan_and_send_signals()
        time.sleep(3600)  # check every hour

def send_daily_pnl():
    pnl_data = get_daily_pnl()
    msg = (f"📊 *Daily PnL Summary (Auto)*\n"
           f"✅ Wins: {pnl_data['wins']}\n"
           f"❌ Losses: {pnl_data['losses']}\n"
           f"💰 PnL: {pnl_data['pnl']}R (simulated)\n")
    bot.send_message(YOUR_TELEGRAM_CHAT_ID, msg, parse_mode="Markdown")

def schedule_pnl():
    schedule.every().day.at("23:59").do(send_daily_pnl)
    while True:
        schedule.run_pending()
        time.sleep(60)

# Start scheduler in a thread
    threading.Thread(target=schedule_pnl).start()
