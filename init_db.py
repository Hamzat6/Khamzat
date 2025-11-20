import sqlite3
from data.config import DATABASE_PATH

schema = '''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT,
    country TEXT,
    type TEXT,
    price REAL,
    description TEXT,
    images TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    product TEXT,
    comment TEXT,
    status TEXT DEFAULT 'new',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
'''

conn = sqlite3.connect(DATABASE_PATH)
cur = conn.cursor()
cur.executescript(schema)
conn.commit()
conn.close()
print('OK: DB created at', DATABASE_PATH)
