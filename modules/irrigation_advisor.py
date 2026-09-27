import sqlite3
import streamlit as st
from datetime import datetime

DB_PATH = "database/agrisense.db"


def get_latest_farm_reading(farmer_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM farm_readings
            WHERE farmer_id = ?
            ORDER BY id DESC
            LIMIT 1
        """, (farmer_id,))

        row = cursor.fetchone()
        return dict(row) if row else None

    finally:
        conn.close()


def irrigation_recommendation(reading):
    """
    Generate irrigation advice from the latest farm reading.

    Soil moisture is preferred when available.
    Other environmental values are used as supporting information.
    """

    moisture = reading.get("soil_moisture")
    temperature = reading.get("temperature")
    humidity = reading.get("humidity")
    rainfall = reading.get("rainfall")

    reasons = []

    # --------------------------------------------------
    # Soil moisture based recommendation
    # --------------------------------------------------

    if moisture is not None:

        if moisture < 20:
            status = "🔴 Irrigation Recommended"
            message = "Your soil is very dry. Irrigation is recommended."
            reasons.append("Soil moisture is very low.")

        elif moisture < 35:
            status = "🟡 Irrigate Soon"
            message = "The soil is becoming dry. Plan irrigation soon."
            reasons.append("Soil moisture is getting low.")

        elif moisture <= 70:
            status = "🟢 No Immediate Irrigation"
            message = "Soil moisture is currently sufficient."
            reasons.append("Soil has enough moisture.")

        else:
            status = "🔵 Soil Is Wet"
            message = "The soil is already quite wet. Avoid unnecessary irrigation."
            reasons.append("Soil moisture is high.")

    else:
        # --------------------------------------------------
        # Fallback when moisture sensor is unavailable
        # --------------------------------------------------

        score = 0

        if temperature is not None and temperature >= 30:
            score += 2
            reasons.append("Temperature is high.")

        elif temperature is not None and temperature >= 25:
            score += 1
            reasons.append("Temperature is moderately high.")

        if humidity is not None and humidity < 50:
            score += 2
            reasons.append("Air humidity is low.")

        elif humidity is not None and humidity < 65:
            score += 1
            reasons.append("Air humidity is moderate.")

        if rainfall is not None:

            if rainfall >= 150:
                score -= 3
                reasons.append("Recent rainfall level is high.")

            elif rainfall >= 75:
                score -= 1
                reasons.append("Rainfall level is moderate.")

            elif rainfall < 30:
                score += 2
                reasons.append("Rainfall level is low.")

        if score >= 3:
            status = "🔴 Irrigation Recommended"
            message = (
                "The available farm conditions indicate that "
                "irrigation may be needed."
            )

        elif score >= 1:
            status = "🟡 Irrigate Soon"
            message = (
                "Monitor the field and consider irrigation if "
                "the soil feels dry."
            )

        else:
            status = "🟢 No Immediate Irrigation"
            message = "Current available conditions do not indicate immediate irrigation."

        reasons.append(
            "Soil moisture sensor data is not available, so this is an "
            "environment-based recommendation."
        )

    return {
        "status": status,
        "message": message,
        "reasons": reasons
    }


def show_irrigation_advisor():

    farmer = st.session_state.get("farmer")

    if not farmer:
        st.warning("Please login first.")
        return

    farmer_id = farmer["id"]

    st.title("💧 Irrigation Advisor")
    st.caption("Smart irrigation advice using your latest farm data")

    reading = get_latest_farm_reading(farmer_id)

    if not reading:
        st.info(
            "🌱 No farm data is available yet. "
            "Please enter your farm data in **My Farm Data** first."
        )

        if st.button("📡 Go to My Farm Data", use_container_width=True):
            st.session_state.page = "farm"
            st.rerun()

        return

    # --------------------------------------------------
    # Source
    # --------------------------------------------------

    source = reading.get("source", "manual")

    if source in ("iot", "live", "sensor"):
        st.success("📡 Using live sensor data")
    else:
        st.info("✍️ Using your latest manually entered farm data")

    # --------------------------------------------------
    # Recommendation
    # --------------------------------------------------

    result = irrigation_recommendation(reading)

    st.subheader("🌱 Irrigation Recommendation")

    if "Recommended" in result["status"]:
        st.error(result["status"])
    elif "Soon" in result["status"]:
        st.warning(result["status"])
    elif "Wet" in result["status"]:
        st.info(result["status"])
    else:
        st.success(result["status"])

    st.write(f"### {result['message']}")

    # --------------------------------------------------
    # Reasons
    # --------------------------------------------------

    st.subheader("🔎 Why?")

    for reason in result["reasons"]:
        st.write(f"• {reason}")

    # --------------------------------------------------
    # Farm conditions
    # --------------------------------------------------

    st.subheader("📊 Current Farm Conditions")

    col1, col2, col3, col4 = st.columns(4)

    temperature = reading.get("temperature")
    humidity = reading.get("humidity")
    rainfall = reading.get("rainfall")
    moisture = reading.get("soil_moisture")

    with col1:
        st.metric(
            "🌡️ Temperature",
            f"{temperature:.1f} °C" if temperature is not None else "N/A"
        )

    with col2:
        st.metric(
            "💨 Humidity",
            f"{humidity:.1f} %" if humidity is not None else "N/A"
        )

    with col3:
        st.metric(
            "🌧️ Rainfall",
            f"{rainfall:.1f} mm" if rainfall is not None else "N/A"
        )

    with col4:
        st.metric(
            "💧 Soil Moisture",
            f"{moisture:.1f} %" if moisture is not None else "N/A"
        )

    # --------------------------------------------------
    # Farmer guidance
    # --------------------------------------------------

    st.subheader("👨‍🌾 Farmer Guidance")

    if moisture is not None:

        if moisture < 20:
            st.error(
                "The soil is very dry. Irrigate according to your crop's "
                "water requirement and avoid excessive watering."
            )

        elif moisture < 35:
            st.warning(
                "The soil is drying. Check the field and prepare for irrigation."
            )

        elif moisture > 70:
            st.info(
                "The soil is wet. Avoid unnecessary irrigation to reduce "
                "water wastage and possible waterlogging."
            )

        else:
            st.success(
                "Soil moisture is currently in a reasonable range. "
                "Continue monitoring the field."
            )

    else:

        st.info(
            "💡 For more accurate irrigation advice, connect a soil-moisture "
            "sensor. The app will automatically use the live reading when "
            "available."
        )

    # --------------------------------------------------
    # Data timestamp
    # --------------------------------------------------

    recorded_at = reading.get("date")

    if recorded_at:
        st.caption(
            f"Last farm reading: {recorded_at}"
        )

    st.divider()

    st.caption(
        "⚠️ This is decision-support guidance. Actual irrigation should "
        "also consider crop type, growth stage, soil type and local weather."
    )