import os
import json
import sqlite3
import streamlit as st
import streamlit.components.v1 as components
from fertilizer import fertilizer_information

DB_PATH = "database/agrisense.db"


# =========================================================
# DATABASE HELPERS
# =========================================================

def get_latest_farm_data(farmer_id):
    """Retrieve the latest farm reading from SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM farm_readings
            WHERE farmer_id = ?
            ORDER BY id DESC
            LIMIT 1
        """, (farmer_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    except Exception:
        return None


def get_latest_crop(farmer_id):
    """Retrieve the latest predicted crop for the farmer."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT crop
            FROM predictions
            WHERE farmer_id = ?
            ORDER BY id DESC
            LIMIT 1
        """, (farmer_id,))
        row = cursor.fetchone()
        conn.close()
        return str(row[0]).lower().strip() if row else "rice"
    except Exception:
        return "rice"


# =========================================================
# CROP NPK BENCHMARKS & 4-STAGE SPLIT DOSAGE SCHEDULES
# =========================================================

CROP_FERTILIZER_SCHEDULES = {
    "rice": {
        "ideal_npk": (100, 50, 50),
        "zinc_req": "25 kg/ha Zinc Sulphate (21%) at basal",
        "bag_calc_per_acre": "Urea: 2.0 Bags (100 kg) • DAP: 1.0 Bag (50 kg) • MOP (Potash): 0.7 Bag (35 kg)",
        "stages": [
            {"stage": "Stage 1: Basal (At Transplanting - Day 0)", "products": "DAP (50 kg) + MOP (20 kg) + Zinc Sulphate (10 kg)", "method": "Soil broadcast & incorporate during last puddling", "why": "Stimulates rapid root growth and tiller emergence."},
            {"stage": "Stage 2: Active Tillering (20-25 DAS)", "products": "Neem-Coated Urea (35 kg)", "method": "Broadcast in 2 cm standing water (drain field after 24h if flooded)", "why": "Drives rapid leaf greening and vigorous vegetative tillering."},
            {"stage": "Stage 3: Panicle Initiation (45-50 DAS)", "products": "Neem-Coated Urea (35 kg) + MOP (15 kg)", "method": "Top-dressing with soil moisture", "why": "Directly boosts panicle length, spikelet count, and grain number."},
            {"stage": "Stage 4: Heading & Grain Filling (70-75 DAS)", "products": "Foliar Spray 0:0:50 (SOP) @ 1.5 kg/acre + 100g Boron", "method": "Foliar spray in 150 Liters water during morning", "why": "Fills grain weight (1000-grain weight) and eliminates empty chaffy grains."}
        ]
    },
    "maize": {
        "ideal_npk": (120, 60, 40),
        "zinc_req": "25 kg/ha Zinc Sulphate (21%)",
        "bag_calc_per_acre": "Urea: 2.5 Bags (125 kg) • DAP: 1.2 Bags (60 kg) • MOP: 0.6 Bag (30 kg)",
        "stages": [
            {"stage": "Stage 1: Basal (At Sowing - Day 0)", "products": "Full DAP (60 kg) + Full MOP (30 kg) + 1/3 Urea (40 kg) + Zinc", "method": "Band placement 5 cm to the side and 5 cm below seed", "why": "Deep starter nutrition without seed scorching."},
            {"stage": "Stage 2: Knee-High Stage (30-35 DAS)", "products": "Neem-Coated Urea (45 kg)", "method": "Side dressing along crop rows followed by light earthing up", "why": "Fuel for stem elongation and cob bud initiation."},
            {"stage": "Stage 3: Tasseling / Silking (50-55 DAS)", "products": "Neem-Coated Urea (40 kg) + 19:19:19 Foliar Spray (1 kg/acre)", "method": "Top dressing before tasseling + foliar misting", "why": "Guarantees complete silk emergence and full kernel row filling."},
            {"stage": "Stage 4: Grain Filling / Dough (70-75 DAS)", "products": "Foliar Spray of 13:0:45 (Potassium Nitrate) @ 1.5 kg/acre", "method": "Foliar spray on upper foliage", "why": "Increases starch density and prevents tip kernel abortion."}
        ]
    },
    "cotton": {
        "ideal_npk": (120, 60, 60),
        "zinc_req": "15 kg/ha Zinc Sulphate + 10 kg/ha Magnesium Sulphate",
        "bag_calc_per_acre": "Urea: 2.5 Bags (125 kg) • DAP: 1.2 Bags (60 kg) • MOP: 1.0 Bag (50 kg)",
        "stages": [
            {"stage": "Stage 1: Basal (At Sowing)", "products": "Full DAP (60 kg) + 1/2 MOP (25 kg) + Magnesium Sulphate (10 kg)", "method": "Furrow placement during field preparation", "why": "Strong taproot and early pest resistance."},
            {"stage": "Stage 2: Square Formation (35-40 DAS)", "products": "Urea (45 kg)", "method": "Ring application 10 cm away from plant stem", "why": "Promotes productive sympodial branches and squares."},
            {"stage": "Stage 3: Peak Flowering & Boll Setting (60-70 DAS)", "products": "Urea (40 kg) + Remaining MOP (25 kg) + 2% DAP spray", "method": "Top dressing followed by irrigation", "why": "Drastically reduces flower and young square dropping."},
            {"stage": "Stage 4: Peak Boll Development (85-95 DAS)", "products": "Foliar Spray of Potassium Nitrate (13:0:45) @ 1.5% + Boron @ 0.1%", "method": "Foliar spray on canopy in afternoon", "why": "Increases boll weight, fiber strength, and ginning outturn."}
        ]
    },
    "chickpea": {
        "ideal_npk": (20, 40, 20),
        "zinc_req": "Rhizobium + PSB bio-fertilizer seed treatment",
        "bag_calc_per_acre": "DAP: 0.8 Bag (40 kg) • MOP: 0.3 Bag (15 kg) • Starter Urea: 0.2 Bag (10 kg)",
        "stages": [
            {"stage": "Stage 1: Basal (At Sowing)", "products": "Full DAP (40 kg) + Full MOP (15 kg) + Rhizobium inoculant", "method": "Drilled below seed at 7-10 cm depth", "why": "Promotes root nodulation for natural nitrogen fixation."},
            {"stage": "Stage 2: Vegetative & Branching (30-35 DAS)", "products": "Foliar spray of 2% Urea or 19:19:19 (1 kg/acre)", "method": "Foliar spray after nipping shoots", "why": "Triggers vigorous lateral branches and bud set."},
            {"stage": "Stage 3: 50% Flowering (55-60 DAS)", "products": "Foliar spray of 2% DAP solution + 0.5g/L NAA", "method": "Foliar spray during calm morning hours", "why": "Prevents flower drop and boosts pod set by 30%."},
            {"stage": "Stage 4: Pod Filling (75-80 DAS)", "products": "Foliar spray 0:52:34 (MKP) @ 1.0 kg/acre", "method": "Foliar spray", "why": "Ensures bold, uniform seed size and high test weight."}
        ]
    },
    "banana": {
        "ideal_npk": (200, 50, 300),
        "zinc_req": "Neem Cake (250g/plant) + Micronutrient spray",
        "bag_calc_per_acre": "Urea: 4.5 Bags • SSP / DAP: 1.5 Bags • MOP: 5.0 Bags per 1000 plants",
        "stages": [
            {"stage": "Stage 1: Planting / Establishment (Month 1-2)", "products": "DAP (50g) + Urea (40g) + MOP (40g) + 5 kg FYM per pit", "method": "Ring basin placement around plant", "why": "Promotes rapid early root establishment."},
            {"stage": "Stage 2: Vegetative Growth (Month 3-4)", "products": "Urea (50g) + MOP (60g) + Micronutrients (15g) per plant", "method": "Side dressing before drip watering", "why": "Broad leaf formation and robust pseudostem girth."},
            {"stage": "Stage 3: Shooting & Bunch Initiation (Month 6-7)", "products": "Urea (50g) + MOP (100g) per plant", "method": "Drip fertigation or soil ring basin", "why": "High Potassium requirement for long, heavy bunch stems."},
            {"stage": "Stage 4: Bunch Development (Month 8-9)", "products": "MOP (80g) per plant + Bunch spray of 0:0:50 @ 1.0%", "method": "Soil application + direct spray on developing fingers", "why": "Increases fruit sugar, curvature, skin shine, and shelf life."}
        ]
    }
}

DEFAULT_SCHEDULE = {
    "ideal_npk": (80, 40, 40),
    "zinc_req": "10-15 kg/ha Micronutrient mixture",
    "bag_calc_per_acre": "Urea: 1.5 Bags (75 kg) • DAP: 1.0 Bag (50 kg) • MOP: 0.5 Bag (25 kg)",
    "stages": [
        {"stage": "Stage 1: Basal Application (At Sowing)", "products": "Full Phosphorus (DAP) + Full Potash (MOP) + 1/3 Nitrogen (Urea)", "method": "Incorporate in soil during final land prep", "why": "Develops deep root architecture."},
        {"stage": "Stage 2: Active Vegetative (25-30 DAS)", "products": "1/3 Nitrogen (Urea 35 kg)", "method": "Top-dressing with soil moisture", "why": "Enhances chlorophyll and canopy density."},
        {"stage": "Stage 3: Flowering Stage (50-60 DAS)", "products": "Remaining 1/3 Nitrogen (Urea 35 kg) + 19:19:19 Foliar spray", "method": "Top-dressing & Foliar misting", "why": "Maximizes flower retention and fertilization."},
        {"stage": "Stage 4: Grain / Fruit Development (75-85 DAS)", "products": "Foliar spray 0:0:50 (Potash) @ 1.5 kg/acre", "method": "Foliar spray in 150L water", "why": "Fills grain/fruit weight and quality."}
    ]
}


# =========================================================
# MULTILINGUAL FERTILIZER UI & TRANSLATIONS
# =========================================================

FERT_LANG = {
    "en": {
        "title": "🌿 Smart Fertilizer Advisor",
        "sub": "Precision soil nutrient balancing & 4-stage split-dosage schedule",
        "voice_title": "🔊 Listen to AI Fertilizer Plan (20s)",
        "voice_sub": "Clear voice explanation — Tap Play to hear exact fertilizer bags and application dates",
        "btn_play": "🔊 Play Fertilizer Advice",
        "btn_stop": "⏹ Stop",
        "speech_lang": "en-IN",
        "balance_title": "🧪 Soil Nutrient Balance & Deficit Assessment",
        "dosage_title": "📦 Total Fertilizer Quantity Required per Acre",
        "schedule_title": "📅 4-Stage Split-Dose Application Schedule",
        "organic_title": "🌿 Organic & Bio-Fertilizer Alternatives",
        "faq_title": "❓ Frequently Asked Farmer Fertilizer Questions"
    },
    "te": {
        "title": "🌿 స్మార్ట్ ఎరువుల సలహాదారు",
        "sub": "మీ నేల పోషకాల లోపం ఆధారంగా ఖచ్చితమైన ఎరువుల మోతాదు & దశలవారీ కాలపట్టిక",
        "voice_title": "🔊 నేటి ఎరువుల ప్రణాళిక వాయిస్ సలహా (20 సెకన్లు)",
        "voice_sub": "స్పష్టమైన తెలుగు వాయిస్‌లో — ఏ ఎరువు ఎంత వేయాలో వినడానికి నొక్కండి",
        "btn_play": "🔊 సలహా వినండి (Play Audio)",
        "btn_stop": "⏹ ఆపండి",
        "speech_lang": "te-IN",
        "balance_title": "🧪 నేల పోషకాల లోపం & విశ్లేషణ",
        "dosage_title": "📦 ఎకరానికి అవసరమైన మొత్తం ఎరువుల బస్తాల అంచనా",
        "schedule_title": "📅 4 దశలవారీ ఎరువుల యాజమాన్య ప్రణాళిక",
        "organic_title": "🌿 సేంద్రీయ & జీవ ఎరువుల ప్రత్యామ్నాయాలు",
        "faq_title": "❓ ఎరువుల వాడకంపై రైతుల సందేహాలు & సమాధానాలు"
    },
    "hi": {
        "title": "🌿 स्मार्ट उर्वरक सलाहकार",
        "sub": "मिट्टी के पोषक तत्वों और फसल के अनुसार सटीक खाद की मात्रा एवं 4-चरणीय समय-सारणी",
        "voice_title": "🔊 आज की खाद सलाह सुनें (20 सेकंड)",
        "voice_sub": "स्पष्ट हिंदी आवाज में — कौन सी खाद कितनी मात्रा में डालनी है जानने के लिए दबाएं",
        "btn_play": "🔊 सलाह सुनें (Play Audio)",
        "btn_stop": "⏹ रोकें",
        "speech_lang": "hi-IN",
        "balance_title": "🧪 मृदा पोषक तत्व संतुलन एवं विश्लेषण",
        "dosage_title": "📦 प्रति एकड़ आवश्यक कुल खाद (बोरी की गणना)",
        "schedule_title": "📅 4-चरणीय खाद प्रयोग समय-सारणी",
        "organic_title": "🌿 जैविक खाद एवं जैव उर्वरक विकल्प",
        "faq_title": "❓ खाद एवं उर्वरक पर किसानों के महत्वपूर्ण प्रश्न"
    },
    "ta": {
        "title": "🌿 ஸ்மார்ட் உர ஆலோசகர்",
        "sub": "மண் சத்துக்கள் மற்றும் பயிருக்கு ஏற்ப துல்லியமான உர அளவு & 4-நிலை கால அட்டவணை",
        "voice_title": "🔊 உர ஆலோசனை குரல் வழியே கேளுங்கள்",
        "voice_sub": "தெளிவான தமிழ் குரலில் — உர நிர்வாகத்தை அறிய அழுத்தவும்",
        "btn_play": "🔊 ஆடியோவைக் கேளுங்கள்",
        "btn_stop": "⏹ நிறுத்து",
        "speech_lang": "ta-IN",
        "balance_title": "🧪 மண் சத்து சமநிலை மற்றும் பகுப்பாய்வு",
        "dosage_title": "📦 ஏக்கருக்கு தேவையான உர அளவு (மூட்டை கணக்கு)",
        "schedule_title": "📅 4-நிலை உர பயன்பாட்டு அட்டவணை",
        "organic_title": "🌿 இயற்கை மற்றும் உயிர் உர வழிகாட்டி",
        "faq_title": "❓ உரம் பற்றிய விவசாயிகளின் சந்தேகங்கள்"
    },
    "kn": {
        "title": "🌿 ಸ್ಮಾರ್ಟ್ ರಸಗೊಬ್ಬರ ಸಲಹೆಗಾರ",
        "sub": "ಮಣ್ಣಿನ ಪೋಷಕಾಂಶಗಳ ಸಮತೋಲನ ಮತ್ತು 4-ಹಂತದ ರಸಗೊಬ್ಬರ ವೇಳಾಪಟ್ಟಿ",
        "voice_title": "🔊 ರಸಗೊಬ್ಬರ ಧ್ವನಿ ಸಾರಾಂಶ ಆಲಿಸಿ",
        "voice_sub": "ಕನ್ನಡ ಧ್ವನಿಯಲ್ಲಿ — ರಸಗೊಬ್ಬರ ಪ್ರಮಾಣ ತಿಳಿಯಲು ಒತ್ತಿ",
        "btn_play": "🔊 ಸಾರಾಂಶ ಆಲಿಸಿ",
        "btn_stop": "⏹ ನಿಲ್ಲಿಸಿ",
        "speech_lang": "kn-IN",
        "balance_title": "🧪 ಮಣ್ಣಿನ ಪೋಷಕಾಂಶಗಳ ಸಮತೋಲನ ಪರೀಕ್ಷೆ",
        "dosage_title": "📦 ಪ್ರತಿ ಎಕರೆಗೆ ಅಗತ್ಯವಿರುವ ರಸಗೊಬ್ಬರ ಚೀಲಗಳ ಲೆಕ್ಕ",
        "schedule_title": "📅 4-ಹಂತಗಳ ರಸಗೊಬ್ಬರ ನಿರ್ವಹಣಾ ವೇಳಾಪಟ್ಟಿ",
        "organic_title": "🌿 ಸಾವಯವ ಮತ್ತು ಜೈವಿಕ ಗೊಬ್ಬರಗಳು",
        "faq_title": "❓ ರಸಗೊಬ್ಬರ ಕುರಿತ ರೈತರ ಪ್ರಶ್ನೋತ್ತರಗಳು"
    },
    "mr": {
        "title": "🌿 स्मार्ट खत व्यवस्थापन सल्लागार",
        "sub": "मातीतील अन्नद्रव्यांची कमतरता व पिकाच्या गरजेनुसार खताचे 4-टप्प्यांचे नियोजन",
        "voice_title": "🔊 खत व्यवस्थापन सल्ला ऐका",
        "voice_sub": "मराठी ऑडिओमध्ये — कोणती खते कधी आणि किती द्यावीत हे ऐका",
        "btn_play": "🔊 सल्ला ऐका",
        "btn_stop": "⏹ थांबवा",
        "speech_lang": "mr-IN",
        "balance_title": "🧪 माती अन्नद्रव्य विश्लेषण व संतुलन",
        "dosage_title": "📦 प्रति एकर खतांचे प्रमाण (बॅग हिशोब)",
        "schedule_title": "📅 4-टप्प्यांमधील खत वापर वेळापत्रक",
        "organic_title": "🌿 सेंद्रिय व जैविक खत पर्याय",
        "faq_title": "❓ खत वापराबाबत शेतकऱ्यांचे प्रश्न"
    }
}


# =========================================================
# MAIN FERTILIZER ADVISOR VIEW
# =========================================================

def show_fertilizer_advisor(crop=None):
    farmer = st.session_state.get("farmer")
    if not farmer:
        st.warning("Please login first.")
        return

    farmer_id = farmer.get("id", 1)
    farmer_name = farmer.get("name", "Farmer")
    lang_code = st.session_state.get("language_code", "en")
    ui = FERT_LANG.get(lang_code, FERT_LANG["en"])

    st.title(ui["title"])
    st.caption(f"👨‍🌾 {farmer_name} • 🌐 {ui['sub']}")
    st.markdown("---")

    farm_data = get_latest_farm_data(farmer_id)
    if not farm_data:
        st.info("🌱 No farm data is available yet. Please enter your farm readings first.")
        if st.button("📡 Go to My Farm Data", use_container_width=True):
            st.session_state.page = "farm"
            st.rerun()
        return

    if not crop:
        crop = get_latest_crop(farmer_id)

    crop_key = crop.lower().strip()
    sched_info = CROP_FERTILIZER_SCHEDULES.get(crop_key, DEFAULT_SCHEDULE)
    gen_info = fertilizer_information.get(crop_key, {})

    n_val = float(farm_data.get("nitrogen", 80.0))
    p_val = float(farm_data.get("phosphorus", 40.0))
    k_val = float(farm_data.get("potassium", 40.0))
    ph_val = float(farm_data.get("ph", 7.0))

    ideal_n, ideal_p, ideal_k = sched_info["ideal_npk"]

    # Soil Deficit / Surplus calculation
    n_diff = n_val - ideal_n
    p_diff = p_val - ideal_p
    k_diff = k_val - ideal_k

    def get_status_tag(diff):
        if diff < -20:
            return "🔴 Deficit (Low)", "#fee2e2", "#b91c1c"
        elif diff > 30:
            return "⚠️ High (Excess)", "#fef3c7", "#b45309"
        else:
            return "🟢 Normal (Balanced)", "#dcfce7", "#15803d"

    n_tag, n_bg, n_fg = get_status_tag(n_diff)
    p_tag, p_bg, p_fg = get_status_tag(p_diff)
    k_tag, k_bg, k_fg = get_status_tag(k_diff)

    # Localized Voice Script
    voice_scripts = {
        "en": f"Namaste {farmer_name}! For your {crop.title()} crop, your soil Nitrogen is {n_val:.0f}, Phosphorus is {p_val:.0f}, and Potassium is {k_val:.0f}. Estimated total fertilizer needed per acre is: {sched_info['bag_calc_per_acre']}. Apply full Phosphorus and Potash at basal sowing, and split Urea into three doses at tillering and flowering.",
        "te": f"నమస్కారం {farmer_name} గారు! మీ {crop.title()} పంటకు, మీ పొలంలో నత్రజని {n_val:.0f}, భాస్వరం {p_val:.0f}, పొటాష్ {k_val:.0f} ఉంది. ఎకరానికి అవసరమైన ఎరువుల అంచనా: {sched_info['bag_calc_per_acre']}. విత్తే సమయంలో DAP మరియు పొటాష్ పూర్తి మోతాదు వేయండి, యూరియాను మూడు దఫాలుగా వేయడం ద్వారా అధిక దిగుబడి పొందవచ్చు.",
        "hi": f"नमस्ते {farmer_name} जी! आपकी {crop.title()} फसल के लिए मिट्टी में नाइट्रोजन {n_val:.0f}, फास्फोरस {p_val:.0f} और पोटाश {k_val:.0f} है। प्रति एकड़ आवश्यक खाद: {sched_info['bag_calc_per_acre']}। बुवाई के समय पूरा डीएपी और पोटाश डालें, तथा यूरिया को 3 भागों में बांटकर दें।",
        "ta": f"வணக்கம் {farmer_name}! உங்கள் {crop.title()} பயிருக்கு தேவையான உர அளவு: {sched_info['bag_calc_per_acre']}. விதைக்கும் போது அடி உரமாக DAP மற்றும் பொட்டாஷ் இடவும்.",
        "kn": f"ನಮಸ್ಕಾರ {farmer_name}! ನಿಮ್ಮ {crop.title()} ಬೆಳೆಗೆ ಅಗತ್ಯವಿರುವ ರಸಗೊಬ್ಬರ: {sched_info['bag_calc_per_acre']}. ಬಿತ್ತನೆ ಸಮಯದಲ್ಲಿ DAP ಮತ್ತು ಪೊಟ್ಯಾಶ್ ಹಾಕಿ, ಯೂರಿಯಾವನ್ನು 3 ಕಂತುಗಳಲ್ಲಿ ನೀಡಿ.",
        "mr": f"नमस्कार {farmer_name}! तुमच्या {crop.title()} पिकासाठी आवश्यक खत: {sched_info['bag_calc_per_acre']}. पेरणीवेळी पूर्ण DAP व पोटॅश द्या आणि युरिया 3 हप्त्यांत विभागून द्या."
    }

    current_script = voice_scripts.get(lang_code, voice_scripts["en"])
    speech_lang_code = ui["speech_lang"]

    # =====================================================
    # 🔊 AI VOICE SUMMARY COMPONENT
    # =====================================================
    st.markdown(
        f"""
        <div style="background: #ffffff; border: 2px solid #16a34a; border-radius: 16px; padding: 18px 20px; margin-bottom: 18px; box-shadow: 0 4px 14px rgba(22, 163, 74, 0.15);">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                <div>
                    <div style="font-weight: 800; font-size: 16px; color: #15803d; display: flex; align-items: center; gap: 8px;">
                        <span>📢</span> {ui['voice_title']}
                    </div>
                    <div style="font-size: 13px; color: #64748b; margin-top: 2px;">
                        {ui['voice_sub']}
                    </div>
                </div>
                <div style="font-size: 12px; font-weight: 700; color: #0f172a; background: #dcfce7; padding: 4px 10px; border-radius: 999px;">
                    🌾 Recommended Crop: {crop.title()}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    script_json = json.dumps(current_script)
    components.html(
        f"""
        <div style="display: flex; gap: 10px; margin-bottom: 12px;">
            <button id="playFertVoice" onclick="playVoice()" style="
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
            <button id="stopFertVoice" onclick="stopVoice()" style="
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

                const btn = document.getElementById('playFertVoice');
                btn.style.background = '#059669';
                utterance.onend = function() {{
                    btn.style.background = 'linear-gradient(135deg, #16a34a 0%, #15803d 100%)';
                }};
                window.speechSynthesis.speak(utterance);
            }}

            function stopVoice() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    const btn = document.getElementById('playFertVoice');
                    btn.style.background = 'linear-gradient(135deg, #16a34a 0%, #15803d 100%)';
                }}
            }}
        </script>
        """,
        height=62
    )

    # =====================================================
    # NPK SOIL DEFICIT & NUTRIENT BALANCE SCORECARD
    # =====================================================
    st.subheader(ui["balance_title"])

    n_c1, n_c2, n_c3, n_c4 = st.columns(4)
    with n_c1:
        st.metric("🌱 Nitrogen (N)", f"{n_val:.0f} kg/ha", delta=f"{n_diff:+.0f} vs Ideal ({ideal_n})")
        st.markdown(f"<span style='background: {n_bg}; color: {n_fg}; padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 700;'>{n_tag}</span>", unsafe_allow_html=True)
    with n_c2:
        st.metric("🧪 Phosphorus (P)", f"{p_val:.0f} kg/ha", delta=f"{p_diff:+.0f} vs Ideal ({ideal_p})")
        st.markdown(f"<span style='background: {p_bg}; color: {p_fg}; padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 700;'>{p_tag}</span>", unsafe_allow_html=True)
    with n_c3:
        st.metric("🪴 Potassium (K)", f"{k_val:.0f} kg/ha", delta=f"{k_diff:+.0f} vs Ideal ({ideal_k})")
        st.markdown(f"<span style='background: {k_bg}; color: {k_fg}; padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 700;'>{k_tag}</span>", unsafe_allow_html=True)
    with n_c4:
        st.metric("⚗️ Soil pH Level", f"{ph_val:.1f}", delta=f"{'Optimal' if 6.0 <= ph_val <= 7.5 else ('Acidic' if ph_val < 6.0 else 'Alkaline')}")
        st.markdown(f"<span style='background: #dcfce7; color: #15803d; padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 700;'>⚡ pH {ph_val:.1f}</span>", unsafe_allow_html=True)

    # =====================================================
    # TOTAL FERTILIZER BAG QUANTITY HERO CARD
    # =====================================================
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #14532d 0%, #166534 100%); border-radius: 18px; padding: 20px 24px; color: white; margin-bottom: 20px; box-shadow: 0 8px 24px rgba(20, 83, 45, 0.35);">
            <div style="font-weight: 700; font-size: 13px; color: #86efac; text-transform: uppercase; letter-spacing: 0.5px;">
                📦 {ui['dosage_title']} ({crop.title()})
            </div>
            <h2 style="color: #ffffff !important; font-size: 22px !important; font-weight: 800; margin: 8px 0;">
                {sched_info['bag_calc_per_acre']}
            </h2>
            <div style="font-size: 13px; color: #dcfce7; font-weight: 600;">
                ✨ Micronutrients: <strong>{sched_info['zinc_req']}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # =====================================================
    # 📅 4-STAGE SPLIT-DOSE APPLICATION SCHEDULE TABLE
    # =====================================================
    st.subheader(f"{ui['schedule_title']} ({crop.title()})")

    stages = sched_info["stages"]
    for idx, stg in enumerate(stages, 1):
        with st.container(border=True):
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <div style="font-weight: 800; font-size: 16px; color: #15803d;">
                            {stg['stage']}
                        </div>
                        <div style="font-size: 14px; font-weight: 700; color: #0f172a; margin-top: 4px;">
                            🌿 <strong>Fertilizers & Dosage:</strong> <span style="color: #166534;">{stg['products']}</span>
                        </div>
                        <div style="font-size: 13px; color: #475569; margin-top: 4px;">
                            🚜 <strong>Application Method:</strong> {stg['method']}
                        </div>
                        <div style="font-size: 13px; color: #64748b; margin-top: 2px;">
                            🎯 <strong>Benefit:</strong> {stg['why']}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # =====================================================
    # 🌿 ORGANIC & BIO-FERTILIZER ALTERNATIVES
    # =====================================================
    st.subheader(ui["organic_title"])
    o_col1, o_col2 = st.columns(2)

    with o_col1:
        with st.container(border=True):
            st.markdown("#### 🪱 Vermicompost & Farmyard Manure (FYM)")
            st.write("• Apply **2 to 3 Tons / acre** of well-decomposed FYM or **1 Ton / acre** of Vermicompost during field preparation.")
            st.write("• Enriches soil organic carbon (SOC), boosts water holding capacity, and builds root microbes.")

        with o_col1:
            with st.container(border=True):
                st.markdown("#### 🧪 Bio-fertilizers (Rhizobium & PSB)")
                st.write("• **Rhizobium:** Fixes 40-50 kg atmospheric nitrogen per hectare for legume crops.")
                st.write("• **PSB (Phosphate Solubilizing Bacteria):** Solubilizes locked soil phosphorus into plant-absorbable form.")

    with o_col2:
        with st.container(border=True):
            st.markdown("#### 🌿 Neem Cake & Pongamia Cake")
            st.write("• Apply **150-200 kg / acre** of Neem cake blended with chemical fertilizers.")
            st.write("• Acts as a natural nitrification inhibitor, preventing nitrogen volatilization, while killing soil nematodes and white grubs.")

        with o_col2:
            with st.container(border=True):
                st.markdown("#### ⚗️ Soil pH Balance & Correction")
                if ph_val < 6.0:
                    st.warning("⚠️ **Acidic Soil (pH < 6.0):** Apply **200 kg / acre Agricultural Lime** or Dolomite to neutralize soil acidity.")
                elif ph_val > 7.5:
                    st.warning("⚠️ **Alkaline Soil (pH > 7.5):** Apply **150 kg / acre Gypsum** and increase organic matter to lower pH.")
                else:
                    st.success("✅ **Balanced pH (6.0 - 7.5):** Optimum range for nutrient absorption without chemical locking.")

    st.markdown("---")

    # =====================================================
    # ❓ FREQUENTLY ASKED FARMER FERTILIZER QUESTIONS
    # =====================================================
    st.subheader(ui["faq_title"])

    with st.expander("❓ Why should Nitrogen (Urea) be split into 3 doses instead of applied all at once?", expanded=False):
        st.markdown(
            """
            * **Prevents Fertilizer Loss:** Applying all Urea at once causes up to **60% loss** through nitrate leaching into groundwater and ammonia gas volatilization.
            * **Continuous Feeding:** Crops require nitrogen in peak amounts during tillering and panicle/tasseling stages. Split doses provide nutrition exactly when the plant needs it most.
            """
        )

    with st.expander("❓ Can I mix Urea with DAP or Pesticides in the same tank?", expanded=False):
        st.markdown(
            """
            * **Soil Application:** Urea and DAP can be mixed immediately before spreading on soil, but should NOT be stored together in bags as moisture absorption turns them sticky.
            * **Foliar Spray:** Do NOT mix chemical fertilizers with systemic insecticides or fungicides without doing a small jar compatibility test.
            """
        )

    with st.expander("❓ What are the benefits of Neem-Coated Urea (NCU)?", expanded=False):
        st.markdown(
            """
            * **Slow-Release Action:** The natural neem oil coating slows down nitrification, keeping nitrogen available to plant roots for **15-20 days longer**.
            * **Reduces Consumption:** Farmers need **10% to 15% less Urea bags** per acre while achieving equal or higher yields.
            """
        )

    with st.expander("❓ When should I use water-soluble foliar sprays (19:19:19 / 0:0:50)?", expanded=False):
        st.markdown(
            """
            * **Fast Absorption:** Foliar spraying delivers nutrients through leaf stomata within 3 to 6 hours, bypassing soil locking.
            * **Best Stages:** Spray **19:19:19** during vegetative/pre-flowering, and **0:0:50 (Potassium Sulphate)** during grain/fruit sizing.
            """
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    if st.button("💧 Check Water & Irrigation Schedule", use_container_width=True, type="primary"):
        st.session_state.page = "water"
        st.rerun()