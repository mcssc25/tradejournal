import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. Setup Gemini API using Streamlit Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key missing! Add GOOGLE_API_KEY to your Streamlit Secrets.")

# Using the stable 2026 model
model = genai.GenerativeModel('gemini-3-flash-preview')

st.set_page_config(page_title="ICT Trade Journal & Fakeout Detector", layout="wide")

st.title("📊 ICT Trade Journal: Fakeout Detector")
st.write("Upload your NQ/GC screenshot to analyze if a move is a high-probability setup or a trap.")

# 2. Sidebar for Trade Metadata
with st.sidebar:
    st.header("Trade Log")
    instrument = st.selectbox("Instrument", ["NQ (Nasdaq)", "GC (Gold)", "ES (S&P 500)"])
    session = st.radio("Session", ["AM Silver Bullet (10-11am)", "PM Silver Bullet (2-3pm)", "London"])
    user_notes = st.text_area("Your initial thoughts on this trade:")

# 3. Image Upload
uploaded_file = st.file_uploader("Drop your chart screenshot here...", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Analyzing this setup...", use_container_width=True)
    
    if st.button("Run Fakeout Analysis"):
        with st.spinner("Scanning for Smart Money signatures..."):
            # The Updated "Fakeout-Aware" Prompt
            prompt = f"""
            Act as an elite ICT (Inner Circle Trader) mentor. Analyze this {instrument} chart during the {session}.
            
            Focus specifically on identifying 'Fake Outs' vs. 'Valid Entries':
            
            1. LIQUIDITY ANALYSIS: Was there a clear sweep of Sell-Side or Buy-Side liquidity BEFORE the MSS? 
               (If no sweep occurred, flag this as a potential low-probability 'inducement' move).
            2. DISPLACEMENT CHECK: Did the Market Structure Shift (MSS) happen with energetic, full-bodied candles? 
               (If the break was made only by wicks or small, hesitant candles, identify it as a Fake Out).
            3. UNICORN VALIDATION: Look for a Breaker Block overlapping a Fair Value Gap (FVG). 
               Did the price respect the FVG, or did it slice through it immediately (Inversion)?
            
            FINAL VERDICT:
            - Provide a Grade (A, B, or C).
            - Explicitly state: "VALID SETUP" or "POTENTIAL FAKEOUT".
            - Explain WHY the first MSS on the chart might have failed if it was a trap.
            """
            
            response = model.generate_content([prompt, img])
            
            st.subheader("🕵️ AI Strategy Breakdown")
            st.markdown(response.text)
            
            st.info("Tip: If the AI mentions 'Turtle Soup,' it means a liquidity grab occurred without a real trend change.")
