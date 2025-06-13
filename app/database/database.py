import sqlite3
from contextlib import contextmanager
import os

DATABASE_URL = "blog.db"

ADMIN_ROLE = 1
EDITOR_ROLE = 2

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    try:
        yield conn

    finally:
        conn.close()

def create_tables():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT UNIQUE NOT NULL,
            role INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        ''')
        conn.commit()

def init_database():
    create_tables()
    print("Database initialized successfully")


if __name__ == "__main__":
    # Can run this file directly to set up database
    init_database()

