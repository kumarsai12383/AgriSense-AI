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
        padding-bottom: 96px;
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

    /* Primary & Secondary Action Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        transition: all 0.15s ease-in-out;
        cursor: pointer;
    }

    /* Primary Buttons (Green Gradient) */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        min-height: 48px;
        font-size: 15px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #15803d 0%, #16a34a 100%) !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(22, 163, 74, 0.28) !important;
    }

    .stButton > button[kind="primary"] *,
    .stButton > button[data-testid="baseButton-primary"] * {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(22, 163, 74, 0.40) !important;
        background: linear-gradient(135deg, #166534 0%, #15803d 100%) !important;
    }

    /* Secondary Buttons (Crisp White / Subtle Border) */
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="baseButton-secondary"] {
        min-height: 44px;
        font-size: 14px !important;
        font-weight: 700 !important;
        background: #ffffff !important;
        color: #1e293b !important;
        border: 1.5px solid #cbd5e1 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    }

    .stButton > button[kind="secondary"] *,
    .stButton > button[data-testid="baseButton-secondary"] * {
        color: #1e293b !important;
        font-weight: 700 !important;
    }

    .stButton > button[kind="secondary"]:hover,
    .stButton > button[data-testid="baseButton-secondary"]:hover {
        background: #f8fafc !important;
        border-color: #94a3b8 !important;
        transform: translateY(-1px);
    }

    /* Sticky Bottom Navigation Bar (Native Streamlit) */
    div[data-testid="stBottom"] {
        background: #ffffff !important;
        border-top: 1.5px solid #e2e8f0 !important;
        box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.08) !important;
        z-index: 9999 !important;
    }

    div[data-testid="stBottom"] > div {
        padding: 6px 8px max(10px, env(safe-area-inset-bottom)) 8px !important;
        max-width: 900px !important;
        margin: 0 auto !important;
    }

    div[data-testid="stBottom"] [data-testid="column"] {
        padding: 0 2px !important;
    }

    div[data-testid="stBottom"] button,
    div[data-testid="stBottom"] [data-testid="stPopover"] button {
        min-height: 42px !important;
        height: 42px !important;
        padding: 2px 2px !important;
        border-radius: 10px !important;
        margin: 0 !important;
        line-height: 1.2 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    div[data-testid="stBottom"] button *,
    div[data-testid="stBottom"] [data-testid="stPopover"] button * {
        font-size: 12px !important;
        letter-spacing: -0.2px !important;
    }

    /* Active Tab in Bottom Bar */
    div[data-testid="stBottom"] button[kind="primary"],
    div[data-testid="stBottom"] button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #15803d 0%, #16a34a 100%) !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 2px 8px rgba(22, 163, 74, 0.35) !important;
    }

    div[data-testid="stBottom"] button[kind="primary"] *,
    div[data-testid="stBottom"] button[data-testid="baseButton-primary"] * {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    /* Inactive Tab in Bottom Bar */
    div[data-testid="stBottom"] button[kind="secondary"],
    div[data-testid="stBottom"] button[data-testid="baseButton-secondary"],
    div[data-testid="stBottom"] [data-testid="stPopover"] button {
        background: #f1f5f9 !important;
        color: #334155 !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: none !important;
    }

    div[data-testid="stBottom"] button[kind="secondary"] *,
    div[data-testid="stBottom"] button[data-testid="baseButton-secondary"] *,
    div[data-testid="stBottom"] [data-testid="stPopover"] button * {
        color: #334155 !important;
        font-weight: 700 !important;
    }

    /* Popover Body Styling */
    [data-testid="stPopoverBody"] {
        border-radius: 18px !important;
        border: 1.5px solid #e2e8f0 !important;
        box-shadow: 0 -8px 30px rgba(0, 0, 0, 0.12) !important;
        padding: 12px !important;
        max-height: 65vh !important;
    }

    [data-testid="stPopoverBody"] button {
        min-height: 42px !important;
        margin-bottom: 5px !important;
        font-size: 14px !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 8px 12px !important;
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
        "📊 Market Prices & Gov Policies": "market",
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
        "📊 మార్కెట్ ధరలు & పథకాలు": "market",
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
        "📊 बाज़ार भाव & सरकारी योजनाएं": "market",
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
        "📊 சந்தை விலைகள் & அரசு திட்டங்கள்": "market",
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
        "📊 ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು & ಯೋಜನೆಗಳು": "market",
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
        "📊 बाजार भाव & सरकारी योजना": "market",
        "❓ शेतकरी मदत केंद्र": "help",
    }
}

HELP_BTN_LABEL = {
    "en": "❓ Help",
    "te": "❓ సహాయం",
    "hi": "❓ सहायता",
    "ta": "❓ உதவி",
    "kn": "❓ ಸಹಾಯ",
    "mr": "❓ मदत"
}

lang_code = st.session_state.language_code
CURRENT_MENU = MENUS_BY_LANG.get(lang_code, MENUS_BY_LANG["en"])
help_btn_text = HELP_BTN_LABEL.get(lang_code, "❓ Help")

PAGE_TO_LABEL = {v: k for k, v in CURRENT_MENU.items()}
page_values = list(CURRENT_MENU.values())
page_keys = list(CURRENT_MENU.keys())

current_page = st.session_state.get("page", "home")
if current_page not in page_values:
    current_page = "home"
    st.session_state.page = "home"


# =========================================================
# APP-STYLE NAVIGATION (CLEAN, MINIMAL, MOBILE-FIRST)
# =========================================================

current_lang = st.session_state.selected_language
f_name = farmer.get('name', 'Farmer')
f_phone = farmer.get('phone', '')

# ---- Slim Top App Bar ----
st.markdown(
    f"""
    <div style="
        background: linear-gradient(135deg, #14532d 0%, #166534 50%, #15803d 100%);
        border-radius: 16px;
        padding: 12px 18px;
        margin-bottom: 10px;
        box-shadow: 0 4px 16px rgba(20, 83, 45, 0.20);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 36px; height: 36px; border-radius: 50%; background: rgba(255,255,255,0.18); display: flex; align-items: center; justify-content: center; font-size: 20px;">
                    🌱
                </div>
                <div>
                    <div style="font-weight: 800; color: #ffffff; font-size: 16px; line-height: 1.1;">AgriSense AI</div>
                    <div style="font-size: 11px; color: #bbf7d0; font-weight: 600;">
                        👨‍🌾 {f_name} &nbsp;•&nbsp; 🌐 {current_lang}
                    </div>
                </div>
            </div>
            <span style="font-size: 10px; background: rgba(220, 252, 231, 0.25); color: #bbf7d0; padding: 2px 8px; border-radius: 9999px; font-weight: 700; border: 1px solid rgba(255,255,255,0.2);">
                🟢 IoT
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---- Compact Settings Row ----
settings_c1, settings_c2, settings_c3 = st.columns([3, 2, 1])

with settings_c1:
    lang_keys = list(LANGUAGES_MAP.keys())
    c_idx = lang_keys.index(current_lang) if current_lang in lang_keys else 0
    header_lang = st.selectbox(
        "🌐 Language",
        lang_keys,
        index=c_idx,
        key="header_language_select",
        label_visibility="collapsed"
    )
    if header_lang != current_lang:
        st.session_state.selected_language = header_lang
        st.session_state.language_code = LANGUAGES_MAP[header_lang]
        if isinstance(st.session_state.get("farmer"), dict):
            st.session_state.farmer["language"] = header_lang
        if farmer.get("id"):
            update_farmer_language(farmer["id"], header_lang)
        st.rerun()

with settings_c2:
    is_on_help = (current_page == "help")
    if st.button(help_btn_text, key="top_help_center_btn", use_container_width=True, type="primary" if is_on_help else "secondary"):
        st.session_state.page = "help"
        st.rerun()

with settings_c3:
    if st.button("🚪", key="logout_top", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ---- Sticky Bottom Navigation Bar (Native, Blazing-Fast & Mobile-First) ----
BOTTOM_NAV_LABELS = {
    "en": {
        "farm": "Farm Data", "crop": "Predicted Crop", "schemes": "Governments", "voice": "AI",
        "more": "More", "more_title": "All Modules & Features",
        "home": "Home Dashboard", "market": "Market Prices", "soil": "Soil Health & NPK",
        "water": "Smart Irrigation", "fertilizer": "Fertilizer Schedule", "disease": "Crop Disease Doctor",
        "progress": "Prediction History", "voice_live": "Gemini Live Call", "help": "Farmer Help Center"
    },
    "te": {
        "farm": "పొలం డేటా", "crop": "పంట సిఫార్సు", "schemes": "ప్రభుత్వ పథకాలు", "voice": "AI",
        "more": "మరిన్ని", "more_title": "అన్ని విభాగాలు & సాధనాలు",
        "home": "హోమ్ డ్యాష్‌బోర్డ్", "market": "మార్కెట్ ధరలు", "soil": "నేల ఆరోగ్యం & NPK",
        "water": "స్మార్ట్ నీటిపారుదల", "fertilizer": "ఎరువుల సలహా", "disease": "వ్యాధి నివారణ",
        "progress": "మునుపటి రికార్డులు", "voice_live": "లైవ్ కాల్ మోడ్", "help": "సహాయ కేంద్రం"
    },
    "hi": {
        "farm": "खेत डेटा", "crop": "फसल सिफारिश", "schemes": "सरकारी योजनाएं", "voice": "AI",
        "more": "और", "more_title": "सभी मॉड्यूल और उपकरण",
        "home": "होम डैशबोर्ड", "market": "मंडी भाव", "soil": "मिट्टी स्वास्थ्य & NPK",
        "water": "स्मार्ट सिंचाई", "fertilizer": "खाद प्रबंधन", "disease": "रोग पहचान",
        "progress": "इतिहास", "voice_live": "लाइव कॉल", "help": "सहायता केंद्र"
    },
    "ta": {
        "farm": "பண்ணை தகவல்", "crop": "பயிர் பரிந்துரை", "schemes": "அரசு திட்டங்கள்", "voice": "AI",
        "more": "மேலும்", "more_title": "அனைத்து சேவைகள்",
        "home": "முகப்பு", "market": "சந்தை விலைகள்", "soil": "மண் ஆரோக்கியம்",
        "water": "பாசன மேலாண்மை", "fertilizer": "உர வழிகாட்டி", "disease": "நோய் மருத்துவர்",
        "progress": "வரலாறு", "voice_live": "நேரலை அழைப்பு", "help": "உதவி மையம்"
    },
    "kn": {
        "farm": "ಹೊಲ ಮಾಹಿತಿ", "crop": "ಬೆಳೆ ಶಿಫಾರಸು", "schemes": "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು", "voice": "AI",
        "more": "ಇನ್ನಷ್ಟು", "more_title": "ಎಲ್ಲಾ ಆಯ್ಕೆಗಳು",
        "home": "ಮುಖಪುಟ", "market": "ಮಾರುಕಟ್ಟೆ ದರಗಳು", "soil": "ಮಣ್ಣಿನ ಆರೋಗ್ಯ",
        "water": "ನೀರಾವರಿ", "fertilizer": "ಗೊಬ್ಬರ ಸಲಹೆ", "disease": "ರೋಗ ವೈದ್ಯ",
        "progress": "ದಾಖಲೆಗಳು", "voice_live": "ಲೈವ್ ಕಾಲ್", "help": "ಸಹಾಯ ಕೇಂದ್ರ"
    },
    "mr": {
        "farm": "शेत डेटा", "crop": "पीक शिफारस", "schemes": "शासकीय योजना", "voice": "AI",
        "more": "अजून", "more_title": "सर्व साधने",
        "home": "मुख्य पृष्ठ", "market": "बाजार भाव", "soil": "माती परीक्षण & NPK",
        "water": "सिंचन व्यवस्थापन", "fertilizer": "खत व्यवस्थापन", "disease": "रोग निदान",
        "progress": "मागील निकाल", "voice_live": "लाइव्ह कॉल", "help": "मदत केंद्र"
    },
}

bnav = BOTTOM_NAV_LABELS.get(lang_code, BOTTOM_NAV_LABELS["en"])

with st.bottom:
    nav_c1, nav_c2, nav_c3, nav_c4, nav_c5 = st.columns(5)

    # 1. Farm Data
    with nav_c1:
        if st.button(
            f"📡 {bnav['farm']}",
            key="nav_btn_farm",
            use_container_width=True,
            type="primary" if current_page == "farm" else "secondary"
        ):
            st.session_state.page = "farm"
            st.rerun()

    # 2. Predicted Crop
    with nav_c2:
        if st.button(
            f"🌾 {bnav['crop']}",
            key="nav_btn_crop",
            use_container_width=True,
            type="primary" if current_page == "crop" else "secondary"
        ):
            st.session_state.page = "crop"
            st.rerun()

    # 3. Governments
    with nav_c3:
        if st.button(
            f"🏛️ {bnav['schemes']}",
            key="nav_btn_gov",
            use_container_width=True,
            type="primary" if current_page == "gov_schemes" else "secondary"
        ):
            st.session_state.page = "gov_schemes"
            st.rerun()

    # 4. AI
    with nav_c4:
        if st.button(
            f"🤖 {bnav['voice']}",
            key="nav_btn_voice",
            use_container_width=True,
            type="primary" if current_page == "voice" else "secondary"
        ):
            st.session_state.page = "voice"
            st.rerun()

    # 5. More (All other options)
    with nav_c5:
        with st.popover(f"☰ {bnav['more']}", use_container_width=True):
            st.markdown(f"<div style='font-size:14px;font-weight:800;color:#0f172a;margin-bottom:8px;'>☰ {bnav['more_title']}</div>", unsafe_allow_html=True)

            if st.button(f"🏠 {bnav['home']}", key="pop_btn_home", use_container_width=True, type="primary" if current_page == "home" else "secondary"):
                st.session_state.page = "home"
                st.rerun()

            if st.button(f"📊 {bnav['market']}", key="pop_btn_market", use_container_width=True, type="primary" if current_page == "market" else "secondary"):
                st.session_state.page = "market"
                st.rerun()

            if st.button(f"🧪 {bnav['soil']}", key="pop_btn_soil", use_container_width=True, type="primary" if current_page == "soil" else "secondary"):
                st.session_state.page = "soil"
                st.rerun()

            if st.button(f"💧 {bnav['water']}", key="pop_btn_water", use_container_width=True, type="primary" if current_page == "water" else "secondary"):
                st.session_state.page = "water"
                st.rerun()

            if st.button(f"🌿 {bnav['fertilizer']}", key="pop_btn_fert", use_container_width=True, type="primary" if current_page == "fertilizer" else "secondary"):
                st.session_state.page = "fertilizer"
                st.rerun()

            if st.button(f"🦠 {bnav['disease']}", key="pop_btn_disease", use_container_width=True, type="primary" if current_page == "disease" else "secondary"):
                st.session_state.page = "disease"
                st.rerun()

            if st.button(f"📈 {bnav['progress']}", key="pop_btn_progress", use_container_width=True, type="primary" if current_page == "progress" else "secondary"):
                st.session_state.page = "progress"
                st.rerun()

            if st.button(f"⚡ {bnav['voice_live']}", key="pop_btn_voice_live", use_container_width=True, type="primary" if current_page == "voice_live" else "secondary"):
                st.session_state.page = "voice_live"
                st.rerun()

            if st.button(f"❓ {bnav['help']}", key="pop_btn_help", use_container_width=True, type="primary" if current_page == "help" else "secondary"):
                st.session_state.page = "help"
                st.rerun()



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
# GOVERNMENT SCHEMES & SUBSIDIES (STANDALONE PAGE)
# =========================================================

elif st.session_state.page == "gov_schemes":

    from modules.government_schemes import show_government_schemes

    show_government_schemes()


# =========================================================
# LIVE MANDI MARKET PRICES & COST ESTIMATOR
# =========================================================

elif st.session_state.page == "market":

    from modules.market_policy import show_market_policy

    show_market_policy()


# =========================================================
# HELP CENTER
# =========================================================

elif st.session_state.page == "help":

    from modules.help_center import show_help_center

    show_help_center()