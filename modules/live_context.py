from database.database import connect, DB_PATH


def get_farm_context(farmer_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            nitrogen,
            phosphorus,
            potassium,
            ph,
            temperature,
            humidity,
            rainfall,
            source,
            date
        FROM farm_readings
        WHERE farmer_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (farmer_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return "No farm data has been recorded yet."

    return f"""
Nitrogen: {row[0]}
Phosphorus: {row[1]}
Potassium: {row[2]}
Soil pH: {row[3]}
Temperature: {row[4]} °C
Humidity: {row[5]} %
Rainfall: {row[6]} mm
Data source: {row[7]}
Recorded: {row[8]}
"""


def get_crop_recommendation(farmer_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT crop
        FROM predictions
        WHERE farmer_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (farmer_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return "No ML crop recommendation available yet."