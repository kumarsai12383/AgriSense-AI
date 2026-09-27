"""
AgriSense AI — Official Government Schemes & Subsidies Portal
=============================================================
Provides a dedicated, presentation-grade Government Agricultural Schemes page
with authentic Ministry of Agriculture imagery, official national schemes (PM-KISAN,
PMFBY, KCC, PM-KUSUM, Soil Health Card, SMAM), state-wise agricultural subsidies,
eligibility filters, and AI-powered scheme advisory.

Fully localized in 6 Indian languages: English, Telugu, Hindi, Tamil, Kannada, Marathi.
"""

import os
import base64
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import streamlit as st
from modules.ai_engine import ask_agrisense_stream


# =========================================================
# HELPER: LOAD BACKGROUND IMAGE AS BASE64 (CACHED FOR INSTANT SPEED)
# =========================================================

@st.cache_data
def _get_bg_base64():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_path = os.path.join(base_dir, "images", "gov_schemes_bg.jpg")
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""


# =========================================================
# MULTILINGUAL TRANSLATIONS FOR GOVERNMENT SCHEMES
# =========================================================

GOV_TEXT = {
    "en": {
        "portal_badge": "🏛️ Ministry of Agriculture & Farmers Welfare | Govt. of India",
        "page_title": "Government Schemes & Subsidies",
        "page_subtitle": "Official financial support, crop insurance, equipment subsidies & welfare programs for Indian farmers",
        "search_label": "🔍 Search Schemes by Name or Keyword",
        "category_label": "📋 Filter by Scheme Category",
        "state_label": "📍 Select State for State-Specific Schemes",
        "btn_check_eligibility": "🤖 Check My Scheme Eligibility with AI",
        "btn_find_schemes": "🔍 Find Schemes for My Farm",
        "loading_schemes": "⏳ Consulting Ministry of Agriculture guidelines...",
        "official_helpline": "📞 Farmer Welfare Toll-Free Helpline: 1800-180-1551 / 155261",
        "filter_all": "All Schemes",
        "filter_income": "Direct Income & Grants (₹)",
        "filter_insurance": "Crop Insurance & Risk 🛡️",
        "filter_credit": "Farm Credit & Loans 💳",
        "filter_machinery": "Solar & Machinery Subsidies 🚜",
        "filter_soil_water": "Soil & Water Conservation 💧",
        "eligibility_title": "🎯 Instant AI Eligibility Checker",
        "eligibility_desc": "Enter your farm details to get an instant personalized list of schemes you qualify for with step-by-step application guidance.",
        "farm_size": "Farm Size (Acres)",
        "farm_crop": "Primary Crop",
        "farmer_category": "Farmer Category",
        "categories": ["Small / Marginal Farmer (< 5 acres)", "Medium Farmer (5-10 acres)", "Large Farmer (> 10 acres)", "Women Farmer", "Tenant / Sharecropper"],
        "tab_featured": "🌟 Key National Schemes",
        "tab_state": "📍 State Welfare Schemes",
        "tab_ai": "🤖 AI Scheme Advisor",
    },
    "te": {
        "portal_badge": "🏛️ వ్యవసాయం & రైతు సంక్షేమ మంత్రిత్వ శాఖ | భారత ప్రభుత్వం",
        "page_title": "ప్రభుత్వ పథకాలు & సబ్సిడీలు",
        "page_subtitle": "రైతుల కోసం అధికారిక ఆర్థిక సహాయం, పంట బీమా, పరికరాల సబ్సిడీలు & సంక్షేమ పథకాలు",
        "search_label": "🔍 పథకం పేరు లేదా కీవర్డ్ తో శోధించండి",
        "category_label": "📋 పథక వర్గం ద్వారా ఫిల్టర్ చేయండి",
        "state_label": "📍 రాష్ట్ర స్థాయి పథకాల కోసం రాష్ట్రాన్ని ఎంచుకోండి",
        "btn_check_eligibility": "🤖 AI తో నా అర్హతను తనిఖీ చేయండి",
        "btn_find_schemes": "🔍 నా పొలానికి పథకాలు కనుగొనండి",
        "loading_schemes": "⏳ వ్యవసాయ శాఖ మార్గదర్శకాలను పరిశీలిస్తున్నాము...",
        "official_helpline": "📞 రైతు సంక్షేమ టోల్ ఫ్రీ హెల్ప్‌లైన్: 1800-180-1551 / 155261",
        "filter_all": "అన్ని పథకాలు",
        "filter_income": "నేరుగా నగదు బదిలీ (₹)",
        "filter_insurance": "పంట బీమా & రక్షణ 🛡️",
        "filter_credit": "వ్యవసాయ రుణాలు 💳",
        "filter_machinery": "సోలార్ & యంత్రాల సబ్సిడీ 🚜",
        "filter_soil_water": "నేల & నీటి సంరక్షణ 💧",
        "eligibility_title": "🎯 తక్షణ AI అర్హత తనిఖీ",
        "eligibility_desc": "మీ పొలం వివరాలను నమోదు చేసి, మీరు అర్హులైన పథకాల జాబితా మరియు దరఖాస్తు విధానాన్ని పొందండి.",
        "farm_size": "పొలం విస్తీర్ణం (ఎకరాలు)",
        "farm_crop": "ప్రధాన పంట",
        "farmer_category": "రైతు వర్గం",
        "categories": ["చిన్న / సన్నకారు రైతు (< 5 ఎకరాలు)", "మధ్యతరహా రైతు (5-10 ఎకరాలు)", "పెద్ద రైతు (> 10 ఎకరాలు)", "మహిళా రైతు", "కౌలు రైతు"],
        "tab_featured": "🌟 ప్రధాన జాతీయ పథకాలు",
        "tab_state": "📍 రాష్ట్ర సంక్షేమ పథకాలు",
        "tab_ai": "🤖 AI పథక సలహాదారు",
    },
    "hi": {
        "portal_badge": "🏛️ कृषि एवं किसान कल्याण मंत्रालय | भारत सरकार",
        "page_title": "सरकारी योजनाएं और सब्सिडी",
        "page_subtitle": "भारतीय किसानों के लिए आधिकारिक वित्तीय सहायता, फसल बीमा, कृषि उपकरण सब्सिडी और कल्याणकारी योजनाएं",
        "search_label": "🔍 योजना का नाम या कीवर्ड खोजें",
        "category_label": "📋 योजना श्रेणी चुनें",
        "state_label": "📍 राज्य स्तरीय योजनाओं के लिए राज्य चुनें",
        "btn_check_eligibility": "🤖 AI से अपनी पात्रता जांचें",
        "btn_find_schemes": "🔍 मेरे खेत के लिए योजनाएं खोजें",
        "loading_schemes": "⏳ कृषि मंत्रालय के दिशा-निर्देश देखे जा रहे हैं...",
        "official_helpline": "📞 किसान कल्याण टोल-फ्री हेल्पलाइन: 1800-180-1551 / 155261",
        "filter_all": "सभी योजनाएं",
        "filter_income": "प्रत्यक्ष आय और अनुदान (₹)",
        "filter_insurance": "फसल बीमा और सुरक्षा 🛡️",
        "filter_credit": "कृषि ऋण और क्रेडिट कार्ड 💳",
        "filter_machinery": "सोलर पंप और मशीनरी सब्सिडी 🚜",
        "filter_soil_water": "मिट्टी और जल संरक्षण 💧",
        "eligibility_title": "🎯 तत्काल AI पात्रता चेकर",
        "eligibility_desc": "अपने खेत की जानकारी दर्ज करें और तुरंत जानें कि आप किन योजनाओं के पात्र हैं और आवेदन कैसे करें।",
        "farm_size": "खेत का आकार (एकड़)",
        "farm_crop": "मुख्य फसल",
        "farmer_category": "किसान श्रेणी",
        "categories": ["लघु एवं सीमांत किसान (< 5 एकड़)", "मध्यम किसान (5-10 एकड़)", "बड़े किसान (> 10 एकड़)", "महिला किसान", "बटाईदार / पट्टेदार"],
        "tab_featured": "🌟 प्रमुख राष्ट्रीय योजनाएं",
        "tab_state": "📍 राज्य कल्याणकारी योजनाएं",
        "tab_ai": "🤖 AI योजना सलाहकार",
    },
    "ta": {
        "portal_badge": "🏛️ வேளாண்மை மற்றும் உழவர் நல அமைச்சகம் | இந்திய அரசு",
        "page_title": "அரசு திட்டங்கள் மற்றும் மானியங்கள்",
        "page_subtitle": "விவசாயிகளுக்கான நேரடி பண உதவி, பயிர் காப்பீடு, உபகரண மானியங்கள் மற்றும் நலத்திட்டங்கள்",
        "search_label": "🔍 திட்டத்தின் பெயர் கொண்டு தேடவும்",
        "category_label": "📋 திட்ட வகை",
        "state_label": "📍 மாநில வாரியான திட்டங்களுக்கு மாநிலத்தைத் தேர்ந்தெடுக்கவும்",
        "btn_check_eligibility": "🤖 AI மூலம் என் தகுதியை சரிபார்க்கவும்",
        "btn_find_schemes": "🔍 என் பண்ணைக்கான திட்டங்களைக் கண்டறியவும்",
        "loading_schemes": "⏳ வேளாண் அமைச்சக வழிகாட்டுதல்கள் பெறப்படுகின்றன...",
        "official_helpline": "📞 உழவர் நல இலவச உதவி எண்: 1800-180-1551 / 155261",
        "filter_all": "அனைத்து திட்டங்கள்",
        "filter_income": "நேரடி வருமான உதவி (₹)",
        "filter_insurance": "பயிர் காப்பீடு 🛡️",
        "filter_credit": "விவசாய கடன் மற்றும் அட்டை 💳",
        "filter_machinery": "சோலார் மற்றும் இயந்திர மானியம் 🚜",
        "filter_soil_water": "மண் மற்றும் நீர் பாதுகாப்பு 💧",
        "eligibility_title": "🎯 உடனடி AI தகுதி சரிபார்ப்பு",
        "eligibility_desc": "உங்கள் பண்ணை விவரங்களை உள்ளிட்டு நீங்கள் தகுதியுள்ள திட்டங்கள் மற்றும் விண்ணப்பிக்கும் வழிகளைப் பெறுங்கள்.",
        "farm_size": "பண்ணை அளவு (ஏக்கர்)",
        "farm_crop": "முக்கிய பயிர்",
        "farmer_category": "விவசாயி வகை",
        "categories": ["சிறு/குறு விவசாயி (< 5 ஏக்கர்)", "நடுத்தர விவசாயி (5-10 ஏக்கர்)", "பெரிய விவசாயி (> 10 ஏக்கர்)", "பெண் விவசாயி", "குத்தகை விவசாயி"],
        "tab_featured": "🌟 முதன்மை தேசிய திட்டங்கள்",
        "tab_state": "📍 மாநில நலத்திட்டங்கள்",
        "tab_ai": "🤖 AI திட்ட ஆலோசகர்",
    },
    "kn": {
        "portal_badge": "🏛️ ಕೃಷಿ ಮತ್ತು ರೈತರ ಕಲ್ಯಾಣ ಸಚಿವಾಲಯ | ಭಾರತ ಸರ್ಕಾರ",
        "page_title": "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು ಮತ್ತು ಸಬ್ಸಿಡಿಗಳು",
        "page_subtitle": "ರೈತರಿಗೆ ಅಧಿಕೃತ ಆರ್ಥಿಕ ನೆರವು, ಬೆಳೆ ವಿಮೆ, ಉಪಕರಣ ಸಬ್ಸಿಡಿ ಮತ್ತು ಕಲ್ಯಾಣ ಕಾರ್ಯಕ್ರಮಗಳು",
        "search_label": "🔍 ಯೋಜನೆಯ ಹೆಸರು ಹುಡುಕಿ",
        "category_label": "📋 ಯೋಜನೆ ವರ್ಗ",
        "state_label": "📍 ರಾಜ್ಯ ಯೋಜನೆಗಳಿಗಾಗಿ ರಾಜ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "btn_check_eligibility": "🤖 AI ಮೂಲಕ ನನ್ನ ಅರ್ಹತೆ ಪರಿಶೀಲಿಸಿ",
        "btn_find_schemes": "🔍 ನನ್ನ ಜಮೀನಿಗೆ ಸೂಕ್ತ ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಿ",
        "loading_schemes": "⏳ ಕೃಷಿ ಸಚಿವಾಲಯದ ಮಾರ್ಗಸೂಚಿಗಳನ್ನು ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ...",
        "official_helpline": "📞 ರೈತ ಕಲ್ಯಾಣ ಉಚಿತ ಸಹಾಯವಾಣಿ: 1800-180-1551 / 155261",
        "filter_all": "ಎಲ್ಲಾ ಯೋಜನೆಗಳು",
        "filter_income": "ನೇರ ಆದಾಯ ಬೆಂಬಲ (₹)",
        "filter_insurance": "ಬೆಳೆ ವಿಮೆ ಮತ್ತು ರಕ್ಷಣೆ 🛡️",
        "filter_credit": "ಕೃಷಿ ಸಾಲ ಮತ್ತು ಕಾರ್ಡ್ 💳",
        "filter_machinery": "ಸೌರ ಮತ್ತು ಯಂತ್ರೋಪಕರಣ ಸಬ್ಸಿಡಿ 🚜",
        "filter_soil_water": "ಮಣ್ಣು ಮತ್ತು ನೀರು ಸಂರಕ್ಷಣೆ 💧",
        "eligibility_title": "🎯 ತ್ವರಿತ AI ಅರ್ಹತೆ ಪರೀಕ್ಷಕ",
        "eligibility_desc": "ನಿಮ್ಮ ಕೃಷಿ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ ಮತ್ತು ನೀವು ಅರ್ಹರಾಗಿರುವ ಯೋಜನೆಗಳು ಮತ್ತು ಅರ್ಜಿ ವಿಧಾನವನ್ನು ತಿಳಿಯಿರಿ.",
        "farm_size": "ಜಮೀನಿನ ವಿಸ್ತೀರ್ಣ (ಎಕರೆ)",
        "farm_crop": "ಮುಖ್ಯ ಬೆಳೆ",
        "farmer_category": "ರೈತರ ವರ್ಗ",
        "categories": ["ಸಣ್ಣ ಮತ್ತು ಅತಿ ಸಣ್ಣ ರೈತರು (< 5 ಎಕರೆ)", "ಮಧ್ಯಮ ರೈತರು (5-10 ಎಕರೆ)", "ದೊಡ್ಡ ರೈತರು (> 10 ಎಕರೆ)", "ಮಹಿಳಾ ರೈತರು", "ಗೇಣಿ ರೈತರು"],
        "tab_featured": "🌟 ಪ್ರಮುಖ ರಾಷ್ಟ್ರೀಯ ಯೋಜನೆಗಳು",
        "tab_state": "📍 ರಾಜ್ಯ ಕಲ್ಯಾಣ ಯೋಜನೆಗಳು",
        "tab_ai": "🤖 AI ಯೋಜನೆ ಸಲಹೆಗಾರ",
    },
    "mr": {
        "portal_badge": "🏛️ कृषी व शेतकरी कल्याण मंत्रालय | भारत सरकार",
        "page_title": "सरकारी योजना आणि अनुदाने",
        "page_subtitle": "शेतकऱ्यांसाठी अधिकृत आर्थिक मदत, पीक विमा, अवजारे अनुदाने आणि कल्याणकारी योजना",
        "search_label": "🔍 योजनेचे नाव किंवा कीवर्ड शोधा",
        "category_label": "📋 योजना प्रकार",
        "state_label": "📍 राज्यस्तरीय योजनांसाठी राज्य निवडा",
        "btn_check_eligibility": "🤖 AI द्वारे माझी पात्रता तपासा",
        "btn_find_schemes": "🔍 माझ्या शेतीसाठी योजना शोधा",
        "loading_schemes": "⏳ कृषी मंत्रालय मार्गदर्शक तत्त्वे तपासत आहोत...",
        "official_helpline": "📞 शेतकरी कल्याण टोल-फ्री हेल्पलाइन: 1800-180-1551 / 155261",
        "filter_all": "सर्व योजना",
        "filter_income": "थेट उत्पन्न आणि अनुदान (₹)",
        "filter_insurance": "पीक विमा आणि संरक्षण 🛡️",
        "filter_credit": "शेती कर्ज आणि क्रेडिट कार्ड 💳",
        "filter_machinery": "सोलर पंप आणि यंत्रसामग्री अनुदान 🚜",
        "filter_soil_water": "माती आणि जलसंधारण 💧",
        "eligibility_title": "🎯 झटपट AI पात्रता चेकर",
        "eligibility_desc": "आपल्या शेतीची माहिती प्रविष्ट करा आणि आपण कोणत्या योजनांसाठी पात्र आहात ते त्वरित जाणून घ्या.",
        "farm_size": "शेत क्षेत्र (एकर)",
        "farm_crop": "मुख्य पीक",
        "farmer_category": "शेतकरी प्रवर्ग",
        "categories": ["अल्प व अल्पभूधारक शेतकरी (< ५ एकर)", "मध्यम शेतकरी (५-१० एकर)", "मोठे शेतकरी (> १० एकर)", "महिला शेतकरी", "कुळ / भाडेकरू"],
        "tab_featured": "🌟 प्रमुख राष्ट्रीय योजना",
        "tab_state": "📍 राज्य कल्याणकारी योजना",
        "tab_ai": "🤖 AI योजना सल्लागार",
    }
}

# =========================================================
# COMPREHENSIVE SCHEMES DATA STORE
# =========================================================

NATIONAL_SCHEMES = [
    {
        "id": "pm_kisan",
        "category": "income",
        "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "benefit": "₹6,000 / year (Direct Bank Transfer in 3 instalments of ₹2,000)",
        "eligibility": "All landholding farmer families with cultivable land in their name.",
        "documents": "Aadhaar Card, Land ownership papers (Pahani/7/12/Patta), Bank Account linked with Aadhaar.",
        "portal": "https://pmkisan.gov.in",
        "helpline": "155261 / 1800-115-526",
        "badge_color": "#166534",
        "badge_bg": "#dcfce7",
        "icon": "🌾"
    },
    {
        "id": "pmfby",
        "category": "insurance",
        "name": "PMFBY (Pradhan Mantri Fasal Bima Yojana)",
        "benefit": "Comprehensive crop insurance against droughts, floods, pests & natural calamities. Low premium: 2% (Kharif), 1.5% (Rabi), 5% (Commercial/Horticulture).",
        "eligibility": "All farmers growing notified crops in notified areas including sharecroppers and tenant farmers.",
        "documents": "Land record (ROR/LPC), Sowing Certificate, Bank passbook, Aadhaar.",
        "portal": "https://pmfby.gov.in",
        "helpline": "1800-180-1551",
        "badge_color": "#1e40af",
        "badge_bg": "#dbeafe",
        "icon": "🛡️"
    },
    {
        "id": "kcc",
        "category": "credit",
        "name": "KCC (Kisan Credit Card)",
        "benefit": "Low-interest institutional credit up to ₹3,00,000 at effective 4% interest rate (after 3% prompt repayment incentive). Collateral-free loan up to ₹1.60 Lakh.",
        "eligibility": "All farmers, individual/joint borrowers, tenant farmers, oral lessees & sharecroppers, SHGs.",
        "documents": "Duly filled application form, Identity & Address proof (Aadhaar, Voter ID), Land record certified by revenue authorities.",
        "portal": "https://myscheme.gov.in/schemes/kcc",
        "helpline": "1800-11-2211 / Nearest Bank Branch",
        "badge_color": "#92400e",
        "badge_bg": "#fef3c7",
        "icon": "💳"
    },
    {
        "id": "pm_kusum",
        "category": "machinery",
        "name": "PM-KUSUM (Pradhan Mantri Kisan Urja Suraksha evam Utthaan Mahabhiyan)",
        "benefit": "Up to 60% Central + State subsidy for standalone solar agriculture pumps (3HP, 5HP, 7.5HP) + 30% bank loan. Farmer only pays 10% upfront!",
        "eligibility": "Individual farmers, groups of farmers, cooperatives, panchayats, FPOs and Water User Associations.",
        "documents": "Aadhaar Card, Land documents, Bank Passbook, Electricity connection proof (if grid-connected).",
        "portal": "https://pmkusum.mnre.gov.in",
        "helpline": "1800-180-3333",
        "badge_color": "#c2410c",
        "badge_bg": "#ffedd5",
        "icon": "☀️"
    },
    {
        "id": "smam",
        "category": "machinery",
        "name": "SMAM (Sub-Mission on Agricultural Mechanization)",
        "benefit": "40% to 80% government subsidy on purchase of Tractors, Power Tillers, Rotavators, Harvesters, Drone spraying equipment and Custom Hiring Centers.",
        "eligibility": "Small, marginal, SC/ST, and women farmers receive highest preference and maximum subsidy rates.",
        "documents": "Aadhaar, Land documents, Bank details, Caste certificate (for SC/ST), Passport photo.",
        "portal": "https://agrimachinery.nic.in",
        "helpline": "1800-180-1551",
        "badge_color": "#4338ca",
        "badge_bg": "#e0e7ff",
        "icon": "🚜"
    },
    {
        "id": "soil_health",
        "category": "soil_water",
        "name": "Soil Health Card Scheme (National Mission for Sustainable Agriculture)",
        "benefit": "Free lab testing of 12 soil parameters (N, P, K, S, Zn, Fe, Cu, Mn, Bo, pH, EC, OC) + tailored fertilizer dosage recommendations to reduce input costs by 15-25%.",
        "eligibility": "Every agricultural landholder across all states in India.",
        "documents": "Land record number/Khata number, Soil sample collected by village agriculture officer.",
        "portal": "https://soilhealth.dac.gov.in",
        "helpline": "Contact Local Krishi Vigyan Kendra (KVK)",
        "badge_color": "#065f46",
        "badge_bg": "#d1fae5",
        "icon": "🧪"
    },
    {
        "id": "pmksy",
        "category": "soil_water",
        "name": "PMKSY (Per Drop More Crop - Pradhan Mantri Krishi Sinchayee Yojana)",
        "benefit": "55% subsidy for Small & Marginal farmers and 45% for other farmers on Drip and Sprinkler micro-irrigation systems. Saves up to 40% water and boosts yield by 30%.",
        "eligibility": "Farmers with valid land ownership and an assured water source on their farm.",
        "documents": "Aadhaar card, Land title deed, Water availability certificate, Bank passbook.",
        "portal": "https://pmksy.gov.in",
        "helpline": "District Horticulture / Agriculture Officer",
        "badge_color": "#0369a1",
        "badge_bg": "#e0f2fe",
        "icon": "💧"
    },
    {
        "id": "pkvy",
        "category": "soil_water",
        "name": "PKVY (Paramparagat Krishi Vikas Yojana - Organic Farming)",
        "benefit": "Financial assistance of ₹50,000 per hectare over 3 years for organic farming clusters, PGS organic certification, biological inputs, and marketing support.",
        "eligibility": "Groups of 20-50 farmers forming a 50-acre contiguous cluster.",
        "documents": "Group formation resolution, Member Aadhaar copies, Cluster GPS coordinates.",
        "portal": "https://pgsindia-ncof.gov.in",
        "helpline": "Contact State Agriculture Department",
        "badge_color": "#15803d",
        "badge_bg": "#f0fdf4",
        "icon": "🌱"
    }
]

STATE_SCHEMES = {
    "Andhra Pradesh": [
        {"name": "YSR Rythu Bharosa - PM KISAN", "benefit": "₹13,500/year per farmer family (including ₹6,000 PM-KISAN + ₹7,500 state grant). Also covers tenant farmers.", "portal": "ysrrythubharosa.ap.gov.in"},
        {"name": "Free 9-Hours Daytime Agricultural Power", "benefit": "100% free electricity for irrigation pump-sets up to 10HP.", "portal": "apcpdcl.in"},
        {"name": "YSR Sunna Vaddi Panta Runalu", "benefit": "Zero-interest crop loans up to ₹1,00,000 on prompt repayment.", "portal": "apagrisnet.gov.in"}
    ],
    "Telangana": [
        {"name": "Rythu Bandhu (Farmer Investment Support)", "benefit": "₹10,000 per acre per year (₹5,000 Kharif + ₹5,000 Rabi) directly credited to bank account.", "portal": "rythubandhu.telangana.gov.in"},
        {"name": "Rythu Bima (Group Life Insurance)", "benefit": "₹5,00,000 life insurance coverage for farmers aged 18-59 with 100% government paid premium.", "portal": "rythubima.telangana.gov.in"},
        {"name": "24x7 Free Agricultural Power Supply", "benefit": "Round-the-clock free uninterrupted three-phase electricity for all farm pump-sets.", "portal": "tssouthernpower.com"}
    ],
    "Karnataka": [
        {"name": "Raitha Siri Scheme", "benefit": "₹10,000 per hectare incentive directly to millet-growing farmers.", "portal": "raitamitra.karnataka.gov.in"},
        {"name": "Krishi Bhagya", "benefit": "Up to 80% subsidy for construction of Farm Ponds (Krishi Honda) with polythene lining and diesel pumps in dryland areas.", "portal": "raitamitra.karnataka.gov.in"},
        {"name": "Ganga Kalyana Scheme", "benefit": "Free borewell drilling with submersible pump installation for SC/ST and OBC small/marginal farmers.", "portal": "kmdc.karnataka.gov.in"}
    ],
    "Tamil Nadu": [
        {"name": "Chief Minister's Uzhavar Pathukappu Thittam", "benefit": "Comprehensive social security, accidental death assistance (₹1,00,000), monthly old-age pension for farm labourers.", "portal": "tn.gov.in/scheme/data_view/11833"},
        {"name": "Free Agricultural Power & Solar Subsidy", "benefit": "Free power for farm pumps + 70% subsidy for solar water pumping systems.", "portal": "tangedco.gov.in"},
        {"name": "Uzhavar Sandhai Direct Farm Marketing", "benefit": "Free retail stalls and weighing scales in state markets to sell directly to consumers without middleman commissions.", "portal": "agritech.tnau.ac.in"}
    ],
    "Maharashtra": [
        {"name": "Namo Shetkari Mahasanman Nidhi Yojana", "benefit": "Additional ₹6,000/year from Maharashtra State Government on top of ₹6,000 PM-KISAN (Total ₹12,000/year).", "portal": "mahadbt.maharashtra.gov.in"},
        {"name": "Magel Tyala Shet Tale (Farm Pond On Demand)", "benefit": "Direct subsidy grant of up to ₹50,000 for digging farm pond to harvest rainwater.", "portal": "krishi.maharashtra.gov.in"},
        {"name": "Gopinath Munde Shetkari Apghat Vima", "benefit": "₹2,00,000 accidental death/disability insurance cover for farmers with 100% state funded premium.", "portal": "krishi.maharashtra.gov.in"}
    ],
    "Uttar Pradesh": [
        {"name": "UP Krishi Yantra Subsidy", "benefit": "Up to 50% DBT subsidy on purchase of modern farm machinery and rotavators.", "portal": "upagriculture.com"},
        {"name": "Kisan Pension Yojana", "benefit": "Monthly pension of ₹500 for small and destitute farmers aged 60+.", "portal": "sspy-up.gov.in"}
    ],
    "Madhya Pradesh": [
        {"name": "Mukhya Mantri Kisan Kalyan Yojana", "benefit": "Additional ₹6,000/year state grant in 3 equal installments matching PM-KISAN (Total ₹12,000/year).", "portal": "saara.mp.gov.in"},
        {"name": "Bhavantar Bhugtan Yojana", "benefit": "Direct cash transfer compensating the price difference if market rate falls below MSP.", "portal": "mpkrishi.mp.gov.in"}
    ],
    "Punjab": [
        {"name": "Crop Residue Management (CRM) Subsidy", "benefit": "50% to 80% subsidy on Happy Seeder, Super Seeder, Straw Management Systems to stop stubble burning.", "portal": "agrimachinerypb.com"},
        {"name": "Pani Bachao Paisa Kamao", "benefit": "Direct incentive in bank account for saving electricity and groundwater on tubewells.", "portal": "pspcl.in"}
    ],
    "Haryana": [
        {"name": "Mera Pani Meri Virasat", "benefit": "₹7,000 per acre financial incentive for farmers switching from water-intensive paddy to maize, pulses or cotton.", "portal": "fasal.haryana.gov.in"},
        {"name": "Bhavantar Bharpai Yojana (BBY)", "benefit": "Risk mitigation scheme ensuring minimum guaranteed price for vegetables and fruits.", "portal": "hortharyana.gov.in"}
    ]
}


# =========================================================
# OFFICIAL VERIFIED SCHEME GUIDES & RESILIENT FALLBACKS
# =========================================================

OFFICIAL_SCHEME_GUIDES = {
    "pm_kisan": """
### 🌾 PM-KISAN (Pradhan Mantri Kisan Samman Nidhi) — Official Guide
**💰 Financial Benefit:** ₹6,000 / year via Direct Benefit Transfer (DBT) directly into your Aadhaar-linked bank account (3 equal installments of ₹2,000 each: April–July, August–November, December–March).

**🎯 Who is Eligible?**
* All landholding farmer families with cultivable land recorded in their name in revenue records.
* Both small, marginal, and large farmers qualify.
* (Ineligible: Institutional landholders, serving/retired government employees, income tax payers).

**📋 Essential Steps to Receive Your ₹6,000 Instantly:**
1. **Complete e-KYC (Mandatory)**:
   - Visit official portal: [pmkisan.gov.in](https://pmkisan.gov.in)
   - Click on **'e-KYC'** in the Farmer Corner.
   - Enter your 12-digit Aadhaar number and enter the OTP received on your mobile.
   - Or visit nearest CSC / MeeSeva center for biometric fingerprint e-KYC.
2. **Aadhaar-Bank NPCI Seeding**:
   - Ensure your bank account is mapped to **Aadhaar NPCI DBT mapper** at your bank branch. Without this, DBT money cannot be credited.
3. **Land Record Seeding**:
   - Verify that your Patta / Pahani / 7/12 land record is seeded by the local Village Agriculture Officer (VAA/AEO).
4. **Track Payment Status**:
   - Visit [pmkisan.gov.in](https://pmkisan.gov.in) -> **'Know Your Status'** -> Enter Registration Number.

**📞 Official Helpline:** 155261 / 1800-115-526 | Kisan Call Centre: 1800-180-1551 (Toll-Free)
""",
    "pm_kusum": """
### ☀️ PM-KUSUM Solar Agricultural Pumps (60% to 80% Subsidy)
**💰 Financial Benefit:**
* Standalone Solar Agricultural Pumps (3 HP, 5 HP, 7.5 HP):
  - **Central Government Subsidy:** 30% of benchmark cost
  - **State Government Subsidy:** 30% to 50% (Total subsidy reaches 60% to 80%!)
  - **Bank Loan Available:** Up to 30%
  - **Farmer Upfront Share:** Only 10% to 20%!

**🚜 Benefits for Farmers:**
* Daytime reliable irrigation without power cuts or low voltage.
* Replaces expensive diesel pumps, saving ₹30,000 to ₹60,000 annually in fuel.
* Can be easily connected to Drip and Sprinkler systems.

**📄 Required Documents:**
1. Aadhaar Card
2. Land Ownership Document (Patta / Pahani / 7/12)
3. Bank Account Passbook
4. Water source certificate (Borewell or Open Well NOC)
5. Passport size photograph

**🌐 How to Apply:**
* Apply on the official Ministry of New and Renewable Energy portal: [pmkusum.mnre.gov.in](https://pmkusum.mnre.gov.in) or your State Renewable Energy Agency (NREDCAP in AP, REDCO in Telangana, KREDL in Karnataka, MEDA in Maharashtra).

**📞 Helpline:** 1800-180-3333 (MNRE Toll-Free)
""",
    "pmfby": """
### 🛡️ PMFBY (Pradhan Mantri Fasal Bima Yojana) — Crop Insurance & Claims
**💰 Financial Protection:**
* Comprehensive insurance cover against yield loss due to non-preventable natural risks:
  - Prevented Sowing / Planting risk
  - Standing crop loss (Drought, Flood, Pests & Diseases, Landslide, Lightning)
  - Post-harvest losses (up to 14 days after harvesting for crops in unbundled condition)
  - Localized calamities (Hailstorm, Cloudburst, Inundation)

**🌾 Minimal Farmer Premium:**
* **Kharif Crops (Paddy, Maize, Cotton, Soybean):** Only **2.0%** of sum insured.
* **Rabi Crops (Wheat, Gram, Mustard, Pulses):** Only **1.5%** of sum insured.
* **Horticultural / Commercial Crops:** **5.0%** of sum insured.
* The remaining premium (often 85% to 95%) is paid equally by Central & State governments.

**⚠️ CRITICAL 72-HOUR LOSS INTIMATION RULE:**
In case of localized damage (hailstorm, flood, waterlogging, or severe pest outbreak), you MUST intimate loss within **72 hours**:
1. **Via Mobile App:** Download official **'Crop Insurance'** app from Google Play Store -> Tap 'Crop Loss Intimation' -> upload photo of damaged field.
2. **Via National Toll-Free Helpline:** Call **1800-180-1551** or **14447**.
3. **Via Bank / Agriculture Officer:** Submit written report to your bank branch or Village Agriculture Assistant.

**🌐 Official Portal:** [pmfby.gov.in](https://pmfby.gov.in)
"""
}


def get_state_schemes_fallback(state_name):
    schemes = STATE_SCHEMES.get(state_name, [])
    if not schemes:
        return f"### 🏛️ Agricultural Schemes for {state_name}\n\n* Please contact your District Agriculture Office or visit the official state portal."

    out = [f"### 🏛️ Complete Welfare & Subsidy Schemes for {state_name}, India:\n"]
    for i, sc in enumerate(schemes, 1):
        out.append(f"#### {i}. {sc['name']}")
        out.append(f"- **💰 Financial Benefit:** {sc['benefit']}")
        out.append(f"- **🌐 Official Portal:** [{sc['portal']}](https://{sc['portal']})")
        out.append("- **📄 Documents Needed:** Land Record (Pahani/Patta), Aadhaar Card, Bank Passbook linked to NPCI.")
        out.append("")
    out.append("💡 **Application Tip:** Visit your local MeeSeva / CSC Centre or Village Agriculture Assistant (VAA / AEO) with your land documents to apply directly.")
    return "\n".join(out)


def get_eligibility_report_fallback(farm_size, crop_name, farmer_category, state_name):
    is_small = (farm_size <= 5.0) or ("Small" in farmer_category) or ("Marginal" in farmer_category)
    
    report = f"""
### 🎯 Personalized Scheme Eligibility Report for Your Farm
* **Farm Size:** {farm_size} acres ({'Small / Marginal Farmer' if is_small else 'Medium / Large Farmer'})
* **Primary Crop:** {crop_name}
* **Farmer Category:** {farmer_category}
* **State / Region:** {state_name}

---

#### 🌟 1. Central Government Schemes You Are 100% Eligible For:
1. **🌾 PM-KISAN Samman Nidhi:**
   - **Status:** ✅ **100% Eligible**
   - **Cash Benefit:** **₹6,000 / year** directly to your bank account (3 x ₹2,000 installments).
   - **Requirement:** Cultivable land registered in your name + e-KYC completed on [pmkisan.gov.in](https://pmkisan.gov.in).

2. **🛡️ PMFBY Crop Insurance:**
   - **Status:** ✅ **100% Eligible for {crop_name}**
   - **Benefit:** Full compensation against drought, flood, pests, and unseasonal rainfall.
   - **Farmer Premium:** Only 1.5% to 2% of sum insured. Government pays the remaining 95%+.

3. **💳 Kisan Credit Card (KCC) Loan:**
   - **Status:** ✅ **Eligible**
   - **Benefit:** Institutional crop loan up to **₹3,00,000** at an effective **4% interest rate** (with prompt repayment). Collateral-free loan up to ₹1,60,000.

4. **☀️ PM-KUSUM Solar Irrigation Pump:**
   - **Status:** ✅ **{'Priority High (Small/Marginal Subsidy)' if is_small else 'Eligible'}**
   - **Benefit:** **60% to 80% Subsidy** on 3HP / 5HP solar pump. Farmer pays only 10% to 20% upfront.

5. **🚜 SMAM Farm Machinery Subsidy:**
   - **Status:** ✅ **Eligible ({'40% to 80% Subsidy' if is_small else '40% to 50% Subsidy'})**
   - **Benefit:** High subsidy on purchase of rotavators, power tillers, seed drills, and drone spraying equipment.

---

#### 📍 2. {state_name} State Welfare Schemes:
"""
    state_items = STATE_SCHEMES.get(state_name, [])
    for sc in state_items:
        report += f"- **{sc['name']}:** {sc['benefit']} ([Official Portal: {sc['portal']}](https://{sc['portal']}))\n"
    
    report += f"""
---

#### 📄 3. Checklist of Required Documents:
* 🪪 Aadhaar Card (linked to active mobile number for OTP)
* 📜 Land Ownership Record (Pahani / Patta / 7/12 / ROR / Khatauni)
* 🏦 Bank Account Passbook (must have active **Aadhaar NPCI DBT mapper**)
* 🌾 Sowing Certificate / Crop Declaration from Village Agriculture Officer

#### 🚀 4. How to Apply:
1. Visit your local **CSC (Common Service Center)** or **MeeSeva / E-Seva Kendra**.
2. Or contact your **Village Agriculture Assistant (VAA / AEO)** at the local Rythu Bharosa Kendra (RBK) or Krishi Bhavan.
3. For immediate assistance, dial the National Kisan Helpline: **1800-180-1551** (Toll-Free, 6 AM to 10 PM in your language).
"""
    return report


# =========================================================
# MAIN GOVERNMENT SCHEMES PAGE RENDERER
# =========================================================

def show_government_schemes():
    """Renders the standalone Government Schemes & Subsidies portal with backdrop imagery."""

    farmer = st.session_state.get("farmer", {})
    farmer_id = farmer.get("id", 1)
    current_lang = st.session_state.get("selected_language", "English")

    lang_map = {"English": "en", "తెలుగు": "te", "हिंदी": "hi", "தமிழ்": "ta", "ಕನ್ನಡ": "kn", "मराठी": "mr"}
    lang_code = lang_map.get(current_lang, "en")
    t = GOV_TEXT.get(lang_code, GOV_TEXT["en"])

    bg_b64 = _get_bg_base64()

    # =====================================================
    # EMBEDDED GOVERNMENT PORTAL CSS WITH BACKGROUND IMAGE
    # =====================================================
    bg_style = ""
    if bg_b64:
        bg_style = f"""
        .gov-portal-wrapper {{
            background: linear-gradient(180deg, rgba(248, 250, 252, 0.94) 0%, rgba(248, 250, 252, 0.97) 100%),
                        url('data:image/jpeg;base64,{bg_b64}');
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center top;
            background-attachment: fixed;
            border-radius: 20px;
            padding: 16px;
            margin-bottom: 24px;
        }}
        """
    else:
        bg_style = """
        .gov-portal-wrapper {
            background-color: #f8fafc;
            border-radius: 20px;
            padding: 16px;
            margin-bottom: 24px;
        }
        """

    st.markdown(
        f"""
        <style>
        {bg_style}

        /* Official Tricolor Ribbon */
        .gov-tricolor-bar {{
            height: 5px;
            width: 100%;
            background: linear-gradient(90deg, #ff9933 0%, #ff9933 33%, #ffffff 33%, #ffffff 66%, #138808 66%, #138808 100%);
            border-radius: 4px;
            margin-bottom: 14px;
        }}

        /* Government Hero Banner */
        .gov-hero-card {{
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #064e3b 100%);
            border: 2px solid #cbd5e1;
            border-radius: 18px;
            padding: 24px;
            margin-bottom: 18px;
            color: #ffffff;
            box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.25);
            position: relative;
            overflow: hidden;
        }}

        .gov-hero-card::after {{
            content: "🏛️";
            position: absolute;
            right: 20px;
            top: 20px;
            font-size: 75px;
            opacity: 0.12;
            pointer-events: none;
        }}

        /* Scheme Cards */
        .gov-scheme-box {{
            background: #ffffff;
            border: 1.5px solid #e2e8f0;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
            transition: all 0.2s ease;
        }}

        .gov-scheme-box:hover {{
            transform: translateY(-2px);
            border-color: #16a34a;
            box-shadow: 0 8px 24px rgba(22, 163, 74, 0.12);
        }}

        .gov-benefit-tag {{
            display: inline-block;
            background: #ecfdf5;
            color: #166534;
            border: 1px solid #86efac;
            font-size: 13px;
            font-weight: 800;
            padding: 6px 12px;
            border-radius: 8px;
            margin: 8px 0;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Wrap content in gov portal container
    st.markdown('<div class="gov-portal-wrapper">', unsafe_allow_html=True)

    # 1. Official Tricolor Accent
    st.markdown('<div class="gov-tricolor-bar"></div>', unsafe_allow_html=True)

    # 2. Hero Header Card with Ministry Badge
    st.markdown(
        f"""
        <div class="gov-hero-card">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                <span style="background:rgba(255,255,255,0.15);padding:3px 10px;border-radius:9999px;font-size:11px;font-weight:700;letter-spacing:0.5px;border:1px solid rgba(255,255,255,0.30);">
                    {t['portal_badge']}
                </span>
            </div>
            <h1 style="color:#ffffff !important;margin:8px 0 6px 0;font-size:26px;font-weight:800;">
                {t['page_title']}
            </h1>
            <p style="color:#cbd5e1;margin:0 0 10px 0;font-size:14px;line-height:1.5;">
                {t['page_subtitle']}
            </p>
            <div style="font-size:12px;color:#86efac;font-weight:700;display:flex;align-items:center;gap:6px;">
                {t['official_helpline']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 3. Proactive AgriSense AI Scheme Guidance Card
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #064e3b 0%, #047857 100%); border-radius: 16px; padding: 18px 20px; margin-bottom: 18px; color: #ffffff; box-shadow: 0 6px 18px rgba(4, 120, 87, 0.25); border: 1.5px solid #86efac;">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
                <span style="font-size:28px;">🤖</span>
                <div>
                    <div style="font-size:16px;font-weight:800;color:#ffffff;">Not Sure Which Government Schemes You Qualify For?</div>
                    <div style="font-size:12.5px;color:#d1fae5;">Ask AgriSense AI! Tap below to get instant personalized scheme recommendations, required documents, and subsidy calculation in your language.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    ai_sch_c1, ai_sch_c2, ai_sch_c3 = st.columns(3)
    with ai_sch_c1:
        if st.button("🌾 PM-KISAN & Cash Grant", key="btn_sch_ai_1", use_container_width=True):
            st.session_state.gov_active_topic = "pm_kisan"
            st.session_state.gov_active_prompt = "Explain PM-KISAN eligibility, how to complete e-KYC, and how small/marginal farmers can claim ₹6,000 yearly directly in their bank account."
    with ai_sch_c2:
        if st.button("☀️ Solar Pump 60-80% Subsidy", key="btn_sch_ai_2", use_container_width=True):
            st.session_state.gov_active_topic = "pm_kusum"
            st.session_state.gov_active_prompt = "How can a farmer apply for PM-KUSUM solar agricultural pump subsidy? What documents and portal should be used to get 60% to 80% government grant?"
    with ai_sch_c3:
        if st.button("🛡️ PMFBY Crop Damage Claim", key="btn_sch_ai_3", use_container_width=True):
            st.session_state.gov_active_topic = "pmfby"
            st.session_state.gov_active_prompt = "How can a farmer report crop damage due to drought, unseasonal rain, or pests within 72 hours under PMFBY to claim insurance compensation?"

    if st.session_state.get("gov_active_topic") or st.session_state.get("gov_active_prompt"):
        topic = st.session_state.get("gov_active_topic")
        q_prompt = st.session_state.get("gov_active_prompt")
        st.markdown("<div style='background:#f0fdf4;border:1.5px solid #86efac;border-radius:14px;padding:18px;margin:14px 0;box-shadow:0 4px 14px rgba(22,163,74,0.12);'>", unsafe_allow_html=True)
        h_col1, h_col2 = st.columns([5, 1])
        with h_col1:
            st.markdown("<div style='font-size:16px;font-weight:800;color:#166534;'>🤖 AgriSense AI Official Scheme Advisor:</div>", unsafe_allow_html=True)
        with h_col2:
            if st.button("✖ Close", key="btn_close_gov_quick", use_container_width=True):
                st.session_state.gov_active_topic = None
                st.session_state.gov_active_prompt = None
                st.rerun()

        with st.spinner("Consulting Ministry of Agriculture guidelines..."):
            ai_success = False
            try:
                stream = ask_agrisense_stream(farmer_id=farmer_id, question=q_prompt, language=current_lang)
                st.write_stream(stream)
                ai_success = True
            except Exception:
                pass

            if not ai_success and topic in OFFICIAL_SCHEME_GUIDES:
                st.markdown(OFFICIAL_SCHEME_GUIDES[topic])
        st.markdown("</div>", unsafe_allow_html=True)

    # 4. Main Navigation Tabs: National Schemes | State Schemes | AI Eligibility Checker
    tab_featured, tab_state, tab_ai = st.tabs([
        t["tab_featured"],
        t["tab_state"],
        t["tab_ai"]
    ])

    # =====================================================
    # TAB 1: KEY NATIONAL SCHEMES
    # =====================================================
    with tab_featured:
        # Category Filter
        cat_options = [
            t["filter_all"],
            t["filter_income"],
            t["filter_insurance"],
            t["filter_credit"],
            t["filter_machinery"],
            t["filter_soil_water"]
        ]
        selected_cat_label = st.radio(
            t["category_label"],
            cat_options,
            horizontal=True,
            key="gov_cat_filter"
        )

        cat_key_map = {
            t["filter_all"]: "all",
            t["filter_income"]: "income",
            t["filter_insurance"]: "insurance",
            t["filter_credit"]: "credit",
            t["filter_machinery"]: "machinery",
            t["filter_soil_water"]: "soil_water"
        }
        selected_cat = cat_key_map.get(selected_cat_label, "all")

        # Filter Schemes
        filtered_schemes = [
            s for s in NATIONAL_SCHEMES
            if selected_cat == "all" or s["category"] == selected_cat
        ]

        st.caption(f"Showing {len(filtered_schemes)} verified official government schemes")

        for scheme in filtered_schemes:
            st.markdown(
                f"""
                <div class="gov-scheme-box">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
                        <div style="font-size:18px;font-weight:800;color:#0f172a;">
                            <span style="margin-right:6px;">{scheme['icon']}</span>{scheme['name']}
                        </div>
                        <span style="background:{scheme['badge_bg']};color:{scheme['badge_color']};font-size:11px;font-weight:800;padding:3px 10px;border-radius:9999px;border:1px solid {scheme['badge_color']}40;">
                            🛡️ Official Govt Portal (.gov.in)
                        </span>
                    </div>
                    <div class="gov-benefit-tag">
                        💰 <b>Financial Benefit:</b> {scheme['benefit']}
                    </div>
                    <div style="font-size:14px;color:#334155;margin-top:8px;line-height:1.5;">
                        <b>🎯 Eligibility:</b> {scheme['eligibility']}
                    </div>
                    <div style="font-size:13px;color:#64748b;margin-top:6px;line-height:1.4;">
                        <b>📄 Required Documents:</b> {scheme['documents']}
                    </div>
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-top:14px;padding-top:12px;border-top:1px solid #f1f5f9;flex-wrap:wrap;gap:8px;">
                        <span style="font-size:12px;font-weight:600;color:#0f172a;">
                            📞 Helpline: <span style="color:#166534;font-weight:700;">{scheme['helpline']}</span>
                        </span>
                        <a href="{scheme['portal']}" target="_blank" style="text-decoration:none;background:#15803d;color:#ffffff;font-size:13px;font-weight:700;padding:6px 14px;border-radius:8px;display:inline-block;">
                            🌐 Visit Official Portal (.gov.in) ↗
                        </a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # =====================================================
    # TAB 2: STATE WELFARE SCHEMES
    # =====================================================
    with tab_state:
        st.markdown(f"### {t['tab_state']}")
        states_list = list(STATE_SCHEMES.keys())

        # Auto-detect or select state
        selected_state = st.selectbox(
            t["state_label"],
            states_list,
            index=0,
            key="gov_state_selector"
        )

        state_schemes = STATE_SCHEMES.get(selected_state, [])
        st.markdown(
            f"""
            <div style="background:#f0fdf4;border:1.5px solid #86efac;border-radius:12px;padding:12px 16px;margin-bottom:16px;">
                <span style="font-size:14px;font-weight:700;color:#166534;">
                    🏛️ Showing official agriculture & farmer welfare schemes for: <b>{selected_state}</b>
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        for s_idx, sc in enumerate(state_schemes, 1):
            st.markdown(
                f"""
                <div class="gov-scheme-box" style="border-left: 5px solid #16a34a;">
                    <div style="font-size:17px;font-weight:800;color:#0f172a;margin-bottom:4px;">
                        {s_idx}. {sc['name']}
                    </div>
                    <div style="font-size:14px;color:#166534;font-weight:700;margin:6px 0;">
                        🎁 Benefit: {sc['benefit']}
                    </div>
                    <div style="font-size:12px;color:#64748b;margin-top:6px;">
                        🌐 Official Portal: <a href="https://{sc['portal']}" target="_blank" style="color:#2563eb;font-weight:600;">{sc['portal']} ↗</a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # AI prompt for unlisted or custom state inquiries
        if st.button(f"🔍 Ask AI for More {selected_state} Schemes", key="btn_more_state_schemes", use_container_width=True):
            st.session_state.gov_tab2_state = selected_state

        if st.session_state.get("gov_tab2_state") == selected_state:
            st.markdown("<div style='background:#f0fdf4;border:1.5px solid #86efac;border-radius:14px;padding:16px;margin:14px 0;'>", unsafe_allow_html=True)
            h_c1, h_c2 = st.columns([5, 1])
            with h_c1:
                st.markdown(f"**🏛️ Official State Welfare Schemes for {selected_state}:**")
            with h_c2:
                if st.button("✖ Close", key="btn_close_tab2_state", use_container_width=True):
                    st.session_state.gov_tab2_state = None
                    st.rerun()

            with st.spinner(t["loading_schemes"]):
                prompt = (
                    f"Give me a comprehensive list of all current state-government agricultural subsidies, "
                    f"farmer welfare programs, free electricity, input subsidies, and equipment grants "
                    f"provided specifically by the Government of {selected_state}, India for farmers. "
                    f"Include scheme names, monetary benefits, eligibility, and how to apply in simple steps."
                )
                ai_success = False
                try:
                    stream_gen = ask_agrisense_stream(
                        farmer_id=farmer_id,
                        question=prompt,
                        language=current_lang
                    )
                    st.write_stream(stream_gen)
                    ai_success = True
                except Exception:
                    pass

                if not ai_success:
                    st.markdown(get_state_schemes_fallback(selected_state))
            st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # TAB 3: AI SCHEME ADVISOR & ELIGIBILITY CHECKER
    # =====================================================
    with tab_ai:
        st.markdown(f"### {t['eligibility_title']}")
        st.caption(t["eligibility_desc"])

        col_sz, col_cr, col_cat = st.columns(3)
        with col_sz:
            farm_size = st.number_input(
                t["farm_size"],
                min_value=0.5,
                max_value=200.0,
                value=2.5,
                step=0.5,
                key="gov_ai_farm_size"
            )
        with col_cr:
            crop_name = st.selectbox(
                t["farm_crop"],
                ["Paddy / Rice", "Wheat", "Cotton", "Maize", "Sugarcane", "Chilli", "Tomato", "Soybean", "Groundnut", "Pulses", "Millets"],
                key="gov_ai_crop"
            )
        with col_cat:
            farmer_category = st.selectbox(
                t["farmer_category"],
                t["categories"],
                key="gov_ai_category"
            )

        farmer_state = st.selectbox(
            "State / Region",
            list(STATE_SCHEMES.keys()),
            key="gov_ai_state"
        )

        if st.button(t["btn_check_eligibility"], key="btn_gov_check_eligibility", use_container_width=True, type="primary"):
            st.session_state.gov_tab3_active = True
            st.session_state.gov_tab3_params = {
                "size": farm_size,
                "crop": crop_name,
                "cat": farmer_category,
                "state": farmer_state
            }

        if st.session_state.get("gov_tab3_active"):
            params = st.session_state.get("gov_tab3_params", {})
            p_size = params.get("size", farm_size)
            p_crop = params.get("crop", crop_name)
            p_cat = params.get("cat", farmer_category)
            p_state = params.get("state", farmer_state)

            st.markdown("<div style='background:#f0fdf4;border:1.5px solid #86efac;border-radius:14px;padding:18px;margin:14px 0;'>", unsafe_allow_html=True)
            h_c1, h_c2 = st.columns([5, 1])
            with h_c1:
                st.markdown("**🎯 Personalized Scheme Eligibility Analysis:**")
            with h_c2:
                if st.button("✖ Close", key="btn_close_tab3_elig", use_container_width=True):
                    st.session_state.gov_tab3_active = False
                    st.rerun()

            with st.spinner(t["loading_schemes"]):
                ai_prompt = (
                    f"I am a farmer from {p_state}, India. Here are my farm details:\n"
                    f"- Farm Size: {p_size} acres\n"
                    f"- Primary Crop: {p_crop}\n"
                    f"- Category: {p_cat}\n\n"
                    f"Please give me a complete, structured analysis of:\n"
                    f"1. Which Central Government schemes am I 100% eligible for? (e.g. PM-KISAN, PMFBY, KCC, PM-KUSUM)\n"
                    f"2. Which {p_state} state schemes am I eligible for?\n"
                    f"3. Exact subsidy percentages & money I can receive in rupees (₹)\n"
                    f"4. Exact documents I need to carry to the local agriculture office or MeeSeva/CSC center\n"
                    f"5. Step-by-step application procedure to get the money or subsidy without delays.\n"
                    f"Format with clear headings, bullet points, and practical advice."
                )
                ai_success = False
                try:
                    stream_gen = ask_agrisense_stream(
                        farmer_id=farmer_id,
                        question=ai_prompt,
                        language=current_lang
                    )
                    st.write_stream(stream_gen)
                    ai_success = True
                except Exception:
                    pass

                if not ai_success:
                    st.markdown(get_eligibility_report_fallback(p_size, p_crop, p_cat, p_state))
            st.markdown("</div>", unsafe_allow_html=True)

    # Close gov portal wrapper
    st.markdown('</div>', unsafe_allow_html=True)
