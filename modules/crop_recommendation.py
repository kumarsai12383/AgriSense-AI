import streamlit as st
import sqlite3
import joblib
from modules.ai_crop_advisor import show_ai_crop_advisor
from modules.crop_details import CROP_DETAILS

DB_PATH = "database/agrisense.db"
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
    conn = sqlite3.connect(DB_PATH)
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
    conn = sqlite3.connect(DB_PATH)
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
    farmer = st.session_state.get("farmer")

    if not farmer:
        st.warning("Please login first.")
        return

    lang_code = st.session_state.get("language_code", "en")
    text = PAGE_TEXT.get(lang_code, PAGE_TEXT["en"])

    st.title(text["title"])
    st.caption(f"👨‍🌾 {farmer['name']} • 🌐 {farmer.get('language', 'English')}")
    st.markdown("---")

    data = get_latest_farm_data(farmer["id"])

    if not data:
        st.info(text["no_data"])
        if st.button(text["btn_farm"], use_container_width=True):
            st.session_state.page = "farm"
            st.rerun()
        return

    (
        nitrogen,
        phosphorus,
        potassium,
        ph,
        temperature,
        humidity,
        rainfall,
        date
    ) = data

    st.subheader(text["farm_status"])
    st.caption(f"Last recorded: {date}")

    col1, col2, col3 = st.columns(3)
    col1.metric("🌱 N (Nitrogen)", nitrogen)
    col2.metric("🧪 P (Phosphorus)", phosphorus)
    col3.metric("🪴 K (Potassium)", potassium)

    col4, col5, col6 = st.columns(3)
    col4.metric("⚗️ Soil pH", ph)
    col5.metric("🌡️ Temperature", f"{temperature} °C")
    col6.metric("💧 Humidity", f"{humidity} %")

    st.metric("🌧️ Rainfall", f"{rainfall} mm")
    st.markdown("---")

    if st.button(text["find_btn"], key="btn_run_crop_pred", use_container_width=True):
        try:
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

            st.session_state.recommended_crop = crop
            
            # Localized crop display
            crop_display = LOCALIZED_CROP_NAMES.get(lang_code, {}).get(crop, crop.title())

            st.success(f"{text['rec_title']}: **{crop_display}**")

            details = CROP_DETAILS.get(crop)
            show_ai_crop_advisor(crop, details)
            
            st.markdown("---")
            st.info(f"🤖 {text['rec_info']}")

        except Exception as e:
            st.error(f"Prediction Error: {e}")