import streamlit as st

from database.farmers import get_or_create_farmer


def show_login():

    st.markdown(
        """
        <div class="agri-hero" style="text-align: center; padding: 32px 20px;">
            <span style="font-size: 48px; display: block; margin-bottom: 6px;">🌱</span>
            <h1 style="color: #ffffff !important; font-size: 32px; font-weight: 800; margin: 0 0 6px 0;">AgriSense AI</h1>
            <p style="color: #dcfce7 !important; font-size: 16px; margin: 0;">Smart Agricultural Decision Support & Live AI Assistant</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="agri-card" style="padding: 24px; margin-top: -10px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 16px;">
                <span style="font-size: 26px;">👨‍🌾</span>
                <div>
                    <div style="font-weight: 800; font-size: 18px; color: #0f172a;">Farmer Login / Registration</div>
                    <div style="font-size: 13px; color: #64748b;">Enter your details to access personalized farm recommendations</div>
                </div>
            </div>
        """,
        unsafe_allow_html=True
    )

    name = st.text_input(
        "👤 Farmer Name",
        placeholder="e.g. Ramesh Kumar"
    )

    phone = st.text_input(
        "📱 Mobile Number",
        placeholder="e.g. 9876543210"
    )

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    if st.button(
        "🚜 Enter Dashboard",
        use_container_width=True
    ):

        name = name.strip()
        phone = phone.strip()

        if not name:
            st.warning("⚠️ Please enter your name.")
            return

        if not phone.isdigit() or len(phone) != 10:
            st.warning(
                "⚠️ Please enter a valid 10-digit mobile number."
            )
            return

        farmer = get_or_create_farmer(
            name,
            phone
        )

        st.session_state.farmer = farmer

        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)