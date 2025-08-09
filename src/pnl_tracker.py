import sqlite3
from datetime import datetime

DB_FILE = "trades.db"

# ✅ Initialize DB & ensure pnl column exists
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Create trades table if it doesn't exist
    c.execute('''
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
    ''')

    # ✅ Try to add pnl column if it doesn’t exist already
    try:
        c.execute("ALTER TABLE trades ADD COLUMN pnl REAL")
        conn.commit()
        print("✅ Added missing pnl column to trades table.")
    except sqlite3.OperationalError:
        pass  # Column already exists – ignore

    conn.commit()
    conn.close()


# ✅ Save trade entry
def save_trade(pair, direction, entry, tp, sl):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO trades (pair, direction, entry, tp, sl, status) VALUES (?, ?, ?, ?, ?, ?)",
        (pair, direction, entry, tp, sl, 'open')
    )
    conn.commit()
    conn.close()


# ✅ Update trade when closed (hit TP or SL)
def update_trade_status(trade_id, status, pnl_value):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "UPDATE trades SET status = ?, pnl = ? WHERE id = ?",
        (status, pnl_value, trade_id)
    )
    conn.commit()
    conn.close()


# ✅ Fetch daily PnL summary + recent trades (ONLY TODAY’S TRADES)
def get_daily_pnl():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    c.execute(
        "SELECT pair, direction, status, pnl FROM trades WHERE created_at LIKE ? ORDER BY created_at DESC",
        (f"{today}%",)
    )
    rows = c.fetchall()
    conn.close()

    wins = sum(1 for r in rows if r[2] == 'tp')
    losses = sum(1 for r in rows if r[2] == 'sl')
    net_pnl = sum(r[3] for r in rows if r[3] is not None)

    recent_trades = [
        {"pair": r[0], "direction": r[1], "status": r[2], "pnl": r[3]} for r in rows
    ]

    return {
        "wins": wins,
        "losses": losses,
        "net_pnl": round(net_pnl, 2),
        "recent_trades": recent_trades
    }

# ✅ Initialize DB on import
init_db()
