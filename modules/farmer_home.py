import streamlit as st


# =========================================================
# SUPPORTED LANGUAGES
# =========================================================

LANGUAGES = {
    "English": "en",
    "తెలుగు": "te",
    "हिंदी": "hi",
    "தமிழ்": "ta",
    "ಕನ್ನಡ": "kn",
    "मराठी": "mr",
}


# =========================================================
# TRANSLATIONS
# =========================================================

TEXT = {

    # -----------------------------------------------------
    # ENGLISH
    # -----------------------------------------------------

    "en": {

        "title": "🌱 AgriSense AI",
        "subtitle": "Smart Farming Assistant",

        "choose": "🌐 Choose your language",
        "continue": "🚜 Continue",

        "welcome": "👨‍🌾 Welcome Farmer!",
        "choose_action": "What would you like to do?",

        "crop": "🌾 Find Best Crop",

        "water": "💧 Water Advice",

        "soil": "🧪 Soil Health",

        "fertilizer": "🌿 Fertilizer Advice",

        "disease": "🦠 Disease Detection",

        "voice": "🎤 Ask AgriSense",

        "farm": "📊 My Farm",

        "talk": "🤖 Ask AgriSense AI",

        "voice_info":
            "Ask your farming question by voice or text.",

        "speak":
            "🎤 Open AI Assistant",

    },


    # -----------------------------------------------------
    # TELUGU
    # -----------------------------------------------------

    "te": {

        "title": "🌱 AgriSense AI",

        "subtitle":
            "స్మార్ట్ వ్యవసాయ సహాయకుడు",

        "choose":
            "🌐 మీ భాషను ఎంచుకోండి",

        "continue":
            "🚜 కొనసాగించండి",

        "welcome":
            "👨‍🌾 రైతులకు స్వాగతం!",

        "choose_action":
            "మీరు ఏమి చేయాలనుకుంటున్నారు?",

        "crop":
            "🌾 మంచి పంటను తెలుసుకోండి",

        "water":
            "💧 నీటి సలహా",

        "soil":
            "🧪 నేల ఆరోగ్యం",

        "fertilizer":
            "🌿 ఎరువుల సలహా",

        "disease":
            "🦠 పంట వ్యాధులను గుర్తించండి",

        "voice":
            "🎤 AgriSense ని అడగండి",

        "farm":
            "📊 నా పొలం",

        "talk":
            "🤖 AgriSense AI ని అడగండి",

        "voice_info":
            "మీ వ్యవసాయ ప్రశ్నను వాయిస్ లేదా టెక్స్ట్ ద్వారా అడగండి.",

        "speak":
            "🎤 AI సహాయకుడిని తెరవండి",

    },


    # -----------------------------------------------------
    # HINDI
    # -----------------------------------------------------

    "hi": {

        "title": "🌱 AgriSense AI",

        "subtitle":
            "स्मार्ट कृषि सहायक",

        "choose":
            "🌐 अपनी भाषा चुनें",

        "continue":
            "🚜 आगे बढ़ें",

        "welcome":
            "👨‍🌾 किसान का स्वागत है!",

        "choose_action":
            "आप क्या करना चाहते हैं?",

        "crop":
            "🌾 सबसे अच्छी फसल खोजें",

        "water":
            "💧 पानी की सलाह",

        "soil":
            "🧪 मिट्टी की जाँच",

        "fertilizer":
            "🌿 खाद की सलाह",

        "disease":
            "🦠 फसल रोग पहचानें",

        "voice":
            "🎤 AgriSense से पूछें",

        "farm":
            "📊 मेरा खेत",

        "talk":
            "🤖 AgriSense AI से पूछें",

        "voice_info":
            "अपना कृषि प्रश्न आवाज़ या टेक्स्ट से पूछें।",

        "speak":
            "🎤 AI सहायक खोलें",

    },


    # -----------------------------------------------------
    # TAMIL
    # -----------------------------------------------------

    "ta": {

        "title": "🌱 AgriSense AI",

        "subtitle":
            "ஸ்மார்ட் விவசாய உதவியாளர்",

        "choose":
            "🌐 உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்",

        "continue":
            "🚜 தொடரவும்",

        "welcome":
            "👨‍🌾 விவசாயிக்கு வரவேற்பு!",

        "choose_action":
            "நீங்கள் என்ன செய்ய விரும்புகிறீர்கள்?",

        "crop":
            "🌾 சிறந்த பயிரைக் கண்டறியவும்",

        "water":
            "💧 நீர் ஆலோசனை",

        "soil":
            "🧪 மண் ஆரோக்கியம்",

        "fertilizer":
            "🌿 உர ஆலோசனை",

        "disease":
            "🦠 பயிர் நோயைக் கண்டறியவும்",

        "voice":
            "🎤 AgriSense-ஐ கேளுங்கள்",

        "farm":
            "📊 என் பண்ணை",

        "talk":
            "🤖 AgriSense AI-ஐ கேளுங்கள்",

        "voice_info":
            "உங்கள் விவசாயக் கேள்வியை குரல் அல்லது உரை மூலம் கேளுங்கள்.",

        "speak":
            "🎤 AI உதவியாளரைத் திறக்கவும்",

    },


    # -----------------------------------------------------
    # KANNADA
    # -----------------------------------------------------

    "kn": {

        "title": "🌱 AgriSense AI",

        "subtitle":
            "ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ಸಹಾಯಕ",

        "choose":
            "🌐 ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",

        "continue":
            "🚜 ಮುಂದುವರಿಸಿ",

        "welcome":
            "👨‍🌾 ರೈತರಿಗೆ ಸ್ವಾಗತ!",

        "choose_action":
            "ನೀವು ಏನು ಮಾಡಲು ಬಯಸುತ್ತೀರಿ?",

        "crop":
            "🌾 ಉತ್ತಮ ಬೆಳೆ ಹುಡುಕಿ",

        "water":
            "💧 ನೀರಿನ ಸಲಹೆ",

        "soil":
            "🧪 ಮಣ್ಣಿನ ಆರೋಗ್ಯ",

        "fertilizer":
            "🌿 ರಸಗೊಬ್ಬರ ಸಲಹೆ",

        "disease":
            "🦠 ಬೆಳೆ ರೋಗ ಪತ್ತೆ",

        "voice":
            "🎤 AgriSense ಅನ್ನು ಕೇಳಿ",

        "farm":
            "📊 ನನ್ನ ಹೊಲ",

        "talk":
            "🤖 AgriSense AI ಅನ್ನು ಕೇಳಿ",

        "voice_info":
            "ನಿಮ್ಮ ಕೃಷಿ ಪ್ರಶ್ನೆಯನ್ನು ಧ್ವನಿ ಅಥವಾ ಪಠ್ಯದ ಮೂಲಕ ಕೇಳಿ.",

        "speak":
            "🎤 AI ಸಹಾಯಕವನ್ನು ತೆರೆಯಿರಿ",

    },


    # -----------------------------------------------------
    # MARATHI
    # -----------------------------------------------------

    "mr": {

        "title": "🌱 AgriSense AI",

        "subtitle":
            "स्मार्ट शेती सहाय्यक",

        "choose":
            "🌐 आपली भाषा निवडा",

        "continue":
            "🚜 पुढे जा",

        "welcome":
            "👨‍🌾 शेतकऱ्यांचे स्वागत!",

        "choose_action":
            "आपण काय करू इच्छिता?",

        "crop":
            "🌾 सर्वोत्तम पीक शोधा",

        "water":
            "💧 पाण्याचा सल्ला",

        "soil":
            "🧪 मातीचे आरोग्य",

        "fertilizer":
            "🌿 खताचा सल्ला",

        "disease":
            "🦠 पीक रोग ओळखा",

        "voice":
            "🎤 AgriSense ला विचारा",

        "farm":
            "📊 माझे शेत",

        "talk":
            "🤖 AgriSense AI ला विचारा",

        "voice_info":
            "तुमचा शेतीचा प्रश्न आवाज किंवा मजकूराद्वारे विचारा.",

        "speak":
            "🎤 AI सहाय्यक उघडा",

    }

}


# =========================================================
# NAVIGATION
# =========================================================

def go_to(page):

    st.session_state.page = page

    st.rerun()


# ==========================================
# Language Selection
# ==========================================

def show_language_selection():

    # ------------------------------------------
    # Header
    # ------------------------------------------

    st.title("🌱 AgriSense AI")

    st.subheader("Smart Farming Assistant")

    st.markdown("---")


    # ------------------------------------------
    # Language Selection
    # ------------------------------------------

    language = st.selectbox(
        "🌐 Choose your language",
        list(LANGUAGES.keys())
    )


    # ------------------------------------------
    # Continue Button
    # ------------------------------------------

    if st.button(
        "🚜 Continue",
        use_container_width=True
    ):

        # Save selected language
        st.session_state.selected_language = language

        # Save language code
        st.session_state.language_code = LANGUAGES[language]

        # Mark language as selected
        st.session_state.language_selected = True

        # Open Home page
        st.session_state.page = "home"

        # Refresh application
        st.rerun()
# =========================================================
# FARMER HOME DASHBOARD
# =========================================================

def show_farmer_home():

    language_code = st.session_state.get(
        "language_code",
        "en"
    )

    text = TEXT.get(
        language_code,
        TEXT["en"]
    )

    farmer = st.session_state.get(
        "farmer"
    )

    farmer_name = farmer['name'] if farmer else "Farmer"

    # =====================================================
    # HERO BANNER
    # =====================================================

    st.markdown(
        f"""
        <div class="agri-hero">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                <div>
                    <span class="agri-pill pill-green" style="background: rgba(255,255,255,0.2); color: #ffffff; border: 1px solid rgba(255,255,255,0.3); margin-bottom: 8px;">
                        🌾 AgriSense AI v2.0
                    </span>
                    <h1 style="color: #ffffff; font-size: 30px; font-weight: 800; margin: 6px 0 4px 0;">
                        {text["welcome"]}
                    </h1>
                    <p style="color: #dcfce7; font-size: 15px; margin: 0;">
                        {text["choose_action"]}
                    </p>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 38px;">🚜</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # 2-COLUMN FEATURE GRID (Clean & Responsive Cards)
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown(f"### {text['crop']}")
            st.caption(text.get("crop_caption", "AI-powered crop prediction based on your soil & climate."))
            if st.button(text["crop"], key="btn_crop", use_container_width=True):
                go_to("crop")

        with st.container(border=True):
            st.markdown(f"### {text['soil']}")
            st.caption(text.get("soil_caption", "Detailed N-P-K nutrient score, pH check, and fertility report."))
            if st.button(text["soil"], key="btn_soil", use_container_width=True):
                go_to("soil")

        with st.container(border=True):
            st.markdown(f"### {text['disease']}")
            st.caption(text.get("disease_caption", "Upload or capture leaf photos for instant diagnosis & cure."))
            if st.button(text["disease"], key="btn_disease", use_container_width=True):
                go_to("disease")

    with col2:
        with st.container(border=True):
            st.markdown(f"### {text['fertilizer']}")
            st.caption(text.get("fertilizer_caption", "Custom NPK dosage calculations & application schedule."))
            if st.button(text["fertilizer"], key="btn_fertilizer", use_container_width=True):
                go_to("fertilizer")

        with st.container(border=True):
            st.markdown(f"### {text['water']}")
            st.caption(text.get("water_caption", "Moisture monitoring, watering alerts, and schedule."))
            if st.button(text["water"], key="btn_water", use_container_width=True):
                go_to("water")

        with st.container(border=True):
            st.markdown(f"### {text['farm']}")
            st.caption(text.get("farm_caption", "Enter or sync IoT sensor readings & farm logs."))
            if st.button(text["farm"], key="btn_farm", use_container_width=True):
                go_to("farm")

    # =====================================================
    # AI ASSISTANT HERO CARD
    # =====================================================

    with st.container(border=True):
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <div style="width: 44px; height: 44px; border-radius: 12px; background: #15803d; display: flex; align-items: center; justify-content: center; font-size: 24px;">
                    🤖
                </div>
                <div>
                    <div style="font-weight: 800; font-size: 17px; color: #0f172a;">{text['talk']}</div>
                    <div style="font-size: 13px; color: #64748b;">{text['voice_info']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        ai_c1, ai_c2 = st.columns(2)
        with ai_c1:
            if st.button(f"🤖🎙️ {text['speak']}", key="btn_ai_chat", use_container_width=True):
                go_to("voice")
        with ai_c2:
            if st.button("⚡ Live Phone Call Mode", key="btn_ai_live", use_container_width=True):
                go_to("voice_live")

    # =====================================================
    # LANGUAGE SWITCHER FOOTER
    # =====================================================

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    if st.button("🌐 Switch Language / భాష మార్చండి", key="btn_lang", use_container_width=True):
        st.session_state.language_selected = False
        st.rerun()