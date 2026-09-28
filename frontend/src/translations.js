export const TRANSLATIONS = {
  "English": {
    "code": "en-IN",
    "appName": "AgriSense AI",
    "tagline": "Smart Agricultural Decision Support & Farm Intelligence",
    "nav": {
      "dashboard": "Dashboard",
      "crop": "Crop Advisory",
      "soil": "Soil Health",
      "irrigation": "Irrigation",
      "fertilizer": "Fertilizer",
      "disease": "Plant Doctor",
      "mandi": "Mandi Prices",
      "schemes": "Govt Schemes",
      "voice": "Voice AI",
      "chat": "AI Chat",
      "help": "Help Guide",
      "sensors": "IoT Sensors",
      "briefing": "1-Min Briefing",
      "menu": "All Modules"
    },
    "login": {
      "title": "Farmer Profile Access",
      "subtitle": "Enter your name and mobile number to load your personalized farm data",
      "name": "Farmer Name",
      "phone": "10-Digit Mobile Number",
      "submit": "Enter Farm Portal",
      "placeholderName": "e.g. Ramesh Kumar",
      "placeholderPhone": "e.g. 9876543210"
    },
    "dashboard": {
      "welcome": "Welcome, Farmer",
      "greeting": "Here is today's real-time farm intelligence & soil diagnostics.",
      "weatherTitle": "Live Climate Conditions",
      "weatherDesc": "Optimal conditions for Kharif & Rabi field operations",
      "soilScore": "Soil Vitality Score",
      "iotStatus": "IoT Telemetry Status",
      "quickActions": "Quick Farm Actions",
      "recCrop": "Recommended Crop",
      "waterStatus": "Soil Moisture Status",
      "optimal": "Optimal",
      "needsWater": "Needs Irrigation",
      "viewDetails": "View Details",
      "steps": {
        "step1": "1. Soil Test",
        "step2": "2. AI Recommendation",
        "step3": "3. Advice & Economics"
      },
      "features": {
        "sensors": {
          "title": "Step 1 — Soil Test",
          "desc": "Enter NPK, pH, moisture manually or connect the ESP32 7-in-1 sensor probe for live data.",
          "cta": "Start Soil Test"
        },
        "crop": {
          "title": "Step 2 — Crop AI Recommendation",
          "desc": "ML RandomForest model analyses your 7 soil & climate values to predict the best crop with alternatives.",
          "cta": "Get Crop Recommendation"
        },
        "soil": {
          "title": "Soil Health Report",
          "desc": "Detailed NPK deficiency chart, pH chemistry, and personalized soil enrichment treatment plan.",
          "cta": "View Soil Report"
        },
        "irrigation": {
          "title": "Smart Irrigation",
          "desc": "Red = water urgently, Green = soil moist. Calculates exact motor pump hours for your field size.",
          "cta": "Open Irrigation Advisor"
        },
        "fertilizer": {
          "title": "Fertilizer Schedule",
          "desc": "Stage-wise Urea, DAP, MOP bag quantities across 4 crop growth stages to minimize cost.",
          "cta": "View Fertilizer Plan"
        },
        "disease": {
          "title": "Plant Doctor (AI)",
          "desc": "Upload a leaf photo or describe symptoms — AI diagnoses disease and gives organic + chemical cure.",
          "cta": "Open Plant Doctor"
        },
        "mandi": {
          "title": "Live Mandi Prices",
          "desc": "e-NAM APMC rates, MSP comparison, best market timing, and full farm cost-profit estimator.",
          "cta": "View Market Prices"
        },
        "schemes": {
          "title": "Government Schemes",
          "desc": "PM-KISAN ₹6,000 / PM-KUSUM solar pump / PMFBY insurance / KCC credit and 20+ state schemes.",
          "cta": "Browse Schemes"
        },
        "voice": {
          "title": "Voice AI Assistant",
          "desc": "Speak in your language — AgriSense AI answers instantly with voice. Zero typing needed.",
          "cta": "Talk to AgriSense"
        },
        "chat": {
          "title": "AI Chat Assistant",
          "desc": "Ask any farming question by text. AI uses your actual farm data to give personalised advice.",
          "cta": "Open AI Chat"
        },
        "help": {
          "title": "Help & Guide",
          "desc": "7-step audio walkthrough, colour guide, best practices, and toll-free Kisan Helpline 1551.",
          "cta": "Open Help Guide"
        }
      }
    },
    "crop": {
      "title": "ML Crop Recommendation",
      "subtitle": "Our trained Machine Learning algorithm analyzes your 7 soil & climate factors to predict the highest yielding crop.",
      "nitrogen": "Nitrogen (N)",
      "phosphorus": "Phosphorus (P)",
      "potassium": "Potassium (K)",
      "temp": "Temperature (°C)",
      "humidity": "Humidity (%)",
      "ph": "Soil pH Level",
      "rainfall": "Rainfall (mm)",
      "predictBtn": "🌱 Predict Best Crop",
      "useLatest": "⚡ Autofill from Farm Sensors",
      "resultTitle": "Recommended Crop",
      "suitability": "Suitability Score",
      "packageOfPractice": "Agronomy Guidelines & Sowing Package"
    },
    "soil": {
      "title": "Soil Health & Nutrient Balance",
      "subtitle": "Evaluate NPK elemental reserves and pH chemistry for maximum nutrient uptake.",
      "npkRatio": "Current NPK Ratio",
      "idealRatio": "Ideal Ratio (4:2:1)",
      "organicCarbon": "Organic Carbon Status",
      "phStatus": "pH Reaction",
      "recommendations": "Soil Enhancement Directives"
    },
    "irrigation": {
      "title": "Precision Irrigation Advisor",
      "subtitle": "Real-time soil moisture calculations with automated watering scheduling.",
      "moistureGauge": "Root Zone Soil Moisture",
      "schedule": "Recommended Watering Schedule",
      "waterReq": "Estimated Water Requirement",
      "calcBtn": "Calculate Irrigation Need"
    },
    "fertilizer": {
      "title": "Customized Fertilizer Calculator",
      "subtitle": "Targeted NPK gap replenishment using both chemical and organic manures.",
      "targetCrop": "Target Crop",
      "landSize": "Field Size (Acres)",
      "calcBtn": "Generate Fertilizer Plan",
      "organicPlan": "Organic Manure Plan",
      "chemicalPlan": "Chemical Fertilizer Dosage"
    },
    "disease": {
      "title": "AI Plant Doctor & Disease Diagnosis",
      "subtitle": "Snap or select leaf symptoms to receive instant pathology diagnosis and cures.",
      "cropSelect": "Select Crop",
      "symptomsLabel": "Describe Observed Symptoms",
      "uploadPrompt": "Upload or Drop Leaf Photo",
      "diagnoseBtn": "🔬 Diagnose Disease with AI",
      "diagnosisResult": "Pathology Diagnosis & Treatment Plan"
    },
    "mandi": {
      "title": "Live Mandi Prices & Farm Economics",
      "subtitle": "Official e-NAM & APMC Mandi rates, price intelligence & farm profitability calculations",
      "tabMarket": "📈 Live Mandi Prices (e-NAM)",
      "tabCost": "💰 Farming Cost & Profit Estimator",
      "stateSelect": "Select State",
      "cropSelect": "Select Crop",
      "getPrices": "📊 Get Live Mandi Prices",
      "bestMandi": "🌾 Which mandi pays highest today?",
      "mspPrompt": "📜 What is Govt MSP for this crop?",
      "bestTime": "🗓️ When is the best time to sell?",
      "costCrop": "Crop Name",
      "costArea": "Farm Area (Acres)",
      "costSeason": "Season",
      "calcCost": "💰 Calculate Profit Estimate"
    },
    "schemes": {
      "title": "Government Schemes & Subsidies",
      "subtitle": "Official financial support, crop insurance, equipment subsidies & welfare programs",
      "tabNational": "🌟 Key National Schemes",
      "tabState": "📍 State Welfare Schemes",
      "tabEligibility": "🎯 Instant AI Eligibility Checker",
      "searchPlaceholder": "Search schemes by name or keyword...",
      "filterAll": "All Schemes",
      "checkBtn": "Check My Eligibility",
      "applyGuide": "How to Apply & Required Documents"
    },
    "voice": {
      "title": "AgriSense Multilingual Live Voice AI",
      "subtitle": "Speak naturally in your native language with your AI agricultural advisor.",
      "tabLive": "⚡ Gemini Live Audio Streaming (WebSocket)",
      "tabBrowser": "🎙️ Direct Browser Voice Assistant (Zero Setup)",
      "startBtn": "🎤 Start Speaking",
      "stopBtn": "⏹ Stop Session",
      "serverOnline": "🟢 Real-Time Server Online (Port 8000)",
      "serverOffline": "🔴 WebSocket Server Offline (Port 8000)",
      "transcriptTitle": "AI Response & Live Transcript",
      "tapMic": "Tap microphone and ask your farming question in"
    },
    "chat": {
      "title": "AI Agronomist Chat",
      "subtitle": "Instant farming advice personalized with your soil, weather, and ML recommendations.",
      "inputPlaceholder": "Ask AgriSense in your language (e.g., Best sowing time for cotton?)...",
      "quick1": "🌾 Best crop for my soil?",
      "quick2": "💧 When should I irrigate next?",
      "quick3": "🌿 Fertilizer dosage for my farm?",
      "clear": "Clear Chat",
      "micTooltip": "Speak your question in English",
      "listening": "Listening... speak now",
      "listenReply": "🔊 Read Aloud",
      "stopReply": "⏹ Stop Voice"
    },
    "help": {
      "title": "Farmer Help Center & Visual Guide",
      "subtitle": "Ultra-simple, icon-driven, voice-assisted guide designed for all farmers",
      "workflowTitle": "🚜 7-Step Simple Farming Workflow",
      "colorsTitle": "🎨 Color & Symbol Meaning Guide",
      "dosDontsTitle": "✅ Best Practices & ❌ Common Mistakes",
      "helplineTitle": "📞 Emergency Kisan Helpline"
    },
    "sensors": {
      "title": "IoT Sensor Hub & Telemetry",
      "subtitle": "Manage manual soil test reports and simulate live 7-in-1 IoT soil sensor broadcasts.",
      "manualTab": "📝 Manual Reading Entry",
      "iotTab": "📡 IoT Sensor Live Telemetry",
      "historyTab": "📊 Reading History Log",
      "saveBtn": "Save Farm Reading",
      "broadcastBtn": "📡 Broadcast IoT Packet Now"
    },
    "briefing": {
      "badge": "Daily 1-Min Audio Briefing",
      "title": "Today's Farm & Market Intelligence",
      "subtitle": "1-minute spoken briefing explaining your soil data, selected crop, live market price, and health advice.",
      "play": "▶️ Play 1-Min Briefing",
      "pause": "⏸ Pause",
      "stop": "⏹ Stop",
      "playing": "AgriSense AI Speaking in English",
      "updateToday": "📝 Update Today's Farm Data",
      "saving": "Saving Today's Reading...",
      "saved": "Today's farm reading updated!",
      "cropCardTitle": "Selected Crop",
      "mandiCardTitle": "Today's Mandi Price",
      "healthCardTitle": "Health & Protection",
      "tipCardTitle": "Tip of the Day",
      "transcriptTitle": "1-Minute Spoken Transcript",
      "audioSpeed": "Voice Speed",
      "quickCheckin": "Quick Daily Check-In",
      "saveTodayBtn": "Save Today's Reading"
    }
  },
  "తెలుగు": {
    "code": "te-IN",
    "appName": "అగ్రిసెన్స్ AI",
    "tagline": "స్మార్ట్ వ్యవసాయ సలహాదారు & నేల నిఘా వేదిక",
    "nav": {
      "dashboard": "డ్యాష్‌బోర్డ్",
      "crop": "పంట సిఫార్సు",
      "soil": "నేల ఆరోగ్యం",
      "irrigation": "నీటిపారుదల",
      "fertilizer": "ఎరువుల ప్రణాళిక",
      "disease": "తెగుళ్ల నివారణ",
      "mandi": "మండి ధరలు",
      "schemes": "ప్రభుత్వ పథకాలు",
      "voice": "వాయిస్ AI",
      "chat": "AI చాట్",
      "help": "సహాయ కేంద్రం",
      "sensors": "IoT సెన్సార్లు",
      "briefing": "1 నిమిషం అప్‌డేట్",
      "menu": "అన్ని విభాగాలు"
    },
    "login": {
      "title": "రైతు ప్రొఫైల్ లాగిన్",
      "subtitle": "మీ పొలం సమాచారం మరియు సలహాలు పొందడానికి మీ పేరు, ఫోన్ నంబర్ నమోదు చేయండి",
      "name": "రైతు పేరు",
      "phone": "10 అంకెల మొబైల్ నంబర్",
      "submit": "డ్యాష్‌బోర్డ్‌లోకి ప్రవేశించండి",
      "placeholderName": "ఉదా: రమేష్ కుమార్",
      "placeholderPhone": "ఉదా: 9876543210"
    },
    "dashboard": {
      "welcome": "స్వాగతం, రైతు సోదరా",
      "greeting": "ఈనాటి మీ పొలం నేల పరీక్ష వివరాలు మరియు వాతావరణ సమాచారం.",
      "weatherTitle": "ప్రస్తుత వాతావరణం",
      "weatherDesc": "పంట సాగు పనులకు అనుకూలమైన పరిస్థితులు",
      "soilScore": "నేల సారవంత స్కోరు",
      "iotStatus": "IoT సెన్సార్ స్థితి",
      "quickActions": "త్వరిత సేవలు",
      "recCrop": "సిఫార్సు చేయబడిన పంట",
      "waterStatus": "నేల తేమ శాతం",
      "optimal": "సరిపడా తేమ ఉంది",
      "needsWater": "నీరు పెట్టాలి",
      "viewDetails": "పూర్తి వివరాలు",
      "steps": {
        "step1": "1. నేల పరీక్ష",
        "step2": "2. పంట సిఫార్సు AI",
        "step3": "3. వ్యవసాయ సలహాలు"
      },
      "features": {
        "sensors": {
          "title": "దశ 1 — నేల పరీక్ష",
          "desc": "NPK, pH, తేమను నమోదు చేయండి లేదా ESP32 సెన్సార్ ద్వారా నేరుగా లైవ్ డేటా పొందండి.",
          "cta": "నేల పరీక్ష ప్రారంభించండి"
        },
        "crop": {
          "title": "దశ 2 — పంట సిఫార్సు AI",
          "desc": "మీ నేల మరియు వాతావరణం ఆధారంగా అత్యధిక దిగుబడినిచ్చే పంటను ML మోడల్ సిఫార్సు చేస్తుంది.",
          "cta": "పంట సిఫార్సు పొందండి"
        },
        "soil": {
          "title": "నేల ఆరోగ్య నివేదిక",
          "desc": "NPK పోషకాల సమతుల్యత, pH పరీక్ష మరియు నేల సారవంతం చేయడానికి సహజ ప్రణాళిక.",
          "cta": "నేల నివేదిక చూడండి"
        },
        "irrigation": {
          "title": "స్మార్ట్ నీటిపారుదల",
          "desc": "నేల తేమ ఆధారంగా మోటారు నడపాల్సిన సరైన సమయం మరియు నీటి అవసరాల లెక్కింపు.",
          "cta": "నీటిపారుదల సలహాదారు"
        },
        "fertilizer": {
          "title": "ఎరువుల ప్రణాళిక",
          "desc": "యూరియా, DAP, పొటాష్ ఎరువులను 4 దశల్లో వేయాల్సిన మోతాదు వివరాలు.",
          "cta": "ఎరువుల పట్టిక చూడండి"
        },
        "disease": {
          "title": "AI ప్లాంట్ డాక్టర్",
          "desc": "ఆకుల ఫోటో తీయండి లేదా లక్షణాలు వివరించండి — AI తక్షణమే నివారణ పద్ధతులను తెలుపుతుంది.",
          "cta": "ప్లాంట్ డాక్టర్ తెరవండి"
        },
        "mandi": {
          "title": "లైవ్ మార్కెట్ ధరలు",
          "desc": "e-NAM మరియు APMC మార్కెట్ ధరలు, MSP పోలిక మరియు వ్యవసాయ ఖర్చు-లాభాల లెక్కింపు.",
          "cta": "మార్కెట్ ధరలు చూడండి"
        },
        "schemes": {
          "title": "ప్రభుత్వ పథకాలు",
          "desc": "PM-కిసాన్, PM-కుసుమ్ సౌర పంపులు, పంటల బీమా మరియు రైతు రుణ పథకాలు.",
          "cta": "పథకాలు బ్రౌజ్ చేయండి"
        },
        "voice": {
          "title": "వాయిస్ AI అసిస్టెంట్",
          "desc": "మీ స్వంత తెలుగు భాషలో మాట్లాడండి — AgriSense AI తక్షణమే సమాధానం ఇస్తుంది.",
          "cta": "వాయిస్‌తో మాట్లాడండి"
        },
        "chat": {
          "title": "AI చాట్ అసిస్టెంట్",
          "desc": "మీ వ్యవసాయ సందేహాలను తెలుగులో అడగండి, మీ పొలం డేటాతో తగిన సలహాలు పొందండి.",
          "cta": "చాట్ ప్రారంభించండి"
        },
        "help": {
          "title": "రైతు సహాయ కేంద్రం",
          "desc": "7 దశల గైడ్, సూచనలు మరియు కిసాన్ కాల్ సెంటర్ 1551 సమాచారం.",
          "cta": "సహాయ కేంద్రం తెరవండి"
        }
      }
    },
    "crop": {
      "title": "ML ఆధారిత పంట సిఫార్సు",
      "subtitle": "మీ నేల NPK మరియు వాతావరణ పరిస్థితుల ఆధారంగా అత్యధిక దిగుబడినిచ్చే పంటను ఎంపిక చేస్తుంది.",
      "nitrogen": "నత్రజని (N)",
      "phosphorus": "భాస్వరం (P)",
      "potassium": "పొటాషియం (K)",
      "temp": "ఉష్ణోగ్రత (°C)",
      "humidity": "గాలిలో తేమ (%)",
      "ph": "నేల pH విలువ",
      "rainfall": "వర్షపాతం (మి.మీ)",
      "predictBtn": "🌱 సరైన పంటను కనుగొనండి",
      "useLatest": "⚡ సెన్సార్ డేటా ఉపయోగించండి",
      "resultTitle": "మీ పొలానికి అనువైన పంట",
      "suitability": "అనుకూలత స్కోరు",
      "packageOfPractice": "సాగు పద్ధతులు & మెళకువలు"
    },
    "soil": {
      "title": "నేల ఆరోగ్యం & పోషకాల సమతుల్యత",
      "subtitle": "NPK పోషక స్థాయిలు మరియు నేల pH సమతుల్యత విశ్లేషణ.",
      "npkRatio": "ప్రస్తుత NPK నిష్పత్తి",
      "idealRatio": "ఆదర్శ నిష్పత్తి (4:2:1)",
      "organicCarbon": "సేంద్రియ కర్బనం",
      "phStatus": "నేల స్వభావం (pH)",
      "recommendations": "నేల అభివృద్ధి సూచనలు"
    },
    "irrigation": {
      "title": "స్మార్ట్ నీటిపారుదల సలహాదారు",
      "subtitle": "నేల తేమ శాతం ఆధారంగా పంటకు ఎప్పుడు ఎంత నీరు పెట్టాలో తెలియజేస్తుంది.",
      "moistureGauge": "వేరు మండలంలో తేమ శాతం",
      "schedule": "నీటిపారుదల సమయ పట్టిక",
      "waterReq": "అవసరమైన నీటి పరిమాణం",
      "calcBtn": "నీటి అవసరాన్ని లెక్కించండి"
    },
    "fertilizer": {
      "title": "ఎరువుల మోతాదు కాలిక్యులేటర్",
      "subtitle": "పంటకు అవసరమైన సేంద్రియ మరియు రసాయన ఎరువుల ఖచ్చితమైన పరిమాణం.",
      "targetCrop": "సాగు చేసే పంట",
      "landSize": "పొలం విస్తీర్ణం (ఎకరాలు)",
      "calcBtn": "ఎరువుల పట్టికను రూపొందించండి",
      "organicPlan": "సేంద్రియ ఎరువుల ప్రణాళిక",
      "chemicalPlan": "రసాయన ఎరువుల మోతాదు"
    },
    "disease": {
      "title": "AI ప్లాంట్ డాక్టర్ - పంట తెగుళ్లు",
      "subtitle": "ఆకు ఫోటో తీసి అప్‌లోడ్ చేస్తే AI తెగుళ్లను గుర్తించి సరైన నివారణలను సూచిస్తుంది.",
      "cropSelect": "పంటను ఎంచుకోండి",
      "symptomsLabel": "కనిపిస్తున్న లక్షణాలు వివరించండి",
      "uploadPrompt": "ఆకు ఫోటోను ఇక్కడ అప్‌లోడ్ చేయండి",
      "diagnoseBtn": "🔬 AI తో తెగులును గుర్తించండి",
      "diagnosisResult": "రోగ నిర్ధారణ & నివారణ పద్ధతులు"
    },
    "mandi": {
      "title": "లైవ్ మండి ధరలు & వ్యవసాయ వ్యయ అంచనా",
      "subtitle": "అధికారిక e-NAM & APMC మండి ధరలు, మార్కెట్ సమాచారం & లాభాల గణన",
      "tabMarket": "📈 లైవ్ మండి ధరలు (Mandi Bhav)",
      "tabCost": "💰 వ్యవసాయ వ్యయ & లాభ అంచనా",
      "stateSelect": "రాష్ట్రం ఎంచుకోండి",
      "cropSelect": "పంట ఎంచుకోండి",
      "getPrices": "📊 మండి ధరలు చూడండి",
      "bestMandi": "🌾 ఏ మండీలో ఎక్కువ రేటు వస్తుంది?",
      "mspPrompt": "📜 ఈ పంటకు ప్రభుత్వ మద్దతు ధర (MSP) ఎంత?",
      "bestTime": "🗓️ పంటను అమ్మడానికి ఉత్తమ సమయం ఏది?",
      "costCrop": "పంట పేరు",
      "costArea": "పొలం విస్తీర్ణం (ఎకరాలు)",
      "costSeason": "సీజన్",
      "calcCost": "💰 లాభం లెక్కించండి"
    },
    "schemes": {
      "title": "ప్రభుత్వ పథకాలు & సబ్సిడీలు",
      "subtitle": "రైతుల కోసం అధికారిక ఆర్థిక సహాయం, పంట బీమా, పరికరాల సబ్సిడీలు & సంక్షేమ పథకాలు",
      "tabNational": "🌟 ప్రధాన జాతీయ పథకాలు",
      "tabState": "📍 రాష్ట్ర సంక్షేమ పథకాలు",
      "tabEligibility": "🎯 తక్షణ AI అర్హత తనిఖీ",
      "searchPlaceholder": "పథకం పేరు లేదా కీవర్డ్ తో శోధించండి...",
      "filterAll": "అన్ని పథకాలు",
      "checkBtn": "నా అర్హత తనిఖీ చేయండి",
      "applyGuide": "దరఖాస్తు విధానం & పత్రాలు"
    },
    "voice": {
      "title": "అగ్రిసెన్స్ తెలుగు లైవ్ వాయిస్ AI",
      "subtitle": "మీ వ్యవసాయ సమస్యలను సహజంగా మాట్లాడి అడగండి.",
      "tabLive": "⚡ జెమిని లైవ్ స్ట్రీమింగ్ (WebSocket)",
      "tabBrowser": "🎙️ బ్రౌజర్ వాయిస్ అసిస్టెంట్ (తక్షణ స్పందన)",
      "startBtn": "🎤 మాట్లాడటం ప్రారంభించండి",
      "stopBtn": "⏹ ఆపండి",
      "serverOnline": "🟢 లైవ్ సర్వర్ ఆన్‌లైన్‌లో ఉంది",
      "serverOffline": "🔴 లైవ్ సర్వర్ ఆఫ్‌లైన్ (పోర్ట్ 8000)",
      "transcriptTitle": "AI సమాధానం & సంభాషణ",
      "tapMic": "మైక్రోఫోన్ నొక్కి మీ ప్రశ్నను తెలుగులో అడగండి"
    },
    "chat": {
      "title": "AI వ్యవసాయ నిపుణుడి చాట్",
      "subtitle": "మీ పొలం వివరాలతో కూడిన వ్యక్తిగత వ్యవసాయ సలహాలు.",
      "inputPlaceholder": "మీ వ్యవసాయ ప్రశ్నను ఇక్కడ అడగండి (ఉదా: పత్తికి యూరియా ఎప్పుడు వేయాలి?)...",
      "quick1": "🌾 నా పొలానికి ఏ పంట మంచిది?",
      "quick2": "💧 తదుపరి నీరు ఎప్పుడు పెట్టాలి?",
      "quick3": "🌿 సరైన ఎరువుల మోతాదు ఎంత?",
      "clear": "చాట్ క్లియర్ చేయండి",
      "micTooltip": "తెలుగులో మాట్లాడటానికి మైక్ నొక్కండి",
      "listening": "వింటోంది... మాట్లాడండి",
      "listenReply": "🔊 చదివి వినిపించు",
      "stopReply": "⏹ ఆపండి"
    },
    "help": {
      "title": "రైతు సహాయ కేంద్రం & గైడ్",
      "subtitle": "రైతుల కోసం సులభమైన బొమ్మలు మరియు వాయిస్ సహాయంతో కూడిన గైడ్",
      "workflowTitle": "🚜 7-దశల సులభ వ్యవసాయ విధానం",
      "colorsTitle": "🎨 రంగులు & చిహ్నాల వివరణ",
      "dosDontsTitle": "✅ చేయవలసినవి & ❌ చేయకూడనివి",
      "helplineTitle": "📞 కిసాన్ టోల్ ఫ్రీ హెల్ప్‌లైన్"
    },
    "sensors": {
      "title": "IoT నేల సెన్సార్లు & డేటా హబ్",
      "subtitle": "మాన్యువల్ డేటా నమోదు మరియు లైవ్ 7-ఇన్-1 IoT సెన్సార్ డేటా పంపే విధానం.",
      "manualTab": "📝 మాన్యువల్ ఎంట్రీ",
      "iotTab": "📡 IoT సెన్సార్ లైవ్ టెలిమెట్రీ",
      "historyTab": "📊 గత రీడింగుల చరిత్ర",
      "saveBtn": "సమాచారాన్ని సేవ్ చేయండి",
      "broadcastBtn": "📡 IoT డేటాను పంపండి"
    },
    "briefing": {
      "badge": "రోజువారీ 1 నిమిషం ఆడియో అప్‌డేట్",
      "title": "నేటి వ్యవసాయ & మార్కెట్ సమాచారం",
      "subtitle": "మీ నేల సమాచారం, ఎంపిక పంట, మార్కెట్ ధర మరియు పంట రక్షణ సలహాలను 1 నిమిషంలో వివరించే ఆడియో.",
      "play": "▶️ 1 నిమిషం అప్‌డేట్ వినండి",
      "pause": "⏸ ఆపండి",
      "stop": "⏹ ముగించు",
      "playing": "AgriSense AI తెలుగులో మాట్లాడుతోంది",
      "updateToday": "📝 నేటి డేటా నమోదు చేయండి",
      "saving": "భద్రపరుస్తోంది...",
      "saved": "నేటి డేటా విజయవంతంగా నమోదైంది!",
      "cropCardTitle": "ఎంపిక చేసిన పంట",
      "mandiCardTitle": "నేటి మార్కెట్ ధర",
      "healthCardTitle": "పంట రక్షణ & ఆరోగ్యం",
      "tipCardTitle": "నేటి వ్యవసాయ సలహా",
      "transcriptTitle": "1 నిమిషం పూర్తి పాఠం",
      "audioSpeed": "స్పీచ్ వేగం",
      "quickCheckin": "నేటి త్వరిత నమోదు",
      "saveTodayBtn": "నేటి రీడింగ్ భద్రపరచు"
    }
  },
  "हिंदी": {
    "code": "hi-IN",
    "appName": "एग्रीसेंस AI",
    "tagline": "स्मार्ट कृषि निर्णय सहायता और खेत की बुद्धिमत्ता",
    "nav": {
      "dashboard": "डैशबोर्ड",
      "crop": "फसल सिफारिश",
      "soil": "मृदा स्वास्थ्य",
      "irrigation": "सिंचाई सलाह",
      "fertilizer": "खाद योजना",
      "disease": "पौधा डॉक्टर",
      "mandi": "मंडी भाव",
      "schemes": "सरकारी योजनाएं",
      "voice": "वॉयस AI",
      "chat": "AI चैट",
      "help": "सहायता केंद्र",
      "sensors": "IoT सेंसर",
      "briefing": "1 मिनट अपडेट",
      "menu": "सभी सुविधाएं"
    },
    "login": {
      "title": "किसान प्रोफाइल लॉगिन",
      "subtitle": "अपनी व्यक्तिगत कृषि जानकारी के लिए नाम और मोबाइल नंबर दर्ज करें",
      "name": "किसान का नाम",
      "phone": "10 अंकों का मोबाइल नंबर",
      "submit": "डैशबोर्ड खोलें",
      "placeholderName": "उदा: रमेश कुमार",
      "placeholderPhone": "उदा: 9876543210"
    },
    "dashboard": {
      "welcome": "स्वागत है, किसान साथी",
      "greeting": "यहाँ आपके खेत की मिट्टी और मौसम का ताज़ा विवरण है।",
      "weatherTitle": "वर्तमान मौसम",
      "weatherDesc": "खेती के कार्यों के लिए अनुकूल मौसम",
      "soilScore": "मृदा उर्वरता स्कोर",
      "iotStatus": "IoT सेंसर स्थिति",
      "quickActions": "त्वरित सेवाएं",
      "recCrop": "अनुशंसित फसल",
      "waterStatus": "मिट्टी में नमी",
      "optimal": "पर्याप्त नमी",
      "needsWater": "सिंचाई की आवश्यकता",
      "viewDetails": "पूरी जानकारी",
      "steps": {
        "step1": "1. मिट्टी परीक्षण",
        "step2": "2. फसल चयन AI",
        "step3": "3. कृषि सलाह व अर्थशास्त्र"
      },
      "features": {
        "sensors": {
          "title": "चरण 1 — मिट्टी परीक्षण",
          "desc": "NPK, pH और नमी मैन्युअल दर्ज करें या 7-इन-1 IoT सेंसर से सीधा डेटा लें।",
          "cta": "मिट्टी परीक्षण शुरू करें"
        },
        "crop": {
          "title": "चरण 2 — फसल अनुशंसा AI",
          "desc": "आपकी मिट्टी व मौसम के अनुसार सर्वोत्तम उपज वाली फसल का सटीक सुझाव।",
          "cta": "फसल सुझाव प्राप्त करें"
        },
        "soil": {
          "title": "मृदा स्वास्थ्य रिपोर्ट",
          "desc": "NPK पोषक तत्वों का विश्लेषण, pH स्थिति और जैविक सुधार योजना।",
          "cta": "मृदा रिपोर्ट देखें"
        },
        "irrigation": {
          "title": "स्मार्ट सिंचाई सलाहकार",
          "desc": "मिट्टी की नमी के आधार पर मोटर चलाने का सटीक समय और पानी की मात्रा।",
          "cta": "सिंचाई योजना देखें"
        },
        "fertilizer": {
          "title": "उर्वरक खुराक कैलकुलेटर",
          "desc": "यूरिया, डीएपी, एमओपी की 4 विकास चरणों में सही मात्रा व लागत बचत।",
          "cta": "उर्वरक चार्ट देखें"
        },
        "disease": {
          "title": "AI प्लांट डॉक्टर",
          "desc": "पत्ती की फोटो खींचें या लक्षण बताएं — तुरंत जैविक व रासायनिक उपचार पाएं।",
          "cta": "प्लांट डॉक्टर खोलें"
        },
        "mandi": {
          "title": "लाइव मंडी भाव",
          "desc": "e-NAM व APMC दरें, एमएसपी तुलना और खेती की लागत-लाभ का सटीक हिसाब।",
          "cta": "मंडी भाव देखें"
        },
        "schemes": {
          "title": "सरकारी योजनाएं",
          "desc": "पीएम-किसान, पीएम-कुसुम सोलर पंप, फसल बीमा और किसान क्रेडिट कार्ड।",
          "cta": "योजनाएं देखें"
        },
        "voice": {
          "title": "वॉइस AI सहायक",
          "desc": "अपनी हिंदी भाषा में बोलें — AgriSense AI बोलकर उत्तर देगा।",
          "cta": "वॉइस AI से बात करें"
        },
        "chat": {
          "title": "AI चैट सलाहकार",
          "desc": "खेती से जुड़ा कोई भी सवाल पूछें, आपके खेत के अनुसार सही जवाब मिलेगा।",
          "cta": "AI चैट खोलें"
        },
        "help": {
          "title": "किसान सहायता केंद्र",
          "desc": "7-चरणीय गाइड, रंग संकेत और टोल-फ्री किसान हेल्पलाइन 1551।",
          "cta": "मार्गदर्शिका देखें"
        }
      }
    },
    "crop": {
      "title": "ML आधारित फसल सिफारिश",
      "subtitle": "आपकी मिट्टी और जलवायु के आधार पर सबसे अधिक उपज देने वाली फसल।",
      "nitrogen": "नाइट्रोजन (N)",
      "phosphorus": "फास्फोरस (P)",
      "potassium": "पोटैशियम (K)",
      "temp": "तापमान (°C)",
      "humidity": "नमी (%)",
      "ph": "मिट्टी का pH",
      "rainfall": "वर्षा (मिमी)",
      "predictBtn": "🌱 सही फसल चुनें",
      "useLatest": "⚡ सेंसर डेटा का उपयोग करें",
      "resultTitle": "आपके लिए अनुशंसित फसल",
      "suitability": "उपयुक्तता स्कोर",
      "packageOfPractice": "बुवाई और देखभाल के दिशा-निर्देश"
    },
    "soil": {
      "title": "मृदा स्वास्थ्य और पोषण संतुलन",
      "subtitle": "NPK पोषण स्तर और मिट्टी के pH का संपूर्ण विश्लेषण।",
      "npkRatio": "वर्तमान NPK अनुपात",
      "idealRatio": "आदर्श अनुपात (4:2:1)",
      "organicCarbon": "जैविक कार्बन",
      "phStatus": "मिट्टी का pH स्तर",
      "recommendations": "मिट्टी सुधार के सुझाव"
    },
    "irrigation": {
      "title": "सटीक सिंचाई सलाहकार",
      "subtitle": "मिट्टी की नमी के अनुसार पानी देने का सही समय और मात्रा।",
      "moistureGauge": "जड़ क्षेत्र में नमी",
      "schedule": "सिंचाई समय सारणी",
      "waterReq": "आवश्यक पानी की मात्रा",
      "calcBtn": "पानी की आवश्यकता मापें"
    },
    "fertilizer": {
      "title": "खाद मात्रा कैलकुलेटर",
      "subtitle": "फसल के लिए आवश्यक जैविक और रासायनिक खाद की सटीक मात्रा।",
      "targetCrop": "बोई जाने वाली फसल",
      "landSize": "खेत का आकार (एकड़)",
      "calcBtn": "खाद योजना बनाएं",
      "organicPlan": "जैविक खाद योजना",
      "chemicalPlan": "रासायनिक खाद की मात्रा"
    },
    "disease": {
      "title": "AI पौधा डॉक्टर - फसल रोग",
      "subtitle": "पत्ती की फोटो खींचें और तुरंत रोग निदान और उपचार पाएं।",
      "cropSelect": "फसल चुनें",
      "symptomsLabel": "दिखने वाले लक्षण बताएं",
      "uploadPrompt": "पत्ती की फोटो अपलोड करें",
      "diagnoseBtn": "🔬 AI से रोग पहचानें",
      "diagnosisResult": "रोग निदान और उपचार योजना"
    },
    "mandi": {
      "title": "लाइव मंडी भाव और खेती लागत अनुमान",
      "subtitle": "आधिकारिक e-NAM और APMC मंडी दरें, भाव रुझान और मुनाफा कैलकुलेटर",
      "tabMarket": "📈 लाइव मंडी भाव (e-NAM)",
      "tabCost": "💰 खेती लागत और मुनाफा कैलकुलेटर",
      "stateSelect": "राज्य चुनें",
      "cropSelect": "फसल चुनें",
      "getPrices": "📊 मंडी भाव देखें",
      "bestMandi": "🌾 आज किस मंडी में सबसे ज्यादा भाव है?",
      "mspPrompt": "📜 इस फसल का सरकारी MSP क्या है?",
      "bestTime": "🗓️ फसल बेचने का सबसे सही समय कब है?",
      "costCrop": "फसल का नाम",
      "costArea": "खेत का क्षेत्रफल (एकड़)",
      "costSeason": "मौसम",
      "calcCost": "💰 मुनाफे का अनुमान लगाएं"
    },
    "schemes": {
      "title": "सरकारी योजनाएं और सब्सिडी",
      "subtitle": "भारतीय किसानों के लिए आधिकारिक वित्तीय सहायता, फसल बीमा और अनुदान",
      "tabNational": "🌟 प्रमुख राष्ट्रीय योजनाएं",
      "tabState": "📍 राज्य कल्याणकारी योजनाएं",
      "tabEligibility": "🎯 तत्काल AI पात्रता चेकर",
      "searchPlaceholder": "योजना का नाम या कीवर्ड खोजें...",
      "filterAll": "सभी योजनाएं",
      "checkBtn": "मेरी पात्रता जांचें",
      "applyGuide": "आवेदन प्रक्रिया और आवश्यक दस्तावेज"
    },
    "voice": {
      "title": "एग्रीसेंस हिंदी लाइव वॉयस AI",
      "subtitle": "अपनी मातृभाषा में बोलकर कृषि संबंधी सलाह लें।",
      "tabLive": "⚡ जेमिनी लाइव स्ट्रीमिंग (WebSocket)",
      "tabBrowser": "🎙️ सीधा वॉयस असिस्टेंट",
      "startBtn": "🎤 बोलना शुरू करें",
      "stopBtn": "⏹ बंद करें",
      "serverOnline": "🟢 लाइव सर्वर चालू है (Port 8000)",
      "serverOffline": "🔴 सर्वर बंद है",
      "transcriptTitle": "AI का उत्तर और बातचीत",
      "tapMic": "माइक दबाएं और हिंदी में अपना प्रश्न पूछें"
    },
    "chat": {
      "title": "AI कृषि विशेषज्ञ चैट",
      "subtitle": "आपके खेत के डेटा के साथ व्यक्तिगत कृषि मार्गदर्शन।",
      "inputPlaceholder": "हिंदी में प्रश्न पूछें (उदा: गेहूं में पहली सिंचाई कब करें?)...",
      "quick1": "🌾 मेरे खेत के लिए कौन सी फसल सही है?",
      "quick2": "💧 अगली सिंचाई कब करनी चाहिए?",
      "quick3": "🌿 खाद की सही मात्रा क्या है?",
      "clear": "चैट साफ करें",
      "micTooltip": "हिंदी में बोलने के लिए माइक दबाएं",
      "listening": "सुन रहा है... बोलिए",
      "listenReply": "🔊 बोलकर सुनाएं",
      "stopReply": "⏹ आवाज रोकें"
    },
    "help": {
      "title": "किसान सहायता केंद्र व मार्गदर्शिका",
      "subtitle": "चित्रों और बोलकर समझाने वाली सरल मार्गदर्शिका",
      "workflowTitle": "🚜 7-चरणों की सरल खेती कार्यप्रणाली",
      "colorsTitle": "🎨 रंग और प्रतीकों का अर्थ",
      "dosDontsTitle": "✅ क्या करें और ❌ क्या न करें",
      "helplineTitle": "📞 किसान हेल्पलाइन"
    },
    "sensors": {
      "title": "IoT मृदा सेंसर और डेटा हब",
      "subtitle": "मैन्युअल प्रविष्टि और 7-इन-1 IoT सेंसर डेटा प्रसारण।",
      "manualTab": "📝 मैन्युअल प्रविष्टि",
      "iotTab": "📡 लाइव सेंसर डेटा",
      "historyTab": "📊 पिछला रिकॉर्ड",
      "saveBtn": "डेटा सुरक्षित करें",
      "broadcastBtn": "📡 डेटा भेजें"
    },
    "briefing": {
      "badge": "दैनिक 1 मिनट ऑडियो ब्रीफिंग",
      "title": "आज की कृषि व मंडी जानकारी",
      "subtitle": "आपकी मिट्टी की नमी, चुनी हुई फसल, लाइव मंडी भाव और फसल सुरक्षा की 1 मिनट की ऑडियो रिपोर्ट।",
      "play": "▶️ 1 मिनट ब्रीफिंग सुनें",
      "pause": "⏸ रोकें",
      "stop": "⏹ समाप्त",
      "playing": "AgriSense AI हिंदी में बोल रहा है",
      "updateToday": "📝 आज का डेटा दर्ज करें",
      "saving": "सहेज रहा है...",
      "saved": "आज का डेटा दर्ज हो गया!",
      "cropCardTitle": "चुनी हुई फसल",
      "mandiCardTitle": "आज का मंडी भाव",
      "healthCardTitle": "फसल सुरक्षा निर्देश",
      "tipCardTitle": "आज की उपयोगी सलाह",
      "transcriptTitle": "1 मिनट का पूरा विवरण",
      "audioSpeed": "आवाज की गति",
      "quickCheckin": "दैनिक त्वरित चेक-इन",
      "saveTodayBtn": "आज का डेटा सहेजें"
    }
  },
  "தமிழ்": {
    "code": "ta-IN",
    "appName": "அக்ரிசென்ஸ் AI",
    "tagline": "ஸ்மார்ட் விவசாய வழிகாட்டி & மண் வள தளம்",
    "nav": {
      "dashboard": "டாஷ்போர்டு",
      "crop": "பயிர் பரிந்துரை",
      "soil": "மண் வளம்",
      "irrigation": "பாசனம்",
      "fertilizer": "உர திட்டம்",
      "disease": "தாவர மருத்துவர்",
      "mandi": "மண்டி விலைகள்",
      "schemes": "அரசு திட்டங்கள்",
      "voice": "குரல் AI",
      "chat": "AI உரையாடல்",
      "help": "உதவி மையம்",
      "sensors": "IoT சென்சார்கள்",
      "briefing": "1 நிமிட அறிக்கை",
      "menu": "அனைத்து சேவைகள்"
    },
    "login": {
      "title": "விவசாயி உள்நுழைவு",
      "subtitle": "உங்கள் பண்ணை விவரங்களைப் பெற பெயர் மற்றும் கைபேசி எண்ணை உள்ளிடவும்",
      "name": "விவசாயி பெயர்",
      "phone": "10 இலக்க கைபேசி எண்",
      "submit": "உள்நுழையவும்",
      "placeholderName": "उदा: கார்த்திக்",
      "placeholderPhone": "उदा: 9876543210"
    },
    "dashboard": {
      "welcome": "வணக்கம், விவசாயி தோழரே",
      "greeting": "இன்றைய பண்ணை மண் பரிசோதனை மற்றும் வானிலை விவரங்கள்.",
      "weatherTitle": "தற்போதைய வானிலை",
      "weatherDesc": "விவசாய பணிகளுக்கு ஏற்ற சூழல்",
      "soilScore": "மண் வள மதிப்பெண்",
      "iotStatus": "IoT சென்சார் நிலை",
      "quickActions": "விரைவு சேவைகள்",
      "recCrop": "பரிந்துரைக்கப்பட்ட பயிர்",
      "waterStatus": "மண் ஈரப்பதம்",
      "optimal": "போதுமான ஈரப்பதம்",
      "needsWater": "தண்ணீர் பாய்ச்ச வேண்டும்",
      "viewDetails": "முழு விவரங்கள்",
      "steps": {
        "step1": "1. மண் பரிசோதனை",
        "step2": "2. பயிர் பரிந்துரை AI",
        "step3": "3. வேளாண் வழிகாட்டல்"
      },
      "features": {
        "sensors": {
          "title": "படி 1 — மண் பரிசோதனை",
          "desc": "NPK, pH, ஈரப்பதத்தை பதிவு செய்யவும் அல்லது IoT சென்சார் மூலம் நேரடி தரவு பெறவும்.",
          "cta": "மண் பரிசோதனை செய்க"
        },
        "crop": {
          "title": "படி 2 — பயிர் பரிந்துரை AI",
          "desc": "மண் மற்றும் காலநிலைக்கு ஏற்ற அதிக மகசூல் தரும் பயிரை கண்டறியவும்.",
          "cta": "பயிர் பரிந்துரை பெறுக"
        },
        "soil": {
          "title": "மண் வள அறிக்கை",
          "desc": "NPK ஊட்டச்சத்து விகிதம் மற்றும் இயற்கை உர பரிந்துரை திட்டம்.",
          "cta": "மண் அறிக்கை காண்க"
        },
        "irrigation": {
          "title": "துல்லிய பாசனம்",
          "desc": "மண் ஈரப்பதத்திற்கு ஏற்ப நீர் பாய்ச்சும் நேரம் கணக்கீடு.",
          "cta": "பாசன திட்டம் காண்க"
        },
        "fertilizer": {
          "title": "உர கணக்கீடு",
          "desc": "யூரியா, டிஏபி, பொட்டாஷ் உரங்களின் 4 பருவ அளவுகள்.",
          "cta": "உர அட்டவணை காண்க"
        },
        "disease": {
          "title": "AI பயிர் மருத்துவர்",
          "desc": "இலை புகைப்படத்தை பதிவேற்றி உடனடியாக நோயறிதல் மற்றும் தீர்வு பெறவும்.",
          "cta": "மருத்துவரை காண்க"
        },
        "mandi": {
          "title": "நேரடி சந்தை விலை",
          "desc": "e-NAM APMC விலை மற்றும் பண்ணை வரவு-செலவு கணக்கீடு.",
          "cta": "சந்தை விலை காண்க"
        },
        "schemes": {
          "title": "அரசு திட்டங்கள்",
          "desc": "பிஎம்-கிசான், சூரிய மின் பம்பு, பயிர் காப்பீட்டு திட்டங்கள்.",
          "cta": "திட்டங்களை காண்க"
        },
        "voice": {
          "title": "குரல் AI உதவியாளர்",
          "desc": "தமிழில் பேசுங்கள் — AgriSense AI தமிழில் குரலில் பதிலளிக்கும்.",
          "cta": "தமிழில் பேசுக"
        },
        "chat": {
          "title": "AI சாட் உதவியாளர்",
          "desc": "விவசாய கேள்விகளை தமிழில் கேட்டு பண்ணைக்கேற்ற ஆலோசனை பெறுக.",
          "cta": "சாட் செய்க"
        },
        "help": {
          "title": "உதவி மையம்",
          "desc": "7 படி வழிகாட்டி மற்றும் அவசர உழவர் உதவி எண் 1551.",
          "cta": "உதவி மையம் காண்க"
        }
      }
    },
    "crop": {
      "title": "ML பயிர் பரிந்துரை",
      "subtitle": "உங்கள் மண் மற்றும் வானிலை அடிப்படையில் அதிக மகசூல் தரும் பயிர்.",
      "nitrogen": "நைட்ரஜன் (N)",
      "phosphorus": "பாஸ்பரஸ் (P)",
      "potassium": "பொட்டாசியம் (K)",
      "temp": "வெப்பநிலை (°C)",
      "humidity": "ஈரப்பதம் (%)",
      "ph": "மண் pH",
      "rainfall": "மழைப்பொழிவு (மி.மீ)",
      "predictBtn": "🌱 சிறந்த பயிரைக் கண்டறியவும்",
      "useLatest": "⚡ சென்சார் தரவைப் பயன்படுத்தவும்",
      "resultTitle": "பரிந்துரைக்கப்பட்ட பயிர்",
      "suitability": "பொருத்த மதிப்பெண்",
      "packageOfPractice": "சாகுபடி வழிகாட்டி"
    },
    "soil": {
      "title": "மண் வளம் மற்றும் ஊட்டச்சத்து சமநிலை",
      "subtitle": "NPK மற்றும் pH ஊட்டச்சத்து பகுப்பாய்வு.",
      "npkRatio": "தற்போதைய NPK விகிதம்",
      "idealRatio": "சரியான விகிதம் (4:2:1)",
      "organicCarbon": "கரிம கார்பன்",
      "phStatus": "மண் pH நிலை",
      "recommendations": "மண் மேம்பாட்டு ஆலோசனைகள்"
    },
    "irrigation": {
      "title": "துல்லிய பாசன ஆலோசகர்",
      "subtitle": "மண் ஈரப்பதத்திற்கு ஏற்ப பாசன திட்டமிடல்.",
      "moistureGauge": "வேர் பகுதி ஈரப்பதம்",
      "schedule": "பாசன கால அட்டவணை",
      "waterReq": "தேவையான நீர் அளவு",
      "calcBtn": "நீர்த் தேவையை கணக்கிடுங்கள்"
    },
    "fertilizer": {
      "title": "உர அளவு கால்குலேட்டர்",
      "subtitle": "பயிருக்கான சரியான உரம் மற்றும் இயற்கை உரம் அளவு.",
      "targetCrop": "பயிர்",
      "landSize": "பண்ணை அளவு (ஏக்கர்)",
      "calcBtn": "உர அட்டவணை உருவாக்கு",
      "organicPlan": "இயற்கை உர திட்டம்",
      "chemicalPlan": "ரசாயன உர அளவு"
    },
    "disease": {
      "title": "AI தாவர மருத்துவர் - நோய் கண்டறிதல்",
      "subtitle": "இலை புகைப்படத்தை பதிவேற்றி நோயைக் கண்டறிந்து தீர்வு பெறுங்கள்.",
      "cropSelect": "பயிரைத் தேர்ந்தெடுக்கவும்",
      "symptomsLabel": "அறிகுறிகள்",
      "uploadPrompt": "இலை புகைப்படத்தைப் பதிவேற்றவும்",
      "diagnoseBtn": "🔬 நோயைக் கண்டறியவும்",
      "diagnosisResult": "நோய் அறிதல் & சிகிச்சை திட்டம்"
    },
    "mandi": {
      "title": "நேரலை மண்டி விலைகள் & பண்ணை செலவு",
      "subtitle": "e-NAM மற்றும் APMC மண்டி விலைகள், சந்தை விவரம் மற்றும் லாப கால்குலேட்டர்",
      "tabMarket": "📈 நேரலை மண்டி விலைகள்",
      "tabCost": "💰 பண்ணை செலவு & லாப மதிப்பீடு",
      "stateSelect": "மாநிலம்",
      "cropSelect": "பயிர்",
      "getPrices": "📊 மண்டி விலைகளைக் காண்க",
      "bestMandi": "🌾 இன்று எந்த மண்டியில் அதிக விலை?",
      "mspPrompt": "📜 இந்த பயிருக்கான அரசு MSP விலை என்ன?",
      "bestTime": "🗓️ விற்க சிறந்த நேரம் எது?",
      "costCrop": "பயிர் பெயர்",
      "costArea": "பண்ணை பரப்பளவு (ஏக்கர்)",
      "costSeason": "பருவம்",
      "calcCost": "💰 லாபத்தை கணக்கிடுங்கள்"
    },
    "schemes": {
      "title": "அரசு திட்டங்கள் மற்றும் மானியங்கள்",
      "subtitle": "விவசாயிகளுக்கான நேரடி பண உதவி, பயிர் காப்பீடு மற்றும் நலத்திட்டங்கள்",
      "tabNational": "🌟 முதன்மை தேசிய திட்டங்கள்",
      "tabState": "📍 மாநில நலத்திட்டங்கள்",
      "tabEligibility": "🎯 உடனடி AI தகுதி சரிபார்ப்பு",
      "searchPlaceholder": "திட்டத்தின் பெயர் கொண்டு தேடவும்...",
      "filterAll": "அனைத்து திட்டங்கள்",
      "checkBtn": "என் தகுதியை சரிபார்க்கவும்",
      "applyGuide": "விண்ணப்பிக்கும் முறை மற்றும் ஆவணங்கள்"
    },
    "voice": {
      "title": "அக்ரிசென்ஸ் தமிழ் குரல் AI",
      "subtitle": "தமிழில் பேசி விவசாய ஆலோசனை பெறுங்கள்.",
      "tabLive": "⚡ ஜெமினி லைவ் ஸ்ட்ரீமிங்",
      "tabBrowser": "🎙️ பிரவுசர் குரல் உதவியாளர்",
      "startBtn": "🎤 பேசத் தொடங்குங்கள்",
      "stopBtn": "⏹ நிறுத்து",
      "serverOnline": "🟢 சர்வர் செயலில் உள்ளது",
      "serverOffline": "🔴 சர்வர் முடங்கியுள்ளது",
      "transcriptTitle": "AI பதில் & உரையாடல்",
      "tapMic": "மைக் அழுத்தி தமிழில் கேள்வி கேட்கவும்"
    },
    "chat": {
      "title": "AI விவசாய நிபுணர்",
      "subtitle": "உங்கள் பண்ணை விவரங்களுடன் கூடிய உடனடி ஆலோசனை.",
      "inputPlaceholder": "தமிழில் கேள்வி கேளுங்கள்...",
      "quick1": "🌾 என் நிலத்திற்கு எந்த பயிர் ஏற்றது?",
      "quick2": "💧 அடுத்த பாசனம் எப்போது?",
      "quick3": "🌿 உர அளவு என்ன?",
      "clear": "அழிக்கவும்",
      "micTooltip": "தமிழில் பேச மைக் தொடவும்",
      "listening": "கேட்கிறது... பேசுங்கள்",
      "listenReply": "🔊 வாசிக்கவும்",
      "stopReply": "⏹ குரலை நிறுத்து"
    },
    "help": {
      "title": "விவசாயி உதவி மையம் & வழிகாட்டி",
      "subtitle": "படங்கள் மற்றும் குரல் உதவியுடன் கூடிய எளிமையான வழிகாட்டி",
      "workflowTitle": "🚜 7-படி எளிய விவசாய வழிகாட்டி",
      "colorsTitle": "🎨 வண்ணங்கள் மற்றும் குறியீடுகள் விளக்கம்",
      "dosDontsTitle": "✅ செய்ய வேண்டியவை & ❌ தவிர்க்க வேண்டியவை",
      "helplineTitle": "📞 உழவர் உதவி எண்"
    },
    "sensors": {
      "title": "IoT சென்சார்கள் மற்றும் தரவு",
      "subtitle": "நேரடி சென்சார் தரவு பதிவு.",
      "manualTab": "📝 நேரடி பதிவு",
      "iotTab": "📡 நேரலை சென்சார்",
      "historyTab": "📊 முந்தைய தரவு",
      "saveBtn": "சேமிக்கவும்",
      "broadcastBtn": "📡 அனுப்பவும்"
    },
    "briefing": {
      "badge": "தினசரி 1 நிமிட குரல் அறிக்கை",
      "title": "இன்றைய பண்ணை & சந்தை தகவல்",
      "subtitle": "மண் வளம், பயிர் பாதுகாப்பு, சந்தை விலை குறித்த 1 நிமிட குரல் அறிக்கை.",
      "play": "▶️ 1 நிமிட அறிக்கை கேட்க",
      "pause": "⏸ இடைநிறுத்து",
      "stop": "⏹ நிறுத்து",
      "playing": "AgriSense AI தமிழில் பேசுகிறது",
      "updateToday": "📝 இன்றைய தரவை பதிவிடவும்",
      "saving": "சேமிக்கிறது...",
      "saved": "இன்றைய தரவு சேமிக்கப்பட்டது!",
      "cropCardTitle": "பரிந்துரை பயிர்",
      "mandiCardTitle": "இன்றைய சந்தை விலை",
      "healthCardTitle": "பயிர் பாதுகாப்பு",
      "tipCardTitle": "இன்றைய விவசாய குறிப்பு",
      "transcriptTitle": "1 நிமிட உரை வடிவம்",
      "audioSpeed": "குரல் வேகம்",
      "quickCheckin": "இன்றைய விரைவு பதிவு",
      "saveTodayBtn": "இன்றைய தரவை சேமி"
    }
  },
  "ಕನ್ನಡ": {
    "code": "kn-IN",
    "appName": "ಅಗ್ರಿಸೆನ್ಸ್ AI",
    "tagline": "ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ನಿರ್ಧಾರ ಬೆಂಬಲ ಮತ್ತು ಸಲಹಾ ವೇದಿಕೆ",
    "nav": {
      "dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
      "crop": "ಬೆಳೆ ಶಿಫಾರಸು",
      "soil": "ಮಣ್ಣಿನ ಆರೋಗ್ಯ",
      "irrigation": "ನೀರಾವರಿ",
      "fertilizer": "ಗೊಬ್ಬರ ಯೋಜನೆ",
      "disease": "ಸಸ್ಯ ವೈದ್ಯ",
      "mandi": "ಮಂಡಿ ದರಗಳು",
      "schemes": "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು",
      "voice": "ಧ್ವನಿ AI",
      "chat": "AI ಚಾಟ್",
      "help": "ಸಹಾಯ ಕೇಂದ್ರ",
      "sensors": "IoT ಸಂವೇದಕಗಳು",
      "briefing": "1 ನಿಮಿಷ ವರದಿ",
      "menu": "ಎಲ್ಲಾ ಸೇವೆಗಳು"
    },
    "login": {
      "title": "ರೈತ ಪ್ರೊಫೈಲ್ ಲಾಗಿನ್",
      "subtitle": "ನಿಮ್ಮ ಜಮೀನಿನ ಮಾಹಿತಿ ಪಡೆಯಲು ಹೆಸರು ಮತ್ತು ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ",
      "name": "ರೈತರ ಹೆಸರು",
      "phone": "10 ಅಂಕಿಯ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ",
      "submit": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ಪ್ರವೇಶಿಸಿ",
      "placeholderName": "ಉದಾ: ಸುರೇಶ್ ಗೌಡ",
      "placeholderPhone": "ಉದಾ: 9876543210"
    },
    "dashboard": {
      "welcome": "ಸ್ವಾಗತ, ರೈತ ಮಿತ್ರ",
      "greeting": "ಇಂದಿನ ಮಣ್ಣಿನ ಪರೀಕ್ಷೆ ಮತ್ತು ಹವಾಮಾನ ವಿವರಗಳು.",
      "weatherTitle": "ಪ್ರಸ್ತುತ ಹವಾಮಾನ",
      "weatherDesc": "ಕೃಷಿ ಕೆಲಸಗಳಿಗೆ ಸೂಕ್ತ ಹವಾಮಾನ",
      "soilScore": "ಮಣ್ಣಿನ ಫಲವತ್ತತೆ ಅಂಕ",
      "iotStatus": "IoT ಸಂವೇದಕ ಸ್ಥಿತಿ",
      "quickActions": "ತ್ವರಿತ ಸೇವೆಗಳು",
      "recCrop": "ಶಿಫಾರಸು ಮಾಡಿದ ಬೆಳೆ",
      "waterStatus": "ಮಣ್ಣಿನ ತೇವಾಂಶ",
      "optimal": "ಉತ್ತಮ ತೇವಾಂಶ",
      "needsWater": "ನೀರಿನ ಅಗತ್ಯವಿದೆ",
      "viewDetails": "ಸಂಪೂರ್ಣ ವಿವರ",
      "steps": {
        "step1": "1. ಮಣ್ಣು ಪರೀಕ್ಷೆ",
        "step2": "2. ಬೆಳೆ ಶಿಫಾರಸು AI",
        "step3": "3. ಕೃಷಿ ಸಲಹೆ"
      },
      "features": {
        "sensors": {
          "title": "ಹಂತ 1 — ಮಣ್ಣು ಪರೀಕ್ಷೆ",
          "desc": "NPK, pH, ತೇವಾಂಶ ನಮೂದಿಸಿ ಅಥವಾ IoT ಸಂವೇದಕದಿಂದ ನೇರ ಡೇಟಾ ಪಡೆಯಿರಿ.",
          "cta": "ಪರೀಕ್ಷೆ ಪ್ರಾರಂಭಿಸಿ"
        },
        "crop": {
          "title": "ಹಂತ 2 — ಬೆಳೆ ಶಿಫಾರಸು AI",
          "desc": "ನಿಮ್ಮ ಮಣ್ಣು ಮತ್ತು ಹವಾಮಾನಕ್ಕೆ ತಕ್ಕಂತೆ ಉತ್ತಮ ಇಳುವರಿ ನೀಡುವ ಬೆಳೆ ಆಯ್ಕೆ.",
          "cta": "ಬೆಳೆ ಶಿಫಾರಸು ಪಡೆಯಿರಿ"
        },
        "soil": {
          "title": "ಮಣ್ಣಿನ ಆರೋಗ್ಯ ವರದಿ",
          "desc": "NPK ಪೋಷಕಾಂಶಗಳ ಕೊರತೆ ಮತ್ತು ಸಾವಯವ ಮಣ್ಣು ಸುಧಾರಣಾ ಯೋಜನೆ.",
          "cta": "ವರದಿ ವೀಕ್ಷಿಸಿ"
        },
        "irrigation": {
          "title": "ಸ್ಮಾರ್ಟ್ ನೀರಾವರಿ",
          "desc": "ಮಣ್ಣಿನ ತೇವಾಂಶಕ್ಕೆ ಅನುಗುಣವಾಗಿ ಮೋಟಾರ್ ಚಾಲನೆಯ ನಿಖರ ಸಮಯ.",
          "cta": "ನೀರಾವರಿ ಸಲಹೆಗಾರ"
        },
        "fertilizer": {
          "title": "ಗೊಬ್ಬರ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
          "desc": "ಯೂರಿಯಾ, DAP, ಪೊಟ್ಯಾಶ್ ರಸಗೊಬ್ಬರಗಳ 4 ಹಂತಗಳ ಪ್ರಮಾಣ.",
          "cta": "ಗೊಬ್ಬರ ಪಟ್ಟಿ ವೀಕ್ಷಿಸಿ"
        },
        "disease": {
          "title": "AI ಸಸ್ಯ ವೈದ್ಯ",
          "desc": "ಎಲೆಯ ಫೋಟೋ ತೆಗೆಯಿರಿ — AI ತಕ್ಷಣವೇ ಸಾವಯವ ಮತ್ತು ರಾಸಾಯನಿಕ ಚಿಕಿತ್ಸೆ ನೀಡುತ್ತದೆ.",
          "cta": "ವೈದ್ಯರನ್ನು ಭೇಟಿ ಮಾಡಿ"
        },
        "mandi": {
          "title": "ಮಾರುಕಟ್ಟೆ ದರಗಳು",
          "desc": "e-NAM APMC ದರಗಳು ಮತ್ತು ಕೃಷಿ ವೆಚ್ಚ-ಲಾಭದ ನಿಖರ ಲೆಕ್ಕಾಚಾರ.",
          "cta": "ದರಗಳನ್ನು ಪರಿಶೀಲಿಸಿ"
        },
        "schemes": {
          "title": "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು",
          "desc": "ಪಿಎಂ-ಕಿಸಾನ್, ಸೋಲಾರ್ ಪಂಪ್, ಬೆಳೆ ವಿಮೆ ಮತ್ತು ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್.",
          "cta": "ಯೋಜನೆಗಳನ್ನು ನೋಡಿ"
        },
        "voice": {
          "title": "ಧ್ವನಿ AI ಸಹಾಯಕ",
          "desc": "ಕನ್ನಡದಲ್ಲೇ ಮಾತನಾಡಿ — AgriSense AI ಧ್ವನಿಯ ಮೂಲಕ ಉತ್ತರಿಸುತ್ತದೆ.",
          "cta": "ಧ್ವನಿಯಲ್ಲಿ ಮಾತನಾಡಿ"
        },
        "chat": {
          "title": "AI ಚಾಟ್ ಸಹಾಯಕ",
          "desc": "ಕೃಷಿ ಪ್ರಶ್ನೆಗಳನ್ನು ಕನ್ನಡದಲ್ಲಿ ಕೇಳಿ ನಿಖರ ಉತ್ತರ ಪಡೆಯಿರಿ.",
          "cta": "ಚಾಟ್ ಪ್ರಾರಂಭಿಸಿ"
        },
        "help": {
          "title": "ರೈತ ಸಹಾಯ ಕೇಂದ್ರ",
          "desc": "7 ಹಂತಗಳ ಮಾರ್ಗದರ್ಶಿ ಮತ್ತು ಕಿಸಾನ್ ಸಹಾಯವಾಣಿ 1551.",
          "cta": "ಸಹಾಯ ಕೇಂದ್ರ ನೋಡಿ"
        }
      }
    },
    "crop": {
      "title": "ML ಬೆಳೆ ಶಿಫಾರಸು",
      "subtitle": "ನಿಮ್ಮ ಮಣ್ಣು ಮತ್ತು ಹವಾಮಾನಕ್ಕೆ ತಕ್ಕಂತೆ ಅತಿ ಹೆಚ್ಚು ಇಳುವರಿ ನೀಡುವ ಬೆಳೆ.",
      "nitrogen": "ಸಾರಜನಕ (N)",
      "phosphorus": "ರಂಜಕ (P)",
      "potassium": "ಪೊಟ್ಯಾಶ್ (K)",
      "temp": "ತಾಪಮಾನ (°C)",
      "humidity": "ತೇವಾಂಶ (%)",
      "ph": "ಮಣ್ಣಿನ pH",
      "rainfall": "ಮಳೆ (ಮಿ.ಮೀ)",
      "predictBtn": "🌱 ಸೂಕ್ತ ಬೆಳೆ ಹುಡುಕಿ",
      "useLatest": "⚡ ಸಂವೇದಕ ಮಾಹಿತಿ ಬಳಸಿ",
      "resultTitle": "ಸೂಕ್ತ ಬೆಳೆ",
      "suitability": "ಹೊಂದಾಣಿಕೆ ಅಂಕ",
      "packageOfPractice": "ಕೃಷಿ ಕೈಪಿಡಿ"
    },
    "soil": {
      "title": "ಮಣ್ಣಿನ ಆರೋಗ್ಯ ಮತ್ತು ಪೋಷಕಾಂಶಗಳು",
      "subtitle": "NPK ಮತ್ತು pH ಸಮತೋಲನ ವಿಶ್ಲೇಷಣೆ.",
      "npkRatio": "ಪ್ರಸ್ತುತ NPK ಅನುಪಾತ",
      "idealRatio": "ಆದರ್ಶ ಅನುಪಾತ (4:2:1)",
      "organicCarbon": "ಸಾವಯವ ಇಂಗಾಲ",
      "phStatus": "ಮಣ್ಣಿನ pH ಸ್ಥಿತಿ",
      "recommendations": "ಮಣ್ಣು ಸುಧಾರಣಾ ಕ್ರಮಗಳು"
    },
    "irrigation": {
      "title": "ಸ್ಮಾರ್ಟ್ ನೀರಾವರಿ ಸಲಹೆಗಾರ",
      "subtitle": "ತೇವಾಂಶ ಆಧರಿಸಿ ನೀರುಣಿಸುವ ಸೂಕ್ತ ಸಮಯ.",
      "moistureGauge": "ಬೇರಿನ ಪ್ರದೇಶದ ತೇವಾಂಶ",
      "schedule": "ನೀರಾವರಿ ವೇಳಾಪಟ್ಟಿ",
      "waterReq": "ಅಗತ್ಯವಿರುವ ನೀರಿನ ಪ್ರಮಾಣ",
      "calcBtn": "ನೀರಿನ ಪ್ರಮಾಣ ಲೆಕ್ಕಿಸಿ"
    },
    "fertilizer": {
      "title": "ರಸಗೊಬ್ಬರ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
      "subtitle": "ಬೆಳೆಗೆ ಅಗತ್ಯವಿರುವ ಸಾವಯವ ಮತ್ತು ರಾಸಾಯನಿಕ ಗೊಬ್ಬರದ ಪ್ರಮಾಣ.",
      "targetCrop": "ಬೆಳೆ",
      "landSize": "ಜಮೀನಿನ ವಿಸ್ತೀರ್ಣ (ಎಕರೆ)",
      "calcBtn": "ಗೊಬ್ಬರ ಪಟ್ಟಿ ತಯಾರಿಸಿ",
      "organicPlan": "ಸಾವಯವ ಗೊಬ್ಬರ",
      "chemicalPlan": "ರಾಸಾಯನಿಕ ಗೊಬ್ಬರ"
    },
    "disease": {
      "title": "AI ಸಸ್ಯ ವೈದ್ಯ - ರೋಗ ಪತ್ತೆ",
      "subtitle": "ಎಲೆಯ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ತಕ್ಷಣ ರೋಗ ಪತ್ತೆ ಮತ್ತು ಪರಿಹಾರ ಪಡೆಯಿರಿ.",
      "cropSelect": "ಬೆಳೆ ಆಯ್ಕೆಮಾಡಿ",
      "symptomsLabel": "ರೋಗದ ಲಕ್ಷಣಗಳು",
      "uploadPrompt": "ಎಲೆಯ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
      "diagnoseBtn": "🔬 ರೋಗ ಪತ್ತೆ ಮಾಡಿ",
      "diagnosisResult": "ರೋಗ ಪತ್ತೆ ಮತ್ತು ಪರಿಹಾರ"
    },
    "mandi": {
      "title": "ಲೈವ್ ಮಂಡಿ ದರಗಳು & ಕೃಷಿ ವೆಚ್ಚದ ಅಂದಾಜು",
      "subtitle": "ಅಧಿಕೃತ e-NAM & APMC ಮಾರುಕಟ್ಟೆ ದರಗಳು ಮತ್ತು ಲಾಭದ ಲೆಕ್ಕಾಚಾರ",
      "tabMarket": "📈 ಲೈವ್ ಮಂಡಿ ದರಗಳು",
      "tabCost": "💰 ಕೃಷಿ ವೆಚ್ಚ ಮತ್ತು ಲಾಭದ ಅಂದಾಜು",
      "stateSelect": "ರಾಜ್ಯ",
      "cropSelect": "ಬೆಳೆ",
      "getPrices": "📊 ಮಂಡಿ ಬೆಲೆ ವೀಕ್ಷಿಸಿ",
      "bestMandi": "🌾 ಇಂದು ಯಾವ ಮಂಡಿಯಲ್ಲಿ ಗರಿಷ್ಠ ಬೆಲೆ?",
      "mspPrompt": "📜 ಈ ಬೆಳೆಗೆ ಸರ್ಕಾರದ ಬೆಂಬಲ ಬೆಲೆ (MSP) ಎಷ್ಟು?",
      "bestTime": "🗓️ ಮಾರಾಟಕ್ಕೆ ಸೂಕ್ತ ಸಮಯ ಯಾವುದು?",
      "costCrop": "ಬೆಳೆ ಹೆಸರು",
      "costArea": "ಜಮೀನಿನ ವಿಸ್ತೀರ್ಣ (ಎಕರೆ)",
      "costSeason": "ಋತು",
      "calcCost": "💰 ಲಾಭ ಲೆಕ್ಕಿಸಿ"
    },
    "schemes": {
      "title": "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು ಮತ್ತು ಸಬ್ಸಿಡಿಗಳು",
      "subtitle": "ರೈತರಿಗೆ ಅಧಿಕೃತ ಆರ್ಥಿಕ ನೆರವು, ಬೆಳೆ ವಿಮೆ ಮತ್ತು ಕಲ್ಯಾಣ ಕಾರ್ಯಕ್ರಮಗಳು",
      "tabNational": "🌟 ಪ್ರಮುಖ ರಾಷ್ಟ್ರೀಯ ಯೋಜನೆಗಳು",
      "tabState": "📍 ರಾಜ್ಯ ಕಲ್ಯಾಣ ಯೋಜನೆಗಳು",
      "tabEligibility": "🎯 ತ್ವರಿತ AI ಅರ್ಹತೆ ಪರೀಕ್ಷಕ",
      "searchPlaceholder": "ಯೋಜನೆಯ ಹೆಸರು ಹುಡುಕಿ...",
      "filterAll": "ಎಲ್ಲಾ ಯೋಜನೆಗಳು",
      "checkBtn": "ಅರ್ಹತೆ ಪರಿಶೀಲಿಸಿ",
      "applyGuide": "ಅರ್ಜಿ ಸಲ್ಲಿಸುವ ವಿಧಾನ"
    },
    "voice": {
      "title": "ಅಗ್ರಿಸೆನ್ಸ್ ಕನ್ನಡ ಧ್ವನಿ AI",
      "subtitle": "ಕನ್ನಡದಲ್ಲಿ ಮಾತನಾಡಿ ಕೃಷಿ ಸಲಹೆ ಪಡೆಯಿರಿ.",
      "tabLive": "⚡ ಲೈವ್ ಸ್ಟ್ರೀಮಿಂಗ್",
      "tabBrowser": "🎙️ ನೇರ ಧ್ವನಿ ಸಹಾಯಕ",
      "startBtn": "🎤 ಮಾತನಾಡಲು ಪ್ರಾರಂಭಿಸಿ",
      "stopBtn": "⏹ ನಿಲ್ಲಿಸಿ",
      "serverOnline": "🟢 ಸರ್ವರ್ ಚಾಲನೆಯಲ್ಲಿದೆ",
      "serverOffline": "🔴 ಸರ್ವರ್ ಆಫ್‌ಲೈನ್ ಆಗಿದೆ",
      "transcriptTitle": "AI ಉತ್ತರ ಮತ್ತು ಸಂಭಾಷಣೆ",
      "tapMic": "ಮೈಕ್ ಒತ್ತಿ ಕನ್ನಡದಲ್ಲಿ ಪ್ರಶ್ನೆ ಕೇಳಿ"
    },
    "chat": {
      "title": "AI ಕೃಷಿ ತಜ್ಞರ ಚಾಟ್",
      "subtitle": "ನಿಮ್ಮ ಜಮೀನಿನ ವಿವರಗಳೊಂದಿಗೆ ತಕ್ಷಣದ ಸಲಹೆ.",
      "inputPlaceholder": "ಕನ್ನಡದಲ್ಲಿ ಪ್ರಶ್ನೆ ಕೇಳಿ...",
      "quick1": "🌾 ನನ್ನ ಜಮೀನಿಗೆ ಯಾವ ಬೆಳೆ ಸೂಕ್ತ?",
      "quick2": "💧 ಮುಂದಿನ ನೀರಾವರಿ ಯಾವಾಗ?",
      "quick3": "🌿 ಗೊಬ್ಬರದ ಪ್ರಮಾಣ ಎಷ್ಟು?",
      "clear": "ಚಾಟ್ ತೆರವುಗೊಳಿಸಿ",
      "micTooltip": "ಕನ್ನಡದಲ್ಲಿ ಮಾತನಾಡಲು ಮೈಕ್ ಒತ್ತಿರಿ",
      "listening": "ಆಲಿಸುತ್ತಿದೆ... ಮಾತನಾಡಿ",
      "listenReply": "🔊 ಧ್ವನಿಯಲ್ಲಿ ಆಲಿಸಿ",
      "stopReply": "⏹ ಧ್ವನಿ ನಿಲ್ಲಿಸಿ"
    },
    "help": {
      "title": "ರೈತ ಸಹಾಯ ಕೇಂದ್ರ ಮತ್ತು ಮಾರ್ಗದರ್ಶಿ",
      "subtitle": "ಚಿತ್ರಗಳು ಮತ್ತು ಧ್ವನಿ ಸಹಾಯದೊಂದಿಗೆ ಸರಳ ಮಾರ್ಗದರ್ಶಿ",
      "workflowTitle": "🚜 7-ಹಂತಗಳ ಸರಳ ಕೃಷಿ ಪದ್ಧತಿ",
      "colorsTitle": "🎨 ಬಣ್ಣಗಳು ಮತ್ತು ಸಂಕೇತಗಳ ಅರ್ಥ",
      "dosDontsTitle": "✅ ಮಾಡಬೇಕಾದದ್ದು & ❌ ಮಾಡಬಾರದ್ದು",
      "helplineTitle": "📞 ಕಿಸಾನ್ ಸಹಾಯವಾಣಿ"
    },
    "sensors": {
      "title": "IoT ಸಂವೇದಕಗಳು ಮತ್ತು ಡೇಟಾ ಹಬ್",
      "subtitle": "ನೇರ ಸಂವೇದಕ ಮಾಹಿತಿ ದಾಖಲೆ.",
      "manualTab": "📝 ಮ್ಯಾನುಯಲ್ ಎಂಟ್ರಿ",
      "iotTab": "📡 ಲೈವ್ ಸಂವೇದಕ",
      "historyTab": "📊 ಹಿಂದಿನ ದಾಖಲೆಗಳು",
      "saveBtn": "ಉಳಿಸಿ",
      "broadcastBtn": "📡 ಕಳುಹಿಸಿ"
    },
    "briefing": {
      "badge": "ದೈನಂದಿನ 1 ನಿಮಿಷ ಆಡಿಯೋ ವರದಿ",
      "title": "ಇಂದಿನ ಕೃಷಿ ಮತ್ತು ಮಾರುಕಟ್ಟೆ ಮಾಹಿತಿ",
      "subtitle": "ಮಣ್ಣಿನ ತೇವಾಂಶ, ಬೆಳೆ ರಕ್ಷಣೆ, ಮಾರುಕಟ್ಟೆ ದರದ ಕುರಿತು 1 ನಿಮಿಷದ ವಿವರಣೆ.",
      "play": "▶️ 1 ನಿಮಿಷ ವರದಿ ಆಲಿಸಿ",
      "pause": "⏸ ವಿರಾಮ",
      "stop": "⏹ ನಿಲ್ಲಿಸಿ",
      "playing": "AgriSense AI ಕನ್ನಡದಲ್ಲಿ ಮಾತನಾಡುತ್ತಿದೆ",
      "updateToday": "📝 ಇಂದಿನ ಡೇಟಾ ನಮೂದಿಸಿ",
      "saving": "ಉಳಿಸಲಾಗುತ್ತಿದೆ...",
      "saved": "ಇಂದಿನ ಡೇಟಾ ಯಶಸ್ವಿಯಾಗಿ ನಮೂದಾಗಿದೆ!",
      "cropCardTitle": "ಶಿಫಾರಸು ಬೆಳೆ",
      "mandiCardTitle": "ಇಂದಿನ ಮಾರುಕಟ್ಟೆ ದರ",
      "healthCardTitle": "ಬೆಳೆ ರಕ್ಷಣೆ ಸೂಚನೆ",
      "tipCardTitle": "ಇಂದಿನ ಕೃಷಿ ಸಲಹೆ",
      "transcriptTitle": "1 ನಿಮಿಷದ ಪೂರ್ಣ ವಿವರ",
      "audioSpeed": "ಧ್ವನಿ ವೇಗ",
      "quickCheckin": "ದೈನಂದಿನ ತ್ವರಿತ ದಾಖಲಾತಿ",
      "saveTodayBtn": "ಇಂದಿನ ಡೇಟಾ ಉಳಿಸಿ"
    }
  },
  "मराठी": {
    "code": "mr-IN",
    "appName": "एग्रीसेन्स AI",
    "tagline": "स्मार्ट कृषी निर्णय सहाय्यक आणि शेती सल्लागार",
    "nav": {
      "dashboard": "डॅशबोर्ड",
      "crop": "पीक सल्ला",
      "soil": "मृदा आरोग्य",
      "irrigation": "सिंचन व्यवस्थापन",
      "fertilizer": "खत नियोजन",
      "disease": "वनस्पती डॉक्टर",
      "mandi": "मंडी भाव",
      "schemes": "सरकारी योजना",
      "voice": "व्हॉईस AI",
      "chat": "AI चॅट",
      "help": "मदत केंद्र",
      "sensors": "IoT सेन्सर्स",
      "briefing": "1 मिनिट अपडेट",
      "menu": "सर्व वैशिष्ट्ये"
    },
    "login": {
      "title": "शेतकरी प्रोफाइल लॉगिन",
      "subtitle": "आपल्या शेताची माहिती मिळवण्यासाठी नाव आणि मोबाईल नंबर टाका",
      "name": "शेतकऱ्याचे नाव",
      "phone": "१० अंकी मोबाईल नंबर",
      "submit": "डॅशबोर्ड उघडा",
      "placeholderName": "उदा: सचिन पाटील",
      "placeholderPhone": "उदा: 9876543210"
    },
    "dashboard": {
      "welcome": "स्वागत आहे, शेतकरी मित्र",
      "greeting": "आजचे माती परीक्षण आणि हवामान तपशील.",
      "weatherTitle": "सध्याचे हवामान",
      "weatherDesc": "शेतीच्या कामांसाठी अनुकूल वातावरण",
      "soilScore": "माती सुपीकता गुण",
      "iotStatus": "IoT सेन्सर स्थिती",
      "quickActions": "जलद सेवा",
      "recCrop": "शिफारस केलेले पीक",
      "waterStatus": "मातीतील ओलावा",
      "optimal": "पुरेसा ओलावा",
      "needsWater": "पाणी देण्याची गरज",
      "viewDetails": "सविस्तर माहिती",
      "steps": {
        "step1": "1. माती परीक्षण",
        "step2": "2. पीक शिफारस AI",
        "step3": "3. कृषी सल्ला व नियोजन"
      },
      "features": {
        "sensors": {
          "title": "पायरी 1 — माती परीक्षण",
          "desc": "NPK, pH व ओलावा नोंदवा किंवा IoT सेन्सरद्वारे थेट डेटा मिळवा.",
          "cta": "माती परीक्षण सुरू करा"
        },
        "crop": {
          "title": "पायरी 2 — पीक शिफारस AI",
          "desc": "माती व हवामानानुसार सर्वाधिक उत्पादन देणाऱ्या पिकाची अचूक शिफारस.",
          "cta": "पीक शिफारस मिळवा"
        },
        "soil": {
          "title": "मृदा आरोग्य अहवाल",
          "desc": "NPK पोषण विश्लेषण, pH आणि सेंद्रिय माती सुधारणा उपाय.",
          "cta": "मृदा अहवाल पाहा"
        },
        "irrigation": {
          "title": "स्मार्ट सिंचन सल्ला",
          "desc": "मातीतील ओलाव्यानुसार पाणी देण्याची योग्य वेळ व प्रमाण.",
          "cta": "सिंचन सल्लागार"
        },
        "fertilizer": {
          "title": "खत व्यवस्थापन",
          "desc": "युरिया, डीएपी, पोटॅश खतांचे ४ टप्प्यांतील अचूक प्रमाण.",
          "cta": "खत वेळापत्रक पाहा"
        },
        "disease": {
          "title": "AI वनस्पती डॉक्टर",
          "desc": "पानाचा फोटो काढा — AI तात्काळ सेंद्रिय व रासायनिक उपाय सांगेल.",
          "cta": "डॉक्टर उघडा"
        },
        "mandi": {
          "title": "थेट बाजारभाव",
          "desc": "e-NAM व APMC दर, हमीभाव तुलना आणि शेती नफा-तोटा हिशोब.",
          "cta": "बाजारभाव पाहा"
        },
        "schemes": {
          "title": "सरकारी योजना",
          "desc": "पीएम-किसान, सोलर पंप, पीक विमा आणि किसान क्रेडिट कार्ड.",
          "cta": "योजना पाहा"
        },
        "voice": {
          "title": "व्हॉइस AI सहाय्यक",
          "desc": "मराठीत बोला — AgriSense AI आवाजाद्वारे तात्काळ उत्तर देईल.",
          "cta": "मराठीत बोला"
        },
        "chat": {
          "title": "AI चॅट सहाय्यक",
          "desc": "शेतीविषयी कोणतेही प्रश्न विचारा व सविस्तर सल्ला मिळवा.",
          "cta": "चॅट सुरू करा"
        },
        "help": {
          "title": "शेतकरी मदत केंद्र",
          "desc": "७ पायऱ्यांचे मार्गदर्शन आणि टोल-फ्री किसान हेल्पलाइन १५५१.",
          "cta": "मार्गदर्शन पाहा"
        }
      }
    },
    "crop": {
      "title": "ML पीक शिफारस",
      "subtitle": "माती आणि हवामानानुसार सर्वाधिक उत्पादन देणारे पीक.",
      "nitrogen": "नायट्रोजन (N)",
      "phosphorus": "फॉस्फरस (P)",
      "potassium": "पोटॅशियम (K)",
      "temp": "तापमान (°C)",
      "humidity": "हवेतील ओलावा (%)",
      "ph": "मातीचा pH",
      "rainfall": "पाऊस (मिमी)",
      "predictBtn": "🌱 योग्य पीक निवडा",
      "useLatest": "⚡ सेन्सर डेटा वापरा",
      "resultTitle": "शिफारस केलेले पीक",
      "suitability": "अनुकूलता स्कोर",
      "packageOfPractice": "लागवड मार्गदर्शक सूचना"
    },
    "soil": {
      "title": "मृदा आरोग्य आणि NPK शिल्लक",
      "subtitle": "NPK पोषण पातळी आणि जमिनीच्या pH चे विश्लेषण.",
      "npkRatio": "सध्याचे NPK प्रमाण",
      "idealRatio": "आदर्श प्रमाण (4:2:1)",
      "organicCarbon": "सेंद्रिय कर्ब",
      "phStatus": "मातीचा pH स्तर",
      "recommendations": "जमीन सुधारणा उपाय"
    },
    "irrigation": {
      "title": "अचूक सिंचन व्यवस्थापन",
      "subtitle": "जमिनीतील ओलाव्यानुसार पाणी देण्याची योग्य वेळ आणि प्रमाण.",
      "moistureGauge": "मुळांच्या भागातील ओलावा",
      "schedule": "सिंचन वेळापत्रक",
      "waterReq": "आवश्यक पाण्याची मात्रा",
      "calcBtn": "सिंचनाची गरज मोजा"
    },
    "fertilizer": {
      "title": "खत मात्रा कॅल्क्युलेटर",
      "subtitle": "पिकासाठी आवश्यक सेंद्रिय आणि रासायनिक खतांचे अचूक प्रमाण.",
      "targetCrop": "लागवड करावयाचे पीक",
      "landSize": "शेताचे क्षेत्रफळ (एकर)",
      "calcBtn": "खत योजना तयार करा",
      "organicPlan": "सेंद्रिय खत योजना",
      "chemicalPlan": "रासायनिक खतांची मात्रा"
    },
    "disease": {
      "title": "AI वनस्पती डॉक्टर - रोग निदान",
      "subtitle": "पानांच्या फोटोद्वारे रोगांचे त्वरित निदान आणि योग्य उपाययोजना.",
      "cropSelect": "पीक निवडा",
      "symptomsLabel": "दिसणारी लक्षणे सांगा",
      "uploadPrompt": "पानाचा फोटो अपलोड करा",
      "diagnoseBtn": "🔬 रोगाचे निदान करा",
      "diagnosisResult": "रोग निदान व उपाय"
    },
    "mandi": {
      "title": "थेट मंडी भाव आणि शेती खर्च अंदाज",
      "subtitle": "अधिकृत e-NAM आणि कृषी उत्पन्न बाजार समिती (APMC) थेट दर व नफा कॅल्क्युलेटर",
      "tabMarket": "📈 थेट मंडी भाव (e-NAM)",
      "tabCost": "💰 शेती खर्च व नफा कॅल्क्युलेटर",
      "stateSelect": "राज्य निवडा",
      "cropSelect": "पीक निवडा",
      "getPrices": "📊 मंडी भाव पहा",
      "bestMandi": "🌾 आज कोणत्या मंडईत सर्वाधिक भाव आहे?",
      "mspPrompt": "📜 या पिकाचा हमीभाव (MSP) किती आहे?",
      "bestTime": "🗓️ माल विकण्याची सर्वोत्तम वेळ कोणती?",
      "costCrop": "पिकाचे नाव",
      "costArea": "शेत क्षेत्र (एकर)",
      "costSeason": "हंगाम",
      "calcCost": "💰 नफा मोजा"
    },
    "schemes": {
      "title": "सरकारी योजना आणि अनुदाने",
      "subtitle": "शेतकऱ्यांसाठी अधिकृत आर्थिक मदत, पीक विमा आणि कल्याणकारी योजना",
      "tabNational": "🌟 प्रमुख राष्ट्रीय योजना",
      "tabState": "📍 राज्य कल्याणकारी योजना",
      "tabEligibility": "🎯 झटपट AI पात्रता चेकर",
      "searchPlaceholder": "योजनेचे नाव किंवा कीवर्ड शोधा...",
      "filterAll": "सर्व योजना",
      "checkBtn": "माझी पात्रता तपासा",
      "applyGuide": "अर्ज प्रक्रिया व आवश्यक कागदपत्रे"
    },
    "voice": {
      "title": "एग्रीसेन्स मराठी थेट व्हॉईस AI",
      "subtitle": "मराठीत बोलून शेतीविषयक मार्गदर्शन मिळवा.",
      "tabLive": "⚡ जेमिनी लाईव्ह स्ट्रीमिंग",
      "tabBrowser": "🎙️ थेट व्हॉईस असिस्टंट",
      "startBtn": "🎤 बोलायला सुरुवात करा",
      "stopBtn": "⏹ थांबवा",
      "serverOnline": "🟢 सर्व्हर चालू आहे (Port 8000)",
      "serverOffline": "🔴 सर्व्हर बंद आहे",
      "transcriptTitle": "AI चे उत्तर व संवाद",
      "tapMic": "माइक दाबा आणि मराठीत प्रश्न विचारा"
    },
    "chat": {
      "title": "AI कृषी तज्ज्ञ चॅट",
      "subtitle": "आपल्या शेताच्या माहितीसह अचूक मार्गदर्शन.",
      "inputPlaceholder": "मराठीत प्रश्न विचारा...",
      "quick1": "🌾 माझ्या शेतीसाठी कोणते पीक योग्य?",
      "quick2": "💧 पुढील सिंचन कधी करावे?",
      "quick3": "🌿 खतांचे योग्य प्रमाण काय?",
      "clear": "चॅट साफ करा",
      "micTooltip": "मराठीत बोलण्यासाठी माइक दाबा",
      "listening": "ऐकत आहे... बोला",
      "listenReply": "🔊 ऐका",
      "stopReply": "⏹ आवाज थांबवा"
    },
    "help": {
      "title": "शेतकरी मदत केंद्र आणि मार्गदर्शिका",
      "subtitle": "चित्रे आणि ऑडिओ सहाय्यासह सोपी मार्गदर्शिका",
      "workflowTitle": "🚜 ७-टप्प्यांची सोपी शेती पद्धती",
      "colorsTitle": "🎨 रंग आणि चिन्हांचा अर्थ",
      "dosDontsTitle": "✅ काय करावे आणि ❌ काय करू नये",
      "helplineTitle": "📞 किसान हेल्पलाइन"
    },
    "sensors": {
      "title": "IoT सेन्सर्स आणि डेटा हब",
      "subtitle": "मॅन्युअल नोंद आणि थेट IoT सेन्सर डेटा.",
      "manualTab": "📝 मॅन्युअल नोंद",
      "iotTab": "📡 थेट सेन्सर डेटा",
      "historyTab": "📊 मागील नोंदी",
      "saveBtn": "जतन करा",
      "broadcastBtn": "📡 डेटा पाठवा"
    },
    "briefing": {
      "badge": "दैनिक १ मिनिट ऑडिओ बुलेटीन",
      "title": "आजची कृषी व बाजार माहिती",
      "subtitle": "मातीचा ओलावा, पिकाचे संरक्षण आणि आजचे बाजारभाव यावर १ मिनिटांचा ऑडिओ अहवाल.",
      "play": "▶️ १ मिनिट बुलेटीन ऐका",
      "pause": "⏸ थांबवा",
      "stop": "⏹ बंद करा",
      "playing": "AgriSense AI मराठीत बोलत आहे",
      "updateToday": "📝 आजचा डेटा नोंदवा",
      "saving": "जतन होत आहे...",
      "saved": "आजचा डेटा जतन केला!",
      "cropCardTitle": "निवडलेले पीक",
      "mandiCardTitle": "आजचे बाजारभाव",
      "healthCardTitle": "पीक संरक्षण सल्ला",
      "tipCardTitle": "आजचा शेती सल्ला",
      "transcriptTitle": "१ मिनिटांचे संपूर्ण विवरण",
      "audioSpeed": "आवाज गती",
      "quickCheckin": "दैनिक जलद नोंदणी",
      "saveTodayBtn": "आजचा डेटा जतन करा"
    }
  }
};
