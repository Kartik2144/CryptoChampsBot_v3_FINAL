import telebot
import threading

TOKEN = "TELEGRAM_BOT_TOKEN"
CHAT_ID = "TELEGRAM_CHAT_ID"
bot = telebot.TeleBot(TOKEN)

def send_signal(pair, direction, entry, tp, sl, confidence):
    msg = f"📢 Signal Alert ({direction})\n\n" \
          f"🔹 Pair: {pair}\n" \
          f"🎯 Entry: {entry}\n" \
          f"✅ TP: {tp}\n" \
          f"⛔ SL: {sl}\n" \
          f"📊 Confidence: {confidence}%"
    bot.send_message(CHAT_ID, msg)

@bot.message_handler(commands=['testsignal'])
def test_signal(message):
    bot.reply_to(message, "✅ Bot is active and ready!")

def run_telegram_bot():
    threading.Thread(target=lambda: bot.polling(non_stop=True)).start()
