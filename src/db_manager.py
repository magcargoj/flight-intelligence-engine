import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "deals.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sent_deals 
                 (id INTEGER PRIMARY KEY, 
                  deal_id TEXT UNIQUE, 
                  sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def is_deal_sent(deal_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM sent_deals WHERE deal_id = ?", (deal_id,))
    result = c.fetchone()
    conn.close()
    return result is not None

def mark_deal_as_sent(deal_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO sent_deals (deal_id) VALUES (?)", (deal_id,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

if __name__ == "__main__":
    init_db()
