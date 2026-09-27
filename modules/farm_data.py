import streamlit as st
import requests

# =========================================================
# AgriSense AI - Mobile Farm Data Page
# =========================================================

API_BASE = "http://127.0.0.1:8000"
SENSOR_TIMEOUT_SECONDS = 5


def api_get(path):
    try:
        response = requests.get(
            f"{API_BASE}{path}",
            timeout=SENSOR_TIMEOUT_SECONDS
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"⚠️ Backend connection error: {e}")
        return None


def api_post(path, payload):
    try:
        response = requests.post(
            f"{API_BASE}{path}",
            json=payload,
            timeout=SENSOR_TIMEOUT_SECONDS
        )
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        try:
            detail = response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        st.error(f"⚠️ {detail}")
        return None
    except requests.RequestException as e:
        st.error(f"⚠️ Backend connection error: {e}")
        return None


def show_reading_cards(data):
    st.markdown("### 📊 Current Farm Readings")

    c1, c2 = st.columns(2)
    c1.metric("🌱 Nitrogen", data.get("nitrogen", "N/A"))
    c2.metric("🧪 Phosphorus", data.get("phosphorus", "N/A"))

    c3, c4 = st.columns(2)
    c3.metric("🪴 Potassium", data.get("potassium", "N/A"))
    c4.metric("⚗️ Soil pH", data.get("ph", "N/A"))

    c5, c6 = st.columns(2)
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    c5.metric(
        "🌡️ Temperature",
        f"{temperature} °C" if temperature is not None else "N/A"
    )
    c6.metric(
        "💧 Humidity",
        f"{humidity} %" if humidity is not None else "N/A"
    )

    c7, c8 = st.columns(2)
    rainfall = data.get("rainfall")
    moisture = data.get("soil_moisture")
    c7.metric(
        "🌧️ Rainfall",
        f"{rainfall} mm" if rainfall is not None else "N/A"
    )
    c8.metric(
        "💦 Soil Moisture",
        f"{moisture} %" if moisture is not None else "N/A"
    )


def predict_latest_crop(farmer_id):
    result = api_post(
        f"/crop/predict-latest/{farmer_id}",
        {}
    )

    if result and result.get("status") == "success":
        crop = result.get("crop", "Unknown")
        source = result.get("source", "unknown")

        st.success(
            f"🌾 Recommended Crop: **{str(crop).title()}**"
        )
        st.caption(
            f"🤖 Prediction generated from {source.upper()} farm data."
        )


def show_farm_data():
    st.title("📡 My Farm")

    farmer = st.session_state.get("farmer")

    if not farmer:
        st.warning("Please login first.")
        return

    farmer_id = farmer["id"]

    st.caption(f"👨‍🌾 {farmer['name']}")
    st.markdown("---")

    # -----------------------------------------------------
    # Select data mode
    # -----------------------------------------------------

    mode = st.radio(
        "How do you want to provide farm data?",
        [
            "📝 Manual Entry",
            "📡 Live Sensors"
        ],
        key="farm_data_mode"
    )

    # =====================================================
    # MANUAL MODE
    # =====================================================

    if mode == "📝 Manual Entry":

        st.info(
            "✍️ Enter your current farm conditions. "
            "The data will be saved to your farm record."
        )

        st.subheader("🌱 Soil Values")

        nitrogen = st.number_input(
            "Nitrogen (N)",
            min_value=0.0,
            value=80.0,
            step=1.0
        )

        phosphorus = st.number_input(
            "Phosphorus (P)",
            min_value=0.0,
            value=42.0,
            step=1.0
        )

        potassium = st.number_input(
            "Potassium (K)",
            min_value=0.0,
            value=43.0,
            step=1.0
        )

        ph = st.number_input(
            "Soil pH",
            min_value=0.0,
            max_value=14.0,
            value=7.5,
            step=0.1
        )

        st.subheader("🌦️ Weather & Water")

        temperature = st.number_input(
            "Temperature (°C)",
            value=28.0,
            step=0.1
        )

        humidity = st.number_input(
            "Humidity (%)",
            min_value=0.0,
            max_value=100.0,
            value=82.0,
            step=1.0
        )

        rainfall = st.number_input(
            "Rainfall (mm)",
            min_value=0.0,
            value=110.0,
            step=1.0
        )

        soil_moisture = st.number_input(
            "Soil Moisture (%)",
            min_value=0.0,
            max_value=100.0,
            value=35.0,
            step=1.0
        )

        st.markdown("---")

        if st.button(
            "💾 Save Farm Data",
            use_container_width=True,
            type="primary"
        ):
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

            result = api_post("/farm/manual", payload)

            if not result or result.get("status") != "success":
                # Direct Database Fallback if backend server is offline
                try:
                    import sqlite3
                    import joblib
                    conn = sqlite3.connect("database/agrisense.db")
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO farm_readings (
                            farmer_id, nitrogen, phosphorus, potassium, ph,
                            temperature, humidity, rainfall, soil_moisture, source
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (farmer_id, nitrogen, phosphorus, potassium, ph, temperature, humidity, rainfall, soil_moisture, "manual"))
                    conn.commit()

                    # Run ML prediction directly
                    model = joblib.load("models/crop_model.pkl")
                    pred = model.predict([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])[0]
                    cursor.execute("""
                        INSERT INTO predictions (farmer_id, crop, temperature, humidity, nitrogen, phosphorus, potassium, ph, rainfall)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (farmer_id, str(pred).lower(), temperature, humidity, nitrogen, phosphorus, potassium, ph, rainfall))
                    conn.commit()
                    conn.close()

                    st.success(f"✅ Farm data saved! Predicted Crop: **{str(pred).title()}**")
                    st.session_state["farm_data_refresh"] = st.session_state.get("farm_data_refresh", 0) + 1
                except Exception as ex:
                    st.error(f"Save error: {ex}")
            else:
                st.success("✅ Farm data saved successfully!")
                st.session_state["farm_data_refresh"] = st.session_state.get("farm_data_refresh", 0) + 1
                predict_latest_crop(farmer_id)

    # =====================================================
    # LIVE SENSOR MODE
    # =====================================================

    else:

        st.subheader("📡 Live Sensor Data")

        status = api_get(
            f"/sensor/status/{farmer_id}"
        )

        if not status:
            return

        if status.get("connected"):
            st.success(
                "🟢 Sensor Connected — receiving live data"
            )
        else:
            st.warning(
                "🔴 Sensor Offline — no recent IoT reading"
            )

        last_seen = status.get("last_seen_seconds")

        if last_seen is not None:
            if last_seen < 60:
                last_seen_text = f"{last_seen:.0f} seconds ago"
            elif last_seen < 3600:
                last_seen_text = f"{last_seen / 60:.1f} minutes ago"
            else:
                last_seen_text = f"{last_seen / 3600:.1f} hours ago"

            st.caption(f"🕒 Last sensor reading: {last_seen_text}")

        data = status.get("data")

        if data:
            show_reading_cards(data)

            st.caption(
                f"📡 Source: {data.get('source', 'iot').upper()}"
            )

            st.markdown("---")

            if st.button(
                "🔄 Refresh Sensor Data",
                use_container_width=True
            ):
                st.rerun()

            if st.button(
                "🌾 Predict Best Crop",
                use_container_width=True,
                type="primary"
            ):
                predict_latest_crop(farmer_id)

        else:
            st.info(
                "📡 No IoT sensor reading is available yet."
            )

            st.markdown(
                """
                **When your ESP32 is connected, this page will
                automatically show:**

                - 🌱 Nitrogen
                - 🧪 Phosphorus
                - 🪴 Potassium
                - ⚗️ Soil pH
                - 🌡️ Temperature
                - 💧 Humidity
                - 🌧️ Rainfall
                - 💦 Soil Moisture
                """
            )

    # =====================================================
    # LATEST FARM RECORD
    # =====================================================

    st.markdown("---")
    st.subheader("📊 Latest Saved Farm Data")

    latest = api_get(
        f"/farm/latest/{farmer_id}"
    )

    if latest and latest.get("status") == "success":
        latest_data = latest.get("data")

        if latest_data:
            source = latest_data.get("source", "manual")

            if source == "iot":
                st.success("📡 Latest record came from IoT sensors.")
            else:
                st.info("📝 Latest record was entered manually.")

            show_reading_cards(latest_data)

            st.caption(
                f"🕒 Recorded: {latest_data.get('date', 'N/A')}"
            )

    elif latest and latest.get("status") == "no_data":
        st.info("📭 No farm data has been saved yet.")
