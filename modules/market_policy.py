"""
AgriSense AI — Government Policy & Live Market Prices Module
==============================================================
Provides:
  1. Government Agricultural Schemes & Subsidies (AI-powered, localized)
  2. Live Mandi Market Prices (Estimated crop prices via AI intelligence)
  3. Cost Estimation Calculator (Input-based yield/profit estimator)

Architecturally independent — does NOT modify any other module.
"""

import os
import json
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import streamlit as st
import streamlit.components.v1 as components
from modules.ai_engine import ask_agrisense_stream


# =========================================================
# MULTILINGUAL TEXT TRANSLATIONS
# =========================================================

MARKET_TEXT = {
    "en": {
        "page_title": "📊 Market Prices & Government Policies",
        "page_subtitle": "Live crop prices, government schemes & cost estimator for smart farming decisions",
        "tab_market": "📈 Live Market Prices",
        "tab_policy": "🏛️ Government Schemes",
        "tab_cost": "💰 Cost Estimator",

        # Market Tab
        "market_title": "📈 Today's Estimated Crop Market Prices",
        "market_desc": "AI-estimated mandi prices based on current season, region & demand trends",
        "select_state": "🌍 Select Your State",
        "select_crop": "🌾 Select Crop",
        "get_prices": "📊 Get Market Prices",
        "price_loading": "⏳ Fetching latest market intelligence...",

        # Policy Tab
        "policy_title": "🏛️ Government Agricultural Schemes & Subsidies",
        "policy_desc": "Find schemes you are eligible for — subsidies, loans, insurance & support programs",
        "select_scheme_type": "📋 Scheme Category",
        "scheme_types": ["All Schemes", "Crop Insurance", "Subsidies & Grants", "Farm Loans", "Soil Health", "Irrigation Support", "MSP & Price Support"],
        "get_schemes": "🔍 Find Government Schemes",
        "policy_loading": "⏳ Searching government agricultural schemes...",

        # Cost Tab
        "cost_title": "💰 Farming Cost & Profit Estimator",
        "cost_desc": "Estimate your farming costs, expected yield & potential profit",
        "input_crop": "🌾 Crop Name",
        "input_area": "📐 Farm Area (acres)",
        "input_season": "🗓️ Season",
        "seasons": ["Kharif (Monsoon)", "Rabi (Winter)", "Zaid (Summer)"],
        "calculate": "💰 Calculate Estimate",
        "cost_loading": "⏳ Calculating farming costs & profit estimate...",

        # States
        "states": [
            "Andhra Pradesh", "Telangana", "Karnataka", "Tamil Nadu",
            "Maharashtra", "Madhya Pradesh", "Uttar Pradesh", "Punjab",
            "Haryana", "Rajasthan", "Gujarat", "Bihar",
            "West Bengal", "Odisha", "Kerala", "Assam"
        ],
        # Common crops
        "crops": [
            "Rice (Paddy)", "Wheat", "Maize (Corn)", "Cotton",
            "Sugarcane", "Soybean", "Groundnut", "Tomato",
            "Onion", "Potato", "Chilli", "Turmeric",
            "Banana", "Mango", "Sunflower", "Jowar (Sorghum)"
        ],
    },
    "te": {
        "page_title": "📊 మార్కెట్ ధరలు & ప్రభుత్వ పథకాలు",
        "page_subtitle": "తాజా పంట ధరలు, ప్రభుత్వ సబ్సిడీలు & వ్యయ అంచనా",
        "tab_market": "📈 మార్కెట్ ధరలు",
        "tab_policy": "🏛️ ప్రభుత్వ పథకాలు",
        "tab_cost": "💰 వ్యయ అంచనా",

        "market_title": "📈 నేటి పంట మార్కెట్ ధరల అంచనా",
        "market_desc": "ప్రస్తుత సీజన్, ప్రాంతం & డిమాండ్ ట్రెండ్ల ఆధారంగా AI అంచనా ధరలు",
        "select_state": "🌍 మీ రాష్ట్రం ఎంచుకోండి",
        "select_crop": "🌾 పంట ఎంచుకోండి",
        "get_prices": "📊 మార్కెట్ ధరలు చూడండి",
        "price_loading": "⏳ తాజా మార్కెట్ సమాచారం తెస్తున్నాము...",

        "policy_title": "🏛️ ప్రభుత్వ వ్యవసాయ పథకాలు & సబ్సిడీలు",
        "policy_desc": "మీకు అర్హత ఉన్న పథకాలను కనుగొనండి — సబ్సిడీలు, రుణాలు, బీమా & మద్దతు కార్యక్రమాలు",
        "select_scheme_type": "📋 పథక వర్గం",
        "scheme_types": ["అన్ని పథకాలు", "పంట బీమా", "సబ్సిడీలు & గ్రాంట్లు", "వ్యవసాయ రుణాలు", "నేల ఆరోగ్యం", "నీటిపారుదల మద్దతు", "MSP & ధర మద్దతు"],
        "get_schemes": "🔍 ప్రభుత్వ పథకాలు చూడండి",
        "policy_loading": "⏳ ప్రభుత్వ వ్యవసాయ పథకాలను వెతుకుతున్నాము...",

        "cost_title": "💰 వ్యవసాయ వ్యయ & లాభ అంచనా",
        "cost_desc": "మీ వ్యవసాయ ఖర్చులు, ఊహించిన దిగుబడి & సంభావ్య లాభాన్ని అంచనా వేయండి",
        "input_crop": "🌾 పంట పేరు",
        "input_area": "📐 పొలం విస్తీర్ణం (ఎకరాలు)",
        "input_season": "🗓️ సీజన్",
        "seasons": ["ఖరీఫ్ (వర్షాకాలం)", "రబీ (శీతాకాలం)", "జైద్ (వేసవి)"],
        "calculate": "💰 అంచనా లెక్కించండి",
        "cost_loading": "⏳ వ్యవసాయ వ్యయాలు & లాభ అంచనా లెక్కిస్తున్నాము...",

        "states": [
            "ఆంధ్రప్రదేశ్", "తెలంగాణ", "కర్ణాటక", "తమిళనాడు",
            "మహారాష్ట్ర", "మధ్యప్రదేశ్", "ఉత్తరప్రదేశ్", "పంజాబ్",
            "హర్యానా", "రాజస్థాన్", "గుజరాత్", "బీహార్",
            "పశ్చిమ బెంగాల్", "ఒడిషా", "కేరళ", "అస్సాం"
        ],
        "crops": [
            "వరి (ధాన్యం)", "గోధుమ", "మొక్కజొన్న", "పత్తి",
            "చెరకు", "సోయాబీన్", "వేరుశనగ", "టమాటో",
            "ఉల్లిపాయ", "బంగాళదుంప", "మిరపకాయ", "పసుపు",
            "అరటి", "మామిడి", "పొద్దుతిరుగుడు", "జొన్న"
        ],
    },
    "hi": {
        "page_title": "📊 बाज़ार भाव & सरकारी योजनाएं",
        "page_subtitle": "ताज़ा फसल भाव, सरकारी सब्सिडी & लागत अनुमान",
        "tab_market": "📈 बाज़ार भाव",
        "tab_policy": "🏛️ सरकारी योजनाएं",
        "tab_cost": "💰 लागत अनुमान",

        "market_title": "📈 आज की फसल बाज़ार भाव",
        "market_desc": "वर्तमान सीजन, क्षेत्र और मांग के आधार पर AI अनुमानित भाव",
        "select_state": "🌍 अपना राज्य चुनें",
        "select_crop": "🌾 फसल चुनें",
        "get_prices": "📊 बाज़ार भाव देखें",
        "price_loading": "⏳ ताज़ा बाज़ार जानकारी ला रहे हैं...",

        "policy_title": "🏛️ सरकारी कृषि योजनाएं और सब्सिडी",
        "policy_desc": "आप किन योजनाओं के पात्र हैं — सब्सिडी, ऋण, बीमा और सहायता कार्यक्रम",
        "select_scheme_type": "📋 योजना श्रेणी",
        "scheme_types": ["सभी योजनाएं", "फसल बीमा", "सब्सिडी और अनुदान", "कृषि ऋण", "मिट्टी स्वास्थ्य", "सिंचाई सहायता", "MSP और मूल्य समर्थन"],
        "get_schemes": "🔍 सरकारी योजनाएं खोजें",
        "policy_loading": "⏳ सरकारी कृषि योजनाएं खोज रहे हैं...",

        "cost_title": "💰 खेती लागत और मुनाफा अनुमान",
        "cost_desc": "अपनी खेती की लागत, अनुमानित उपज और संभावित मुनाफे का अनुमान लगाएं",
        "input_crop": "🌾 फसल का नाम",
        "input_area": "📐 खेत का क्षेत्रफल (एकड़)",
        "input_season": "🗓️ मौसम",
        "seasons": ["खरीफ (बरसात)", "रबी (सर्दी)", "जायद (गर्मी)"],
        "calculate": "💰 अनुमान निकालें",
        "cost_loading": "⏳ खेती लागत और मुनाफा अनुमान निकाल रहे हैं...",

        "states": [
            "आंध्र प्रदेश", "तेलंगाना", "कर्नाटक", "तमिलनाडु",
            "महाराष्ट्र", "मध्य प्रदेश", "उत्तर प्रदेश", "पंजाब",
            "हरियाणा", "राजस्थान", "गुजरात", "बिहार",
            "पश्चिम बंगाल", "ओडिशा", "केरल", "असम"
        ],
        "crops": [
            "धान (चावल)", "गेहूं", "मक्का", "कपास",
            "गन्ना", "सोयाबीन", "मूंगफली", "टमाटर",
            "प्याज", "आलू", "मिर्च", "हल्दी",
            "केला", "आम", "सूरजमुखी", "ज्वार"
        ],
    },
    "ta": {
        "page_title": "📊 சந்தை விலைகள் & அரசு திட்டங்கள்",
        "page_subtitle": "புதிய பயிர் விலைகள், அரசு மானியங்கள் & செலவு மதிப்பீடு",
        "tab_market": "📈 சந்தை விலைகள்",
        "tab_policy": "🏛️ அரசு திட்டங்கள்",
        "tab_cost": "💰 செலவு மதிப்பீடு",

        "market_title": "📈 இன்றைய பயிர் சந்தை விலைகள்",
        "market_desc": "தற்போதைய பருவம், பகுதி & தேவை போக்குகளின் அடிப்படையில் AI மதிப்பீடு",
        "select_state": "🌍 உங்கள் மாநிலத்தை தேர்ந்தெடுக்கவும்",
        "select_crop": "🌾 பயிரை தேர்ந்தெடுக்கவும்",
        "get_prices": "📊 சந்தை விலைகளைப் பார்க்கவும்",
        "price_loading": "⏳ சமீபத்திய சந்தை தகவல்களைப் பெறுகிறது...",

        "policy_title": "🏛️ அரசு வேளாண் திட்டங்கள் & மானியங்கள்",
        "policy_desc": "நீங்கள் பெறக்கூடிய திட்டங்களைக் கண்டறியுங்கள்",
        "select_scheme_type": "📋 திட்ட வகை",
        "scheme_types": ["அனைத்து திட்டங்கள்", "பயிர் காப்பீடு", "மானியங்கள்", "வேளாண் கடன்கள்", "மண் ஆரோக்கியம்", "பாசன ஆதரவு", "MSP & விலை ஆதரவு"],
        "get_schemes": "🔍 அரசு திட்டங்களைக் கண்டறியுங்கள்",
        "policy_loading": "⏳ அரசு வேளாண் திட்டங்களைத் தேடுகிறது...",

        "cost_title": "💰 விவசாய செலவு & லாப மதிப்பீடு",
        "cost_desc": "உங்கள் விவசாய செலவுகள், எதிர்பார்க்கப்படும் விளைச்சல் & சாத்தியமான லாபத்தை மதிப்பிடுங்கள்",
        "input_crop": "🌾 பயிர் பெயர்",
        "input_area": "📐 பண்ணை பரப்பளவு (ஏக்கர்)",
        "input_season": "🗓️ பருவம்",
        "seasons": ["கரிஃப் (பருவமழை)", "ரபி (குளிர்காலம்)", "ஜெய்ட் (கோடைகாலம்)"],
        "calculate": "💰 மதிப்பீடு கணக்கிடுங்கள்",
        "cost_loading": "⏳ விவசாய செலவு & லாப மதிப்பீடு கணக்கிடுகிறது...",

        "states": [
            "ஆந்திரப் பிரதேசம்", "தெலங்கானா", "கர்நாடகா", "தமிழ்நாடு",
            "மகாராஷ்டிரா", "மத்தியப் பிரதேசம்", "உத்தரப் பிரதேசம்", "பஞ்சாப்",
            "ஹரியானா", "ராஜஸ்தான்", "குஜராத்", "பீகார்",
            "மேற்கு வங்காளம்", "ஒடிசா", "கேரளா", "அசாம்"
        ],
        "crops": [
            "நெல்", "கோதுமை", "சோளம்", "பருத்தி",
            "கரும்பு", "சோயாபீன்", "நிலக்கடலை", "தக்காளி",
            "வெங்காயம்", "உருளைக்கிழங்கு", "மிளகாய்", "மஞ்சள்",
            "வாழை", "மாம்பழம்", "சூரியகாந்தி", "ஜோவார்"
        ],
    },
    "kn": {
        "page_title": "📊 ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು & ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು",
        "page_subtitle": "ಹೊಸ ಬೆಳೆ ಬೆಲೆಗಳು, ಸರ್ಕಾರಿ ಸಬ್ಸಿಡಿಗಳು & ವೆಚ್ಚ ಅಂದಾಜು",
        "tab_market": "📈 ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು",
        "tab_policy": "🏛️ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು",
        "tab_cost": "💰 ವೆಚ್ಚ ಅಂದಾಜು",

        "market_title": "📈 ಇಂದಿನ ಬೆಳೆ ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು",
        "market_desc": "ಪ್ರಸ್ತುತ ಋತು, ಪ್ರದೇಶ & ಬೇಡಿಕೆ ಪ್ರವೃತ್ತಿಗಳ ಆಧಾರದ ಮೇಲೆ AI ಅಂದಾಜು",
        "select_state": "🌍 ನಿಮ್ಮ ರಾಜ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "select_crop": "🌾 ಬೆಳೆ ಆಯ್ಕೆಮಾಡಿ",
        "get_prices": "📊 ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳನ್ನು ನೋಡಿ",
        "price_loading": "⏳ ಇತ್ತೀಚಿನ ಮಾರುಕಟ್ಟೆ ಮಾಹಿತಿ ತರುತ್ತಿದ್ದೇವೆ...",

        "policy_title": "🏛️ ಸರ್ಕಾರಿ ಕೃಷಿ ಯೋಜನೆಗಳು & ಸಬ್ಸಿಡಿಗಳು",
        "policy_desc": "ನೀವು ಅರ್ಹರಾಗಿರುವ ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಿ",
        "select_scheme_type": "📋 ಯೋಜನೆ ವರ್ಗ",
        "scheme_types": ["ಎಲ್ಲಾ ಯೋಜನೆಗಳು", "ಬೆಳೆ ವಿಮೆ", "ಸಬ್ಸಿಡಿಗಳು", "ಕೃಷಿ ಸಾಲಗಳು", "ಮಣ್ಣಿನ ಆರೋಗ್ಯ", "ನೀರಾವರಿ ಬೆಂಬಲ", "MSP & ಬೆಲೆ ಬೆಂಬಲ"],
        "get_schemes": "🔍 ಸರ್ಕಾರಿ ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಿ",
        "policy_loading": "⏳ ಸರ್ಕಾರಿ ಕೃಷಿ ಯೋಜನೆಗಳನ್ನು ಹುಡುಕುತ್ತಿದ್ದೇವೆ...",

        "cost_title": "💰 ಕೃಷಿ ವೆಚ್ಚ & ಲಾಭ ಅಂದಾಜು",
        "cost_desc": "ನಿಮ್ಮ ಕೃಷಿ ವೆಚ್ಚಗಳು, ನಿರೀಕ್ಷಿತ ಇಳುವರಿ & ಸಂಭಾವ್ಯ ಲಾಭವನ್ನು ಅಂದಾಜು ಮಾಡಿ",
        "input_crop": "🌾 ಬೆಳೆ ಹೆಸರು",
        "input_area": "📐 ಹೊಲದ ವಿಸ್ತೀರ್ಣ (ಎಕರೆ)",
        "input_season": "🗓️ ಋತು",
        "seasons": ["ಖಾರಿಫ್ (ಮಳೆಗಾಲ)", "ರಬಿ (ಚಳಿಗಾಲ)", "ಜೈದ್ (ಬೇಸಿಗೆ)"],
        "calculate": "💰 ಅಂದಾಜು ಲೆಕ್ಕ ಹಾಕಿ",
        "cost_loading": "⏳ ಕೃಷಿ ವೆಚ್ಚ & ಲಾಭ ಅಂದಾಜು ಲೆಕ್ಕ ಹಾಕುತ್ತಿದ್ದೇವೆ...",

        "states": [
            "ಆಂಧ್ರ ಪ್ರದೇಶ", "ತೆಲಂಗಾಣ", "ಕರ್ನಾಟಕ", "ತಮಿಳುನಾಡು",
            "ಮಹಾರಾಷ್ಟ್ರ", "ಮಧ್ಯ ಪ್ರದೇಶ", "ಉತ್ತರ ಪ್ರದೇಶ", "ಪಂಜಾಬ್",
            "ಹರಿಯಾಣ", "ರಾಜಸ್ಥಾನ", "ಗುಜರಾತ್", "ಬಿಹಾರ",
            "ಪಶ್ಚಿಮ ಬಂಗಾಳ", "ಒಡಿಶಾ", "ಕೇರಳ", "ಅಸ್ಸಾಂ"
        ],
        "crops": [
            "ಭತ್ತ", "ಗೋಧಿ", "ಮೆಕ್ಕೆಜೋಳ", "ಹತ್ತಿ",
            "ಕಬ್ಬು", "ಸೋಯಾಬೀನ್", "ಶೇಂಗಾ", "ಟೊಮೆಟೊ",
            "ಈರುಳ್ಳಿ", "ಆಲೂಗಡ್ಡೆ", "ಮೆಣಸಿನಕಾಯಿ", "ಅರಿಶಿನ",
            "ಬಾಳೆ", "ಮಾವು", "ಸೂರ್ಯಕಾಂತಿ", "ಜೋಳ"
        ],
    },
    "mr": {
        "page_title": "📊 बाजार भाव & सरकारी योजना",
        "page_subtitle": "ताज्या पीक भाव, सरकारी अनुदाने & खर्च अंदाज",
        "tab_market": "📈 बाजार भाव",
        "tab_policy": "🏛️ सरकारी योजना",
        "tab_cost": "💰 खर्च अंदाज",

        "market_title": "📈 आजचे पीक बाजार भाव",
        "market_desc": "सध्याचा हंगाम, प्रदेश आणि मागणीच्या आधारावर AI अंदाजित भाव",
        "select_state": "🌍 तुमचे राज्य निवडा",
        "select_crop": "🌾 पीक निवडा",
        "get_prices": "📊 बाजार भाव पहा",
        "price_loading": "⏳ ताज्या बाजार माहिती आणत आहोत...",

        "policy_title": "🏛️ सरकारी कृषी योजना आणि अनुदाने",
        "policy_desc": "तुम्ही कोणत्या योजनांसाठी पात्र आहात ते शोधा",
        "select_scheme_type": "📋 योजना प्रकार",
        "scheme_types": ["सर्व योजना", "पीक विमा", "अनुदाने", "शेती कर्ज", "माती आरोग्य", "सिंचन सहाय्य", "MSP & किंमत आधार"],
        "get_schemes": "🔍 सरकारी योजना शोधा",
        "policy_loading": "⏳ सरकारी कृषी योजना शोधत आहोत...",

        "cost_title": "💰 शेती खर्च व नफा अंदाज",
        "cost_desc": "तुमचा शेती खर्च, अपेक्षित उत्पादन व संभाव्य नफ्याचा अंदाज लावा",
        "input_crop": "🌾 पिकाचे नाव",
        "input_area": "📐 शेत क्षेत्र (एकर)",
        "input_season": "🗓️ हंगाम",
        "seasons": ["खरीप (पावसाळा)", "रब्बी (हिवाळा)", "उन्हाळी"],
        "calculate": "💰 अंदाज काढा",
        "cost_loading": "⏳ शेती खर्च आणि नफा अंदाज काढत आहोत...",

        "states": [
            "आंध्र प्रदेश", "तेलंगणा", "कर्नाटक", "तामिळनाडू",
            "महाराष्ट्र", "मध्य प्रदेश", "उत्तर प्रदेश", "पंजाब",
            "हरियाणा", "राजस्थान", "गुजरात", "बिहार",
            "पश्चिम बंगाल", "ओडिशा", "केरळ", "आसाम"
        ],
        "crops": [
            "भात (तांदूळ)", "गहू", "मका", "कापूस",
            "ऊस", "सोयाबीन", "भुईमूग", "टोमॅटो",
            "कांदा", "बटाटा", "मिरची", "हळद",
            "केळ", "आंबा", "सूर्यफूल", "ज्वारी"
        ],
    },
}


# =========================================================
# MAIN PAGE FUNCTION
# =========================================================

def show_market_policy():
    """Renders the Government Policy & Live Market page."""

    farmer = st.session_state.get("farmer", {})
    farmer_id = farmer.get("id", 1)
    current_lang = st.session_state.get("selected_language", "English")

    # Get language code for translations
    lang_map = {"English": "en", "తెలుగు": "te", "हिंदी": "hi", "தமிழ்": "ta", "ಕನ್ನಡ": "kn", "मराठी": "mr"}
    lang_code = lang_map.get(current_lang, "en")
    t = MARKET_TEXT.get(lang_code, MARKET_TEXT["en"])

    # =====================================================
    # PAGE HERO HEADER
    # =====================================================
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 60%, #3b82f6 100%); border-radius: 20px; padding: 22px 24px; margin-bottom: 16px; box-shadow: 0 8px 24px rgba(37, 99, 235, 0.25);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div>
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                        <span style="background: rgba(255,255,255,0.20); color: #ffffff; padding: 3px 10px; border-radius: 9999px; font-size: 11px; font-weight: 700; border: 1px solid rgba(255,255,255,0.35);">
                            🏛️ Gov Policies & Market Data
                        </span>
                    </div>
                    <h2 style="color: white !important; margin: 0; font-size: 22px; font-weight: 800;">{t['page_title']}</h2>
                    <p style="color: #bfdbfe; margin: 4px 0 0 0; font-size: 13px; font-weight: 500;">{t['page_subtitle']}</p>
                </div>
                <div style="font-size: 38px;">📊</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # THREE TABS: Market | Policy | Cost Estimator
    # =====================================================
    tab_market, tab_policy, tab_cost = st.tabs([
        t["tab_market"],
        t["tab_policy"],
        t["tab_cost"]
    ])

    # -------------------------------------------------
    # TAB 1: LIVE MARKET PRICES
    # -------------------------------------------------
    with tab_market:
        st.markdown(f"### {t['market_title']}")
        st.caption(t["market_desc"])

        m_col1, m_col2 = st.columns(2)
        with m_col1:
            selected_state = st.selectbox(
                t["select_state"],
                t["states"],
                key="market_state_select"
            )
        with m_col2:
            selected_crop = st.selectbox(
                t["select_crop"],
                t["crops"],
                key="market_crop_select"
            )

        if st.button(t["get_prices"], key="btn_get_market_prices", use_container_width=True, type="primary"):
            with st.spinner(t["price_loading"]):
                market_question = (
                    f"Give me the current estimated mandi/market prices for {selected_crop} in {selected_state}, India. "
                    f"Include: Min price (₹/quintal), Max price (₹/quintal), Modal/average price, "
                    f"which mandi/market yard has best price, price trend (rising/falling/stable), "
                    f"and best time to sell. Present as a clear, structured table/list. "
                    f"Also mention MSP (Minimum Support Price) if applicable."
                )
                try:
                    stream_gen = ask_agrisense_stream(
                        farmer_id=farmer_id,
                        question=market_question,
                        language=current_lang
                    )
                    st.write_stream(stream_gen)
                except Exception as e:
                    st.error(f"Error: {e}")

        # Quick price cards for common crops
        st.markdown("---")
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #ecfdf5, #f0fdf4); border: 1.5px solid #86efac; border-radius: 14px; padding: 16px; margin: 8px 0;">
                <div style="font-size: 13px; font-weight: 700; color: #166534; margin-bottom: 8px;">
                    💡 {"Quick tip: Select your state and crop above, then tap the button to get AI-estimated live market prices!" if lang_code == "en" else "మీ రాష్ట్రం & పంట ఎంచుకుని బటన్ నొక్కండి!" if lang_code == "te" else "अपना राज्य और फसल चुनें!" if lang_code == "hi" else "உங்கள் மாநிலம் & பயிரை தேர்ந்தெடுக்கவும்!" if lang_code == "ta" else "ನಿಮ್ಮ ರಾಜ್ಯ & ಬೆಳೆ ಆಯ್ಕೆಮಾಡಿ!" if lang_code == "kn" else "तुमचे राज्य आणि पीक निवडा!"}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -------------------------------------------------
    # TAB 2: GOVERNMENT SCHEMES & POLICIES
    # -------------------------------------------------
    with tab_policy:
        st.markdown(f"### {t['policy_title']}")
        st.caption(t["policy_desc"])

        scheme_category = st.selectbox(
            t["select_scheme_type"],
            t["scheme_types"],
            key="policy_scheme_type"
        )

        if st.button(t["get_schemes"], key="btn_get_gov_schemes", use_container_width=True, type="primary"):
            with st.spinner(t["policy_loading"]):
                policy_question = (
                    f"List the top government agricultural schemes and subsidies available for Indian farmers "
                    f"under the category: '{scheme_category}'. "
                    f"For each scheme, provide: "
                    f"1. Scheme name (official name), "
                    f"2. What it provides (money/subsidy/insurance amount), "
                    f"3. Eligibility criteria, "
                    f"4. How to apply (step-by-step), "
                    f"5. Official website or helpline number. "
                    f"Focus on Central Government and State Government schemes. "
                    f"Include PM-KISAN, PMFBY, KCC, Soil Health Card, PM-KUSUM etc where relevant."
                )
                try:
                    stream_gen = ask_agrisense_stream(
                        farmer_id=farmer_id,
                        question=policy_question,
                        language=current_lang
                    )
                    st.write_stream(stream_gen)
                except Exception as e:
                    st.error(f"Error: {e}")

        # Key Schemes Quick Cards
        st.markdown("---")

        schemes_data = [
            ("🌾 PM-KISAN", "₹6,000/year", "pm-kisan"),
            ("🛡️ PMFBY", "Crop Insurance", "pmfby"),
            ("💳 KCC", "Farm Credit Card", "kcc"),
            ("🧪 Soil Health", "Free Soil Testing", "soil-health"),
        ]

        scheme_cols = st.columns(4)
        for idx, (name, benefit, key) in enumerate(schemes_data):
            with scheme_cols[idx]:
                colors = ["#dcfce7", "#dbeafe", "#fef3c7", "#fce7f3"]
                borders = ["#86efac", "#93c5fd", "#fde68a", "#f9a8d4"]
                text_colors = ["#166534", "#1e40af", "#92400e", "#9d174d"]
                st.markdown(
                    f"""
                    <div style="background: {colors[idx]}; border: 1.5px solid {borders[idx]}; border-radius: 12px; padding: 12px; text-align: center;">
                        <div style="font-size: 14px; font-weight: 800; color: {text_colors[idx]};">{name}</div>
                        <div style="font-size: 12px; font-weight: 600; color: {text_colors[idx]}; opacity: 0.8; margin-top: 4px;">{benefit}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # -------------------------------------------------
    # TAB 3: COST ESTIMATOR
    # -------------------------------------------------
    with tab_cost:
        st.markdown(f"### {t['cost_title']}")
        st.caption(t["cost_desc"])

        c_col1, c_col2, c_col3 = st.columns(3)
        with c_col1:
            cost_crop = st.selectbox(
                t["input_crop"],
                t["crops"],
                key="cost_crop_select"
            )
        with c_col2:
            cost_area = st.number_input(
                t["input_area"],
                min_value=0.5,
                max_value=500.0,
                value=2.0,
                step=0.5,
                key="cost_area_input"
            )
        with c_col3:
            cost_season = st.selectbox(
                t["input_season"],
                t["seasons"],
                key="cost_season_select"
            )

        if st.button(t["calculate"], key="btn_calculate_cost", use_container_width=True, type="primary"):
            with st.spinner(t["cost_loading"]):
                cost_question = (
                    f"Calculate the detailed farming cost and profit estimate for growing {cost_crop} "
                    f"on {cost_area} acres of land during {cost_season} season in India. "
                    f"Break down the costs into: "
                    f"1. Land preparation cost, "
                    f"2. Seed cost, "
                    f"3. Fertilizer & Pesticide cost, "
                    f"4. Irrigation cost, "
                    f"5. Labour cost, "
                    f"6. Total investment, "
                    f"7. Expected yield (quintals), "
                    f"8. Expected market price per quintal, "
                    f"9. Total expected revenue, "
                    f"10. Net profit/loss. "
                    f"Present all amounts in Indian Rupees (₹). Make it practical and realistic."
                )
                try:
                    stream_gen = ask_agrisense_stream(
                        farmer_id=farmer_id,
                        question=cost_question,
                        language=current_lang
                    )
                    st.write_stream(stream_gen)
                except Exception as e:
                    st.error(f"Error: {e}")
