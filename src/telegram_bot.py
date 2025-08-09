import telebot
import threading
from datetime import datetime
import pytz
import sqlite3
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DB_FILE = "trades.db"

bot = telebot.TeleBot(TOKEN)

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


# Start polling + PnL thread
threading.Thread(target=send_daily_pnl, daemon=True).start()
threading.Thread(target=lambda: bot.polling(non_stop=True)).start()
