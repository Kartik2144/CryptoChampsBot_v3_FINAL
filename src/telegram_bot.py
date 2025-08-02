import telebot
import threading
import os
import requests

TOKEN = os.getenv("YOUR_TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("YOUR_TELEGRAM_CHAT_ID")

requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")
print("✅ Webhook deleted (polling enabled)")

if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN is not set. Please add it to Railway environment variables.")
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

@bot.message_handler(commands=['testsignal'])
def test_signal(message):
    bot.reply_to(message, "✅ Bot is active and ready!")

def run_telegram_bot():
    threading.Thread(target=lambda: bot.polling(non_stop=True)).start()
