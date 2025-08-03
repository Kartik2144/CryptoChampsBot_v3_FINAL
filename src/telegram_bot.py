import telebot
import threading
import os
import requests
from src.pnl_tracker import get_daily_pnl
from src.pnl_tracker import save_trade

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


@bot.message_handler(commands=['testsignal'])
def test_signal(message):
    bot.reply_to(message, "✅ Bot is active and ready!")

@bot.message_handler(commands=['pnl'])
def pnl_command(message):
    pnl_data = get_daily_pnl()

    # ✅ Build the response
    response = (
        f"📊 *Daily PnL Summary*\n"
        f"✅ Wins: {pnl_data['wins']} | ❌ Losses: {pnl_data['losses']}\n"
        f"💰 Net PnL: ${pnl_data['net_pnl']}\n\n"
        f"📝 *Last 5 Trades Today:*\n"
    )

    if pnl_data['recent_trades']:
        for i, trade in enumerate(pnl_data['recent_trades'], start=1):
            pair, direction, status, pnl = trade
            status_emoji = "✅" if status == "TP" else "❌"
            response += f"{i}. {pair} – {direction} – {status_emoji} ({pnl}%)\n"
    else:
        response += "No trades today yet."

    bot.send_message(message.chat.id, response, parse_mode="Markdown")


def run_telegram_bot():
    threading.Thread(target=lambda: bot.polling(non_stop=True)).start()
