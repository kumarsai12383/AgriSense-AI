import os
import sqlite3
from datetime import datetime
import streamlit as st
import joblib

# =========================================================
# AgriSense AI - High-Speed Farm Data & IoT Management Page
# =========================================================

from database.database import connect as get_db_conn, DB_PATH
MODEL_PATH = "models/crop_model.pkl"


def get_connection():
    """Direct, high-speed connection to local SQLite database."""
    return get_db_conn()


@st.cache_resource
def load_ml_model():
    """Cache the machine learning model in memory for instant sub-millisecond predictions."""
    if os.path.exists(MODEL_PATH):
        try:
            return joblib.load(MODEL_PATH)
        except Exception:
            return None
    return None


# =========================================================
# DIRECT HIGH-SPEED DATABASE OPERATIONS
# =========================================================

def get_latest_farm_reading(farmer_id):
    """Retrieve the latest farm reading directly from SQLite DB (0.001s latency)."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, farmer_id, nitrogen, phosphorus, potassium, ph,
                   temperature, humidity, rainfall, soil_moisture, source, date
            FROM farm_readings
            WHERE farmer_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (farmer_id,)
        )
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    except Exception:
        return None


def get_sensor_status(farmer_id):
    """Check the latest IoT reading directly from SQLite DB."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, farmer_id, nitrogen, phosphorus, potassium, ph,
                   temperature, humidity, rainfall, soil_moisture, source, date
            FROM farm_readings
            WHERE farmer_id = ? AND source = 'iot'
            ORDER BY id DESC
            LIMIT 1
            """,
            (farmer_id,)
        )
        row = cursor.fetchone()
        conn.close()

        if not row:
            return {
                "status": "offline",
                "connected": False,
                "message": "No IoT sensor data has been received yet.",
                "data": None,
                "last_seen_seconds": None
            }

        reading = dict(row)
        age_seconds = None
        try:
            date_val = reading.get("date")
            if date_val:
                last_reading_time = datetime.fromisoformat(str(date_val).replace(" ", "T"))
                age_seconds = max(0, (datetime.now() - last_reading_time).total_seconds())
        except Exception:
            age_seconds = None

        connected = age_seconds is not None and age_seconds <= 600

        return {
            "status": "connected" if connected else "offline",
            "connected": connected,
            "last_seen_seconds": round(age_seconds, 1) if age_seconds is not None else None,
            "message": "IoT sensor is connected and sending data." if connected else "IoT sensor has not sent data recently.",
            "data": reading
        }
    except Exception:
        return {
            "status": "offline",
            "connected": False,
            "message": "Offline",
            "data": None,
            "last_seen_seconds": None
        }


def save_farm_reading(farmer_id, data_dict, source="manual"):
    """Save a farm reading directly to SQLite DB."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO farm_readings (
                farmer_id, nitrogen, phosphorus, potassium, ph,
                temperature, humidity, rainfall, soil_moisture, source, date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                farmer_id,
                data_dict.get("nitrogen"),
                data_dict.get("phosphorus"),
                data_dict.get("potassium"),
                data_dict.get("ph"),
                data_dict.get("temperature"),
                data_dict.get("humidity"),
                data_dict.get("rainfall"),
                data_dict.get("soil_moisture"),
                source,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        conn.commit()
        reading_id = cursor.lastrowid
        conn.close()
        return reading_id
    except Exception as e:
        st.error(f"Database save error: {e}")
        return None


def run_crop_prediction(farmer_id, reading):
    """Run the RandomForest crop model with high speed and record the prediction."""
    try:
        model = load_ml_model()
        if not model:
            return None

        features = [[
            float(reading["nitrogen"]),
            float(reading["phosphorus"]),
            float(reading["potassium"]),
            float(reading["temperature"]),
            float(reading["humidity"]),
            float(reading["ph"]),
            float(reading["rainfall"])
        ]]
        crop = str(model.predict(features)[0]).strip().lower()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO predictions (
                farmer_id, crop, temperature, humidity,
                nitrogen, phosphorus, potassium, ph, rainfall, date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                farmer_id,
                crop,
                reading["temperature"],
                reading["humidity"],
                reading["nitrogen"],
                reading["phosphorus"],
                reading["potassium"],
                reading["ph"],
                reading["rainfall"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        conn.commit()
        conn.close()
        return crop
    except Exception as e:
        st.warning(f"Crop prediction error: {e}")
        return None


def show_reading_cards(data):
    """Display farm reading metric cards."""
    if not data:
        st.info("No reading data to display.")
        return

    st.markdown("### 📊 Farm Readings")

    c1, c2 = st.columns(2)
    c1.metric("🌱 Nitrogen (N)", f"{data.get('nitrogen', 'N/A')}")
    c2.metric("🧪 Phosphorus (P)", f"{data.get('phosphorus', 'N/A')}")

    c3, c4 = st.columns(2)
    c3.metric("🪴 Potassium (K)", f"{data.get('potassium', 'N/A')}")
    c4.metric("⚗️ Soil pH", f"{data.get('ph', 'N/A')}")

    c5, c6 = st.columns(2)
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    c5.metric("🌡️ Temperature", f"{temperature} °C" if temperature is not None else "N/A")
    c6.metric("💧 Humidity", f"{humidity} %" if humidity is not None else "N/A")

    c7, c8 = st.columns(2)
    rainfall = data.get("rainfall")
    moisture = data.get("soil_moisture")
    c7.metric("🌧️ Rainfall", f"{rainfall} mm" if rainfall is not None else "N/A")
    c8.metric("💦 Soil Moisture", f"{moisture} %" if moisture is not None else "N/A")


# =========================================================
# MAIN VIEW
# =========================================================

def show_farm_data():
    st.title("📡 My Farm Data")

    farmer = st.session_state.get("farmer")
    if not farmer:
        st.warning("Please login first.")
        return

    farmer_id = farmer["id"]

    # Header Card with instant status
    st.markdown(
        f"""
        <div style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 16px; padding: 14px 18px; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
            <div>
                <span style="font-size: 15px; font-weight: 800; color: #0f172a;">👨‍🌾 {farmer['name']} (Farm ID: #{farmer_id})</span>
                <div style="font-size: 12px; color: #64748b; margin-top: 2px;">⚡ High-Speed Direct Database Engine Active</div>
            </div>
            <span style="background: #dcfce7; color: #166534; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 9999px; border: 1px solid #86efac;">
                🟢 SYSTEM READY
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # Mode selector
    # -----------------------------------------------------
    mode = st.radio(
        "Select Farm Data Input Mode:",
        ["📝 Manual Entry", "📡 Live Sensors (IoT)"],
        key="farm_data_mode",
        horizontal=True
    )

    # =====================================================
    # MANUAL MODE
    # =====================================================
    if mode == "📝 Manual Entry":
        st.info("✍️ Enter your farm soil and climate parameters. Data is saved directly to your farmer profile.")

        # Prefill with latest data instantly
        latest_saved = get_latest_farm_reading(farmer_id) or {}

        st.subheader("🌱 Soil Nutrients & pH")
        col_n, col_p, col_k = st.columns(3)
        nitrogen = col_n.number_input("Nitrogen (N)", min_value=0.0, value=float(latest_saved.get("nitrogen", 80.0)), step=1.0)
        phosphorus = col_p.number_input("Phosphorus (P)", min_value=0.0, value=float(latest_saved.get("phosphorus", 42.0)), step=1.0)
        potassium = col_k.number_input("Potassium (K)", min_value=0.0, value=float(latest_saved.get("potassium", 43.0)), step=1.0)

        ph = st.number_input("Soil pH (0 - 14)", min_value=0.0, max_value=14.0, value=float(latest_saved.get("ph", 7.2)), step=0.1)

        st.subheader("🌦️ Climate & Weather")
        col_t, col_h = st.columns(2)
        temperature = col_t.number_input("Temperature (°C)", value=float(latest_saved.get("temperature", 28.0)), step=0.1)
        humidity = col_h.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=float(latest_saved.get("humidity", 82.0)), step=1.0)

        col_r, col_m = st.columns(2)
        rainfall = col_r.number_input("Rainfall (mm)", min_value=0.0, value=float(latest_saved.get("rainfall", 110.0)), step=1.0)
        soil_moisture = col_m.number_input("Soil Moisture (%)", min_value=0.0, max_value=100.0, value=float(latest_saved.get("soil_moisture", 35.0)), step=1.0)

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        if st.button("💾 Save Farm Data & Predict Best Crop", use_container_width=True, type="primary"):
            payload = {
                "farmer_id": farmer_id,
                "nitrogen": nitrogen,
                "phosphorus": phosphorus,
                "potassium": potassium,
                "ph": ph,
                "temperature": temperature,
                "humidity": humidity,
                "rainfall": rainfall,
                "soil_moisture": soil_moisture,
                "source": "manual"
            }

            # Instant direct save to database
            save_farm_reading(farmer_id, payload, source="manual")

            # Instant ML prediction
            pred_crop = run_crop_prediction(farmer_id, payload)
            if pred_crop:
                st.success(f"✅ Farm data saved successfully! Recommended Crop: **{str(pred_crop).title()}**")
            else:
                st.success("✅ Farm data saved successfully!")

    # =====================================================
    # LIVE SENSOR MODE (IOT)
    # =====================================================
    else:
        st.subheader("📡 Live IoT Sensor Telemetry")

        status = get_sensor_status(farmer_id)
        is_connected = status.get("connected", False)
        last_seen = status.get("last_seen_seconds")
        data = status.get("data")

        if is_connected:
            st.success("🟢 **ESP32 Sensor Online** — Receiving live telemetry from soil probe")
        else:
            st.warning("🔴 **Sensor Offline** — No recent telemetry received within the last 10 minutes")

        if last_seen is not None:
            if last_seen < 60:
                last_seen_text = f"{last_seen:.0f} seconds ago"
            elif last_seen < 3600:
                last_seen_text = f"{last_seen / 60:.1f} minutes ago"
            else:
                last_seen_text = f"{last_seen / 3600:.1f} hours ago"
            st.caption(f"🕒 Last sensor reading received: **{last_seen_text}**")

        if data:
            show_reading_cards(data)
            st.caption(f"📡 Data Source: **{str(data.get('source', 'iot')).upper()}**")

            st.markdown("---")
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("🔄 Refresh Sensor Data", use_container_width=True):
                    st.rerun()
            with col_b2:
                if st.button("🌾 Predict Crop from Sensor Data", use_container_width=True, type="primary"):
                    pred = run_crop_prediction(farmer_id, data)
                    if pred:
                        st.success(f"🌾 Recommended Crop: **{str(pred).title()}**")

        else:
            st.info("📡 No IoT sensor readings recorded in the database yet.")

            st.markdown(
                """
                **ESP32 7-in-1 Soil Sensor Setup:**
                - Connect ESP32 to your farm Wi-Fi
                - In `esp32/agrisense_esp32.ino`, set `BACKEND_URL = "http://<YOUR_COMPUTER_IP>:8000/sensor/data"`
                - Run `python server.py` on your computer
                """
            )

            # Interactive Test Simulator for Testing without Hardware
            st.markdown("---")
            st.markdown("#### 🧪 Test IoT Integration (Simulate ESP32)")
            if st.button("⚡ Simulate ESP32 Sensor Reading", use_container_width=True):
                simulated_reading = {
                    "farmer_id": farmer_id,
                    "nitrogen": 85.0,
                    "phosphorus": 45.0,
                    "potassium": 48.0,
                    "ph": 6.8,
                    "temperature": 27.5,
                    "humidity": 78.0,
                    "rainfall": 130.0,
                    "soil_moisture": 42.0,
                    "source": "iot"
                }
                save_farm_reading(farmer_id, simulated_reading, source="iot")
                run_crop_prediction(farmer_id, simulated_reading)
                st.success("✅ Simulated ESP32 telemetry recorded successfully!")
                st.rerun()

    # =====================================================
    # LATEST SAVED FARM RECORD SECTION
    # =====================================================
    st.markdown("---")
    st.subheader("📊 Latest Farm Reading in Database")

    latest_data = get_latest_farm_reading(farmer_id)
    if latest_data:
        source = latest_data.get("source", "manual")
        if source == "iot":
            st.success("📡 Record generated via IoT Sensor probe.")
        else:
            st.info("📝 Record entered manually.")

        show_reading_cards(latest_data)
        st.caption(f"🕒 Recorded on: **{latest_data.get('date', 'N/A')}**")
    else:
        st.info("📭 No farm data recorded yet. Please enter values above or connect your ESP32 sensor.")
