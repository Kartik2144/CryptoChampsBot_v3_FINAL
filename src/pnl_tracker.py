import sqlite3
from datetime import datetime

# ✅ define DB_FILE first
DB_FILE = "pnl_data.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pair TEXT,
            direction TEXT,
            entry REAL,
            tp REAL,
            sl REAL,
            status TEXT,
            pnl REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    try:
    c.execute("ALTER TABLE trades ADD COLUMN pnl REAL")
    conn.commit()
    print("✅ Added missing pnl column to trades table.")
    except sqlite3.OperationalError:
    # Column already exists
    pass
    conn.close()

def save_trade(pair, direction, entry, tp, sl):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO trades (pair, direction, entry, tp, sl, status) VALUES (?, ?, ?, ?, ?, ?)",
              (pair, direction, entry, tp, sl, "open"))
    conn.commit()
    conn.close()

def update_trade_status(trade_id, status):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE trades SET status = ? WHERE id = ?", (status, trade_id))
    conn.commit()
    conn.close()

def get_daily_pnl():
    """
    Returns today's PnL summary.
    Always returns a dict with keys: wins, losses, pnl.
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")

    # ✅ Fetch today's trades
    c.execute("SELECT pair, direction, status, pnl FROM trades WHERE created_at LIKE ? ORDER BY created_at DESC", (f"{today}%",))
    trades = c.fetchall()

    wins = sum(1 for t in trades if t[2] == 'TP')
    losses = sum(1 for t in trades if t[2] == 'SL')
    net_pnl = sum(t[3] for t in trades)

    # ✅ Get only the last 5 trades
    recent_trades = trades[:5]
    
    c.execute("SELECT status FROM trades WHERE created_at LIKE ?", (f"{today}%",))
    rows = c.fetchall()
    conn.close()

    wins = sum(1 for r in rows if r[0] == "TP")
    losses = sum(1 for r in rows if r[0] == "SL")

    total_trades = wins + losses
    pnl = ((wins - losses) / total_trades * 100) if total_trades > 0 else 0

    return {
        "wins": wins,
        "losses": losses,
        "net_pnl": round(net_pnl, 2),
        "recent_trades": recent_trades
    }

    for trade in trades:
        direction, entry, tp, sl, status = trade
        if status == "TP":
            tp_hits += 1
            total_pnl += abs(tp - entry)
        elif status == "SL":
            sl_hits += 1
            total_pnl -= abs(sl - entry)

    return {"date": today, "total_pnl": total_pnl, "tp_hits": tp_hits, "sl_hits": sl_hits}
