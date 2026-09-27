"""
AgriSense AI — Professional Multilingual Voice & AI Chat Assistant
===================================================================
Provides two distinct, presentation-grade modes:
  1. 🎙️ Dedicated Voice Assistant Mode: Standalone, large glowing microphone orb
     with real-time speech recognition, animated acoustic waves, and instant audio playback.
  2. 💬 Text Conversation Mode: Clean, mobile-friendly chat bubble interface
     with quick question chips, streaming AI response, and 'Listen Aloud' audio controls.

Supports 6 Indian languages: English, Telugu, Hindi, Tamil, Kannada, Marathi.
"""

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
        "title": "AgriSense AI Voice & Chat Assistant",
        "subtitle": "Your AI Agronomist — Speak in your native language or type questions",
        "tab_voice": "🎙️ Dedicated Voice Assistant",
        "tab_chat": "💬 Text Chat & History",
        "tap_to_speak": "Tap Microphone to Speak",
        "listening": "Listening in English... Speak your question now!",
        "stop_voice": "Stop Voice Audio",
        "clear_chat": "Clear Chat History",
        "chips": [
            ("🌾 Best crop for my soil?", "What is the best crop recommendation for my soil and climate conditions?"),
            ("💧 Irrigation advice?", "Based on my current soil moisture and temperature, how should I irrigate my farm?"),
            ("🌿 Fertilizer schedule?", "What is the recommended fertilizer application schedule for my farm's NPK values?"),
            ("🏛️ Government subsidies?", "What are the top government agriculture subsidies and schemes available for my farm?")
        ],
        "greeting": "Namaste 👨‍🌾 **{name}**! I am your AgriSense AI farming assistant. Speak into the microphone or type below — I will answer and explain everything clearly!",
        "input_placeholder": "💬 Type your farming question in English..."
    },
    "తెలుగు": {
        "code": "te",
        "speech_lang": "te-IN",
        "title": "అగ్రిసెన్స్ AI వాయిస్ & చాట్ అసిస్టెంట్",
        "subtitle": "మీ వ్యవసాయ సలహాదారు — మాట్లాడండి లేదా టైప్ చేయండి",
        "tab_voice": "🎙️ ప్రత్యేక వాయిస్ అసిస్టెంట్",
        "tab_chat": "💬 చాట్ & మునుపటి ప్రశ్నలు",
        "tap_to_speak": "మాట్లాడటానికి మైక్ నొక్కండి",
        "listening": "తెలుగులో వింటున్నాను... మీ ప్రశ్న మాట్లాడండి!",
        "stop_voice": "వాయిస్ ఆపండి",
        "clear_chat": "చాట్ క్లియర్ చేయండి",
        "chips": [
            ("🌾 ఏ పంట మంచిది?", "నా నేల పోషకాలు మరియు వాతావరణానికి ఏ పంట వేస్తే ఎక్కువ దిగుబడి వస్తుంది?"),
            ("💧 ఎంత నీరు పెట్టాలి?", "నా పొలం తేమ ప్రకారం నీటిపారుదల ఎప్పుడు మరియు ఎంత ఇవ్వాలి?"),
            ("🌿 ఎరువుల మోతాదు?", "నా పొలంలోని NPK విలువల ప్రకారం ఏ ఎరువులు ఎంత మోతాదులో వేయాలి?"),
            ("🏛️ ప్రభుత్వ సబ్సిడీలు?", "నా పొలానికి వర్తించే ముఖ్యమైన ప్రభుత్వ వ్యవసాయ పథకాలు మరియు సబ్సిడీలు ఏమిటి?")
        ],
        "greeting": "నమస్తే 👨‍🌾 **{name}** గారు! నేను మీ అగ్రిసెన్స్ AI వ్యవసాయ సహాయకుడిని. మైక్ నొక్కి మాట్లాడండి లేదా కింద టైప్ చేయండి — నేను వివరంగా సమాధానం చెబుతాను!",
        "input_placeholder": "💬 తెలుగులో మీ వ్యవసాయ ప్రశ్నను అడగండి..."
    },
    "हिंदी": {
        "code": "hi",
        "speech_lang": "hi-IN",
        "title": "एग्रीसेंस AI वॉइस और चैट सहायक",
        "subtitle": "आपका कृषि विशेषज्ञ — बोलें या लिखें",
        "tab_voice": "🎙️ समर्पित वॉइस सहायक",
        "tab_chat": "💬 टेक्स्ट चैट और इतिहास",
        "tap_to_speak": "बोलने के लिए माइक दबाएं",
        "listening": "हिंदी में सुन रहा हूँ... अपना सवाल बोलें!",
        "stop_voice": "आवाज़ बंद करें",
        "clear_chat": "चैट साफ करें",
        "chips": [
            ("🌾 सबसे अच्छी फसल?", "मेरी मिट्टी की गुणवत्ता और मौसम के अनुसार सबसे अच्छी फसल कौन सी है?"),
            ("💧 सिंचाई कितनी करें?", "मेरी खेत की नमी के अनुसार सिंचाई का सही समय और पानी की मात्रा बताएं?"),
            ("🌿 खाद की सही मात्रा?", "मेरे खेत के NPK मान के आधार पर खाद का सही समय और मात्रा बताएं?"),
            ("🏛️ सरकारी सब्सिडी?", "किसानों के लिए प्रमुख सरकारी कृषि योजनाएं और सब्सिडी कौन सी हैं?")
        ],
        "greeting": "नमस्ते 👨‍🌾 **{name}** जी! मैं आपका एग्रीसेंस AI कृषि सहायक हूँ। माइक दबाकर बोलें या लिखें — मैं आपको पूरा समाधान बताऊंगा!",
        "input_placeholder": "💬 हिंदी में अपना खेती से जुड़ा सवाल पूछें..."
    },
    "தமிழ்": {
        "code": "ta",
        "speech_lang": "ta-IN",
        "title": "அக்ரிசென்ஸ் AI குரல் மற்றும் அரட்டை உதவியாளர்",
        "subtitle": "உங்கள் விவசாய ஆலோசகர் — பேசுங்கள் அல்லது தட்டச்சு செய்யுங்கள்",
        "tab_voice": "🎙️ குரல் உதவியாளர்",
        "tab_chat": "💬 உரை அரட்டை",
        "tap_to_speak": "பேச மைக்கை அழுத்தவும்",
        "listening": "தமிழில் கேட்கிறது... உங்கள் கேள்வியைப் பேசுங்கள்!",
        "stop_voice": "குரலை நிறுத்து",
        "clear_chat": "அரட்டையை அழிக்கவும்",
        "chips": [
            ("🌾 சிறந்த பயிர்?", "என் மண் மற்றும் தட்பவெப்ப நிலைக்கு எந்த பயிர் ஏற்றது?"),
            ("💧 பாசன அளவு?", "என் மண்ணின் ஈரப்பதத்திற்கு ஏற்ப பாசன அளவு என்ன?"),
            ("🌿 உர அளவு?", "என் மண்ணின் NPK அளவுக்கு ஏற்ப உரமிடும் முறை என்ன?"),
            ("🏛️ அரசு மானியம்?", "விவசாயிகளுக்கான முக்கிய அரசு மானியங்கள் என்ன?")
        ],
        "greeting": "வணக்கம் 👨‍🌾 **{name}**! உங்கள் விவசாயக் கேள்விகளை மைக்கில் பேசலாம் அல்லது தட்டச்சு செய்யலாம்!",
        "input_placeholder": "💬 தமிழில் உங்கள் கேள்வியைக் கேளுங்கள்..."
    },
    "ಕನ್ನಡ": {
        "code": "kn",
        "speech_lang": "kn-IN",
        "title": "ಅಗ್ರಿಸೆನ್ಸ್ AI ವಾಯ್ಸ್ ಮತ್ತು ಚಾಟ್ ಸಹಾಯಕ",
        "subtitle": "ನಿಮ್ಮ ಕೃಷಿ ಸಲಹೆಗಾರ — ಮಾತನಾಡಿ ಅಥವಾ ಬರೆಯಿರಿ",
        "tab_voice": "🎙️ ವಾಯ್ಸ್ ಸಹಾಯಕ",
        "tab_chat": "💬 ಚಾಟ್ ಇತಿಹಾಸ",
        "tap_to_speak": "ಮಾತನಾಡಲು ಮೈಕ್ ಒತ್ತಿ",
        "listening": "ಕನ್ನಡದಲ್ಲಿ ಆಲಿಸಲಾಗುತ್ತಿದೆ... ಪ್ರಶ್ನೆ ಮಾತನಾಡಿ!",
        "stop_voice": "ಧ್ವನಿ ನಿಲ್ಲಿಸಿ",
        "clear_chat": "ಚಾಟ್ ಅಳಿಸಿ",
        "chips": [
            ("🌾 ಸೂಕ್ತ ಬೆಳೆ?", "ನನ್ನ ಮಣ್ಣಿಗೆ ಯಾವ ಬೆಳೆ ಉತ್ತಮ?"),
            ("💧 ನೀರಾವರಿ?", "ನನ್ನ ಮಣ್ಣಿನ ತೇವಾಂಶಕ್ಕೆ ನೀರಾವರಿ ಹೇಗೆ ಮಾಡಬೇಕು?"),
            ("🌿 ರಸಗೊಬ್ಬರ?", "ರಸಗೊಬ್ಬರ ಪ್ರಮಾಣ ಎಷ್ಟು?"),
            ("🏛️ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು?", "ಪ್ರಮುಖ ಸರ್ಕಾರಿ ಕೃಷಿ ಸಬ್ಸಿಡಿಗಳು ಯಾವುವು?")
        ],
        "greeting": "ನಮಸ್ಕಾರ 👨‍🌾 **{name}**! ಮೈಕ್ ಒತ್ತಿ ಮಾತನಾಡಿ ಅಥವಾ ಟೈಪ್ ಮಾಡಿ — ನಾನು ಉತ್ತರಿಸುತ್ತೇನೆ!",
        "input_placeholder": "💬 ಕನ್ನಡದಲ್ಲಿ ಪ್ರಶ್ನೆ ಕೇಳಿ..."
    },
    "मराठी": {
        "code": "mr",
        "speech_lang": "mr-IN",
        "title": "ॲग्रीसेन्स AI व्हॉईस आणि चॅट असिस्टंट",
        "subtitle": "तुमचा शेती मार्गदर्शक — बोला किंवा लिहा",
        "tab_voice": "🎙️ व्हॉईस असिस्टंट",
        "tab_chat": "💬 चॅट आणि इतिहास",
        "tap_to_speak": "बोलण्यासाठी माइक दाबा",
        "listening": "मराठीत ऐकत आहे... तुमचा प्रश्न बोला!",
        "stop_voice": "आवाज बंद करा",
        "clear_chat": "चॅट साफ करा",
        "chips": [
            ("🌾 योग्य पीक?", "माझ्या मातीसाठी सर्वात योग्य पीक कोणते?"),
            ("💧 सिंचन सल्ला?", "जमिनीतील ओलाव्यानुसार पाणी कधी द्यावे?"),
            ("🌿 खताचे प्रमाण?", "माझ्या शेतासाठी खताचे योग्य प्रमाण काय?"),
            ("🏛️ सरकारी योजना?", "शेतकऱ्यांसाठी प्रमुख सरकारी योजना कोणत्या?")
        ],
        "greeting": "नमस्कार 👨‍🌾 **{name}**! माइक दाबा आणि बोला किंवा लिहा — मी शेतीविषयक मार्गदर्शन करेन!",
        "input_placeholder": "💬 मराठीत प्रश्न विचारा..."
    }
}


def clean_text_for_speech(text: str) -> str:
    """Strips markdown and emojis for clean, natural speech pronunciation."""
    if not text:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = re.sub(r'http\S+|www\.\S+', '', clean)
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0\U000024C2-\U0001F251\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F"
        "\U0001FA70-\U0001FAFF\U00002600-\U000026FF\U00002B50-\U00002B55\U0000200D\U0000FE0F]+",
        flags=re.UNICODE
    )
    clean = emoji_pattern.sub('', clean)
    clean = re.sub(r'#+\s*', '', clean)
    clean = re.sub(r'[*_~`]+', '', clean)
    clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean)
    clean = re.sub(r'[-–—•]\s*', ', ', clean)
    clean = re.sub(r'[:;()[\]{}|]', ', ', clean)
    clean = re.sub(r'\n+', '. ', clean)
    clean = re.sub(r'\.{2,}', '.', clean)
    clean = re.sub(r',{2,}', ',', clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean


# =========================================================
# MAIN AI ASSISTANT VIEW
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

    # 1. Sleek Mobile-Friendly Hero Header
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #14532d 0%, #15803d 60%, #16a34a 100%); color: white; padding: 20px 22px; border-radius: 18px; margin-bottom: 16px; box-shadow: 0 6px 20px rgba(20, 83, 45, 0.22);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                <div>
                    <span style="background: rgba(255,255,255,0.20); color: #ffffff; padding: 3px 10px; border-radius: 9999px; font-size: 11px; font-weight: 700; border: 1px solid rgba(255,255,255,0.30);">
                        🎙️ AgriSense Multilingual AI
                    </span>
                    <h2 style="color: white !important; margin: 8px 0 2px 0; font-size: 22px; font-weight: 800;">
                        {meta['title']}
                    </h2>
                    <p style="color: #bbf7d0; margin: 0; font-size: 13px; font-weight: 500;">
                        {meta['subtitle']}
                    </p>
                </div>
                <div style="font-size: 36px;">🤖</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. Two Clean, Distinct Modes: Voice Mode vs Text Chat Mode
    tab_voice, tab_chat = st.tabs([
        meta["tab_voice"],
        meta["tab_chat"]
    ])

    # =====================================================
    # TAB 1: 🎙️ DEDICATED SEPARATE VOICE ASSISTANT (MIC MODE)
    # =====================================================
    with tab_voice:
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 8px;">
                <p style="color: #64748b; font-size: 14px; margin: 0; font-weight: 600;">
                    Speak into the microphone in <b>{current_lang} ({speech_lang})</b>. AgriSense AI will listen and speak out the answer.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Dedicated, Professional Voice Orb & Audio Waveform Component
        voice_orb_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                * {{ box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
                body {{ margin: 0; padding: 12px; background: transparent; text-align: center; }}
                
                .voice-card {{
                    background: #ffffff;
                    border: 2px solid #e2e8f0;
                    border-radius: 24px;
                    padding: 28px 20px;
                    max-width: 480px;
                    margin: 0 auto;
                    box-shadow: 0 8px 28px rgba(0,0,0,0.06);
                }}

                /* Glowing Central Mic Button */
                .mic-container {{
                    position: relative;
                    width: 100px;
                    height: 100px;
                    margin: 12px auto 18px auto;
                }}

                .mic-orb {{
                    width: 90px;
                    height: 90px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #15803d 0%, #16a34a 100%);
                    color: white;
                    border: none;
                    font-size: 38px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 8px 24px rgba(22, 163, 74, 0.40);
                    transition: all 0.25s ease;
                    outline: none;
                }}

                .mic-orb:hover {{
                    transform: scale(1.06);
                    box-shadow: 0 10px 30px rgba(22, 163, 74, 0.55);
                }}

                .mic-orb.active-listening {{
                    background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%) !important;
                    animation: pulse-wave 1.4s infinite;
                }}

                @keyframes pulse-wave {{
                    0% {{ transform: scale(0.96); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }}
                    70% {{ transform: scale(1.08); box-shadow: 0 0 0 18px rgba(239, 68, 68, 0); }}
                    100% {{ transform: scale(0.96); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }}
                }}

                /* Soundwave Visualizer Bars */
                .wave-bars {{
                    display: none;
                    justify-content: center;
                    align-items: center;
                    gap: 5px;
                    height: 28px;
                    margin: 10px 0;
                }}
                .wave-bars.active {{
                    display: flex;
                }}
                .bar {{
                    width: 4px;
                    background: #16a34a;
                    border-radius: 3px;
                    animation: wave-anim 1s ease-in-out infinite;
                }}
                .bar:nth-child(1) {{ height: 10px; animation-delay: 0.1s; }}
                .bar:nth-child(2) {{ height: 22px; animation-delay: 0.2s; }}
                .bar:nth-child(3) {{ height: 16px; animation-delay: 0.3s; }}
                .bar:nth-child(4) {{ height: 28px; animation-delay: 0.4s; }}
                .bar:nth-child(5) {{ height: 14px; animation-delay: 0.2s; }}
                .bar:nth-child(6) {{ height: 20px; animation-delay: 0.1s; }}
                .bar:nth-child(7) {{ height: 8px; animation-delay: 0.3s; }}

                @keyframes wave-anim {{
                    0%, 100% {{ transform: scaleY(0.4); }}
                    50% {{ transform: scaleY(1.2); }}
                }}

                .status-badge {{
                    display: inline-block;
                    background: #f1f5f9;
                    color: #0f172a;
                    padding: 6px 16px;
                    border-radius: 999px;
                    font-size: 14px;
                    font-weight: 800;
                    margin-bottom: 8px;
                }}

                .status-sub {{
                    font-size: 13px;
                    color: #64748b;
                    font-weight: 600;
                }}

                .transcript-display {{
                    display: none;
                    background: #f0fdf4;
                    border: 1.5px solid #86efac;
                    border-radius: 12px;
                    padding: 12px 16px;
                    margin-top: 14px;
                    text-align: left;
                    font-size: 14px;
                    color: #166534;
                    line-height: 1.5;
                }}

                .stop-btn {{
                    background: #f1f5f9;
                    border: 1.5px solid #cbd5e1;
                    border-radius: 10px;
                    padding: 8px 18px;
                    font-size: 13px;
                    font-weight: 700;
                    color: #475569;
                    cursor: pointer;
                    margin-top: 14px;
                    display: inline-flex;
                    align-items: center;
                    gap: 6px;
                    transition: all 0.2s;
                }}
                .stop-btn:hover {{
                    background: #e2e8f0;
                    color: #0f172a;
                }}
            </style>
        </head>
        <body>
            <div class="voice-card">
                <div id="statusBadge" class="status-badge">
                    🎙️ {meta['tap_to_speak']}
                </div>
                <div id="statusSub" class="status-sub">
                    Language: <strong>{current_lang} ({speech_lang})</strong>
                </div>

                <div class="mic-container">
                    <button id="micOrb" class="mic-orb" title="Tap to Speak">🎙️</button>
                </div>

                <div id="waveBars" class="wave-bars">
                    <div class="bar"></div>
                    <div class="bar"></div>
                    <div class="bar"></div>
                    <div class="bar"></div>
                    <div class="bar"></div>
                    <div class="bar"></div>
                    <div class="bar"></div>
                </div>

                <div id="transcriptBox" class="transcript-display"></div>

                <div>
                    <button id="stopVoiceBtn" class="stop-btn">
                        ⏹ {meta['stop_voice']}
                    </button>
                </div>
            </div>

            <script>
                const speechLang = "{speech_lang}";
                const languageName = "{current_lang}";
                const farmerId = "{farmer_id}";

                const micOrb = document.getElementById("micOrb");
                const statusBadge = document.getElementById("statusBadge");
                const statusSub = document.getElementById("statusSub");
                const waveBars = document.getElementById("waveBars");
                const transcriptBox = document.getElementById("transcriptBox");
                const stopVoiceBtn = document.getElementById("stopVoiceBtn");

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
                        micOrb.classList.add("active-listening");
                        waveBars.classList.add("active");
                        statusBadge.innerText = "🔴 Listening in " + languageName + "...";
                        statusBadge.style.background = "#fee2e2";
                        statusBadge.style.color = "#b91c1c";
                        statusSub.innerText = "Speak your agricultural question clearly...";
                        transcriptBox.style.display = "none";
                    }};

                    recognition.onresult = async (event) => {{
                        const transcript = event.results[0][0].transcript;
                        isListening = false;
                        micOrb.classList.remove("active-listening");
                        statusBadge.innerText = "⏳ Thinking...";
                        statusBadge.style.background = "#fef3c7";
                        statusBadge.style.color = "#92400e";
                        statusSub.innerText = "Consulting AgriSense AI Engine...";

                        transcriptBox.innerHTML = "<b>🗣️ You Asked:</b> &ldquo;" + transcript + "&rdquo;";
                        transcriptBox.style.display = "block";

                        // Send query to parent Streamlit chat
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
                                const answer = data.answer || "No response";
                                statusBadge.innerText = "🔊 AgriSense AI Speaking...";
                                statusBadge.style.background = "#dcfce7";
                                statusBadge.style.color = "#166534";
                                statusSub.innerText = "Speaking out loud in " + languageName;
                                transcriptBox.innerHTML += "<br/><br/><b>🤖 AI Answer:</b> " + answer;
                                speakCleanText(answer);
                            }} else {{
                                throw new Error("Backend query failed");
                            }}
                        }} catch (e) {{
                            console.warn("Direct voice API fallback:", e);
                            statusBadge.innerText = "✅ Recorded: '" + transcript + "'";
                            statusBadge.style.background = "#e0f2fe";
                            statusBadge.style.color = "#0369a1";
                            statusSub.innerText = "Check Chat Tab to view full response";
                            waveBars.classList.remove("active");
                        }}
                    }};

                    recognition.onerror = (e) => {{
                        isListening = false;
                        micOrb.classList.remove("active-listening");
                        waveBars.classList.remove("active");
                        statusBadge.innerText = "⚠️ Voice Notice: " + (e.error || "Ready");
                        statusBadge.style.background = "#f1f5f9";
                        statusBadge.style.color = "#475569";
                        statusSub.innerText = "Tap the microphone to try again";
                    }};

                    recognition.onend = () => {{
                        micOrb.classList.remove("active-listening");
                        waveBars.classList.remove("active");
                    }};
                }} else {{
                    statusBadge.innerText = "⚠️ Voice Speech Not Supported";
                    statusSub.innerText = "Please open in Google Chrome or Microsoft Edge";
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
                    utterance.lang = speechLang;
                    utterance.rate = 0.90;
                    utterance.pitch = 1.0;
                    utterance.onend = () => {{
                        statusBadge.innerText = "🎙️ {meta['tap_to_speak']}";
                        statusBadge.style.background = "#f1f5f9";
                        statusBadge.style.color = "#0f172a";
                        statusSub.innerText = "Language: " + languageName;
                        waveBars.classList.remove("active");
                    }};
                    synth.speak(utterance);
                }}

                micOrb.onclick = () => {{
                    if (!recognition) {{
                        alert("Speech recognition is supported in Chrome & Edge.");
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
                    if (recognition && isListening) recognition.stop();
                    statusBadge.innerText = "🎙️ {meta['tap_to_speak']}";
                    statusBadge.style.background = "#f1f5f9";
                    statusBadge.style.color = "#0f172a";
                    statusSub.innerText = "Audio stopped.";
                    waveBars.classList.remove("active");
                }};
            </script>
        </body>
        </html>
        """
        components.html(voice_orb_html, height=390, scrolling=False)

        # Quick Voice Question Chips for Farmers
        st.markdown(
            f"""
            <div style="font-size: 13px; font-weight: 700; color: #475569; margin: 12px 0 8px 0; text-align: center;">
                💡 1-Tap Quick Questions (Tap to Ask AI):
            </div>
            """,
            unsafe_allow_html=True
        )
        q_cols = st.columns(len(meta["chips"]))
        for idx, (chip_label, chip_query) in enumerate(meta["chips"]):
            with q_cols[idx]:
                if st.button(chip_label, key=f"voice_chip_{idx}_{current_lang}", use_container_width=True):
                    with st.spinner("🤖 Consulting AgriSense AI..."):
                        try:
                            stream_gen = ask_agrisense_stream(farmer_id=farmer_id, question=chip_query, language=current_lang)
                            st.write_stream(stream_gen)
                        except Exception as e:
                            st.error(f"Error: {e}")

    # =====================================================
    # TAB 2: 💬 TEXT CHAT & CONVERSATION HISTORY
    # =====================================================
    with tab_chat:
        col_clear, col_mode = st.columns([1, 2])
        with col_clear:
            if st.button(f"🗑️ {meta['clear_chat']}", key="btn_clear_chat_tab", use_container_width=True):
                st.session_state.ai_messages = []
                st.session_state.latest_tts_text = None
                st.rerun()

        # Chat History Initialization
        if "ai_messages" not in st.session_state or not st.session_state.ai_messages:
            formatted_greeting = meta["greeting"].format(name=farmer_name)
            st.session_state.ai_messages = [
                {
                    "role": "assistant",
                    "content": formatted_greeting
                }
            ]

        # Display Chat Conversation
        for message in st.session_state.ai_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Text input at bottom
        user_text = st.chat_input(meta["input_placeholder"])
        if user_text:
            st.session_state.ai_messages.append({"role": "user", "content": user_text})
            with st.chat_message("user"):
                st.markdown(user_text)

            with st.chat_message("assistant"):
                try:
                    stream_gen = ask_agrisense_stream(
                        farmer_id=farmer_id,
                        question=user_text,
                        language=current_lang
                    )
                    ans_text = st.write_stream(stream_gen)
                    st.session_state.ai_messages.append({"role": "assistant", "content": ans_text})
                except Exception as err:
                    st.error(f"AI Assistant Error: {err}")