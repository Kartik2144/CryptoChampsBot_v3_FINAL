import telebot
import threading
import os
import requests
from src.pnl_tracker import get_daily_pnl
from src.pnl_tracker import save_trade
from datetime import datetime

TOKEN = os.getenv("YOUR_TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("YOUR_TELEGRAM_CHAT_ID")

requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")
print("✅ Webhook deleted (polling enabled)")

if not TOKEN:
    raise ValueError("❌ YOUR_TELEGRAM_BOT_TOKEN is not set. Please add it to Railway environment variables.")
bot = telebot.TeleBot(TOKEN)

def send_signal(pair, direction, entry, tp, sl, confidence):
    msg = f"📢 Signal Alert ({direction})\n\n" \
          f"🔹 Pair: {pair}\n" \
          f"🎯 Entry: {entry}\n" \
          f"✅ TP: {tp}\n" \
          f"⛔ SL: {sl}\n" \
          f"📊 Confidence: {confidence}%"
    bot.send_message(CHAT_ID, msg)
    print(f"✅ Signal sent: {signal['pair']}")
    save_trade(signal['pair'], signal['direction'], signal['entry'], signal['tp'], signal['sl'])

# ✅ Command: /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(
        message,
        "👋 <b>Welcome to CryptoChamps Hybrid Bot!</b>\n\n"
        "Use the following commands:\n"
        "📊 /pnl - Show today’s simulated PnL\n"
        "🚀 /testsignal - Send a sample signal\n",
        parse_mode="HTML"
    )
@bot.message_handler(commands=['testsignal'])
def test_signal(message):
    bot.reply_to(message, "✅ Bot is active and ready!")

@bot.message_handler(commands=['pnl'])
def pnl_command(message):
    pnl_data = get_daily_pnl()

   # ✅ Basic summary
    summary_msg = (
        f"📊 <b>Daily PnL Report ({datetime.now().strftime('%Y-%m-%d')})</b>\n\n"
        f"✅ Wins: <b>{pnl_data['wins']}</b>\n"
        f"❌ Losses: <b>{pnl_data['losses']}</b>\n"
        f"💰 Net PnL: <b>${pnl_data['net_pnl']}</b>\n\n"
    )

    # ✅ Add recent trades if available
    if pnl_data["recent_trades"]:
        summary_msg += "<b>📜 Recent Trades:</b>\n"
        for trade in pnl_data["recent_trades"]:
            summary_msg += f"{trade}\n"
    else:
        summary_msg += "No trades today yet."

    bot.reply_to(message, summary_msg, parse_mode="HTML")

def run_telegram_bot():
    print("✅ Telegram bot listener started (polling mode)...")
    threading.Thread(target=lambda: bot.polling(non_stop=True)).start()
