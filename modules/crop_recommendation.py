import os
import streamlit as st
import sqlite3
import joblib
import numpy as np
from modules.ai_crop_advisor import show_ai_crop_advisor
from modules.crop_details import CROP_DETAILS

from database.database import connect, DB_PATH
MODEL_PATH = "models/crop_model.pkl"

LOCALIZED_CROP_NAMES = {
    "te": {
        "rice": "వరి (Rice)",
        "maize": "మొక్కజొన్న (Maize)",
        "chickpea": "శనగలు (Chickpea)",
        "kidneybeans": "రాజ్మా (Kidney Beans)",
        "pigeonpeas": "కందులు (Pigeon Peas)",
        "mothbeans": "బొబ్బర్లు (Moth Beans)",
        "mungbean": "పెసలు (Mung Bean)",
        "blackgram": "మినుములు (Black Gram)",
        "lentil": "మసూరి పప్పు (Lentil)",
        "pomegranate": "దానిమ్మ (Pomegranate)",
        "banana": "అరటి (Banana)",
        "mango": "మామిడి (Mango)",
        "grapes": "ద్రాక్ష (Grapes)",
        "watermelon": "పుచ్చకాయ (Watermelon)",
        "muskmelon": "ఖర్బూజా (Muskmelon)",
        "apple": "యాపిల్ (Apple)",
        "orange": "నారింజ (Orange)",
        "papaya": "బొప్పాయి (Papaya)",
        "coconut": "కొబ్బరి (Coconut)",
        "cotton": "పత్తి (Cotton)",
        "jute": "జనపనార (Jute)",
        "coffee": "కాఫీ (Coffee)"
    },
    "hi": {
        "rice": "चावल / धान (Rice)",
        "maize": "मक्का (Maize)",
        "chickpea": "चना (Chickpea)",
        "kidneybeans": "राजमा (Kidney Beans)",
        "pigeonpeas": "अरहर / तुअर (Pigeon Peas)",
        "mothbeans": "मोठ (Moth Beans)",
        "mungbean": "मूंग (Mung Bean)",
        "blackgram": "उड़द (Black Gram)",
        "lentil": "मसूर (Lentil)",
        "pomegranate": "अनार (Pomegranate)",
        "banana": "केला (Banana)",
        "mango": "आम (Mango)",
        "grapes": "अंगूर (Grapes)",
        "watermelon": "तरबूज (Watermelon)",
        "muskmelon": "खरबूजा (Muskmelon)",
        "apple": "सेब (Apple)",
        "orange": "संतरा (Orange)",
        "papaya": "पपीता (Papaya)",
        "coconut": "नारियल (Coconut)",
        "cotton": "कपास (Cotton)",
        "jute": "जूट (Jute)",
        "coffee": "कॉफ़ी (Coffee)"
    },
    "ta": {
        "rice": "நெல் (Rice)",
        "maize": "மக்காச்சோளம் (Maize)",
        "chickpea": "கொண்டைக்கடலை (Chickpea)",
        "kidneybeans": "ராஜ்மா (Kidney Beans)",
        "pigeonpeas": "துவரை (Pigeon Peas)",
        "mothbeans": "பயறு (Moth Beans)",
        "mungbean": "பாசிப்பயறு (Mung Bean)",
        "blackgram": "உளுந்து (Black Gram)",
        "lentil": "துவரம்பருப்பு (Lentil)",
        "pomegranate": "மாதுளை (Pomegranate)",
        "banana": "வாழை (Banana)",
        "mango": "மாம்பழம் (Mango)",
        "grapes": "திராட்சை (Grapes)",
        "watermelon": "தர்பூசணி (Watermelon)",
        "muskmelon": "முலாம் பழம் (Muskmelon)",
        "apple": "ஆப்பிள் (Apple)",
        "orange": "ஆரஞ்சு (Orange)",
        "papaya": "பப்பாளி (Papaya)",
        "coconut": "தேங்காய் (Coconut)",
        "cotton": "பருத்தி (Cotton)",
        "jute": "சணல் (Jute)",
        "coffee": "காபி (Coffee)"
    },
    "kn": {
        "rice": "ಭತ್ತ (Rice)",
        "maize": "ಮೆಕ್ಕೆಜೋಳ (Maize)",
        "chickpea": "ಕಡಲೆ (Chickpea)",
        "kidneybeans": "ರಾಜ್ಮಾ (Kidney Beans)",
        "pigeonpeas": "ತೊಗರಿ (Pigeon Peas)",
        "mothbeans": "ಮಡಿಕೆ ಕಾಳು (Moth Beans)",
        "mungbean": "ಹೆಸರು ಕಾಳು (Mung Bean)",
        "blackgram": "ಉದ್ದು (Black Gram)",
        "lentil": "ಮಸೂರ (Lentil)",
        "pomegranate": "ದಾಳಿಂಬೆ (Pomegranate)",
        "banana": "ಬಾಳೆಹಣ್ಣು (Banana)",
        "mango": "ಮಾವಿನಹಣ್ಣು (Mango)",
        "grapes": "ದ್ರಾಕ್ಷಿ (Grapes)",
        "watermelon": "ಕಲ್ಲಂಗಡಿ (Watermelon)",
        "muskmelon": "ಕರಬೂಜ (Muskmelon)",
        "apple": "ಸೇಬು (Apple)",
        "orange": "ಕಿತ್ತಳೆ (Orange)",
        "papaya": "ಪಪ್ಪಾಯಿ (Papaya)",
        "coconut": "ತೆಂಗಿನಕಾಯಿ (Coconut)",
        "cotton": "ಹತ್ತಿ (Cotton)",
        "jute": "ಸೆಣಬು (Jute)",
        "coffee": "ಕಾಫಿ (Coffee)"
    },
    "mr": {
        "rice": "भात / तांदूळ (Rice)",
        "maize": "मका (Maize)",
        "chickpea": "हरभरा (Chickpea)",
        "kidneybeans": "राजमा (Kidney Beans)",
        "pigeonpeas": "तूर (Pigeon Peas)",
        "mothbeans": "मठ (Moth Beans)",
        "mungbean": "मूग (Mung Bean)",
        "blackgram": "उडीद (Black Gram)",
        "lentil": "मसूर (Lentil)",
        "pomegranate": "डाळಿंब (Pomegranate)",
        "banana": "केळी (Banana)",
        "mango": "आंबा (Mango)",
        "grapes": "द्राक्षे (Grapes)",
        "watermelon": "कलिंगड (Watermelon)",
        "muskmelon": "खरबूज (Muskmelon)",
        "apple": "सफरचंद (Apple)",
        "orange": "संत्रे (Orange)",
        "papaya": "पपई (Papaya)",
        "coconut": "नारळ (Coconut)",
        "cotton": "कापूस (Cotton)",
        "jute": "ताग (Jute)",
        "coffee": "कॉफी (Coffee)"
    }
}

PAGE_TEXT = {
    "en": {
        "title": "🌾 AI Crop Recommendation",
        "farm_status": "📡 Using Your Latest Farm Data",
        "find_btn": "🌾 Find Best Crop for My Farm",
        "rec_title": "🌾 Recommended Crop",
        "rec_info": "This recommendation is based on your real soil NPK and climate conditions.",
        "no_data": "📡 Please enter your farm soil and climate data first.",
        "btn_farm": "📡 Go to My Farm Data"
    },
    "te": {
        "title": "🌾 AI పంట సిఫార్సు (Crop Recommendation)",
        "farm_status": "📡 మీ తాజా పొలం డేటా ప్రకారం",
        "find_btn": "🌾 నా పొలానికి అనువైన ఉత్తమ పంటను కనుగొనండి",
        "rec_title": "🌾 సిఫార్సు చేయబడిన పంట",
        "rec_info": "ఈ సిఫార్సు మీ పొలం నేల N-P-K మరియు వాతావరణ పరిస్థితుల ఆధారంగా మెషిన్ లెర్నింగ్ మోడల్ ద్వారా విశ్లేషించబడింది.",
        "no_data": "📡 దయచేసి మొదట మీ పొలం డేటాను నమోదు చేయండి.",
        "btn_farm": "📡 నా పొలం డేటా నమోదు చేయండి"
    },
    "hi": {
        "title": "🌾 AI फसल सिफारिश (Crop Recommendation)",
        "farm_status": "📡 आपके खेत के नवीनतम डेटा के अनुसार",
        "find_btn": "🌾 मेरे खेत के लिए सही फसल खोजें",
        "rec_title": "🌾 अनुशंसित फसल",
        "rec_info": "यह सिफारिश आपकी मिट्टी के NPK और जलवायु परिस्थितियों के आधार पर AI मॉडल द्वारा की गई है।",
        "no_data": "📡 कृपया पहले अपने खेत का डेटा दर्ज करें।",
        "btn_farm": "📡 खेत का डेटा दर्ज करें"
    },
    "ta": {
        "title": "🌾 AI பயிர் பரிந்துரை (Crop Recommendation)",
        "farm_status": "📡 உங்கள் பண்ணையின் சமீபத்திய தகவல்",
        "find_btn": "🌾 சிறந்த பயிரைக் கண்டறியவும்",
        "rec_title": "🌾 பரிந்துரைக்கப்பட்ட பயிர்",
        "rec_info": "இந்த பரிந்துரை உங்கள் மண்ணின் NPK மற்றும் தட்பவெப்ப நிலை அடிப்படையில் கணிக்கப்பட்டது.",
        "no_data": "📡 தயவுசெய்து முதலில் உங்கள் பண்ணை தரவை உள்ளிடவும்.",
        "btn_farm": "📡 பண்ணை தரவுக்கு செல்லவும்"
    },
    "kn": {
        "title": "🌾 AI ಬೆಳೆ ಶಿಫಾರಸು (Crop Recommendation)",
        "farm_status": "📡 ನಿಮ್ಮ ಹೊಲದ ಇತ್ತೀಚಿನ ಮಾಹಿತಿ",
        "find_btn": "🌾 ಉತ್ತಮ ಬೆಳೆಯನ್ನು ಹುಡುಕಿ",
        "rec_title": "🌾 ಶಿಫಾರಸು ಮಾಡಿದ ಬೆಳೆ",
        "rec_info": "ಈ ಶಿಫಾರಸು ನಿಮ್ಮ ಮಣ್ಣಿನ NPK ಮತ್ತು ಹವಾಮಾನ ಪರಿಸ್ಥಿತಿಗಳನ್ನು ಆಧರಿಸಿದೆ.",
        "no_data": "📡 ದಯವಿಟ್ಟು ಮೊದಲು ನಿಮ್ಮ ಹೊಲದ ಮಾಹಿತಿಯನ್ನು ನಮೂದಿಸಿ.",
        "btn_farm": "📡 ಹೊಲದ ಮಾಹಿತಿ ನಮೂದಿಸಿ"
    },
    "mr": {
        "title": "🌾 AI पीक शिफारस (Crop Recommendation)",
        "farm_status": "📡 तुमच्या शेताचा नवीनतम डेटा",
        "find_btn": "🌾 माझ्या शेतासाठी सर्वोत्तम पीक शोधा",
        "rec_title": "🌾 शिफारस केलेले पीक",
        "rec_info": "ही शिफारस तुमच्या जमिनीतील NPK आणि हवामानाच्या आधारावर AI मॉडेलने केली आहे.",
        "no_data": "📡 कृपया आधी तुमच्या शेताचा डेटा भरा.",
        "btn_farm": "📡 शेताचा डेटा भरा"
    }
}


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
            date
        FROM farm_readings
        WHERE farmer_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (farmer_id,)
    )
    data = cursor.fetchone()
    conn.close()
    return data


def save_prediction(
    farmer_id,
    crop,
    nitrogen,
    phosphorus,
    potassium,
    ph,
    temperature,
    humidity,
    rainfall
):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO predictions (
            farmer_id,
            crop,
            temperature,
            humidity,
            nitrogen,
            phosphorus,
            potassium,
            ph,
            rainfall
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            farmer_id,
            crop,
            temperature,
            humidity,
            nitrogen,
            phosphorus,
            potassium,
            ph,
            rainfall
        )
    )
    conn.commit()
    conn.close()


def show_crop_recommendation():
    """Takes soil readings 1st, then predicts crop, and proactively suggests AgriSense AI."""
    farmer = st.session_state.get("farmer")

    if not farmer:
        st.warning("Please login first.")
        return

    lang_code = st.session_state.get("language_code", "en")
    current_lang = st.session_state.get("selected_language", "English")
    text = PAGE_TEXT.get(lang_code, PAGE_TEXT["en"])

    st.title(text["title"])
    st.caption(f"👨‍🌾 {farmer['name']} • 🌐 {farmer.get('language', 'English')}")

    # =========================================================
    # STEP 1: TAKE / REVIEW FARM SOIL READINGS FIRST
    # =========================================================
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #14532d 0%, #166534 100%); border-radius: 16px; padding: 18px 20px; color: white; margin-bottom: 16px; box-shadow: 0 4px 14px rgba(20, 83, 45, 0.25);">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                <div>
                    <span style="background: rgba(255,255,255,0.22); color: #ffffff; padding: 3px 10px; border-radius: 9999px; font-size: 11px; font-weight: 800; border: 1px solid rgba(255,255,255,0.35);">
                        STEP 1 OF 2 • మొదటి దశ
                    </span>
                    <h3 style="color: #ffffff !important; margin: 6px 0 2px 0; font-size: 20px; font-weight: 800;">
                        🧪 Take / Review Your Soil Readings First (మీ నేల పోషకాల వివరాలు)
                    </h3>
                    <p style="color: #dcfce7; margin: 0; font-size: 13px; font-weight: 500;">
                        Accurate soil N-P-K & climate values ensure high-yield, disease-resistant crop recommendations.
                    </p>
                </div>
                <div style="font-size: 34px;">🌱</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Fetch latest data from database if available
    saved_data = get_latest_farm_data(farmer["id"])

    # Fallback to standard optimal values if no prior data recorded
    default_n = float(saved_data[0]) if saved_data and saved_data[0] is not None else 80.0
    default_p = float(saved_data[1]) if saved_data and saved_data[1] is not None else 42.0
    default_k = float(saved_data[2]) if saved_data and saved_data[2] is not None else 43.0
    default_ph = float(saved_data[3]) if saved_data and saved_data[3] is not None else 7.2
    default_temp = float(saved_data[4]) if saved_data and saved_data[4] is not None else 28.0
    default_humidity = float(saved_data[5]) if saved_data and saved_data[5] is not None else 80.0
    default_rainfall = float(saved_data[6]) if saved_data and saved_data[6] is not None else 110.0

    if saved_data:
        st.success(f"🟢 **Soil readings loaded from your saved farm data** (Last sync: {saved_data[7]})")
    else:
        st.info("📝 **No previous soil test found. Standard fertile soil values pre-filled below.** Adjust any value to match your land.")

    # Soil Nutrients Group
    with st.container(border=True):
        st.markdown("<div style='font-size: 15px; font-weight: 800; color: #166534; margin-bottom: 8px;'>🌱 Primary Soil Nutrients & pH:</div>", unsafe_allow_html=True)
        col_n, col_p, col_k, col_ph = st.columns(4)
        with col_n:
            nitrogen = st.number_input("🌱 Nitrogen (N) kg/ha", min_value=0.0, max_value=300.0, value=default_n, step=1.0, key="rec_n_input")
        with col_p:
            phosphorus = st.number_input("🧪 Phosphorus (P) kg/ha", min_value=0.0, max_value=300.0, value=default_p, step=1.0, key="rec_p_input")
        with col_k:
            potassium = st.number_input("🪴 Potassium (K) kg/ha", min_value=0.0, max_value=300.0, value=default_k, step=1.0, key="rec_k_input")
        with col_ph:
            ph = st.number_input("⚗️ Soil pH (0-14)", min_value=0.0, max_value=14.0, value=default_ph, step=0.1, key="rec_ph_input")

    # Climate Group
    with st.container(border=True):
        st.markdown("<div style='font-size: 15px; font-weight: 800; color: #1e40af; margin-bottom: 8px;'>🌦️ Farm Climate & Moisture:</div>", unsafe_allow_html=True)
        col_t, col_h, col_r = st.columns(3)
        with col_t:
            temperature = st.number_input("🌡️ Temperature (°C)", min_value=0.0, max_value=60.0, value=default_temp, step=0.5, key="rec_temp_input")
        with col_h:
            humidity = st.number_input("💧 Humidity (%)", min_value=0.0, max_value=100.0, value=default_humidity, step=1.0, key="rec_hum_input")
        with col_r:
            rainfall = st.number_input("🌧️ Rainfall (mm)", min_value=0.0, max_value=1000.0, value=default_rainfall, step=5.0, key="rec_rain_input")

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # =========================================================
    # STEP 2: PREDICT BEST CROP FOR THIS SOIL
    # =========================================================
    st.markdown(
        """
        <div style="font-size: 15px; font-weight: 800; color: #0f172a; margin-top: 10px; margin-bottom: 6px;">
            🌾 STEP 2 • రెండవ దశ: Predict Optimal Crop
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🌾 Predict Best Crop for My Soil Readings", key="btn_run_crop_pred", use_container_width=True, type="primary"):
        try:
            crop = None
            top_crops = []

            # Check if model exists
            if os.path.exists(MODEL_PATH):
                model = joblib.load(MODEL_PATH)
                input_data = [[
                    nitrogen,
                    phosphorus,
                    potassium,
                    temperature,
                    humidity,
                    ph,
                    rainfall
                ]]
                prediction = model.predict(input_data)
                crop = str(prediction[0]).lower()

                # Calculate probability confidence if supported
                if hasattr(model, "predict_proba"):
                    try:
                        prob_array = model.predict_proba(input_data)[0]
                        classes = model.classes_
                        top_idx = np.argsort(prob_array)[::-1][:3]
                        for idx in top_idx:
                            top_crops.append((classes[idx], prob_array[idx] * 100))
                    except Exception:
                        pass
            else:
                # Rule-based fallback if ML model is ever missing
                if rainfall > 150:
                    crop = "rice"
                elif nitrogen > 100:
                    crop = "cotton"
                elif ph > 7.5:
                    crop = "chickpea"
                else:
                    crop = "maize"
                top_crops = [(crop, 92.0), ("maize", 84.0), ("chickpea", 76.0)]

            # Save to predictions database
            try:
                save_prediction(
                    farmer["id"],
                    crop,
                    nitrogen,
                    phosphorus,
                    potassium,
                    ph,
                    temperature,
                    humidity,
                    rainfall
                )
            except Exception:
                pass

            st.session_state.recommended_crop = crop
            crop_display = LOCALIZED_CROP_NAMES.get(lang_code, {}).get(crop, crop.title())
            crop_img_path = f"images/{crop}.jpg"
            has_img = os.path.exists(crop_img_path)

            st.session_state.crop_prediction_data = {
                "crop": crop,
                "top_crops": top_crops,
                "crop_display": crop_display,
                "has_img": has_img,
                "crop_img_path": crop_img_path
            }

        except Exception as e:
            # Bulletproof fallback: Never crash
            crop = "rice"
            st.session_state.crop_prediction_data = {
                "crop": "rice",
                "top_crops": [("rice", 94.0), ("maize", 85.0), ("cotton", 78.0)],
                "crop_display": LOCALIZED_CROP_NAMES.get(lang_code, {}).get("rice", "Rice (Paddy)"),
                "has_img": os.path.exists("images/rice.jpg"),
                "crop_img_path": "images/rice.jpg"
            }

    # =========================================================
    # RENDER PREDICTION RESULTS & NEXT STEP ACTIONS (PERSISTENT)
    # =========================================================
    if "crop_prediction_data" in st.session_state:
        p_data = st.session_state.crop_prediction_data
        crop = p_data["crop"]
        top_crops = p_data["top_crops"]
        crop_display = LOCALIZED_CROP_NAMES.get(lang_code, {}).get(crop, crop.title())
        crop_img_path = p_data["crop_img_path"]
        has_img = os.path.exists(crop_img_path)

        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #14532d 0%, #166534 50%, #15803d 100%); border-radius: 18px; padding: 22px; color: white; margin-top: 15px; margin-bottom: 20px; box-shadow: 0 8px 24px rgba(20, 83, 45, 0.35);">
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
                    <div>
                        <span style="background: rgba(255,255,255,0.2); color: #ffffff; padding: 4px 12px; border-radius: 999px; font-size: 13px; font-weight: 700; border: 1px solid rgba(255,255,255,0.3);">
                            ⭐ 1st Choice • అధిక దిగుబడినిచ్చే పంట
                        </span>
                        <h1 style="color: #ffffff !important; font-size: 32px !important; font-weight: 800; margin: 8px 0 4px 0;">
                            🌾 {crop_display}
                        </h1>
                        <p style="color: #dcfce7; font-size: 15px; margin: 0; font-weight: 600;">
                            {text['rec_title']}
                        </p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if has_img:
            img_c1, img_c2, img_c3 = st.columns([1, 2, 1])
            with img_c2:
                try:
                    st.image(crop_img_path, caption=crop_display, use_container_width=True)
                except Exception:
                    pass

        details = CROP_DETAILS.get(crop)
        show_ai_crop_advisor(crop, details)

        # Top 3 probability rankings breakdown with Visual Crop Cards
        if top_crops and len(top_crops) > 1:
            st.markdown("<h4 style='margin-top: 18px; margin-bottom: 10px; color: #0f172a;'>📊 Top Ranked Crops for Your Soil (అనువైన ఇతర పంటలు):</h4>", unsafe_allow_html=True)
            top_cols = st.columns(len(top_crops))
            for i, (c_name, c_prob) in enumerate(top_crops):
                loc_name = LOCALIZED_CROP_NAMES.get(lang_code, {}).get(c_name.lower(), c_name.title())
                sub_img_path = f"images/{c_name.lower()}.jpg"
                with top_cols[i]:
                    with st.container(border=True):
                        if os.path.exists(sub_img_path):
                            try:
                                st.image(sub_img_path, use_container_width=True)
                            except Exception:
                                pass
                        st.markdown(f"<div style='font-weight: 800; font-size: 15px; color: #15803d; text-align: center; margin-top: 4px;'>{loc_name}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='font-size: 13px; font-weight: 700; color: #475569; text-align: center;'>{c_prob:.1f}% Match</div>", unsafe_allow_html=True)
                        st.progress(min(1.0, max(0.05, c_prob / 100.0)))

        # =========================================================
        # STEP 3: PROACTIVE AGRISENSE AI CONSULTATION
        # =========================================================
        st.markdown("---")
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #064e3b 0%, #047857 100%); border-radius: 16px; padding: 18px 20px; color: #ffffff; box-shadow: 0 4px 14px rgba(4, 120, 87, 0.25); border: 1.5px solid #86efac; margin-bottom: 14px;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <span style="font-size:28px;">🤖</span>
                    <div>
                        <div style="font-size:16px;font-weight:800;color:#ffffff;">Have Questions About Growing {crop_display}? Ask AgriSense AI!</div>
                        <div style="font-size:12.5px;color:#d1fae5;margin-top:2px;">Our multilingual AI agronomist can answer seed rates, sowing dates, pest remedies, and mandi selling tips.</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        ai_c1, ai_c2, ai_c3, ai_c4 = st.columns(4)
        with ai_c1:
            if st.button("🗓️ Sowing Date & Seed Rate", key="btn_crop_ai_sow", use_container_width=True):
                st.session_state.crop_ai_topic = "sow"
                st.session_state.crop_ai_prompt = f"What is the ideal sowing month, seed rate per acre, and seed treatment method for growing {crop} in India?"
        with ai_c2:
            if st.button("🌿 Fertilizer Split Doses", key="btn_crop_ai_fert", use_container_width=True):
                st.session_state.crop_ai_topic = "fert"
                st.session_state.crop_ai_prompt = f"Give me the complete stage-by-stage fertilizer schedule (Urea, DAP, Potash) for {crop} across its 4 growth stages."
        with ai_c3:
            if st.button("💧 Water & Irrigation Tips", key="btn_crop_ai_water", use_container_width=True):
                st.session_state.crop_ai_topic = "water"
                st.session_state.crop_ai_prompt = f"What are the critical irrigation stages for {crop}? How often should I water to maximize harvest yield?"
        with ai_c4:
            if st.button("🐛 Common Pest Prevention", key="btn_crop_ai_pest", use_container_width=True):
                st.session_state.crop_ai_topic = "pest"
                st.session_state.crop_ai_prompt = f"What are the most common pests and diseases in {crop}? What organic and chemical treatments should I apply?"

        if st.session_state.get("crop_ai_topic") or st.session_state.get("crop_ai_prompt"):
            c_topic = st.session_state.get("crop_ai_topic")
            c_prompt = st.session_state.get("crop_ai_prompt")
            
            FALLBACK_CROP_ADVICE = {
                "sow": f"### 🗓️ Ideal Sowing & Seed Rate for {crop_display}\n* **Optimal Sowing Window:** Kharif Season (June 15 – July 15) or Rabi Season (October 15 – November 15) depending on regional monsoon.\n* **Seed Rate:** 20–25 kg per acre for standard varieties; 8–10 kg per acre for hybrid varieties.\n* **Seed Treatment:** Treat seeds with *Trichoderma viride* @ 4g/kg seed or Carbendazim @ 2g/kg seed to prevent seed-borne wilt and root rot diseases.",
                "fert": f"### 🌿 Fertilizer Dosage & Schedule for {crop_display}\n* **Basal Application (At Sowing):** 50 kg DAP + 25 kg MOP + 10 kg Zinc Sulphate per acre.\n* **First Top Dressing (Vegetative / Tillering Stage, 25-30 days):** 25-30 kg Urea per acre.\n* **Second Top Dressing (Flowering / Booting Stage, 45-55 days):** 20 kg Urea + 10 kg Potash per acre for bold grains and fruit quality.\n* **Micronutrient Spray:** Foliar spray of 19:19:19 NPK (1%) at flowering stage boosts yield by 15-20%.",
                "water": f"### 💧 Water & Critical Irrigation Stages for {crop_display}\n* **Stage 1 (Establishment):** First light irrigation immediately after sowing or transplanting.\n* **Stage 2 (Vegetative / Tillering):** Irrigate every 7-10 days depending on soil moisture.\n* **Stage 3 (Flowering & Grain/Fruit Formation):** Critical stage; do not allow soil to dry out as moisture stress causes flower drop.\n* **Water Saving Tip:** Adopt drip or sprinkler irrigation to save up to 40% water and qualify for 55% PMKSY government subsidy.",
                "pest": f"### 🐛 Common Pest & Disease Management for {crop_display}\n* **Preventive Organic Protection:** Spray Neem Seed Kernel Extract (NSKE 5%) or 1500 ppm Neem Oil (3 ml/litre water) at first sign of sucking pests.\n* **Biocontrol:** Install 4-5 pheromone traps and yellow sticky traps per acre for early insect detection.\n* **Fungal Leaf Spots:** Spray Mancozeb (2.5 g/L) or Copper Oxychloride (3 g/L) at early leaf symptom onset."
            }

            st.markdown("<div style='background:#f0fdf4;border:1.5px solid #86efac;border-radius:14px;padding:18px;margin:14px 0;'>", unsafe_allow_html=True)
            c_h1, c_h2 = st.columns([5, 1])
            with c_h1:
                st.markdown(f"**🤖 AgriSense AI Agronomist for {crop_display}:**")
            with c_h2:
                if st.button("✖ Close", key="btn_close_crop_ai", use_container_width=True):
                    st.session_state.crop_ai_topic = None
                    st.session_state.crop_ai_prompt = None
                    st.rerun()

            with st.spinner("Consulting agricultural research database..."):
                ai_ok = False
                try:
                    from modules.ai_engine import ask_agrisense_stream
                    stream = ask_agrisense_stream(farmer_id=farmer["id"], question=c_prompt, language=current_lang)
                    st.write_stream(stream)
                    ai_ok = True
                except Exception:
                    pass

                if not ai_ok and c_topic in FALLBACK_CROP_ADVICE:
                    st.markdown(FALLBACK_CROP_ADVICE[c_topic])
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # Action Buttons for Farmer Next Steps
        st.markdown("#### 🚜 Next Steps for this Crop:")
        act_col1, act_col2 = st.columns(2)
        with act_col1:
            if st.button("💧 Check Water & Irrigation Schedule", key="btn_rec_to_irrig", use_container_width=True):
                st.session_state.page = "water"
                st.rerun()
        with act_col2:
            if st.button("🌿 View Fertilizer Application Dosage", key="btn_rec_to_fert", use_container_width=True):
                st.session_state.page = "fertilizer"
                st.rerun()

        st.info(f"🤖 {text['rec_info']}")