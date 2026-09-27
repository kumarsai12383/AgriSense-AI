import streamlit as st
import sqlite3

from fertilizer import fertilizer_information

DB_PATH = "database/agrisense.db"


# ======================================
# Get Latest Farm Data
# ======================================

def get_latest_farm_data(farmer_id):

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
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
    """, (farmer_id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)

    return None


# ======================================
# Get Latest Predicted Crop
# ======================================

def get_latest_crop(farmer_id):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT crop
        FROM predictions
        WHERE farmer_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (farmer_id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None


# ======================================
# NPK Analysis
# ======================================

def analyze_nutrients(nitrogen, phosphorus, potassium):

    recommendations = []

    # Nitrogen
    if nitrogen < 40:
        recommendations.append(
            "🌱 Nitrogen is low. Consider a nitrogen-rich fertilizer."
        )
    elif nitrogen > 120:
        recommendations.append(
            "⚠️ Nitrogen is high. Avoid applying excess nitrogen fertilizer."
        )
    else:
        recommendations.append(
            "✅ Nitrogen level is within the working range."
        )

    # Phosphorus
    if phosphorus < 30:
        recommendations.append(
            "🧪 Phosphorus is low. A phosphorus-containing fertilizer may help."
        )
    elif phosphorus > 80:
        recommendations.append(
            "⚠️ Phosphorus is high. Avoid unnecessary phosphorus application."
        )
    else:
        recommendations.append(
            "✅ Phosphorus level is within the working range."
        )

    # Potassium
    if potassium < 30:
        recommendations.append(
            "🪴 Potassium is low. Consider a potassium-containing fertilizer."
        )
    elif potassium > 80:
        recommendations.append(
            "⚠️ Potassium is high. Avoid excessive potassium fertilizer."
        )
    else:
        recommendations.append(
            "✅ Potassium level is within the working range."
        )

    return recommendations


# ======================================
# Fertilizer Advisor
# ======================================

def show_fertilizer_advisor(crop=None):

    farmer = st.session_state.get("farmer")

    if not farmer:
        st.warning("Please login first.")
        return

    farmer_id = farmer["id"]

    st.title("🌿 Fertilizer Advisor")

    st.caption(
        "Smart fertilizer guidance using your latest farm data"
    )

    # ======================================
    # Latest Farm Reading
    # ======================================

    farm_data = get_latest_farm_data(farmer_id)

    if not farm_data:

        st.info(
            "🌱 No farm data is available yet."
        )

        st.write(
            "Please enter your farm information in **My Farm Data** first."
        )

        if st.button(
            "📡 Go to My Farm Data",
            use_container_width=True
        ):
            st.session_state.page = "farm"
            st.rerun()

        return

    # ======================================
    # Crop
    # ======================================

    latest_crop = get_latest_crop(farmer_id)

    if crop:
        latest_crop = crop

    if not latest_crop:

        st.warning(
            "🌾 No crop prediction is available yet."
        )

        st.info(
            "First generate a crop recommendation from your latest farm data."
        )

        if st.button(
            "🌾 Go to Crop Recommendation",
            use_container_width=True
        ):
            st.session_state.page = "crop"
            st.rerun()

        return

    latest_crop_key = latest_crop.lower()

    fertilizer = fertilizer_information.get(latest_crop_key)

    # ======================================
    # Data Source
    # ======================================

    source = farm_data.get("source", "manual")

    if source in ("iot", "live", "sensor"):
        st.success("📡 Using latest live sensor reading")
    else:
        st.info("📝 Using latest manually entered farm reading")

    # ======================================
    # Crop Display
    # ======================================

    st.subheader("🌾 Current Recommended Crop")

    st.success(
        f"**{latest_crop.title()}**"
    )

    # ======================================
    # NPK Values
    # ======================================

    st.subheader("🧪 Soil Nutrient Status")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "🌱 Nitrogen",
        farm_data["nitrogen"]
    )

    c2.metric(
        "🧪 Phosphorus",
        farm_data["phosphorus"]
    )

    c3.metric(
        "🪴 Potassium",
        farm_data["potassium"]
    )

    # ======================================
    # pH
    # ======================================

    st.metric(
        "⚗️ Soil pH",
        farm_data["ph"]
    )

    # ======================================
    # Nutrient Analysis
    # ======================================

    st.subheader("🔎 Nutrient Analysis")

    recommendations = analyze_nutrients(
        farm_data["nitrogen"],
        farm_data["phosphorus"],
        farm_data["potassium"]
    )

    for recommendation in recommendations:
        st.write(recommendation)

    # ======================================
    # Crop-specific Fertilizer Information
    # ======================================

    if fertilizer:

        st.markdown("---")

        st.subheader(
            f"🌿 Fertilizer Guidance for {latest_crop.title()}"
        )

        with st.expander(
            "🌿 Recommended Fertilizers",
            expanded=True
        ):
            st.write(
                fertilizer["fertilizer"]
            )

        with st.expander(
            "📅 Application Schedule"
        ):
            st.write(
                fertilizer["schedule"]
            )

        with st.expander(
            "👨‍🌾 Farmer Tips"
        ):
            st.write(
                fertilizer["tips"]
            )

    else:

        st.warning(
            "Fertilizer information for this crop is not available "
            "in the current fertilizer database."
        )

    # ======================================
    # Important Guidance
    # ======================================

    st.markdown("---")

    st.subheader("👨‍🌾 Important")

    st.info(
        """
        Fertilizer recommendations should be considered together with
        soil condition, crop growth stage and local agricultural guidance.

        Do not apply excessive fertilizer only because a nutrient value
        appears low. Soil testing and crop-specific recommendations are
        preferred for final application decisions.
        """
    )

    st.caption(
        f"🕒 Farm data recorded: {farm_data['date']}"
    )