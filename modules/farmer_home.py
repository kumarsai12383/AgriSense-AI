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
    # 🔊 TODAY'S 20-SECOND FARM VOICE SUMMARY WIDGET
    # =====================================================
    from database.database import connect
    import streamlit.components.v1 as components
    import json

    db_moisture = 45.0
    db_temp = 28.0
    db_ph = 6.8
    try:
        conn = connect()
        c = conn.cursor()
        c.execute("SELECT soil_moisture, temperature, ph, rainfall FROM farm_readings WHERE farmer_id = ? ORDER BY id DESC LIMIT 1", (farmer['id'] if farmer else 1,))
        row = c.fetchone()
        if row:
            db_moisture = row[0] if row[0] is not None else 45.0
            db_temp = row[1] if row[1] is not None else 28.0
            db_ph = row[2] if row[2] is not None else 6.8
        conn.close()
    except Exception:
        pass

    # Localized audio summary scripts
    audio_summaries = {
        "te": {
            "title": "🔊 ఈరోజు పొలం సలహా వినండి (20 సెకన్లు)",
            "subtitle": "చదవడం అవసరం లేదు — నేల తేమ & నీటి స్థితి వినడానికి నొక్కండి",
            "btn": "🔊 సలహా వినండి (Play Summary)",
            "stop_btn": "⏹ ఆపండి",
            "speech_lang": "te-IN",
            "script": f"నమస్కారం {farmer_name} గారు! మీ పొలంలో తాజా నేల తేమ {db_moisture:.0f} శాతం ఉంది. ఉష్ణోగ్రత {db_temp:.0f} డిగ్రీలు, నేల పి హెచ్ {db_ph:.1f} ఉంది. {'నేలలో తేమ తక్కువగా ఉంది, నీరు పెట్టడం మంచిది.' if db_moisture < 30 else 'నేలలో తగినంత తేమ ఉంది, పంట ఆరోగ్యంగా ఉంది.'} ఉత్తమ దిగుబడికి అగ్రిసెన్స్ AI తో మాట్లాడండి!"
        },
        "hi": {
            "title": "🔊 आज की खेत की सलाह सुनें (20 सेकंड)",
            "subtitle": "पढ़ने की जरूरत नहीं — नमी और पानी की स्थिति सुनने के लिए दबाएं",
            "btn": "🔊 सलाह सुनें (Play Summary)",
            "stop_btn": "⏹ रोकें",
            "speech_lang": "hi-IN",
            "script": f"नमस्ते {farmer_name} जी! आपके खेत की नमी {db_moisture:.0f} प्रतिशत है। तापमान {db_temp:.0f} डिग्री और मिट्टी का पीएच {db_ph:.1f} है। {'मिट्टी में नमी कम है, सिंचाई करना जरूरी है।' if db_moisture < 30 else 'मिट्टी में पर्याप्त नमी है, फसल स्वस्थ है।'} अधिक जानकारी के लिए एग्रीसेंस AI से पूछें!"
        },
        "ta": {
            "title": "🔊 இன்றைய பண்ணை ஆலோசனையைக் கேளுங்கள்",
            "subtitle": "படிக்கத் தேவையில்லை — குரல் வழியே கேட்க அழுத்தவும்",
            "btn": "🔊 ஆலோசனையைக் கேளுங்கள்",
            "stop_btn": "⏹ நிறுத்து",
            "speech_lang": "ta-IN",
            "script": f"வணக்கம் {farmer_name}! உங்கள் நிலத்தின் ஈரப்பதம் {db_moisture:.0f} சதவீதம் உள்ளது. வெப்பநிலை {db_temp:.0f} டிகிரி. {'மண்ணில் ஈரப்பதம் குறைவு, உடனே நீர் பாய்ச்சவும்.' if db_moisture < 30 else 'மண்ணில் போதுமான ஈரப்பதம் உள்ளது.'} அக்ரிசென்ஸ் AI-ஐப் பயன்படுத்துங்கள்!"
        },
        "kn": {
            "title": "🔊 ಇಂದಿನ ಹೊಲದ ಧ್ವನಿ ಸಾರಾಂಶ ಆಲಿಸಿ",
            "subtitle": "ಓದುವ ಅಗತ್ಯವಿಲ್ಲ — ಧ್ವನಿ ಮೂಲಕ ತಿಳಿಯಲು ಒತ್ತಿ",
            "btn": "🔊 ಸಾರಾಂಶ ಆಲಿಸಿ",
            "stop_btn": "⏹ ನಿಲ್ಲಿಸಿ",
            "speech_lang": "kn-IN",
            "script": f"ನಮಸ್ಕಾರ {farmer_name}! ನಿಮ್ಮ ಜಮೀನಿನ ತೇವಾಂಶ {db_moisture:.0f} ಪ್ರತಿಶತ ಇದೆ. {'ತೇವಾಂಶ ಕಡಿಮೆಯಿದೆ, ನೀರಾವರಿ ಮಾಡಿ.' if db_moisture < 30 else 'ತೇವಾಂಶ ಉತ್ತಮವಾಗಿದೆ, ಬೆಳೆ ಆರೋಗ್ಯವಾಗಿದೆ.'} ಅಗ್ರಿಸೆನ್ಸ್ AI ಬಳಸಿ!"
        },
        "mr": {
            "title": "🔊 आजचा शेती सल्ला ऐका (20 सेकंद)",
            "subtitle": "वाचण्याची गरज नाही — ऑडिओ सल्ला ऐकण्यासाठी दाबा",
            "btn": "🔊 सल्ला ऐका",
            "stop_btn": "⏹ थांबवा",
            "speech_lang": "mr-IN",
            "script": f"नमस्कार {farmer_name}! तुमच्या शेतातील ओलावा {db_moisture:.0f} टक्के आहे. {'जमिनीत ओलावा कमी आहे, पाणी द्या.' if db_moisture < 30 else 'जमिनीत पुरेसा ओलावा आहे, पीक चांगले आहे.'} अधिक सल्ल्यासाठी एग्रीसेन्स AI वापरा!"
        },
        "en": {
            "title": "🔊 Listen to Today's Farm Summary (20s)",
            "subtitle": "No reading needed — Tap to hear real-time soil moisture and watering advice",
            "btn": "🔊 Listen to Summary",
            "stop_btn": "⏹ Stop Audio",
            "speech_lang": "en-IN",
            "script": f"Namaste {farmer_name}! Your latest soil moisture is {db_moisture:.0f} percent, temperature is {db_temp:.0f} degrees Celsius, and soil pH is {db_ph:.1f}. {'Soil moisture is low, irrigation is recommended.' if db_moisture < 30 else 'Soil moisture is optimal, your farm is healthy.'} Tap Ask AgriSense for more details!"
        }
    }

    current_summary = audio_summaries.get(language_code, audio_summaries["en"])

    # High-contrast, easy-to-tap Audio Summary Banner
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 2px solid #22c55e; border-radius: 18px; padding: 18px 20px; margin-bottom: 20px; box-shadow: 0 4px 14px rgba(34, 197, 94, 0.2);">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                <div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 22px;">📢</span>
                        <span style="color: #4ade80; font-size: 17px; font-weight: 800;">{current_summary['title']}</span>
                    </div>
                    <div style="color: #cbd5e1; font-size: 13px; font-weight: 600; margin-top: 4px;">
                        {current_summary['subtitle']}
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Audio player component with speech synthesis
    summary_text_json = json.dumps(current_summary['script'])
    summary_lang_code = current_summary['speech_lang']
    btn_play_text = current_summary['btn']
    btn_stop_text = current_summary['stop_btn']

    components.html(
        f"""
        <div style="display: flex; gap: 10px; margin-bottom: 12px;">
            <button id="playSummaryBtn" onclick="playFarmSummary()" style="
                flex: 1;
                min-height: 48px;
                background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
                color: #ffffff;
                border: none;
                border-radius: 12px;
                font-family: system-ui, sans-serif;
                font-size: 16px;
                font-weight: 800;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(22, 163, 74, 0.35);
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
            ">
                <span>{btn_play_text}</span>
            </button>
            <button id="stopSummaryBtn" onclick="stopFarmSummary()" style="
                min-height: 48px;
                padding: 0 20px;
                background: #334155;
                color: #f8fafc;
                border: 1px solid #475569;
                border-radius: 12px;
                font-family: system-ui, sans-serif;
                font-size: 15px;
                font-weight: 700;
                cursor: pointer;
            ">
                {btn_stop_text}
            </button>
        </div>
        <script>
            const summaryText = {summary_text_json};
            const speechLang = "{summary_lang_code}";

            function playFarmSummary() {{
                if (!('speechSynthesis' in window)) {{
                    alert('Voice is not supported in this browser.');
                    return;
                }}
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(summaryText);
                utterance.lang = speechLang;
                utterance.rate = 0.95;
                utterance.pitch = 1.0;
                
                const btn = document.getElementById('playSummaryBtn');
                btn.style.background = '#059669';
                utterance.onend = function() {{
                    btn.style.background = 'linear-gradient(135deg, #16a34a 0%, #15803d 100%)';
                }};
                window.speechSynthesis.speak(utterance);
            }}

            function stopFarmSummary() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    const btn = document.getElementById('playSummaryBtn');
                    btn.style.background = 'linear-gradient(135deg, #16a34a 0%, #15803d 100%)';
                }}
            }}
        </script>
        """,
        height=62
    )

    # =====================================================
    # 2-COLUMN FEATURE GRID (Clean & High-Contrast Touch Cards)
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
    # ❓ FARMER HELP CENTER & USER GUIDE HERO CARD
    # =====================================================
    with st.container(border=True):
        h_col1, h_col2 = st.columns([3, 1])
        with h_col1:
            st.markdown(
                """
                <div style="font-weight: 800; font-size: 16px; color: #15803d; display: flex; align-items: center; gap: 8px;">
                    <span>❓</span> Farmer Help Center & Step-by-Step Guide
                </div>
                <div style="font-size: 13px; color: #64748b; margin-top: 2px;">
                    New to AgriSense AI? Learn how to use all features step-by-step with voice guidance.
                </div>
                """,
                unsafe_allow_html=True
            )
        with h_col2:
            st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
            if st.button("📖 Open Guide", key="btn_home_to_help", use_container_width=True, type="primary"):
                go_to("help")

    # =====================================================
    # LANGUAGE SWITCHER FOOTER
    # =====================================================

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    with st.expander("🌐 Switch App Language / భాష మార్చండి", expanded=False):
        c_lang = st.session_state.get("selected_language", "English")
        lang_keys = list(LANGUAGES.keys())
        c_i = lang_keys.index(c_lang) if c_lang in lang_keys else 0
        new_l = st.selectbox("🌐 Select Your Language", lang_keys, index=c_i, key="footer_lang_select")
        if new_l != c_lang:
            st.session_state.selected_language = new_l
            st.session_state.language_code = LANGUAGES[new_l]
            if farmer:
                st.session_state.farmer["language"] = new_l
                try:
                    from database.farmers import update_farmer_language
                    update_farmer_language(farmer["id"], new_l)
                except Exception:
                    pass
            st.rerun()