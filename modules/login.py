import os
import streamlit as st
from database.farmers import get_or_create_farmer, update_farmer_language


LANGUAGES_LOGIN = {
    "English": {
        "code": "en",
        "title": "AgriSense AI",
        "subtitle": "Smart Agricultural Decision Support & Live AI Assistant",
        "badge1": "🎙️ Multilingual Voice AI",
        "badge2": "🌾 ML Crop Recommendation",
        "badge3": "📡 Live IoT Sensors",
        "login_card_title": "👨‍🌾 Farmer Login / Registration",
        "login_card_sub": "Enter your name and mobile number to access personalized farm advisory",
        "name_label": "👤 Farmer Name",
        "name_placeholder": "e.g. Ramesh Kumar / Praveen",
        "phone_label": "📱 Mobile Number (10 Digits)",
        "phone_placeholder": "e.g. 7095984500",
        "submit_btn": "🚜 Enter Dashboard",
        "name_error": "⚠️ Please enter your name.",
        "phone_error": "⚠️ Please enter a valid 10-digit mobile number.",
        "pillars_title": "🌱 Smart Agriculture & Modern Farming Solutions",
        "pillars_sub": "Empowering farmers with AI, IoT soil intelligence, and precision irrigation",
        "p1_title": "🌾 Smart Crop Science",
        "p1_desc": "Machine Learning predicts the highest-yielding crop tailored to your soil NPK & climate.",
        "p2_title": "💧 Precision Irrigation",
        "p2_desc": "Automated watering schedule & alerts based on real-time soil moisture monitoring.",
        "p3_title": "🧪 IoT Soil Diagnostics",
        "p3_desc": "Instant NPK nutrient testing, pH balance check, and customized fertilizer plans.",
        "p4_title": "🌿 Plant Protection & Health",
        "p4_desc": "AI vision detects leaf diseases instantly with organic & chemical treatment guides."
    },
    "తెలుగు": {
        "code": "te",
        "title": "అగ్రిసెన్స్ AI",
        "subtitle": "రైతుల కోసం స్మార్ట్ వ్యవసాయ సలహాదారు & లైవ్ AI అసిస్టెంట్",
        "badge1": "🎙️ తెలుగు వాయిస్ అసిస్టెంట్",
        "badge2": "🌾 మంచి పంట సిఫార్సు",
        "badge3": "📡 లైవ్ IoT సెన్సార్లు",
        "login_card_title": "👨‍🌾 రైతు లాగిన్ / నమోదు",
        "login_card_sub": "వ్యక్తిగత వ్యవసాయ సలహాలు పొందడానికి మీ వివరాలు నమోదు చేయండి",
        "name_label": "👤 రైతు పేరు",
        "name_placeholder": "ఉదా: రమేష్ కుమార్ / ప్రవీణ్",
        "phone_label": "📱 మొబైల్ నంబర్ (10 అంకెలు)",
        "phone_placeholder": "ఉదా: 7095984500",
        "submit_btn": "🚜 డ్యాష్‌బోర్డ్‌లోకి ప్రవేశించండి",
        "name_error": "⚠️ దయచేసి మీ పేరును నమోదు చేయండి.",
        "phone_error": "⚠️ దయచేసి సరైన 10 అంకెల మొబైల్ నంబర్‌ను నమోదు చేయండి.",
        "pillars_title": "🌱 ఆధునిక వ్యవసాయ పద్ధతులు & సేవల వివరణ",
        "pillars_sub": "AI, IoT నేల సెన్సార్లు మరియు స్మార్ట్ నీటిపారుదలతో రైతులకు అండగా",
        "p1_title": "🌾 శాస్త్రీయ పంట సాగు",
        "p1_desc": "మీ పొలం నేల NPK మరియు వాతావరణానికి అనువైన అధిక దిగుబడినిచ్చే పంటను ఎంపిక చేస్తుంది.",
        "p2_title": "💧 స్మార్ట్ నీటిపారుదల",
        "p2_desc": "నేల తేమ శాతం ఆధారంగా పంటకు ఎప్పుడు ఎంత నీరు పెట్టాలో స్వయంచాలక హెచ్చరికలు.",
        "p3_title": "🧪 నేల పరీక్ష & IoT",
        "p3_desc": "7-ఇన్-1 సెన్సార్లతో తక్షణ నత్రజని, భాస్వరం, పొటాష్ మరియు pH సమతుల్యత పరీక్ష.",
        "p4_title": "🌿 పంట రక్షణ & తెగుళ్ల నివారణ",
        "p4_desc": "ఆకు ఫోటో తీసి అప్‌లోడ్ చేస్తే AI తెగుళ్లను గుర్తించి సులభ నివారణలను సూచిస్తుంది."
    },
    "हिंदी": {
        "code": "hi",
        "title": "एग्रीसेंस AI",
        "subtitle": "किसानों के लिए स्मार्ट कृषि सहायक और लाइव AI सलाहकार",
        "badge1": "🎙️ हिंदी वॉइस सहायक",
        "badge2": "🌾 AI फसल सिफारिश",
        "badge3": "📡 लाइव IoT सेंसर",
        "login_card_title": "👨‍🌾 किसान लॉगिन / पंजीकरण",
        "login_card_sub": "व्यक्तिगत कृषि सलाह प्राप्त करने के लिए अपना नाम और मोबाइल नंबर दर्ज करें",
        "name_label": "👤 किसान का नाम",
        "name_placeholder": "उदा: रमेश कुमार / प्रवीण",
        "phone_label": "📱 मोबाइल नंबर (10 अंक)",
        "phone_placeholder": "उदा: 7095984500",
        "submit_btn": "🚜 डैशबोर्ड में प्रवेश करें",
        "name_error": "⚠️ कृपया अपना नाम दर्ज करें।",
        "phone_error": "⚠️ कृपया 10 अंकों का सही मोबाइल नंबर दर्ज करें।",
        "pillars_title": "🌱 आधुनिक कृषि और स्मार्ट खेती समाधान",
        "pillars_sub": "AI, IoT सेंसर और सटीक सिंचाई तकनीक द्वारा किसानों का सशक्तिकरण",
        "p1_title": "🌾 सटीक फसल योजना",
        "p1_desc": "आपकी मिट्टी के पोषक तत्वों और मौसम के अनुसार सबसे अधिक उपज देने वाली फसल का चयन।",
        "p2_title": "💧 कुशल सिंचाई प्रबंधन",
        "p2_desc": "मिट्टी की नमी के आधार पर सिंचाई का सही समय और पानी की बचत की सलाह।",
        "p3_title": "🧪 मृदा स्वास्थ्य परीक्षण",
        "p3_desc": "NPK और pH स्तर की लाइव जाँच व सटीक खाद की मात्रा की सिफारिश।",
        "p4_title": "🌿 फसल सुरक्षा और रोग निदान",
        "p4_desc": "पत्तियों की फोटो से रोगों की तत्काल पहचान और जैविक/रासायनिक उपचार।"
    },
    "தமிழ்": {
        "code": "ta",
        "title": "அக்ரிசென்ஸ் AI",
        "subtitle": "விவசாயிகளுக்கான ஸ்மார்ட் முடிவெடுக்கும் தளம் & குரல் உதவியாளர்",
        "badge1": "🎙️ தமிழ் குரல் உதவியாளர்",
        "badge2": "🌾 AI பயிர் பரிந்துரை",
        "badge3": "📡 நேரலை IoT சென்சார்கள்",
        "login_card_title": "👨‍🌾 விவசாயி உள்நுழைவு / பதிவு",
        "login_card_sub": "உங்கள் பண்ணை ஆலோசனையைப் பெற பெயர் மற்றும் மொபைல் எண்ணை உள்ளிடவும்",
        "name_label": "👤 விவசாயி பெயர்",
        "name_placeholder": "எ.கா: ரமேஷ் குமார்",
        "phone_label": "📱 அலைபேசி எண் (10 இலக்கங்கள்)",
        "phone_placeholder": "எ.கா: 7095984500",
        "submit_btn": "🚜 டேஷ்போர்டைத் திறக்கவும்",
        "name_error": "⚠️ உங்கள் பெயரை உள்ளிடவும்.",
        "phone_error": "⚠️ சரியான 10 இலக்க அலைபேசி எண்ணை உள்ளிடவும்.",
        "pillars_title": "🌱 நவீன விவசாய மற்றும் பண்ணை தீர்வுகள்",
        "pillars_sub": "AI மற்றும் IoT தொழில்நுட்பம் மூலம் துல்லியமான விவசாய வழிகாட்டல்",
        "p1_title": "🌾 துல்லிய பயிர் தேர்வு",
        "p1_desc": "மண் சத்துக்கள் மற்றும் தட்பவெப்பத்திற்கு ஏற்ற அதிக விளைச்சல் தரும் பயிர் கணிப்பு.",
        "p2_title": "💧 பாசன மேலாண்மை",
        "p2_desc": "மண் ஈரப்பதத்தைக் கண்காணித்து சரியான நேரத்தில் நீர் பாய்ச்சும் எச்சரிக்கை.",
        "p3_title": "🧪 மண் பரிசோதனை & NPK",
        "p3_desc": "மண்ணின் தரம், pH மற்றும் ஊட்டச்சத்துக்களுக்கு ஏற்ப சரியான உர அளவு பரிந்துரை.",
        "p4_title": "🌿 பயிர் பாதுகாப்பு & நோய் கட்டுப்பாடு",
        "p4_desc": "இலை புகைப்படங்கள் மூலம் நோய்களைக் கண்டறிந்து உரிய மருந்துகளைப் பரிந்துரைத்தல்."
    },
    "ಕನ್ನಡ": {
        "code": "kn",
        "title": "ಅಗ್ರಿಸೆನ್ಸ್ AI",
        "subtitle": "ರೈತರಿಗಾಗಿ ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ಸಹಾಯಕ ಮತ್ತು ಲೈವ್ AI ಮಾರ್ಗದರ್ಶಿ",
        "badge1": "🎙️ ಕನ್ನಡ ವಾಯ್ಸ್ ಸಹಾಯಕ",
        "badge2": "🌾 AI ಬೆಳೆ ಶಿಫಾರಸು",
        "badge3": "📡 ಲೈವ್ IoT ಸೆನ್ಸಾರ್‌ಗಳು",
        "login_card_title": "👨‍🌾 ರೈತರ ಲಾಗಿನ್ / ನೋಂದಣಿ",
        "login_card_sub": "ವೈಯಕ್ತಿಕ ಕೃಷಿ ಸಲಹೆಗಳನ್ನು ಪಡೆಯಲು ನಿಮ್ಮ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ",
        "name_label": "👤 ರೈತರ ಹೆಸರು",
        "name_placeholder": "ಉದಾ: ರಮೇಶ್ ಕುಮಾರ್",
        "phone_label": "📱 ಮೊಬೈಲ್ ಸಂಖ್ಯೆ (10 ಅಂಕಿಗಳು)",
        "phone_placeholder": "ಉದಾ: 7095984500",
        "submit_btn": "🚜 ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ಪ್ರವೇಶಿಸಿ",
        "name_error": "⚠️ ದಯವಿಟ್ಟು ನಿಮ್ಮ ಹೆಸರನ್ನು ನಮೂದಿಸಿ.",
        "phone_error": "⚠️ ದಯವಿಟ್ಟು ಮಾನ್ಯವಾದ 10 ಅಂಕಿಯ ಮೊಬೈಲ್ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ.",
        "pillars_title": "🌱 ಆಧುನಿಕ ಕೃಷಿ ಮತ್ತು ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ಪರಿಹಾರಗಳು",
        "pillars_sub": "AI ಮತ್ತು IoT ತಂತ್ರಜ್ಞಾನದೊಂದಿಗೆ ರೈತರಿಗೆ ನಿಖರ ಮಾರ್ಗದರ್ಶನ",
        "p1_title": "🌾 ನಿಖರ ಬೆಳೆ ಯೋಜನೆ",
        "p1_desc": "ನಿಮ್ಮ ಮಣ್ಣಿನ NPK ಮತ್ತು ಹವಾಮಾನಕ್ಕೆ ಸೂಕ್ತವಾದ ಗರಿಷ್ಠ ಇಳುವರಿ ನೀಡುವ ಬೆಳೆ ಶಿಫಾರಸು.",
        "p2_title": "💧 ಹನಿ ಮತ್ತು ಸ್ಮಾರ್ಟ್ ನೀರಾವರಿ",
        "p2_desc": "ಮಣ್ಣಿನ ತೇವಾಂಶದ ಆಧಾರದ ಮೇಲೆ ನೀರಾವರಿ ಸಮಯ ಮತ್ತು ಎಚ್ಚರಿಕೆಗಳು.",
        "p3_title": "🧪 ಮಣ್ಣಿನ ಆರೋಗ್ಯ ತಪಾಸಣೆ",
        "p3_desc": "NPK ಮತ್ತು pH ಮಟ್ಟಗಳ ನೇರ ಪರೀಕ್ಷೆ ಹಾಗೂ ಸೂಕ್ತ ರಸಗೊಬ್ಬರ ಪ್ರಮಾಣ.",
        "p4_title": "🌿 ಬೆಳೆ ಸಂರಕ್ಷಣೆ ಮತ್ತು ರೋಗ ನಿಯಂತ್ರಣ",
        "p4_desc": "ಎಲೆಗಳ ಫೋಟೋ ಮೂಲಕ ಬೆಳೆ ರೋಗಗಳನ್ನು ಗುರುತಿಸಿ ಸೂಕ್ತ ಪರಿಹಾರ ತಿಳಿಯಿರಿ."
    },
    "मराठी": {
        "code": "mr",
        "title": "एग्रीसेन्स AI",
        "subtitle": "शेतकऱ्यांसाठी स्मार्ट कृषी सल्लागार आणि थेट AI सहाय्यक",
        "badge1": "🎙️ मराठी व्हॉईस सहाय्यक",
        "badge2": "🌾 AI पीक शिफारस",
        "badge3": "📡 थेट IoT सेन्सर्स",
        "login_card_title": "👨‍🌾 शेतकरी लॉगिन / नोंदणी",
        "login_card_sub": "वैयक्तिक शेती सल्ल्यासाठी आपले नाव आणि मोबाईल नंबर प्रविष्ट करा",
        "name_label": "👤 शेतकऱ्याचे नाव",
        "name_placeholder": "उदा: रमेश कुमार",
        "phone_label": "📱 मोबाईल नंबर (10 अंक)",
        "phone_placeholder": "उदा: 7095984500",
        "submit_btn": "🚜 डॅशबोर्ड उघडा",
        "name_error": "⚠️ कृपया आपले नाव प्रविष्ट करा.",
        "phone_error": "⚠️ कृपया 10 अंकी वैध मोबाईल नंबर प्रविष्ट करा.",
        "pillars_title": "🌱 आधुनिक शेती आणि स्मार्ट कृषी उपाय",
        "pillars_sub": "AI आणि IoT तंत्रज्ञानाद्वारे शेतकऱ्यांना योग्य मार्गदर्शन",
        "p1_title": "🌾 योग्य पीक नियोजन",
        "p1_desc": "मातीतील पोषक घटक आणि हवामानानुसार सर्वाधिक उत्पादन देणारे पीक निवडणे.",
        "p2_title": "💧 अचूक सिंचन व्यवस्थापन",
        "p2_desc": "जमिनीतील ओलाव्यानुसार पाणी देण्याची योग्य वेळ आणि प्रमाण.",
        "p3_title": "🧪 माती परीक्षण आणि NPK",
        "p3_desc": "मातीची गुणवत्ता, pH व NPK प्रमाणानुसार खतांचे अचूक नियोजन.",
        "p4_title": "🌿 पीक संरक्षण आणि रोग नियंत्रण",
        "p4_desc": "पानांच्या फोटोद्वारे रोगांचे त्वरित निदान आणि योग्य उपाययोजना."
    }
}


def show_login():
    # -------------------------------------------------------------
    # 1. LANGUAGE SELECTOR HEADER (BEFORE LOGIN)
    # -------------------------------------------------------------
    curr_lang = st.session_state.get("selected_language", "English")
    if curr_lang not in LANGUAGES_LOGIN:
        curr_lang = "English"

    lang_keys = list(LANGUAGES_LOGIN.keys())
    curr_index = lang_keys.index(curr_lang) if curr_lang in lang_keys else 0

    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <span style="font-weight: 800; font-size: 14px; color: #15803d;">🌐 Language / భాష / भाषा / மொழி / ಭಾಷೆ / भाषा:</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    chosen_lang = st.selectbox(
        "Select Language",
        lang_keys,
        index=curr_index,
        key="login_language_selector",
        label_visibility="collapsed"
    )

    if chosen_lang != curr_lang:
        st.session_state.selected_language = chosen_lang
        st.session_state.language_code = LANGUAGES_LOGIN[chosen_lang]["code"]
        st.session_state.language_selected = True
        st.rerun()

    ui = LANGUAGES_LOGIN[chosen_lang]

    # -------------------------------------------------------------
    # 2. AGRICULTURAL HERO BANNER WITH RICH BACKGROUND
    # -------------------------------------------------------------
    st.markdown(
        f"""
        <style>
        .login-hero-container {{
            background: linear-gradient(135deg, rgba(20, 83, 45, 0.90) 0%, rgba(22, 101, 52, 0.88) 50%, rgba(21, 128, 61, 0.90) 100%), 
                        url('https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=1200&q=80') center/cover no-repeat;
            border-radius: 20px;
            padding: 34px 22px 26px 22px;
            text-align: center;
            color: #ffffff;
            margin-bottom: 18px;
            box-shadow: 0 10px 30px -5px rgba(20, 83, 45, 0.4);
            border: 2px solid rgba(255, 255, 255, 0.2);
        }}
        </style>

        <div class="login-hero-container">
            <span style="font-size: 50px; display: block; margin-bottom: 4px; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));">🌱</span>
            <h1 style="color: #ffffff !important; font-size: 32px !important; font-weight: 800; margin: 0 0 6px 0; letter-spacing: -0.5px;">
                {ui['title']}
            </h1>
            <p style="color: #dcfce7 !important; font-size: 15px; font-weight: 600; margin: 0 0 12px 0;">
                {ui['subtitle']}
            </p>
            <div style="display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;">
                <span style="background: rgba(255,255,255,0.2); color: #ffffff; padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 700; border: 1px solid rgba(255,255,255,0.3);">
                    {ui['badge1']}
                </span>
                <span style="background: rgba(255,255,255,0.2); color: #ffffff; padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 700; border: 1px solid rgba(255,255,255,0.3);">
                    {ui['badge2']}
                </span>
                <span style="background: rgba(255,255,255,0.2); color: #ffffff; padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 700; border: 1px solid rgba(255,255,255,0.3);">
                    {ui['badge3']}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -------------------------------------------------------------
    # 3. FARMER LOGIN / REGISTRATION CARD
    # -------------------------------------------------------------
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <div style="width: 44px; height: 44px; border-radius: 12px; background: #15803d; color: white; display: flex; align-items: center; justify-content: center; font-size: 24px;">
                    👨‍🌾
                </div>
                <div>
                    <div style="font-weight: 800; font-size: 18px; color: #0f172a;">{ui['login_card_title']}</div>
                    <div style="font-size: 13px; color: #64748b; font-weight: 600;">{ui['login_card_sub']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        name = st.text_input(
            ui['name_label'],
            placeholder=ui['name_placeholder']
        )

        phone = st.text_input(
            ui['phone_label'],
            placeholder=ui['phone_placeholder']
        )

        st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

        if st.button(ui['submit_btn'], key="btn_login_submit", use_container_width=True):
            name = name.strip()
            phone = phone.strip()

            if not name:
                st.warning(ui['name_error'])
                return

            if not phone.isdigit() or len(phone) != 10:
                st.warning(ui['phone_error'])
                return

            farmer = get_or_create_farmer(name, phone)
            update_farmer_language(farmer["id"], chosen_lang)
            farmer["language"] = chosen_lang

            st.session_state.farmer = farmer
            st.session_state.selected_language = chosen_lang
            st.session_state.language_code = ui["code"]
            st.session_state.language_selected = True
            st.rerun()

    # -------------------------------------------------------------
    # 4. MODERN FARMING & AGRICULTURE SHOWCASE
    # -------------------------------------------------------------
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 16px;">
            <h3 style="color: #0f172a; margin-bottom: 4px; font-size: 20px; font-weight: 800;">
                {ui['pillars_title']}
            </h3>
            <p style="color: #64748b; font-size: 14px; margin: 0; font-weight: 600;">
                {ui['pillars_sub']}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    pillars = [
        ("smart_farm.jpg", ui['p1_title'], ui['p1_desc']),
        ("irrigation_farming.jpg", ui['p2_title'], ui['p2_desc']),
        ("soil_testing.jpg", ui['p3_title'], ui['p3_desc']),
        ("organic_farming.jpg", ui['p4_title'], ui['p4_desc']),
    ]

    p_col1, p_col2 = st.columns(2)
    for idx, (img_file, p_title, p_desc) in enumerate(pillars):
        col_target = p_col1 if idx % 2 == 0 else p_col2
        with col_target:
            with st.container(border=True):
                img_path = os.path.join("images", img_file)
                if os.path.exists(img_path):
                    try:
                        st.image(img_path, use_container_width=True)
                    except Exception:
                        pass
                st.markdown(f"<div style='font-weight: 800; font-size: 16px; color: #15803d; margin-top: 6px;'>{p_title}</div>", unsafe_allow_html=True)
                st.caption(p_desc)