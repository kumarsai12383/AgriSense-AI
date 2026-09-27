import os
import json
import streamlit as st
import streamlit.components.v1 as components

# =========================================================
# MULTILINGUAL STEP-BY-STEP USER GUIDE & VOICE SCRIPTS
# =========================================================

HELP_TEXT = {
    "en": {
        "title": "❓ Farmer Help Center & Step-by-Step Guide",
        "subtitle": "Easy visual guide to operate all AgriSense AI features efficiently",
        "voice_title": "🔊 Listen to Step-by-Step Audio Guide (45s)",
        "voice_sub": "Clear voice explanation — Tap Play to listen to how to use the app",
        "btn_play": "🔊 Play Audio Guide",
        "btn_stop": "⏹ Stop",
        "speech_lang": "en-IN",
        "steps_header": "🚜 7-Step Complete Farming Workflow",
        "faq_header": "❓ Common Farmer Doubts & Troubleshooting",
        "steps": [
            {
                "num": "1",
                "icon": "🌐",
                "title": "Select Language & Login",
                "desc": "Choose your native language (Telugu, Hindi, Tamil, Kannada, Marathi, English) at the top of the screen. Enter your name and 10-digit mobile number to open your personalized dashboard.",
                "action_btn": "Go to Login / Profile",
                "target": "home"
            },
            {
                "num": "2",
                "icon": "📡",
                "title": "Enter Soil Data or Connect ESP32",
                "desc": "Open 'My Farm Data'. Either manually type your soil Nitrogen (N), Phosphorus (P), Potassium (K), pH, and Moisture, or connect your ESP32 7-in-1 sensor to sync readings automatically.",
                "action_btn": "Open Farm Data",
                "target": "farm"
            },
            {
                "num": "3",
                "icon": "🌾",
                "title": "Get AI Crop Recommendation",
                "desc": "Tap 'Find Best Crop'. The machine learning engine analyzes your soil nutrients and climate to recommend the highest-yielding crop with confidence scores and top alternative choices.",
                "action_btn": "Open Crop Recommendation",
                "target": "crop"
            },
            {
                "num": "4",
                "icon": "💧",
                "title": "Check Smart Irrigation & Pump Time",
                "desc": "Open 'Smart Irrigation'. Check your live soil moisture gauge. If it shows Red (Urgent), irrigate today. Use the built-in calculator to find exact water liters and motor pumping run-time for your acreage.",
                "action_btn": "Open Irrigation Advisor",
                "target": "water"
            },
            {
                "num": "5",
                "icon": "🌿",
                "title": "Follow 4-Stage Fertilizer Plan",
                "desc": "Open 'Fertilizer Guidance'. View your soil NPK deficit score and check the 4-stage split-dose table: Stage 1 (Basal at sowing), Stage 2 (Tillering), Stage 3 (Flowering), and Stage 4 (Grain filling).",
                "action_btn": "Open Fertilizer Advisor",
                "target": "fertilizer"
            },
            {
                "num": "6",
                "icon": "🦠",
                "title": "Diagnose Plant Diseases (Leaf Doctor)",
                "desc": "If crop leaves show spots, yellowing, or pests, open 'Plant Disease Doctor'. Take a clear photo or upload an image. The AI Vision Doctor will identify the disease and prescribe organic and chemical cures.",
                "action_btn": "Open Disease Doctor",
                "target": "disease"
            },
            {
                "num": "7",
                "icon": "🤖🎙️",
                "title": "Ask AgriSense AI by Voice or Call",
                "desc": "Tap 'AgriSense AI Chat & Voice' or 'Gemini Live Call'. Speak naturally in your regional language. Ask any question about weather, seeds, mandi prices, or pest control to get instant spoken answers.",
                "action_btn": "Open Voice AI Assistant",
                "target": "voice"
            }
        ]
    },
    "te": {
        "title": "❓ రైతు సహాయ కేంద్రం & ఉపయోగించే విధానం",
        "subtitle": "అగ్రిసెన్స్ AI యాప్‌ను సులభంగా మరియు సమర్థవంతంగా ఎలా ఉపయోగించాలో దశలవారీ గైడ్",
        "voice_title": "🔊 యాప్ ఉపయోగించే విధానం వాయిస్ వినండి (45 సెకన్లు)",
        "voice_sub": "స్పష్టమైన తెలుగు వాయిస్‌లో — యాప్ ఎలా వాడాలో వినడానికి నొక్కండి",
        "btn_play": "🔊 గైడ్ వినండి (Play Audio)",
        "btn_stop": "⏹ ఆపండి",
        "speech_lang": "te-IN",
        "steps_header": "🚜 7 దశల్లో పూర్తి వ్యవసాయ మార్గదర్శకత్వం",
        "faq_header": "❓ రైతుల ముఖ్య సందేహాలు & సమాధానాలు",
        "steps": [
            {
                "num": "1",
                "icon": "🌐",
                "title": "భాషను ఎంచుకోండి & లాగిన్ అవ్వండి",
                "desc": "స్క్రీన్ పైభాగంలో మీ మాతృభాషను (తెలుగు) ఎంచుకోండి. మీ పేరు మరియు 10 అంకెల మొబైల్ నంబర్‌ను నమోదు చేసి డ్యాష్‌బోర్డ్‌లోకి ప్రవేశించండి.",
                "action_btn": "ప్రొఫైల్ చూడండి",
                "target": "home"
            },
            {
                "num": "2",
                "icon": "📡",
                "title": "పొలం వివరాలు నమోదు చేయండి లేదా ESP32 సెన్సార్ కలపండి",
                "desc": "'నా పొలం డేటా' పేజీకి వెళ్లి, మీ నేల నత్రజని (N), భాస్వరం (P), పొటాష్ (K), pH మరియు తేమ నమోదు చేయండి లేదా ESP32 సెన్సార్ ద్వారా ఆటోమేటిక్‌గా రీడింగ్ పొందండి.",
                "action_btn": "పొలం డేటా తెరవండి",
                "target": "farm"
            },
            {
                "num": "3",
                "icon": "🌾",
                "title": "AI పంట సిఫార్సును పొందండి",
                "desc": "'మంచి పంటను తెలుసుకోండి' బటన్ నొక్కండి. మీ నేల పోషకాలు మరియు వాతావరణాన్ని పరిశీలించి AI అధిక దిగుబడినిచ్చే ఉత్తమ పంటను సిఫార్సు చేస్తుంది.",
                "action_btn": "పంట సిఫార్సు చూడండి",
                "target": "crop"
            },
            {
                "num": "4",
                "icon": "💧",
                "title": "స్మార్ట్ నీటిపారుదల & మోటార్ సమయం తనిఖీ చేయండి",
                "desc": "'స్మార్ట్ నీటిపారుదల' పేజీలో నేల తేమను చూడండి. ఎరుపు రంగు వస్తే ఈరోజే నీరు పెట్టండి. మీ ఎకరాల విస్తీర్ణానికి ఎంత నీరు మరియు ఎంత సమయం మోటార్ వేయాలో తెలుసుకోండి.",
                "action_btn": "నీటిపారుదల సలహాదారు",
                "target": "water"
            },
            {
                "num": "5",
                "icon": "🌿",
                "title": "4 దశల ఎరువుల ప్రణాళికను పాటించండి",
                "desc": "'ఎరువుల సలహాదారు' తెరవండి. మీ నేలలో ఏ పోషకం తక్కువగా ఉందో చూసి, విత్తే సమయం, శాకీయ పెరుగుదల, పూత మరియు గింజ బలం దశల్లో ఎరువుల బస్తాల మోతాదు తెలుసుకోండి.",
                "action_btn": "ఎరువుల సలహా చూడండి",
                "target": "fertilizer"
            },
            {
                "num": "6",
                "icon": "🦠",
                "title": "పంట తెగుళ్లను గుర్తించండి (లీఫ్ డాక్టర్)",
                "desc": "ఆకులపై మచ్చలు లేదా తెగుళ్లు కనిపిస్తే 'పంట వ్యాధి డాక్టర్' తెరవండి. ఆకు ఫోటో తీసి అప్‌లోడ్ చేస్తే AI తక్షణ నివారణ మరియు మందులను సూచిస్తుంది.",
                "action_btn": "తెగుళ్ల డాక్టర్ తెరవండి",
                "target": "disease"
            },
            {
                "num": "7",
                "icon": "🤖🎙️",
                "title": "AI తో మాట్లాడండి లేదా లైవ్ కాల్ చేయండి",
                "desc": "'అగ్రిసెన్స్ AI చాట్ & వాయిస్' నొక్కండి. మైక్ ద్వారా తెలుగులోనే మాట్లాడి వాతావరణం, విత్తనాలు లేదా క్రిమిసంహారకాల గురించి ఏ సందేహమైనా అడిగి తెలుసుకోండి.",
                "action_btn": "వాయిస్ AI అసిస్టెంట్",
                "target": "voice"
            }
        ]
    },
    "hi": {
        "title": "❓ किसान सहायता केंद्र और उपयोग गाइड",
        "subtitle": "एग्रीसेंस AI ऐप की सभी सुविधाओं को आसानी से उपयोग करने की चरणबद्ध मार्गदर्शिका",
        "voice_title": "🔊 ऐप उपयोग करने का ऑडियो सुनें (45 सेकंड)",
        "voice_sub": "स्पष्ट हिंदी आवाज में — ऐप का उपयोग कैसे करें जानने के लिए दबाएं",
        "btn_play": "🔊 ऑडियो गाइड सुनें (Play)",
        "btn_stop": "⏹ रोकें",
        "speech_lang": "hi-IN",
        "steps_header": "🚜 7 चरणों में संपूर्ण कृषि मार्गदर्शन",
        "faq_header": "❓ किसानों के महत्वपूर्ण प्रश्न और समाधान",
        "steps": [
            {
                "num": "1",
                "icon": "🌐",
                "title": "भाषा चुनें और लॉगिन करें",
                "desc": "स्क्रीन के शीर्ष पर अपनी भाषा चुनें। अपना नाम और 10 अंकों का मोबाइल नंबर दर्ज करके व्यक्तिगत डैशबोर्ड खोलें।",
                "action_btn": "डैशबोर्ड पर जाएं",
                "target": "home"
            },
            {
                "num": "2",
                "icon": "📡",
                "title": "खेत का डेटा दर्ज करें या ESP32 सेंसर जोड़ें",
                "desc": "'मेरे खेत का डेटा' में जाकर अपनी मिट्टी का N-P-K, pH और नमी दर्ज करें या ESP32 7-इन-1 सेंसर से ऑटो-सिंक करें।",
                "action_btn": "खेत का डेटा खोलें",
                "target": "farm"
            },
            {
                "num": "3",
                "icon": "🌾",
                "title": "AI फसल सिफारिश प्राप्त करें",
                "desc": "'सर्वोत्तम फसल खोजें' पर क्लिक करें। मशीन लर्निंग आपकी मिट्टी के अनुसार सबसे अधिक उपज देने वाली फसल सुझाएगी।",
                "action_btn": "फसल सिफारिश देखें",
                "target": "crop"
            },
            {
                "num": "4",
                "icon": "💧",
                "title": "स्मार्ट सिंचाई और मोटर समय जांचें",
                "desc": "'स्मार्ट सिंचाई' में नमी देखें। लाल संकेत पर आज ही पानी दें। कैलकुलेटर से पानी की कुल मात्रा और मोटर चलाने का समय जानें।",
                "action_btn": "सिंचाई सलाहकार खोलें",
                "target": "water"
            },
            {
                "num": "5",
                "icon": "🌿",
                "title": "4-चरणीय खाद योजना का पालन करें",
                "desc": "'खाद सलाह' में जाकर मिट्टी की पोषक कमी देखें और बुवाई, बढ़वार, फूल व दाना भराव अवस्था की सही खाद मात्रा जानें।",
                "action_btn": "खाद सलाह खोलें",
                "target": "fertilizer"
            },
            {
                "num": "6",
                "icon": "🦠",
                "title": "पत्तियों के रोग पहचानें (फसल डॉक्टर)",
                "desc": "पत्तियों पर रोग दिखने पर 'फसल रोग डॉक्टर' में फोटो खींचकर अपलोड करें। AI जैविक और रासायनिक उपचार बताएगा।",
                "action_btn": "रोग डॉक्टर खोलें",
                "target": "disease"
            },
            {
                "num": "7",
                "icon": "🤖🎙️",
                "title": "AI से बोलकर पूछें या लाइव कॉल करें",
                "desc": "'एग्रीसेंस AI चैट और वॉइस' खोलें और माइक दबाकर हिंदी में कोई भी कृषि सवाल पूछें और आवाज में उत्तर सुनें।",
                "action_btn": "वॉइस AI खोलें",
                "target": "voice"
            }
        ]
    },
    "ta": {
        "title": "❓ உதவி மையம் & வழிகாட்டி",
        "subtitle": "அக்ரிசென்ஸ் AI செயலியை எளிதாகப் பயன்படுத்தும் வழிகாட்டி",
        "voice_title": "🔊 குரல் வழியே வழிகாட்டுதலைக் கேளுங்கள்",
        "voice_sub": "தெளிவான தமிழ் குரலில் — செயலியை எவ்வாறு இயக்குவது என்பதை அறிய அழுத்தவும்",
        "btn_play": "🔊 வழிகாட்டலைக் கேளுங்கள்",
        "btn_stop": "⏹ நிறுத்து",
        "speech_lang": "ta-IN",
        "steps_header": "🚜 7-படி முழுமையான விவசாய வழிகாட்டுதல்",
        "faq_header": "❓ பொதுவான சந்தேகங்கள்",
        "steps": [
            { "num": "1", "icon": "🌐", "title": "மொழி தேர்வு & உள்நுழைவு", "desc": "உங்கள் மொழியைத் தேர்ந்தெடுத்து பெயர் மற்றும் தொலைபேசி எண்ணை உள்ளிடவும்.", "action_btn": "முகப்பு", "target": "home" },
            { "num": "2", "icon": "📡", "title": "மண் தகவல் பதிவு செய்தல்", "desc": "மண் NPK, pH மற்றும் ஈரப்பதத்தை பதிவு செய்யவும் அல்லது சென்சாரை இணைக்கவும்.", "action_btn": "பண்ணை தகவல்", "target": "farm" },
            { "num": "3", "icon": "🌾", "title": "AI பயிர் பரிந்துரை", "desc": "உங்கள் நிலத்திற்கு அதிக மகசூல் தரும் சிறந்த பயிரை AI கண்டறியும்.", "action_btn": "பயிர் பரிந்துரை", "target": "crop" },
            { "num": "4", "icon": "💧", "title": "ஸ்மார்ட் பாசன முறை", "desc": "மண் ஈரப்பதத்தை அறிந்து நீர் பாய்ச்சும் நேரம் மற்றும் அளவைக் கணக்கிடவும்.", "action_btn": "பாசன ஆலோசகர்", "target": "water" },
            { "num": "5", "icon": "🌿", "title": "உர மேலாண்மை திட்டம்", "desc": "4-நிலை உர அட்டவணையைப் பின்பற்றி சரியான உர அளவை இடவும்.", "action_btn": "உர வழிகாட்டி", "target": "fertilizer" },
            { "num": "6", "icon": "🦠", "title": "பயிர் நோய் மருத்துவர்", "desc": "பாதிக்கப்பட்ட இலை புகைப்படத்தை பதிவேற்றி உடனடி தீர்வு பெறவும்.", "action_btn": "நோய் மருத்துவர்", "target": "disease" },
            { "num": "7", "icon": "🤖🎙️", "title": "குரல் வழி AI உதவியாளர்", "desc": "குரல் வழியே உங்கள் விவசாயக் கேள்விகளைக் கேட்டு தெளிவு பெறவும்.", "action_btn": "குரல் உதவியாளர்", "target": "voice" }
        ]
    },
    "kn": {
        "title": "❓ ರೈತ ಸಹಾಯ ಕೇಂದ್ರ & ಮಾರ್ಗದರ್ಶಿ",
        "subtitle": "ಅಗ್ರಿಸೆನ್ಸ್ AI ಆ್ಯಪ್ ಅನ್ನು ಸುಲಭವಾಗಿ ಬಳಸುವ ಹಂತ-ಹಂತದ ಮಾರ್ಗದರ್ಶಿ",
        "voice_title": "🔊 ಆ್ಯಪ್ ಬಳಕೆಯ ಆಡಿಯೋ ಮಾರ್ಗದರ್ಶಿ ಆಲಿಸಿ",
        "voice_sub": "ಕನ್ನಡ ಧ್ವನಿಯಲ್ಲಿ — ಆ್ಯಪ್ ಹೇಗೆ ಬಳಸಬೇಕೆಂದು ತಿಳಿಯಲು ಒತ್ತಿ",
        "btn_play": "🔊 ಧ್ವನಿ ಆಲಿಸಿ",
        "btn_stop": "⏹ ನಿಲ್ಲಿಸಿ",
        "speech_lang": "kn-IN",
        "steps_header": "🚜 7 ಹಂತಗಳಲ್ಲಿ ಸಂಪೂರ್ಣ ಕೃಷಿ ಮಾರ್ಗದರ್ಶನ",
        "faq_header": "❓ ರೈತರ ಪ್ರಶ್ನೋತ್ತರಗಳು",
        "steps": [
            { "num": "1", "icon": "🌐", "title": "ಭಾಷೆ ಆಯ್ಕೆ ಮತ್ತು ಲಾಗಿನ್", "desc": "ಕನ್ನಡ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ ನಿಮ್ಮ ಹೆಸರು ಮತ್ತು ಮೊಬೈಲ್ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ.", "action_btn": "ಮುಖಪುಟ", "target": "home" },
            { "num": "2", "icon": "📡", "title": "ಮಣ್ಣಿನ ಮಾಹಿತಿ ನಮೂದಿಸಿ", "desc": "ಮಣ್ಣಿನ NPK, pH ಮತ್ತು ತೇವಾಂಶವನ್ನು ದಾಖಲಿಸಿ ಅಥವಾ ಸೆನ್ಸರ್ ಬಳಸಿ.", "action_btn": "ಹೊಲದ ಮಾಹಿತಿ", "target": "farm" },
            { "num": "3", "icon": "🌾", "title": "AI ಬೆಳೆ ಶಿಫಾರಸು ಪಡೆಯಿರಿ", "desc": "ನಿಮ್ಮ ಜಮೀನಿಗೆ ಗರಿಷ್ಠ ಇಳುವರಿ ನೀಡುವ ಉತ್ತಮ ಬೆಳೆಯನ್ನು ತಿಳಿಯಿರಿ.", "action_btn": "ಬೆಳೆ ಶಿಫಾರಸು", "target": "crop" },
            { "num": "4", "icon": "💧", "title": "ಸ್ಮಾರ್ಟ್ ನೀರಾವರಿ ಸಲಹೆ", "desc": "ಮಣ್ಣಿನ ತೇವಾಂಶ ಮತ್ತು ಪಂಪ್ ಚಲಾಯಿಸುವ ಸಮಯವನ್ನು ಲೆಕ್ಕಹಾಕಿ.", "action_btn": "ನೀರಾವರಿ ಸಲಹೆ", "target": "water" },
            { "num": "5", "icon": "🌿", "title": "ರಸಗೊಬ್ಬರ ನಿರ್ವಹಣೆ", "desc": "4-ಹಂತದ ರಸಗೊಬ್ಬರ ವೇಳಾಪಟ್ಟಿ ಮತ್ತು ಅಗತ್ಯ ಚೀಲಗಳ ಲೆಕ್ಕ ಪಡೆಯಿರಿ.", "action_btn": "ರಸಗೊಬ್ಬರ ಸಲಹೆ", "target": "fertilizer" },
            { "num": "6", "icon": "🦠", "title": "ಬೆಳೆ ರೋಗ ವೈದ್ಯ", "desc": "ಎಲೆಯ ಫೋಟೋ ತೆಗೆದು ಅಪ್ಲೋಡ್ ಮಾಡಿ ರೋಗ ಪರಿಹಾರ ತಿಳಿಯಿರಿ.", "action_btn": "ರೋಗ ವೈದ್ಯ", "target": "disease" },
            { "num": "7", "icon": "🤖🎙️", "title": "ವಾಯ್ಸ್ AI ಮೂಲಕ ಮಾತನಾಡಿ", "desc": "ಕನ್ನಡದಲ್ಲೇ ಮಾತನಾಡಿ ಕೃಷಿ ಸಂದೇಹಗಳಿಗೆ ತಕ್ಷಣ ಧ್ವನಿ ಉತ್ತರ ಪಡೆಯಿರಿ.", "action_btn": "ವಾಯ್ಸ್ AI", "target": "voice" }
        ]
    },
    "mr": {
        "title": "❓ शेतकरी मदत केंद्र व वापर मार्गदर्शक",
        "subtitle": "ॲग्रीसेन्स AI ॲप सहज वापरण्यासाठी टप्प्याटप्प्याने मार्गदर्शक",
        "voice_title": "🔊 ॲप वापरण्याचा ऑडिओ सल्ला ऐका",
        "voice_sub": "मराठी ऑडिओमध्ये — ॲप कसे वापरावे हे ऐकण्यासाठी दाबा",
        "btn_play": "🔊 ऑडिओ ऐका",
        "btn_stop": "⏹ थांबवा",
        "speech_lang": "mr-IN",
        "steps_header": "🚜 7 टप्प्यांमध्ये संपूर्ण कृषी मार्गदर्शन",
        "faq_header": "❓ शेतकऱ्यांचे प्रश्न व उत्तरे",
        "steps": [
            { "num": "1", "icon": "🌐", "title": "भाषा निवडा व लॉगिन करा", "desc": "मराठी भाषा निवडून नाव आणि मोबाईल नंबर टाकून डॅशबोर्ड उघडा.", "action_btn": "मुख्य डॅशबोर्ड", "target": "home" },
            { "num": "2", "icon": "📡", "title": "शेताचा डेटा भरा", "desc": "मातीतील NPK, pH आणि ओलावा प्रविष्ट करा किंवा सेन्सर जोडा.", "action_btn": "शेताचा डेटा", "target": "farm" },
            { "num": "3", "icon": "🌾", "title": "AI पीक शिफारस मिळवा", "desc": "तुमच्या शेतासाठी सर्वाधिक उत्पादन देणारे पीक शोधा.", "action_btn": "पीक शिफारस", "target": "crop" },
            { "num": "4", "icon": "💧", "title": "स्मार्ट सिंचन सल्ला", "desc": "मातीतील ओलावा तपासा व मोटर चालवण्याची वेळ जाणून घ्या.", "action_btn": "सिंचन सल्ला", "target": "water" },
            { "num": "5", "icon": "🌿", "title": "4-टप्प्यांचे खत नियोजन", "desc": "पेरणी ते दाना भरण्यापर्यंत खतांचे अचूक नियोजन करा.", "action_btn": "खत सल्ला", "target": "fertilizer" },
            { "num": "6", "icon": "🦠", "title": "पीक रोग डॉक्टर", "desc": "पानांचा फोटो काढून त्वरित रोग निदान व उपाय मिळवा.", "action_btn": "रोग डॉक्टर", "target": "disease" },
            { "num": "7", "icon": "🤖🎙️", "title": "AI व्हॉईस सहाय्यक", "desc": "मराठीत बोलून शेतीविषयक कोणत्याही प्रश्नाचे त्वरित उत्तर मिळवा.", "action_btn": "व्हॉईस AI", "target": "voice" }
        ]
    }
}


# =========================================================
# MAIN HELP CENTER VIEW
# =========================================================

def show_help_center():
    farmer = st.session_state.get("farmer", {})
    farmer_name = farmer.get("name", "Farmer")
    lang_code = st.session_state.get("language_code", "en")
    ui = HELP_TEXT.get(lang_code, HELP_TEXT["en"])

    st.title(ui["title"])
    st.caption(f"👨‍🌾 {farmer_name} • 🌐 {ui['subtitle']}")
    st.markdown("---")

    # =====================================================
    # 🔊 MULTILINGUAL AUDIO WALKTHROUGH COMPONENT
    # =====================================================
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #14532d 0%, #166534 100%); border-radius: 18px; padding: 20px 24px; color: white; margin-bottom: 20px; box-shadow: 0 8px 24px rgba(20, 83, 45, 0.35);">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                <div>
                    <span style="background: rgba(255,255,255,0.2); color: #ffffff; padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 700; border: 1px solid rgba(255,255,255,0.3);">
                        📢 Voice User Guide
                    </span>
                    <h2 style="color: #ffffff !important; font-size: 22px !important; font-weight: 800; margin: 8px 0 4px 0;">
                        {ui['voice_title']}
                    </h2>
                    <p style="color: #dcfce7; font-size: 13px; margin: 0; font-weight: 600;">
                        {ui['voice_sub']}
                    </p>
                </div>
                <div style="font-size: 38px;">🎧</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Voice script generation
    voice_walkthroughs = {
        "en": f"Welcome to AgriSense AI {farmer_name}! Here is how to use the app in seven simple steps: Step 1, select your language. Step 2, enter your soil readings in My Farm Data. Step 3, tap Find Best Crop for machine learning recommendations. Step 4, check Smart Irrigation for moisture and pump timing. Step 5, follow the four-stage fertilizer schedule. Step 6, take a photo of unhealthy leaves in Plant Disease Doctor for instant remedies. Step 7, speak to AgriSense AI in your native language by voice!",
        "te": f"అగ్రిసెన్స్ AI కి స్వాగతం {farmer_name} గారు! యాప్‌ను ఉపయోగించే 7 సులభమైన దశలు: దశ 1, మీ భాషను ఎంచుకోండి. దశ 2, నా పొలం డేటాలో మీ నేల వివరాలు నమోదు చేయండి. దశ 3, మంచి పంట సిఫార్సును పొందండి. దశ 4, స్మార్ట్ నీటిపారుదలలో నేల తేమ మరియు మోటార్ సమయం తనిఖీ చేయండి. దశ 5, 4 దశల ఎరువుల ప్రణాళికను పాటించండి. దశ 6, పంట ఆకు ఫోటో తీసి తెగుళ్ల డాక్టర్‌లో మందులు తెలుసుకోండి. దశ 7, వాయిస్ అసిస్టెంట్ ద్వారా తెలుగులోనే మాట్లాడి సందేహాలు నివృత్తి చేసుకోండి!",
        "hi": f"एग्रीसेंस AI में आपका स्वागत है {farmer_name} जी! ऐप का उपयोग करने के 7 आसान चरण: चरण 1, अपनी भाषा चुनें। चरण 2, खेत का डेटा दर्ज करें। चरण 3, AI फसल सिफारिश प्राप्त करें। चरण 4, स्मार्ट सिंचाई में पानी और मोटर का समय देखें। चरण 5, 4-चरणीय खाद योजना अपनाएं। चरण 6, फसल रोग डॉक्टर में पत्ती का फोटो खींचकर उपचार जानें। चरण 7, वॉइस सहायक से हिंदी में बोलकर सवाल पूछें!",
        "ta": f"அக்ரிசென்ஸ் AI-க்கு நல்வரவு {farmer_name}! செயலியைப் பயன்படுத்த 7 எளிய படிகள்: மொழி தேர்வு, மண் தகவல் பதிவு, பயிர் பரிந்துரை, பாசன ஆலோசனை, உர மேலாண்மை, நோய் மருத்துவர் மற்றும் குரல் வழி உதவியாளர்!",
        "kn": f"ಅಗ್ರಿಸೆನ್ಸ್ AI ಗೆ ಸುಸ್ವಾಗತ {farmer_name}! ಆ್ಯಪ್ ಬಳಸಲು 7 ಹಂತಗಳು: ಭಾಷೆ ಆಯ್ಕೆ, ಮಣ್ಣಿನ ಮಾಹಿತಿ, ಬೆಳೆ ಶಿಫಾರಸು, ನೀರಾವರಿ ಸಲಹೆ, ರಸಗೊಬ್ಬರ ಯೋಜನೆ, ಬೆಳೆ ರೋಗ ವೈದ್ಯ ಮತ್ತು ವಾಯ್ಸ್ AI ಸಹಾಯ!",
        "mr": f"ॲग्रीसेन्स AI मध्ये आपले स्वागत आहे {farmer_name}! ॲप वापरण्याचे 7 सोपे टप्पे: भाषा निवड, शेताचा डेटा, पीक शिफारस, सिंचन सल्ला, खत व्यवस्थापन, रोग डॉक्टर आणि व्हॉईस AI सहाय्यक!"
    }

    current_script = voice_walkthroughs.get(lang_code, voice_walkthroughs["en"])
    script_json = json.dumps(current_script)
    speech_lang_code = ui["speech_lang"]

    components.html(
        f"""
        <div style="display: flex; gap: 10px; margin-bottom: 16px;">
            <button id="playHelpVoice" onclick="playVoice()" style="
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
            <button id="stopHelpVoice" onclick="stopVoice()" style="
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

                const btn = document.getElementById('playHelpVoice');
                btn.style.background = '#059669';
                utterance.onend = function() {{
                    btn.style.background = 'linear-gradient(135deg, #16a34a 0%, #15803d 100%)';
                }};
                window.speechSynthesis.speak(utterance);
            }}

            function stopVoice() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    const btn = document.getElementById('playHelpVoice');
                    btn.style.background = 'linear-gradient(135deg, #16a34a 0%, #15803d 100%)';
                }}
            }}
        </script>
        """,
        height=62
    )

    # =====================================================
    # 🚜 7-STEP INTERACTIVE WORKFLOW CARDS
    # =====================================================
    st.subheader(ui["steps_header"])

    steps = ui["steps"]
    for item in steps:
        with st.container(border=True):
            col_icon, col_content, col_btn = st.columns([1, 6, 3])
            with col_icon:
                st.markdown(
                    f"""
                    <div style="width: 48px; height: 48px; border-radius: 14px; background: #dcfce7; color: #166534; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: 800;">
                        {item['icon']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with col_content:
                st.markdown(f"<div style='font-weight: 800; font-size: 16px; color: #0f172a;'>Step {item['num']}: {item['title']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size: 13px; color: #475569; margin-top: 4px; line-height: 1.5;'>{item['desc']}</div>", unsafe_allow_html=True)
            with col_btn:
                st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
                if st.button(f"👉 {item['action_btn']}", key=f"btn_step_{item['num']}", use_container_width=True):
                    st.session_state.page = item["target"]
                    st.rerun()

    st.markdown("---")

    # =====================================================
    # ❓ COMMON FARMER QUESTIONS & TROUBLESHOOTING
    # =====================================================
    st.subheader(ui["faq_header"])

    with st.expander("❓ What should I do if I don't know my exact soil NPK values?", expanded=False):
        st.markdown(
            """
            * **Use Standard Regional Defaults:** In 'My Farm Data', default balanced values (e.g. N: 80, P: 40, K: 40, pH: 7.0) are already pre-filled.
            * **Connect 7-in-1 Soil Sensor:** If you plug in the ESP32 soil probe, it will automatically measure real-time Nitrogen, Phosphorus, Potassium, and pH in 1 second.
            """
        )

    with st.expander("❓ How does the Smart Irrigation Advisor tell me if I should water today?", expanded=False):
        st.markdown(
            """
            * The app reads the soil moisture percentage from your IoT probe or manual entry.
            * **Red (&lt;25%):** Urgent watering needed today.
            * **Yellow (25-40%):** Water within 24 to 48 hours.
            * **Green (40-75%):** Soil is healthy and moist — No watering needed.
            * **Blue (&gt;75%):** Soil is saturated — Pause watering to prevent root rot.
            """
        )

    with st.expander("❓ How does the Plant Disease Doctor work from a photo?", expanded=False):
        st.markdown(
            """
            * Take a clear photo of the infected leaf in daylight.
            * The Gemini Vision AI scans the visible lesions, discoloration, and spots.
            * It identifies the exact fungus, bacteria, or pest and provides both **organic home remedies (Neem oil, buttermilk spray)** and **chemical fungicide dosages per liter**.
            """
        )

    with st.expander("❓ Can I talk to the app in my own regional language?", expanded=False):
        st.markdown(
            """
            * **Yes!** Switch your language at the top to Telugu, Hindi, Tamil, Kannada, or Marathi.
            * Open 'AgriSense AI Chat & Voice' or 'Live Call', press the microphone button, and speak naturally. The AI will respond with voice audio in your language.
            """
        )
