import telebot
import os
from src.telegram_bot import send_signal, send_daily_pnl

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "✅ CryptoChamps Bot is LIVE! Use /testsignal to get a sample signal.")

@bot.message_handler(commands=['testsignal'])
def test_signal(message):
    sample_signal = {
        'strategy': 'Breakout',
        'pair': 'BTC/USDT',
        'direction': 'LONG',
        'entry': 29000,
        'sl': 28500,
        'tp': 30000,
        'confidence': 95
    }
    send_signal(sample_signal)
    bot.reply_to(message, "📡 Test signal sent! Check your Telegram group.")

@bot.message_handler(commands=['pnl'])
def pnl_command(message):
    pnl = send_daily_pnl()
    bot.reply_to(message, f"📊 Daily PnL: {pnl}")

def run_bot():
    print("🤖 Starting Telegram bot polling...")
    bot.infinity_polling()
