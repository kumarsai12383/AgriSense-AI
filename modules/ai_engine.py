import os
import sqlite3
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import streamlit as st
from google import genai


from database.database import connect, DB_PATH
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.1-flash-lite")


# =========================================================
# Gemini Client
# =========================================================

def get_gemini_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        try:
            if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
                api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            pass

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Please set GEMINI_API_KEY in your environment or Streamlit Secrets."
        )

    return genai.Client(
        api_key=api_key
    )


# =========================================================
# Latest Farm Data
# =========================================================

def get_latest_farm_data(farmer_id):
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
        return None

    return {
        "nitrogen": row[0],
        "phosphorus": row[1],
        "potassium": row[2],
        "ph": row[3],
        "temperature": row[4],
        "humidity": row[5],
        "rainfall": row[6],
        "source": row[7],
        "date": row[8],
    }


# =========================================================
# Latest ML Crop Prediction
# =========================================================

def get_latest_crop_prediction(farmer_id):
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

    return None


# =========================================================
# Farm Context Builder
# =========================================================

def build_farm_context(farmer_id):

    farm_data = get_latest_farm_data(
        farmer_id
    )

    recommended_crop = get_latest_crop_prediction(
        farmer_id
    )

    # -----------------------------------------
    # Farm data
    # -----------------------------------------

    if farm_data:

        farm_context = f"""
Nitrogen: {farm_data['nitrogen']}
Phosphorus: {farm_data['phosphorus']}
Potassium: {farm_data['potassium']}
Soil pH: {farm_data['ph']}
Temperature: {farm_data['temperature']} °C
Humidity: {farm_data['humidity']} %
Rainfall: {farm_data['rainfall']} mm
Data source: {farm_data['source']}
Recorded: {farm_data['date']}
"""

    else:

        farm_context = (
            "No farm data has been recorded yet."
        )

    # -----------------------------------------
    # ML crop recommendation
    # -----------------------------------------

    if recommended_crop:

        crop_context = recommended_crop

    else:

        crop_context = (
            "No ML crop recommendation "
            "is available yet."
        )

    return farm_context, crop_context


# =========================================================
# Conversation Memory
# =========================================================

def get_conversation_key(farmer_id):

    return f"gemini_previous_interaction_{farmer_id}"


# =========================================================
# AgriSense AI
# =========================================================

def ask_agrisense_stream(
    farmer_id,
    question,
    language
):
    """
    Generator that yields real-time streaming response tokens.
    Provides sub-second perceived response latency.
    """
    if not question or not question.strip():
        raise ValueError("Please enter a farming question.")

    question = question.strip()
    client = get_gemini_client()
    farm_context, crop_context = build_farm_context(farmer_id)

    prompt = f"""You are AgriSense AI, an expert, friendly agricultural assistant for Indian farmers.

Farmer ID: {farmer_id} | Language: {language}
Latest Farm Data:
{farm_context}
Recommended Crop: {crop_context}

Farmer's Question: {question}

Instructions:
- Respond in {language} in a warm, practical, farmer-friendly tone.
- Use the farmer's real soil/weather data when relevant.
- Keep the response clear, structured (using bullet points), actionable, and concise.
"""

    candidate_models = ["gemini-3.1-flash-lite", "gemini-3.5-flash-lite", "gemini-flash-lite-latest", "gemini-3.8-flash", "gemini-3.7-flash"]
    # Deduplicate while preserving order
    seen = set()
    models_to_try = [m for m in candidate_models if m and not (m in seen or seen.add(m))]

    last_err = None

    for candidate in models_to_try:
        try:
            stream = client.models.generate_content_stream(
                model=candidate,
                contents=prompt
            )
            has_yielded = False
            for chunk in stream:
                if chunk.text:
                    has_yielded = True
                    yield chunk.text
            if has_yielded:
                return
        except Exception as e:
            last_err = e
            try:
                interaction = client.interactions.create(
                    model=candidate,
                    input=prompt
                )
                answer = getattr(interaction, "output_text", None)
                if answer:
                    for w in answer.split(" "):
                        yield w + " "
                    return
            except Exception as e2:
                last_err = e2

    raise RuntimeError(f"AgriSense AI Error: {last_err or 'No response from AI model'}")


def ask_agrisense(
    farmer_id,
    question,
    language
):
    if not question or not question.strip():
        raise ValueError("Please enter a farming question.")

    chunks = list(ask_agrisense_stream(farmer_id, question, language))
    return "".join(chunks)