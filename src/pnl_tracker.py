# ✅ NEW FILE: src/pnl_tracker.py
import sqlite3
from datetime import datetime
import pytz

DB_FILE = "trades.db"
IST = pytz.timezone("Asia/Kolkata")

def track_trade(pair, direction, entry, sl, tp):
    """
    Track each trade for PnL simulation.
    Stores trade details into an SQLite DB for later PnL calculation.
    """
    conn = sqlite3.connect("pnl_tracker.db")
    cur = conn.cursor()
    
    def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pair TEXT,
                    direction TEXT,
                    entry REAL,
                    tp REAL,
                    sl REAL,
                    confidence INTEGER,
                    status TEXT,
                    created_at TEXT,
                    closed_at TEXT
                )''')
    conn.commit()
    conn.close()
    

    # ✅ Insert the trade into DB
    cur.execute("""
        INSERT INTO trades (timestamp, pair, direction, entry, sl, tp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), pair, direction, entry, sl, tp))

    conn.commit()
    conn.close()
    print(f"✅ Trade tracked: {pair} | {direction} | Entry {entry}")

def log_trade(pair, direction, entry, tp, sl, confidence):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO trades (pair, direction, entry, tp, sl, confidence, status, created_at) VALUES (?,?,?,?,?,?,?,?)",
              (pair, direction, entry, tp, sl, confidence, "open", datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def update_trade_status(pair, status):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE trades SET status=?, closed_at=? WHERE pair=? AND status='open'",
              (status, datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S"), pair))
    conn.commit()
    conn.close()

def save_trade(pair, direction, entry, tp, sl):
    conn = sqlite3.connect("pnl_data.db")
    c = conn.cursor()
    c.execute("INSERT INTO trades (pair, direction, entry, tp, sl, status) VALUES (?, ?, ?, ?, ?, ?)",
              (pair, direction, entry, tp, sl, "open"))
    conn.commit()
    conn.close()

def get_daily_pnl():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    today = datetime.now(IST).strftime("%Y-%m-%d")
    c.execute("SELECT status FROM trades WHERE created_at LIKE ?", (f"{today}%",))
    trades = c.fetchall()
    conn.close()

    wins = sum(1 for t in trades if t[0] == "hit-tp")
    losses = sum(1 for t in trades if t[0] == "hit-sl")

    pnl = (wins * 1.5) - (losses * 1.0)
    return {
        "wins": wins,
        "losses": losses,
        "pnl": pnl
    }
