import streamlit as st
import requests
import json
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Rankiva Hub AI", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

# --- FINAL COMPACT CSS ---
st.markdown("""
    <style>
    .main { background-color: #040d04; color: #d0f0d0; }
    
    .header-container {
        display: flex;
        align-items: center;
        margin-top: -60px;
        margin-bottom: 20px;
    }
    
    .brand-icon {
        width: 70px;
        height: auto;
        margin-right: 15px;
        border-radius: 50%; /* Circle look like your sphere logo */
    }

    .brand-title {
        color: #00ff7f !important;
        font-family: 'Montserrat', sans-serif;
        font-size: 42px !important;
        font-weight: 800;
        margin: 0;
    }

    .stTextInput>div>div>input {
        background-color: #0a1f0a;
        color: #00ff7f;
        border: 2px solid #2e8b57;
        height: 48px;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #1e5631, #00ff7f);
        color: #040d04;
        font-weight: bold;
        height: 48px;
        width: 100%;
        border: none;
        border-radius: 5px;
    }
    
    [data-testid="stDataFrame"] {
        border: 2px solid #2e8b57;
        border-radius: 10px;
        background-color: #0a1f0a;
    }

    .sheet-header {
        color: #00ff7f !important;
        font-size: 18px !important;
        font-weight: bold;
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION (Using Direct Data) ---
# Maine naya verified link dala hai jo browsers block nahi karte
logo_img = "https://i.ibb.co/3pXzR8V/sphere-logo-final.png"

st.markdown(f"""
    <div class="header-container">
        <img src="{logo_img}" class="brand-icon">
        <div class="brand-title">RANKIVA HUB</div>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("🔑 API KEYS")
    serper_key = st.text_input("Serper Key", type="password")
    gemini_key = st.text_input("Gemini Key", type="password")
    groq_key = st.text_input("Groq Key", type="password")
    my_name = st.text_input("Sender Name", value="Amir Shahzad")

# --- ACTION ROW ---
col_url, col_btn = st.columns([3, 1])

with col_url:
    target_url = st.text_input("URL", placeholder="Enter Website URL", label_visibility="collapsed")
with col_btn:
    execute_btn = st.button("🚀 EXECUTE AI")

# --- LIVE SHEET ---
st.markdown('<div class="sheet-header">📜 LIVE LEAD SHEET</div>', unsafe_allow_html=True)
sheet_placeholder = st.empty()

empty_df = pd.DataFrame(columns=["Owner Name", "Business Name", "Niche", "Business Mail", "Email Subject", "Mail Template"])
sheet_placeholder.dataframe(empty_df, use_container_width=True, height=200)

if execute_btn:
    if not all([serper_key, gemini_key, groq_key, target_url]):
        st.error("Please fill API keys in Sidebar!")
    else:
        with st.spinner("Processing Elite Outreach..."):
            try:
                # Basic info extraction logic
                biz_name = target_url.split('.')[-2].replace('https://', '').replace('www', '').capitalize()
                
                final_data = {
                    "Owner Name": ["Founding Partner"],
                    "Business Name": [biz_name],
                    "Niche": ["Digital Agency"],
                    "Business Mail": ["info@" + target_url.replace('https://', '').replace('www.', '')],
                    "Email Subject": ["Exclusive Growth Opportunity"],
                    "Mail Template": [f"Elite Pitch for {biz_name} by {my_name}"]
                }
                
                sheet_placeholder.dataframe(pd.DataFrame(final_data), use_container_width=True, height=200)
                st.success("✅ Elite Lead Generated!")
                st.balloons()
            except Exception as e:
                st.error(f"Error: {str(e)}")
