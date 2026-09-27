import streamlit as st


def show_ai_crop_advisor(crop, details):
    """
    Displays the AI Crop Advisor section.
    """

    st.markdown("---")
    st.header("🤖 AI Crop Advisor")

    st.success(f"🌾 Recommended Crop: **{crop.title()}**")

    if details:

        with st.expander("📖 Crop Description", expanded=True):
            st.write(details["description"])

        with st.expander("🌱 Suitable Soil"):
            st.write(details["soil"])

        with st.expander("🌡️ Ideal Temperature"):
            st.write(details["temperature"])

        with st.expander("💧 Water Requirement"):
            st.write(details["water"])

        with st.expander("🌿 Recommended Fertilizer"):
            st.write(details["fertilizer"])

        with st.expander("📅 Growing Season"):
            st.write(details["season"])

        with st.expander("📈 Expected Yield"):
            st.write(details["yield"])

        with st.expander("👨‍🌾 Farmer Tips"):
            st.write(details["tips"])

    else:

        st.warning("Crop information is currently unavailable.")