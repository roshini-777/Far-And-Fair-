import os
import sqlite3
import json

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stays.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            city TEXT NOT NULL,
            address TEXT NOT NULL,
            daily_cost INTEGER NOT NULL,
            deposit INTEGER NOT NULL,
            rating REAL NOT NULL,
            reviews_count INTEGER NOT NULL,
            max_persons INTEGER NOT NULL,
            food_included INTEGER NOT NULL,
            wifi INTEGER NOT NULL,
            gym INTEGER NOT NULL,
            laundry INTEGER NOT NULL,
            security INTEGER NOT NULL,
            study_room INTEGER NOT NULL,
            lat REAL NOT NULL,
            lng REAL NOT NULL,
            images TEXT NOT NULL,
            description TEXT NOT NULL,
            reviews_json TEXT NOT NULL,
            attractions_json TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def fetch_all_stays():
    init_db()
    conn = get_connection()
    rows = conn.execute("SELECT * FROM stays").fetchall()
    conn.close()
    return [_row_to_dict(r) for r in rows]


def fetch_stay_by_id(stay_id):
    init_db()
    conn = get_connection()
    row = conn.execute("SELECT * FROM stays WHERE id = ?", (stay_id,)).fetchone()
    conn.close()
    return _row_to_dict(row) if row else None


def _row_to_dict(row):
    d = dict(row)
    d["food_included"] = bool(d["food_included"])
    d["wifi"] = bool(d["wifi"])
    d["gym"] = bool(d["gym"])
    d["laundry"] = bool(d["laundry"])
    d["security"] = bool(d["security"])
    d["study_room"] = bool(d["study_room"])
    d["images"] = json.loads(d["images"])
    d["reviews"] = json.loads(d["reviews_json"])
    d["attractions"] = json.loads(d["attractions_json"])
    del d["reviews_json"]
    del d["attractions_json"]
    return d
