import sqlite3
from faker import Faker
import random
from datetime import datetime
from tqdm import tqdm

fake = Faker()
conn = sqlite3.connect("source.db")
cur = conn.cursor()

def setup_schema():
    cur.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            created_at TEXT
        );
    ''')
    cur.execute('''
        CREATE TABLE addresses (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            address TEXT,
            city TEXT,
            country TEXT,
            created_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    ''')
    cur.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            price REAL
        );
    ''')
    cur.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            created_at TEXT,
            status TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    ''')
    cur.execute('''
        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        );
    ''')
    cur.execute('''
        CREATE TABLE logs (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            message TEXT,
            level TEXT,
            timestamp TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    ''')
    conn.commit()

def insert_users(n):
    for i in tqdm(range(n), desc="Users"):
        cur.execute("INSERT INTO users (name, email, created_at) VALUES (?, ?, ?)", (
            fake.name(), fake.email(), datetime.now().isoformat()))
    conn.commit()

def insert_addresses(n, user_count):
    for i in tqdm(range(n), desc="Addresses"):
        cur.execute("INSERT INTO addresses (user_id, address, city, country, created_at) VALUES (?, ?, ?, ?, ?)", (
            random.randint(1, user_count),
            fake.address().replace('\n', ', '),
            fake.city(),
            fake.country(),
            datetime.now().isoformat()
        ))
    conn.commit()

def insert_products(n):
    for i in tqdm(range(n), desc="Products"):
        cur.execute("INSERT INTO products (name, description, price) VALUES (?, ?, ?)", (
            fake.word(), fake.text(max_nb_chars=200), round(random.uniform(5, 500), 2)))
    conn.commit()

def insert_orders(n, user_count):
    statuses = ["pending", "shipped", "cancelled", "delivered"]
    for i in tqdm(range(n), desc="Orders"):
        cur.execute("INSERT INTO orders (user_id, created_at, status) VALUES (?, ?, ?)", (
            random.randint(1, user_count),
            datetime.now().isoformat(),
            random.choice(statuses)))
    conn.commit()

def insert_order_items(n, order_count, product_count):
    for i in tqdm(range(n), desc="Order Items"):
        cur.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)", (
            random.randint(1, order_count),
            random.randint(1, product_count),
            random.randint(1, 10)))
    conn.commit()

def insert_logs(n, user_count):
    levels = ["INFO", "WARN", "DEBUG", "ERROR"]
    for i in tqdm(range(n), desc="Logs"):
        cur.execute("INSERT INTO logs (user_id, message, level, timestamp) VALUES (?, ?, ?, ?)", (
            random.randint(1, user_count),
            fake.sentence(),
            random.choice(levels),
            datetime.now().isoformat()))
    conn.commit()

if __name__ == '__main__':
    setup_schema()
    user_count = 5_000_000
    address_count = 5_000_000
    product_count = 100_000
    order_count = 10_000_000
    order_item_count = 20_000_000
    log_count = 15_000_000

    insert_users(user_count)
    insert_addresses(address_count, user_count)
    insert_products(product_count)
    insert_orders(order_count, user_count)
    insert_order_items(order_item_count, order_count, product_count)
    insert_logs(log_count, user_count)

    conn.close()

