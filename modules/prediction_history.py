import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "database/agrisense.db"


# ======================================
# Get Farmer Prediction History
# ======================================

def get_prediction_history(farmer_id):

    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
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
        ORDER BY id DESC
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(farmer_id,)
    )

    conn.close()

    return df


# ======================================
# Show Prediction History
# ======================================

def show_prediction_history():

    farmer = st.session_state.get("farmer")

    if not farmer:
        st.warning("Please login first.")
        return

    farmer_id = farmer["id"]

    st.title("📊 My Progress")

    st.caption(
        f"👨‍🌾 Crop prediction history for {farmer['name']}"
    )

    # ======================================
    # Get History
    # ======================================

    history_df = get_prediction_history(farmer_id)

    if history_df.empty:

        st.info(
            "🌱 No crop predictions yet. "
            "Make your first crop recommendation to start tracking your progress."
        )

        if st.button(
            "🌾 Go to Crop Recommendation",
            use_container_width=True
        ):
            st.session_state.page = "crop"
            st.rerun()

        return

    # ======================================
    # Summary
    # ======================================

    total_predictions = len(history_df)

    latest_crop = history_df.iloc[0]["crop"]

    unique_crops = history_df["crop"].nunique()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📈 Total Predictions",
            total_predictions
        )

    with col2:
        st.metric(
            "🌾 Latest Crop",
            str(latest_crop).title()
        )

    with col3:
        st.metric(
            "🌱 Crops Recommended",
            unique_crops
        )

    st.markdown("---")

    # ======================================
    # Latest Recommendation
    # ======================================

    st.subheader("🌾 Latest Recommendation")

    st.success(
        f"Your latest recommended crop is **{str(latest_crop).title()}**."
    )

    # ======================================
    # Prediction History
    # ======================================

    st.subheader("📜 Prediction History")

    display_df = history_df.copy()

    display_df = display_df.rename(columns={
        "crop": "🌾 Crop",
        "temperature": "🌡️ Temperature",
        "humidity": "💧 Humidity",
        "nitrogen": "🌱 Nitrogen",
        "phosphorus": "🧪 Phosphorus",
        "potassium": "🪴 Potassium",
        "ph": "⚗️ pH",
        "rainfall": "🌧️ Rainfall",
        "date": "📅 Date"
    })

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    # ======================================
    # Crop Frequency
    # ======================================

    st.markdown("---")

    st.subheader("🌱 Recommended Crop Summary")

    crop_counts = (
        history_df["crop"]
        .value_counts()
        .reset_index()
    )

    crop_counts.columns = [
        "Crop",
        "Recommendations"
    ]

    crop_counts["Crop"] = (
        crop_counts["Crop"]
        .astype(str)
        .str.title()
    )

    st.dataframe(
        crop_counts,
        use_container_width=True,
        hide_index=True
    )

    # ======================================
    # Latest Farm Conditions
    # ======================================

    st.markdown("---")

    st.subheader("📊 Latest Prediction Conditions")

    latest = history_df.iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "🌱 N",
            latest["nitrogen"]
        )

    with c2:
        st.metric(
            "🧪 P",
            latest["phosphorus"]
        )

    with c3:
        st.metric(
            "🪴 K",
            latest["potassium"]
        )

    with c4:
        st.metric(
            "⚗️ pH",
            latest["ph"]
        )

    c5, c6, c7 = st.columns(3)

    with c5:
        st.metric(
            "🌡️ Temperature",
            f"{latest['temperature']} °C"
        )

    with c6:
        st.metric(
            "💧 Humidity",
            f"{latest['humidity']} %"
        )

    with c7:
        st.metric(
            "🌧️ Rainfall",
            f"{latest['rainfall']} mm"
        )

    # ======================================
    # Session History Migration / Compatibility
    # ======================================

    # Keep this only for compatibility with older
    # versions of the application.
    if "history" not in st.session_state:
        st.session_state.history = []

    st.markdown("---")

    st.caption(
        "📌 Your prediction history is stored permanently "
        "for your farmer account."
    )