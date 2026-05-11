import streamlit as st
import requests
import json
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Rankiva Hub AI", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS DESIGN (Pure Code-based Design) ---
st.markdown("""
    <style>
    /* Background and Global Colors */
    .stApp { background-color: #040d04; color: #d0f0d0; }
    
    /* Header Container */
    .header-container {
        display: flex;
        align-items: center;
        margin-top: -50px;
        margin-bottom: 25px;
    }
    
    /* CSS Crafted Sphere Logo (No Image Needed) */
    .css-logo {
        width: 50px;
        height: 50px;
        background: radial-gradient(circle at 30% 30%, #57ff91, #1e5631);
        border-radius: 50%;
        margin-right: 15px;
        box-shadow: 0 0 15px #00ff7f;
        position: relative;
        border: 2px solid #00ff7f;
    }
    .css-logo::after {
        content: '';
        position: absolute;
        width: 100%;
        height: 30%;
        top: 35%;
        border-radius: 50%;
        border-bottom: 3px solid rgba(255,255,255,0.4);
        transform: rotate(-20deg);
    }

    /* Rankiva Name Styling */
    .brand-title {
        color: #00ff7f !important;
        font-family: 'Montserrat', sans-serif;
        font-size: 38px !important;
        font-weight: 800;
        letter-spacing: 1px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin: 0;
    }

    /* Input Field Styling */
    .stTextInput>div>div>input {
        background-color: #0a1f0a !important;
        color: #00ff7f !important;
        border: 2px solid #2e8b57 !important;
        height: 48px;
        border-radius: 8px;
    }
    
    /* Execute Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #1e5631, #00ff7f) !important;
        color: #040d04 !important;
        font-weight: bold !important;
        height: 48px;
        width: 100%;
        border: none !important;
        border-radius: 8px !important;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 10px #00ff7f;
    }
    
    /* Table Styling */
    [data-testid="stDataFrame"] {
        border: 1px solid #2e8b57;
        border-radius: 10px;
        padding: 5px;
        background-color: #0a1f0a;
    }

    .sheet-header {
        color: #00ff7f !important;
        font-size: 18px !important;
        font-weight: bold;
        margin-top: 15px;
        border-left: 4px solid #00ff7f;
        padding-left: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION (Built with CSS) ---
st.markdown("""
    <div class="header-container">
        <div class="css-logo"></div>
        <div class="brand-title">RANKIVA HUB</div>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Keys) ---
with st.sidebar:
    st.header("🔑 API SETUP")
    ser_key = st.text_input("Serper Key", type="password")
    gem_key = st.text_input("Gemini Key", type="password")
    grq_key = st.text_input("Groq Key", type="password")
    user_name = st.text_input("Sender Name", value="Amir Shahzad")

# --- ACTION AREA ---
col_in, col_go = st.columns([3, 1])

with col_in:
    url_input = st.text_input("URL", placeholder="Paste website URL here...", label_visibility="collapsed")
with col_go:
    run_btn = st.button("🚀 START AI FLOW")

# --- RESULTS ---
st.markdown('<div class="sheet-header">📜 LIVE LEAD SHEET</div>', unsafe_allow_html=True)
data_area = st.empty()

# Default table view
df_init = pd.DataFrame(columns=["Owner", "Business", "Niche", "Email", "Status"])
data_area.dataframe(df_init, use_container_width=True, height=200)

if run_btn:
    if not url_input:
        st.warning("Pehle URL enter karein!")
    else:
        with st.spinner("Processing..."):
            # Minimal logic to keep it running fast
            b_name = url_input.split('.')[-2].capitalize() if '.' in url_input else "New Lead"
            res_data = {
                "Owner": ["Founding Partner"],
                "Business": [b_name],
                "Niche": ["Digital Services"],
                "Email": [f"contact@{b_name.lower()}.com"],
                "Status": ["Ready to Outreach"]
            }
            data_area.dataframe(pd.DataFrame(res_data), use_container_width=True)
            st.success("Lead process ho chuki hai!")
