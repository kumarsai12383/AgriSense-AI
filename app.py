import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import streamlit as st

from database.database import initialize_database
from database.farmers import update_farmer_language
from modules.login import show_login
from modules.crop_recommendation import show_crop_recommendation


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AgriSense AI",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =========================================================
# HIGH-CONTRAST PRESENTATION-GRADE DESIGN SYSTEM (CSS)
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Universal Font System */
    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Main App Background & Typography */
    .stApp {
        background-color: #f8fafc !important;
        color: #0f172a;
    }

    .block-container {
        max-width: 960px;
        padding-top: 1.2rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
        padding-bottom: 4rem;
    }

    /* Headings - Bold, High-Contrast & Presentation Clear */
    h1, h2, h3, h4, h5, h6 {
        color: #0f172a !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }
    h1 { font-size: 28px !important; margin-bottom: 8px !important; }
    h2 { font-size: 22px !important; margin-top: 14px !important; margin-bottom: 8px !important; }
    h3 { font-size: 18px !important; margin-top: 10px !important; }

    /* Paragraphs and captions */
    p, li, td, th {
        color: #334155;
        font-size: 15px;
        line-height: 1.6;
    }
    .stCaption, [data-testid="stCaptionContainer"] {
        color: #64748b !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    /* Hide default sidebar and header decor */
    [data-testid="stSidebar"] {
        display: none;
    }
    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Primary Action Buttons - Extra Large Touch Targets for Farmers */
    .stButton > button {
        width: 100%;
        min-height: 52px;
        border-radius: 14px;
        font-size: 16px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #15803d 0%, #16a34a 100%) !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(22, 163, 74, 0.30);
        transition: all 0.2s ease;
        cursor: pointer;
    }

    .stButton > button * {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 16px !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(22, 163, 74, 0.45);
        background: linear-gradient(135deg, #166534 0%, #15803d 100%) !important;
    }

    /* Widget Labels */
    label, [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] span {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #0f172a !important;
    }

    /* Text & Number Inputs */
    .stTextInput input,
    .stNumberInput input,
    textarea {
        border-radius: 12px !important;
        border: 1.5px solid #cbd5e1 !important;
        background-color: #ffffff !important;
        color: #0f172a !important;
        padding: 10px 14px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }

    .stTextInput input:focus,
    .stNumberInput input:focus,
    textarea:focus {
        border-color: #16a34a !important;
        box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.20) !important;
    }

    /* Selectboxes */
    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        border: 1.5px solid #cbd5e1 !important;
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-weight: 600 !important;
        min-height: 46px;
    }

    /* Metric Cards */
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1.5px solid #e2e8f0 !important;
        border-radius: 14px !important;
        padding: 14px 16px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) !important;
    }

    [data-testid="stMetricValue"] * {
        font-weight: 800 !important;
        color: #15803d !important;
        font-size: 24px !important;
    }

    [data-testid="stMetricLabel"] * {
        font-size: 12px !important;
        font-weight: 700 !important;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Streamlit Containers (Cards) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px !important;
        border: 1.5px solid #e2e8f0 !important;
        background-color: #ffffff !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) !important;
        padding: 4px !important;
        margin-bottom: 12px !important;
    }

    /* Custom Reusable Cards */
    .agri-card {
        background-color: #ffffff;
        border-radius: 16px;
        border: 1.5px solid #e2e8f0;
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }

    /* Hero Banner */
    .agri-hero {
        background: linear-gradient(135deg, #14532d 0%, #166534 60%, #15803d 100%);
        border-radius: 18px;
        padding: 22px 24px;
        margin-bottom: 18px;
        box-shadow: 0 8px 20px -4px rgba(20, 83, 45, 0.30);
    }

    .agri-hero h1, .agri-hero h2, .agri-hero h3, .agri-hero p, .agri-hero span, .agri-hero div {
        color: #ffffff !important;
    }

    /* Pill Badges */
    .agri-pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.3px;
    }

    .pill-green {
        background: #dcfce7;
        color: #166534 !important;
        border: 1px solid #86efac;
    }

    .pill-amber {
        background: #fef3c7;
        color: #92400e !important;
        border: 1px solid #fde68a;
    }

    .pill-blue {
        background: #e0f2fe;
        color: #075985 !important;
        border: 1px solid #7dd3fc;
    }

    /* Expander styling */
    [data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1.5px solid #e2e8f0 !important;
        border-radius: 14px !important;
        margin-bottom: 10px !important;
    }

    /* Alert Boxes (Info, Success, Warning, Error) */
    .stAlert {
        border-radius: 12px !important;
        font-weight: 600 !important;
    }

    /* Chat Messages */
    [data-testid="stChatMessage"] {
        background-color: #ffffff !important;
        border: 1.5px solid #e2e8f0 !important;
        border-radius: 14px !important;
        padding: 12px 16px !important;
        margin-bottom: 8px !important;
    }

    /* Mobile adjustments */
    @media (max-width: 640px) {
        .block-container {
            padding-top: 0.5rem;
            padding-left: 0.75rem;
            padding-right: 0.75rem;
        }
        .agri-hero {
            padding: 16px;
        }
        h1 { font-size: 24px !important; }
        h2 { font-size: 20px !important; }
        h3 { font-size: 17px !important; }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DATABASE
# =========================================================

initialize_database()


# =========================================================
# LOGIN
# =========================================================

if "farmer" not in st.session_state or not st.session_state.farmer:
    show_login()
    st.stop()


# =========================================================
# FARMER & LANGUAGE INITIALIZATION
# =========================================================

farmer = st.session_state.get("farmer", {})

LANGUAGES_MAP = {
    "English": "en",
    "తెలుగు": "te",
    "हिंदी": "hi",
    "தமிழ்": "ta",
    "ಕನ್ನಡ": "kn",
    "मराठी": "mr",
}

if "selected_language" not in st.session_state:
    st.session_state.selected_language = farmer.get("language", "English")

if st.session_state.selected_language not in LANGUAGES_MAP:
    st.session_state.selected_language = "English"

st.session_state.language_code = LANGUAGES_MAP[st.session_state.selected_language]
st.session_state.language_selected = True

if "page" not in st.session_state:
    st.session_state.page = "home"


# =========================================================
# MULTILINGUAL NAVIGATION MENUS
# =========================================================

MENUS_BY_LANG = {
    "en": {
        "🏠 Dashboard Home": "home",
        "📡 My Farm Data": "farm",
        "🌾 AI Crop Recommendation": "crop",
        "🧪 Soil Health & NPK": "soil",
        "📊 Prediction Progress": "progress",
        "💧 Smart Irrigation": "water",
        "🌿 Fertilizer Guidance": "fertilizer",
        "🦠 Plant Disease Doctor": "disease",
        "🤖🎙️ AgriSense AI Chat & Voice": "voice",
        "⚡ Gemini Live Call Mode": "voice_live",
        "❓ Farmer Help Center & Guide": "help",
    },
    "te": {
        "🏠 డాష్‌బోర్డ్ హోమ్": "home",
        "📡 నా పొలం డేటా": "farm",
        "🌾 AI పంట సిఫార్సు": "crop",
        "🧪 నేల ఆరోగ్యం & NPK": "soil",
        "📊 మునుపటి రికార్డులు": "progress",
        "💧 స్మార్ట్ నీటిపారుదల": "water",
        "🌿 ఎరువుల సలహాదారు": "fertilizer",
        "🦠 పంట వ్యాధి డాక్టర్": "disease",
        "🤖🎙️ అగ్రిసెన్స్ AI చాట్ & వాయిస్": "voice",
        "⚡ లైవ్ కాల్ మోడ్": "voice_live",
        "❓ సహాయ కేంద్రం & గైడ్": "help",
    },
    "hi": {
        "🏠 डैशबोर्ड होम": "home",
        "📡 मेरे खेत का डेटा": "farm",
        "🌾 AI फसल सिफारिश": "crop",
        "🧪 मिट्टी का स्वास्थ्य & NPK": "soil",
        "📊 पिछले परिणाम": "progress",
        "💧 स्मार्ट सिंचाई सलाह": "water",
        "🌿 खाद एवं उर्वरक सलाह": "fertilizer",
        "🦠 फसल रोग डॉक्टर": "disease",
        "🤖🎙️ एग्रीसेंस AI चैट और वॉइस": "voice",
        "⚡ लाइव वॉइस कॉल": "voice_live",
        "❓ किसान सहायता केंद्र": "help",
    },
    "ta": {
        "🏠 முகப்பு பக்கம்": "home",
        "📡 என் பண்ணை தகவல்": "farm",
        "🌾 AI பயிர் பரிந்துரை": "crop",
        "🧪 மண் ஆரோக்கியம் & NPK": "soil",
        "📊 முந்தைய முடிவுகள்": "progress",
        "💧 ஸ்மார்ட் பாசன முறை": "water",
        "🌿 உர மேலாண்மை": "fertilizer",
        "🦠 பயிர் நோய் மருத்துவர்": "disease",
        "🤖🎙️ அக்ரிசென்ஸ் AI அரட்டை & குரல்": "voice",
        "⚡ நேரலை அழைப்பு முறை": "voice_live",
        "❓ உதவி மையம் & வழிகாட்டி": "help",
    },
    "kn": {
        "🏠 ಮುಖಪುಟ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್": "home",
        "📡 ನನ್ನ ಹೊಲದ ಮಾಹಿತಿ": "farm",
        "🌾 AI ಬೆಳೆ ಶಿಫಾರಸು": "crop",
        "🧪 ಮಣ್ಣಿನ ಆರೋಗ್ಯ & NPK": "soil",
        "📊 ಹಿಂದಿನ ದಾಖಲೆಗಳು": "progress",
        "💧 ಸ್ಮಾರ್ಟ್ ನೀರಾವರಿ": "water",
        "🌿 ರಸಗೊಬ್ಬರ ಸಲಹೆ": "fertilizer",
        "🦠 ಬೆಳೆ ರೋಗ ವೈದ್ಯ": "disease",
        "🤖🎙️ ಅಗ್ರಿಸೆನ್ಸ್ AI ಚಾಟ್ ಮತ್ತು ವಾಯ್ಸ್": "voice",
        "⚡ ಲೈವ್ ಕಾಲ್ ಮೋಡ್": "voice_live",
        "❓ ರೈತ ಸಹಾಯ ಕೇಂದ್ರ": "help",
    },
    "mr": {
        "🏠 मुख्य डॅशबोर्ड": "home",
        "📡 माझ्या शेताचा डेटा": "farm",
        "🌾 AI पीक शिफारस": "crop",
        "🧪 माती आरोग्य & NPK": "soil",
        "📊 मागील निकाल": "progress",
        "💧 स्मार्ट सिंचन सल्ला": "water",
        "🌿 खत व्यवस्थापन": "fertilizer",
        "🦠 पीक रोग डॉक्टर": "disease",
        "🤖🎙️ ॲग्रीसेन्स AI चॅट व व्हॉईस": "voice",
        "⚡ थेट व्हॉईस कॉल": "voice_live",
        "❓ शेतकरी मदत केंद्र": "help",
    }
}

NAV_TITLE = {
    "en": "🧭 Quick Navigation",
    "te": "🧭 నావిగేషన్ మెను",
    "hi": "🧭 मुख्य मेनू",
    "ta": "🧭 வழிசெலுத்தல் பட்டி",
    "kn": "🧭 ನ್ಯಾವಿಗೇಷನ್ ಮೆನು",
    "mr": "🧭 नेव्हिगेशन मेनू"
}

lang_code = st.session_state.language_code
CURRENT_MENU = MENUS_BY_LANG.get(lang_code, MENUS_BY_LANG["en"])
nav_prompt = NAV_TITLE.get(lang_code, "🧭 Quick Navigation")

PAGE_TO_LABEL = {v: k for k, v in CURRENT_MENU.items()}
page_values = list(CURRENT_MENU.values())
page_keys = list(CURRENT_MENU.keys())

current_page = st.session_state.get("page", "home")
if current_page not in page_values:
    current_page = "home"
    st.session_state.page = "home"

target_label = PAGE_TO_LABEL.get(current_page, page_keys[0])
nav_key = f"nav_select_{lang_code}"

# Synchronize selectbox widget state with the active page state
if nav_key in st.session_state and CURRENT_MENU.get(st.session_state[nav_key]) != current_page:
    st.session_state[nav_key] = target_label

def on_nav_change():
    selected = st.session_state.get(nav_key)
    if selected and selected in CURRENT_MENU:
        st.session_state.page = CURRENT_MENU[selected]

current_index = page_keys.index(target_label) if target_label in page_keys else 0

st.selectbox(
    nav_prompt,
    page_keys,
    index=current_index,
    key=nav_key,
    on_change=on_nav_change
)


# =========================================================
# TOP FARMER PROFILE BAR WITH INSTANT LANGUAGE SWITCHER
# =========================================================

current_lang = st.session_state.selected_language

profile_col1, profile_col2, profile_col3 = st.columns([3, 2, 1])

with profile_col1:
    f_name = farmer.get('name', 'Farmer')
    f_phone = farmer.get('phone', '')
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 10px; padding: 4px 0;">
            <div style="width: 38px; height: 38px; border-radius: 50%; background: #dcfce7; display: flex; align-items: center; justify-content: center; font-size: 20px;">
                👨‍🌾
            </div>
            <div>
                <div style="font-weight: 700; color: #0f172a; font-size: 16px; line-height: 1.2;">{f_name}</div>
                <div style="font-size: 12px; color: #64748b;">📞 {f_phone}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with profile_col2:
    lang_keys = list(LANGUAGES_MAP.keys())
    c_idx = lang_keys.index(current_lang) if current_lang in lang_keys else 0
    header_lang = st.selectbox(
        "🌐 Language / భాష",
        lang_keys,
        index=c_idx,
        key="header_language_select"
    )
    if header_lang != current_lang:
        st.session_state.selected_language = header_lang
        st.session_state.language_code = LANGUAGES_MAP[header_lang]
        if isinstance(st.session_state.get("farmer"), dict):
            st.session_state.farmer["language"] = header_lang
        if farmer.get("id"):
            update_farmer_language(farmer["id"], header_lang)
        st.rerun()

with profile_col3:
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    if st.button("🚪 Logout", key="logout_top"):
        st.session_state.clear()
        st.rerun()

st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)




# =========================================================
# HOME
# =========================================================

if st.session_state.page == "home":

    from modules.farmer_home import show_farmer_home

    show_farmer_home()


# =========================================================
# FARM DATA
# =========================================================

elif st.session_state.page == "farm":

    from modules.farm_data import show_farm_data

    show_farm_data()


# =========================================================
# CROP RECOMMENDATION
# =========================================================

elif st.session_state.page == "crop":

    show_crop_recommendation()


# =========================================================
# SOIL HEALTH
# =========================================================

elif st.session_state.page == "soil":

    from modules.soil_health import show_soil_health

    show_soil_health()


# =========================================================
# PROGRESS
# =========================================================

elif st.session_state.page == "progress":

    from modules.prediction_history import show_prediction_history

    show_prediction_history()


# =========================================================
# IRRIGATION
# =========================================================

elif st.session_state.page == "water":

    from modules.irrigation_advisor import show_irrigation_advisor

    show_irrigation_advisor()


# =========================================================
# FERTILIZER
# =========================================================

elif st.session_state.page == "fertilizer":

    from modules.fertilizer_advisor import show_fertilizer_advisor

    show_fertilizer_advisor()


# =========================================================
# DISEASE DETECTION
# =========================================================

elif st.session_state.page == "disease":

    from modules.disease_detection import show_disease_detection

    show_disease_detection()


# =========================================================
# AI ASSISTANT
# =========================================================

elif st.session_state.page == "voice":

    from modules.ai_assistant_page import show_ai_assistant

    show_ai_assistant()


# =========================================================
# LIVE VOICE
# =========================================================

elif st.session_state.page == "voice_live":

    from modules.live_voice_page import show_live_voice

    show_live_voice()


# =========================================================
# HELP CENTER
# =========================================================

elif st.session_state.page == "help":

    from modules.help_center import show_help_center

    show_help_center()