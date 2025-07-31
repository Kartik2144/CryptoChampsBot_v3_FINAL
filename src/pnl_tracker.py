import datetime

# Temporary in-memory log
trade_log = []

def log_trade(result, profit):
    trade_log.append({"result": result, "profit": profit})

def get_daily_pnl_summary():
    today = datetime.date.today()
    pnl_today = [trade for trade in trade_log if datetime.date.today() == today]
    wins = sum(1 for t in pnl_today if t['result'] == 'TP')
    losses = sum(1 for t in pnl_today if t['result'] == 'SL')
    profit = sum(t['profit'] for t in pnl_today)
    return f"📊 PnL Summary for {today}:\n✅ Wins: {wins}\n❌ Losses: {losses}\n💰 Profit: ${profit}"
