from faker import Faker
import sqlite3
from tqdm import tqdm
import random

fake = Faker()
conn = sqlite3.connect("billion_rows.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    age INTEGER,
    created_at TEXT
);
""")
conn.commit()

BATCH = 10_000
TOTAL = 1_000_000_000

for _ in tqdm(range(0, TOTAL, BATCH)):
    data = [
        (fake.name(), fake.email(), random.randint(18, 80), fake.date_time().isoformat())
        for _ in range(BATCH)
    ]
    cur.executemany("INSERT INTO users (name, email, age, created_at) VALUES (?, ?, ?, ?);", data)
    conn.commit()

