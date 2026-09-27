import sqlite3
import os

DB_PATH = "database/agrisense.db"


def connect():
    # Make sure database folder exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    return sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )


def initialize_database():

    conn = connect()
    cursor = conn.cursor()

    # ======================================
    # Farmers
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            language TEXT DEFAULT 'English',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ======================================
    # Farm Readings
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS farm_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER NOT NULL,
            nitrogen REAL,
            phosphorus REAL,
            potassium REAL,
            ph REAL,
            temperature REAL,
            humidity REAL,
            rainfall REAL,
            soil_moisture REAL,
            source TEXT DEFAULT 'manual',
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (farmer_id) REFERENCES farmers(id)
        )
    """)

    # ======================================
    # Upgrade OLD farm_readings table
    # ======================================

    cursor.execute("PRAGMA table_info(farm_readings)")
    farm_columns = [column[1] for column in cursor.fetchall()]

    # Add soil moisture to old database
    if "soil_moisture" not in farm_columns:
        cursor.execute("""
            ALTER TABLE farm_readings
            ADD COLUMN soil_moisture REAL
        """)

    # Add source if an older database doesn't have it
    if "source" not in farm_columns:
        cursor.execute("""
            ALTER TABLE farm_readings
            ADD COLUMN source TEXT DEFAULT 'manual'
        """)

    # ======================================
    # Predictions
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER,
            crop TEXT,
            temperature REAL,
            humidity REAL,
            nitrogen REAL,
            phosphorus REAL,
            potassium REAL,
            ph REAL,
            rainfall REAL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (farmer_id) REFERENCES farmers(id)
        )
    """)

    # ======================================
    # Upgrade OLD predictions table
    # ======================================

    cursor.execute("PRAGMA table_info(predictions)")
    prediction_columns = [column[1] for column in cursor.fetchall()]

    if "farmer_id" not in prediction_columns:
        cursor.execute("""
            ALTER TABLE predictions
            ADD COLUMN farmer_id INTEGER
        """)

    conn.commit()
    conn.close()


# ======================================
# Run database initialization
# ======================================

initialize_database()