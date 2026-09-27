import os
import sqlite3
from datetime import datetime

import streamlit as st
from PIL import Image
from google import genai
from google.genai import types


# =========================================================
# SETTINGS
# =========================================================

MODEL = os.environ.get(
    "GEMINI_VISION_MODEL",
    "gemini-3.8-flash"
)

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "database",
    "agrisense.db"
)


# =========================================================
# DATABASE
# =========================================================

def initialize_disease_database():
    """Create disease report table without touching existing data."""

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS disease_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER NOT NULL,
            crop TEXT,
            image_name TEXT,
            result TEXT NOT NULL,
            language TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (farmer_id)
                REFERENCES farmers(id)
        )
        """
    )

    conn.commit()
    conn.close()


# =========================================================
# FARM CONTEXT
# =========================================================

def get_latest_farm_context(farmer_id):
    """Get latest farm reading and crop prediction."""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    reading = conn.execute(
        """
        SELECT
            nitrogen,
            phosphorus,
            potassium,
            ph,
            temperature,
            humidity,
            rainfall,
            soil_moisture,
            source,
            date
        FROM farm_readings
        WHERE farmer_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (farmer_id,)
    ).fetchone()

    crop = conn.execute(
        """
        SELECT crop
        FROM predictions
        WHERE farmer_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (farmer_id,)
    ).fetchone()

    conn.close()

    return reading, crop


# =========================================================
# SAVE REPORT
# =========================================================

def save_disease_report(
    farmer_id,
    crop,
    image_name,
    result,
    language
):
    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        """
        INSERT INTO disease_reports
        (
            farmer_id,
            crop,
            image_name,
            result,
            language
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            farmer_id,
            crop,
            image_name,
            result,
            language
        )
    )

    conn.commit()
    conn.close()


# =========================================================
# IMAGE PREPARATION
# =========================================================

def prepare_image(uploaded_file):
    """Resize image to keep Gemini request reasonably small."""

    image = Image.open(uploaded_file).convert("RGB")

    max_size = 1600

    if max(image.size) > max_size:
        image.thumbnail(
            (max_size, max_size),
            Image.Resampling.LANCZOS
        )

    return image


# =========================================================
# AI DISEASE ANALYSIS
# =========================================================

def analyze_plant_image(
    image,
    language,
    crop,
    farm_reading
):
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing."
        )

    client = genai.Client(
        api_key=api_key
    )

    # -----------------------------------------------------
    # Farm context
    # -----------------------------------------------------

    if farm_reading:

        farm_context = f"""
Nitrogen: {farm_reading["nitrogen"]}
Phosphorus: {farm_reading["phosphorus"]}
Potassium: {farm_reading["potassium"]}
pH: {farm_reading["ph"]}
Temperature: {farm_reading["temperature"]} °C
Humidity: {farm_reading["humidity"]} %
Rainfall: {farm_reading["rainfall"]}
Soil moisture: {farm_reading["soil_moisture"]}
Data source: {farm_reading["source"]}
"""

    else:
        farm_context = "No farm measurements are available."

    crop_name = crop["crop"] if crop else "Unknown crop"

    # -----------------------------------------------------
    # Prompt
    # -----------------------------------------------------

    prompt = f"""
You are AgriSense AI, an AI farming assistant.

Analyze the uploaded plant/crop image.

Farmer's selected language:
{language}

Latest predicted crop:
{crop_name}

Latest available farm information:
{farm_context}

IMPORTANT SAFETY RULES:

1. Only analyze what can reasonably be supported by the image.
2. If the image is not clearly a plant, leaf, stem, fruit, or crop,
   say that the image cannot be assessed.
3. Do NOT claim a disease with certainty.
4. If visual evidence is insufficient, clearly say so.
5. Do not invent symptoms.
6. Do not invent farm measurements.
7. Do not recommend dangerous chemical use.
8. If mentioning pesticides or fungicides, advise the farmer to
   follow the product label and local agricultural guidance.
9. Give practical, simple advice for a farmer.
10. Answer in the farmer's selected language.
11. Keep the explanation easy to understand.

Return the answer using exactly these sections:

### 🌿 Plant / Crop
Identify the visible crop or plant if reasonably possible.

### 🦠 Likely Problem
Give the most likely visible problem.
If there is insufficient evidence, say:
"Unable to determine from this image."

### 📊 Visual Confidence
Use:
High / Medium / Low

This means confidence in the IMAGE ASSESSMENT,
not medical or agricultural diagnostic certainty.

### 🔎 What I Can See
List the visible symptoms or signs.

### 🚜 What You Should Do Now
Give practical immediate steps.

### 🛡️ Prevention
Give practical prevention steps.

### ⚠️ Important
Explain when the farmer should get help from a local
agriculture officer, agronomist, or plant specialist.

Do not pretend that you performed a laboratory diagnosis.
"""

    # -----------------------------------------------------
    # Convert image to JPEG bytes
    # -----------------------------------------------------

    from io import BytesIO

    buffer = BytesIO()

    image.save(
        buffer,
        format="JPEG",
        quality=85
    )

    image_bytes = buffer.getvalue()

    # -----------------------------------------------------
    # Gemini Vision
    # -----------------------------------------------------

    response = client.models.generate_content(
        model=MODEL,
        contents=[
            prompt,
            types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg"
            )
        ]
    )

    result = getattr(
        response,
        "text",
        None
    )

    if not result:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return result


# =========================================================
# PAGE
# =========================================================

def show_disease_detection():

    initialize_disease_database()

    farmer = st.session_state.get("farmer")

    if not farmer:
        st.warning(
            "Please login first."
        )
        return

    language = st.session_state.get(
        "selected_language",
        farmer.get(
            "language",
            "English"
        )
    )

    farmer_id = farmer["id"]

    st.title("🦠 Disease Detection")

    st.caption(
        f"👨‍🌾 {farmer['name']}  •  🌐 {language}"
    )

    st.markdown(
        """
        ### 🌱 Check Your Plant

        Take a clear photo of the affected leaf,
        plant, fruit or crop and let AgriSense AI
        examine the visible signs.
        """
    )

    st.info(
        "📸 For better results, take a clear photo "
        "in good light and keep the affected area visible."
    )

    # =====================================================
    # IMAGE SOURCE
    # =====================================================

    source = st.radio(
        "Choose photo method",
        [
            "📁 Upload Photo",
            "📷 Take Photo"
        ],
        horizontal=True
    )

    uploaded_file = None

    if source == "📁 Upload Photo":

        uploaded_file = st.file_uploader(
            "Upload plant photo",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp"
            ]
        )

    else:

        uploaded_file = st.camera_input(
            "Take a photo of your plant"
        )

    # =====================================================
    # ANALYSIS
    # =====================================================

    if uploaded_file:

        try:

            image = prepare_image(
                uploaded_file
            )

            st.image(
                image,
                caption="Selected plant image",
                use_container_width=True
            )

        except Exception as e:

            st.error(
                f"Could not read this image: {e}"
            )
            return

        st.markdown("---")

        if st.button(
            "🤖 Analyze Plant",
            use_container_width=True,
            type="primary"
        ):

            with st.spinner(
                "🤖 AgriSense AI is examining the plant..."
            ):

                try:

                    farm_reading, crop = (
                        get_latest_farm_context(
                            farmer_id
                        )
                    )

                    result = analyze_plant_image(
                        image=image,
                        language=language,
                        crop=crop,
                        farm_reading=farm_reading
                    )

                    crop_name = (
                        crop["crop"]
                        if crop
                        else "Unknown"
                    )

                    save_disease_report(
                        farmer_id=farmer_id,
                        crop=crop_name,
                        image_name=uploaded_file.name,
                        result=result,
                        language=language
                    )

                    st.session_state[
                        "latest_disease_result"
                    ] = result

                except Exception as e:

                    st.error(
                        f"AI analysis failed: {e}"
                    )

    # =====================================================
    # RESULT
    # =====================================================

    result = st.session_state.get(
        "latest_disease_result"
    )

    if result:

        st.markdown("---")

        st.success(
            "✅ Plant analysis completed"
        )

        st.markdown(result)

        st.warning(
            "⚠️ This is an AI image assessment, "
            "not a laboratory diagnosis. If the crop "
            "is seriously affected, consult a local "
            "agriculture expert."
        )