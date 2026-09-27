import sqlite3
from database.database import connect, DB_PATH


def get_connection():
    return connect()


def create_farmer_table():
    """Ensure farmers table exists."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            language TEXT DEFAULT 'English',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def get_or_create_farmer(name, phone):
    """Retrieve existing farmer by phone or create a new profile safely."""
    create_farmer_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, phone, language FROM farmers WHERE phone = ?",
        (phone,)
    )

    farmer = cursor.fetchone()

    if farmer:
        conn.close()
        return {
            "id": farmer["id"] if isinstance(farmer, sqlite3.Row) else farmer[0],
            "name": farmer["name"] if isinstance(farmer, sqlite3.Row) else farmer[1],
            "phone": farmer["phone"] if isinstance(farmer, sqlite3.Row) else farmer[2],
            "language": farmer["language"] if isinstance(farmer, sqlite3.Row) else farmer[3]
        }

    cursor.execute(
        """
        INSERT INTO farmers (name, phone)
        VALUES (?, ?)
        """,
        (name, phone)
    )

    conn.commit()
    farmer_id = cursor.lastrowid
    conn.close()

    return {
        "id": farmer_id,
        "name": name,
        "phone": phone,
        "language": "English"
    }


def update_farmer_language(farmer_id, language):
    """Update preferred language for a farmer in SQLite DB."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE farmers SET language = ? WHERE id = ?",
            (language, farmer_id)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error updating farmer language:", e)
        return False