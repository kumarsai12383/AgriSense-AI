"""
AgriSense AI — Live Mandi Market Prices & Cost Estimator Module
==============================================================
Provides:
  1. Today's Estimated Mandi Crop Prices (state-wise & crop-wise AI intelligence)
  2. Farming Cost & Profit Estimator (input-based yield & net profit calculator)
  3. Direct connection to the standalone Government Schemes portal

Architecturally independent, clean, and presentation-grade.
"""

import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import streamlit as st
from modules.ai_engine import ask_agrisense_stream


# =========================================================
# MULTILINGUAL TEXT TRANSLATIONS
# =========================================================

MARKET_TEXT = {
    "en": {
        "page_title": "📊 Live Mandi Prices & Farm Cost Estimator",
        "page_subtitle": "Real-time crop prices, mandi rate intelligence & farm profitability calculations",
        "tab_market": "📈 Live Mandi Prices",
        "tab_cost": "💰 Farming Cost & Profit Estimator",
        "gov_banner_title": "🏛️ Need Government Agricultural Schemes & Subsidies?",
        "gov_banner_desc": "Explore PM-KISAN, crop insurance, solar pumps & state welfare grants on our dedicated portal.",
        "gov_banner_btn": "Go to Government Schemes Portal ➔",

        # Market Tab
        "market_title": "📈 Today's Estimated Mandi Crop Prices",
        "market_desc": "AI-estimated mandi rates based on current season, state arrivals & market demand",
        "select_state": "🌍 Select Your State",
        "select_crop": "🌾 Select Crop",
        "get_prices": "📊 Get Live Mandi Prices",
        "price_loading": "⏳ Fetching latest market intelligence...",

        # Cost Tab
        "cost_title": "💰 Farm Cost & Profit Calculator",
        "cost_desc": "Estimate your farming investment, expected yield & potential net profit",
        "input_crop": "🌾 Crop Name",
        "input_area": "📐 Farm Area (acres)",
        "input_season": "🗓️ Season",
        "seasons": ["Kharif (Monsoon)", "Rabi (Winter)", "Zaid (Summer)"],
        "calculate": "💰 Calculate Profit Estimate",
        "cost_loading": "⏳ Calculating farm investment and profit forecast...",

        "states": [
            "Andhra Pradesh", "Telangana", "Karnataka", "Tamil Nadu",
            "Maharashtra", "Madhya Pradesh", "Uttar Pradesh", "Punjab",
            "Haryana", "Rajasthan", "Gujarat", "Bihar",
            "West Bengal", "Odisha", "Kerala", "Assam"
        ],
        "crops": [
            "Rice (Paddy)", "Wheat", "Maize (Corn)", "Cotton",
            "Sugarcane", "Soybean", "Groundnut", "Tomato",
            "Onion", "Potato", "Chilli", "Turmeric",
            "Banana", "Mango", "Sunflower", "Jowar (Sorghum)"
        ],
    },
    "te": {
        "page_title": "📊 లైవ్ మార్కెట్ ధరలు & వ్యవసాయ వ్యయ అంచనా",
        "page_subtitle": "తాజా పంట ధరలు, మండి సమాచారం & లాభాల గణన",
        "tab_market": "📈 లైవ్ మార్కెట్ ధరలు",
        "tab_cost": "💰 వ్యవసాయ వ్యయ & లాభ అంచనా",
        "gov_banner_title": "🏛️ ప్రభుత్వ వ్యవసాయ పథకాలు & సబ్సిడీలు కావాలా?",
        "gov_banner_desc": "PM-కిసాన్, పంట బీమా, సోలార్ పంపులు & రాష్ట్ర సంక్షేమ పథకాలను మా ప్రత్యేక పోర్టల్‌లో చూడండి.",
        "gov_banner_btn": "ప్రభుత్వ పథకాల పోర్టల్‌కు వెళ్లండి ➔",

        "market_title": "📈 నేటి పంట మండి ధరల అంచనా",
        "market_desc": "ప్రస్తుత సీజన్, ప్రాంతం & డిమాండ్ ఆధారంగా AI అంచనా ధరలు",
        "select_state": "🌍 మీ రాష్ట్రం ఎంచుకోండి",
        "select_crop": "🌾 పంట ఎంచుకోండి",
        "get_prices": "📊 మార్కెట్ ధరలు చూడండి",
        "price_loading": "⏳ తాజా మార్కెట్ సమాచారం తెస్తున్నాము...",

        "cost_title": "💰 వ్యవసాయ ఖర్చులు & లాభాల కాలిక్యులేటర్",
        "cost_desc": "మీ పెట్టుబడి, ఊహించిన దిగుబడి & లాభాన్ని సులభంగా లెక్కించండి",
        "input_crop": "🌾 పంట పేరు",
        "input_area": "📐 పొలం విస్తీర్ణం (ఎకరాలు)",
        "input_season": "🗓️ సీజన్",
        "seasons": ["ఖరీఫ్ (వర్షాకాలం)", "రబీ (శీతాకాలం)", "జైద్ (వేసవి)"],
        "calculate": "💰 లాభం లెక్కించండి",
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
        "page_title": "📊 लाइव मंडी भाव और खेती लागत अनुमान",
        "page_subtitle": "ताज़ा फसल भाव, मंडी इंटेलिजेंस और संभावित मुनाफा कैलकुलेटर",
        "tab_market": "📈 लाइव मंडी भाव",
        "tab_cost": "💰 खेती लागत और मुनाफा कैलकुलेटर",
        "gov_banner_title": "🏛️ क्या आपको सरकारी कृषि योजनाएं और सब्सिडी चाहिए?",
        "gov_banner_desc": "पीएम-किसान, फसल बीमा, सोलर पंप और राज्य अनुदान योजनाओं के लिए समर्पित पोर्टल देखें।",
        "gov_banner_btn": "सरकारी योजनाएं पोर्टल पर जाएं ➔",

        "market_title": "📈 आज के अनुमानित मंडी फसल भाव",
        "market_desc": "वर्तमान सीजन, आवक और मांग के आधार पर AI अनुमानित मंडी दरें",
        "select_state": "🌍 अपना राज्य चुनें",
        "select_crop": "🌾 फसल चुनें",
        "get_prices": "📊 मंडी भाव देखें",
        "price_loading": "⏳ ताज़ा मंडी जानकारी लाई जा रही है...",

        "cost_title": "💰 खेती लागत और लाभ कैलकुलेटर",
        "cost_desc": "खेती का निवेश, अनुमानित उपज और शुद्ध लाभ का सटीक हिसाब लगाएं",
        "input_crop": "🌾 फसल का नाम",
        "input_area": "📐 खेत का क्षेत्रफल (एकड़)",
        "input_season": "🗓️ मौसम",
        "seasons": ["खरीफ (बरसात)", "रबी (सर्दी)", "जायद (गर्मी)"],
        "calculate": "💰 मुनाफे का अनुमान लगाएं",
        "cost_loading": "⏳ खेती लागत और मुनाफा अनुमान निकाला जा रहा है...",

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
        "page_title": "📊 நேரலை சந்தை விலை & பண்ணை செலவு மதிப்பீடு",
        "page_subtitle": "பயிர் சந்தை நிலவரம், விலை போக்குகள் மற்றும் லாப கணக்கீடு",
        "tab_market": "📈 நேரலை சந்தை விலைகள்",
        "tab_cost": "💰 பண்ணை செலவு & லாப கால்குலேட்டர்",
        "gov_banner_title": "🏛️ அரசு திட்டங்கள் மற்றும் மானியங்கள் வேண்டுமா?",
        "gov_banner_desc": "பிஎம்-கிசான், பயிர் காப்பீடு, சோலார் பம்புகள் மற்றும் அரசு திட்டங்களை எங்கள் தனி போர்ட்டலில் காண்க.",
        "gov_banner_btn": "அரசு திட்டங்கள் போர்ட்டலுக்கு செல்லவும் ➔",

        "market_title": "📈 இன்றைய உத்தேச சந்தை விலைகள்",
        "market_desc": "பருவகாலம் மற்றும் தேவைக்கேற்ப AI மதிப்பீடு செய்த சந்தை விலைகள்",
        "select_state": "🌍 உங்கள் மாநிலம்",
        "select_crop": "🌾 பயிர்",
        "get_prices": "📊 சந்தை விலையை காண்க",
        "price_loading": "⏳ சந்தை தகவல் பெறப்படுகிறது...",

        "cost_title": "💰 விவசாய முதலீடு மற்றும் லாப கணக்கீடு",
        "cost_desc": "உங்கள் முதலீடு மற்றும் எதிர்பார்க்கப்படும் நிகர லாபத்தை மதிப்பிடுங்கள்",
        "input_crop": "🌾 பயிர் பெயர்",
        "input_area": "📐 பண்ணை பரப்பு (ஏக்கர்)",
        "input_season": "🗓️ பருவம்",
        "seasons": ["காரீப் (மழைக்காலம்)", "ரபி (குளிர்காலம்)", "கோடை"],
        "calculate": "💰 லாபம் கணக்கிடவும்",
        "cost_loading": "⏳ மதிப்பீடு கணக்கிடப்படுகிறது...",

        "states": ["Tamil Nadu", "Andhra Pradesh", "Telangana", "Karnataka", "Kerala", "Maharashtra"],
        "crops": ["Rice (Paddy)", "Cotton", "Sugarcane", "Banana", "Tomato", "Chilli", "Turmeric", "Groundnut"],
    },
    "kn": {
        "page_title": "📊 ಲೈವ್ ಮಾರುಕಟ್ಟೆ ದರಗಳು & ಕೃಷಿ ವೆಚ್ಚ ಅಂದಾಜು",
        "page_subtitle": "ನೈಜ ಬೆಳೆ ಮಾರುಕಟ್ಟೆ ದರಗಳು ಮತ್ತು ನಿವ್ವಳ ಲಾಭದ ಲೆಕ್ಕಾಚಾರ",
        "tab_market": "📈 ಲೈವ್ ಮಾರುಕಟ್ಟೆ ದರಗಳು",
        "tab_cost": "💰 ಕೃಷಿ ವೆಚ್ಚ & ಲಾಭದ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
        "gov_banner_title": "🏛️ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು ಮತ್ತು ಸಬ್ಸಿಡಿಗಳು ಬೇಕೇ?",
        "gov_banner_desc": "ಪ್ರಧಾನ ಮಂತ್ರಿ ಕಿಸಾನ್, ಬೆಳೆ ವಿಮೆ ಮತ್ತು ಸೌರ ಪಂಪ್ ಯೋಜನೆಗಳನ್ನು ಪ್ರತ್ಯೇಕ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ವೀಕ್ಷಿಸಿ.",
        "gov_banner_btn": "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ಪೋರ್ಟಲ್‌ಗೆ ಹೋಗಿ ➔",

        "market_title": "📈 ಇಂದಿನ ಅಂದಾಜು ಎಪಿಎಂಸಿ ಮಾರುಕಟ್ಟೆ ದರಗಳು",
        "market_desc": "ಪ್ರಸ್ತುತ ಋತುಮಾನ ಮತ್ತು ಬೇಡಿಕೆಯ ಆಧಾರದ ಮೇಲೆ AI ಅಂದಾಜು ಬೆಲೆಗಳು",
        "select_state": "🌍 ರಾಜ್ಯ ಆಯ್ಕೆಮಾಡಿ",
        "select_crop": "🌾 ಬೆಳೆ ಆಯ್ಕೆಮಾಡಿ",
        "get_prices": "📊 ಮಾರುಕಟ್ಟೆ ಬೆಲೆ ವೀಕ್ಷಿಸಿ",
        "price_loading": "⏳ ಮಾರುಕಟ್ಟೆ ಮಾಹಿತಿ ಪಡೆಯಲಾಗುತ್ತಿದೆ...",

        "cost_title": "💰 ಕೃಷಿ ಹೂಡಿಕೆ ಮತ್ತು ಲಾಭದ ಅಂದಾಜು",
        "cost_desc": "ಖರ್ಚುಗಳು ಮತ್ತು ನಿರೀಕ್ಷಿತ ಲಾಭವನ್ನು ಸರಳವಾಗಿ ಲೆಕ್ಕಹಾಕಿ",
        "input_crop": "🌾 ಬೆಳೆ ಹೆಸರು",
        "input_area": "📐 ಜಮೀನಿನ ವಿಸ್ತೀರ್ಣ (ಎಕರೆ)",
        "input_season": "🗓️ ಋತು",
        "seasons": ["ಖಾರೀಫ್", "ರಬಿ", "ಬೇಸಿಗೆ"],
        "calculate": "💰 ಲಾಭ ಲೆಕ್ಕಿಸಿ",
        "cost_loading": "⏳ ವೆಚ್ಚ ಮತ್ತು ಲಾಭ ಲೆಕ್ಕಿಸಲಾಗುತ್ತಿದೆ...",

        "states": ["Karnataka", "Andhra Pradesh", "Telangana", "Tamil Nadu", "Maharashtra"],
        "crops": ["Rice (Paddy)", "Maize (Corn)", "Cotton", "Sugarcane", "Jowar (Sorghum)", "Tomato", "Onion"],
    },
    "mr": {
        "page_title": "📊 थेट बाजार भाव आणि शेती खर्च अंदाज",
        "page_subtitle": "बाजार भाव, आवक माहिती आणि नफा कॅल्क्युलेटर",
        "tab_market": "📈 थेट बाजार भाव",
        "tab_cost": "💰 शेती खर्च व नफा कॅल्क्युलेटर",
        "gov_banner_title": "🏛️ शासकीय कृषी योजना आणि अनुदान हवे आहे का?",
        "gov_banner_desc": "पीएम-किसान, पीक विमा आणि सोलर पंप योजनांसाठी समर्पित पोर्टल पहा.",
        "gov_banner_btn": "शासकीय योजना पोर्टलवर जा ➔",

        "market_title": "📈 आजचे अंदाजित कृषी उत्पन्न बाजार भाव",
        "market_desc": "सध्याचा हंगाम व आवक यावर आधारित AI अंदाजित दर",
        "select_state": "🌍 राज्य निवडा",
        "select_crop": "🌾 पीक निवडा",
        "get_prices": "📊 बाजार भाव पहा",
        "price_loading": "⏳ ताज्या बाजार माहिती आणत आहोत...",

        "cost_title": "💰 शेती खर्च आणि नफा अंदाज",
        "cost_desc": "गुंतवणूक आणि संभाव्य नफ्याचा अचूक अंदाज लावा",
        "input_crop": "🌾 पिकाचे नाव",
        "input_area": "📐 शेत क्षेत्र (एकर)",
        "input_season": "🗓️ हंगाम",
        "seasons": ["खरीप", "रब्बी", "उन्हाळी"],
        "calculate": "💰 नफा अंदाज काढा",
        "cost_loading": "⏳ खर्च आणि नफा अंदाज काढत आहोत...",

        "states": ["Maharashtra", "Madhya Pradesh", "Gujarat", "Karnataka", "Telangana", "Andhra Pradesh"],
        "crops": ["Soybean", "Cotton", "Sugarcane", "Onion", "Tomato", "Wheat", "Gram (Chana)", "Banana"],
    }
}


# =========================================================
# MAIN FUNCTION
# =========================================================

def show_market_policy():
    """Renders the standalone Live Market Prices & Farm Cost Estimator page."""

    farmer = st.session_state.get("farmer", {})
    farmer_id = farmer.get("id", 1)
    current_lang = st.session_state.get("selected_language", "English")

    lang_map = {"English": "en", "తెలుగు": "te", "हिंदी": "hi", "தமிழ்": "ta", "ಕನ್ನಡ": "kn", "मराठी": "mr"}
    lang_code = lang_map.get(current_lang, "en")
    t = MARKET_TEXT.get(lang_code, MARKET_TEXT["en"])

    # 1. Page Header Card
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #1e3a5f 0%, #1e40af 60%, #3b82f6 100%); border-radius: 20px; padding: 22px 24px; margin-bottom: 16px; box-shadow: 0 8px 24px rgba(30, 64, 175, 0.25);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div>
                    <span style="background: rgba(255,255,255,0.20); color: #ffffff; padding: 3px 10px; border-radius: 9999px; font-size: 11px; font-weight: 700; border: 1px solid rgba(255,255,255,0.35);">
                        📈 Mandi Rates & Farm Economics
                    </span>
                    <h1 style="color: white !important; margin: 8px 0 4px 0; font-size: 24px; font-weight: 800;">{t['page_title']}</h1>
                    <p style="color: #bfdbfe; margin: 0; font-size: 13px; font-weight: 500;">{t['page_subtitle']}</p>
                </div>
                <div style="font-size: 40px;">📊</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. Government Schemes Direct Shortcut Banner
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%); border: 1.5px solid #86efac; border-radius: 14px; padding: 14px 18px; margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <div style="font-weight: 800; font-size: 15px; color: #166534;">
                    {t['gov_banner_title']}
                </div>
                <div style="font-size: 12px; color: #334155; margin-top: 2px;">
                    {t['gov_banner_desc']}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button(t['gov_banner_btn'], key="btn_jump_to_gov_schemes", use_container_width=True):
        st.session_state.page = "gov_schemes"
        st.rerun()

    # 3. Two Dedicated Tabs: Live Mandi Rates | Farming Cost Estimator
    tab_market, tab_cost = st.tabs([
        t["tab_market"],
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

        # Quick price guidance card
        st.markdown("---")
        st.markdown(
            f"""
            <div style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 14px; padding: 16px; margin: 8px 0;">
                <div style="font-size: 14px; font-weight: 700; color: #0f172a; margin-bottom: 6px;">
                    💡 Smart Mandi Selling Tips:
                </div>
                <ul style="margin: 0; padding-left: 20px; font-size: 13px; color: #475569; line-height: 1.6;">
                    <li>Always check MSP (Minimum Support Price) before selling at private mandis.</li>
                    <li>Grade and clean your produce to get 10-15% higher modal price.</li>
                    <li>Utilize e-NAM (National Agriculture Market) for inter-state trading.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -------------------------------------------------
    # TAB 2: COST ESTIMATOR
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
