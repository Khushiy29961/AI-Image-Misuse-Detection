import streamlit as st
import google.generativeai as genai
from PIL import Image
import os, hashlib, requests
from io import BytesIO
from dotenv import load_dotenv
from utils.protector import generate_dna_fingerprint
from utils.detector import perform_forensic_audit
# 1. SETUP
# --- STEP 1: INITIALIZE ENVIRONMENT ---
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# --- STEP 2: SECURITY CHECK ---
if not API_KEY:
    st.error("❌ API Key Missing: Please check your .env file and ensure it says GOOGLE_API_KEY=your_key")
    st.stop()
else:
    genai.configure(api_key=API_KEY)

# --- STEP 3: UI CONFIGURATION ---
st.set_page_config(page_title="AI Shield Lab", layout="wide")

# 2. SIDEBAR
with st.sidebar:
    st.title("🛡️ AI Security Hub")
    st.subheader("Lead: Khushi Yadav")
    st.info("🛡️ AI Shield Lab: Next-Gen Digital Forensics")
    if st.button("🔄 Reset System"):
        st.rerun()

# 3. MAIN UI
st.title("🛡️ Image Security & Misuse Detection")
tab1, tab2 = st.tabs(["🔒 Shield & Fingerprint", "🔍 Forensic Audit"])

with tab1:
    st.header("Shield Your Image")
    shield_file = st.file_uploader("Upload original image...", type=["jpg", "png"])
    if shield_file:
        img = Image.open(shield_file)
        st.image(img, width=300)
        if st.button("Generate DNA Fingerprint", type="primary"):
            fingerprint = hashlib.sha256(img.tobytes()).hexdigest()
            st.code(f"ID: {fingerprint}")

with tab2:
    st.header("Social Media Forensic Audit")
    source = st.radio("Evidence Source:", ["Upload File", "Web URL"])
    audit_img = None

    if source == "Upload File":
        file = st.file_uploader("Upload evidence...")
        if file:
            audit_img = Image.open(file)
    else:
        url = st.text_input("Paste Image URL:")
        if url:
            try:
                res = requests.get(url)
                audit_img = Image.open(BytesIO(res.content))
            except:
                st.error("Failed to fetch image.")

    if audit_img:
        col1, col2 = st.columns(2)
        with col1:
            st.image(audit_img, caption="Evidence Found", use_container_width=True)
            if st.button("🔍 Run AI Forensic Scan", type="primary"):
                # Indented everything inside this button block
                st.write("Checking available models...")
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        st.write(f"Found: {m.name}")
                
                # After checking, we use the specific model version
                model = genai.GenerativeModel('gemini-3-flash-preview')
                prompt = "Analyze this image for AI edits, face-swaps, or context manipulation. Provide a risk report."
                response = model.generate_content([prompt, audit_img])
                st.session_state.report = response.text
        
        with col2:
            if "report" in st.session_state:
                st.subheader("Forensic Report")
                st.info(st.session_state.report)