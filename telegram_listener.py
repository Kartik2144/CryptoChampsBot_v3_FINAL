import telebot
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ CryptoChampsBot is live! Use /testsignal to see a demo signal.")

@bot.message_handler(commands=['testsignal'])
def test_signal(message):
    msg = "📊 TEST SIGNAL\nPair: BTC/USDT\nDirection: LONG (20x)\nEntry: 29000\nSL: 28500\nTP: 30000\nStrategy: Breakout\nConfidence: 92%"
    bot.send_message(CHAT_ID, msg)

@bot.message_handler(commands=['pnl'])
def pnl_summary(message):
    from src.pnl_tracker import get_daily_pnl_summary
    summary = get_daily_pnl_summary()
    bot.reply_to(message, summary)

def run_bot():
    bot.polling()
