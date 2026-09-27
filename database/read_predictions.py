import sqlite3
import pandas as pd


DB_PATH = "database/agrisense.db"


def load_predictions(farmer_id):

    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            id,
            crop,
            temperature,
            humidity,
            nitrogen,
            phosphorus,
            potassium,
            ph,
            rainfall,
            date
        FROM predictions
        WHERE farmer_id = ?
        ORDER BY date DESC
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(farmer_id,)
    )

    conn.close()

    return df