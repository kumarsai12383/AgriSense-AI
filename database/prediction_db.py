import sqlite3
from database.database import connect, DB_PATH


def save_prediction(
    crop,
    temperature,
    humidity,
    nitrogen,
    phosphorus,
    potassium,
    ph,
    rainfall,
    farmer_id=None
):
    """Save crop prediction with thread-safe WAL database connection."""
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO predictions (
            farmer_id,
            crop,
            temperature,
            humidity,
            nitrogen,
            phosphorus,
            potassium,
            ph,
            rainfall
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            farmer_id,
            crop,
            temperature,
            humidity,
            nitrogen,
            phosphorus,
            potassium,
            ph,
            rainfall
        )
    )

    conn.commit()
    conn.close()