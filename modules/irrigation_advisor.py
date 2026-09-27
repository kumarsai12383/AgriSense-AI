import os
import json
import sqlite3
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

from database.database import connect, DB_PATH


# =========================================================
# DATABASE ACCESS HELPERS
# =========================================================

def get_latest_farm_reading(farmer_id):
    """Retrieve the latest farm reading from SQLite database."""
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM farm_readings
            WHERE farmer_id = ?
            ORDER BY id DESC
            LIMIT 1
        """, (farmer_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    except Exception:
        return None


def get_latest_predicted_crop(farmer_id):
    """Retrieve the latest recommended crop for the farmer."""
    try:
        conn = connect()
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
        return str(row[0]).lower().strip() if row else "rice"
    except Exception:
        return "rice"


# =========================================================
# CROP-SPECIFIC IRRIGATION SCHEDULES & WATER REQUIREMENTS
# =========================================================

CROP_IRRIGATION_DATA = {
    "rice": {
        "water_req": "1200 - 1500 mm",
        "method": "Shallow Flooding / Alternate Wetting & Drying (AWD)",
        "freq_days": "Continuous 2-5 cm standing water (Tillering to Flowering)",
        "critical_stages": [
            {"stage": "Transplanting / Establishment (0-15 DAS)", "depth": "2-3 cm standing water", "freq": "Daily check", "importance": "Crucial for root anchoring"},
            {"stage": "Active Tillering (20-40 DAS)", "depth": "3-5 cm standing water", "freq": "Every 2-3 days", "importance": "Promotes productive tillers"},
            {"stage": "Panicle Initiation & Booting (45-65 DAS)", "depth": "5 cm standing water", "freq": "Critical - Never allow drying", "importance": "Determines grain count"},
            {"stage": "Flowering & Milk Stage (70-90 DAS)", "depth": "3-5 cm depth", "freq": "Every 3-4 days", "importance": "Prevents empty chaffy grains"},
            {"stage": "Grain Maturity (100+ DAS)", "depth": "Drain completely 10 days before harvest", "freq": "Withhold water", "importance": "Facilitates uniform ripening"}
        ],
        "liters_per_acre": "25,000 - 35,000 Liters / irrigation"
    },
    "maize": {
        "water_req": "500 - 750 mm",
        "method": "Furrow Irrigation / Drip System",
        "freq_days": "Every 6 - 8 days (Soil moisture > 50%)",
        "critical_stages": [
            {"stage": "Germination & Seedling (0-15 DAS)", "depth": "25 - 30 mm", "freq": "Once at sowing + 1 light", "importance": "Uniform plant stand"},
            {"stage": "Knee-High Stage (25-35 DAS)", "depth": "40 - 50 mm", "freq": "Every 7 days", "importance": "Rapid vegetative growth"},
            {"stage": "Tasseling & Silking (45-60 DAS)", "depth": "50 - 60 mm", "freq": "Critical - Every 5-6 days", "importance": "Essential for complete pollination"},
            {"stage": "Grain Filling / Dough (65-85 DAS)", "depth": "40 - 50 mm", "freq": "Every 7-8 days", "importance": "Maximizes kernel size and weight"}
        ],
        "liters_per_acre": "18,000 - 22,000 Liters / irrigation"
    },
    "cotton": {
        "water_req": "700 - 900 mm",
        "method": "Alternate Furrow / Drip Irrigation",
        "freq_days": "Every 8 - 12 days",
        "critical_stages": [
            {"stage": "Germination & Early Vegetative (0-25 DAS)", "depth": "30 mm", "freq": "Light irrigation", "importance": "Deep taproot development"},
            {"stage": "Square Formation (35-55 DAS)", "depth": "45 mm", "freq": "Every 8-10 days", "importance": "Prevents early flower shedding"},
            {"stage": "Peak Flowering & Boll Setting (60-95 DAS)", "depth": "55 mm", "freq": "Critical - Every 6-8 days", "importance": "Prevents square and boll drop"},
            {"stage": "Boll Maturation & Bursting (100-130 DAS)", "depth": "30 mm", "freq": "Stop 15 days prior to picking", "importance": "Prevents staining of cotton fiber"}
        ],
        "liters_per_acre": "16,000 - 20,000 Liters / irrigation"
    },
    "chickpea": {
        "water_req": "250 - 400 mm",
        "method": "Sprinkler / Light Furrow",
        "freq_days": "1 to 2 critical irrigations only",
        "critical_stages": [
            {"stage": "Pre-sowing (0 DAS)", "depth": "50 mm", "freq": "Heavy pre-sowing soaking", "importance": "Good seedbed moisture"},
            {"stage": "Pre-Flowering / Branching (30-40 DAS)", "depth": "35 mm", "freq": "1st post-sowing irrigation", "importance": "Promotes branching & flower buds"},
            {"stage": "Pod Development (65-75 DAS)", "depth": "35 mm", "freq": "2nd irrigation if no winter rain", "importance": "Full grain filling"}
        ],
        "liters_per_acre": "12,000 - 15,000 Liters / irrigation"
    },
    "pigeonpeas": {
        "water_req": "600 - 750 mm",
        "method": "Broad Bed & Furrow (BBF) / Drip",
        "freq_days": "Every 12 - 15 days during dry spells",
        "critical_stages": [
            {"stage": "Seedling (15-25 DAS)", "depth": "30 mm", "freq": "If monsoon dry spell exceeds 15 days", "importance": "Prevents seedling wilting"},
            {"stage": "Flower Initiation (70-85 DAS)", "depth": "45 mm", "freq": "Critical", "importance": "Reduces flower drop by 40%"},
            {"stage": "Pod Development (100-120 DAS)", "depth": "45 mm", "freq": "1 irrigation", "importance": "Increases 100-seed weight"}
        ],
        "liters_per_acre": "14,000 - 18,000 Liters / irrigation"
    },
    "banana": {
        "water_req": "1500 - 2200 mm",
        "method": "Daily Drip Fertigation (15-20 Liters/plant/day)",
        "freq_days": "Daily or Alternate Day Drip",
        "critical_stages": [
            {"stage": "Early Vegetative (Months 1-3)", "depth": "10-12 L/plant/day", "freq": "Daily", "importance": "Root system & pseudostem growth"},
            {"stage": "Grand Growth Stage (Months 4-6)", "depth": "16-20 L/plant/day", "freq": "Daily", "importance": "Leaf area expansion"},
            {"stage": "Shooting & Bunch Emergence (Months 7-8)", "depth": "20-25 L/plant/day", "freq": "Daily - Never stress", "importance": "Determines number of hands and fingers"},
            {"stage": "Fruit Maturation (Months 9-11)", "depth": "15 L/plant/day", "freq": "Stop 7 days before harvest", "importance": "Improves fruit shelf life"}
        ],
        "liters_per_acre": "22,000 - 28,000 Liters / acre / day"
    },
    "watermelon": {
        "water_req": "400 - 600 mm",
        "method": "Drip Irrigation with Plastic Mulch",
        "freq_days": "Every 2 - 3 days (Drip: 2-3 hours)",
        "critical_stages": [
            {"stage": "Sowing & Germination (0-10 DAS)", "depth": "Light daily moisture", "freq": "Daily until emergence", "importance": "Quick uniform sprouting"},
            {"stage": "Vine Elongation (15-35 DAS)", "depth": "25 mm depth", "freq": "Every 3 days", "importance": "Strong canopy development"},
            {"stage": "Flowering & Fruit Set (40-55 DAS)", "depth": "35 mm depth", "freq": "Every 2 days", "importance": "Prevents blossom drop & hollow heart"},
            {"stage": "Fruit Ripening (65-80 DAS)", "depth": "Withhold/Reduce by 60%", "freq": "Light watering only", "importance": "Maximizes sweetness (Brix %) & prevents splitting"}
        ],
        "liters_per_acre": "15,000 - 18,000 Liters / irrigation"
    }
}

# Default for crops not explicitly mapped
DEFAULT_IRRIGATION = {
    "water_req": "500 - 800 mm",
    "method": "Furrow / Drip Irrigation",
    "freq_days": "Every 5 - 7 days based on topsoil dryness",
    "critical_stages": [
        {"stage": "Initial Vegetative Stage", "depth": "30 mm", "freq": "Every 5-7 days", "importance": "Healthy root establishment"},
        {"stage": "Flowering / Reproductive Stage", "depth": "45 mm", "freq": "Critical - Keep moist", "importance": "Flower retention & seed setting"},
        {"stage": "Maturity / Grain Development", "depth": "35 mm", "freq": "Every 7-10 days", "importance": "Quality and yield development"}
    ],
    "liters_per_acre": "18,000 - 22,000 Liters / irrigation"
}


# =========================================================
# MULTILINGUAL IRRIGATION INTELLIGENCE & SPEECH SCRIPTS
# =========================================================

IRRIG_LANG = {
    "en": {
        "title": "💧 Smart Irrigation Advisor",
        "sub": "Precision watering intelligence & schedule tailored to your soil moisture & crop",
        "voice_title": "🔊 Listen to Today's Irrigation Advice (20s)",
        "voice_sub": "Audio advice in clear Indian voice — Tap Play to hear exact watering plan",
        "btn_play": "🔊 Play Voice Advice",
        "btn_stop": "⏹ Stop",
        "speech_lang": "en-IN",
        "calc_title": "💧 Water Volume & Pump Run-Time Calculator",
        "calc_acres": "Select Farm Size (Acres):",
        "calc_pump": "Select Pump Power (HP):",
        "calc_result": "Estimated Water Volume:",
        "calc_time": "Estimated Pumping Time:",
        "schedule_title": "📅 Critical Crop Growth Stages & Watering Schedule",
        "status_urgent": "🔴 URGENT: Irrigate Field Today",
        "status_soon": "🟡 PLAN IRRIGATION: Irrigate within 24-48 Hours",
        "status_ok": "🟢 OPTIMAL: Soil Moisture is Sufficient — No Irrigation Needed Today",
        "status_wet": "🔵 WATERLOGGED: Soil is Saturated — Withhold Watering & Drain excess",
        "faq_title": "❓ Frequently Asked Irrigation Questions & Doubts"
    },
    "te": {
        "title": "💧 స్మార్ట్ నీటిపారుదల సలహాదారు",
        "sub": "మీ పొలం నేల తేమ మరియు పంటకు అనుగుణంగా ఖచ్చితమైన నీటి యాజమాన్య సలహాలు",
        "voice_title": "🔊 నేటి నీటిపారుదల వాయిస్ సలహా వినండి (20 సెకన్లు)",
        "voice_sub": "స్పష్టమైన తెలుగు వాయిస్‌లో — నీరు పెట్టాలో లేదో తెలుసుకోవడానికి నొక్కండి",
        "btn_play": "🔊 సలహా వినండి (Play Audio)",
        "btn_stop": "⏹ ఆపండి",
        "speech_lang": "te-IN",
        "calc_title": "💧 నీటి పరిమాణం & మోటార్ రన్-టైమ్ కాలిక్యులేటర్",
        "calc_acres": "పొలం విస్తీర్ణం ఎంచుకోండి (ఎకరాలు):",
        "calc_pump": "మోటార్ సామర్థ్యం ఎంచుకోండి (HP):",
        "calc_result": "అవసరమైన మొత్తం నీరు:",
        "calc_time": "మోటార్ నడపవలసిన సమయం:",
        "schedule_title": "📅 పంట ముఖ్యమైన దశలు & నీటిపారుదల కాలపట్టిక",
        "status_urgent": "🔴 తక్షణం: ఈరోజే పొలానికి నీరు పెట్టండి (నేలలో తేమ చాలా తక్కువగా ఉంది)",
        "status_soon": "🟡 ప్రణాళిక: రాబోయే 24-48 గంటల్లో నీటిపారుదల చేయండి",
        "status_ok": "🟢 సరైన స్థితి: నేలలో తగినంత తేమ ఉంది — ఈరోజు నీరు పెట్టవలసిన అవసరం లేదు",
        "status_wet": "🔵 అధిక తేమ: నేలలో నీరు నిలిచి ఉంది — నీరు పెట్టవద్దు, అవసరమైతే నీటిని బయటకు పంపండి",
        "faq_title": "❓ రైతుల నీటిపారుదల సందేహాలు & సమాధానాలు"
    },
    "hi": {
        "title": "💧 स्मार्ट सिंचाई सलाहकार",
        "sub": "आपकी मिट्टी की नमी और फसल के अनुसार सटीक सिंचाई मार्गदर्शन",
        "voice_title": "🔊 आज की सिंचाई सलाह सुनें (20 सेकंड)",
        "voice_sub": "स्पष्ट हिंदी आवाज में — पानी देने का सही समय और मात्रा जानने के लिए दबाएं",
        "btn_play": "🔊 सलाह सुनें (Play Audio)",
        "btn_stop": "⏹ रोकें",
        "speech_lang": "hi-IN",
        "calc_title": "💧 पानी की मात्रा एवं मोटर समय कैलकुलेटर",
        "calc_acres": "खेत का आकार चुनें (एकड़):",
        "calc_pump": "मोटर की क्षमता चुनें (HP):",
        "calc_result": "आवश्यक कुल पानी:",
        "calc_time": "मोटर चलाने का अनुमानित समय:",
        "schedule_title": "📅 फसल की महत्वपूर्ण अवस्थाएं और सिंचाई समय-सारणी",
        "status_urgent": "🔴 आवश्यक: आज ही खेत में सिंचाई करें (मिट्टी में नमी बहुत कम है)",
        "status_soon": "🟡 योजना बनाएं: अगले 24-48 घंटों में सिंचाई करें",
        "status_ok": "🟢 उत्तम स्थिति: मिट्टी में पर्याप्त नमी है — आज पानी देने की जरूरत नहीं है",
        "status_wet": "🔵 अत्यधिक नमी: मिट्टी में पानी भरा है — पानी न दें और जल निकासी करें",
        "faq_title": "❓ किसानों के सिंचाई संबंधी सवाल और जवाब"
    },
    "ta": {
        "title": "💧 ஸ்மார்ட் பாசன ஆலோசகர்",
        "sub": "உங்கள் நிலத்தின் ஈரப்பதத்திற்கு ஏற்ப துல்லியமான பாசன வழிகாட்டுதல்",
        "voice_title": "🔊 இன்றைய பாசன ஆலோசனையைக் கேளுங்கள்",
        "voice_sub": "தெளிவான தமிழ் குரலில் — நீர் பாய்ச்சும் திட்டத்தை அறிய அழுத்தவும்",
        "btn_play": "🔊 ஆடியோவைக் கேளுங்கள்",
        "btn_stop": "⏹ நிறுத்து",
        "speech_lang": "ta-IN",
        "calc_title": "💧 பாசன நீர் மற்றும் மோட்டார் நேரம் கணக்கீடு",
        "calc_acres": "நிலத்தின் பரப்பளவு (ஏக்கர்):",
        "calc_pump": "மோட்டார் திறன் (HP):",
        "calc_result": "தேவையான மொத்த நீர்:",
        "calc_time": "மோட்டார் இயக்கும் நேரம்:",
        "schedule_title": "📅 பயிர் வளர்ச்சி நிலைகள் & நீர் பாசன அட்டவணை",
        "status_urgent": "🔴 அவசரம்: இன்றே பயிருக்கு நீர் பாய்ச்சவும்",
        "status_soon": "🟡 திட்டம்: அடுத்த 1-2 நாட்களில் நீர் பாய்ச்சவும்",
        "status_ok": "🟢 நன்று: மண்ணில் போதிய ஈரப்பதம் உள்ளது — இன்று நீர் தேவை இல்லை",
        "status_wet": "🔵 அதிக ஈரப்பதம்: நீர் தேங்கியுள்ளது — பாசனம் செய்ய வேண்டாம்",
        "faq_title": "❓ பாசனம் பற்றிய விவசாயிகளின் சந்தேகங்கள்"
    },
    "kn": {
        "title": "💧 ಸ್ಮಾರ್ಟ್ ನೀರಾವರಿ ಸಲಹೆಗಾರ",
        "sub": "ಮಣ್ಣಿನ ತೇವಾಂಶ ಮತ್ತು ಬೆಳೆಗೆ ತಕ್ಕಂತೆ ನಿಖರ ನೀರಾವರಿ ಮಾರ್ಗದರ್ಶನ",
        "voice_title": "🔊 ಇಂದಿನ ನೀರಾವರಿ ಧ್ವನಿ ಸಾರಾಂಶ ಆಲಿಸಿ",
        "voice_sub": "ಕನ್ನಡ ಧ್ವನಿಯಲ್ಲಿ — ನೀರು ಹಾಯಿಸುವ ಯೋಜನೆಯನ್ನು ತಿಳಿಯಲು ಒತ್ತಿ",
        "btn_play": "🔊 ಸಾರಾಂಶ ಆಲಿಸಿ",
        "btn_stop": "⏹ ನಿಲ್ಲಿಸಿ",
        "speech_lang": "kn-IN",
        "calc_title": "💧 ನೀರಿನ ಪ್ರಮಾಣ & ಪಂಪ್ ಸಮಯ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
        "calc_acres": "ಜಮೀನಿನ ವಿಸ್ತೀರ್ಣ (ಎಕರೆ):",
        "calc_pump": "ಪಂಪ್ ಸಾಮರ್ಥ್ಯ (HP):",
        "calc_result": "ಅಗತ್ಯವಿರುವ ಒಟ್ಟು ನೀರು:",
        "calc_time": "ಪಂಪ್ ಚಲಾಯಿಸುವ ಸಮಯ:",
        "schedule_title": "📅 ಬೆಳೆಯ ಪ್ರಮುಖ ಹಂತಗಳು ಮತ್ತು ನೀರಾವರಿ ವೇಳಾಪಟ್ಟಿ",
        "status_urgent": "🔴 ತುರ್ತು: ಇಂದೇ ಜಮೀನಿಗೆ ನೀರು ಹಾಯಿಸಿ",
        "status_soon": "🟡 ಯೋಜನೆ: ಮುಂದಿನ 24-48 ಗಂಟೆಗಳಲ್ಲಿ ನೀರು ಹಾಯಿಸಿ",
        "status_ok": "🟢 ಉತ್ತಮ: ಮಣ್ಣಿನಲ್ಲಿ ಸಾಕಷ್ಟು ತೇವಾಂಶವಿದೆ — ಇಂದು ನೀರು ಅಗತ್ಯವಿಲ್ಲ",
        "status_wet": "🔵 ಅಧಿಕ ನೀರು: ನೀರು ನಿಂತಿದೆ — ನೀರಾವರಿ ಮಾಡಬೇಡಿ",
        "faq_title": "❓ ನೀರಾವರಿ ಕುರಿತ ರೈತರ ಪ್ರಶ್ನೋತ್ತರಗಳು"
    },
    "mr": {
        "title": "💧 स्मार्ट सिंचन सल्लागार",
        "sub": "मातीतील ओलावा व पिकाच्या गरजेनुसार अचूक पाणी व्यवस्थापन",
        "voice_title": "🔊 आजचा सिंचन सल्ला ऐका",
        "voice_sub": "मराठी ऑडिओमध्ये — पाणी देण्याची वेळ व प्रमाण जाणून घेण्यासाठी दाबा",
        "btn_play": "🔊 सल्ला ऐका",
        "btn_stop": "⏹ थांबवा",
        "speech_lang": "mr-IN",
        "calc_title": "💧 पाण्याचे प्रमाण व मोटर वेळ कॅल्क्युलेटर",
        "calc_acres": "शेताचे क्षेत्रफळ (एकर):",
        "calc_pump": "मोटर क्षमता (HP):",
        "calc_result": "आवश्यक एकूण पाणी:",
        "calc_time": "मोटर चालवण्याची वेळ:",
        "schedule_title": "📅 पिकाच्या महत्त्वाच्या अवस्था व सिंचन वेळापत्रक",
        "status_urgent": "🔴 तातडीने: आजच शेताला पाणी द्या (ओलावा खूप कमी आहे)",
        "status_soon": "🟡 नियोजन: पुढील 1-2 दिवसांत पाणी द्या",
        "status_ok": "🟢 उत्तम: जमिनीत पुरेसा ओलावा आहे — आज पाणी देण्याची गरज नाही",
        "status_wet": "🔵 दलदल: जास्त पाणी साचले आहे — पाणी देऊ नका",
        "faq_title": "❓ सिंचनाविषयी शेतकऱ्यांचे नेहमीचे प्रश्न"
    }
}


# =========================================================
# MAIN IRRIGATION ADVISOR VIEW
# =========================================================

def show_irrigation_advisor():
    farmer = st.session_state.get("farmer")
    if not farmer:
        st.warning("Please login first.")
        return

    farmer_id = farmer.get("id", 1)
    farmer_name = farmer.get("name", "Farmer")
    lang_code = st.session_state.get("language_code", "en")
    ui = IRRIG_LANG.get(lang_code, IRRIG_LANG["en"])

    st.title(ui["title"])
    st.caption(f"👨‍🌾 {farmer_name} • 🌐 {ui['sub']}")
    st.markdown("---")

    reading = get_latest_farm_reading(farmer_id)
    if not reading:
        st.info("🌱 No farm data is available yet. Please enter your farm readings first.")
        if st.button("📡 Go to My Farm Data", use_container_width=True):
            st.session_state.page = "farm"
            st.rerun()
        return

    crop = get_latest_predicted_crop(farmer_id)
    crop_info = CROP_IRRIGATION_DATA.get(crop, DEFAULT_IRRIGATION)

    moisture = reading.get("soil_moisture")
    if moisture is None:
        moisture = 40.0
    moisture = float(moisture)

    temperature = reading.get("temperature", 28.0)
    humidity = reading.get("humidity", 70.0)
    rainfall = reading.get("rainfall", 100.0)

    # Status Determination
    if moisture < 25.0:
        status_key = "status_urgent"
        banner_bg = "linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%)"
        border_color = "#ef4444"
        voice_verdict_en = "Soil moisture is critically low at {:.0f} percent. Immediate irrigation is required today. Apply approximately 20,000 to 25,000 liters per acre.".format(moisture)
        voice_verdict_te = "మీ పొలంలో నేల తేమ కేవలం {:.0f} శాతం మాత్రమే ఉంది. చాలా తక్కువగా ఉన్నందున ఈరోజే తప్పనిసరిగా నీరు పెట్టండి.".format(moisture)
        voice_verdict_hi = "खेत में नमी केवल {:.0f} प्रतिशत है। मिट्टी बहुत सूखी है, इसलिए आज ही सिंचाई करना अति आवश्यक है।".format(moisture)
        voice_verdict_ta = "நிலத்தில் ஈரப்பதம் {:.0f} சதவீதம் மட்டுமே உள்ளது. உடனே நீர் பாய்ச்சவும்.".format(moisture)
        voice_verdict_kn = "ಜಮೀನಿನಲ್ಲಿ ತೇವಾಂಶ {:.0f} ಪ್ರತಿಶತ ಇದೆ. ಮಣ್ಣು ಒಣಗಿದೆ, ಇಂದೇ ನೀರಾವರಿ ಮಾಡಿ.".format(moisture)
        voice_verdict_mr = "शेतात ओलावा केवळ {:.0f} टक्के आहे. आजच पिकाला पाणी द्यावे.".format(moisture)
    elif moisture < 40.0:
        status_key = "status_soon"
        banner_bg = "linear-gradient(135deg, #78350f 0%, #92400e 100%)"
        border_color = "#f59e0b"
        voice_verdict_en = "Soil moisture is getting low at {:.0f} percent. Plan to irrigate your {} crop within the next 24 to 48 hours.".format(moisture, crop)
        voice_verdict_te = "నేల తేమ {:.0f} శాతానికి తగ్గింది. రాబోయే 1 లేదా 2 రోజుల్లో మీ {} పంటకు నీరు పెట్టండి.".format(moisture, crop)
        voice_verdict_hi = "मिट्टी की नमी {:.0f} प्रतिशत है। अगले 24 से 48 घंटों में अपनी {} फसल में पानी देने की योजना बनाएं।".format(moisture, crop)
        voice_verdict_ta = "ஈரப்பதம் {:.0f} சதவீதமாக உள்ளது. அடுத்த 1-2 நாட்களில் நீர் பாய்ச்சவும்.".format(moisture)
        voice_verdict_kn = "ತೇವಾಂಶ {:.0f} ಪ್ರತಿಶತ ಇದೆ. ಮುಂದಿನ 1-2 ದಿನಗಳಲ್ಲಿ ನೀರು ಹಾಯಿಸಿ.".format(moisture)
        voice_verdict_mr = "जमिनीतील ओलावा {:.0f} टक्के आहे. पुढील 2 दिवसांत पाणी देण्याचे नियोजन करा.".format(moisture)
    elif moisture <= 75.0:
        status_key = "status_ok"
        banner_bg = "linear-gradient(135deg, #14532d 0%, #166534 100%)"
        border_color = "#22c55e"
        voice_verdict_en = "Soil moisture is optimal at {:.0f} percent. Your {} crop has plenty of water. No irrigation is needed today.".format(moisture, crop)
        voice_verdict_te = "నేలలో తేమ {:.0f} శాతంతో చాలా బాగుంది. మీ {} పంటకు తగినంత తేమ ఉంది. ఈరోజు నీరు పెట్టవలసిన అవసరం లేదు.".format(moisture, crop)
        voice_verdict_hi = "मिट्टी में नमी {:.0f} प्रतिशत के साथ बहुत अच्छी है। आपकी {} फसल को आज पानी देने की कोई आवश्यकता नहीं है।".format(moisture, crop)
        voice_verdict_ta = "மண்ணில் போதுமான ஈரப்பதம் {:.0f} சதவீதம் உள்ளது. இன்று நீர் பாய்ச்ச தேவையில்லை.".format(moisture)
        voice_verdict_kn = "ಮಣ್ಣಿನಲ್ಲಿ ತೇವಾಂಶ {:.0f} ಪ್ರತಿಶತ ಉತ್ತಮವಾಗಿದೆ. ಇಂದು ನೀರು ಹಾಯಿಸುವ ಅಗತ್ಯವಿಲ್ಲ.".format(moisture)
        voice_verdict_mr = "जमिनीत ओलावा {:.0f} टक्के उत्तम आहे. आज पाणी देण्याची गरज नाही.".format(moisture)
    else:
        status_key = "status_wet"
        banner_bg = "linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%)"
        border_color = "#3b82f6"
        voice_verdict_en = "Soil moisture is high at {:.0f} percent. The field is saturated. Do not irrigate to avoid root rot and waterlogging.".format(moisture)
        voice_verdict_te = "నేలలో తేమ చాలా ఎక్కువగా {:.0f} శాతం ఉంది. నీరు పెట్టవద్దు, అదనపు నీటిని బయటకు పంపండి.".format(moisture)
        voice_verdict_hi = "खेत में नमी {:.0f} प्रतिशत अधिक है। जलभराव से बचने के लिए पानी न दें।".format(moisture)
        voice_verdict_ta = "ஈரப்பதம் அதிகமாக உள்ளது. நீர் பாய்ச்ச வேண்டாம்.".format(moisture)
        voice_verdict_kn = "ತೇವಾಂಶ ಹೆಚ್ಚಾಗಿದೆ. ನೀರು ಹಾಯಿಸಬೇಡಿ.".format(moisture)
        voice_verdict_mr = "जमिनीत जास्त पाणी आहे. सिंचन करू नका.".format(moisture)

    # Full localized voice text mapping
    voice_scripts = {
        "en": f"Namaste {farmer_name}! For your {crop.title()} crop, {voice_verdict_en} Ambient temperature is {temperature:.0f} degrees Celsius and humidity is {humidity:.0f} percent. Best watering time is early morning between 6 and 9 AM.",
        "te": f"నమస్కారం {farmer_name} గారు! మీ {crop.title()} పంటకు, {voice_verdict_te} వాతావరణ ఉష్ణోగ్రత {temperature:.0f} డిగ్రీలు ఉంది. ఉదయం 6 నుండి 9 గంటల మధ్య లేదా సాయంత్రం వేళలో నీరు పెట్టడం ఉత్తమం.",
        "hi": f"नमस्ते {farmer_name} जी! आपकी {crop.title()} फसल के लिए, {voice_verdict_hi} तापमान {temperature:.0f} डिग्री है। सुबह 6 से 9 बजे के बीच पानी देना सबसे उत्तम होता है।",
        "ta": f"வணக்கம் {farmer_name}! உங்கள் {crop.title()} பயிருக்கு, {voice_verdict_ta} வெப்பநிலை {temperature:.0f} டிகிரி. அதிகாலை அல்லது மாலையில் நீர் பாய்ச்சவும்.",
        "kn": f"ನಮಸ್ಕಾರ {farmer_name}! ನಿಮ್ಮ {crop.title()} ಬೆಳೆಗೆ, {voice_verdict_kn} ತಾಪಮಾನ {temperature:.0f} ಡಿಗ್ರಿ ಇದೆ. ಬೆಳಿಗ್ಗೆ ಅಥವಾ ಸಂಜೆ ನೀರು ಹಾಯಿಸುವುದು ಉತ್ತಮ.",
        "mr": f"नमस्कार {farmer_name}! तुमच्या {crop.title()} पिकासाठी, {voice_verdict_mr} तापमान {temperature:.0f} अंश आहे. सकाळी लवकर पाणी देणे उत्तम ठरेल."
    }

    current_script = voice_scripts.get(lang_code, voice_scripts["en"])
    speech_lang_code = ui["speech_lang"]

    # =====================================================
    # 🔊 AI VOICE SUMMARY COMPONENT
    # =====================================================
    st.markdown(
        f"""
        <div style="background: #ffffff; border: 2px solid #22c55e; border-radius: 16px; padding: 18px 20px; margin-bottom: 18px; box-shadow: 0 4px 14px rgba(34, 197, 94, 0.15);">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                <div>
                    <div style="font-weight: 800; font-size: 16px; color: #15803d; display: flex; align-items: center; gap: 8px;">
                        <span>📢</span> {ui['voice_title']}
                    </div>
                    <div style="font-size: 13px; color: #64748b; margin-top: 2px;">
                        {ui['voice_sub']}
                    </div>
                </div>
                <div style="font-size: 12px; font-weight: 700; color: #0f172a; background: #dcfce7; padding: 4px 10px; border-radius: 999px;">
                    🌾 Crop: {crop.title()}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    script_json = json.dumps(current_script)
    components.html(
        f"""
        <div style="display: flex; gap: 10px; margin-bottom: 12px;">
            <button id="playIrrigVoice" onclick="playVoice()" style="
                flex: 1;
                min-height: 48px;
                background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
                color: #ffffff;
                border: none;
                border-radius: 12px;
                font-family: system-ui, sans-serif;
                font-size: 15px;
                font-weight: 800;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(22, 163, 74, 0.35);
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
            ">
                <span>{ui['btn_play']}</span>
            </button>
            <button id="stopIrrigVoice" onclick="stopVoice()" style="
                min-height: 48px;
                padding: 0 20px;
                background: #334155;
                color: #f8fafc;
                border: 1px solid #475569;
                border-radius: 12px;
                font-family: system-ui, sans-serif;
                font-size: 14px;
                font-weight: 700;
                cursor: pointer;
            ">
                {ui['btn_stop']}
            </button>
        </div>
        <script>
            const textToSpeak = {script_json};
            const speechLang = "{speech_lang_code}";

            function playVoice() {{
                if (!('speechSynthesis' in window)) {{
                    alert('Speech synthesis is not supported on this device.');
                    return;
                }}
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(textToSpeak);
                utterance.lang = speechLang;
                utterance.rate = 0.90;
                utterance.pitch = 1.0;

                const voices = window.speechSynthesis.getVoices();
                const match = voices.find(v => v.lang === speechLang || v.lang.startsWith(speechLang.split('-')[0]));
                if (match) {{
                    utterance.voice = match;
                }}

                const btn = document.getElementById('playIrrigVoice');
                btn.style.background = '#059669';
                utterance.onend = function() {{
                    btn.style.background = 'linear-gradient(135deg, #16a34a 0%, #15803d 100%)';
                }};
                window.speechSynthesis.speak(utterance);
            }}

            function stopVoice() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    const btn = document.getElementById('playIrrigVoice');
                    btn.style.background = 'linear-gradient(135deg, #16a34a 0%, #15803d 100%)';
                }}
            }}
        </script>
        """,
        height=62
    )

    # =====================================================
    # ACTION RECOMMENDATION HERO CARD
    # =====================================================
    st.markdown(
        f"""
        <div style="background: {banner_bg}; border: 2px solid {border_color}; border-radius: 18px; padding: 22px; color: white; margin-bottom: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.12);">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                <div>
                    <span style="background: rgba(255,255,255,0.2); color: #ffffff; padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 700; border: 1px solid rgba(255,255,255,0.3);">
                        ⚡ Live AI Water Verdict
                    </span>
                    <h2 style="color: #ffffff !important; font-size: 24px !important; font-weight: 800; margin: 8px 0 4px 0;">
                        {ui[status_key]}
                    </h2>
                    <p style="color: #f1f5f9; font-size: 14px; margin: 0; font-weight: 600;">
                        Target Crop: <strong>{crop.title()}</strong> • Total Crop Water Need: <strong>{crop_info['water_req']}</strong>
                    </p>
                </div>
                <div style="font-size: 42px;">💧</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # LIVE SENSOR METRICS & GAUGE
    # =====================================================
    st.subheader("📊 Real-Time Field Readings & Moisture Gauge")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric("💦 Soil Moisture", f"{moisture:.1f} %", delta=f"{'Low (-)' if moisture < 35 else ('High (+)' if moisture > 70 else 'Ideal')}")
    with m_col2:
        st.metric("🌡️ Temperature", f"{temperature:.1f} °C")
    with m_col3:
        st.metric("💧 Humidity", f"{humidity:.1f} %")
    with m_col4:
        st.metric("🌧️ Rainfall", f"{rainfall:.1f} mm")

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    st.progress(min(1.0, max(0.05, moisture / 100.0)))
    st.caption(f"Soil Moisture Scale: 0-25% (Critical Dry) • 25-40% (Low) • 40-75% (Optimal Root Zone) • 75-100% (Saturated)")

    st.markdown("---")

    # =====================================================
    # 📅 CRITICAL GROWTH STAGES & WATERING SCHEDULE TABLE
    # =====================================================
    st.subheader(f"{ui['schedule_title']} ({crop.title()})")
    st.markdown(f"**Recommended Method:** `{crop_info['method']}` • **Standard Frequency:** `{crop_info['freq_days']}`")

    stages = crop_info["critical_stages"]
    for idx, stg in enumerate(stages, 1):
        with st.container(border=True):
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <div style="font-weight: 800; font-size: 16px; color: #15803d;">
                            #{idx}. {stg['stage']}
                        </div>
                        <div style="font-size: 13px; color: #475569; margin-top: 4px;">
                            🎯 <strong>Why Critical:</strong> {stg['importance']}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span style="background: #e0f2fe; color: #0369a1; font-weight: 700; font-size: 12px; padding: 4px 10px; border-radius: 999px;">
                            💧 {stg['depth']}
                        </span>
                        <div style="font-size: 12px; color: #64748b; margin-top: 4px; font-weight: 600;">
                            🕒 {stg['freq']}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # =====================================================
    # 💧 WATER VOLUME & PUMP RUN-TIME CALCULATOR
    # =====================================================
    st.subheader(ui["calc_title"])
    c_col1, c_col2 = st.columns(2)

    with c_col1:
        acres = st.selectbox(ui["calc_acres"], [1, 2, 3, 4, 5, 10], index=0)
    with c_col2:
        pump_hp = st.selectbox(ui["calc_pump"], ["3 HP Motor (~15,000 L/hr)", "5 HP Motor (~25,000 L/hr)", "7.5 HP Motor (~38,000 L/hr)", "Drip Line (1.2 L/hr/emitter)"], index=1)

    liters_per_acre_base = 22000
    if "rice" in crop:
        liters_per_acre_base = 32000
    elif "watermelon" in crop or "chickpea" in crop:
        liters_per_acre_base = 15000

    total_liters = liters_per_acre_base * acres
    
    if "3 HP" in pump_hp:
        flow_rate = 15000
    elif "5 HP" in pump_hp:
        flow_rate = 25000
    elif "7.5 HP" in pump_hp:
        flow_rate = 38000
    else:
        flow_rate = 20000

    est_hours = total_liters / flow_rate

    calc_res1, calc_res2 = st.columns(2)
    with calc_res1:
        st.metric(ui["calc_result"], f"{total_liters:,} Liters", delta=f"{acres} Acre(s)")
    with calc_res2:
        st.metric(ui["calc_time"], f"{est_hours:.1f} Hours ({est_hours * 60:.0f} mins)", delta=pump_hp.split("(")[0].strip())

    st.info(f"💡 **Pro-Tip for Farmers:** Water between **6:00 AM - 9:00 AM** or **4:30 PM - 7:00 PM** to prevent 30-40% water loss from midday solar evaporation.")

    st.markdown("---")

    # =====================================================
    # ❓ FREQUENTLY ASKED FARMER QUESTIONS & DOUBTS
    # =====================================================
    st.subheader(ui["faq_title"])

    with st.expander("❓ What is the best time of day to irrigate my crop?", expanded=False):
        st.markdown(
            """
            * **Best Time:** Early morning (**6:00 AM to 9:00 AM**) or late evening (**4:30 PM to 7:00 PM**).
            * **Why:** In midday heat, 30% to 40% of irrigation water evaporates before reaching plant roots, and cold water on hot leaves can cause physiological stress or fungal leaf scorching.
            """
        )

    with st.expander("❓ What happens if I over-water my field?", expanded=False):
        st.markdown(
            """
            * **Root Suffocation:** Waterlogged soil replaces air pockets in the root zone with water, starving roots of oxygen.
            * **Root Rot & Wilt Disease:** Soil-borne pathogens (like *Phytophthora* and *Fusarium*) thrive in soggy soil, turning roots black and rotting them.
            * **Nutrient Leaching:** Excess water washes away Nitrogen and Potassium beyond the reach of plant roots.
            """
        )

    with st.expander("❓ How does Drip Irrigation save 50% water compared to flooding?", expanded=False):
        st.markdown(
            """
            * **Targeted Delivery:** Delivers water directly to the plant root zone drop-by-drop with 95% efficiency.
            * **Weed Control:** Inter-row spaces remain dry, preventing weeds from stealing moisture and fertilizers.
            * **Yield Boost:** Provides uniform moisture without stress cycles, increasing crop yield by **20% to 35%**.
            """
        )

    with st.expander("❓ If rain is expected today, should I stop irrigation?", expanded=False):
        st.markdown(
            """
            * **Yes, always check rainfall readings:** If rainfall > 20 mm is recorded or overcast cloud cover is present, pause irrigation for 24-48 hours.
            * This saves pumping electricity and protects your crops from root rot and nutrient loss.
            """
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    if st.button("🌿 Next Step: View Fertilizer Guidance", use_container_width=True, type="primary"):
        st.session_state.page = "fertilizer"
        st.rerun()