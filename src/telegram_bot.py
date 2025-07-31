import os
import telebot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN is not set. Please add it to Railway environment variables.")
bot = telebot.TeleBot(TOKEN)

def send_signal(signal):
    msg = f"🚀 CryptoChamps Signal ({signal['strategy']})\n\n" \
          f"🔹 Pair: {signal['pair']}\n" \
          f"📍 Direction: {signal['direction']} (20x)\n" \
          f"🎯 Entry: {signal['entry']}\n" \
          f"⛔ Stoploss: {signal['sl']}\n" \
          f"✅ Target: {signal['tp']}\n" \
          f"📈 Risk-Reward: 1:1.5\n" \
          f"🤖 Confidence: {signal['confidence']}%"
    bot.send_message(CHAT_ID, msg)
    print(f"✅ Signal sent: {signal['pair']}")
    
# def send_daily_pnl(summary):
 #   bot.send_message(CHAT_ID, f"📊 Daily PnL Report:\n{summary}")
