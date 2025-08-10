import ccxt
import pandas as pd
from datetime import datetime
import time
from src.telegram_bot import test_signal
from src.pnl_tracker import save_trade
#from src.pnl_tracker import log_trade
exchange = ccxt.binance()

def fetch_ohlcv(pair, timeframe="15m", limit=50):
    return exchange.fetch_ohlcv(pair, timeframe=timeframe, limit=limit)

def hybrid_strategy(pair):
    data = fetch_ohlcv(pair)
    df = pd.DataFrame(data, columns=["time","open","high","low","close","volume"])
    df['EMA20'] = df['close'].ewm(span=20).mean()
    df['EMA50'] = df['close'].ewm(span=50).mean()
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
        send_signal(pair, direction, signal, entry, tp, sl, confidence)
        save_trade(pair, direction, entry, tp, sl)
     #  send_signal(signal)
        log_trade(signal['pair'], signal['direction'], signal['entry'], signal['tp'], signal['sl'], signal['confidence'])

def scan_and_send_signals(return_results=False):
    signals_found = []
    
    # Your scanning logic here...
    # Instead of directly sending Telegram messages,
    # store them in signals_found list like:
    # signals_found.append(f"📈 {pair} {direction}\nEntry: {entry}\nSL: {sl}\nTP: {tp}")
    
    if return_results:
        return signals_found
    
    # Old behavior - send signals via send_signal()
    for sig in signals_found:
        send_signal(sig)
