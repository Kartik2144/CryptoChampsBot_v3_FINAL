What’s inside?
main.py → Runs both Telegram bot (polling) & signal engine.

telegram_listener.py → Handles /start, /testsignal, /pnl commands.

src/signal_engine.py → Scans top 25 Binance pairs & generates Breakout & Reversal signals.

src/telegram_bot.py → Sends formatted signals to Telegram.

src/pnl_tracker.py → Keeps track of trades for PnL summary.

requirements.txt → Dependencies (ccxt, telebot, flask).
