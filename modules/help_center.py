import os
import json
import streamlit as st
import streamlit.components.v1 as components

# =========================================================
# MULTILINGUAL STEP-BY-STEP USER GUIDE & VOICE SCRIPTS
# =========================================================

HELP_TEXT = {
    "en": {
        "title": "❓ Farmer Help Center & Step-by-Step Visual Guide",
        "subtitle": "Ultra-simple, icon-driven, voice-assisted guide designed for all farmers",
        "voice_title": "🔊 Listen to Complete Audio Guide (45s)",
        "voice_sub": "Clear spoken walkthrough — Tap Play to hear how to use the app",
        "btn_play": "🔊 Play All Guide",
        "btn_stop": "⏹ Stop Voice",
        "speech_lang": "en-IN",
        "color_guide_title": "🎨 Color & Symbol Meaning Guide (Traffic Lights)",
        "color_guide_sub": "Look at colors and icons on any screen to understand your farm's status instantly:",
        "steps_header": "🚜 7-Step Simple Farming Workflow (Tap 🔊 to Listen to Each Step)",
        "dos_donts_header": "✅ What to Do & ❌ What to Avoid (Farming Best Practices)",
        "emergency_header": "📞 Emergency Toll-Free Farmer Helpline & Instant AI Voice",
        "emergency_sub": "Call the Government Kisan Helpline for free or talk to AgriSense AI:",
        "kisan_call_btn": "📞 Call 1551 (Kisan Helpline)",
        "open_voice_btn": "🎙️ Speak to AgriSense AI",
        "download_ppt_btn": "📥 Download Farmer Guide Slide Presentation (PDF)",
        "steps": [
            {
                "num": "1",
                "icon": "🌐",
                "title": "Select Language & Login",
                "desc": "Choose your mother tongue (Telugu, Hindi, Tamil, Kannada, Marathi, English) at the top. Enter your name and 10-digit mobile number to open your farm dashboard.",
                "voice_text": "Step 1: Choose your language at the top right corner. Enter your name and mobile number, then tap Enter Dashboard.",
                "action_btn": "Go to Login / Profile",
                "target": "home"
            },
            {
                "num": "2",
                "icon": "📡",
                "title": "Enter Soil Data or Connect ESP32 Sensor",
                "desc": "Open 'My Farm Data'. Standard soil readings are pre-filled. Adjust Nitrogen, Phosphorus, Potash, pH, and Moisture, or plug in your 7-in-1 sensor to sync live.",
                "voice_text": "Step 2: In My Farm Data, default soil values are pre-filled. You can save your soil test values or connect the ESP32 probe to read live values.",
                "action_btn": "Open Farm Data",
                "target": "farm"
            },
            {
                "num": "3",
                "icon": "🌾",
                "title": "Get AI Crop Recommendation",
                "desc": "Tap 'Find Best Crop'. The AI analyzes your soil and weather to recommend the highest-yielding crop with top alternatives and confidence percentages.",
                "voice_text": "Step 3: In AI Crop Recommendation, tap Find Best Crop to see the most profitable crop suited for your soil and season.",
                "action_btn": "Open Crop Recommendation",
                "target": "crop"
            },
            {
                "num": "4",
                "icon": "💧",
                "title": "Check Smart Irrigation & Motor Time",
                "desc": "Open 'Smart Irrigation'. Check the moisture meter: Red means water today, Green means soil is moist. Use the calculator to see exact pumping hours.",
                "voice_text": "Step 4: In Smart Irrigation, Red means urgent watering needed today. Green means safe. Check the calculator for exact motor hours.",
                "action_btn": "Open Irrigation Advisor",
                "target": "water"
            },
            {
                "num": "5",
                "icon": "🌿",
                "title": "Follow 4-Stage Fertilizer Schedule",
                "desc": "Open 'Fertilizer Guidance'. View soil NPK deficits and follow the 4-stage split dose table (Sowing, Tillering, Flowering, Grain filling) to save fertilizer cost.",
                "voice_text": "Step 5: In Fertilizer Guidance, check how many bags of Urea, DAP, and Potash are needed across 4 crop growth stages.",
                "action_btn": "Open Fertilizer Advisor",
                "target": "fertilizer"
            },
            {
                "num": "6",
                "icon": "🦠",
                "title": "Diagnose Plant Diseases (Leaf Doctor)",
                "desc": "If crop leaves have spots or yellowing, take a clear photo in daylight. The AI leaf doctor identifies the disease and gives organic and chemical remedies.",
                "voice_text": "Step 6: In Plant Disease Doctor, take a daylight photo of the sick leaf. The AI will instantly tell you the disease name and medicine dosage.",
                "action_btn": "Open Disease Doctor",
                "target": "disease"
            },
            {
                "num": "7",
                "icon": "🤖🎙️",
                "title": "Speak to AgriSense AI by Voice or Call",
                "desc": "Tap the microphone button and speak in your language. Ask about weather, seeds, mandi rates, or crop pests to get instant spoken advice.",
                "voice_text": "Step 7: In AgriSense AI Chat and Voice, press the green microphone and speak naturally in your mother tongue for instant spoken advice.",
                "action_btn": "Open Voice AI Assistant",
                "target": "voice"
            }
        ],
        "colors": [
            {"color": "#ef4444", "bg": "#fef2f2", "border": "#fca5a5", "icon": "🔴", "name": "RED (Urgent Action)", "desc": "Soil is Dry / Water Immediately / Disease Detected / High Nutrient Deficit"},
            {"color": "#eab308", "bg": "#fefce8", "border": "#fde047", "icon": "🟡", "name": "YELLOW (Warning / Watch)", "desc": "Soil moisture dropping / Water within 2 days / Moderate nutrient level"},
            {"color": "#22c55e", "bg": "#f0fdf4", "border": "#86efac", "icon": "🟢", "name": "GREEN (Safe / Healthy)", "desc": "Soil is Moist & Optimal / Crop is Healthy / No immediate action needed"},
            {"color": "#0284c7", "bg": "#f0f9ff", "border": "#7dd3fc", "icon": "💧", "name": "BLUE WATER DROP", "desc": "Shows water liters needed and exact motor pumping runtime in hours"},
            {"color": "#16a34a", "bg": "#f0fdf4", "border": "#86efac", "icon": "🌿", "name": "GREEN LEAF & BAG", "desc": "Shows exact fertilizer bags (Urea, DAP, Potash) for your farm acreage"},
            {"color": "#7c3aed", "bg": "#faf5ff", "border": "#d8b4fe", "icon": "🎤", "name": "PURPLE MICROPHONE", "desc": "Tap and speak your question in your regional language with zero typing"}
        ],
        "dos_donts": [
            {
                "topic": "💧 Irrigation Timing",
                "do_text": "Irrigate in early morning (6-9 AM) or evening (5-7 PM) when sun is gentle.",
                "dont_text": "Do NOT irrigate in hot noon sun (causes 30% solar evaporation loss)."
            },
            {
                "topic": "🌿 Fertilizer Application",
                "do_text": "Split Urea into 3 doses across vegetative and flowering stages.",
                "dont_text": "Do NOT dump all Urea at sowing time (causes nitrogen burning and soil leaching)."
            },
            {
                "topic": "🦠 Leaf Photo Diagnosis",
                "do_text": "Take close-up photos of leaves in clear daylight with visible spots.",
                "dont_text": "Do NOT take dark, blurry, or far-away photos of the entire plant."
            },
            {
                "topic": "📡 Soil Sensor Placement",
                "do_text": "Insert the ESP32 probe 10 cm deep into root-zone moist soil.",
                "dont_text": "Do NOT leave sensor probe loosely lying on dry surface dust."
            }
        ]
    },
    "te": {
        "title": "❓ రైతు సహాయ కేంద్రం & చిత్రాల గైడ్",
        "subtitle": "చదువురాని రైతులకు కూడా సులభంగా అర్థమయ్యేలా చిహ్నాలు, రంగులు మరియు వాయిస్ గైడ్",
        "voice_title": "🔊 పూర్తి గైడ్ వాయిస్ వినండి (45 సెకన్లు)",
        "voice_sub": "స్పష్టమైన తెలుగు వాయిస్‌లో — యాప్ ఎలా వాడాలో వినడానికి నొక్కండి",
        "btn_play": "🔊 మొత్తం గైడ్ వినండి",
        "btn_stop": "⏹ ఆపండి",
        "speech_lang": "te-IN",
        "color_guide_title": "🎨 రంగులు & చిహ్నాల అర్థం (ట్రాఫిక్ లైట్స్ పద్ధతి)",
        "color_guide_sub": "యాప్‌లో కనిపించే రంగులను బట్టి మీ పొలం పరిస్థితిని సులభంగా గుర్తించండి:",
        "steps_header": "🚜 7 దశల్లో వ్యవసాయం (ప్రతి దశ వద్ద 🔊 నొక్కి వినండి)",
        "dos_donts_header": "✅ చేయాల్సిన మంచి పనులు & ❌ చేయకూడని పనులు",
        "emergency_header": "📞 ఉచిత ప్రభుత్వ కిసాన్ హెల్ప్‌లైన్ & వాయిస్ AI",
        "emergency_sub": "సందేహాలు ఉంటే ఉచిత కిసాన్ నంబర్‌కు కాల్ చేయండి లేదా AI తో మాట్లాడండి:",
        "kisan_call_btn": "📞 1551 కిసాన్ కాల్ సెంటర్ (ఉచితం)",
        "open_voice_btn": "🎙️ AI తో మాట్లాడండి",
        "download_ppt_btn": "📥 రైతు గైడ్ స్లైడ్ ప్రెజెంటేషన్ డౌన్‌లోడ్ (PDF)",
        "steps": [
            {
                "num": "1",
                "icon": "🌐",
                "title": "భాషను ఎంచుకోండి & లాగిన్ అవ్వండి",
                "desc": "స్క్రీన్ పైభాగంలో 'తెలుగు' ఎంచుకోండి. మీ పేరు మరియు 10 అంకెల మొబైల్ నంబర్ నమోదు చేసి డ్యాష్‌బోర్డ్ తెరవండి.",
                "voice_text": "మొదటి దశ: పైన కుడివైపున తెలుగు భాషను ఎంచుకోండి. మీ పేరు, ఫోన్ నంబర్ నమోదు చేసి డ్యాష్‌బోర్డ్‌లోకి వెళ్లండి.",
                "action_btn": "ప్రొఫైల్ / లాగిన్",
                "target": "home"
            },
            {
                "num": "2",
                "icon": "📡",
                "title": "పొలం వివరాలు నమోదు చేయండి లేదా సెన్సార్ కలపండి",
                "desc": "'నా పొలం డేటా' లో మీ నేల నత్రజని, భాస్వరం, పొటాష్, pH నమోదు చేయండి లేదా సెన్సార్ జోడించండి.",
                "voice_text": "రెండవ దశ: నా పొలం డేటాలో మీ నేల పోషకాలు మరియు తేమను నమోదు చేయండి లేదా సెన్సార్ ద్వారా రీడింగ్ పొందండి.",
                "action_btn": "పొలం డేటా తెరవండి",
                "target": "farm"
            },
            {
                "num": "3",
                "icon": "🌾",
                "title": "AI మంచి పంట సిఫార్సు పొందండి",
                "desc": "'మంచి పంటను తెలుసుకోండి' నొక్కండి. మీ నేలకు అత్యధిక దిగుబడి మరియు లాభం ఇచ్చే పంటను AI చెబుతుంది.",
                "voice_text": "మూడవ దశ: పంట సిఫార్సు పేజీలో మీ నేలకు ఏ పంట బాగా పండుతుందో తెలుసుకోండి.",
                "action_btn": "పంట సిఫార్సు చూడండి",
                "target": "crop"
            },
            {
                "num": "4",
                "icon": "💧",
                "title": "స్మార్ట్ నీటిపారుదల & మోటార్ సమయం",
                "desc": "ఎరుపు రంగు వస్తే వెంటనే నీరు పెట్టండి. పచ్చ రంగు వస్తే నేల బాగుంది. ఎన్ని గంటలు మోటార్ వేయాలో లెక్క చూసుకోండి.",
                "voice_text": "నాల్గవ దశ: నీటిపారుదల పేజీలో ఎరుపు రంగు వస్తే ఈరోజే నీరు పెట్టండి. పచ్చ రంగు ఉంటే నీరు అవసరం లేదు.",
                "action_btn": "నీటిపారుదల తెరవండి",
                "target": "water"
            },
            {
                "num": "5",
                "icon": "🌿",
                "title": "4 దశల ఎరువుల ప్రణాళికను పాటించండి",
                "desc": "యూరియా, డీఏపీ, పొటాష్ బస్తాల లెక్కను విత్తే సమయం, పెరుగుదల, పూత మరియు గింజ బలం దశల్లో వేయండి.",
                "voice_text": "ఐదవ దశ: ఎరువుల సలహాదారులో విత్తే సమయం నుంచి కోత వరకు ఎన్ని బస్తాల ఎరువులు వేయాలో తెలుసుకోండి.",
                "action_btn": "ఎరువుల సలహా చూడండి",
                "target": "fertilizer"
            },
            {
                "num": "6",
                "icon": "🦠",
                "title": "ఆకు తెగుళ్లు గుర్తించండి (లీఫ్ డాక్టర్)",
                "desc": "ఆకుపై మచ్చలు ఉంటే మంచి వెలుతురులో ఫోటో తీయండి. AI వెంటనే వ్యాధి పేరు మరియు మందుల మోతాదు చెబుతుంది.",
                "voice_text": "ఆరవ దశ: తెగుళ్ల డాక్టర్‌లో వ్యాధి సోకిన ఆకు ఫోటో తీసి అప్‌లోడ్ చేస్తే తగిన మందులను AI సూచిస్తుంది.",
                "action_btn": "తెగుళ్ల డాక్టర్ తెరవండి",
                "target": "disease"
            },
            {
                "num": "7",
                "icon": "🤖🎙️",
                "title": "వాయిస్ ద్వారా మాట్లాడండి లేదా కాల్ చేయండి",
                "desc": "ఆకుపచ్చ మైక్ బటన్ నొక్కి తెలుగులోనే మాట్లాడండి. వాతావరణం, విత్తనాలు, మార్కెట్ ధరల గురించి సమాధానం వినండి.",
                "voice_text": "ఏడవ దశ: వాయిస్ అసిస్టెంట్‌లో మైక్ నొక్కి తెలుగులోనే మాట్లాడి ఏ సందేహమైనా అడగండి.",
                "action_btn": "వాయిస్ AI తెరవండి",
                "target": "voice"
            }
        ],
        "colors": [
            {"color": "#ef4444", "bg": "#fef2f2", "border": "#fca5a5", "icon": "🔴", "name": "ఎరుపు రంగు (తక్షణ చర్య)", "desc": "నేలలో తేమ లేదు / వెంటనే నీరు పెట్టాలి / తెగులు వచ్చింది / పోషకాలు తక్కువగా ఉన్నాయి"},
            {"color": "#eab308", "bg": "#fefce8", "border": "#fde047", "icon": "🟡", "name": "పసుపు రంగు (హెచ్చరిక)", "desc": "తేమ తగ్గుతోంది / 2 రోజుల్లో నీరు పెట్టాలి / పోషకాలు మధ్యస్థంగా ఉన్నాయి"},
            {"color": "#22c55e", "bg": "#f0fdf4", "border": "#86efac", "icon": "🟢", "name": "ఆకుపచ్చ రంగు (సురక్షితం)", "desc": "నేలలో తగినంత తేమ ఉంది / పంట ఆరోగ్యంగా ఉంది / ప్రస్తుతానికి నీరు అవసరం లేదు"},
            {"color": "#0284c7", "bg": "#f0f9ff", "border": "#7dd3fc", "icon": "💧", "name": "నీలి రంగు నీటి చుక్క", "desc": "పొలానికి ఎన్ని లీటర్ల నీరు మరియు మోటార్ ఎన్ని గంటలు వేయాలో తెలుపుతుంది"},
            {"color": "#16a34a", "bg": "#f0fdf4", "border": "#86efac", "icon": "🌿", "name": "ఆకుపచ్చ ఆకు & బస్తా", "desc": "మీ ఎకరానికి ఎన్ని బస్తాల యూరియా, డీఏపీ, పొటాష్ వేయాలో చూపిస్తుంది"},
            {"color": "#7c3aed", "bg": "#faf5ff", "border": "#d8b4fe", "icon": "🎤", "name": "ఊదా రంగు మైక్రోఫోన్", "desc": "టైపింగ్ అవసరం లేకుండా నేరుగా నోటితో మాట్లాడి సమాధానం వినడానికి మైక్ నొక్కండి"}
        ],
        "dos_donts": [
            {
                "topic": "💧 నీరు పెట్టే సమయం",
                "do_text": "ఉదయం (6-9 గంటలు) లేదా సాయంత్రం (5-7 గంటలు) చల్లని వేళల్లో నీరు పెట్టండి.",
                "dont_text": "మధ్యాహ్నం ఎండ తీవ్రంగా ఉన్నప్పుడు నీరు పెట్టవద్దు (నీరు ఆవిరైపోతుంది)."
            },
            {
                "topic": "🌿 ఎరువులు వేసే విధానం",
                "do_text": "యూరియాను ఒకేసారి వేయకుండా 3 వాయిదాలుగా పైపాటుగా వేయండి.",
                "dont_text": "మొత్తం యూరియాను ఒకేసారి వేయవద్దు (మొక్కలు మాడిపోతాయి, నేల పాడవుతుంది)."
            },
            {
                "topic": "🦠 ఆకు ఫోటో తీసే విధానం",
                "do_text": "పగటి వెలుతురులో ఆకు దగ్గరగా స్పష్టంగా కనిపించేలా ఫోటో తీయండి.",
                "dont_text": "చీకటిలో లేదా దూరం నుంచి మసకగా ఉండే ఫోటోలు తీయవద్దు."
            },
            {
                "topic": "📡 సెన్సార్ ఉపయోగించే విధానం",
                "do_text": "సెన్సార్‌ను వేర్ల లోతులో 10 సెం.మీ లోపలికి దింపి రీడింగ్ తీసుకోండి.",
                "dont_text": "పైపై పొడి మట్టిలో సెన్సార్‌ను వదిలివేయవద్దు."
            }
        ]
    },
    "hi": {
        "title": "❓ किसान सहायता केंद्र और चित्र मार्गदर्शिका",
        "subtitle": "अनपढ़ और कम पढ़े-लिखे किसान भाइयों के लिए आसान रंग, प्रतीक और आवाज गाइड",
        "voice_title": "🔊 संपूर्ण ऑडियो गाइड सुनें (45 सेकंड)",
        "voice_sub": "स्पष्ट हिंदी आवाज में — ऐप चलाने का तरीका जानने के लिए दबाएं",
        "btn_play": "🔊 पूरा गाइड सुनें",
        "btn_stop": "⏹ रोकें",
        "speech_lang": "hi-IN",
        "color_guide_title": "🎨 रंग और प्रतीकों का मतलब (ट्रैफिक लाइट नियम)",
        "color_guide_sub": "स्क्रीन पर रंगों को देखकर अपने खेत की स्थिति तुरंत समझें:",
        "steps_header": "🚜 7 चरणों में खेती का तरीका (हर चरण पर 🔊 दबाकर सुनें)",
        "dos_donts_header": "✅ क्या करें और ❌ क्या न करें (उत्तम खेती नियम)",
        "emergency_header": "📞 फ्री किसान कॉल सेंटर 1551 और वॉइस AI",
        "emergency_sub": "कृषि सलाह के लिए टोल-फ्री कॉल करें या AI से बोलकर पूछें:",
        "kisan_call_btn": "📞 1551 किसान कॉल सेंटर (मुफ्त)",
        "open_voice_btn": "🎙️ AI से बोलकर पूछें",
        "download_ppt_btn": "📥 किसान गाइड प्रेजेंटेशन डाउनलोड (PDF)",
        "steps": [
            {
                "num": "1",
                "icon": "🌐",
                "title": "भाषा चुनें और लॉगिन करें",
                "desc": "स्क्रीन पर हिंदी चुनें। अपना नाम और 10 अंकों का मोबाइल नंबर डालकर डैशबोर्ड खोलें।",
                "voice_text": "पहला चरण: अपनी भाषा चुनें। नाम और फोन नंबर दर्ज करके डैशबोर्ड पर जाएं।",
                "action_btn": "डैशबोर्ड पर जाएं",
                "target": "home"
            },
            {
                "num": "2",
                "icon": "📡",
                "title": "खेत का डेटा भरें या सेंसर जोड़ें",
                "desc": "'मेरे खेत का डेटा' में मिट्टी के पोषक तत्व और नमी दर्ज करें या सेंसर से मापें।",
                "voice_text": "दूसरा चरण: मेरे खेत का डेटा में मिट्टी की जांच भरें या सेंसर से लाइव डेटा लें।",
                "action_btn": "खेत का डेटा खोलें",
                "target": "farm"
            },
            {
                "num": "3",
                "icon": "🌾",
                "title": "AI फसल सिफारिश प्राप्त करें",
                "desc": "'सर्वोत्तम फसल खोजें' दबाएं। AI आपके खेत के लिए सबसे ज्यादा पैदावार देने वाली फसल बताएगा।",
                "voice_text": "तीसरा चरण: फसल सिफारिश में अपनी मिट्टी के अनुसार सबसे अच्छी फसल चुनें।",
                "action_btn": "फसल सिफारिश देखें",
                "target": "crop"
            },
            {
                "num": "4",
                "icon": "💧",
                "title": "स्मार्ट सिंचाई और मोटर समय जांचें",
                "desc": "लाल रंग दिखे तो आज ही पानी दें। हरा रंग दिखे तो मिट्टी में नमी पर्याप्त है। मोटर समय देखें।",
                "voice_text": "चौथा चरण: सिंचाई पेज पर लाल रंग दिखे तो पानी दें, हरा दिखे तो पानी न दें।",
                "action_btn": "सिंचाई सलाहकार खोलें",
                "target": "water"
            },
            {
                "num": "5",
                "icon": "🌿",
                "title": "4-चरणीय खाद योजना अपनाएं",
                "desc": "बुवाई, बढ़वार, फूल और दाना भराव अवस्था पर यूरिया, डीएपी और पोटाश की सही बोरी डालें।",
                "voice_text": "पांचवां चरण: खाद सलाह में 4 चरणों में खाद डालने का सही समय और मात्रा जानें।",
                "action_btn": "खाद सलाह खोलें",
                "target": "fertilizer"
            },
            {
                "num": "6",
                "icon": "🦠",
                "title": "फसल रोग पहचानें (पत्ती डॉक्टर)",
                "desc": "बीमार पत्ती का साफ फोटो खींचें। AI तुरंत रोग का नाम और दवा की मात्रा बताएगा।",
                "voice_text": "छठा चरण: रोग डॉक्टर में पत्ती का फोटो खींचें और जैविक व रासायनिक दवा जानें।",
                "action_btn": "रोग डॉक्टर खोलें",
                "target": "disease"
            },
            {
                "num": "7",
                "icon": "🤖🎙️",
                "title": "AI से बोलकर पूछें या कॉल करें",
                "desc": "हरा माइक दबाएं और हिंदी में बोलें। मौसम, बीज या कीटनाशक के बारे में आवाज में उत्तर सुनें।",
                "voice_text": "सातवां चरण: माइक दबाकर हिंदी में कोई भी खेती का सवाल पूछें और आवाज में जवाब सुनें।",
                "action_btn": "वॉइस AI खोलें",
                "target": "voice"
            }
        ],
        "colors": [
            {"color": "#ef4444", "bg": "#fef2f2", "border": "#fca5a5", "icon": "🔴", "name": "लाल रंग (तुरंत ध्यान दें)", "desc": "खेत में नमी खत्म / आज ही पानी दें / पत्ती में रोग मिला / पोषक तत्व कम"},
            {"color": "#eab308", "bg": "#fefce8", "border": "#fde047", "icon": "🟡", "name": "पीला रंग (सावधानी)", "desc": "नमी कम हो रही है / 2 दिन में पानी दें / सामान्य खाद स्थिति"},
            {"color": "#22c55e", "bg": "#f0fdf4", "border": "#86efac", "icon": "🟢", "name": "हरा रंग (सुरक्षित)", "desc": "मिट्टी में नमी सही है / फसल स्वस्थ है / अभी पानी की जरूरत नहीं"},
            {"color": "#0284c7", "bg": "#f0f9ff", "border": "#7dd3fc", "icon": "💧", "name": "नीली पानी की बूंद", "desc": "खेत के लिए आवश्यक पानी की मात्रा और मोटर चलाने का कुल समय"},
            {"color": "#16a34a", "bg": "#f0fdf4", "border": "#86efac", "icon": "🌿", "name": "हरी पत्ती और बोरी", "desc": "यूरिया, डीएपी और पोटाश की कुल बोरियों की सटीक गिनती"},
            {"color": "#7c3aed", "bg": "#faf5ff", "border": "#d8b4fe", "icon": "🎤", "name": "बैंगनी माइक", "desc": "बिना लिखे अपनी भाषा में बोलकर सवाल पूछने के लिए माइक दबाएं"}
        ],
        "dos_donts": [
            {
                "topic": "💧 सिंचाई का सही समय",
                "do_text": "सुबह (6-9 बजे) या शाम (5-7 बजे) के समय सिंचाई करें।",
                "dont_text": "दोपहर की तेज धूप में सिंचाई न करें (पानी भाप बनकर उड़ जाता है)।"
            },
            {
                "topic": "🌿 खाद देने का तरीका",
                "do_text": "यूरिया को 3 भागों में बांटकर अलग-अलग चरणों पर डालें।",
                "dont_text": "बुवाई के समय एक साथ पूरा यूरिया न डालें (फसल जल सकती है)।"
            },
            {
                "topic": "🦠 पत्ती का फोटो खींचना",
                "do_text": "दिन की अच्छी रोशनी में पत्ती के धब्बों का साफ और पास से फोटो लें।",
                "dont_text": "अंधेरे में या दूर से धुंधला फोटो न खींचें।"
            },
            {
                "topic": "📡 सेंसर लगाना",
                "do_text": "सेंसर को मिट्टी में 10 सेमी गहराई पर जड़ों के पास लगाएं।",
                "dont_text": "ऊपर की सूखी धूल में सेंसर न छोड़ें।"
            }
        ]
    },
    "ta": {
        "title": "❓ விவசாய உதவி மையம் & காட்சி வழிகாட்டி",
        "subtitle": "எளிமையான சின்னங்கள், வண்ணங்கள் மற்றும் குரல் வழிகாட்டி",
        "voice_title": "🔊 முழு ஆடியோ வழிகாட்டலைக் கேளுங்கள்",
        "voice_sub": "தெளிவான தமிழ் குரலில் — செயலியை எவ்வாறு இயக்குவது என அறிய அழுத்தவும்",
        "btn_play": "🔊 வழிகாட்டலைக் கேளுங்கள்",
        "btn_stop": "⏹ நிறுத்து",
        "speech_lang": "ta-IN",
        "color_guide_title": "🎨 வண்ணங்கள் & சின்னங்களின் விளக்கம்",
        "color_guide_sub": "வண்ணங்களைப் பார்த்து நிலத்தின் நிலையை உடனே தெரிந்து கொள்ளுங்கள்:",
        "steps_header": "🚜 7-படி எளிய விவசாய வழிகாட்டுதல் (ஒவ்வொரு படியிலும் 🔊 அழுத்தவும்)",
        "dos_donts_header": "✅ செய்ய வேண்டியவை & ❌ தவிர்க்க வேண்டியவை",
        "emergency_header": "📞 இலவச உழவர் உதவி எண் 1551 & குரல் AI",
        "emergency_sub": "அரசு கிசான் உதவி எண்ணை அழைக்கவும் அல்லது AI உடன் பேசவும்:",
        "kisan_call_btn": "📞 1551 கிசான் உதவி மையம்",
        "open_voice_btn": "🎙️ AI உடன் பேசுங்கள்",
        "download_ppt_btn": "📥 வழிகாட்டி PDF பதிவிறக்கம்",
        "steps": [
            { "num": "1", "icon": "🌐", "title": "மொழி தேர்வு & உள்நுழைவு", "desc": "மொழியைத் தேர்ந்தெடுத்து பெயர், தொலைபேசி எண்ணை உள்ளிடவும்.", "voice_text": "படி ஒன்று: தமிழ் மொழியைத் தேர்ந்தெடுத்து பெயர் மற்றும் தொலைபேசி எண்ணை உள்ளிடவும்.", "action_btn": "முகப்பு", "target": "home" },
            { "num": "2", "icon": "📡", "title": "மண் தகவல் பதிவு செய்தல்", "desc": "மண் NPK, pH மற்றும் ஈரப்பதத்தை பதிவு செய்யவும் அல்லது சென்சாரை இணைக்கவும்.", "voice_text": "படி இரண்டு: மண் தகவல் பக்கத்தில் உங்கள் நிலத்தின் விவரங்களை உள்ளிடவும்.", "action_btn": "பண்ணை தகவல்", "target": "farm" },
            { "num": "3", "icon": "🌾", "title": "AI பயிர் பரிந்துரை", "desc": "உங்கள் நிலத்திற்கு அதிக மகசூல் தரும் சிறந்த பயிரை AI கண்டறியும்.", "voice_text": "படி மூன்று: உங்கள் மண்ணுக்கு ஏற்ற சிறந்த பயிரைத் தேர்ந்தெடுக்கவும்.", "action_btn": "பயிர் பரிந்துரை", "target": "crop" },
            { "num": "4", "icon": "💧", "title": "ஸ்மார்ட் பாசன முறை", "desc": "சிவப்பு நிறம் வந்தால் நீர் பாய்ச்சவும். பச்சை வந்தால் நீர் தேவையில்லை.", "voice_text": "படி நான்கு: சிவப்பு நிறம் வந்தால் இன்று நீர் பாய்ச்சவும், பச்சை நிறம் வந்தால் நீர் தேவையில்லை.", "action_btn": "பாசன ஆலோசகர்", "target": "water" },
            { "num": "5", "icon": "🌿", "title": "உர மேலாண்மை திட்டம்", "desc": "4-நிலை உர அட்டவணையைப் பின்பற்றி சரியான உர அளவை இடவும்.", "voice_text": "படி ஐந்து: 4 நிலைகளில் சரியான உர அளவை இடவும்.", "action_btn": "உர வழிகாட்டி", "target": "fertilizer" },
            { "num": "6", "icon": "🦠", "title": "பயிர் நோய் மருத்துவர்", "desc": "பாதிக்கப்பட்ட இலை புகைப்படத்தை பதிவேற்றி உடனடி தீர்வு பெறவும்.", "voice_text": "படி ஆறு: இலை புகைப்படத்தை பதிவேற்றி உடனடி மருந்து அளவை அறியவும்.", "action_btn": "நோய் மருத்துவர்", "target": "disease" },
            { "num": "7", "icon": "🤖🎙️", "title": "குரல் வழி AI உதவியாளர்", "desc": "குரல் வழியே உங்கள் விவசாயக் கேள்விகளைக் கேட்டு தெளிவு பெறவும்.", "voice_text": "படி ஏழு: மைக் பட்டனை அழுத்தி தமிழில் பேசி உடனடி குரல் பதில் பெறவும்.", "action_btn": "குரல் உதவியாளர்", "target": "voice" }
        ],
        "colors": [
            {"color": "#ef4444", "bg": "#fef2f2", "border": "#fca5a5", "icon": "🔴", "name": "சிவப்பு (உடனடி கவனம்)", "desc": "மண்ணில் ஈரம் இல்லை / உடனே நீர் பாய்ச்சவும் / நோய் பாதிப்பு"},
            {"color": "#eab308", "bg": "#fefce8", "border": "#fde047", "icon": "🟡", "name": "மஞ்சள் (எச்சரிக்கை)", "desc": "ஈரப்பதம் குறைகிறது / 2 நாட்களில் நீர் பாய்ச்சவும்"},
            {"color": "#22c55e", "bg": "#f0fdf4", "border": "#86efac", "icon": "🟢", "name": "பச்சை (பாதுகாப்பானது)", "desc": "மண் ஈரமாக உள்ளது / பயிர் நலம் / நீர் தேவையில்லை"},
            {"color": "#0284c7", "bg": "#f0f9ff", "border": "#7dd3fc", "icon": "💧", "name": "நீர்த்துளி", "desc": "பாசன நீர் அளவு மற்றும் மோட்டார் இயங்கும் நேரம்"},
            {"color": "#16a34a", "bg": "#f0fdf4", "border": "#86efac", "icon": "🌿", "name": "பச்சை இலை", "desc": "தேவையான உர மூட்டைகளின் எண்ணிக்கை"},
            {"color": "#7c3aed", "bg": "#faf5ff", "border": "#d8b4fe", "icon": "🎤", "name": "மைக்", "desc": "தமிழில் பேசி கேள்வி கேட்க மைக் பட்டனை அழுத்தவும்"}
        ],
        "dos_donts": [
            { "topic": "💧 பாசன நேரம்", "do_text": "காலை (6-9 மணி) அல்லது மாலை (5-7 மணி) நேரத்தில் நீர் பாய்ச்சவும்.", "dont_text": "நண்பகல் வெயிலில் நீர் பாய்ச்ச வேண்டாம்." },
            { "topic": "🌿 உர பயன்பாடு", "do_text": "யூரியாவை 3 தவணைகளாகப் பிரித்து இடவும்.", "dont_text": "ஒரே நேரத்தில் அதிக யூரியா இட வேண்டாம்." },
            { "topic": "🦠 இலை புகைப்படம்", "do_text": "நல்ல வெளிச்சத்தில் தெளிவான புகைப்படம் எடுக்கவும்.", "dont_text": "இருட்டில் மங்கலான படம் எடுக்க வேண்டாம்." },
            { "topic": "📡 சென்சார் முறை", "do_text": "சென்சாரை 10 செ.மீ ஆழத்தில் மண்ணில் வைக்கவும்.", "dont_text": "மேல் தரை தூசியில் சென்சாரை வைக்க வேண்டாம்." }
        ]
    },
    "kn": {
        "title": "❓ ರೈತ ಸಹಾಯ ಕೇಂದ್ರ & ದೃಶ್ಯ ಮಾರ್ಗದರ್ಶಿ",
        "subtitle": "ಅನಕ್ಷರಸ್ಥ ರೈತರಿಗಾಗಿ ಸರಳ ಚಿಹ್ನೆಗಳು, ಬಣ್ಣಗಳು ಮತ್ತು ಧ್ವನಿ ಮಾರ್ಗದರ್ಶಿ",
        "voice_title": "🔊 ಸಂಪೂರ್ಣ ಆಡಿಯೋ ಮಾರ್ಗದರ್ಶಿ ಆಲಿಸಿ",
        "voice_sub": "ಕನ್ನಡ ಧ್ವನಿಯಲ್ಲಿ — ಆ್ಯಪ್ ಹೇಗೆ ಬಳಸಬೇಕೆಂದು ತಿಳಿಯಲು ಒತ್ತಿ",
        "btn_play": "🔊 ಮಾರ್ಗದರ್ಶಿ ಆಲಿಸಿ",
        "btn_stop": "⏹ ನಿಲ್ಲಿಸಿ",
        "speech_lang": "kn-IN",
        "color_guide_title": "🎨 ಬಣ್ಣಗಳು ಮತ್ತು ಚಿಹ್ನೆಗಳ ವಿವರಣೆ",
        "color_guide_sub": "ಬಣ್ಣಗಳನ್ನು ನೋಡಿ ನಿಮ್ಮ ಹೊಲದ ಸ್ಥಿತಿಯನ್ನು ಸುಲಭವಾಗಿ ತಿಳಿಯಿರಿ:",
        "steps_header": "🚜 7 ಹಂತಗಳಲ್ಲಿ ಸುಲಭ ಕೃಷಿ ಮಾರ್ಗದರ್ಶನ (ಪ್ರತಿ ಹಂತದಲ್ಲಿ 🔊 ಒತ್ತಿ ಆಲಿಸಿ)",
        "dos_donts_header": "✅ ಮಾಡಬೇಕಾದದ್ದು & ❌ ಮಾಡಬಾರದ್ದು",
        "emergency_header": "📞 ಉಚಿತ ಕಿಸಾನ್ ಸಹಾಯವಾಣಿ 1551 & ವಾಯ್ಸ್ AI",
        "emergency_sub": "ಸಂದೇಹಗಳಿದ್ದರೆ ಉಚಿತ ಕಿಸಾನ್ ಸಂಖ್ಯೆಗೆ ಕರೆ ಮಾಡಿ ಅಥವಾ AI ಜೊತೆ ಮಾತನಾಡಿ:",
        "kisan_call_btn": "📞 1551 ಕಿಸಾನ್ ಕಾಲ್ ಸೆಂಟರ್",
        "open_voice_btn": "🎙️ AI ಜೊತೆ ಮಾತನಾಡಿ",
        "download_ppt_btn": "📥 ಮಾರ್ಗದರ್ಶಿ PDF ಡೌನ್‌ಲೋಡ್",
        "steps": [
            { "num": "1", "icon": "🌐", "title": "ಭಾಷೆ ಆಯ್ಕೆ & ಲಾಗಿನ್", "desc": "ಕನ್ನಡ ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ ಹೆಸರು, ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ.", "voice_text": "ಹಂತ 1: ಕನ್ನಡ ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ ನಿಮ್ಮ ಹೆಸರು ಮತ್ತು ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ.", "action_btn": "ಮುಖಪುಟ", "target": "home" },
            { "num": "2", "icon": "📡", "title": "ಮಣ್ಣಿನ ಮಾಹಿತಿ ದಾಖಲಿಸಿ", "desc": "ಮಣ್ಣಿನ NPK, pH ಮತ್ತು ತೇವಾಂಶ ನಮೂದಿಸಿ ಅಥವಾ ಸೆನ್ಸರ್ ಬಳಸಿ.", "voice_text": "ಹಂತ 2: ಹೊಲದ ಮಾಹಿತಿ ಪುಟದಲ್ಲಿ ಮಣ್ಣಿನ ಪೋಷಕಾಂಶಗಳನ್ನು ದಾಖಲಿಸಿ.", "action_btn": "ಹೊಲದ ಮಾಹಿತಿ", "target": "farm" },
            { "num": "3", "icon": "🌾", "title": "AI ಬೆಳೆ ಶಿಫಾರಸು", "desc": "ನಿಮ್ಮ ಜಮೀನಿಗೆ ಗರಿಷ್ಠ ಇಳುವರಿ ನೀಡುವ ಉತ್ತಮ ಬೆಳೆಯನ್ನು ತಿಳಿಯಿರಿ.", "voice_text": "ಹಂತ 3: ನಿಮ್ಮ ಮಣ್ಣಿಗೆ ಸೂಕ್ತವಾದ ಉತ್ತಮ ಬೆಳೆಯನ್ನು ತಿಳಿಯಿರಿ.", "action_btn": "ಬೆಳೆ ಶಿಫಾರಸು", "target": "crop" },
            { "num": "4", "icon": "💧", "title": "ಸ್ಮಾರ್ಟ್ ನೀರಾವರಿ ಸಲಹೆ", "desc": "ಕೆಂಪು ಬಣ್ಣ ಕಂಡರೆ ನೀರು ಕೊಡಿ. ಹಸಿರು ಇದ್ದರೆ ನೀರು ಅಗತ್ಯವಿಲ್ಲ.", "voice_text": "ಹಂತ 4: ಕೆಂಪು ಬಣ್ಣ ಕಂಡರೆ ನೀರು ಹರಿಸಿ, ಹಸಿರು ಇದ್ದರೆ ನೀರು ಬೇಡ.", "action_btn": "ನೀರಾವರಿ ಸಲಹೆ", "target": "water" },
            { "num": "5", "icon": "🌿", "title": "ರಸಗೊಬ್ಬರ ನಿರ್ವಹಣೆ", "desc": "4-ಹಂತದ ರಸಗೊಬ್ಬರ ವೇಳಾಪಟ್ಟಿ ಮತ್ತು ಚೀಲಗಳ ಲೆಕ್ಕ ಪಡೆಯಿರಿ.", "voice_text": "ಹಂತ 5: 4 ಹಂತಗಳಲ್ಲಿ ರಸಗೊಬ್ಬರ ಪ್ರಮಾಣ ಮತ್ತು ಸಮಯ ತಿಳಿಯಿರಿ.", "action_btn": "ರಸಗೊಬ್ಬರ ಸಲಹೆ", "target": "fertilizer" },
            { "num": "6", "icon": "🦠", "title": "ಬೆಳೆ ರೋಗ ವೈದ್ಯ", "desc": "ಎಲೆಯ ಫೋಟೋ ತೆಗೆದು ಅಪ್ಲೋಡ್ ಮಾಡಿ ತಕ್ಷಣ ಪರಿಹಾರ ತಿಳಿಯಿರಿ.", "voice_text": "ಹಂತ 6: ಎಲೆಯ ಫೋಟೋ ಅಪ್ಲೋಡ್ ಮಾಡಿ ರೋಗ ಪರಿಹಾರ ಔಷಧಿ ತಿಳಿಯಿರಿ.", "action_btn": "ರೋಗ ವೈದ್ಯ", "target": "disease" },
            { "num": "7", "icon": "🤖🎙️", "title": "ವಾಯ್ಸ್ AI ಮೂಲಕ ಮಾತನಾಡಿ", "desc": "ಮೈಕ್ ಒತ್ತಿ ಕನ್ನಡದಲ್ಲೇ ಮಾತನಾಡಿ ಧ್ವನಿ ಉತ್ತರ ಪಡೆಯಿರಿ.", "voice_text": "ಹಂತ 7: ಮೈಕ್ ಒತ್ತಿ ಕನ್ನಡದಲ್ಲೇ ಕೃಷಿ ಪ್ರಶ್ನೆಗಳನ್ನು ಕೇಳಿ.", "action_btn": "ವಾಯ್ಸ್ AI", "target": "voice" }
        ],
        "colors": [
            {"color": "#ef4444", "bg": "#fef2f2", "border": "#fca5a5", "icon": "🔴", "name": "ಕೆಂಪು (ತಕ್ಷಣ ಕ್ರಮ)", "desc": "ತೇವಾಂಶವಿಲ್ಲ / ತಕ್ಷಣ ನೀರು ಕೊಡಿ / ರೋಗ ಪತ್ತೆಯಾಗಿದೆ"},
            {"color": "#eab308", "bg": "#fefce8", "border": "#fde047", "icon": "🟡", "name": "ಹಳದಿ (ಎಚ್ಚರಿಕೆ)", "desc": "ತೇವಾಂಶ ಕಡಿಮೆಯಾಗುತ್ತಿದೆ / 2 ದಿನದಲ್ಲಿ ನೀರು ಕೊಡಿ"},
            {"color": "#22c55e", "bg": "#f0fdf4", "border": "#86efac", "icon": "🟢", "name": "ಹಸಿರು (ಸುರಕ್ಷಿತ)", "desc": "ಮಣ್ಣಿನಲ್ಲಿ ತೇವಾಂಶ ಸರಿಯಾಗಿದೆ / ಬೆಳೆ ಆರೋಗ್ಯವಾಗಿದೆ"},
            {"color": "#0284c7", "bg": "#f0f9ff", "border": "#7dd3fc", "icon": "💧", "name": "ನೀರಿನ ಹನಿ", "desc": "ಅಗತ್ಯ ನೀರಿನ ಪ್ರಮಾಣ ಮತ್ತು ಮೋಟಾರ್ ಚಾಲನಾ ಸಮಯ"},
            {"color": "#16a34a", "bg": "#f0fdf4", "border": "#86efac", "icon": "🌿", "name": "ಹಸಿರು ಎಲೆ", "desc": "ಅಗತ್ಯ ರಸಗೊಬ್ಬರ ಚೀಲಗಳ ನಿಖರ ಸಂಖ್ಯೆ"},
            {"color": "#7c3aed", "bg": "#faf5ff", "border": "#d8b4fe", "icon": "🎤", "name": "ಮೈಕ್ರೋಫೋನ್", "desc": "ಕನ್ನಡದಲ್ಲೇ ಮಾತನಾಡಿ ಪ್ರಶ್ನೆ ಕೇಳಲು ಮೈಕ್ ಒತ್ತಿ"}
        ],
        "dos_donts": [
            { "topic": "💧 ನೀರಾವರಿ ಸಮಯ", "do_text": "ಬೆಳಿಗ್ಗೆ (6-9 ಗಂಟೆ) ಅಥವಾ ಸಂಜೆ (5-7 ಗಂಟೆ) ನೀರು ಕೊಡಿ.", "dont_text": "ಮಧ್ಯಾಹ್ನದ ಬಿರುಬಿಸಿಲಿನಲ್ಲಿ ನೀರು ಕೊಡಬೇಡಿ." },
            { "topic": "🌿 ಗೊಬ್ಬರ ಬಳಕೆ", "do_text": "ಯೂರಿಯಾವನ್ನು 3 ಕಂತುಗಳಲ್ಲಿ ವಿಭಜಿಸಿ ಹಾಕಿ.", "dont_text": "ಒಂದೇ ಬಾರಿಗೆ ಪೂರ್ತಿ ಯೂರಿಯಾ ಹಾಕಬೇಡಿ." },
            { "topic": "🦠 ಎಲೆಯ ಫೋಟೋ", "do_text": "ಬೆಳಕಿನಲ್ಲಿ ಎಲೆಯ ಸ್ಪಷ್ಟ ಫೋಟೋ ತೆಗೆದುಕೊಳ್ಳಿ.", "dont_text": "ಕತ್ತಲೆಯಲ್ಲಿ ಮಸುಕಾದ ಫೋಟೋ ತೆಗೆಯಬೇಡಿ." },
            { "topic": "📡 ಸೆನ್ಸರ್ ಬಳಕೆ", "do_text": "ಸೆನ್ಸರ್ ಅನ್ನು 10 ಸೆಂ.ಮೀ ಮಣ್ಣಿನ ಆಳದಲ್ಲಿ ಇರಿಸಿ.", "dont_text": "ಮೇಲ್ಭಾಗದ ಒಣ ಮಣ್ಣಿನಲ್ಲಿ ಸೆನ್ಸರ್ ಇಡಬೇಡಿ." }
        ]
    },
    "mr": {
        "title": "❓ शेतकरी मदत केंद्र व दृश्य मार्गदर्शक",
        "subtitle": "अशिक्षित शेतकरी बांधवांसाठी सोपी चिन्हे, रंग आणि ऑडिओ मार्गदर्शक",
        "voice_title": "🔊 संपूर्ण ऑडिओ सल्ला ऐका (45 सेकंद)",
        "voice_sub": "मराठी ऑडिओमध्ये — ॲप कसे वापरावे हे ऐकण्यासाठी दाबा",
        "btn_play": "🔊 ऑडिओ ऐका",
        "btn_stop": "⏹ थांबवा",
        "speech_lang": "mr-IN",
        "color_guide_title": "🎨 रंग आणि चिन्हांचा अर्थ (ट्रॅफिक लाईट पद्धत)",
        "color_guide_sub": "स्क्रीनवरील रंगांवरून आपल्या शेताची स्थिती त्वरित ओळखा:",
        "steps_header": "🚜 7 टप्प्यांमध्ये शेती मार्गदर्शक (प्रत्येक टप्प्यावर 🔊 दाबून ऐका)",
        "dos_donts_header": "✅ काय करावे & ❌ काय करू नये (उत्तम शेती नियम)",
        "emergency_header": "📞 मोफत किसान कॉल सेंटर 1551 & व्हॉईस AI",
        "emergency_sub": "सल्ल्यासाठी मोफत किसान क्रमांकावर कॉल करा किंवा AI शी बोला:",
        "kisan_call_btn": "📞 1551 किसान कॉल सेंटर",
        "open_voice_btn": "🎙️ AI शी बोला",
        "download_ppt_btn": "📥 मार्गदर्शक PDF डाउनलोड",
        "steps": [
            { "num": "1", "icon": "🌐", "title": "भाषा निवडा व लॉगिन करा", "desc": "मराठी भाषा निवडून नाव आणि मोबाईल नंबर टाका.", "voice_text": "टप्पा 1: मराठी भाषा निवडा, नाव आणि फोन नंबर टाकून डॅशबोर्ड उघडा.", "action_btn": "मुख्य डॅशबोर्ड", "target": "home" },
            { "num": "2", "icon": "📡", "title": "शेताचा डेटा भरा", "desc": "मातीतील NPK, pH आणि ओलावा भरा किंवा सेन्सर जोडा.", "voice_text": "टप्पा 2: शेताचा डेटा पानावर मातीची माहिती भरा किंवा सेन्सर जोडा.", "action_btn": "शेताचा डेटा", "target": "farm" },
            { "num": "3", "icon": "🌾", "title": "AI पीक शिफारस मिळवा", "desc": "तुमच्या शेतासाठी सर्वाधिक उत्पादन देणारे पीक शोधा.", "voice_text": "टप्पा 3: तुमच्या जमिनीसाठी उत्तम पीक शिफारस मिळवा.", "action_btn": "पीक शिफारस", "target": "crop" },
            { "num": "4", "icon": "💧", "title": "स्मार्ट सिंचन सल्ला", "desc": "लाल रंग दिसल्यास पाणी द्या. हिरवा असल्यास पाणी देऊ नका.", "voice_text": "टप्पा 4: लाल रंग दिसल्यास आजच पाणी द्या, हिरवा असल्यास पाणी देऊ नका.", "action_btn": "सिंचन सल्ला", "target": "water" },
            { "num": "5", "icon": "🌿", "title": "4-टप्प्यांचे खत नियोजन", "desc": "पेरणी ते दाना भरण्यापर्यंत खतांचे अचूक नियोजन करा.", "voice_text": "टप्पा 5: 4 टप्प्यांमध्ये खतांचे योग्य नियोजन आणि पोत्यांची संख्या जाणून घ्या.", "action_btn": "खत सल्ला", "target": "fertilizer" },
            { "num": "6", "icon": "🦠", "title": "पीक रोग डॉक्टर", "desc": "पानांचा फोटो काढून त्वरित रोग निदान व औषध उपाय मिळवा.", "voice_text": "टप्पा 6: आजारी पानाचा फोटो काढून त्वरित औषध व उपाय जाणून घ्या.", "action_btn": "रोग डॉक्टर", "target": "disease" },
            { "num": "7", "icon": "🤖🎙️", "title": "AI व्हॉईस सहाय्यक", "desc": "मराठीत बोलून शेतीविषयक कोणत्याही प्रश्नाचे उत्तर मिळवा.", "voice_text": "टप्पा 7: माईक दाबून मराठीत बोला आणि आवाजात उत्तर मिळवा.", "action_btn": "व्हॉईस AI", "target": "voice" }
        ],
        "colors": [
            {"color": "#ef4444", "bg": "#fef2f2", "border": "#fca5a5", "icon": "🔴", "name": "लाल रंग (तातडीची कृती)", "desc": "मातीत ओलावा नाही / आजच पाणी द्या / रोग आढळला"},
            {"color": "#eab308", "bg": "#fefce8", "border": "#fde047", "icon": "🟡", "name": "पिवळा रंग (सावधानता)", "desc": "ओलावा कमी होत आहे / 2 दिवसांत पाणी द्या"},
            {"color": "#22c55e", "bg": "#f0fdf4", "border": "#86efac", "icon": "🟢", "name": "हिरवा रंग (सुरक्षित)", "desc": "मातीत पुरेसा ओलावा आहे / पीक निरोगी आहे"},
            {"color": "#0284c7", "bg": "#f0f9ff", "border": "#7dd3fc", "icon": "💧", "name": "निळा पाण्याचा थेंब", "desc": "पाण्याचे प्रमाण आणि मोटर चालवण्याची अचूक वेळ"},
            {"color": "#16a34a", "bg": "#f0fdf4", "border": "#86efac", "icon": "🌿", "name": "हिरवे पान व पोते", "desc": "युरिया, डीएपी आणि पोटॅश पोत्यांची अचूक संख्या"},
            {"color": "#7c3aed", "bg": "#faf5ff", "border": "#d8b4fe", "icon": "🎤", "name": "मायक्रोफोन", "desc": "मराठीत बोलून प्रश्न विचारण्यासाठी माईक दाबा"}
        ],
        "dos_donts": [
            { "topic": "💧 पाणी देण्याची वेळ", "do_text": "सकाळी (6-9) किंवा संध्याकाळी (5-7) थंड वेळेत पाणी द्या.", "dont_text": "दुपारच्या कडक उन्हात पाणी देऊ नका." },
            { "topic": "🌿 खत वापर पद्धत", "do_text": "युरिया 3 टप्प्यांमध्ये विभागून द्या.", "dont_text": "एकाच वेळी सर्व युरिया टाकू नका." },
            { "topic": "🦠 पानाचा फोटो", "do_text": "दिवसाच्या प्रकाशात पानाचा स्पष्ट फोटो घ्या.", "dont_text": "अंधारात अस्पष्ट फोटो काढू नका." },
            { "topic": "📡 सेन्सर वापर", "do_text": "सेन्सर मातीत 10 सेमी खोल मुळांपाशी लावा.", "dont_text": "वरच्या कोरड्या धुळीत सेन्सर ठेवू नका." }
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
    # 🔊 MASTER MULTILINGUAL AUDIO WALKTHROUGH COMPONENT
    # =====================================================
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #14532d 0%, #166534 100%); border-radius: 18px; padding: 22px 24px; color: white; margin-bottom: 20px; box-shadow: 0 8px 24px rgba(20, 83, 45, 0.35);">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
                <div style="flex: 1; min-width: 250px;">
                    <span style="background: rgba(255,255,255,0.2); color: #ffffff; padding: 4px 14px; border-radius: 999px; font-size: 12px; font-weight: 800; border: 1px solid rgba(255,255,255,0.35);">
                        📢 Voice User Guide • వాయిస్ గైడ్
                    </span>
                    <h2 style="color: #ffffff !important; font-size: 22px !important; font-weight: 800; margin: 10px 0 6px 0;">
                        {ui['voice_title']}
                    </h2>
                    <p style="color: #dcfce7; font-size: 13.5px; margin: 0; font-weight: 600; line-height: 1.4;">
                        {ui['voice_sub']}
                    </p>
                </div>
                <div style="font-size: 44px;">🎧</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Master audio script
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
        <div style="display: flex; gap: 12px; margin-bottom: 16px;">
            <button id="playHelpVoice" onclick="playVoice()" style="
                flex: 1;
                min-height: 52px;
                background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
                color: #ffffff;
                border: none;
                border-radius: 14px;
                font-family: system-ui, -apple-system, sans-serif;
                font-size: 16px;
                font-weight: 800;
                cursor: pointer;
                box-shadow: 0 4px 14px rgba(22, 163, 74, 0.4);
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
                transition: transform 0.15s ease;
            " onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1.0)'">
                <span>{ui['btn_play']}</span>
            </button>
            <button id="stopHelpVoice" onclick="stopVoice()" style="
                min-height: 52px;
                padding: 0 24px;
                background: #334155;
                color: #f8fafc;
                border: 1px solid #475569;
                border-radius: 14px;
                font-family: system-ui, -apple-system, sans-serif;
                font-size: 15px;
                font-weight: 700;
                cursor: pointer;
                transition: transform 0.15s ease;
            " onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1.0)'">
                {ui['btn_stop']}
            </button>
        </div>
        <script>
            const textToSpeak = {script_json};
            const speechLang = "{speech_lang_code}";

            function playVoice() {{
                if (!('speechSynthesis' in window)) {{
                    alert('Speech synthesis is not supported on this browser.');
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
        height=68
    )

    # =====================================================
    # 🎨 COLOR & SYMBOL MEANING GUIDE (TRAFFIC LIGHTS)
    # =====================================================
    with st.expander(f"🎨 {ui['color_guide_title']}", expanded=True):
        st.write(ui["color_guide_sub"])
        cols = st.columns(2)
        for i, c in enumerate(ui["colors"]):
            col_target = cols[i % 2]
            with col_target:
                st.markdown(
                    f"""
                    <div style="background: {c['bg']}; border: 1.5px solid {c['border']}; border-radius: 14px; padding: 14px 16px; margin-bottom: 12px;">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                            <span style="font-size: 22px;">{c['icon']}</span>
                            <span style="font-weight: 800; font-size: 15px; color: {c['color']};">{c['name']}</span>
                        </div>
                        <div style="font-size: 13px; color: #334155; line-height: 1.45; font-weight: 500;">
                            {c['desc']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown("---")

    # =====================================================
    # 🚜 7-STEP INTERACTIVE WORKFLOW CARDS WITH STEP AUDIO
    # =====================================================
    st.subheader(ui["steps_header"])

    steps = ui["steps"]
    for item in steps:
        with st.container(border=True):
            col_icon, col_content, col_actions = st.columns([1, 6, 3])
            
            with col_icon:
                st.markdown(
                    f"""
                    <div style="width: 52px; height: 52px; border-radius: 16px; background: #dcfce7; color: #166534; display: flex; align-items: center; justify-content: center; font-size: 28px; font-weight: 800; border: 1px solid #86efac; box-shadow: 0 2px 8px rgba(22, 101, 52, 0.15);">
                        {item['icon']}
                    </div>
                    <div style="text-align: center; margin-top: 4px; font-size: 11px; font-weight: 800; color: #15803d;">
                        STEP {item['num']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col_content:
                st.markdown(f"<div style='font-weight: 800; font-size: 17px; color: #0f172a;'>{item['title']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size: 13.5px; color: #334155; margin-top: 4px; line-height: 1.5;'>{item['desc']}</div>", unsafe_allow_html=True)
                
                # Dedicated Audio Play Button for this Step
                step_voice_text = json.dumps(item["voice_text"])
                components.html(
                    f"""
                    <div style="margin-top: 6px;">
                        <button id="btn_step_voice_{item['num']}" onclick="playStepVoice_{item['num']}()" style="
                            background: #f1f5f9;
                            border: 1px solid #cbd5e1;
                            color: #1e293b;
                            border-radius: 8px;
                            padding: 6px 14px;
                            font-size: 12.5px;
                            font-weight: 700;
                            font-family: system-ui, sans-serif;
                            cursor: pointer;
                            display: inline-flex;
                            align-items: center;
                            gap: 6px;
                            transition: all 0.15s ease;
                        " onmouseover="this.style.background='#e2e8f0'" onmouseout="this.style.background='#f1f5f9'">
                            <span>🔊 వినండి / Listen (Step {item['num']})</span>
                        </button>
                    </div>
                    <script>
                        function playStepVoice_{item['num']}() {{
                            if (!('speechSynthesis' in window)) return;
                            window.speechSynthesis.cancel();
                            const u = new SpeechSynthesisUtterance({step_voice_text});
                            u.lang = "{speech_lang_code}";
                            u.rate = 0.90;
                            const btn = document.getElementById('btn_step_voice_{item['num']}');
                            btn.style.background = '#dcfce7';
                            btn.style.color = '#166534';
                            btn.style.borderColor = '#86efac';
                            u.onend = function() {{
                                btn.style.background = '#f1f5f9';
                                btn.style.color = '#1e293b';
                                btn.style.borderColor = '#cbd5e1';
                            }};
                            window.speechSynthesis.speak(u);
                        }}
                    </script>
                    """,
                    height=44
                )

                # Visual Screenshot Flow Card with Pointer Arrows
                step_images = {
                    "1": "images/step1_login_ui.png",
                    "2": "images/step2_farm_data_ui.png",
                    "3": "images/step3_crop_recommendation_ui.png",
                    "4": "images/step4_irrigation_advisor_ui.png",
                    "5": "images/step5_fertilizer_advisor_ui.png",
                    "6": "images/step6_disease_doctor_ui.png",
                    "7": "images/step7_voice_ai_ui.png"
                }
                s_img = step_images.get(str(item["num"]))
                if s_img and os.path.exists(s_img):
                    with st.expander(f"🖼️ స్క్రీన్ చిత్రం & ఎక్కడ నొక్కాలో చూడండి (Step {item['num']} Visual Guide)", expanded=True):
                        st.image(s_img, caption=f"Step {item['num']} Screen & Pointer Arrows (ఎరుపు బాణం సూచించిన చోట నొక్కండి / Tap where red arrow points)", use_container_width=True)

            with col_actions:
                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                if st.button(f"👉 {item['action_btn']}", key=f"btn_step_nav_{item['num']}", use_container_width=True):
                    st.session_state.page = item["target"]
                    st.rerun()

    st.markdown("---")

    # =====================================================
    # ✅ WHAT TO DO & ❌ WHAT TO AVOID (DO'S & DON'TS)
    # =====================================================
    st.subheader(ui["dos_donts_header"])
    
    dos_cols = st.columns(2)
    for idx, d in enumerate(ui["dos_donts"]):
        col_dos = dos_cols[idx % 2]
        with col_dos:
            st.markdown(
                f"""
                <div style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 16px; padding: 16px; margin-bottom: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.04);">
                    <div style="font-weight: 800; font-size: 15px; color: #0f172a; margin-bottom: 10px; border-bottom: 1px solid #f1f5f9; padding-bottom: 6px;">
                        {d['topic']}
                    </div>
                    <div style="background: #f0fdf4; border: 1px solid #86efac; border-radius: 10px; padding: 10px 12px; margin-bottom: 8px;">
                        <span style="color: #16a34a; font-weight: 800; font-size: 13px;">✅ చేయండి / DO:</span>
                        <div style="font-size: 12.5px; color: #166534; margin-top: 2px; line-height: 1.4;">
                            {d['do_text']}
                        </div>
                    </div>
                    <div style="background: #fef2f2; border: 1px solid #fca5a5; border-radius: 10px; padding: 10px 12px;">
                        <span style="color: #dc2626; font-weight: 800; font-size: 13px;">❌ చేయవద్దు / DON'T:</span>
                        <div style="font-size: 12.5px; color: #991b1b; margin-top: 2px; line-height: 1.4;">
                            {d['dont_text']}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # =====================================================
    # 📞 EMERGENCY TOLL-FREE KISAN HELPLINE & QUICK ACTIONS
    # =====================================================
    st.subheader(ui["emergency_header"])
    st.caption(ui["emergency_sub"])

    c_help1, c_help2, c_help3 = st.columns(3)

    with c_help1:
        st.markdown(
            f"""
            <a href="tel:1551" style="text-decoration: none;">
                <div style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); color: white; padding: 16px; border-radius: 14px; text-align: center; box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35); cursor: pointer;">
                    <div style="font-size: 28px; margin-bottom: 4px;">📞</div>
                    <div style="font-weight: 800; font-size: 15px;">{ui['kisan_call_btn']}</div>
                    <div style="font-size: 11.5px; color: #e0f2fe; margin-top: 4px;">Toll-Free Govt Support (6 AM - 10 PM)</div>
                </div>
            </a>
            """,
            unsafe_allow_html=True
        )

    with c_help2:
        if st.button(ui["open_voice_btn"], key="btn_open_voice_emergency", use_container_width=True):
            st.session_state.page = "voice"
            st.rerun()

    with c_help3:
        ppt_path = "AgriSense_AI_Farmer_Guide_Slides.pdf"
        if os.path.exists(ppt_path):
            with open(ppt_path, "rb") as f:
                st.download_button(
                    label=ui["download_ppt_btn"],
                    data=f,
                    file_name="AgriSense_AI_Farmer_Guide_Slides.pdf",
                    mime="application/pdf",
                    key="btn_download_ppt_help",
                    use_container_width=True
                )
        else:
            st.button(ui["download_ppt_btn"], disabled=True, use_container_width=True)
