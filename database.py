import sqlite3
from data.config import DATABASE_PATH


def _connect():
    return sqlite3.connect(DATABASE_PATH)


def add_product(name, category, subcategory, country, ptype, price, description, images_csv):
    conn = _connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO products
                (name, category, subcategory, country, type, price, description, images)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (name, category, subcategory, country, ptype, price, description, images_csv))
    conn.commit()
    conn.close()


def list_products(category=None):
    conn = _connect()
    cur = conn.cursor()
    if category:
        cur.execute("SELECT id, name, category, subcategory, country, type, price, description, images FROM products WHERE category=?", (category,))
    else:
        cur.execute("SELECT id, name, category, subcategory, country, type, price, description, images FROM products")
    rows = cur.fetchall()
    conn.close()
    return rows


def add_order(name, phone, product, comment):
    conn = _connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (name, phone, product, comment) VALUES (?, ?, ?, ?)", (name, phone, product, comment))
    conn.commit()
    conn.close()
