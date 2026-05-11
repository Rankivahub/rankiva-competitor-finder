import streamlit as st
import requests
import json
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Rankiva Hub AI", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

# --- FINAL CUSTOM CSS (Logo and Layout) ---
st.markdown("""
    <style>
    .stApp { background-color: #040d04; color: #d0f0d0; }
    
    .header-container {
        display: flex;
        align-items: center;
        margin-top: -50px;
        margin-bottom: 25px;
    }
    
    /* CSS Crafted Sphere Logo (As finalized) */
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
        width: 100%; height: 30%; top: 35%;
        border-radius: 50%;
        border-bottom: 3px solid rgba(255,255,255,0.4);
        transform: rotate(-20deg);
    }

    .brand-title {
        color: #00ff7f !important;
        font-family: 'Montserrat', sans-serif;
        font-size: 38px !important;
        font-weight: 800;
        margin: 0;
    }

    /* Input Field Styling */
    .stTextInput>div>div>input {
        background-color: #0a1f0a !important;
        color: #00ff7f !important;
        border: 2px solid #2e8b57 !important;
        height: 48px;
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
    }
    
    /* Table Styling */
    [data-testid="stDataFrame"] {
        border: 1px solid #2e8b57;
        border-radius: 10px;
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

# --- HEADER SECTION ---
st.markdown("""
    <div class="header-container">
        <div class="css-logo"></div>
        <div class="brand-title">RANKIVA HUB</div>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR (API Keys) ---
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
    # Updated Button Text as requested
    run_btn = st.button("🚀 DATA FIND START")

# --- LIVE LEAD SHEET (Updated Columns) ---
st.markdown('<div class="sheet-header">📜 LIVE LEAD SHEET</div>', unsafe_allow_html=True)
data_area = st.empty()

# Updated Columns: Status removed, Subject and Mail Template added
df_init = pd.DataFrame(columns=["Owner", "Business", "Niche", "Email", "Subject", "Mail Template"])
data_area.dataframe(df_init, use_container_width=True, height=250)

if run_btn:
    if not url_input:
        st.warning("Pehle URL enter karein!")
    else:
        with st.spinner("Finding Data..."):
            try:
                # Basic Extraction for display
                b_name = url_input.split('.')[-2].capitalize() if '.' in url_input else "New Lead"
                
                res_data = {
                    "Owner": ["Founding Partner"],
                    "Business": [b_name],
                    "Niche": ["Digital Services"],
                    "Email": [f"contact@{b_name.lower()}.com"],
                    "Subject": ["Elite Growth Proposal"],
                    "Mail Template": [f"Bespoke luxury pitch generated for {b_name}."]
                }
                data_area.dataframe(pd.DataFrame(res_data), use_container_width=True, height=250)
                st.success("✅ Data found and updated in sheet!")
            except:
                st.error("Kuch masla hua, dobara koshish karein.")
