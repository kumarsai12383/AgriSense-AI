import sqlite3
import streamlit as st


DB_PATH = "database/agrisense.db"


# =========================================================
# GET LATEST FARM READING
# =========================================================

def get_latest_farm_reading(farmer_id):

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM farm_readings
            WHERE farmer_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (farmer_id,)
        )

        row = cursor.fetchone()

        if row:

            return dict(row)

        return None

    finally:

        conn.close()


# =========================================================
# GET LATEST CROP
# =========================================================

def get_latest_crop(farmer_id):

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    try:

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

        if row:

            return row["crop"]

        return None

    finally:

        conn.close()


# =========================================================
# PARAMETER ASSESSMENT
# =========================================================

def assess_parameter(
    value,
    low,
    high,
    name,
    unit=""
):

    if value < low:

        return (
            "Low",
            f"⚠️ {name} is below the preferred range "
            f"({low}{unit}–{high}{unit})."
        )

    elif value > high:

        return (
            "High",
            f"⚠️ {name} is above the preferred range "
            f"({low}{unit}–{high}{unit})."
        )

    else:

        return (
            "Good",
            f"✅ {name} is in a suitable range."
        )


# =========================================================
# SOIL HEALTH CALCULATION
# =========================================================

def calculate_soil_health(
    N,
    P,
    K,
    ph,
    temperature,
    humidity,
    rainfall,
    soil_moisture=None
):

    score = 100


    # Nitrogen

    if N < 40 or N > 120:

        score -= 15


    # Phosphorus

    if P < 30 or P > 80:

        score -= 15


    # Potassium

    if K < 30 or K > 80:

        score -= 15


    # pH

    if ph < 5.5 or ph > 7.5:

        score -= 20


    # Humidity

    if humidity < 40:

        score -= 10


    # Rainfall

    if rainfall < 50:

        score -= 10


    # Soil moisture

    if soil_moisture is not None:

        if soil_moisture < 20:

            score -= 10

        elif soil_moisture > 85:

            score -= 5


    return max(
        0,
        min(score, 100)
    )


# =========================================================
# SOIL HEALTH PAGE
# =========================================================

def show_soil_health():

    # -----------------------------------------------------
    # LOGIN CHECK
    # -----------------------------------------------------

    farmer = st.session_state.get("farmer")


    if not farmer:

        st.warning(
            "Please login first."
        )

        return


    farmer_id = farmer["id"]


    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    st.title(
        "🧪 Soil Health"
    )

    st.caption(
        "Understand your soil condition using your latest farm data."
    )


    # -----------------------------------------------------
    # GET FARM DATA
    # -----------------------------------------------------

    reading = get_latest_farm_reading(
        farmer_id
    )


    # -----------------------------------------------------
    # NO DATA
    # -----------------------------------------------------

    if not reading:

        st.info(
            "🌱 No farm data is available yet. "
            "Please enter your farm readings first."
        )


        if st.button(
            "📡 Go to My Farm Data",
            use_container_width=True
        ):

            st.session_state.page = "farm"

            st.rerun()


        return


    # -----------------------------------------------------
    # SOURCE
    # -----------------------------------------------------

    source = reading.get(
        "source"
    ) or "manual"


    recorded_at = reading.get(
        "date"
    )


    if source.lower() in (
        "iot",
        "live",
        "sensor"
    ):

        st.success(
            "📡 Using live sensor data"
        )

    else:

        st.info(
            "📝 Using your latest manual farm data"
        )


    if recorded_at:

        st.caption(
            f"🕒 Latest reading: {recorded_at}"
        )


    # -----------------------------------------------------
    # READ VALUES
    # -----------------------------------------------------

    N = float(
        reading.get("nitrogen") or 0
    )

    P = float(
        reading.get("phosphorus") or 0
    )

    K = float(
        reading.get("potassium") or 0
    )

    ph = float(
        reading.get("ph") or 0
    )

    temperature = float(
        reading.get("temperature") or 0
    )

    humidity = float(
        reading.get("humidity") or 0
    )

    rainfall = float(
        reading.get("rainfall") or 0
    )


    soil_moisture = reading.get(
        "soil_moisture"
    )


    if soil_moisture is not None:

        soil_moisture = float(
            soil_moisture
        )


    # -----------------------------------------------------
    # CALCULATE SCORE
    # -----------------------------------------------------

    score = calculate_soil_health(

        N=N,

        P=P,

        K=K,

        ph=ph,

        temperature=temperature,

        humidity=humidity,

        rainfall=rainfall,

        soil_moisture=soil_moisture

    )


    # =====================================================
    # OVERALL HEALTH
    # =====================================================

    st.markdown("---")

    st.subheader(
        "🌱 Overall Soil Health"
    )


    st.progress(
        score / 100
    )


    st.metric(
        "Health Score",
        f"{score}/100"
    )


    if score >= 85:

        st.success(
            "🟢 Excellent Soil Condition"
        )

    elif score >= 70:

        st.info(
            "🟡 Good Soil Condition"
        )

    elif score >= 50:

        st.warning(
            "🟠 Soil Needs Improvement"
        )

    else:

        st.error(
            "🔴 Soil Needs Attention"
        )


    # =====================================================
    # LATEST FARM READINGS
    # =====================================================

    st.markdown("---")

    st.subheader(
        "📊 Latest Farm Readings"
    )


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "🌱 Nitrogen",
        f"{N:.1f}"
    )


    c2.metric(
        "🧪 Phosphorus",
        f"{P:.1f}"
    )


    c3.metric(
        "🪴 Potassium",
        f"{K:.1f}"
    )


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "⚗️ Soil pH",
        f"{ph:.1f}"
    )


    c2.metric(
        "🌡️ Temperature",
        f"{temperature:.1f} °C"
    )


    c3.metric(
        "💧 Humidity",
        f"{humidity:.1f}%"
    )


    c1, c2 = st.columns(2)


    c1.metric(
        "🌧️ Rainfall",
        f"{rainfall:.1f} mm"
    )


    if soil_moisture is not None:

        c2.metric(
            "💦 Soil Moisture",
            f"{soil_moisture:.1f}%"
        )

    else:

        c2.metric(
            "💦 Soil Moisture",
            "Not available"
        )


    # =====================================================
    # PARAMETER ANALYSIS
    # =====================================================

    st.markdown("---")

    st.subheader(
        "🔎 Soil Condition Analysis"
    )


    parameters = [

        (
            "Nitrogen",
            N,
            40,
            120,
            ""
        ),

        (
            "Phosphorus",
            P,
            30,
            80,
            ""
        ),

        (
            "Potassium",
            K,
            30,
            80,
            ""
        ),

        (
            "Soil pH",
            ph,
            5.5,
            7.5,
            ""
        ),

        (
            "Humidity",
            humidity,
            40,
            100,
            "%"
        ),

        (
            "Rainfall",
            rainfall,
            50,
            300,
            " mm"
        ),

    ]


    for name, value, low, high, unit in parameters:

        condition, message = assess_parameter(

            value,
            low,
            high,
            name,
            unit

        )


        if condition == "Good":

            st.success(
                message
            )

        else:

            st.warning(
                message
            )


    # =====================================================
    # SOIL MOISTURE ANALYSIS
    # =====================================================

    if soil_moisture is not None:

        if 20 <= soil_moisture <= 85:

            st.success(
                f"✅ Soil Moisture is in a reasonable range "
                f"({soil_moisture:.1f}%)."
            )

        elif soil_moisture < 20:

            st.warning(
                f"⚠️ Soil Moisture is low "
                f"({soil_moisture:.1f}%). "
                "Check the field and irrigation requirement."
            )

        else:

            st.warning(
                f"⚠️ Soil Moisture is high "
                f"({soil_moisture:.1f}%). "
                "Avoid unnecessary irrigation."
            )


    # =====================================================
    # CROP CONTEXT
    # =====================================================

    recommended_crop = get_latest_crop(
        farmer_id
    )


    if recommended_crop:

        st.markdown("---")

        st.subheader(
            "🌾 Crop Context"
        )


        st.write(
            "Your latest ML crop recommendation is "
            f"**{recommended_crop.title()}**."
        )


        st.info(
            "The crop recommendation comes from your ML model. "
            "This Soil Health report evaluates the current farm "
            "readings separately."
        )


    # =====================================================
    # FARMER GUIDANCE
    # =====================================================

    st.markdown("---")

    st.subheader(
        "💡 What You Can Do"
    )


    if score >= 85:

        st.success(
            "Your current readings look healthy. "
            "Continue monitoring your soil and farm conditions."
        )

    elif score >= 70:

        st.info(
            "Your soil condition is generally good. "
            "Focus on the parameters marked for improvement."
        )

    elif score >= 50:

        st.warning(
            "Some soil conditions need attention. "
            "Review the highlighted parameters and follow "
            "suitable soil management practices."
        )

    else:

        st.error(
            "Several readings need attention. "
            "Consider proper soil testing and expert guidance "
            "before making major changes."
        )


    # =====================================================
    # DISCLAIMER
    # =====================================================

    st.caption(
        "⚠️ This report is decision-support based on the latest "
        "available farm readings. It does not replace laboratory "
        "soil testing."
    )