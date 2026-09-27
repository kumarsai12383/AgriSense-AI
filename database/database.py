import sqlite3
import os

# Resilient absolute path regardless of current working directory or hosting environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "agrisense.db")


def connect():
    """Establish a robust, thread-safe connection with WAL mode enabled for multi-device concurrency."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(
        DB_PATH,
        timeout=30.0,
        check_same_thread=False
    )
    conn.row_factory = sqlite3.Row

    # Performance & Concurrency Pragmas
    try:
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA busy_timeout = 10000;")
        conn.execute("PRAGMA foreign_keys = ON;")
    except Exception:
        pass

    return conn


def initialize_database():
    """Auto-bootstrap all required tables, columns, and indices for flawless multi-device operation."""
    conn = connect()
    cursor = conn.cursor()

    # ======================================
    # 1. Farmers Table
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
    # 2. Farm Readings Table
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

    # Check & migrate any missing columns in farm_readings
    cursor.execute("PRAGMA table_info(farm_readings)")
    farm_columns = [col[1] for col in cursor.fetchall()]

    if "soil_moisture" not in farm_columns:
        cursor.execute("ALTER TABLE farm_readings ADD COLUMN soil_moisture REAL")
    if "source" not in farm_columns:
        cursor.execute("ALTER TABLE farm_readings ADD COLUMN source TEXT DEFAULT 'manual'")

    # ======================================
    # 3. Crop Predictions Table
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

    # Check & migrate any missing columns in predictions
    cursor.execute("PRAGMA table_info(predictions)")
    pred_columns = [col[1] for col in cursor.fetchall()]

    if "farmer_id" not in pred_columns:
        cursor.execute("ALTER TABLE predictions ADD COLUMN farmer_id INTEGER")

    # ======================================
    # 4. Disease Reports Table
    # ======================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disease_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER NOT NULL,
            crop TEXT,
            image_name TEXT,
            result TEXT NOT NULL,
            language TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (farmer_id) REFERENCES farmers(id)
        )
    """)

    # ======================================
    # 5. Performance Indices
    # ======================================
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_farmers_phone ON farmers(phone)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_farm_readings_farmer_date ON farm_readings(farmer_id, date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_predictions_farmer_date ON predictions(farmer_id, date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_disease_reports_farmer ON disease_reports(farmer_id, date)")

    conn.commit()
    conn.close()


def get_database_health():
    """Return live database diagnostic health status and row counts."""
    try:
        conn = connect()
        cursor = conn.cursor()

        farmers_count = cursor.execute("SELECT COUNT(*) FROM farmers").fetchone()[0]
        readings_count = cursor.execute("SELECT COUNT(*) FROM farm_readings").fetchone()[0]
        pred_count = cursor.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]
        disease_count = cursor.execute("SELECT COUNT(*) FROM disease_reports").fetchone()[0]

        file_size_bytes = os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
        conn.close()

        return {
            "status": "healthy",
            "db_path": DB_PATH,
            "size_kb": round(file_size_bytes / 1024, 2),
            "tables": {
                "farmers": farmers_count,
                "farm_readings": readings_count,
                "predictions": pred_count,
                "disease_reports": disease_count
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "db_path": DB_PATH
        }


# Auto-initialize on module load
initialize_database()