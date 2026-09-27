import streamlit as st
import os
from database.farmers import get_or_create_farmer


def show_login():
    # -------------------------------------------------------------
    # 1. AGRICULTURAL HERO BANNER WITH BACKGROUND ILLUMINATION
    # -------------------------------------------------------------
    st.markdown(
        """
        <style>
        .login-hero-container {
            background: linear-gradient(135deg, rgba(20, 83, 45, 0.92) 0%, rgba(22, 101, 52, 0.90) 50%, rgba(21, 128, 61, 0.92) 100%), 
                        url('https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=1200&q=80') center/cover no-repeat;
            border-radius: 20px;
            padding: 36px 24px 28px 24px;
            text-align: center;
            color: #ffffff;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px -5px rgba(20, 83, 45, 0.4);
            border: 2px solid rgba(255, 255, 255, 0.2);
        }
        .crop-badge-card {
            background: #ffffff;
            border: 1.5px solid #e2e8f0;
            border-radius: 14px;
            padding: 8px;
            text-align: center;
            transition: all 0.2s ease;
            box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        }
        .crop-badge-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 14px rgba(22, 163, 74, 0.2);
            border-color: #22c55e;
        }
        </style>

        <div class="login-hero-container">
            <span style="font-size: 52px; display: block; margin-bottom: 6px; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));">🌱</span>
            <h1 style="color: #ffffff !important; font-size: 34px !important; font-weight: 800; margin: 0 0 6px 0; letter-spacing: -0.5px;">
                AgriSense AI
            </h1>
            <p style="color: #dcfce7 !important; font-size: 16px; font-weight: 600; margin: 0 0 12px 0;">
                రైతుల కోసం స్మార్ట్ వ్యవసాయ సహాయకుడు • AI Agricultural Decision Platform
            </p>
            <div style="display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;">
                <span style="background: rgba(255,255,255,0.2); color: #ffffff; padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 700; border: 1px solid rgba(255,255,255,0.3);">
                    🎙️ వాయిస్ అసిస్టెంట్ (Voice AI)
                </span>
                <span style="background: rgba(255,255,255,0.2); color: #ffffff; padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 700; border: 1px solid rgba(255,255,255,0.3);">
                    🌾 పంట సిఫార్సు (Crop Predictor)
                </span>
                <span style="background: rgba(255,255,255,0.2); color: #ffffff; padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 700; border: 1px solid rgba(255,255,255,0.3);">
                    📡 ESP32 Live IoT
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -------------------------------------------------------------
    # 2. FARMER LOGIN CARD
    # -------------------------------------------------------------
    with st.container(border=True):
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <div style="width: 44px; height: 44px; border-radius: 12px; background: #15803d; color: white; display: flex; align-items: center; justify-content: center; font-size: 24px;">
                    👨‍🌾
                </div>
                <div>
                    <div style="font-weight: 800; font-size: 19px; color: #0f172a;">రైతు లాగిన్ / Farmer Login</div>
                    <div style="font-size: 13px; color: #64748b; font-weight: 600;">మీ పేరు మరియు ఫోన్ నంబర్ నమోదు చేయండి</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        name = st.text_input(
            "👤 Farmer Name / రైతు పేరు",
            placeholder="e.g. Praveen Reddy / రమేష్ కుమార్"
        )

        phone = st.text_input(
            "📱 Mobile Number / మొబైల్ నంబర్",
            placeholder="e.g. 7095984500"
        )

        st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

        if st.button("🚜 Enter Dashboard (డ్యాష్‌బోర్డ్ తెరవండి)", key="btn_login_enter", use_container_width=True):
            name = name.strip()
            phone = phone.strip()

            if not name:
                st.warning("⚠️ Please enter your name (దయచేసి మీ పేరు నమోదు చేయండి).")
                return

            if not phone.isdigit() or len(phone) != 10:
                st.warning("⚠️ Please enter a valid 10-digit mobile number (దయచేసి 10 అంకెల మొబైల్ నంబర్ ఇవ్వండి).")
                return

            farmer = get_or_create_farmer(name, phone)
            st.session_state.farmer = farmer
            st.rerun()

    # -------------------------------------------------------------
    # 3. VISUAL CROP SHOWCASE GALLERY FOR FARMERS
    # -------------------------------------------------------------
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 14px;">
            <h3 style="color: #0f172a; margin-bottom: 4px; font-size: 20px; font-weight: 800;">
                🌾 సిఫార్సు చేయగల ప్రధాన పంటలు • Supported Crops
            </h3>
            <p style="color: #64748b; font-size: 14px; margin: 0; font-weight: 600;">
                నేల పోషకాలు (NPK) మరియు వాతావరణం ఆధారంగా సరైన పంటను గుర్తిస్తుంది
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    gallery_crops = [
        ("rice", "వరి (Rice)", "images/rice.jpg"),
        ("maize", "మొక్కజొన్న (Maize)", "images/maize.jpg"),
        ("cotton", "హత్తి (Cotton)", "images/cotton.jpg"),
        ("banana", "అరటి (Banana)", "images/banana.jpg"),
        ("mango", "మామిడి (Mango)", "images/mango.jpg"),
        ("coffee", "కాఫీ (Coffee)", "images/coffee.jpg"),
    ]

    cols = st.columns(3)
    for i, (c_key, c_label, c_path) in enumerate(gallery_crops):
        col_idx = i % 3
        with cols[col_idx]:
            with st.container(border=True):
                if os.path.exists(c_path):
                    st.image(c_path, use_container_width=True)
                else:
                    st.markdown("<div style='font-size: 32px; text-align: center;'>🌾</div>", unsafe_allow_html=True)
                st.markdown(
                    f"<div style='text-align: center; font-weight: 800; font-size: 14px; color: #15803d; margin-top: 4px;'>{c_label}</div>",
                    unsafe_allow_html=True
                )