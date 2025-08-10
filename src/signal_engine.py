import ccxt
import pandas as pd
from datetime import datetime
import time
from src.telegram_bot import test_signal
from src.pnl_tracker import save_trade
#from src.pnl_tracker import log_trade
exchange = ccxt.binance()

def fetch_ohlcv(symbol, timeframe="15m", limit=50):
    return exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

def hybrid_strategy(symbol):
    data = fetch_ohlcv(symbol)
    df = pd.DataFrame(data, columns=["time","open","high","low","close","volume"])
    df['EMA20'] = df['close'].ewm(span=20).mean()
    df['EMA50'] = df['close'].ewm(span=50).mean()from src.telegram_bot import send_signal
    df['RSI'] = 100 - (100 / (1 + df['close'].pct_change().rolling(14).mean()))
    
    last = df.iloc[-1]
    signal = None
    confidence = 0

    # Hybrid logic: EMA cross + RSI + volume filter
    if last['EMA20'] > last['EMA50'] and last['RSI'] > 55 and last['volume'] > df['volume'].mean():
        signal = "LONG"
        confidence = 90
    elif last['EMA20'] < last['EMA50'] and last['RSI'] < 45 and last['volume'] > df['volume'].mean():
        signal = "SHORT"
        confidence = 88

    if signal:
        entry = round(last['close'], 2)
        tp = entry * (1.015 if signal == "LONG" else 0.985)
        sl = entry * (0.985 if signal == "LONG" else 1.015)
        send_signal(symbol, direction, signal, entry, tp, sl, confidence)
        save_trade(symbol, direction, entry, tp, sl)
     #  send_signal(signal)
        log_trade(signal['pair'], signal['direction'], signal['entry'], signal['tp'], signal['sl'], signal['confidence'])

def scan_and_send_signals():
    top_pairs = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT"]
    for pair in top_pairs:
        try:
            hybrid_strategy(pair)
        except Exception as e:
            print(f"⚠️ Error scanning {pair}: {e}")
