import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. Setup Gemini API using Streamlit Secrets
# This is more secure than hard-coding your key
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Please add your GOOGLE_API_KEY to Streamlit Secrets.")

model = genai.GenerativeModel('gemini-3-flash-preview')

st.set_page_config(page_title="ICT Trade Journal", layout="wide")

st.title("📊 ICT Visual Trade Journal")

# 2. Sidebar for Stats & Notes
with st.sidebar:
    st.header("Trade Details")
    trade_date = st.date_input("Trade Date")
    instrument = st.selectbox("Instrument", ["NQ (Nasdaq)", "GC (Gold)", "ES (S&P 500)"])
    session = st.radio("Session", ["AM Silver Bullet", "PM Silver Bullet", "London"])
    user_notes = st.text_area("Why did you take this trade?", placeholder="Describe your bias...")

# 3. Main Upload Area
uploaded_file = st.file_uploader("Drop your chart screenshot here...", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Current Setup", use_container_width=True)
    
    if st.button("Analyze with Gemini"):
        with st.spinner("Analyzing price action..."):
            prompt = f"""
            Analyze this trading chart based on ICT (Inner Circle Trader) concepts:
            1. Identify if there was a Liquidity Sweep (buy/sell side) prior to the entry.
            2. Locate any Market Structure Shift (MSS).
            3. Check for a 'Unicorn Model': Is there a Breaker Block overlapping with a Fair Value Gap (FVG)?
            4. Verify if this occurred during the {session} window.
            5. Final Verdict: Grade this setup (A, B, or C) based on ICT high-probability rules.
            """
            response = model.generate_content([prompt, img])
            st.subheader("AI Strategy Analysis")
            st.markdown(response.text)
