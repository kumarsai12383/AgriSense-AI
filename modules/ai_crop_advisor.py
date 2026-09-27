import os
import json
import streamlit as st
import streamlit.components.v1 as components


LOCALIZED_TITLES = {
    "te": {
        "guide_title": "📖 పంట పూర్తి సాగు వివరాలు (Farming Guide)",
        "desc": "📖 పంట వివరాలు",
        "soil": "🌱 అనువైన నేల రకం",
        "temp": "🌡️ ఉష్ణోగ్రత & వాతావరణం",
        "water": "💧 నీటి అవసరం & పారుదల",
        "fert": "🌿 ఎరువుల షెడ్యూల్",
        "season": "📅 విత్తే కాలం & పంట సమయం",
        "yield": "📈 ఆశించిన దిగుబడి (హెక్టారుకు)",
        "tips": "👨‍🌾 అధిక దిగుబడికి రైతు చిట్కాలు",
        "listen_btn": "🔊 ఈ పంట వివరాలు వినండి (Listen Audio Guide)",
        "stop_btn": "⏹ ఆపండి",
        "speech_lang": "te-IN"
    },
    "hi": {
        "guide_title": "📖 फसल की पूरी कृषि गाइड (Farming Guide)",
        "desc": "📖 फसल विवरण",
        "soil": "🌱 उपयुक्त मिट्टी",
        "temp": "🌡️ तापमान और जलवायु",
        "water": "💧 पानी की आवश्यकता",
        "fert": "🌿 खाद की सिफारिश",
        "season": "📅 बुवाई और कटाई का समय",
        "yield": "📈 अपेक्षित उपज (प्रति हेक्टेयर)",
        "tips": "👨‍🌾 किसानों के लिए महत्वपूर्ण सुझाव",
        "listen_btn": "🔊 इस फसल की जानकारी सुनें (Listen Audio Guide)",
        "stop_btn": "⏹ रोकें",
        "speech_lang": "hi-IN"
    },
    "ta": {
        "guide_title": "📖 பயிர் சாகுபடி வழிகாட்டி (Farming Guide)",
        "desc": "📖 பயிர் விளக்கம்",
        "soil": "🌱 ஏற்ற மண் வகை",
        "temp": "🌡️ வெப்பநிலை & தட்பவெப்பம்",
        "water": "💧 நீர் தேவை & பாசனம்",
        "fert": "🌿 உர அட்டவணை",
        "season": "📅 பருவம் & அறுவடை காலம்",
        "yield": "📈 எதிர்பார்க்கப்படும் மகசூல்",
        "tips": "👨‍🌾 விவசாயிகளுக்கான குறிப்புகள்",
        "listen_btn": "🔊 பயிர் விவரங்களை கேளுங்கள்",
        "stop_btn": "⏹ நிறுத்து",
        "speech_lang": "ta-IN"
    },
    "kn": {
        "guide_title": "📖 ಬೆಳೆ ಕೃಷಿ ಮಾರ್ಗದರ್ಶಿ (Farming Guide)",
        "desc": "📖 ಬೆಳೆ ವಿವರಣೆ",
        "soil": "🌱 ಸೂಕ್ತ ಮಣ್ಣು",
        "temp": "🌡️ ತಾಪಮಾನ ಮತ್ತು ಹವಾಮಾನ",
        "water": "💧 ನೀರಿನ ಅಗತ್ಯತೆ",
        "fert": "🌿 ರಸಗೊಬ್ಬರ ಶಿಫಾರಸು",
        "season": "📅 ಬಿತ್ತನೆ ಮತ್ತು ಕೊಯ್ಲು ಕಾಲ",
        "yield": "📈 ನಿರೀಕ್ಷಿತ ಇಳುವರಿ",
        "tips": "👨‍🌾 ರೈತರಿಗೆ ಪ್ರಮುಖ ಸಲಹೆಗಳು",
        "listen_btn": "🔊 ಬೆಳೆಯ ಮಾಹಿತಿಯನ್ನು ಆಲಿಸಿ",
        "stop_btn": "⏹ ನಿಲ್ಲಿಸಿ",
        "speech_lang": "kn-IN"
    },
    "mr": {
        "guide_title": "📖 पीक लागवड माहिती (Farming Guide)",
        "desc": "📖 पीक वर्णन",
        "soil": "🌱 योग्य माती",
        "temp": "🌡️ तापमान आणि हवामान",
        "water": "💧 पाण्याची आवश्यकता",
        "fert": "🌿 खत व्यवस्थापन",
        "season": "📅 पेरणी व काढणी काळ",
        "yield": "📈 अपेक्षित उत्पादन",
        "tips": "👨‍🌾 शेतकऱ्यांसाठी महत्त्वाच्या टिप्स",
        "listen_btn": "🔊 पीक माहिती ऐका",
        "stop_btn": "⏹ थांबवा",
        "speech_lang": "mr-IN"
    },
    "en": {
        "guide_title": "📖 Comprehensive Agronomic Crop Guide",
        "desc": "📖 Crop Description",
        "soil": "🌱 Suitable Soil & Drainage",
        "temp": "🌡️ Optimal Temperature",
        "water": "💧 Water & Irrigation Requirement",
        "fert": "🌿 Recommended Fertilizer Schedule",
        "season": "📅 Growing & Harvesting Season",
        "yield": "📈 Expected Yield per Hectare",
        "tips": "👨‍🌾 Pro Tips for Maximum Yield",
        "listen_btn": "🔊 Listen to Crop Guide (Audio)",
        "stop_btn": "⏹ Stop Audio",
        "speech_lang": "en-IN"
    }
}


def show_ai_crop_advisor(crop, details):
    """
    Displays the visual AI Crop Advisor section with photos, structured cards, and voice synthesis.
    """
    lang_code = st.session_state.get("language_code", "en")
    labels = LOCALIZED_TITLES.get(lang_code, LOCALIZED_TITLES["en"])

    st.markdown(f"<h3 style='color: #0f172a; margin-top: 18px; margin-bottom: 8px;'>{labels['guide_title']}</h3>", unsafe_allow_html=True)

    if not details:
        st.warning("Crop details are currently unavailable.")
        return

    # -------------------------------------------------------------
    # 🔊 VOICE SYNTHESIS FOR THIS CROP
    # -------------------------------------------------------------
    speech_text = f"Recommended crop is {crop}. {details.get('description', '')} Suitable soil is {details.get('soil', '')}. Water requirement: {details.get('water', '')}. Fertilizer recommendation: {details.get('fertilizer', '')}. Sowing season: {details.get('season', '')}. Farmer tip: {details.get('tips', '')}"
    speech_json = json.dumps(speech_text)
    speech_lang = labels["speech_lang"]
    listen_btn_text = labels["listen_btn"]
    stop_btn_text = labels["stop_btn"]

    components.html(
        f"""
        <div style="display: flex; gap: 10px; margin-bottom: 14px;">
            <button id="playCropAudioBtn" onclick="playCropAudio()" style="
                flex: 1;
                min-height: 48px;
                background: linear-gradient(135deg, #15803d 0%, #16a34a 100%);
                color: #ffffff;
                border: none;
                border-radius: 12px;
                font-family: system-ui, sans-serif;
                font-size: 15px;
                font-weight: 800;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(22, 163, 74, 0.3);
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
            ">
                <span>{listen_btn_text}</span>
            </button>
            <button id="stopCropAudioBtn" onclick="stopCropAudio()" style="
                min-height: 48px;
                padding: 0 18px;
                background: #334155;
                color: #f8fafc;
                border: 1px solid #475569;
                border-radius: 12px;
                font-family: system-ui, sans-serif;
                font-size: 14px;
                font-weight: 700;
                cursor: pointer;
            ">
                {stop_btn_text}
            </button>
        </div>
        <script>
            const cropSpeechText = {speech_json};
            const cropSpeechLang = "{speech_lang}";

            function playCropAudio() {{
                if (!('speechSynthesis' in window)) return;
                window.speechSynthesis.cancel();
                const utter = new SpeechSynthesisUtterance(cropSpeechText);
                utter.lang = cropSpeechLang;
                utter.rate = 0.95;
                
                const btn = document.getElementById('playCropAudioBtn');
                btn.style.background = '#047857';
                utter.onend = function() {{
                    btn.style.background = 'linear-gradient(135deg, #15803d 0%, #16a34a 100%)';
                }};
                window.speechSynthesis.speak(utter);
            }}

            function stopCropAudio() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    const btn = document.getElementById('playCropAudioBtn');
                    btn.style.background = 'linear-gradient(135deg, #15803d 0%, #16a34a 100%)';
                }}
            }}
        </script>
        """,
        height=62
    )

    # -------------------------------------------------------------
    # STRUCTURED AGRONOMIC CARDS (2 COLUMNS)
    # -------------------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown(f"**{labels['desc']}**")
            st.write(details.get("description", "N/A"))

        with st.container(border=True):
            st.markdown(f"**{labels['soil']}**")
            st.write(details.get("soil", "N/A"))

        with st.container(border=True):
            st.markdown(f"**{labels['temp']}**")
            st.write(details.get("temperature", "N/A"))

        with st.container(border=True):
            st.markdown(f"**{labels['water']}**")
            st.write(details.get("water", "N/A"))

    with col2:
        with st.container(border=True):
            st.markdown(f"**{labels['fert']}**")
            st.write(details.get("fertilizer", "N/A"))

        with st.container(border=True):
            st.markdown(f"**{labels['season']}**")
            st.write(details.get("season", "N/A"))

        with st.container(border=True):
            st.markdown(f"**{labels['yield']}**")
            st.write(f"🌾 **{details.get('yield', 'N/A')}**")

        with st.container(border=True):
            st.markdown(f"**{labels['tips']}**")
            st.write(f"💡 {details.get('tips', 'N/A')}")