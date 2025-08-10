import telebot
import threading
import requests
from datetime import datetime
import pytz
import sqlite3
import os
import time
from src.signal_engine import scan_and_send_signals

TOKEN = os.getenv("YOUR_TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("YOUR_TELEGRAM_CHAT_ID")
DB_FILE = "trades.db"
requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")
print("✅ Webhook deleted (polling enabled)")
if not TOKEN:
    raise ValueError("❌ YOUR_TELEGRAM_BOT_TOKEN is not set. Please add it to Railway environment variables.")
bot = telebot.TeleBot(TOKEN)

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

# /forcescan command - manually scan for signals
@bot.message_handler(commands=['forcescan'])
def forcescan_command(message):
    if str(message.chat.id) != str(CHAT_ID):
        bot.reply_to(message, "🚫 Unauthorized")
        return
    bot.reply_to(message, "🔍 Manually starting trade signal scan...")
    scan_and_send_signals()
    bot.reply_to(message, "✅ Scan complete.")
    
# /pnl command - shows today's trades
@bot.message_handler(commands=['pnl'])
def pnl_command(message):
    try:
        today = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d")
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
            SELECT pair, direction, status, pnl
            FROM trades
            WHERE created_at LIKE ?
            ORDER BY created_at DESC
        """, (f"{today}%",))
        trades = c.fetchall()
        conn.close()

        if not trades:
            bot.reply_to(message, "📊 No trades recorded today.")
            return

        total_pnl = 0
        wins = 0
        losses = 0
        trade_lines = []

        for t in trades:
            pair, direction, status, pnl = t
            pnl = float(pnl or 0)
            total_pnl += pnl
            if status.lower() == "win":
                wins += 1
            elif status.lower() == "loss":
                losses += 1
            trade_lines.append(f"{pair} | {direction} | {status} | {pnl:.2f}")

        summary = (
            "📊 *Today's Trades:*\n"
            + "\n".join(trade_lines)
            + f"\n\n✅ Wins: {wins} | ❌ Losses: {losses} | 💰 Net PnL: {total_pnl:.2f}"
        )

        bot.reply_to(message, summary, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")


# Background thread to send PnL summary at midnight IST
def send_daily_pnl():
    while True:
        now = datetime.now(pytz.timezone("Asia/Kolkata"))
        if now.hour == 0 and now.minute == 0:
            try:
                today = now.strftime("%Y-%m-%d")
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute("""
                    SELECT pair, direction, status, pnl
                    FROM trades
                    WHERE created_at LIKE ?
                    ORDER BY created_at DESC
                """, (f"{today}%",))
                trades = c.fetchall()
                conn.close()

                if trades:
                    total_pnl = 0
                    wins = 0
                    losses = 0
                    trade_lines = []
                    for t in trades:
                        pair, direction, status, pnl = t
                        pnl = float(pnl or 0)
                        total_pnl += pnl
                        if status.lower() == "win":
                            wins += 1
                        elif status.lower() == "loss":
                            losses += 1
                        trade_lines.append(f"{pair} | {direction} | {status} | {pnl:.2f}")

                    summary = (
                        "📊 *Daily PnL Summary:*\n"
                        + "\n".join(trade_lines)
                        + f"\n\n✅ Wins: {wins} | ❌ Losses: {losses} | 💰 Net PnL: {total_pnl:.2f}"
                    )
                    bot.send_message(CHAT_ID, summary, parse_mode="Markdown")
            except Exception as e:
                bot.send_message(CHAT_ID, f"❌ Error sending daily PnL: {e}")
        # Sleep 60 seconds to avoid multiple sends in same minute
        time.sleep(60)

def run_telegram_bot():
    print("✅ Telegram bot listener started (polling mode)...")
# Start polling + PnL thread
threading.Thread(target=send_daily_pnl, daemon=True).start()
threading.Thread(target=lambda: bot.polling(non_stop=True)).start()
