import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Setup API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key missing!")

model = genai.GenerativeModel('gemini-3-flash-preview')

st.set_page_config(page_title="ICT Trade Coach", layout="wide")
st.title("📊 ICT Trade Journal & Interactive Coach")

# 2. Initialize Chat History in Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

# Sidebar
with st.sidebar:
    st.header("Trade Metadata")
    instrument = st.selectbox("Instrument", ["NQ", "GC", "ES"])
    session = st.radio("Session", ["AM Silver Bullet", "PM Silver Bullet", "London"])
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.analysis_done = False

# 3. Main Analysis Section
uploaded_file = st.file_uploader("Upload chart screenshot...", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, use_container_width=True)
    
    if st.button("Analyze Setup"):
        with st.spinner("Analyzing..."):
            prompt = f"Act as an ICT mentor. Analyze this {instrument} {session} setup for liquidity sweeps, MSS, and Unicorn models. Flag any fakeouts."
            response = model.generate_content([prompt, img])
            
            # Save the initial analysis to history
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            st.session_state.analysis_done = True

# 4. Follow-up Chat UI
if st.session_state.analysis_done:
    st.divider()
    st.subheader("💬 Chat with your ICT Coach")
    
    # Display previous messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input for follow-ups
    if prompt := st.chat_input("Ask a follow-up about this trade..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Get AI response based on full history + the image
        with st.chat_message("assistant"):
            # We send the image again so the AI can "see" what you're asking about
            full_context = f"Based on the chart provided and our previous discussion: {prompt}"
            response = model.generate_content([full_context, img])
            st.markdown(response.text)
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
