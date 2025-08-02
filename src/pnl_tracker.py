from datetime import datetime

trades = []
pnl_log = []

def track_trade(pair, direction, entry, tp, sl):
    trade = {
        "pair": pair,
        "direction": direction,
        "entry": entry,
        "tp": tp,
        "sl": sl,
        "status": "OPEN"
    }
    trades.append(trade)
    print(f"📈 Tracking trade: {trade}")
