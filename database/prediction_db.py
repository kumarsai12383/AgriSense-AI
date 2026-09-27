import sqlite3


DB_PATH = "database/agrisense.db"


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

    conn = sqlite3.connect(DB_PATH)

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