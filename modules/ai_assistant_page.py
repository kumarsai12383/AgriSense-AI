import os
import json
import re
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import streamlit as st
import streamlit.components.v1 as components

from modules.ai_engine import ask_agrisense_stream
from database.farmers import update_farmer_language


# =========================================================
# LANGUAGE CONFIGURATIONS & LOCALIZED PROMPTS
# =========================================================

LANGUAGES_META = {
    "English": {
        "code": "en",
        "speech_lang": "en-IN",
        "title": "🤖🎙️ AgriSense AI Chat & Voice Assistant",
        "subtitle": "Your AI Agronomist — Speak or Type (AI Speaks Every Answer Aloud)",
        "tap_to_speak": "🎙️ Tap Microphone to Speak",
        "listening": "🔴 Listening in English... Speak your question now!",
        "stop_voice": "⏹ Stop Voice",
        "auto_speak_label": "🔊 Auto-Speak AI Responses (Aloud for Farmers)",
        "speed_label": "⚡ Voice Speed",
        "clear_chat": "🗑️ Clear Chat History",
        "switch_live": "⚡ Gemini Live Call Mode",
        "quick_title": "💡 Quick Questions:",
        "chips": [
            ("🌾 Best crop for my soil?", "What is the best crop recommendation for my soil and climate conditions?"),
            ("💧 Irrigation advice?", "Based on my current soil moisture and temperature, how should I irrigate my farm?"),
            ("🌿 Fertilizer schedule?", "What is the recommended fertilizer application schedule for my farm's NPK values?"),
            ("🦠 Plant disease cure?", "How can I prevent and treat common leaf diseases and pest attacks in my crops?")
        ],
        "greeting": "Namaste 👨‍🌾 **{name}**! I am your AgriSense AI farming assistant. Speak or type your question in English — I will answer and speak out loud for you!",
        "input_placeholder": "💬 Type or speak your question in English..."
    },
    "తెలుగు": {
        "code": "te",
        "speech_lang": "te-IN",
        "title": "🤖🎙️ అగ్రిసెన్స్ AI చాట్ & వాయిస్ అసిస్టెంట్",
        "subtitle": "మీ వ్యవసాయ సలహాదారు — మాట్లాడండి లేదా టైప్ చేయండి (సమాధానం స్వయంగా చదివి వినిపిస్తుంది)",
        "tap_to_speak": "🎙️ మాట్లాడటానికి మైక్ నొక్కండి",
        "listening": "🔴 తెలుగులో వింటున్నాను... మీ ప్రశ్న మాట్లాడండి!",
        "stop_voice": "⏹ వాయిస్ ఆపండి",
        "auto_speak_label": "🔊 AI సమాధానాలు స్వయంగా వినిపించండి (చదవడం రాని రైతులకు ఎంతో మేలు)",
        "speed_label": "⚡ వాయిస్ వేగం",
        "clear_chat": "🗑️ చాట్ క్లియర్ చేయండి",
        "switch_live": "⚡ లైవ్ వాయిస్ కాల్ మోడ్",
        "quick_title": "💡 త్వరిత ప్రశ్నలు:",
        "chips": [
            ("🌾 నా నేలకు ఏ పంట మంచిది?", "నా నేల పోషకాలు మరియు వాతావరణానికి ఏ పంట వేస్తే ఎక్కువ దిగుబడి వస్తుంది?"),
            ("💧 ఎంత నీరు పెట్టాలి?", "నా పొలం తేమ మరియు ఉష్ణోగ్రత ప్రకారం నీటిపారుదల ఎప్పుడు మరియు ఎంత ఇవ్వాలి?"),
            ("🌿 ఎరువుల సమయం & మోతాదు?", "నా పొలంలోని N-P-K విలువల ప్రకారం ఏ ఎరువులు ఎప్పుడు ఎంత మోతాదులో వేయాలి?"),
            ("🦠 పంట తెగుళ్ల నివారణ ఎలా?", "పంటలకు వచ్చే ఆకు తెగుళ్లు, పురుగులు మరియు వ్యాధులను సహజంగా ఎలా నివారించాలి?")
        ],
        "greeting": "నమస్తే 👨‍🌾 **{name}** గారు! నేను మీ అగ్రిసెన్స్ AI వ్యవసాయ సహాయకుడిని. మీ పంట, నేల, నీరు లేదా ఎరువుల గురించి ఏదైనా అడగండి — నేను వివరంగా చెప్పి మీకు వినిపిస్తాను!",
        "input_placeholder": "💬 తెలుగులో మీ వ్యవసాయ ప్రశ్నను అడగండి..."
    },
    "हिंदी": {
        "code": "hi",
        "speech_lang": "hi-IN",
        "title": "🤖🎙️ एग्रीसेंस AI चैट और वॉइस सहायक",
        "subtitle": "आपका कृषि विशेषज्ञ — बोलें या लिखें (AI हर जवाब बोलकर भी सुनाएगा)",
        "tap_to_speak": "🎙️ बोलने के लिए माइक दबाएं",
        "listening": "🔴 हिंदी में सुन रहा हूँ... अपना सवाल बोलें!",
        "stop_voice": "⏹ आवाज़ बंद करें",
        "auto_speak_label": "🔊 AI जवाब बोलकर सुनाएं (अनपढ़ किसानों के लिए सुविधाजनक)",
        "speed_label": "⚡ आवाज़ की गति",
        "clear_chat": "🗑️ चैट साफ करें",
        "switch_live": "⚡ लाइव वॉइस कॉल मोड",
        "quick_title": "💡 त्वरित सवाल:",
        "chips": [
            ("🌾 मेरी मिट्टी के लिए सही फसल?", "मेरी मिट्टी की गुणवत्ता और मौसम के अनुसार सबसे अच्छी उपज देने वाली फसल कौन सी है?"),
            ("💧 सिंचाई कितनी और कब करें?", "मेरी खेत की नमी और तापमान के अनुसार सिंचाई का सही समय क्या है?"),
            ("🌿 खाद की सही मात्रा और समय?", "मेरे खेत के NPK मान के आधार पर खाद का सही समय और मात्रा बताएं?"),
            ("🦠 फसल रोग और कीटनाशक?", "फसलों में लगने वाले कीटों और पत्तों के रोगों की रोकथाम कैसे करें?")
        ],
        "greeting": "नमस्ते 👨‍🌾 **{name}** जी! मैं आपका एग्रीसेंस AI कृषि सहायक हूँ। अपनी फसल, मिट्टी, पानी या खाद के बारे में कोई भी सवाल पूछें — मैं जवाब लिखूंगा और बोलकर भी सुनाऊंगा!",
        "input_placeholder": "💬 हिंदी में अपना खेती से जुड़ा सवाल पूछें..."
    },
    "தமிழ்": {
        "code": "ta",
        "speech_lang": "ta-IN",
        "title": "🤖🎙️ அக்ரிசென்ஸ் AI அரட்டை & குரல் உதவியாளர்",
        "subtitle": "உங்கள் விவசாய ஆலோசகர் — பேசுங்கள் அல்லது தட்டச்சு செய்யுங்கள்",
        "tap_to_speak": "🎙️ பேச மைக்கை அழுத்தவும்",
        "listening": "🔴 தமிழில் கேட்கிறது... உங்கள் கேள்வியைப் பேசுங்கள்!",
        "stop_voice": "⏹ குரலை நிறுத்து",
        "auto_speak_label": "🔊 குரல் வழியே உரக்கப் படிக்கவும்",
        "speed_label": "⚡ குரல் வேகம்",
        "clear_chat": "🗑️ அரட்டையை அழிக்கவும்",
        "switch_live": "⚡ நேரலை அழைப்பு முறை",
        "quick_title": "💡 விரைவு கேள்விகள்:",
        "chips": [
            ("🌾 என் நிலத்திற்கு ஏற்ற பயிர்?", "என் மண் மற்றும் தட்பவெப்ப நிலைக்கு எந்த பயிர் பயிரிட்டால் அதிக விளைச்சல் கிடைக்கும்?"),
            ("💧 பாசன அளவு?", "என் மண்ணின் ஈரப்பதத்திற்கு ஏற்ப எவ்வளவு மற்றும் எப்போது பாசனம் செய்ய வேண்டும்?"),
            ("🌿 உர அட்டவணை?", "என் மண்ணின் NPK அளவுக்கு ஏற்ப உரமிடும் அட்டவணை என்ன?"),
            ("🦠 பூச்சி & நோய் கட்டுப்பாடு?", "பயிர் நோய்கள் மற்றும் பூச்சிகளை எவ்வாறு கட்டுப்படுத்துவது?")
        ],
        "greeting": "வணக்கம் 👨‍🌾 **{name}**! நான் உங்கள் அக்ரிசென்ஸ் AI உதவியாளர். உங்கள் விவசாயக் கேள்விகளைத் தமிழில் கேட்கலாம்!",
        "input_placeholder": "💬 தமிழில் உங்கள் விவசாயக் கேள்வியைக் கேளுங்கள்..."
    },
    "ಕನ್ನಡ": {
        "code": "kn",
        "speech_lang": "kn-IN",
        "title": "🤖🎙️ ಅಗ್ರಿಸೆನ್ಸ್ AI ಚಾಟ್ ಮತ್ತು ವಾಯ್ಸ್ ಸಹಾಯಕ",
        "subtitle": "ನಿಮ್ಮ ಕೃಷಿ ಸಲಹೆಗಾರ — ಮಾತನಾಡಿ ಅಥವಾ ಟೈಪ್ ಮಾಡಿ (ಉತ್ತರವನ್ನು ಧ್ವನಿಯಲ್ಲಿ ಕೇಳಿ)",
        "tap_to_speak": "🎙️ ಮಾತನಾಡಲು ಮೈಕ್ ಒತ್ತಿ",
        "listening": "🔴 ಕನ್ನಡದಲ್ಲಿ ಆಲಿಸಲಾಗುತ್ತಿದೆ... ನಿಮ್ಮ ಪ್ರಶ್ನೆ ಮಾತನಾಡಿ!",
        "stop_voice": "⏹ ಧ್ವನಿ ನಿಲ್ಲಿಸಿ",
        "auto_speak_label": "🔊 ಧ್ವನಿಯಲ್ಲಿ ಗಟ್ಟಿಯಾಗಿ ಓದಿ",
        "speed_label": "⚡ ಧ್ವನಿ ವೇಗ",
        "clear_chat": "🗑️ ಚಾಟ್ ಇತಿಹಾಸ ಅಳಿಸಿ",
        "switch_live": "⚡ ಲೈವ್ ಕಾಲ್ ಮೋಡ್",
        "quick_title": "💡 ತ್ವರಿತ ಪ್ರಶ್ನೆಗಳು:",
        "chips": [
            ("🌾 ನನ್ನ ಮಣ್ಣಿಗೆ ಸೂಕ್ತ ಬೆಳೆ?", "ನನ್ನ ಮಣ್ಣಿನ ಪೋಷಕಾಂಶಗಳು ಮತ್ತು ಹವಾಮಾನಕ್ಕೆ ಯಾವ ಬೆಳೆ ಉತ್ತಮ?"),
            ("💧 ನೀರಾವರಿ ಸಲಹೆ?", "ನನ್ನ ಮಣ್ಣಿನ ತೇವಾಂಶಕ್ಕೆ ಅನುಗುಣವಾಗಿ ನೀರಾವರಿ ಹೇಗೆ ಮಾಡಬೇಕು?"),
            ("🌿 ರಸಗೊಬ್ಬರ ಮಾಹಿತಿ?", "ನನ್ನ ಮಣ್ಣಿನ NPK ಮಟ್ಟಕ್ಕೆ ಅನುಗುಣವಾಗಿ ರಸಗೊಬ್ಬರ ಪ್ರಮಾಣ ತಿಳಿಸಿ?"),
            ("🦠 ಕೀಟ ನಿಯಂತ್ರಣ?", "ಬೆಳೆ ರೋಗಗಳು ಮತ್ತು ಕೀಟಗಳನ್ನು ನೈಸರ್ಗಿಕವಾಗಿ ತಡೆಗಟ್ಟುವುದು ಹೇಗೆ?")
        ],
        "greeting": "ನಮಸ್ಕಾರ 👨‍🌾 **{name}**! ನಾನು ನಿಮ್ಮ ಅಗ್ರಿಸೆನ್ಸ್ AI ಕೃಷಿ ಸಹಾಯಕ. ನಿಮ್ಮ ಪ್ರಶ್ನೆಗಳನ್ನು ಕೇಳಿ — ನಾನು ಧ್ವನಿಯ ಮೂಲಕ ಉತ್ತರಿಸುತ್ತೇನೆ!",
        "input_placeholder": "💬 ಕನ್ನಡದಲ್ಲಿ ನಿಮ್ಮ ಕೃಷಿ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ..."
    },
    "मराठी": {
        "code": "mr",
        "speech_lang": "mr-IN",
        "title": "🤖🎙️ ॲग्रीसेन्स AI चॅट आणि व्हॉईस असिस्टंट",
        "subtitle": "तुमचा शेती मार्गदर्शक — बोला किंवा लिहा (AI उत्तर वाचून दाखवेल)",
        "tap_to_speak": "🎙️ बोलण्यासाठी माइक दाबा",
        "listening": "🔴 मराठीत ऐकत आहे... तुमचा प्रश्न बोला!",
        "stop_voice": "⏹ आवाज बंद करा",
        "auto_speak_label": "🔊 AI उत्तर मोठ्याने ऐकवा",
        "speed_label": "⚡ आवाजाचा वेग",
        "clear_chat": "🗑️ चॅट साफ करा",
        "switch_live": "⚡ थेट व्हॉईस कॉल मोड",
        "quick_title": "💡 जलद प्रश्न:",
        "chips": [
            ("🌾 माझ्या मातीसाठी कोणते पीक योग्य?", "माझ्या मातीचे पोषण आणि हवामानानुसार कोणते पीक सर्वाधिक उत्पादन देईल?"),
            ("💧 पाणी व्यवस्थापन?", "मातीच्या ओलाव्यानुसार पिकाला कधी आणि किती पाणी द्यावे?"),
            ("🌿 खतांचे नियोजन?", "माझ्या जमिनीतील NPK प्रमाणानुसार खतांचे योग्य वेळापत्रक काय असावे?"),
            ("🦠 कीड व रोग नियंत्रण?", "पिकांवरील कीड आणि पानांवरील रोगांचे सेंद्रिय व रासायनिक निवारण कसे करावे?")
        ],
        "greeting": "नमस्कार 👨‍🌾 **{name}**! मी तुमचा ॲग्रीसेन्स AI शेती सल्लागार आहे. कोणताही प्रश्न विचारा — मी उत्तर लिहून आणि बोलून दाखवेन!",
        "input_placeholder": "💬 मराठीत तुमचा शेती विषयक प्रश्न विचारा..."
    }
}


def clean_text_for_speech(text: str) -> str:
    """
    Strips markdown symbols, emojis, URLs, and formatting artifacts
    so browser Text-to-Speech (TTS) speaks natural, crystal-clear Indian language sentences.
    """
    if not text:
        return ""

    # Strip HTML tags
    clean = re.sub(r'<[^>]+>', ' ', text)
    # Strip URLs
    clean = re.sub(r'http\S+|www\.\S+', '', clean)

    # Strip all Unicode emoji ranges (emojis make TTS stutter or read out symbol names)
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FA6F"
        "\U0001FA70-\U0001FAFF"
        "\U00002600-\U000026FF"
        "\U00002B50-\U00002B55"
        "\U0000200D"
        "\U0000FE0F"
        "]+",
        flags=re.UNICODE
    )
    clean = emoji_pattern.sub('', clean)

    # Strip markdown headers, bold, italics, code blocks
    clean = re.sub(r'#+\s*', '', clean)
    clean = re.sub(r'[*_~`]+', '', clean)
    clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean)

    # Convert bullets and dashes to brief pauses
    clean = re.sub(r'[-–—•]\s*', ', ', clean)

    # Normalize punctuation & symbols
    clean = re.sub(r'[:;()[\]{}|]', ', ', clean)
    clean = re.sub(r'\n+', '. ', clean)
    clean = re.sub(r'\.{2,}', '.', clean)
    clean = re.sub(r',{2,}', ',', clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean



# =========================================================
# UNIFIED AI CHAT & VOICE ASSISTANT PAGE
# =========================================================

def show_ai_assistant():
    farmer = st.session_state.get("farmer")

    if not farmer:
        st.warning("Please login first.")
        return

    current_lang = st.session_state.get(
        "selected_language",
        farmer.get("language", "English")
    )
    if current_lang not in LANGUAGES_META:
        current_lang = "English"

    meta = LANGUAGES_META[current_lang]
    speech_lang = meta["speech_lang"]
    farmer_name = farmer.get("name", "Farmer")
    farmer_id = farmer.get("id", 1)

    # -----------------------------------------------------
    # HEADER WITH DYNAMIC LANGUAGE SWITCHER
    # -----------------------------------------------------
    st.markdown(
        f"""
        <div class="agri-card" style="background: linear-gradient(135deg, #14532d 0%, #15803d 60%, #16a34a 100%); color: white; padding: 22px; border-radius: 20px; margin-bottom: 14px; box-shadow: 0 8px 24px rgba(20, 83, 45, 0.25);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div>
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                        <span class="agri-pill pill-green" style="background: rgba(255,255,255,0.22); color: #ffffff; border: 1px solid rgba(255,255,255,0.4); font-size: 11px;">
                            🎙️ Smart Multilingual Agronomist
                        </span>
                        <span class="agri-pill pill-green" style="background: rgba(220, 252, 231, 0.25); color: #ffffff; font-size: 11px;">
                            👨‍🌾 {farmer_name}
                        </span>
                    </div>
                    <h2 style="color: white !important; margin: 0; font-size: 23px; font-weight: 800;">{meta['title']}</h2>
                    <p style="color: #dcfce7; margin: 4px 0 0 0; font-size: 13px; font-weight: 500;">{meta['subtitle']}</p>
                </div>
                <div style="font-size: 38px;">🌱</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Quick Toolbar: Language Switcher + Settings
    top_col1, top_col2, top_col3 = st.columns([3, 2, 2])

    with top_col1:
        lang_options = list(LANGUAGES_META.keys())
        current_index = lang_options.index(current_lang) if current_lang in lang_options else 0
        new_selected_lang = st.selectbox(
            "🌐 Active Language / భాష / भाषा",
            lang_options,
            index=current_index,
            key="chat_lang_picker"
        )
        if new_selected_lang != current_lang:
            st.session_state.selected_language = new_selected_lang
            st.session_state.language_code = LANGUAGES_META[new_selected_lang]["code"]
            st.session_state.farmer["language"] = new_selected_lang
            update_farmer_language(farmer_id, new_selected_lang)
            st.session_state.ai_messages = []
            st.rerun()

    with top_col2:
        auto_speak = st.checkbox(
            "🔊 Auto-Speak Audio",
            value=st.session_state.get("auto_speak_enabled", True),
            key="auto_speak_enabled",
            help="Automatically reads out AI answers out loud in clear speech for farmers."
        )

    with top_col3:
        voice_rate = st.selectbox(
            "⚡ Voice Speed",
            ["0.85x (Slow & Clear)", "1.0x (Normal)"],
            index=0 if st.session_state.get("voice_speed_rate", "0.85") == "0.85" else 1,
            key="voice_speed_select"
        )
        rate_val = "0.85" if "0.85" in voice_rate else "1.0"
        st.session_state.voice_speed_rate = rate_val

    # Actions: Live Call Mode / Clear History
    action_c1, action_c2 = st.columns([1, 1])
    with action_c1:
        if st.button("⚡ Switch to Gemini Live Phone Call", key="btn_switch_live_call", use_container_width=True):
            st.session_state.page = "voice_live"
            st.rerun()
    with action_c2:
        if st.button(meta["clear_chat"], key="btn_clear_chat_unified", use_container_width=True):
            st.session_state.ai_messages = []
            st.session_state.latest_tts_text = None
            st.rerun()

    st.markdown("---")

    # =====================================================
    # VOICE INPUT & REAL-TIME SPEECH MICROPHONE CONTROLLER
    # =====================================================
    st.markdown(
        f"""
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
            <span>🎙️ One-Tap Voice Microphone ({current_lang}):</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # HTML5 Web Speech Client for Voice Recognition & Speaking
    # Enhanced: Now uses postMessage to bridge voice text back to Streamlit chat
    html_voice_controller = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            * {{
                box-sizing: border-box;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            body {{
                margin: 0;
                padding: 4px;
                background: transparent;
            }}
            .voice-panel {{
                background: #ffffff;
                border: 1.5px solid #cbd5e1;
                border-radius: 16px;
                padding: 14px 18px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            }}
            .mic-btn {{
                width: 58px;
                height: 58px;
                border-radius: 50%;
                background: linear-gradient(135deg, #15803d 0%, #16a34a 100%);
                color: white;
                border: none;
                font-size: 26px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.2s ease;
                box-shadow: 0 4px 12px rgba(22, 163, 74, 0.35);
                flex-shrink: 0;
            }}
            .mic-btn:hover {{
                transform: scale(1.05);
            }}
            .mic-btn.listening {{
                background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%) !important;
                animation: pulse-ring 1.3s infinite;
            }}
            @keyframes pulse-ring {{
                0% {{ transform: scale(0.96); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }}
                70% {{ transform: scale(1.10); box-shadow: 0 0 0 14px rgba(239, 68, 68, 0); }}
                100% {{ transform: scale(0.96); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }}
            }}
            .status-text {{
                font-size: 14px;
                font-weight: 700;
                color: #1e293b;
                line-height: 1.3;
            }}
            .sub-status {{
                font-size: 12px;
                color: #64748b;
                margin-top: 2px;
            }}
            .stop-btn {{
                padding: 8px 14px;
                border-radius: 10px;
                background: #f1f5f9;
                border: 1px solid #cbd5e1;
                font-size: 13px;
                font-weight: 700;
                color: #334155;
                cursor: pointer;
                display: inline-flex;
                align-items: center;
                gap: 5px;
                transition: all 0.2s;
            }}
            .stop-btn:hover {{
                background: #e2e8f0;
                color: #0f172a;
            }}
            .transcript-box {{
                display: none;
                background: #f0fdf4;
                border: 1.5px solid #86efac;
                border-radius: 10px;
                padding: 10px 14px;
                margin-top: 8px;
                font-size: 13px;
                font-weight: 600;
                color: #166534;
            }}
            .transcript-box.active {{
                display: block;
            }}
        </style>
    </head>
    <body>
        <div class="voice-panel">
            <div style="display: flex; align-items: center; gap: 14px;">
                <button id="micBtn" class="mic-btn" title="{meta['tap_to_speak']}">🎙️</button>
                <div>
                    <div id="statusTitle" class="status-text">{meta['tap_to_speak']}</div>
                    <div id="statusSub" class="sub-status">Language: <strong>{current_lang} ({speech_lang})</strong> • AI answers will speak out loud</div>
                </div>
            </div>
            <div>
                <button id="stopVoiceBtn" class="stop-btn">
                    ⏹ {meta['stop_voice']}
                </button>
            </div>
        </div>
        <div id="transcriptBox" class="transcript-box"></div>

        <script>
            const speechLang = "{speech_lang}";
            const languageName = "{current_lang}";
            const farmerId = "{farmer_id}";
            const voiceSpeed = parseFloat("{rate_val}") || 0.85;

            const micBtn = document.getElementById("micBtn");
            const statusTitle = document.getElementById("statusTitle");
            const statusSub = document.getElementById("statusSub");
            const stopVoiceBtn = document.getElementById("stopVoiceBtn");
            const transcriptBox = document.getElementById("transcriptBox");

            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            let recognition = null;
            let isListening = false;
            let synth = window.speechSynthesis;

            if (SpeechRecognition) {{
                recognition = new SpeechRecognition();
                recognition.lang = speechLang;
                recognition.interimResults = false;
                recognition.maxAlternatives = 1;

                recognition.onstart = () => {{
                    isListening = true;
                    micBtn.classList.add("listening");
                    statusTitle.innerText = "🔴 " + "{meta['listening']}";
                    statusSub.innerText = "Speak clearly into your phone/computer microphone...";
                    transcriptBox.classList.remove("active");
                }};

                recognition.onresult = async (event) => {{
                    const transcript = event.results[0][0].transcript;
                    statusTitle.innerText = "⏳ Thinking: '" + transcript + "'...";
                    statusSub.innerText = "Consulting AgriSense AI & farm database...";
                    transcriptBox.innerHTML = "🎙️ <strong>You said:</strong> " + transcript;
                    transcriptBox.classList.add("active");

                    // Send to parent Streamlit window via query param for chat integration
                    try {{
                        const url = new URL(window.parent.location.href);
                        url.searchParams.set("voice_text", transcript);
                        window.parent.history.replaceState({{}}, "", url.toString());
                    }} catch(e) {{ /* cross-origin fallback */ }}

                    // Send to backend API for immediate voice answer
                    try {{
                        const backendHost = window.location.hostname || "localhost";
                        const response = await fetch("http://" + backendHost + ":8000/ai/ask", {{
                            method: "POST",
                            headers: {{ "Content-Type": "application/json" }},
                            body: JSON.stringify({{
                                farmer_id: parseInt(farmerId),
                                question: transcript,
                                language: languageName
                            }})
                        }});

                        if (response.ok) {{
                            const data = await response.json();
                            const answer = data.answer || "No reply";
                            statusTitle.innerText = "🟢 AgriSense AI is speaking...";
                            statusSub.innerText = "Question: " + transcript;
                            transcriptBox.innerHTML = "🎙️ <strong>You said:</strong> " + transcript + "<br/>🤖 <strong>AI:</strong> " + answer.substring(0, 200) + "...";
                            speakCleanText(answer);
                        }} else {{
                            throw new Error("API call failed");
                        }}
                    }} catch (err) {{
                        console.warn("Direct ask error:", err);
                        statusTitle.innerText = "✅ Voice recorded: " + transcript;
                        statusSub.innerText = "Please type or send below if needed.";
                    }}
                }};

                recognition.onerror = (event) => {{
                    console.error("Speech recognition error:", event.error);
                    statusTitle.innerText = "⚠️ Voice error: " + event.error;
                    statusSub.innerText = "Tap mic to try again in " + languageName;
                    micBtn.classList.remove("listening");
                    isListening = false;
                }};

                recognition.onend = () => {{
                    micBtn.classList.remove("listening");
                    isListening = false;
                }};
            }} else {{
                statusTitle.innerText = "⚠️ Speech Recognition not supported in this browser";
                statusSub.innerText = "Please use Google Chrome or Microsoft Edge on Mobile/Desktop.";
            }}

            function findBestVoice(langCode) {{
                if (!window.speechSynthesis) return null;
                const voices = window.speechSynthesis.getVoices();
                if (!voices || voices.length === 0) return null;
                const code = (langCode || "").toLowerCase().replace("_", "-");
                const prefix = code.split("-")[0];
                let match = voices.find(v => (v.lang.toLowerCase() === code || v.lang.toLowerCase().startsWith(prefix)) &&
                                              (v.name.includes("Natural") || v.name.includes("Google") || v.name.includes("Neural") || v.name.includes("Online")));
                if (match) return match;
                match = voices.find(v => v.lang.toLowerCase() === code);
                if (match) return match;
                match = voices.find(v => v.lang.toLowerCase().startsWith(prefix));
                return match || null;
            }}

            if (window.speechSynthesis) {{
                window.speechSynthesis.onvoiceschanged = () => {{
                    findBestVoice(speechLang);
                }};
            }}

            function speakCleanText(rawText) {{
                if (!synth) return;
                synth.cancel();
                let clean = (rawText || "").replace(/<[^>]+>/g, " ")
                                           .replace(/http\\S+/g, "")
                                           .replace(/[#*_`~]/g, "")
                                           .replace(/[-–—•]/g, ", ")
                                           .replace(/[:;()\\[\\]{{}}|]/g, ", ")
                                           .replace(/\\n+/g, ". ")
                                           .replace(/\\s+/g, " ").trim();
                const utterance = new SpeechSynthesisUtterance(clean);
                const bestVoice = findBestVoice(speechLang);
                if (bestVoice) {{
                    utterance.voice = bestVoice;
                    utterance.lang = bestVoice.lang;
                }} else {{
                    utterance.lang = speechLang;
                }}
                utterance.pitch = 1.0;
                utterance.rate = voiceSpeed;
                utterance.volume = 1.0;
                utterance.onend = () => {{
                    statusTitle.innerText = "{meta['tap_to_speak']}";
                    statusSub.innerText = "Finished speaking in " + languageName;
                }};
                synth.speak(utterance);
            }}

            micBtn.onclick = () => {{
                if (!recognition) {{
                    alert("Speech Recognition is supported in Chrome & Edge.");
                    return;
                }}
                if (synth) synth.cancel();
                if (isListening) {{
                    recognition.stop();
                }} else {{
                    recognition.start();
                }}
            }};

            stopVoiceBtn.onclick = () => {{
                if (synth) synth.cancel();
                statusTitle.innerText = "{meta['tap_to_speak']}";
                statusSub.innerText = "Audio voice stopped.";
            }};
        </script>
    </body>
    </html>
    """
    components.html(html_voice_controller, height=110, scrolling=False)


    # =====================================================
    # QUICK QUESTION CHIPS
    # =====================================================
    st.markdown(f"<div style='font-size: 13px; font-weight: 700; color: #475569; margin: 10px 0 6px 0;'>{meta['quick_title']}</div>", unsafe_allow_html=True)
    chip_cols = st.columns(len(meta["chips"]))
    quick_prompt = None

    for idx, (chip_label, chip_query) in enumerate(meta["chips"]):
        with chip_cols[idx]:
            if st.button(chip_label, key=f"chip_dyn_{idx}_{current_lang}", use_container_width=True):
                quick_prompt = chip_query

    # =====================================================
    # CHAT HISTORY INITIALIZATION
    # =====================================================
    if "ai_messages" not in st.session_state or not st.session_state.ai_messages:
        formatted_greeting = meta["greeting"].format(name=farmer_name)
        st.session_state.ai_messages = [
            {
                "role": "assistant",
                "content": formatted_greeting
            }
        ]

    # =====================================================
    # DISPLAY CHAT CONVERSATION
    # =====================================================
    for msg_idx, message in enumerate(st.session_state.ai_messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # If assistant message, provide manual Listen Aloud button
            if message["role"] == "assistant":
                msg_audio_clean = clean_text_for_speech(message["content"])
                audio_col1, audio_col2 = st.columns([1, 4])
                with audio_col1:
                    clean_js_text = json.dumps(msg_audio_clean)
                    listen_html = f"""
                    <script>
                    function playCrispAudio() {{
                        if (!window.speechSynthesis) return;
                        window.speechSynthesis.cancel();
                        const text = {clean_js_text};
                        const utter = new SpeechSynthesisUtterance(text);
                        const voices = window.speechSynthesis.getVoices() || [];
                        const code = "{speech_lang}".toLowerCase().replace("_", "-");
                        const prefix = code.split("-")[0];
                        let v = voices.find(x => (x.lang.toLowerCase() === code || x.lang.toLowerCase().startsWith(prefix)) &&
                                                 (x.name.includes("Natural") || x.name.includes("Google") || x.name.includes("Neural") || x.name.includes("Online")));
                        if (!v) v = voices.find(x => x.lang.toLowerCase() === code || x.lang.toLowerCase().startsWith(prefix));
                        if (v) {{ utter.voice = v; utter.lang = v.lang; }} else {{ utter.lang = "{speech_lang}"; }}
                        utter.pitch = 1.0;
                        utter.rate = {rate_val};
                        utter.volume = 1.0;
                        window.speechSynthesis.speak(utter);
                    }}
                    </script>
                    <button onclick='playCrispAudio()' style="padding: 4px 12px; font-size: 12px; font-weight: 700; background: #dcfce7; color: #166534; border: 1.5px solid #86efac; border-radius: 8px; cursor: pointer;">
                        🔊 Listen Aloud
                    </button>
                    """
                    components.html(listen_html, height=35)

    # =====================================================
    # TEXT INPUT & REAL-TIME STREAMING RESPONSE
    # =====================================================
    user_input = st.chat_input(meta["input_placeholder"])
    if quick_prompt:
        user_input = quick_prompt

    if user_input:
        # 1. Append User Message
        st.session_state.ai_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # 2. Stream AI Response
        with st.chat_message("assistant"):
            try:
                stream_gen = ask_agrisense_stream(
                    farmer_id=farmer_id,
                    question=user_input,
                    language=current_lang
                )
                response_text = st.write_stream(stream_gen)
                st.session_state.ai_messages.append({"role": "assistant", "content": response_text})
                st.session_state.latest_tts_text = clean_text_for_speech(response_text)

                # Auto-speak if enabled
                if auto_speak and st.session_state.latest_tts_text:
                    js_speech_text = json.dumps(st.session_state.latest_tts_text)
                    auto_tts_html = f"""
                    <script>
                        if (window.speechSynthesis) {{
                            window.speechSynthesis.cancel();
                            const utter = new SpeechSynthesisUtterance({js_speech_text});
                            const voices = window.speechSynthesis.getVoices() || [];
                            const code = "{speech_lang}".toLowerCase().replace("_", "-");
                            const prefix = code.split("-")[0];
                            let v = voices.find(x => (x.lang.toLowerCase() === code || x.lang.toLowerCase().startsWith(prefix)) &&
                                                     (x.name.includes("Natural") || x.name.includes("Google") || x.name.includes("Neural") || x.name.includes("Online")));
                            if (!v) v = voices.find(x => x.lang.toLowerCase() === code || x.lang.toLowerCase().startsWith(prefix));
                            if (v) {{ utter.voice = v; utter.lang = v.lang; }} else {{ utter.lang = "{speech_lang}"; }}
                            utter.pitch = 1.0;
                            utter.rate = {rate_val};
                            utter.volume = 1.0;
                            window.speechSynthesis.speak(utter);
                        }}
                    </script>
                    """
                    components.html(auto_tts_html, height=0)

            except Exception as err:
                st.error(f"AI Assistant Error: {err}")